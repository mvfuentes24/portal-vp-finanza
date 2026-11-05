"""Pruebas del control de acceso por rol y departamento (sección 3.2 del enunciado)."""

import pytest

from tests.conftest import (
    CARGO_CONTRALORIA_SENIOR,
    CARGO_TESORERIA_SENIOR,
    CARGO_VICEPRESIDENTE,
    CONTRALORIA,
    TESORERIA,
)

CAMPOS_DIRECTORIO = {"id", "nombre", "apellido", "correo", "cargo"}


@pytest.mark.parametrize(
    "ruta",
    ["/organizacion/departamentos", "/organizacion/mi-perfil", "/cargos"],
)
def test_todos_los_endpoints_exigen_sesion(anonimo, ruta):
    assert anonimo.get(ruta).status_code == 401


# --- Administrador: acceso a todo ---

def test_admin_ve_los_cuatro_departamentos(admin):
    assert len(admin.get("/organizacion/departamentos").json()) == 4


def test_admin_ve_colaboradores_de_cualquier_departamento(admin):
    assert admin.get(f"/organizacion/departamentos/{CONTRALORIA}/colaboradores").status_code == 200


def test_admin_ve_el_cargo_de_vicepresidente(admin):
    assert admin.get(f"/cargos/{CARGO_VICEPRESIDENTE}").status_code == 200


# --- Jefe de departamento: solo su departamento, ficha completa ---

def test_jefe_solo_ve_su_departamento(jefe_tesoreria):
    departamentos = jefe_tesoreria.get("/organizacion/departamentos").json()
    assert [d["id"] for d in departamentos] == [TESORERIA]


def test_jefe_ve_ficha_completa_incluidos_inactivos(jefe_tesoreria):
    colaboradores = jefe_tesoreria.get(f"/organizacion/departamentos/{TESORERIA}/colaboradores").json()
    assert all("fecha_ingreso" in c and "estado" in c for c in colaboradores)
    assert any(c["estado"] == "inactivo" for c in colaboradores)


def test_jefe_no_ve_otro_departamento(jefe_tesoreria):
    respuesta = jefe_tesoreria.get(f"/organizacion/departamentos/{CONTRALORIA}/colaboradores")
    assert respuesta.status_code == 403


def test_jefe_no_ve_cargos_de_otro_departamento_ni_el_de_vicepresidente(jefe_tesoreria):
    assert jefe_tesoreria.get(f"/cargos/{CARGO_CONTRALORIA_SENIOR}").status_code == 403
    assert jefe_tesoreria.get(f"/cargos/{CARGO_VICEPRESIDENTE}").status_code == 403


# --- Colaborador: solo lectura de información limitada ---

def test_colaborador_ve_a_sus_companeros_solo_con_datos_de_directorio(colab_tesoreria):
    colaboradores = colab_tesoreria.get(f"/organizacion/departamentos/{TESORERIA}/colaboradores").json()
    assert colaboradores
    assert all(set(c) == CAMPOS_DIRECTORIO for c in colaboradores)


def test_colaborador_no_ve_a_companeros_inactivos(colab_tesoreria, jefe_tesoreria):
    vistos_por_colaborador = colab_tesoreria.get(f"/organizacion/departamentos/{TESORERIA}/colaboradores").json()
    vistos_por_jefe = jefe_tesoreria.get(f"/organizacion/departamentos/{TESORERIA}/colaboradores").json()
    activos = [c for c in vistos_por_jefe if c["estado"] == "activo"]
    assert len(vistos_por_colaborador) == len(activos)


def test_colaborador_ve_su_propio_perfil_completo(colab_tesoreria):
    perfil = colab_tesoreria.get("/organizacion/mi-perfil").json()
    assert perfil["fecha_ingreso"] is not None


def test_colaborador_no_ve_otro_departamento(colab_tesoreria):
    assert colab_tesoreria.get(f"/organizacion/departamentos/{CONTRALORIA}").status_code == 403
    assert colab_tesoreria.get(f"/cargos/{CARGO_CONTRALORIA_SENIOR}").status_code == 403


def test_colaborador_ve_cargos_de_su_departamento_con_funciones(colab_tesoreria):
    cargo = colab_tesoreria.get(f"/cargos/{CARGO_TESORERIA_SENIOR}").json()
    assert cargo["funciones"]


def test_cargos_muestran_cantidad_de_colaboradores_activos(jefe_tesoreria):
    cargos = {c["nombre"]: c["total_colaboradores"] for c in jefe_tesoreria.get("/cargos").json()}
    # Tesorería: 1 gerente, 2 senior, 3 semi-senior y 4 junior (uno de ellos inactivo)
    assert cargos == {
        "Gerente de Tesorería": 1,
        "Analista de Tesorería Senior": 2,
        "Analista de Tesorería Semi-senior": 3,
        "Analista de Tesorería Junior": 3,
    }
