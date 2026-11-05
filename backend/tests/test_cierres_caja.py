"""Pruebas del módulo de cierres de caja: acceso, detección, registro y gestión de alertas."""

import pytest
from sqlalchemy.orm import Session

from app.modules.cierres_caja.service import analizar_todos


@pytest.fixture
def alertas_del_dataset(conexion):
    """Genera las alertas de los 60 cierres (dentro de la transacción de la prueba)."""
    with Session(bind=conexion, join_transaction_mode="create_savepoint") as db:
        analizar_todos(db)


ULTIMO_CIERRE_DEL_DATASET = 60


def alertas(cliente, **filtros):
    respuesta = cliente.get("/cierres-caja/alertas", params=filtros)
    assert respuesta.status_code == 200, respuesta.text
    return respuesta.json()


def alertas_del_dataset_original(cliente, **filtros):
    """Solo las alertas de los 60 cierres del dataset, aunque se hayan registrado
    otros cierres en la base de datos local (por ejemplo, al probar el portal)."""
    return [a for a in alertas(cliente, **filtros) if a["cierre_id"] <= ULTIMO_CIERRE_DEL_DATASET]


# Las pruebas que registran cierres usan fechas de 2025, lejos de los datos del
# dataset (junio-julio 2026), para que la regla de reincidencia no se vea afectada
# por cierres de otras pruebas o registrados a mano.
FECHA_PRUEBA = "2025-03-10"


# --- Acceso: el módulo pertenece a Contraloría ---

def test_otros_departamentos_no_acceden(jefe_tesoreria, colab_tesoreria):
    assert jefe_tesoreria.get("/cierres-caja/cierres").status_code == 403
    assert colab_tesoreria.get("/cierres-caja/alertas").status_code == 403


def test_contraloria_y_administradora_consultan(admin, jefe_contraloria, colab_contraloria):
    for cliente in (admin, jefe_contraloria, colab_contraloria):
        assert cliente.get("/cierres-caja/cierres").status_code == 200


def test_colaborador_de_contraloria_no_registra_ni_gestiona(colab_contraloria, alertas_del_dataset):
    nuevo = {"tienda_id": 1, "cajero_id": 5, "fecha": FECHA_PRUEBA,
             "monto_declarado": "100.00", "monto_sistema": "100.00"}
    assert colab_contraloria.post("/cierres-caja/cierres", json=nuevo).status_code == 403
    alerta_id = alertas(colab_contraloria)[0]["id"]
    gestion = {"estado": "revisada", "comentario": "Intento sin permiso"}
    assert colab_contraloria.patch(f"/cierres-caja/alertas/{alerta_id}", json=gestion).status_code == 403


# --- Detección sobre el dataset ---

def test_el_dataset_genera_las_alertas_esperadas(admin, alertas_del_dataset):
    assert len(alertas_del_dataset_original(admin, tipo="fuera_rango")) == 18
    assert {a["cierre_id"] for a in alertas_del_dataset_original(admin, tipo="transposicion")} == {19, 42, 53, 57, 58}
    reincidencias = alertas_del_dataset_original(admin, tipo="reincidencia")
    assert {a["cajero_id"] for a in reincidencias} == {3, 6, 8}
    assert {a["cierre_id"] for a in reincidencias} == {21, 39, 58}


def test_toda_alerta_nace_pendiente_con_historial_del_sistema(admin, alertas_del_dataset):
    alerta = admin.get(f"/cierres-caja/alertas/{alertas(admin)[0]['id']}").json()
    assert alerta["estado"] == "pendiente"
    assert len(alerta["historial"]) == 1
    assert alerta["historial"][0]["gestionado_por"] == "Sistema"


# --- Registro de un cierre nuevo ---

def test_registrar_cierre_con_anomalia_genera_alerta(jefe_contraloria):
    nuevo = {"tienda_id": 2, "cajero_id": 2, "fecha": FECHA_PRUEBA,
             "monto_declarado": "1520.00", "monto_sistema": "1250.00"}
    respuesta = jefe_contraloria.post("/cierres-caja/cierres", json=nuevo)
    assert respuesta.status_code == 201, respuesta.text
    cierre = respuesta.json()
    assert cierre["registrado_por"] == "Carolina Briceño"
    assert {a["tipo"] for a in cierre["alertas"]} == {"fuera_rango", "transposicion"}


def test_un_cajero_puede_cerrar_en_otra_tienda(admin):
    # Cajero 2 está asignado a la tienda 2, pero cubre la tienda 5
    nuevo = {"tienda_id": 5, "cajero_id": 2, "fecha": FECHA_PRUEBA,
             "monto_declarado": "1000.00", "monto_sistema": "1000.00"}
    cierre = admin.post("/cierres-caja/cierres", json=nuevo).json()
    assert cierre["tienda_id"] == 5


def test_registrar_cierre_normal_no_genera_alertas(admin):
    nuevo = {"tienda_id": 1, "cajero_id": 5, "fecha": FECHA_PRUEBA,
             "monto_declarado": "1000.00", "monto_sistema": "1003.00"}
    assert admin.post("/cierres-caja/cierres", json=nuevo).json()["alertas"] == []


@pytest.mark.parametrize("cambio, mensaje", [
    ({"cajero_id": 999}, "cajero"),
    ({"tienda_id": 999}, "tienda"),
    ({"fecha": "2999-01-01"}, "futura"),
])
def test_validaciones_del_registro(admin, cambio, mensaje):
    nuevo = {"tienda_id": 1, "cajero_id": 5, "fecha": FECHA_PRUEBA,
             "monto_declarado": "100.00", "monto_sistema": "100.00", **cambio}
    respuesta = admin.post("/cierres-caja/cierres", json=nuevo)
    assert respuesta.status_code == 422
    assert mensaje in respuesta.json()["detail"]


def test_montos_negativos_son_rechazados(admin):
    nuevo = {"tienda_id": 1, "cajero_id": 5, "fecha": FECHA_PRUEBA,
             "monto_declarado": "-5.00", "monto_sistema": "100.00"}
    assert admin.post("/cierres-caja/cierres", json=nuevo).status_code == 422


# --- Gestión de alertas ---

def test_gestionar_alerta_queda_en_el_historial(jefe_contraloria, alertas_del_dataset):
    alerta_id = alertas(jefe_contraloria, estado="pendiente")[0]["id"]
    gestion = {"estado": "revisada", "comentario": "Se verificó con la tienda: error de conteo"}
    respuesta = jefe_contraloria.patch(f"/cierres-caja/alertas/{alerta_id}", json=gestion)
    assert respuesta.status_code == 200, respuesta.text
    alerta = respuesta.json()
    assert alerta["estado"] == "revisada"
    ultimo = alerta["historial"][-1]
    assert ultimo["estado_anterior"] == "pendiente"
    assert ultimo["estado_nuevo"] == "revisada"
    assert ultimo["gestionado_por"] == "Carolina Briceño"
    assert ultimo["comentario"] == gestion["comentario"]


def test_una_alerta_gestionada_no_se_puede_volver_a_cambiar(admin, alertas_del_dataset):
    alerta_id = alertas(admin, estado="pendiente")[0]["id"]
    admin.patch(f"/cierres-caja/alertas/{alerta_id}", json={"estado": "descartada", "comentario": "Falsa alarma"})
    segundo = admin.patch(f"/cierres-caja/alertas/{alerta_id}", json={"estado": "revisada", "comentario": "Cambio de opinión"})
    assert segundo.status_code == 409


def test_el_comentario_es_obligatorio(admin, alertas_del_dataset):
    alerta_id = alertas(admin)[0]["id"]
    respuesta = admin.patch(f"/cierres-caja/alertas/{alerta_id}", json={"estado": "revisada", "comentario": ""})
    assert respuesta.status_code == 422


def test_las_alertas_descartadas_no_cuentan_para_reincidencia(admin):
    # Cajero 5 (Carla Beltrán) no tiene anomalías en el dataset
    base = {"tienda_id": 1, "cajero_id": 5, "monto_sistema": "1000.00"}
    primero = admin.post("/cierres-caja/cierres", json={**base, "fecha": "2025-03-17", "monto_declarado": "900.00"}).json()
    admin.post("/cierres-caja/cierres", json={**base, "fecha": "2025-03-18", "monto_declarado": "900.00"})
    # Contraloría descarta la primera anomalía
    admin.patch(f"/cierres-caja/alertas/{primero['alertas'][0]['id']}",
                json={"estado": "descartada", "comentario": "Error de digitación ya corregido"})
    tercero = admin.post("/cierres-caja/cierres", json={**base, "fecha": "2025-03-19", "monto_declarado": "900.00"}).json()
    # Solo 2 anomalías vigentes: no hay reincidencia
    assert "reincidencia" not in {a["tipo"] for a in tercero["alertas"]}
    cuarto = admin.post("/cierres-caja/cierres", json={**base, "fecha": "2025-03-20", "monto_declarado": "900.00"}).json()
    # Con la cuarta, son 3 vigentes: ahora sí
    assert "reincidencia" in {a["tipo"] for a in cuarto["alertas"]}
