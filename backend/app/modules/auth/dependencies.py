"""Dependencia que identifica al usuario autenticado en cada petición."""

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.auth import repository
from app.modules.auth.models import Usuario

COOKIE_SESION = "sesion"


def get_usuario_actual(
    sesion: str | None = Cookie(default=None, alias=COOKIE_SESION),
    db: Session = Depends(get_db),
) -> Usuario:
    """Devuelve el usuario dueño de la sesión, o responde 401 si no hay sesión válida.

    Además de validar el token, vuelve a consultar al usuario en la base de datos:
    si fue desactivado después de iniciar sesión, pierde el acceso de inmediato.
    """
    no_autenticado = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesión no válida o expirada",
    )
    if sesion is None:
        raise no_autenticado
    usuario_id = decode_access_token(sesion)
    if usuario_id is None:
        raise no_autenticado
    usuario = repository.obtener_por_id(db, usuario_id)
    if usuario is None or not usuario.puede_iniciar_sesion:
        raise no_autenticado
    return usuario
