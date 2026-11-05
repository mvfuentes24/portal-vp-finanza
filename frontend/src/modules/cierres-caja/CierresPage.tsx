import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Button,
  Chip,
  FormControlLabel,
  Stack,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";

import type { Cierre } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import { useAuth } from "../../auth/AuthContext";
import TituloSeccion from "../../components/TituloSeccion";
import TablaContenedor from "../../components/TablaContenedor";
import { CargandoPagina, MensajeError } from "../../components/Estados";
import { NOMBRE_TIPO_ALERTA } from "../../components/Etiquetas";
import { fecha, monto } from "../../components/formato";
import RegistrarCierreDialog from "./RegistrarCierreDialog";

export default function CierresPage() {
  const { usuario } = useAuth();
  const navegar = useNavigate();
  const [soloConAlertas, setSoloConAlertas] = useState(false);
  const [registrando, setRegistrando] = useState(false);
  const { datos, error, cargando, recargar } = useApi<Cierre[]>(
    `/cierres-caja/cierres?solo_con_alertas=${soloConAlertas}`,
  );

  return (
    <>
      <TituloSeccion componente="h1"
        rotulo="Contraloría"
        titulo="Cierres de caja"
        descripcion="Monto declarado por el cajero frente al monto registrado por el sistema"
        accion={
          usuario?.puede_gestionar_cierres && (
            <Button variant="contained" startIcon={<AddIcon />} onClick={() => setRegistrando(true)}>
              Registrar cierre
            </Button>
          )
        }
      />
      <FormControlLabel
        sx={{ mb: 1 }}
        control={<Switch checked={soloConAlertas} onChange={(e) => setSoloConAlertas(e.target.checked)} />}
        label="Mostrar solo cierres con alertas"
      />
      {cargando && <CargandoPagina />}
      {error && <MensajeError mensaje={error} />}
      {datos && !cargando && (
        <TablaContenedor descontar={392}>
          <Table size="small" stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>#</TableCell>
                <TableCell>Fecha</TableCell>
                <TableCell>Tienda</TableCell>
                <TableCell>Cajero</TableCell>
                <TableCell align="right">Declarado</TableCell>
                <TableCell align="right">Sistema</TableCell>
                <TableCell align="right">Diferencia</TableCell>
                <TableCell>Alertas</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {datos.map((c) => (
                <TableRow key={c.id} hover>
                  <TableCell>{c.id}</TableCell>
                  <TableCell sx={{ whiteSpace: "nowrap" }}>{fecha(c.fecha)}</TableCell>
                  <TableCell>{c.tienda}</TableCell>
                  <TableCell>{c.cajero}</TableCell>
                  <TableCell align="right" sx={{ whiteSpace: "nowrap" }}>{monto(c.monto_declarado)}</TableCell>
                  <TableCell align="right" sx={{ whiteSpace: "nowrap" }}>{monto(c.monto_sistema)}</TableCell>
                  <TableCell align="right" sx={{ whiteSpace: "nowrap", color: c.alertas.length ? "error.main" : undefined }}>
                    {monto(c.diferencia)} ({c.porcentaje_diferencia} %)
                  </TableCell>
                  <TableCell>
                    <Stack direction="row" useFlexGap sx={{ flexWrap: "wrap", gap: 0.75, py: 0.5 }}>
                      {c.alertas.map((a) => (
                        <Chip key={a.id} size="small" clickable
                          color={a.estado === "pendiente" ? "secondary" : "default"}
                          label={NOMBRE_TIPO_ALERTA[a.tipo]}
                          onClick={() => navegar(`/cierres-caja/alertas/${a.id}`)} />
                      ))}
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TablaContenedor>
      )}
      {registrando && (
        <RegistrarCierreDialog
          alCerrar={() => setRegistrando(false)}
          alRegistrar={() => {
            setRegistrando(false);
            recargar();
          }}
        />
      )}
    </>
  );
}