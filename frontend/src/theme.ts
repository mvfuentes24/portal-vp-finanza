import "@fontsource-variable/nunito-sans";
import "@fontsource-variable/source-serif-4";
import { alpha, createTheme } from "@mui/material/styles";

// Paleta basada en los colores del logo de Farmatodo
export const COLORES = {
  azulOscuro: "#004473",
  azul: "#0083BE",
  celeste: "#95C5D7",
  blanco: "#FCFDFF",
  // Azul de los paneles (menú lateral, panel de bienvenida, inicio de sesión)
  azulPanel: "#1B5079",
  // Texto secundario sobre los paneles
  textoPanel: "#D9ECFA",
  // Rótulos pequeños sobre los paneles
  rotuloPanel: "#9CCBEA",
  // Fondo de las pantallas
  fondo: "#EEF3F7",
  azulClaro: "#B8D6F0",
};

// Fondo del inicio de sesión: azul claro con un degradado muy sutil
export const FONDO_DEGRADADO = `linear-gradient(160deg, #CFE3F6 0%, ${"#B8D6F0"} 50%, #A6CAEB 100%)`;

// Colores de acento para los indicadores (borde izquierdo de cada tarjeta)
export const ACENTOS = {
  azul: "#2B78B5",
  pizarra: "#7F93A6",
  violeta: "#7A68A6",
  verde: "#5E8A73",
};

// Tipografías: serifa para títulos y cifras, sin serifa para el resto
export const FUENTE_TITULOS = '"Source Serif 4 Variable", Georgia, "Times New Roman", serif';
export const FUENTE_TEXTO = '"Nunito Sans Variable", "Segoe UI", Roboto, Arial, sans-serif';

export const ALTO_BARRA = 96;
export const RADIO_TARJETA = 14;
export const SOMBRA_TARJETA = "0 6px 20px rgba(27, 80, 121, 0.08)";

export const tema = createTheme({
  palette: {
    primary: { main: COLORES.azulPanel },
    secondary: { main: COLORES.azul },
    info: { main: COLORES.azul },
    // Sin naranja: las advertencias usan el azul de la marca
    warning: { main: COLORES.azul },
    background: { default: COLORES.fondo, paper: COLORES.blanco },
    text: { primary: "#1F2D3A", secondary: "#5B6B7A" },
  },
  shape: { borderRadius: 10 },
  mixins: {
    toolbar: { minHeight: ALTO_BARRA },
  },
  typography: {
    fontFamily: FUENTE_TEXTO,
    h4: { fontFamily: FUENTE_TITULOS, fontWeight: 600, color: COLORES.azulPanel },
    h5: { fontFamily: FUENTE_TITULOS, fontWeight: 600, color: COLORES.azulPanel },
    h6: { fontFamily: FUENTE_TITULOS, fontWeight: 600 },
    overline: { fontWeight: 800, letterSpacing: "0.14em", lineHeight: 1.6 },
    button: { fontWeight: 700 },
  },
  components: {
    MuiCard: {
      defaultProps: { elevation: 0 },
      styleOverrides: {
        root: {
          borderRadius: RADIO_TARJETA,
          boxShadow: SOMBRA_TARJETA,
          border: "1px solid #E1E9F0",
        },
      },
    },
    MuiPaper: {
      styleOverrides: { root: { backgroundImage: "none" } },
    },
    MuiDialog: {
      styleOverrides: { paper: { borderRadius: RADIO_TARJETA, padding: 8 } },
    },
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: {
          borderRadius: 999,
          textTransform: "none",
          paddingInline: 20,
          variants: [
            {
              props: { variant: "contained", color: "primary" },
              style: { backgroundColor: COLORES.azul, "&:hover": { backgroundColor: COLORES.azulPanel } },
            },
          ],
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        // Los títulos de columna no se cortan
        head: { fontWeight: 800, color: COLORES.azulPanel, backgroundColor: "#E6EEF5", whiteSpace: "nowrap" },
        // Fondo opaco y por encima de las filas al desplazar la tabla
        stickyHeader: { backgroundColor: "#E6EEF5", zIndex: 3 },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: { root: { backgroundColor: COLORES.blanco } },
    },
  },
});

export const estiloSuperficie = {
  borderRadius: `${RADIO_TARJETA}px`,
  boxShadow: SOMBRA_TARJETA,
  border: "1px solid #E1E9F0",
};

/** Iniciales de un nombre: "Elisa Montero" -> "EM" */
export const iniciales = (nombre: string) =>
  nombre
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0].toUpperCase())
    .join("");

export { alpha };
