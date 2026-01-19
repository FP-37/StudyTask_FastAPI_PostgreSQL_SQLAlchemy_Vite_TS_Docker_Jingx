import { useEffect, useMemo, useRef, useState } from "react";
import type { BusLine } from "../types/busLine";
import { deleteBusLine, fetchBusLines } from "../api/busLines";
import { getApiErrorMessage } from "../api/client";

type UseBusLinesOptions = {
  limit?: number;
};

export function useBusLines(options: UseBusLinesOptions = {}) {
  const LIMIT = options.limit ?? 20;

  const [lines, setLines] = useState<BusLine[]>([]);
  const [offset, setOffset] = useState<number>(0);
  const [hasMore, setHasMore] = useState<boolean>(true);

  const [loadingFirst, setLoadingFirst] = useState<boolean>(true);
  const [loadingMore, setLoadingMore] = useState<boolean>(false);

  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const sentinelRef = useRef<HTMLDivElement | null>(null);

  const canLoadMore = useMemo(() => {
    return !loadingFirst && !loadingMore && hasMore && !error;
  }, [loadingFirst, loadingMore, hasMore, error]);

  async function refresh() {
    try {
      setError(null);
      setLoadingFirst(true);

      const data = await fetchBusLines(LIMIT, 0);
      setLines(data);
      setOffset(data.length);
      setHasMore(data.length === LIMIT);
    } catch (e) {
      setError(getApiErrorMessage(e, "Не удалось загрузить список bus lines."));
    } finally {
      setLoadingFirst(false);
    }
  }

  async function loadNextPage() {
    if (!canLoadMore) return;

    try {
      setLoadingMore(true);

      const data = await fetchBusLines(LIMIT, offset);

      setLines((prev) => {
        // защита от дублей по id
        const seen = new Set(prev.map((x) => x.id));
        const merged = [...prev];
        for (const item of data) {
          if (!seen.has(item.id)) merged.push(item);
        }
        return merged;
      });

      setOffset((prev) => prev + data.length);
      setHasMore(data.length === LIMIT);
    } catch (e) {
      setError(getApiErrorMessage(e, "Не удалось догрузить данные."));
    } finally {
      setLoadingMore(false);
    }
  }

  async function remove(line: BusLine) {
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

  useEffect(() => {
    void refresh();
  }, []);

  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (entry?.isIntersecting) void loadNextPage();
      },
      { root: null, rootMargin: "200px", threshold: 0 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [offset, canLoadMore]);

  return {
    LIMIT,

    lines,
    hasMore,
    offset,

    loadingFirst,
    loadingMore,

    error,
    deletingId,

    sentinelRef,

    refresh,
    loadNextPage,
    remove,
    setError,
  };
}
