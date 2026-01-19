import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import type { BusLine } from "../types/busLine";
import { deleteBusLine } from "../api/busLines";
import { getApiErrorMessage } from "../api/client";
import { useAuth } from "../hooks/useAuth";
import { useBusLinesInfinite } from "../hooks/useBusLinesInfinite";

export default function BusLinesPage() {
  const navigate = useNavigate();
  const { user, isReady, isAuthed, logout } = useAuth();

  const LIMIT = 20;

  const {
    lines,
    setLines,
    loading,
    loadingMore,
    error,
    hasMore,
    reload,
    loadMoreRef,
  } = useBusLinesInfinite(LIMIT);

  const [deletingId, setDeletingId] = useState<number | null>(null);

  const canModify = useMemo(() => {
    return (line: BusLine) => {
      if (!user) return false;
      return user.is_admin || line.owner_id === user.id;
    };
  }, [user]);

  async function handleDelete(line: BusLine) {
    const ok = window.confirm(
      `Удалить bus line?\n\nid: ${line.id}\nline_number: ${line.line_number}`
    );
    if (!ok) return;

    try {
      setDeletingId(line.id);
      await deleteBusLine(line.id);
      setLines((prev) => prev.filter((x) => x.id !== line.id));
    } catch (e) {
      alert(getApiErrorMessage(e, "Удаление не удалось."));
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <Box>
      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2 }}>
        <Box>
          <Typography variant="h4">Bus Lines</Typography>
          {isReady && (
            <Typography variant="body2" sx={{ opacity: 0.75 }}>
              {isAuthed ? `Вы вошли как: ${user?.username}${user?.is_admin ? " (admin)" : ""}` : "Вы не вошли"}
            </Typography>
          )}
        </Box>

        <Box sx={{ display: "flex", gap: 1 }}>
          {isAuthed ? (
            <>
              <Button variant="outlined" onClick={logout}>
                Выйти
              </Button>
              <Button variant="contained" onClick={() => navigate("/bus-lines/new")}>
                Создать
              </Button>
            </>
          ) : (
            <>
              <Button variant="outlined" onClick={() => navigate("/login")}>
                Войти
              </Button>
              <Button variant="contained" onClick={() => navigate("/register")}>
                Регистрация
              </Button>
            </>
          )}
        </Box>
      </Box>

      {loading && (
        <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {!loading && error && (
        <Alert
          severity="error"
          action={
            <Button color="inherit" size="small" onClick={reload}>
              Повторить
            </Button>
          }
        >
          {error}
        </Alert>
      )}

      {!loading && !error && lines.length === 0 && <Alert severity="info">Пока пусто.</Alert>}

      {!loading && !error && lines.length > 0 && (
        <>
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Line №</TableCell>
                  <TableCell>Depot №</TableCell>
                  <TableCell>Start</TableCell>
                  <TableCell>End</TableCell>
                  <TableCell align="right">Length (km)</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {lines.map((line) => {
                  const allowed = canModify(line);

                  return (
                    <TableRow key={line.id}>
                      <TableCell>{line.id}</TableCell>
                      <TableCell>{line.line_number}</TableCell>
                      <TableCell>{line.depot_number}</TableCell>
                      <TableCell>{line.start_time}</TableCell>
                      <TableCell>{line.end_time}</TableCell>
                      <TableCell align="right">{line.length_km}</TableCell>

                      <TableCell align="right">
                        {allowed ? (
                          <>
                            <Button
                              variant="outlined"
                              size="small"
                              sx={{ mr: 1 }}
                              onClick={() => navigate(`/bus-lines/${line.id}/edit`)}
                            >
                              Изменить
                            </Button>

                            <Button
                              variant="outlined"
                              color="error"
                              size="small"
                              onClick={() => handleDelete(line)}
                              disabled={deletingId === line.id}
                            >
                              {deletingId === line.id ? "Удаляю..." : "Удалить"}
                            </Button>
                          </>
                        ) : (
                          <Typography variant="body2" sx={{ opacity: 0.6 }}>
                            —
                          </Typography>
                        )}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>

          <Box ref={loadMoreRef} sx={{ height: 1 }} />

          <Box sx={{ display: "flex", justifyContent: "center", py: 2 }}>
            {loadingMore && <CircularProgress size={22} />}
            {!loadingMore && !hasMore && (
              <Typography variant="body2" sx={{ opacity: 0.7 }}>
                Всё, больше нет.
              </Typography>
            )}
          </Box>
        </>
      )}
    </Box>
  );
}