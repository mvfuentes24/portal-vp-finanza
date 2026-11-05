"""Control de acceso por rol y por alcance (departamento).

Todas las reglas de acceso del portal pasan por este archivo, para que
estén en un solo lugar y se apliquen igual en todos los módulos.
"""

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.modules.auth.dependencies import get_usuario_actual
from app.modules.auth.models import Usuario

ADMINISTRADOR = "administrador"
JEFE = "jefe_departamento"
COLABORADOR = "colaborador"

PROHIBIDO = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No tienes permiso para acceder a este recurso",
)


def requiere_roles(*roles: str) -> Callable[..., Usuario]:
    """Dependencia que solo deja pasar a usuarios con alguno de los roles indicados."""

    def verificar(usuario: Usuario = Depends(get_usuario_actual)) -> Usuario:
        if usuario.rol not in roles:
            raise PROHIBIDO
        return usuario

    return verificar


def es_administrador(usuario: Usuario) -> bool:
    return usuario.rol == ADMINISTRADOR


def departamento_del_usuario(usuario: Usuario) -> int | None:
    """Departamento del usuario, obtenido a través de su cargo."""
    return usuario.colaborador.departamento_id


def departamentos_visibles(usuario: Usuario) -> list[int] | None:
    """Departamentos que el usuario puede consultar. None significa "todos"."""
    if es_administrador(usuario):
        return None
    departamento = departamento_del_usuario(usuario)
    return [departamento] if departamento is not None else []


def verificar_acceso_departamento(usuario: Usuario, departamento_id: int | None) -> None:
    """Responde 403 si el usuario no puede ver datos de ese departamento.

    El administrador accede a todo. Los demás roles, solo a su propio departamento.
    """
    if es_administrador(usuario):
        return
    if departamento_id is None or departamento_id != departamento_del_usuario(usuario):
        raise PROHIBIDO
