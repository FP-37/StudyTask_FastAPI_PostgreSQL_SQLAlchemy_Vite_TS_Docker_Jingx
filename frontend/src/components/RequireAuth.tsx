import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function RequireAuth({ children }: { children: React.ReactElement }) {
  const { isReady, isAuthed } = useAuth();
  const location = useLocation();

  if (!isReady) return null;

  if (!isAuthed) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return children;
}