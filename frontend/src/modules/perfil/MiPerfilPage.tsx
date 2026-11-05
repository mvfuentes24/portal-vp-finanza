import { Avatar, Box, Card, CardContent, Typography } from "@mui/material";

import type { Colaborador } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import { useAuth } from "../../auth/AuthContext";
import Cuadricula from "../../components/Cuadricula";
import TituloSeccion from "../../components/TituloSeccion";
import { CargandoPagina, MensajeError } from "../../components/Estados";
import { NOMBRE_ROL } from "../../components/Etiquetas";
import { fecha } from "../../components/formato";
import { iniciales } from "../../theme";

function Dato({ etiqueta, valor }: { etiqueta: string; valor: string }) {
  return (
    <Box>
      <Typography variant="caption" color="text.secondary">
        {etiqueta}
      </Typography>
      <Typography sx={{ fontWeight: 500, overflowWrap: "anywhere" }}>{valor}</Typography>
    </Box>
  );
}

export default function MiPerfilPage() {
  const { usuario } = useAuth();
  const { datos: perfil, error, cargando } = useApi<Colaborador>("/organizacion/mi-perfil");

  return (
    <>
      <TituloSeccion componente="h1" rotulo="Cuenta" titulo="Mi perfil" descripcion="Tu información en el portal" />
      {cargando && <CargandoPagina />}
      {error && <MensajeError mensaje={error} />}
      {perfil && usuario && (
        <Card>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ display: "flex", alignItems: "center", gap: 2.5, mb: 4 }}>
              <Avatar sx={{ bgcolor: "#2B78B5", width: 72, height: 72, fontSize: 26, fontWeight: 800 }}>
                {iniciales(`${perfil.nombre} ${perfil.apellido}`)}
              </Avatar>
              <Box>
                <Typography variant="h5">{`${perfil.nombre} ${perfil.apellido}`}</Typography>
                <Typography color="text.secondary">{perfil.cargo}</Typography>
              </Box>
            </Box>
            <Cuadricula anchoMinimo={260}>
              <Dato etiqueta="Correo" valor={perfil.correo} />
              <Dato etiqueta="Rol en el portal" valor={NOMBRE_ROL[usuario.rol]} />
              <Dato etiqueta="Nivel" valor={perfil.nivel ?? "-"} />
              <Dato etiqueta="Departamento" valor={perfil.departamento ?? "-"} />
              <Dato etiqueta="País" valor={perfil.pais ?? "-"} />
              <Dato etiqueta="Fecha de ingreso" valor={perfil.fecha_ingreso ? fecha(perfil.fecha_ingreso) : "-"} />
            </Cuadricula>
          </CardContent>
        </Card>
      )}
    </>
  );
}
