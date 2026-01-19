import {
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import type { BusLine } from "../types/busLine";

type Props = {
  lines: BusLine[];
  deletingId: number | null;
  onEdit: (id: number) => void;
  onDelete: (line: BusLine) => void;
};

export default function BusLinesTable(props: Props) {
  const { lines, deletingId, onEdit, onDelete } = props;

  return (
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
          {lines.map((line) => (
            <TableRow key={line.id}>
              <TableCell>{line.id}</TableCell>
              <TableCell>{line.line_number}</TableCell>
              <TableCell>{line.depot_number}</TableCell>
              <TableCell>{String(line.start_time).slice(0, 5)}</TableCell>
              <TableCell>{String(line.end_time).slice(0, 5)}</TableCell>
              <TableCell align="right">{line.length_km}</TableCell>

              <TableCell align="right">
                <Button
                  variant="outlined"
                  size="small"
                  sx={{ mr: 1 }}
                  onClick={() => onEdit(line.id)}
                >
                  Изменить
                </Button>

                <Button
                  variant="outlined"
                  color="error"
                  size="small"
                  onClick={() => onDelete(line)}
                  disabled={deletingId === line.id}
                >
                  {deletingId === line.id ? "Удаляю..." : "Удалить"}
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
