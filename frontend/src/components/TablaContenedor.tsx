import { Paper, TableContainer } from "@mui/material";
import type { ReactNode } from "react";

import { estiloSuperficie } from "../theme";

/**
 * Contenedor de tabla que ocupa el espacio disponible: todo el ancho y, en alto,
 * hasta el borde inferior de la ventana. Si hay más filas, se desplaza dentro
 * de la tabla manteniendo visible el encabezado.
 */
export default function TablaContenedor({ children, descontar = 240 }: { children: ReactNode; descontar?: number }) {
  return (
    <TableContainer
      component={Paper}
      elevation={0}
      sx={{ ...estiloSuperficie, flexGrow: 1, maxHeight: `calc(100vh - ${descontar}px)`, width: "100%" }}
    >
      {children}
    </TableContainer>
  );
}
