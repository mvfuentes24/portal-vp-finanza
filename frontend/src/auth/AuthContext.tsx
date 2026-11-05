import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";

import { api, configurarExpiracionDeSesion } from "../api/client";
import type { UsuarioActual } from "../api/tipos";

interface ContextoAuth {
  usuario: UsuarioActual | null;
  verificando: boolean;
  iniciarSesion: (correo: string, password: string) => Promise<void>;
  cerrarSesion: () => Promise<void>;
}

const AuthContext = createContext<ContextoAuth | null>(null);

/**
 * Mantiene el usuario autenticado. Al abrir el portal pregunta al backend
 * quién es el usuario (/auth/me): si la cookie de sesión sigue vigente,
 * no hace falta volver a iniciar sesión.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<UsuarioActual | null>(null);
  const [verificando, setVerificando] = useState(true);

  useEffect(() => {
    configurarExpiracionDeSesion(() => setUsuario(null));
    api
      .get<UsuarioActual>("/auth/me")
      .then(setUsuario)
      .catch(() => setUsuario(null))
      .finally(() => setVerificando(false));
  }, []);

  const iniciarSesion = useCallback(async (correo: string, password: string) => {
    await api.post("/auth/login", { correo, password });
    // Se pide /auth/me para obtener también los módulos y permisos del usuario
    setUsuario(await api.get<UsuarioActual>("/auth/me"));
  }, []);

  const cerrarSesion = useCallback(async () => {
    await api.post("/auth/logout").catch(() => undefined);
    setUsuario(null);
  }, []);

  return (
    <AuthContext.Provider value={{ usuario, verificando, iniciarSesion, cerrarSesion }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): ContextoAuth {
  const contexto = useContext(AuthContext);
  if (!contexto) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return contexto;
}
