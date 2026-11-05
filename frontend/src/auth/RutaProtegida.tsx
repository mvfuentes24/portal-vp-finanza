import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";

import type { Modulo } from "../api/tipos";
import { CargandoPagina } from "../components/Estados";
import { useAuth } from "./AuthContext";

/**
 * Muestra la pantalla solo si hay sesión (y, si se indica, acceso al módulo).
 *
 * Es una comodidad de navegación: la protección real está en el backend,
 * que valida rol y departamento en cada endpoint.
 */
export default function RutaProtegida({ modulo, children }: { modulo?: Modulo; children: ReactNode }) {
  const { usuario, verificando } = useAuth();
  const ubicacion = useLocation();

  if (verificando) return <CargandoPagina />;
  if (!usuario) return <Navigate to="/login" replace state={{ desde: ubicacion.pathname }} />;
  if (modulo && !usuario.modulos.includes(modulo)) return <Navigate to="/" replace />;
  return <>{children}</>;
}
