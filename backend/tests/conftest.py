"""Configuración compartida de las pruebas.

Las pruebas usan la base de datos local con los datos semilla y los usuarios
de prueba ya creados (database/seed.sql y scripts/crear_usuarios.py).
"""

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

ADMIN = "elisa.montero@vpfinanzas.example"            # Vicepresidente de Finanzas
JEFE_TESORERIA = "patricia.montilla@vpfinanzas.example"
COLAB_TESORERIA = "diego.paredes@vpfinanzas.example"
COLAB_INACTIVO = "emilio.fajardo@vpfinanzas.example"

TESORERIA = 2
CONTRALORIA = 3
CARGO_VICEPRESIDENTE = 17
CARGO_TESORERIA_SENIOR = 6
CARGO_CONTRALORIA_SENIOR = 10


def _password() -> str:
    if settings.demo_password is None:
        pytest.skip("Define DEMO_PASSWORD en el .env y crea los usuarios de prueba")
    return settings.demo_password.get_secret_value()


def iniciar_sesion(correo: str) -> TestClient:
    cliente = TestClient(app)
    respuesta = cliente.post("/auth/login", json={"correo": correo, "password": _password()})
    assert respuesta.status_code == 200, respuesta.text
    return cliente


@pytest.fixture
def anonimo() -> TestClient:
    return TestClient(app)


@pytest.fixture
def admin() -> TestClient:
    return iniciar_sesion(ADMIN)


@pytest.fixture
def jefe_tesoreria() -> TestClient:
    return iniciar_sesion(JEFE_TESORERIA)


@pytest.fixture
def colab_tesoreria() -> TestClient:
    return iniciar_sesion(COLAB_TESORERIA)
