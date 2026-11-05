import { Alert, Box, CircularProgress } from "@mui/material";

export function CargandoPagina() {
  return (
    <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
      <CircularProgress />
    </Box>
  );
}

export function MensajeError({ mensaje }: { mensaje: string }) {
  return <Alert severity="error">{mensaje}</Alert>;
}
