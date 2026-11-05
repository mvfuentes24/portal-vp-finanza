import { useState, type FormEvent } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  IconButton,
  InputAdornment,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

import { useAuth } from "../../auth/AuthContext";
import { COLORES, FONDO_DEGRADADO, FUENTE_TITULOS } from "../../theme";
import IlustracionLogin from "./IlustracionLogin";

export default function LoginPage() {
  const { usuario, iniciarSesion } = useAuth();
  const navegar = useNavigate();
  const ubicacion = useLocation();
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [verPassword, setVerPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  if (usuario) return <Navigate to="/" replace />;

  async function enviar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      await iniciarSesion(correo, password);
      const destino = (ubicacion.state as { desde?: string } | null)?.desde ?? "/";
      navegar(destino, { replace: true });
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setEnviando(false);
    }
  }

  return (
    <Box sx={{ minHeight: "100vh", display: "grid", placeItems: "center", p: { xs: 2, md: 4 }, background: FONDO_DEGRADADO }}>
      <Paper
        elevation={12}
        sx={{
          width: "100%",
          maxWidth: 1240,
          minHeight: { md: 680 },
          borderRadius: 5,
          overflow: "hidden",
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
        }}
      >
        {/* Panel de marca */}
        <Box
          sx={{
            bgcolor: COLORES.azulPanel,
            color: COLORES.blanco,
            p: { xs: 4, md: 8 },
            display: "flex",
            flexDirection: "column",
            gap: 4,
          }}
        >
          <Box>
            <Typography variant="overline" sx={{ color: COLORES.rotuloPanel, display: "block", mb: 1, fontSize: 14 }}>
              Bienvenido
            </Typography>
            <Typography
              component="h1"
              sx={{ fontFamily: FUENTE_TITULOS, fontWeight: 600, fontSize: { xs: 38, md: 58 }, lineHeight: 1.08, mb: 2.5 }}
            >
              Portal Corporativo
              <br />
              de Finanzas
            </Typography>
            <Typography sx={{ fontSize: { xs: 18, md: 22 }, color: COLORES.textoPanel }}>
              Información clara, control seguro.
            </Typography>
          </Box>
          <Box sx={{ display: { xs: "none", md: "flex" }, flexGrow: 1, alignItems: "flex-end", justifyContent: "center" }}>
            <IlustracionLogin />
          </Box>
        </Box>

        {/* Formulario */}
        <Box
          sx={{
            bgcolor: COLORES.blanco,
            px: { xs: 4, md: 9 },
            pt: { xs: 4, md: 11 },
            pb: { xs: 4, md: 8 },
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-start",
          }}
        >
          <Typography variant="overline" sx={{ color: COLORES.azul, display: "block" }}>
            Acceso
          </Typography>
          <Typography component="h2" sx={{ fontFamily: FUENTE_TITULOS, fontWeight: 600, fontSize: { xs: 30, md: 38 }, color: COLORES.azulPanel, mb: 1 }}>
            Iniciar sesión
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 5, fontSize: 17 }}>
            Ingresa con tu correo corporativo
          </Typography>
          <Box component="form" onSubmit={enviar} sx={{ display: "grid", gap: 3.5 }}>
            <TextField
              label="Correo"
              type="email"
              placeholder="nombre.apellido@vpfinanzas.example"
              autoComplete="username"
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              required
              autoFocus
            />
            <TextField
              label="Contraseña"
              type={verPassword ? "text" : "password"}
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              slotProps={{
                input: {
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setVerPassword((v) => !v)}
                        edge="end"
                        aria-label={verPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
                      >
                        {verPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                },
              }}
            />
            {error && <Alert severity="error">{error}</Alert>}
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={enviando}
              sx={{ py: 1.6, mt: 1, borderRadius: 999, bgcolor: COLORES.azul, "&:hover": { bgcolor: COLORES.azulPanel } }}
            >
              {enviando ? "Ingresando..." : "Ingresar"}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}
