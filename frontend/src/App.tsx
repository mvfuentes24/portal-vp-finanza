import { Navigate, Route, Routes } from "react-router-dom";

import RutaProtegida from "./auth/RutaProtegida";
import Layout from "./components/Layout";
import CargosPage from "./modules/cargos/CargosPage";
import AlertaDetallePage from "./modules/cierres-caja/AlertaDetallePage";
import AlertasPage from "./modules/cierres-caja/AlertasPage";
import CierresPage from "./modules/cierres-caja/CierresPage";
import LoginPage from "./modules/auth/LoginPage";
import InicioPage from "./modules/inicio/InicioPage";
import MiPerfilPage from "./modules/perfil/MiPerfilPage";
import DepartamentoDetallePage from "./modules/organizacion/DepartamentoDetallePage";
import DepartamentosPage from "./modules/organizacion/DepartamentosPage";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        element={
          <RutaProtegida>
            <Layout />
          </RutaProtegida>
        }
      >
        <Route index element={<InicioPage />} />
        <Route path="mi-perfil" element={<MiPerfilPage />} />
        <Route path="organizacion" element={<RutaProtegida modulo="organizacion"><DepartamentosPage /></RutaProtegida>} />
        <Route path="organizacion/:id" element={<RutaProtegida modulo="organizacion"><DepartamentoDetallePage /></RutaProtegida>} />
        <Route path="cargos" element={<RutaProtegida modulo="cargos"><CargosPage /></RutaProtegida>} />
        <Route path="cierres-caja/alertas" element={<RutaProtegida modulo="cierres_caja"><AlertasPage /></RutaProtegida>} />
        <Route path="cierres-caja/alertas/:id" element={<RutaProtegida modulo="cierres_caja"><AlertaDetallePage /></RutaProtegida>} />
        <Route path="cierres-caja/cierres" element={<RutaProtegida modulo="cierres_caja"><CierresPage /></RutaProtegida>} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
