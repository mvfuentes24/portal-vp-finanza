"""Pruebas del inicio de sesión."""

from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import COLAB_INACTIVO, JEFE_TESORERIA, _password

MENSAJE_GENERICO = "Correo o contraseña incorrectos"


def login(correo: str, password: str):
    return TestClient(app).post("/auth/login", json={"correo": correo, "password": password})


def test_login_correcto_entrega_cookie_httponly():
    respuesta = login(JEFE_TESORERIA, _password())
    assert respuesta.status_code == 200
    cookie = respuesta.headers["set-cookie"]
    assert "HttpOnly" in cookie
    assert "password_hash" not in respuesta.text


def test_password_incorrecta_y_correo_inexistente_dan_el_mismo_mensaje():
    mala = login(JEFE_TESORERIA, "contraseña-equivocada")
    inexistente = login("nadie@vpfinanzas.example", _password())
    assert mala.status_code == inexistente.status_code == 401
    assert mala.json()["detail"] == inexistente.json()["detail"] == MENSAJE_GENERICO


def test_colaborador_inactivo_no_puede_iniciar_sesion():
    respuesta = login(COLAB_INACTIVO, _password())
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == MENSAJE_GENERICO


def test_sin_sesion_no_hay_acceso(anonimo):
    assert anonimo.get("/auth/me").status_code == 401


def test_token_alterado_es_rechazado(jefe_tesoreria):
    token = jefe_tesoreria.cookies.get("sesion")
    cliente = TestClient(app, cookies={"sesion": token + "x"})
    assert cliente.get("/auth/me").status_code == 401


def test_me_informa_los_modulos_segun_el_rol(admin, jefe_tesoreria, colab_contraloria):
    yo_admin = admin.get("/auth/me").json()
    assert yo_admin["modulos"] == ["organizacion", "cargos", "cierres_caja"]
    assert yo_admin["puede_gestionar_cierres"] is True

    yo_tesoreria = jefe_tesoreria.get("/auth/me").json()
    assert yo_tesoreria["modulos"] == ["organizacion", "cargos"]
    assert yo_tesoreria["puede_gestionar_cierres"] is False

    yo_contraloria = colab_contraloria.get("/auth/me").json()
    assert "cierres_caja" in yo_contraloria["modulos"]
    assert yo_contraloria["puede_gestionar_cierres"] is False
