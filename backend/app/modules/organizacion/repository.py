"""Acceso a datos de departamentos y colaboradores."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.modules.organizacion.models import Cargo, Colaborador, Departamento


def listar_departamentos(db: Session, ids: list[int] | None) -> list[tuple[Departamento, int]]:
    """Departamentos con su cantidad de colaboradores activos. ids=None devuelve todos."""
    activos = (
        select(Cargo.departamento_id, func.count(Colaborador.id).label("total"))
        .join(Colaborador, Colaborador.cargo_id == Cargo.id)
        .where(Colaborador.estado == "activo")
        .group_by(Cargo.departamento_id)
        .subquery()
    )
    consulta = (
        select(Departamento, func.coalesce(activos.c.total, 0))
        .outerjoin(activos, activos.c.departamento_id == Departamento.id)
        .order_by(Departamento.nombre)
    )
    if ids is not None:
        consulta = consulta.where(Departamento.id.in_(ids))
    return [(d, total) for d, total in db.execute(consulta).all()]


def obtener_departamento(db: Session, departamento_id: int) -> Departamento | None:
    return db.get(Departamento, departamento_id)


def _consulta_colaboradores():
    return select(Colaborador).options(
        joinedload(Colaborador.pais),
        joinedload(Colaborador.cargo).joinedload(Cargo.nivel),
        joinedload(Colaborador.cargo).joinedload(Cargo.departamento),
    )


def listar_colaboradores(
    db: Session, departamento_id: int, incluir_inactivos: bool
) -> list[Colaborador]:
    consulta = (
        _consulta_colaboradores()
        .join(Colaborador.cargo)
        .where(Cargo.departamento_id == departamento_id)
        .order_by(Colaborador.apellido, Colaborador.nombre)
    )
    if not incluir_inactivos:
        consulta = consulta.where(Colaborador.estado == "activo")
    return list(db.scalars(consulta).all())


def obtener_colaborador(db: Session, colaborador_id: int) -> Colaborador | None:
    return db.scalars(
        _consulta_colaboradores().where(Colaborador.id == colaborador_id)
    ).first()
