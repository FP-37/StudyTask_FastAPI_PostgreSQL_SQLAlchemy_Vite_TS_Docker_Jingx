import { authApi } from "./client";

export type UserRead = {
  id: number;
  username: string;
  is_admin: boolean;
};

export async function register(username: string, password: string): Promise<UserRead> {
  const res = await authApi.post<UserRead>("/auth/register", { username, password });
  return res.data;
}

export async function login(username: string, password: string): Promise<{ access_token: string }> {
  const res = await authApi.post<{ access_token: string; token_type: string }>("/auth/login", {
    username,
    password,
  });
  return { access_token: res.data.access_token };
}

export async function me(): Promise<UserRead> {
  const res = await authApi.get<UserRead>("/auth/me");
  return res.data;
}
