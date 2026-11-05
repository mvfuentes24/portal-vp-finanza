import { Card, CardContent, Chip, List, ListItem, ListItemText, Stack, Typography } from "@mui/material";

import type { Cargo } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import Cuadricula from "../../components/Cuadricula";
import TituloSeccion from "../../components/TituloSeccion";
import { CargandoPagina, MensajeError } from "../../components/Estados";
import { plural } from "../../components/formato";

export default function CargosPage() {
  const { datos, error, cargando } = useApi<Cargo[]>("/cargos");

  // Agrupa los cargos por departamento, respetando el orden que envía la API
  const grupos = new Map<string, Cargo[]>();
  datos?.forEach((c) => grupos.set(c.departamento, [...(grupos.get(c.departamento) ?? []), c]));

  return (
    <>
      <TituloSeccion componente="h1" rotulo="Estructura" titulo="Cargos" descripcion="Ficha de cada cargo: nivel, funciones y colaboradores que lo ocupan" />
      {cargando && <CargandoPagina />}
      {error && <MensajeError mensaje={error} />}
      {[...grupos].map(([departamento, cargos]) => (
        <Stack key={departamento} sx={{ mb: 4 }}>
          <Typography variant="h5" sx={{ mb: 2 }}>
            {departamento}
          </Typography>
          <Cuadricula anchoMinimo={240}>
            {cargos.map((c) => (
                <Card key={c.id} sx={{ height: "100%" }}>
                  <CardContent>
                    <Typography sx={{ fontWeight: 600 }}>{c.nombre}</Typography>
                    <Stack direction="row" spacing={1} sx={{ my: 1 }}>
                      <Chip size="small" color="primary" label={c.nivel} />
                      <Chip size="small" variant="outlined" label={plural(c.total_colaboradores, "colaborador", "colaboradores")} />
                    </Stack>
                    <Typography variant="caption" color="text.secondary">
                      Funciones
                    </Typography>
                    <List dense disablePadding>
                      {c.funciones.map((f) => (
                        <ListItem key={f} disableGutters sx={{ py: 0 }}>
                          <ListItemText primary={`• ${f}`} slotProps={{ primary: { variant: "body2" } }} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
            ))}
          </Cuadricula>
        </Stack>
      ))}
    </>
  );
}
