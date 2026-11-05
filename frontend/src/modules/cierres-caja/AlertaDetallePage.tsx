import { useState } from "react";
import { Link as RouterLink, useParams } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

import { api } from "../../api/client";
import type { AlertaDetalle, EstadoAlerta } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import { useAuth } from "../../auth/AuthContext";
import TituloSeccion from "../../components/TituloSeccion";
import { CargandoPagina, MensajeError } from "../../components/Estados";
import { EtiquetaEstado, EtiquetaTipo, NOMBRE_TIPO_ALERTA } from "../../components/Etiquetas";
import { fecha, fechaHora, monto } from "../../components/formato";

type Decision = Exclude<EstadoAlerta, "pendiente">;

export default function AlertaDetallePage() {
  const { id } = useParams();
  const { usuario } = useAuth();
  const { datos: alerta, error, cargando, recargar } = useApi<AlertaDetalle>(`/cierres-caja/alertas/${id}`);
  const [decision, setDecision] = useState<Decision | null>(null);

  const puedeGestionar = usuario?.puede_gestionar_cierres && alerta?.estado === "pendiente";

  return (
    <>
      <TituloSeccion componente="h1"
        rotulo="Detalle de alerta"
        titulo={alerta ? `Alerta #${alerta.id} · ${NOMBRE_TIPO_ALERTA[alerta.tipo]}` : "Alerta"}
        accion={
          <Button component={RouterLink} to="/cierres-caja/alertas" startIcon={<ArrowBackIcon />}>
            Alertas
          </Button>
        }
      />
      {cargando && !alerta && <CargandoPagina />}
      {error && <MensajeError mensaje={error} />}
      {alerta && (
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 5 }}>
            <Card sx={{ height: "100%" }}>
              <CardContent>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <EtiquetaTipo tipo={alerta.tipo} />
                  <EtiquetaEstado estado={alerta.estado} />
                </Stack>
                <Typography sx={{ mb: 2 }}>{alerta.detalle}</Typography>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="subtitle2" gutterBottom>Cierre #{alerta.cierre_id}</Typography>
                <Typography variant="body2">Fecha: {fecha(alerta.fecha_cierre)}</Typography>
                <Typography variant="body2">Tienda: {alerta.tienda}</Typography>
                <Typography variant="body2">Cajero: {alerta.cajero}</Typography>
                <Typography variant="body2">Monto declarado: {monto(alerta.monto_declarado)}</Typography>
                <Typography variant="body2">Monto sistema: {monto(alerta.monto_sistema)}</Typography>

                {puedeGestionar && (
                  <Stack direction="row" spacing={1} sx={{ mt: 3 }}>
                    <Button variant="contained" color="success" onClick={() => setDecision("revisada")}>
                      Marcar como revisada
                    </Button>
                    <Button variant="outlined" onClick={() => setDecision("descartada")}>
                      Descartar
                    </Button>
                  </Stack>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 7 }}>
            <Card sx={{ height: "100%" }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Historial</Typography>
                <Stack divider={<Divider />} spacing={1.5}>
                  {alerta.historial.map((h, i) => (
                    <Box key={i}>
                      <Stack direction="row" spacing={1} sx={{ alignItems: "center", mb: 0.5 }}>
                        {h.estado_anterior && <EtiquetaEstado estado={h.estado_anterior} />}
                        {h.estado_anterior && <Typography variant="body2">→</Typography>}
                        <EtiquetaEstado estado={h.estado_nuevo} />
                      </Stack>
                      <Typography variant="body2">
                        <strong>{h.gestionado_por}</strong> · {fechaHora(h.fecha)}
                      </Typography>
                      {h.comentario && (
                        <Typography variant="body2" color="text.secondary">{h.comentario}</Typography>
                      )}
                    </Box>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {alerta && decision && (
        <DialogoGestion
          alertaId={alerta.id}
          decision={decision}
          alCerrar={() => setDecision(null)}
          alGuardar={() => {
            setDecision(null);
            recargar();
          }}
        />
      )}
    </>
  );
}

function DialogoGestion({
  alertaId,
  decision,
  alCerrar,
  alGuardar,
}: {
  alertaId: number;
  decision: Decision;
  alCerrar: () => void;
  alGuardar: () => void;
}) {
  const [comentario, setComentario] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const valido = comentario.trim().length >= 5;

  async function guardar() {
    setEnviando(true);
    setError(null);
    try {
      await api.patch(`/cierres-caja/alertas/${alertaId}`, { estado: decision, comentario: comentario.trim() });
      alGuardar();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setEnviando(false);
    }
  }

  return (
    <Dialog open onClose={alCerrar} fullWidth maxWidth="sm">
      <DialogTitle>{decision === "revisada" ? "Marcar como revisada" : "Descartar alerta"}</DialogTitle>
      <DialogContent>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          La decisión queda registrada en el historial con tu nombre y no se puede modificar después.
        </Typography>
        <TextField
          label="Comentario (obligatorio)"
          multiline
          minRows={3}
          fullWidth
          value={comentario}
          onChange={(e) => setComentario(e.target.value)}
          helperText="Mínimo 5 caracteres. Explica qué se verificó o por qué se descarta."
          slotProps={{ htmlInput: { maxLength: 255 } }}
        />
        {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      </DialogContent>
      <DialogActions>
        <Button onClick={alCerrar}>Cancelar</Button>
        <Button variant="contained" onClick={guardar} disabled={!valido || enviando}>
          Confirmar
        </Button>
      </DialogActions>
    </Dialog>
  );
}
