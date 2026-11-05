import { Chip } from "@mui/material";

import type { EstadoAlerta, Rol, TipoAlerta } from "../api/tipos";

export const NOMBRE_ROL: Record<Rol, string> = {
  administrador: "Administradora",
  jefe_departamento: "Jefe de departamento",
  colaborador: "Colaborador",
};

export const NOMBRE_TIPO_ALERTA: Record<TipoAlerta, string> = {
  fuera_rango: "Fuera de rango",
  transposicion: "Transposición",
  reincidencia: "Reincidencia",
};

const COLOR_ESTADO = { pendiente: "secondary", revisada: "success", descartada: "default" } as const;

export function EtiquetaEstado({ estado }: { estado: EstadoAlerta }) {
  return <Chip size="small" color={COLOR_ESTADO[estado]} label={estado[0].toUpperCase() + estado.slice(1)} />;
}

export function EtiquetaTipo({ tipo }: { tipo: TipoAlerta }) {
  return <Chip size="small" variant="outlined" label={NOMBRE_TIPO_ALERTA[tipo]} />;
}
