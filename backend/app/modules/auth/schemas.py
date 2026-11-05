"""Datos que entran y salen del módulo de autenticación."""

from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    correo: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=1, max_length=128)


class UsuarioActualOut(BaseModel):
    """Información del usuario autenticado. Nunca incluye el hash de la contraseña."""

    id: int
    nombre: str
    correo: str
    rol: str
    cargo: str
    departamento_id: int | None
    departamento: str | None
    # Lo decide el backend con las mismas reglas que protegen los endpoints;
    # el frontend solo lo usa para mostrar u ocultar opciones.
    modulos: list[str]
    puede_gestionar_cierres: bool
