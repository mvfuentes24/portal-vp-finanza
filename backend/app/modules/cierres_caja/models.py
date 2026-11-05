"""Modelos del módulo de cierres de caja (reflejan las tablas de database/schema.sql)."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.modules.auth.models import Usuario
from app.modules.organizacion.models import Pais


class Tienda(Base):
    __tablename__ = "tiendas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    pais_id: Mapped[int] = mapped_column(ForeignKey("paises.id"))

    pais: Mapped[Pais] = relationship()


class Cajero(Base):
    __tablename__ = "cajeros"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id"))

    tienda: Mapped[Tienda] = relationship()


class CierreCaja(Base):
    __tablename__ = "cierres_caja"

    id: Mapped[int] = mapped_column(primary_key=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id"))
    cajero_id: Mapped[int] = mapped_column(ForeignKey("cajeros.id"))
    fecha: Mapped[date]
    monto_declarado: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    monto_sistema: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    # NULL en los cierres de la carga inicial del dataset
    registrado_por: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"))
    registrado_en: Mapped[datetime] = mapped_column(server_default=func.now())

    tienda: Mapped[Tienda] = relationship()
    cajero: Mapped[Cajero] = relationship()
    registrado_por_usuario: Mapped[Usuario | None] = relationship()
    alertas: Mapped[list["Alerta"]] = relationship(back_populates="cierre", order_by="Alerta.id")


class Alerta(Base):
    __tablename__ = "alertas"

    id: Mapped[int] = mapped_column(primary_key=True)
    cierre_id: Mapped[int] = mapped_column(ForeignKey("cierres_caja.id"))
    tipo: Mapped[str] = mapped_column(String(20))
    detalle: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(12), default="pendiente")
    creada_en: Mapped[datetime] = mapped_column(server_default=func.now())

    cierre: Mapped[CierreCaja] = relationship(back_populates="alertas")
    historial: Mapped[list["AlertaHistorial"]] = relationship(
        back_populates="alerta", order_by="AlertaHistorial.id"
    )


class AlertaHistorial(Base):
    __tablename__ = "alertas_historial"

    id: Mapped[int] = mapped_column(primary_key=True)
    alerta_id: Mapped[int] = mapped_column(ForeignKey("alertas.id"))
    estado_anterior: Mapped[str | None] = mapped_column(String(12))
    estado_nuevo: Mapped[str] = mapped_column(String(12))
    # NULL cuando la acción la realiza el sistema (creación automática)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"))
    comentario: Mapped[str | None] = mapped_column(String(255))
    fecha: Mapped[datetime] = mapped_column(server_default=func.now())

    alerta: Mapped[Alerta] = relationship(back_populates="historial")
    usuario: Mapped[Usuario | None] = relationship()
