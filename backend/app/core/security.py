"""Hash de contraseñas y tokens de sesión (JWT)."""

from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

# Argon2: algoritmo recomendado actualmente para guardar contraseñas.
# Es lento a propósito, para dificultar los ataques de fuerza bruta.
_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Devuelve el hash de una contraseña. El hash incluye su propia sal aleatoria."""
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Compara una contraseña en texto plano con un hash guardado."""
    return _hasher.verify(password, password_hash)


# Hash de una contraseña cualquiera, usado cuando el correo no existe:
# así el login tarda lo mismo exista o no el usuario, y no se puede
# averiguar qué correos están registrados midiendo el tiempo de respuesta.
HASH_FICTICIO = hash_password("contraseña-que-no-corresponde-a-nadie")


def create_access_token(usuario_id: int) -> str:
    """Crea un token firmado que identifica al usuario y expira automáticamente."""
    expira = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(usuario_id), "exp": expira}
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int | None:
    """Devuelve el id del usuario si el token es válido y no ha expirado; si no, None."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
        return int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None
