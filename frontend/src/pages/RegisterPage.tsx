import { useState } from "react";
import { Alert, Box, Button, Paper, Stack, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit() {
    try {
      setError(null);
      setLoading(true);
      await register(username, password);
      navigate("/bus-lines", { replace: true });
    } catch (e: any) {
      setError(e?.message ?? "Не удалось зарегистрироваться");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box sx={{ maxWidth: 480, mx: "auto" }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Регистрация
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
            helperText="Минимум 4 символа"
          />

          <Stack direction="row" spacing={2} justifyContent="flex-end">
            <Button variant="outlined" onClick={() => navigate("/login")}>
              Уже есть аккаунт
            </Button>
            <Button variant="contained" onClick={onSubmit} disabled={loading}>
              {loading ? "Создаю..." : "Создать аккаунт"}
            </Button>
          </Stack>
        </Stack>
      </Paper>
    </Box>
  );
}