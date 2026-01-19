import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { BusLine } from "../types/busLine";
import { fetchBusLines } from "../api/busLines";
import { getApiErrorMessage } from "../api/client";

export function useBusLinesInfinite(limit = 20) {
  const [lines, setLines] = useState<BusLine[]>([]);
  const [loading, setLoading] = useState(true); // первая загрузка
  const [loadingMore, setLoadingMore] = useState(false); // догрузка
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const inFlightRef = useRef(false);
  const offset = useMemo(() => lines.length, [lines.length]);
  const loadFirst = useCallback(async () => {
    if (inFlightRef.current) return;
    inFlightRef.current = true;

    try {
      setError(null);
      setLoading(true);
      setHasMore(true);

      const data = await fetchBusLines(limit, 0);
      setLines(data);
      setHasMore(data.length === limit);
    } catch (e) {
      setError(getApiErrorMessage(e, "Не удалось загрузить список bus lines."));
    } finally {
      setLoading(false);
      inFlightRef.current = false;
    }
  }, [limit]);

  const loadMore = useCallback(async () => {
    if (inFlightRef.current) return;
    if (!hasMore) return;
    if (loading) return;

    inFlightRef.current = true;

    try {
      setError(null);
      setLoadingMore(true);

      const data = await fetchBusLines(limit, offset);

      setLines((prev) => {
        const seen = new Set(prev.map((x) => x.id));
        const merged = [...prev, ...data.filter((x) => !seen.has(x.id))];
        return merged;
      });

      if (data.length < limit) setHasMore(false);
    } catch (e) {
      setError(getApiErrorMessage(e, "Не удалось подгрузить ещё bus lines."));
    } finally {
      setLoadingMore(false);
      inFlightRef.current = false;
    }
  }, [hasMore, loading, limit, offset]);

  const loadMoreRef = useCallback(
    (node: HTMLDivElement | null) => {
      if (!node) return;

      const observer = new IntersectionObserver(
        (entries) => {
          if (entries[0]?.isIntersecting) {
            void loadMore();
          }
        },
        {
          root: null, // окно
          rootMargin: "200px",
          threshold: 0,
        }
      );

      observer.observe(node);

      return () => observer.disconnect();
    },
    [loadMore]
  );

  useEffect(() => {
    void loadFirst();
  }, [loadFirst]);

  return {
    lines,
    setLines,
    loading,
    loadingMore,
    error,
    hasMore,
    reload: loadFirst,
    loadMoreRef,
  };
}