"""Endpoints de autenticación: iniciar sesión, cerrar sesión y usuario actual."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token
from app.modules.auth import service
from app.modules.auth.dependencies import COOKIE_SESION, get_usuario_actual
from app.modules.auth.models import Usuario
from app.modules.auth.schemas import LoginIn, UsuarioActualOut

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=UsuarioActualOut)
def login(datos: LoginIn, response: Response, db: Session = Depends(get_db)):
    usuario = service.autenticar(db, datos.correo, datos.password)
    if usuario is None:
        # Mensaje genérico: no indica si falló el correo o la contraseña
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    # El token viaja en una cookie httpOnly: el JavaScript del navegador
    # no puede leerla, lo que protege la sesión frente a ataques XSS.
    response.set_cookie(
        key=COOKIE_SESION,
        value=create_access_token(usuario.id),
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )
    return service.a_usuario_actual(usuario)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie(key=COOKIE_SESION, path="/")


@router.get("/me", response_model=UsuarioActualOut)
def usuario_actual(usuario: Usuario = Depends(get_usuario_actual)):
    return service.a_usuario_actual(usuario)
