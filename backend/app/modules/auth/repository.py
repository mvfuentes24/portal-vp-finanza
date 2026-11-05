"""Acceso a datos de usuarios."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.modules.auth.models import Usuario
from app.modules.organizacion.models import Cargo, Colaborador


def _consulta_usuario():
    # Carga en la misma consulta el colaborador, su cargo y su departamento,
    # que se necesitan para conocer el alcance del usuario.
    return select(Usuario).options(
        joinedload(Usuario.colaborador)
        .joinedload(Colaborador.cargo)
        .joinedload(Cargo.departamento)
    )


def obtener_por_correo(db: Session, correo: str) -> Usuario | None:
    consulta = _consulta_usuario().join(Usuario.colaborador).where(
        func.lower(Colaborador.correo) == correo.lower()
    )
    return db.scalars(consulta).first()


def obtener_por_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.scalars(_consulta_usuario().where(Usuario.id == usuario_id)).first()
