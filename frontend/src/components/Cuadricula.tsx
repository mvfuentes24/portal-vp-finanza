import { Box } from "@mui/material";
import type { ReactNode } from "react";

/**
 * Cuadrícula adaptable: coloca tantas columnas como quepan (con un ancho
 * mínimo por tarjeta) y estira las tarjetas para ocupar todo el ancho.
 */
export default function Cuadricula({ anchoMinimo = 280, children }: { anchoMinimo?: number; children: ReactNode }) {
  return (
    <Box
      sx={{
        display: "grid",
        gap: 2,
        gridTemplateColumns: `repeat(auto-fit, minmax(min(${anchoMinimo}px, 100%), 1fr))`,
      }}
    >
      {children}
    </Box>
  );
}
