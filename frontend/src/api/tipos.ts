/** Tipos de los datos que devuelve la API (reflejan los schemas del backend). */

export type Rol = "administrador" | "jefe_departamento" | "colaborador";
export type Modulo = "organizacion" | "cargos" | "cierres_caja";

export interface UsuarioActual {
  id: number;
  nombre: string;
  correo: string;
  rol: Rol;
  cargo: string;
  departamento_id: number | null;
  departamento: string | null;
  modulos: Modulo[];
  puede_gestionar_cierres: boolean;
}

export interface Departamento {
  id: number;
  nombre: string;
  descripcion: string | null;
  total_colaboradores: number;
}

/** Los campos opcionales solo llegan en la ficha completa (jefes y administradora). */
export interface Colaborador {
  id: number;
  nombre: string;
  apellido: string;
  correo: string;
  cargo: string;
  nivel?: string;
  departamento?: string;
  pais?: string;
  fecha_ingreso?: string;
  estado?: "activo" | "inactivo";
}

export interface Cargo {
  id: number;
  nombre: string;
  nivel: string;
  departamento_id: number | null;
  departamento: string;
  funciones: string[];
  total_colaboradores: number;
}

export type TipoAlerta = "fuera_rango" | "transposicion" | "reincidencia";
export type EstadoAlerta = "pendiente" | "revisada" | "descartada";

export interface Tienda {
  id: number;
  nombre: string;
  pais: string;
}

export interface Cajero {
  id: number;
  nombre: string;
  tienda_id: number;
  tienda: string;
}

export interface AlertaResumen {
  id: number;
  tipo: TipoAlerta;
  estado: EstadoAlerta;
  detalle: string | null;
}

export interface Cierre {
  id: number;
  fecha: string;
  tienda_id: number;
  tienda: string;
  cajero_id: number;
  cajero: string;
  monto_declarado: string;
  monto_sistema: string;
  diferencia: string;
  porcentaje_diferencia: string;
  registrado_por: string | null;
  alertas: AlertaResumen[];
}

export interface Alerta {
  id: number;
  tipo: TipoAlerta;
  estado: EstadoAlerta;
  detalle: string | null;
  creada_en: string;
  cierre_id: number;
  fecha_cierre: string;
  tienda: string;
  cajero_id: number;
  cajero: string;
}

export interface EntradaHistorial {
  estado_anterior: EstadoAlerta | null;
  estado_nuevo: EstadoAlerta;
  gestionado_por: string;
  comentario: string | null;
  fecha: string;
}

export interface AlertaDetalle extends Alerta {
  monto_declarado: string;
  monto_sistema: string;
  historial: EntradaHistorial[];
}
