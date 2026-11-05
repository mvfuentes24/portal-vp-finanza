"""Datos que devuelve el módulo de cargos."""

from pydantic import BaseModel


class CargoOut(BaseModel):
    id: int
    nombre: str
    nivel: str
    departamento_id: int | None
    departamento: str
    funciones: list[str]
    # Colaboradores activos que ocupan el cargo
    total_colaboradores: int
