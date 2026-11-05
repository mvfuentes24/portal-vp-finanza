import { useState } from "react";
import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { api } from "../../api/client";
import type { Cajero, Cierre, Tienda } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import { NOMBRE_TIPO_ALERTA } from "../../components/Etiquetas";

const hoy = new Date().toISOString().slice(0, 10);
const MONTO_VALIDO = /^\d{1,10}(\.\d{1,2})?$/;

export default function RegistrarCierreDialog({
  alCerrar,
  alRegistrar,
}: {
  alCerrar: () => void;
  alRegistrar: () => void;
}) {
  const tiendas = useApi<Tienda[]>("/cierres-caja/tiendas");
  const cajeros = useApi<Cajero[]>("/cierres-caja/cajeros");
  const [form, setForm] = useState({ tienda_id: "", cajero_id: "", fecha: hoy, monto_declarado: "", monto_sistema: "" });
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [resultado, setResultado] = useState<Cierre | null>(null);

  const cambiar = (campo: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const valor = e.target.value;
    setForm((f) => {
      const nuevo = { ...f, [campo]: valor };
      // Al elegir un cajero se propone su tienda asignada; se puede cambiar si cubrió otra tienda
      if (campo === "cajero_id") {
        const cajero = cajeros.datos?.find((c) => String(c.id) === valor);
        if (cajero) nuevo.tienda_id = String(cajero.tienda_id);
      }
      return nuevo;
    });
  };

  const valido =
    form.tienda_id && form.cajero_id && form.fecha &&
    MONTO_VALIDO.test(form.monto_declarado) && MONTO_VALIDO.test(form.monto_sistema);

  async function registrar() {
    setEnviando(true);
    setError(null);
    try {
      const cierre = await api.post<Cierre>("/cierres-caja/cierres", {
        tienda_id: Number(form.tienda_id),
        cajero_id: Number(form.cajero_id),
        fecha: form.fecha,
        monto_declarado: form.monto_declarado,
        monto_sistema: form.monto_sistema,
      });
      setResultado(cierre);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setEnviando(false);
    }
  }

  if (resultado) {
    return (
      <Dialog open onClose={alRegistrar} fullWidth maxWidth="sm">
        <DialogTitle>Cierre #{resultado.id} registrado</DialogTitle>
        <DialogContent>
          {resultado.alertas.length === 0 ? (
            <Alert severity="success">No se detectaron anomalías en este cierre.</Alert>
          ) : (
            <Alert severity="info">
              <Typography variant="body2" gutterBottom>Se generaron las siguientes alertas:</Typography>
              {resultado.alertas.map((a) => (
                <Typography key={a.id} variant="body2">• {NOMBRE_TIPO_ALERTA[a.tipo]}: {a.detalle}</Typography>
              ))}
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button variant="contained" onClick={alRegistrar}>Aceptar</Button>
        </DialogActions>
      </Dialog>
    );
  }

  return (
    <Dialog open onClose={alCerrar} fullWidth maxWidth="sm">
      <DialogTitle>Registrar cierre de caja</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          <TextField select label="Cajero" value={form.cajero_id} onChange={cambiar("cajero_id")}
            disabled={!cajeros.datos}>
            {(cajeros.datos ?? []).map((c) => <MenuItem key={c.id} value={String(c.id)}>{c.nombre}</MenuItem>)}
          </TextField>
          <TextField select label="Tienda" value={form.tienda_id} onChange={cambiar("tienda_id")}
            disabled={!tiendas.datos} helperText="Se propone la tienda asignada al cajero; cámbiala si cubrió otra tienda">
            {(tiendas.datos ?? []).map((t) => <MenuItem key={t.id} value={String(t.id)}>{t.nombre}</MenuItem>)}
          </TextField>
          <TextField type="date" label="Fecha" value={form.fecha} onChange={cambiar("fecha")}
            slotProps={{ inputLabel: { shrink: true }, htmlInput: { max: hoy } }} />
          <Stack direction="row" spacing={2}>
            <TextField fullWidth label="Monto declarado" value={form.monto_declarado}
              onChange={cambiar("monto_declarado")} placeholder="0.00" slotProps={{ htmlInput: { inputMode: "decimal" } }} />
            <TextField fullWidth label="Monto sistema" value={form.monto_sistema}
              onChange={cambiar("monto_sistema")} placeholder="0.00" slotProps={{ htmlInput: { inputMode: "decimal" } }} />
          </Stack>
          <Typography variant="caption" color="text.secondary">
            Usa punto como separador decimal, con hasta 2 decimales. Las reglas de detección se aplican al registrar.
          </Typography>
          {error && <Alert severity="error">{error}</Alert>}
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={alCerrar}>Cancelar</Button>
        <Button variant="contained" onClick={registrar} disabled={!valido || enviando}>
          Registrar
        </Button>
      </DialogActions>
    </Dialog>
  );
}
