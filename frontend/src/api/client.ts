/**
 * Cliente HTTP del portal. Todas las llamadas al backend pasan por aquí.
 *
 * - Usa rutas relativas (/api/...), que Vite reenvía al backend.
 * - credentials: "include" envía la cookie de sesión (httpOnly) en cada petición.
 *   El frontend nunca lee ni guarda el token: lo maneja el navegador.
 */

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
  }
}

// Se ejecuta cuando la sesión expira (401), para volver al inicio de sesión
let alExpirarSesion: () => void = () => {};
export function configurarExpiracionDeSesion(fn: () => void) {
  alExpirarSesion = fn;
}

async function peticion<T>(metodo: string, ruta: string, cuerpo?: unknown): Promise<T> {
  const respuesta = await fetch(`/api${ruta}`, {
    method: metodo,
    credentials: "include",
    headers: cuerpo !== undefined ? { "Content-Type": "application/json" } : undefined,
    body: cuerpo !== undefined ? JSON.stringify(cuerpo) : undefined,
  });

  if (respuesta.status === 204) return undefined as T;

  const datos = await respuesta.json().catch(() => null);
  if (!respuesta.ok) {
    if (respuesta.status === 401 && ruta !== "/auth/login") alExpirarSesion();
    throw new ApiError(respuesta.status, mensajeDeError(respuesta.status, datos));
  }
  return datos as T;
}

function mensajeDeError(status: number, datos: unknown): string {
  const detalle = (datos as { detail?: unknown } | null)?.detail;
  if (typeof detalle === "string") return detalle;
  // Errores de validación de FastAPI: lista de problemas por campo
  if (Array.isArray(detalle)) return "Revisa los datos ingresados: hay campos con valores no válidos.";
  if (status === 403) return "No tienes permiso para acceder a este recurso.";
  return "Ocurrió un error inesperado. Intenta de nuevo.";
}

export const api = {
  get: <T>(ruta: string) => peticion<T>("GET", ruta),
  post: <T>(ruta: string, cuerpo?: unknown) => peticion<T>("POST", ruta, cuerpo ?? {}),
  patch: <T>(ruta: string, cuerpo: unknown) => peticion<T>("PATCH", ruta, cuerpo),
};
