import { Link as RouterLink, NavLink, Outlet } from "react-router-dom";
import {
  AppBar,
  Avatar,
  Box,
  ButtonBase,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import { alpha } from "@mui/material/styles";
import AccountTreeOutlinedIcon from "@mui/icons-material/AccountTreeOutlined";
import BadgeOutlinedIcon from "@mui/icons-material/BadgeOutlined";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import LogoutIcon from "@mui/icons-material/Logout";
import PointOfSaleOutlinedIcon from "@mui/icons-material/PointOfSaleOutlined";
import ReportProblemOutlinedIcon from "@mui/icons-material/ReportProblemOutlined";
import type { ReactNode } from "react";

import type { Modulo } from "../api/tipos";
import { useAuth } from "../auth/AuthContext";
import { COLORES, FUENTE_TITULOS, iniciales } from "../theme";
import { NOMBRE_ROL } from "./Etiquetas";

const ANCHO_MENU = 344;

interface Opcion {
  ruta: string;
  texto: string;
  icono: ReactNode;
  seccion: "Principal" | "Contraloría";
  modulo?: Modulo;
}

const OPCIONES: Opcion[] = [
  { ruta: "/", texto: "Inicio", icono: <HomeOutlinedIcon />, seccion: "Principal" },
  { ruta: "/organizacion", texto: "Organización", icono: <AccountTreeOutlinedIcon />, seccion: "Principal", modulo: "organizacion" },
  { ruta: "/cargos", texto: "Cargos", icono: <BadgeOutlinedIcon />, seccion: "Principal", modulo: "cargos" },
  { ruta: "/cierres-caja/alertas", texto: "Alertas", icono: <ReportProblemOutlinedIcon />, seccion: "Contraloría", modulo: "cierres_caja" },
  { ruta: "/cierres-caja/cierres", texto: "Cierres de caja", icono: <PointOfSaleOutlinedIcon />, seccion: "Contraloría", modulo: "cierres_caja" },
];


// Opción activa: fondo translúcido con una línea blanca a la izquierda
const estiloOpcion = {
  mx: 2.5,
  my: 0.5,
  py: 1.25,
  borderRadius: 2,
  color: COLORES.blanco,
  borderLeft: "3px solid transparent",
  "& .MuiListItemIcon-root": { color: COLORES.textoPanel, minWidth: 44 },
  "& .MuiListItemText-primary": { fontSize: 17 },
  "&:hover": { bgcolor: alpha(COLORES.blanco, 0.08) },
  "&.active": {
    bgcolor: alpha(COLORES.blanco, 0.14),
    borderLeftColor: COLORES.blanco,
    "& .MuiListItemIcon-root": { color: COLORES.blanco },
    "& .MuiListItemText-primary": { fontWeight: 700 },
  },
};

const estiloRotulo = { display: "block", px: 4, pt: 3, pb: 1, color: COLORES.rotuloPanel };

export default function Layout() {
  const { usuario, cerrarSesion } = useAuth();
  if (!usuario) return null;

  const opciones = OPCIONES.filter((o) => !o.modulo || usuario.modulos.includes(o.modulo));

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", bgcolor: COLORES.fondo }}>
      {/* Menú lateral de altura completa, con la marca arriba */}
      <Drawer
        variant="permanent"
        sx={{
          width: ANCHO_MENU,
          flexShrink: 0,
          "& .MuiDrawer-paper": { width: ANCHO_MENU, bgcolor: COLORES.azulPanel, border: "none", display: "flex", flexDirection: "column" },
        }}
      >
        <Box
          sx={{
            minHeight: 96,
            px: 2.5,
            display: "flex",
            alignItems: "center",
            gap: 1.5,
            borderBottom: `1px solid ${alpha(COLORES.blanco, 0.12)}`,
          }}
        >
          <Avatar
            variant="rounded"
            sx={{ bgcolor: COLORES.blanco, color: COLORES.azulPanel, width: 40, height: 40, borderRadius: 2, fontWeight: 800, fontSize: 14, flexShrink: 0 }}
          >
            PF
          </Avatar>
          <Typography
            sx={{ color: COLORES.blanco, fontFamily: FUENTE_TITULOS, fontWeight: 700, fontSize: 16.5, lineHeight: 1.2, whiteSpace: "nowrap" }}
          >
            Portal Corporativo de Finanzas
          </Typography>
        </Box>

        <List sx={{ flexGrow: 1, pt: 1 }}>
          {opciones.map((o, i) => (
            <Box key={o.ruta}>
              {opciones[i - 1]?.seccion !== o.seccion && (
                <Typography variant="overline" sx={estiloRotulo}>
                  {o.seccion}
                </Typography>
              )}
              <ListItemButton component={NavLink} to={o.ruta} end={o.ruta === "/"} sx={estiloOpcion}>
                <ListItemIcon>{o.icono}</ListItemIcon>
                <ListItemText primary={o.texto} />
              </ListItemButton>
            </Box>
          ))}
        </List>

        <List sx={{ borderTop: `1px solid ${alpha(COLORES.blanco, 0.12)}`, py: 1.5 }}>
          <ListItemButton
            onClick={cerrarSesion}
            sx={{ ...estiloOpcion, color: "#FFE3E0", "& .MuiListItemIcon-root": { color: "#FFB4AB", minWidth: 44 } }}
          >
            <ListItemIcon>
              <LogoutIcon />
            </ListItemIcon>
            <ListItemText primary="Cerrar sesión" />
          </ListItemButton>
        </List>
      </Drawer>

      <Box sx={{ flexGrow: 1, minWidth: 0, display: "flex", flexDirection: "column" }}>
        {/* Barra superior blanca: ubicación y usuario */}
        <AppBar
          position="sticky"
          elevation={0}
          sx={{ bgcolor: COLORES.blanco, color: "text.primary", borderBottom: "1px solid #E1E9F0" }}
        >
          <Toolbar sx={{ gap: 2, px: { xs: 2, md: 6 } }}>
            <Box sx={{ flexGrow: 1 }} />

            <Tooltip title="Ver mi perfil">
              <ButtonBase
                component={RouterLink}
                to="/mi-perfil"
                aria-label={`Ver el perfil de ${usuario.nombre}`}
                sx={{ display: "flex", alignItems: "center", gap: 2, py: 1, pl: 2, pr: 1, borderRadius: 999, "&:hover": { bgcolor: COLORES.fondo } }}
              >
                <Box sx={{ textAlign: "right", display: { xs: "none", sm: "block" } }}>
                  <Typography sx={{ fontWeight: 800, fontSize: 17 }}>{usuario.nombre}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {NOMBRE_ROL[usuario.rol]} · {usuario.departamento ?? "Vicepresidencia"}
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: ACENTO_AVATAR, width: 54, height: 54, fontWeight: 800 }}>{iniciales(usuario.nombre)}</Avatar>
              </ButtonBase>
            </Tooltip>
          </Toolbar>
        </AppBar>

        <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 6 }, pt: { md: 5 }, display: "flex", flexDirection: "column" }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
}

const ACENTO_AVATAR = "#2B78B5";
