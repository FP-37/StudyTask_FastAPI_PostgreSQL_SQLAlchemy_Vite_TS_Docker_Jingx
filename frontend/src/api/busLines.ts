import { buslinesApi } from "./client";
import type { BusLine } from "../types/busLine";

export async function fetchBusLines(limit = 100, offset = 0): Promise<BusLine[]> {
  const res = await buslinesApi.get<BusLine[]>("/bus-lines", { params: { limit, offset } });
  return res.data;
}

export async function getBusLine(id: number): Promise<BusLine> {
  const res = await buslinesApi.get<BusLine>(`/bus-lines/${id}`);
  return res.data;
}

export type BusLineCreate = Omit<BusLine, "id" | "owner_id">;

export async function createBusLine(payload: BusLineCreate): Promise<BusLine> {
  const res = await buslinesApi.post<BusLine>("/bus-lines", payload);
  return res.data;
}

export type BusLineUpdate = Partial<BusLineCreate>;

export async function updateBusLine(id: number, payload: BusLineUpdate): Promise<BusLine> {
  const res = await buslinesApi.put<BusLine>(`/bus-lines/${id}`, payload);
  return res.data;
}

export async function deleteBusLine(id: number): Promise<void> {
  await buslinesApi.delete(`/bus-lines/${id}`);
}