import { useCallback, useEffect, useState } from "react";

import { api } from "./client";

/** Carga datos de la API al mostrar una pantalla. `ruta` null = no cargar todavía. */
export function useApi<T>(ruta: string | null) {
  const [datos, setDatos] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [cargando, setCargando] = useState(ruta !== null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    if (ruta === null) return;
    let vigente = true; // evita actualizar el estado si la pantalla cambió antes de responder
    setCargando(true);
    setError(null);
    api
      .get<T>(ruta)
      .then((respuesta) => vigente && setDatos(respuesta))
      .catch((e: Error) => vigente && setError(e.message))
      .finally(() => vigente && setCargando(false));
    return () => {
      vigente = false;
    };
  }, [ruta, version]);

  const recargar = useCallback(() => setVersion((v) => v + 1), []);
  return { datos, error, cargando, recargar };
}
