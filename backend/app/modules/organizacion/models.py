"""Modelos de la estructura organizacional (reflejan las tablas de database/schema.sql)."""

from datetime import date

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# Tabla intermedia de la relación muchos a muchos entre cargos y funciones
cargo_funciones = Table(
    "cargo_funciones",
    Base.metadata,
    Column("cargo_id", ForeignKey("cargos.id"), primary_key=True),
    Column("funcion_id", ForeignKey("funciones.id"), primary_key=True),
)


class Pais(Base):
    __tablename__ = "paises"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60))


class Departamento(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(255))

    cargos: Mapped[list["Cargo"]] = relationship(back_populates="departamento")


class Nivel(Base):
    __tablename__ = "niveles"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30))


class Funcion(Base):
    __tablename__ = "funciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(String(255))


class Cargo(Base):
    __tablename__ = "cargos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    nivel_id: Mapped[int] = mapped_column(ForeignKey("niveles.id"))
    # NULL solo para el cargo de Vicepresidente de Finanzas
    departamento_id: Mapped[int | None] = mapped_column(ForeignKey("departamentos.id"))

    nivel: Mapped[Nivel] = relationship()
    departamento: Mapped[Departamento | None] = relationship(back_populates="cargos")
    funciones: Mapped[list[Funcion]] = relationship(secondary=cargo_funciones)


class Colaborador(Base):
    __tablename__ = "colaboradores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    apellido: Mapped[str] = mapped_column(String(80))
    correo: Mapped[str] = mapped_column(String(150))
    pais_id: Mapped[int] = mapped_column(ForeignKey("paises.id"))
    fecha_ingreso: Mapped[date]
    estado: Mapped[str] = mapped_column(String(10))
    cargo_id: Mapped[int] = mapped_column(ForeignKey("cargos.id"))

    pais: Mapped[Pais] = relationship()
    cargo: Mapped[Cargo] = relationship()

    @property
    def departamento_id(self) -> int | None:
        """El departamento se obtiene a través del cargo (no se guarda en el colaborador)."""
        return self.cargo.departamento_id
