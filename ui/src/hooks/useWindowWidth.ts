import { useLayoutEffect, useState } from "react";
import { debounce } from "@mui/material";

export function useWindowWidth(): number {
  const [size, setSize] = useState<number>(0);
  useLayoutEffect(() => {
    const updateSize = () => {
      setSize(window.innerWidth);
    };
    const DEBOUNCED_MS = 100;
    const debouncedUpdate = debounce(updateSize, DEBOUNCED_MS);
    window.addEventListener("resize", debouncedUpdate);
    updateSize();
    return () => window.removeEventListener("resize", debouncedUpdate);
  }, []);
  return size;
}
