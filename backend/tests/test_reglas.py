"""Pruebas unitarias de las reglas de detección, con casos tomados del dataset."""

from datetime import date
from decimal import Decimal as D

import pytest

from app.modules.cierres_caja.rules import es_fuera_de_rango, es_reincidencia, es_transposicion


# --- Diferencia fuera de rango (umbral: 1 % del monto del sistema) ---

@pytest.mark.parametrize("declarado, sistema", [
    ("470.41", "473.73"),    # cierre 18: 0,70 %, el cierre normal más cercano al umbral
    ("800.50", "800.50"),    # cierre 16: sin diferencia
    ("3954.90", "3945.90"),  # cierre 58: 0,23 % (solo lo detecta la regla de transposición)
])
def test_diferencias_dentro_del_rango(declarado, sistema):
    assert not es_fuera_de_rango(D(declarado), D(sistema))


@pytest.mark.parametrize("declarado, sistema", [
    ("6765.86", "6915.86"),  # cierre 26: 2,2 %, faltante
    ("1152.09", "658.69"),   # cierre 4: 74,9 %, sobrante
])
def test_diferencias_fuera_de_rango_en_ambas_direcciones(declarado, sistema):
    assert es_fuera_de_rango(D(declarado), D(sistema))


def test_exactamente_el_umbral_no_es_anomalia():
    assert not es_fuera_de_rango(D("101.00"), D("100.00"))
    assert es_fuera_de_rango(D("101.01"), D("100.00"))


def test_monto_sistema_cero():
    assert es_fuera_de_rango(D("10.00"), D("0.00"))
    assert not es_fuera_de_rango(D("0.00"), D("0.00"))


# --- Transposición de dígitos contiguos ---

@pytest.mark.parametrize("declarado, sistema", [
    ("1250.00", "1520.00"),  # ejemplo del enunciado
    ("573.95", "753.95"),    # cierre 19
    ("6255.96", "6525.96"),  # cierre 42
    ("4518.95", "4158.95"),  # cierre 53
    ("9485.87", "4985.87"),  # cierre 57
    ("3954.90", "3945.90"),  # cierre 58
])
def test_transposiciones_del_dataset(declarado, sistema):
    assert es_transposicion(D(declarado), D(sistema))


@pytest.mark.parametrize("declarado, sistema", [
    ("6947.75", "6767.75"),  # cierre 15: diferencia 180 (múltiplo de 9) pero NO es transposición
    ("1700.16", "1880.16"),  # cierre 35: ídem
    ("1147.97", "967.97"),   # cierre 47: ídem
])
def test_multiplo_de_9_no_implica_transposicion(declarado, sistema):
    assert not es_transposicion(D(declarado), D(sistema))


def test_digitos_no_contiguos_no_cuentan():
    assert not es_transposicion(D("1250.00"), D("1052.00"))


def test_montos_iguales_no_son_transposicion():
    assert not es_transposicion(D("800.50"), D("800.50"))


# --- Reincidencia (3 cierres con anomalía en 30 días) ---

def test_tres_anomalias_en_30_dias_es_reincidencia():
    fechas = [date(2026, 6, 2), date(2026, 6, 2), date(2026, 6, 10)]  # cajero 3
    assert es_reincidencia(fechas, date(2026, 6, 10))


def test_anomalias_fuera_de_la_ventana_no_cuentan():
    fechas = [date(2026, 5, 1), date(2026, 6, 20), date(2026, 7, 1)]
    assert not es_reincidencia(fechas, date(2026, 7, 1))


def test_dos_anomalias_no_son_reincidencia():
    assert not es_reincidencia([date(2026, 6, 1), date(2026, 6, 5)], date(2026, 6, 5))
