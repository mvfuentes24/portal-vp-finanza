"""Datos que devuelve el módulo de organización."""

from datetime import date

from pydantic import BaseModel


class DepartamentoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    total_colaboradores: int


class ColaboradorOut(BaseModel):
    """Datos de un colaborador.

    Los campos opcionales solo se incluyen en la ficha completa (jefes y
    administradora). Los colaboradores ven a sus compañeros con datos de
    directorio: nombre, correo y cargo.
    """

    id: int
    nombre: str
    apellido: str
    correo: str
    cargo: str
    # Solo en la ficha completa
    nivel: str | None = None
    departamento: str | None = None
    pais: str | None = None
    fecha_ingreso: date | None = None
    estado: str | None = None
