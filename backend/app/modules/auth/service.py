"""Lógica de inicio de sesión."""

from sqlalchemy.orm import Session

from app.core.permissions import modulos_del_usuario, puede_gestionar_cierres
from app.core.security import HASH_FICTICIO, verify_password
from app.modules.auth import repository
from app.modules.auth.models import Usuario
from app.modules.auth.schemas import UsuarioActualOut


def autenticar(db: Session, correo: str, password: str) -> Usuario | None:
    """Devuelve el usuario si las credenciales son correctas y tiene acceso; si no, None.

    No distingue entre "el correo no existe", "contraseña incorrecta" o
    "usuario inactivo": en todos los casos el resultado es el mismo,
    para no revelar qué correos están registrados.
    """
    usuario = repository.obtener_por_correo(db, correo.strip())
    if usuario is None:
        verify_password(password, HASH_FICTICIO)  # iguala el tiempo de respuesta
        return None
    if not verify_password(password, usuario.password_hash):
        return None
    if not usuario.puede_iniciar_sesion:
        return None
    return usuario


def a_usuario_actual(usuario: Usuario) -> UsuarioActualOut:
    colaborador = usuario.colaborador
    departamento = colaborador.cargo.departamento
    return UsuarioActualOut(
        id=usuario.id,
        nombre=f"{colaborador.nombre} {colaborador.apellido}",
        correo=colaborador.correo,
        rol=usuario.rol,
        cargo=colaborador.cargo.nombre,
        departamento_id=departamento.id if departamento else None,
        departamento=departamento.nombre if departamento else None,
        modulos=modulos_del_usuario(usuario),
        puede_gestionar_cierres=puede_gestionar_cierres(usuario),
    )
