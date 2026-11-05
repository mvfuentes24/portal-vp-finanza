"""Datos que entran y salen del módulo de cierres de caja."""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TiendaOut(BaseModel):
    id: int
    nombre: str
    pais: str


class CajeroOut(BaseModel):
    id: int
    nombre: str
    tienda_id: int
    tienda: str


class CierreIn(BaseModel):
    tienda_id: int
    cajero_id: int
    fecha: date
    monto_declarado: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    monto_sistema: Decimal = Field(ge=0, max_digits=12, decimal_places=2)


class AlertaResumenOut(BaseModel):
    id: int
    tipo: str
    estado: str
    detalle: str | None


class CierreOut(BaseModel):
    id: int
    fecha: date
    tienda_id: int
    tienda: str
    cajero_id: int
    cajero: str
    monto_declarado: Decimal
    monto_sistema: Decimal
    diferencia: Decimal
    porcentaje_diferencia: Decimal
    registrado_por: str | None
    alertas: list[AlertaResumenOut]


class AlertaOut(BaseModel):
    id: int
    tipo: str
    estado: str
    detalle: str | None
    creada_en: datetime
    cierre_id: int
    fecha_cierre: date
    tienda: str
    cajero_id: int
    cajero: str


class HistorialOut(BaseModel):
    estado_anterior: str | None
    estado_nuevo: str
    gestionado_por: str
    comentario: str | None
    fecha: datetime


class AlertaDetalleOut(AlertaOut):
    monto_declarado: Decimal
    monto_sistema: Decimal
    historial: list[HistorialOut]


class GestionAlertaIn(BaseModel):
    estado: Literal["revisada", "descartada"]
    comentario: str = Field(min_length=5, max_length=255)
