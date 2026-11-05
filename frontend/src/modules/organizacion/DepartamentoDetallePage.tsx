import { Link as RouterLink, useParams } from "react-router-dom";
import {
  Alert,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

import type { Colaborador, Departamento } from "../../api/tipos";
import { useApi } from "../../api/useApi";
import TituloSeccion from "../../components/TituloSeccion";
import TablaContenedor from "../../components/TablaContenedor";
import { CargandoPagina, MensajeError } from "../../components/Estados";
import { fecha } from "../../components/formato";

export default function DepartamentoDetallePage() {
  const { id } = useParams();
  const departamento = useApi<Departamento>(`/organizacion/departamentos/${id}`);
  const colaboradores = useApi<Colaborador[]>(`/organizacion/departamentos/${id}/colaboradores`);

  const error = departamento.error ?? colaboradores.error;
  const lista = colaboradores.datos ?? [];
  // La API solo envía la ficha completa a jefes y administradora
  const fichaCompleta = lista.some((c) => c.estado !== undefined);

  return (
    <>
      <TituloSeccion componente="h1"
        rotulo="Departamento"
        titulo={departamento.datos?.nombre ?? "Departamento"}
        descripcion={departamento.datos?.descripcion ?? undefined}
        accion={
          <Button component={RouterLink} to="/organizacion" startIcon={<ArrowBackIcon />}>
            Departamentos
          </Button>
        }
      />
      {(departamento.cargando || colaboradores.cargando) && <CargandoPagina />}
      {error && <MensajeError mensaje={error} />}
      {!error && colaboradores.datos && (
        <>
          {!fichaCompleta && (
            <Alert severity="info" sx={{ mb: 2 }}>
              Vista de directorio: se muestran tus compañeros activos con sus datos de contacto.
            </Alert>
          )}
          <TablaContenedor descontar={342}>
            <Table size="small" stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell>Nombre</TableCell>
                  <TableCell>Correo</TableCell>
                  <TableCell>Cargo</TableCell>
                  {fichaCompleta && (
                    <>
                      <TableCell>Nivel</TableCell>
                      <TableCell>País</TableCell>
                      <TableCell>Ingreso</TableCell>
                      <TableCell>Estado</TableCell>
                    </>
                  )}
                </TableRow>
              </TableHead>
              <TableBody>
                {lista.map((c) => (
                  <TableRow key={c.id} hover>
                    <TableCell>{`${c.nombre} ${c.apellido}`}</TableCell>
                    <TableCell>{c.correo}</TableCell>
                    <TableCell>{c.cargo}</TableCell>
                    {fichaCompleta && (
                      <>
                        <TableCell>{c.nivel}</TableCell>
                        <TableCell>{c.pais}</TableCell>
                        <TableCell sx={{ whiteSpace: "nowrap" }}>{c.fecha_ingreso && fecha(c.fecha_ingreso)}</TableCell>
                        <TableCell>
                          <Chip
                            size="small"
                            label={c.estado}
                            color={c.estado === "activo" ? "success" : "default"}
                            variant={c.estado === "activo" ? "filled" : "outlined"}
                          />
                        </TableCell>
                      </>
                    )}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TablaContenedor>
        </>
      )}
    </>
  );
}
