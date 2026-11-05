import { Box, Typography } from "@mui/material";
import type { ReactNode } from "react";

import { COLORES, FUENTE_TITULOS, RADIO_TARJETA } from "../theme";

/** Panel de encabezado de cada pantalla: rótulo, título con serifa y descripción. */
export default function Encabezado({
  titulo,
  subtitulo,
  rotulo,
  accion,
  lateral,
}: {
  titulo: string;
  subtitulo?: string;
  rotulo?: string;
  accion?: ReactNode;
  /** Bloque opcional a la derecha, separado por una línea vertical */
  lateral?: ReactNode;
}) {
  return (
    <Box
      sx={{
        bgcolor: COLORES.azulPanel,
        color: COLORES.blanco,
        borderRadius: `${RADIO_TARJETA + 4}px`,
        boxShadow: "0 14px 34px rgba(27, 80, 121, 0.22)",
        px: { xs: 3, md: 7 },
        py: { xs: 3, md: 5 },
        mb: 4,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 3,
        flexWrap: "wrap",
      }}
    >
      <Box>
        {rotulo && (
          <Typography variant="overline" sx={{ color: COLORES.rotuloPanel, display: "block", mb: 0.5 }}>
            {rotulo}
          </Typography>
        )}
        <Typography component="h1" sx={{ fontFamily: FUENTE_TITULOS, fontWeight: 600, fontSize: { xs: 30, md: 44 }, lineHeight: 1.15 }}>
          {titulo}
        </Typography>
        {subtitulo && <Typography sx={{ color: COLORES.textoPanel, mt: 1, fontSize: { xs: 16, md: 19 } }}>{subtitulo}</Typography>}
      </Box>

      {lateral && (
        <Box sx={{ borderLeft: `1px solid rgba(255,255,255,0.25)`, pl: 4, py: 1, textAlign: "right" }}>{lateral}</Box>
      )}

      {accion && (
        <Box
          sx={{
            "& .MuiButton-text": { color: COLORES.blanco, "&:hover": { bgcolor: "rgba(255,255,255,0.1)" } },
            "& .MuiButton-contained": { bgcolor: COLORES.blanco, color: COLORES.azulPanel, "&:hover": { bgcolor: COLORES.textoPanel } },
          }}
        >
          {accion}
        </Box>
      )}
    </Box>
  );
}
