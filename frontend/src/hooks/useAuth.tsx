import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { clearAccessToken, getAccessToken, getApiErrorMessage, setAccessToken } from "../api/client";
import * as authApi from "../api/auth";

type AuthState = {
  user: authApi.UserRead | null;
  isReady: boolean;
  isAuthed: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshMe: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<authApi.UserRead | null>(null);
  const [isReady, setIsReady] = useState(false);

  async function refreshMe() {
    const token = getAccessToken();
    if (!token) {
      setUser(null);
      return;
    }
    try {
      const u = await authApi.me();
      setUser(u);
    } catch {
      setUser(null);
    }
  }

  useEffect(() => {
    void (async () => {
      await refreshMe();
      setIsReady(true);
    })();

    const handler = () => void refreshMe();
    window.addEventListener("auth-changed", handler);
    window.addEventListener("storage", handler);

    return () => {
      window.removeEventListener("auth-changed", handler);
      window.removeEventListener("storage", handler);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function login(username: string, password: string) {
    try {
      const { access_token } = await authApi.login(username, password);
      setAccessToken(access_token);
      await refreshMe();
    } catch (e) {
      throw new Error(getApiErrorMessage(e, "Не удалось войти"));
    }
  }

  async function register(username: string, password: string) {
    try {
      await authApi.register(username, password);
      await login(username, password);
    } catch (e) {
      throw new Error(getApiErrorMessage(e, "Не удалось зарегистрироваться"));
    }
  }

  function logout() {
    clearAccessToken();
    setUser(null);
  }

  const value = useMemo<AuthState>(
    () => ({
      user,
      isReady,
      isAuthed: !!user,
      login,
      register,
      logout,
      refreshMe,
    }),
    [user, isReady]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}