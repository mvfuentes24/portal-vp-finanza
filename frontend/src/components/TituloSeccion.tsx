import { Box, Typography } from "@mui/material";
import type { ReactNode } from "react";

import { COLORES, FUENTE_TITULOS } from "../theme";

/**
 * Título de pantalla o de sección: rótulo pequeño, título con serifa y línea divisoria.
 * - descripcion: texto bajo el título
 * - nota: texto suelto a la derecha
 * - accion: botón u otro elemento a la derecha
 */
export default function TituloSeccion({
  rotulo,
  titulo,
  descripcion,
  nota,
  accion,
  componente = "h2",
}: {
  rotulo: string;
  titulo: string;
  descripcion?: string;
  nota?: string;
  accion?: ReactNode;
  componente?: "h1" | "h2";
}) {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "space-between",
        gap: 2,
        flexWrap: "wrap",
        borderBottom: "1px solid #D8E2EB",
        pb: 2,
        mb: 3,
      }}
    >
      <Box>
        <Typography variant="overline" sx={{ color: COLORES.azul, display: "block" }}>
          {rotulo}
        </Typography>
        <Typography component={componente} sx={{ fontFamily: FUENTE_TITULOS, fontSize: componente === "h1" ? { xs: 32, md: 46 } : { xs: 26, md: 34 }, fontWeight: 500, lineHeight: 1.2, color: "#1F2D3A" }}>
          {titulo}
        </Typography>
        {descripcion && (
          <Typography color="text.secondary" sx={{ mt: 0.75 }}>
            {descripcion}
          </Typography>
        )}
      </Box>
      {nota && (
        <Typography color="text.secondary" sx={{ pb: 0.5 }}>
          {nota}
        </Typography>
      )}
      {accion && <Box sx={{ pb: 0.25 }}>{accion}</Box>}
    </Box>
  );
}
