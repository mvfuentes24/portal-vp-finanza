"""Reglas de detección de anomalías en cierres de caja.

Son funciones puras: no consultan la base de datos ni dependen de FastAPI.
Así se pueden probar de forma aislada y modificar sin tocar el resto del módulo.
"""

from datetime import date, timedelta
from decimal import Decimal

# --- Parámetros de las reglas (decididos a partir del análisis del dataset) ---

# Diferencia fuera de rango: porcentaje máximo aceptado respecto al monto del sistema.
# En el dataset, los cierres normales no superan el 0,70 % y las anomalías empiezan en 2,2 %.
UMBRAL_PORCENTAJE = Decimal("1")

# Reincidencia: cantidad de cierres con anomalía de un mismo cajero dentro de la ventana.
REINCIDENCIA_MINIMO = 3
REINCIDENCIA_VENTANA_DIAS = 30

# Tipos de alerta
FUERA_RANGO = "fuera_rango"
TRANSPOSICION = "transposicion"
REINCIDENCIA = "reincidencia"


def porcentaje_diferencia(declarado: Decimal, sistema: Decimal) -> Decimal:
    """Diferencia absoluta entre ambos montos, como porcentaje del monto del sistema."""
    diferencia = abs(declarado - sistema)
    if sistema == 0:
        # Sin monto de sistema, cualquier diferencia es total
        return Decimal("100") if diferencia else Decimal("0")
    return diferencia / sistema * 100


def es_fuera_de_rango(declarado: Decimal, sistema: Decimal) -> bool:
    """True si la diferencia supera el umbral (en cualquier dirección: faltante o sobrante)."""
    return porcentaje_diferencia(declarado, sistema) > UMBRAL_PORCENTAJE


def es_transposicion(declarado: Decimal, sistema: Decimal) -> bool:
    """True si los montos solo difieren en dos dígitos CONTIGUOS intercambiados.

    Ejemplo: 1250.00 y 1520.00 -> "125000" y "152000": solo cambian las posiciones
    1 y 2, y sus dígitos están intercambiados.

    No usa el atajo "la diferencia es múltiplo de 9": esa condición es necesaria
    pero no suficiente, y en el dataset daría falsos positivos (cierres 15, 35 y 47).
    """
    a = f"{declarado:.2f}".replace(".", "")
    b = f"{sistema:.2f}".replace(".", "")
    if a == b or len(a) != len(b):
        return False

    posiciones = [i for i in range(len(a)) if a[i] != b[i]]
    if len(posiciones) != 2:
        return False

    i, j = posiciones
    return j == i + 1 and a[i] == b[j] and a[j] == b[i]


def es_reincidencia(fechas_con_anomalia: list[date], fecha_cierre: date) -> bool:
    """True si el cajero acumula el mínimo de cierres con anomalía en la ventana de días.

    La ventana termina en la fecha del cierre analizado e incluye ese cierre.
    """
    inicio = fecha_cierre - timedelta(days=REINCIDENCIA_VENTANA_DIAS)
    en_ventana = [f for f in fechas_con_anomalia if inicio <= f <= fecha_cierre]
    return len(en_ventana) >= REINCIDENCIA_MINIMO
