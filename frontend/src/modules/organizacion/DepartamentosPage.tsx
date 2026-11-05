import { Link as RouterLink } from "react-router-dom";
import { Avatar, Box, Card, CardActionArea, CardContent, Chip, Typography } from "@mui/material";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import CalculateIcon from "@mui/icons-material/Calculate";
import FactCheckIcon from "@mui/icons-material/FactCheck";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import type { ReactNode } from "react";

import type { Departamento } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import TituloSeccion from "../../components/TituloSeccion";
import { CargandoPagina, MensajeError } from "../../components/Estados";
import { plural } from "../../components/formato";
import { COLORES } from "../../theme";

const ICONOS: Record<string, ReactNode> = {
  "Planificación Financiera": <TrendingUpIcon fontSize="large" />,
  Tesorería: <AccountBalanceIcon fontSize="large" />,
  Contraloría: <FactCheckIcon fontSize="large" />,
  Contabilidad: <CalculateIcon fontSize="large" />,
};

export default function DepartamentosPage() {
  const { datos, error, cargando } = useApi<Departamento[]>("/organizacion/departamentos");
  const columnas = (datos?.length ?? 0) > 1 ? 2 : 1;

  return (
    <>
      <TituloSeccion componente="h1" rotulo="Estructura" titulo="Organización" descripcion="Departamentos y sus colaboradores" />
      {cargando && <CargandoPagina />}
      {error && <MensajeError mensaje={error} />}
      {datos && (
        // Las tarjetas se reparten en 2 columnas y se estiran para ocupar
        // todo el alto disponible de la pantalla
        <Box
          sx={{
            flexGrow: 1,
            display: "grid",
            gap: 3,
            gridTemplateColumns: { xs: "1fr", md: `repeat(${columnas}, 1fr)` },
            gridAutoRows: { xs: "minmax(220px, auto)", md: "1fr" },
            minHeight: 0,
          }}
        >
          {datos.map((d) => (
            <Card key={d.id} sx={{ height: "100%" }}>
              <CardActionArea
                component={RouterLink}
                to={`/organizacion/${d.id}`}
                sx={{ height: "100%", display: "flex", alignItems: "stretch" }}
              >
                <CardContent
                  sx={{ p: 3.5, display: "flex", flexDirection: "column", justifyContent: "space-between", gap: 2, width: "100%" }}
                >
                  <Box>
                    <Avatar sx={{ bgcolor: COLORES.azulOscuro, color: COLORES.celeste, width: 56, height: 56, mb: 1.5 }}>
                      {ICONOS[d.nombre] ?? <AccountBalanceIcon fontSize="large" />}
                    </Avatar>
                    <Typography variant="h5" gutterBottom>
                      {d.nombre}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                      {d.descripcion}
                    </Typography>
                  </Box>
                  <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 1.5 }}>
                    <Chip color="primary" variant="outlined" label={plural(d.total_colaboradores, "colaborador activo", "colaboradores activos")} />
                    <Box sx={{ display: "flex", alignItems: "center", gap: 0.5, color: COLORES.azul, fontWeight: 600, whiteSpace: "nowrap" }}>
                      Ver colaboradores <ArrowForwardIcon fontSize="small" />
                    </Box>
                  </Box>
                </CardContent>
              </CardActionArea>
            </Card>
          ))}
        </Box>
      )}
    </>
  );
}
