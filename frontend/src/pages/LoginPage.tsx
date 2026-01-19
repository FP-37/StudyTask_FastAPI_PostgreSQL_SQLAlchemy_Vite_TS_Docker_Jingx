import { useState } from "react";
import { Alert, Box, Button, Paper, Stack, TextField, Typography } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const from = (location.state as any)?.from ?? "/bus-lines";

  async function onSubmit() {
    try {
      setError(null);
      setLoading(true);
      await login(username, password);
      navigate(from, { replace: true });
    } catch (e: any) {
      setError(e?.message ?? "Не удалось войти");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box sx={{ maxWidth: 480, mx: "auto" }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Вход
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 2 }}>
        <Stack spacing={2}>
          <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Stack direction="row" spacing={2} justifyContent="flex-end">
            <Button variant="outlined" onClick={() => navigate("/register")}>
              Регистрация
            </Button>
            <Button variant="contained" onClick={onSubmit} disabled={loading}>
              {loading ? "Вхожу..." : "Войти"}
            </Button>
          </Stack>
        </Stack>
      </Paper>
    </Box>
  );
}