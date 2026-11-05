import { Box, Card, CardContent, Typography } from "@mui/material";
import { useState } from "react";

import type { Alerta, Cargo, Cierre, Departamento } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import { useAuth } from "../../auth/AuthContext";
import Cuadricula from "../../components/Cuadricula";
import Encabezado from "../../components/Encabezado";
import { NOMBRE_ROL } from "../../components/Etiquetas";
import TituloSeccion from "../../components/TituloSeccion";
import { ACENTOS, COLORES, FUENTE_TITULOS } from "../../theme";

function Indicador({ titulo, valor, color }: { titulo: string; valor: number | null; color: string }) {
  return (
    <Card sx={{ borderLeft: `4px solid ${color}` }}>
      <CardContent sx={{ px: 4, py: 4.5 }}>
        <Typography
          sx={{ fontFamily: FUENTE_TITULOS, fontSize: 48, fontWeight: 500, lineHeight: 1, color: "#1F2D3A", fontVariantNumeric: "oldstyle-nums" }}
        >
          {valor ?? "–"}
        </Typography>
        <Typography color="text.secondary" sx={{ mt: 1.5, fontSize: 17 }}>
          {titulo}
        </Typography>
      </CardContent>
    </Card>
  );
}

function saludo(hora: number) {
  if (hora < 12) return "Buenos días";
  if (hora < 19) return "Buenas tardes";
  return "Buenas noches";
}

const ROTULO_ROL = {
  administrador: "Panel administrativo",
  jefe_departamento: "Panel de jefatura",
  colaborador: "Panel del colaborador",
} as const;

export default function InicioPage() {
  const { usuario } = useAuth();
  const [cargadoEn] = useState(() => new Date());
  const conCierres = usuario?.modulos.includes("cierres_caja") ?? false;

  // Los indicadores usan los mismos endpoints protegidos del resto del portal,
  // así que cada usuario ve solo las cifras de su alcance
  const departamentos = useApi<Departamento[]>("/organizacion/departamentos");
  const cargos = useApi<Cargo[]>("/cargos");
  const alertas = useApi<Alerta[]>(conCierres ? "/cierres-caja/alertas?estado=pendiente" : null);
  const cierres = useApi<Cierre[]>(conCierres ? "/cierres-caja/cierres" : null);

  if (!usuario) return null;
  const colaboradores = departamentos.datos?.reduce((total, d) => total + d.total_colaboradores, 0) ?? null;
  const alcance = usuario.departamento ? `del departamento de ${usuario.departamento}` : "de la Vicepresidencia de Finanzas";
  const hora = cargadoEn.toLocaleTimeString("es-VE", { hour: "2-digit", minute: "2-digit", hour12: false });

  return (
    <>
      <Encabezado
        rotulo={ROTULO_ROL[usuario.rol]}
        titulo={`${saludo(cargadoEn.getHours())}, ${usuario.nombre.split(" ")[0]}`}
        subtitulo={`Resumen general ${alcance}.`}
        lateral={
          <>
            <Typography variant="overline" sx={{ color: COLORES.rotuloPanel, display: "block" }}>
              Última actualización
            </Typography>
            <Typography sx={{ fontWeight: 800, fontSize: 18 }}>Hoy, {hora}</Typography>
          </>
        }
      />

      <TituloSeccion rotulo="Vista general" titulo="Resumen" nota={NOMBRE_ROL[usuario.rol]} />
      <Box>
        <Cuadricula anchoMinimo={230}>
          <Indicador titulo="Colaboradores activos" valor={colaboradores} color={ACENTOS.azul} />
          <Indicador titulo="Cargos" valor={cargos.datos?.length ?? null} color={ACENTOS.pizarra} />
          {conCierres && <Indicador titulo="Alertas pendientes" valor={alertas.datos?.length ?? null} color={ACENTOS.violeta} />}
          {conCierres && <Indicador titulo="Cierres registrados" valor={cierres.datos?.length ?? null} color={ACENTOS.verde} />}
        </Cuadricula>
      </Box>
    </>
  );
}
