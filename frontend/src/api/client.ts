import axios, { AxiosError } from "axios";

const TOKEN_KEY = "access_token";

const BUSLINES_BASE =
  import.meta.env.VITE_BUSLINES_URL ?? "http://127.0.0.1:8000";
const AUTH_BASE =
  import.meta.env.VITE_AUTH_URL ?? "http://127.0.0.1:8001";

export const buslinesApi = axios.create({
  baseURL: BUSLINES_BASE,
  timeout: 15000,
});

export const authApi = axios.create({
  baseURL: AUTH_BASE,
  timeout: 15000,
});

export function getAccessToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setAccessToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
  window.dispatchEvent(new Event("auth-changed"));
}

export function clearAccessToken(): void {
  localStorage.removeItem(TOKEN_KEY);
  window.dispatchEvent(new Event("auth-changed"));
}

// токен нужен и для /auth/me, и для /bus-lines/*
function attachAuthHeader(config: any) {
  const token = getAccessToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}

buslinesApi.interceptors.request.use(attachAuthHeader);
authApi.interceptors.request.use(attachAuthHeader);

function handle401(err: unknown) {
  if (axios.isAxiosError(err) && err.response?.status === 401) {
    clearAccessToken();
  }
  return Promise.reject(err);
}

buslinesApi.interceptors.response.use((res) => res, handle401);
authApi.interceptors.response.use((res) => res, handle401);

function formatFastApiDetail(detail: unknown): string | null {
  if (typeof detail === "string") return detail;

  if (Array.isArray(detail)) {
    const msgs = detail
      .map((x: any) => {
        const loc = Array.isArray(x?.loc) ? x.loc.join(".") : "";
        const msg = typeof x?.msg === "string" ? x.msg : "Validation error";
        return loc ? `${loc}: ${msg}` : msg;
      })
      .filter(Boolean);

    if (msgs.length) return msgs.join("; ");
  }

  return null;
}

export function getApiErrorMessage(
  err: unknown,
  fallback = "Ошибка запроса"
): string {
  if (axios.isAxiosError(err)) {
    const ax = err as AxiosError<any>;

    if (ax.response) {
      const data = ax.response.data;

      if (data && typeof data === "object" && "detail" in data) {
        const msg = formatFastApiDetail((data as any).detail);
        if (msg) return msg;
      }

      if (typeof data === "string" && data.trim()) return data;

      return `HTTP ${ax.response.status} ${ax.response.statusText}`.trim();
    }

    if (ax.code === "ECONNABORTED") return "Таймаут запроса";
    if (ax.message) return ax.message;

    return fallback;
  }

  if (err instanceof Error && err.message) return err.message;

  return fallback;
}