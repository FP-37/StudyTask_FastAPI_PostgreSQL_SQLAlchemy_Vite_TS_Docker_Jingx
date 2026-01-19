import { Container } from "@mui/material";
import { Navigate, Route, Routes } from "react-router-dom";

import BusLinesPage from "./pages/BusLinesPage";
import BusLineFormPage from "./pages/BusLineFormPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

import { AuthProvider } from "./hooks/useAuth";
import RequireAuth from "./components/RequireAuth";

export default function App() {
  return (
    <AuthProvider>
      <Container sx={{ py: 4 }}>
        <Routes>
            <Route path="/" element={<Navigate to="/bus-lines" replace />} />

            <Route path="/login" element={<LoginPage />} />

            <Route path="/register" element={<RegisterPage />} />

            <Route path="/bus-lines" element={<BusLinesPage />} />

            {/* create/edit требуют логина */}
            <Route
            path="/bus-lines/new"
            element={
              <RequireAuth>
                <BusLineFormPage mode="create" />
              </RequireAuth>
            }
            />
            <Route
            path="/bus-lines/:id/edit"
            element={
              <RequireAuth>
                <BusLineFormPage mode="edit" />
              </RequireAuth>
            }
            />

            <Route path="*" element={<Navigate to="/bus-lines" replace />} />
        </Routes>
      </Container>
    </AuthProvider>
  );
}