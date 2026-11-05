import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  MenuItem,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import type { Alerta, EstadoAlerta, TipoAlerta } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import TituloSeccion from "../../components/TituloSeccion";
import TablaContenedor from "../../components/TablaContenedor";
import { CargandoPagina, MensajeError } from "../../components/Estados";
import { EtiquetaEstado, EtiquetaTipo, NOMBRE_TIPO_ALERTA } from "../../components/Etiquetas";
import { fecha } from "../../components/formato";

export default function AlertasPage() {
  const navegar = useNavigate();
  const [estado, setEstado] = useState<EstadoAlerta | "">("pendiente");
  const [tipo, setTipo] = useState<TipoAlerta | "">("");

  const filtros = new URLSearchParams();
  if (estado) filtros.set("estado", estado);
  if (tipo) filtros.set("tipo", tipo);
  const { datos, error, cargando } = useApi<Alerta[]>(`/cierres-caja/alertas?${filtros}`);

  return (
    <>
      <TituloSeccion componente="h1" rotulo="Contraloría" titulo="Alertas de cierres de caja" descripcion="Anomalías detectadas automáticamente" />
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <TextField select size="small" label="Estado" value={estado} sx={{ minWidth: 180 }}
          onChange={(e) => setEstado(e.target.value as EstadoAlerta | "")}>
          <MenuItem value="">Todos</MenuItem>
          <MenuItem value="pendiente">Pendiente</MenuItem>
          <MenuItem value="revisada">Revisada</MenuItem>
          <MenuItem value="descartada">Descartada</MenuItem>
        </TextField>
        <TextField select size="small" label="Tipo" value={tipo} sx={{ minWidth: 180 }}
          onChange={(e) => setTipo(e.target.value as TipoAlerta | "")}>
          <MenuItem value="">Todos</MenuItem>
          {Object.entries(NOMBRE_TIPO_ALERTA).map(([valor, texto]) => (
            <MenuItem key={valor} value={valor}>{texto}</MenuItem>
          ))}
        </TextField>
      </Stack>

      {cargando && <CargandoPagina />}
      {error && <MensajeError mensaje={error} />}
      {datos && !cargando && (
        <TablaContenedor descontar={390}>
          <Table size="small" stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>#</TableCell>
                <TableCell>Tipo</TableCell>
                <TableCell>Detalle</TableCell>
                <TableCell>Cajero</TableCell>
                <TableCell>Tienda</TableCell>
                <TableCell>Fecha</TableCell>
                <TableCell>Estado</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {datos.map((a) => (
                <TableRow key={a.id} hover sx={{ cursor: "pointer" }}
                  onClick={() => navegar(`/cierres-caja/alertas/${a.id}`)}>
                  <TableCell>{a.id}</TableCell>
                  <TableCell><EtiquetaTipo tipo={a.tipo} /></TableCell>
                  <TableCell sx={{ maxWidth: 380 }}>{a.detalle}</TableCell>
                  <TableCell>{a.cajero}</TableCell>
                  <TableCell>{a.tienda}</TableCell>
                  <TableCell sx={{ whiteSpace: "nowrap" }}>{fecha(a.fecha_cierre)}</TableCell>
                  <TableCell><EtiquetaEstado estado={a.estado} /></TableCell>
                </TableRow>
              ))}
              {datos.length === 0 && (
                <TableRow>
                  <TableCell colSpan={7}>
                    <Typography color="text.secondary" sx={{ py: 2, textAlign: "center" }}>
                      No hay alertas con estos filtros.
                    </Typography>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TablaContenedor>
      )}
    </>
  );
}
