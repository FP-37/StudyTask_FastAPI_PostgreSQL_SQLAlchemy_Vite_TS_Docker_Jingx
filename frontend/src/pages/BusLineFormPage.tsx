import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { createBusLine, getBusLine, updateBusLine } from "../api/busLines";

type Props = { mode: "create" } | { mode: "edit" };

type FormState = {
  line_number: string;
  depot_number: string;
  start_time: string;
  end_time: string;
  length_km: string;
};

const emptyForm: FormState = {
  line_number: "",
  depot_number: "",
  start_time: "",
  end_time: "",
  length_km: "",
};

// Ввод цифрами: "1234" >> "12:34"
function formatTimeTyping(raw: string): string {
  const digits = raw.replace(/[^\d]/g, "").slice(0, 4);
  if (digits.length <= 2) {
    return digits;
  }
  if (digits.length === 3) {
    return `${digits[0]}:${digits.slice(1)}`;
  }
  return `${digits.slice(0, 2)}:${digits.slice(2)}`;
}

// Нормализуем "9:05" >> "09:05"
function normalizeTime(raw: string): string {
  const v = raw.trim();
  const m = v.match(/^(\d{1,2}):(\d{2})$/);
  if (!m) return v;

  const h = Number(m[1]);
  const mm = Number(m[2]);
  if (h < 0 || h > 23 || mm < 0 || mm > 59) return v;

  return `${String(h).padStart(2, "0")}:${String(mm).padStart(2, "0")}`;
}

function timeToMinutes(v: string): number | null {
  const m = v.trim().match(/^(\d{1,2}):(\d{2})$/);
  if (!m) return null;

  const h = Number(m[1]);
  const mm = Number(m[2]);
  if (h < 0 || h > 23 || mm < 0 || mm > 59) return null;

  return h * 60 + mm;
}

export default function BusLineFormPage(props: Props) {
  const navigate = useNavigate();
  const params = useParams();

  const id = useMemo(() => {
    if (props.mode !== "edit") return null;
    const raw = params.id;
    const parsed = raw ? Number(raw) : NaN;
    return Number.isFinite(parsed) ? parsed : null;
  }, [params.id, props.mode]);

  const [form, setForm] = useState<FormState>(emptyForm);
  const [loading, setLoading] = useState<boolean>(props.mode === "edit");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState<boolean>(false);

  function setField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  useEffect(() => {
    if (props.mode !== "edit") return;

    if (id === null) {
      setError("Некорректный id в URL.");
      setLoading(false);
      return;
    }

    (async () => {
      try {
        setError(null);
        setLoading(true);
        const line = await getBusLine(id);
        const st = String(line.start_time).slice(0, 5);
        const et = String(line.end_time).slice(0, 5);
        setForm({
          line_number: String(line.line_number),
          depot_number: String(line.depot_number),
          start_time: normalizeTime(st),
          end_time: normalizeTime(et),
          length_km: String(line.length_km),
        });
      } catch {
        setError("Не удалось загрузить bus line для редактирования.");
      } finally {
        setLoading(false);
      }
    })();
  }, [id, props.mode]);

  function validate(): string | null {
    const ln = Number(form.line_number);
    const dn = Number(form.depot_number);
    const lk = Number(form.length_km);

    if (!Number.isFinite(ln) || ln <= 0) return "line_number должен быть > 0";
    if (!Number.isFinite(dn) || dn <= 0) return "depot_number должен быть > 0";
    if (!Number.isFinite(lk) || lk <= 0) return "length_km должен быть > 0";

    if (!form.start_time) return "start_time обязателен";
    if (!form.end_time) return "end_time обязателен";

    const s = timeToMinutes(normalizeTime(form.start_time));
    const e = timeToMinutes(normalizeTime(form.end_time));
    if (s === null) return "start_time: формат H:MM или HH:MM";
    if (e === null) return "end_time: формат H:MM или HH:MM";
    if (s >= e) return "start_time должен быть меньше end_time";

    return null;
  }

  async function onSubmit() {
    const v = validate();
    if (v) {
      setError(v);
      return;
    }

    try {
      setError(null);
      setSaving(true);

      const payload = {
        line_number: Number(form.line_number),
        depot_number: Number(form.depot_number),
        start_time: normalizeTime(form.start_time),
        end_time: normalizeTime(form.end_time),
        length_km: Number(form.length_km),
      };

      if (props.mode === "create") {
        await createBusLine(payload);
      } else {
        if (id === null) throw new Error("Invalid id");
        await updateBusLine(id, payload);
      }

      navigate("/bus-lines");
    } catch {
      setError("Сохранение не удалось.");
    } finally {
      setSaving(false);
    }
  }

  const title =
    props.mode === "create" ? "Create Bus Line" : `Edit Bus Line (id=${id ?? "?"})`;

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
        <Typography variant="h4">{title}</Typography>
        <Button variant="outlined" onClick={() => navigate("/bus-lines")}>
          Назад
        </Button>
      </Stack>

      {loading && (
        <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {!loading && error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {!loading && (
        <Paper sx={{ p: 2 }}>
          <Stack spacing={2}>
            <TextField
              label="Line number"
              value={form.line_number}
              onChange={(e) => setField("line_number", e.target.value)}
              inputMode="numeric"
            />

            <TextField
              label="Depot number"
              value={form.depot_number}
              onChange={(e) => setField("depot_number", e.target.value)}
              inputMode="numeric"
            />

            <TextField
              label="Start time"
              value={form.start_time}
              onChange={(e) => setField("start_time", formatTimeTyping(e.target.value))}
              onBlur={() => setField("start_time", normalizeTime(form.start_time))}
              placeholder="H:MM или HH:MM"
              inputProps={{ inputMode: "numeric", maxLength: 5 }}
            />

            <TextField
              label="End time"
              value={form.end_time}
              onChange={(e) => setField("end_time", formatTimeTyping(e.target.value))}
              onBlur={() => setField("end_time", normalizeTime(form.end_time))}
              placeholder="H:MM или HH:MM"
              inputProps={{ inputMode: "numeric", maxLength: 5 }}
            />

            <TextField
              label="Length (km)"
              value={form.length_km}
              onChange={(e) => setField("length_km", e.target.value)}
              inputMode="decimal"
            />

            <Stack direction="row" spacing={2} justifyContent="flex-end">
              <Button variant="contained" onClick={onSubmit} disabled={saving}>
                {saving ? "Сохраняю..." : "Сохранить"}
              </Button>
            </Stack>
          </Stack>
        </Paper>
      )}
    </Box>
  );
}
