"""Acceso a datos de cargos."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.modules.organizacion.models import Cargo, Colaborador, Departamento


def _consulta_cargos():
    return select(Cargo).options(
        joinedload(Cargo.nivel),
        joinedload(Cargo.departamento),
        selectinload(Cargo.funciones),
    )


def listar_cargos(db: Session, departamento_ids: list[int] | None) -> list[Cargo]:
    """Cargos ordenados por departamento y nivel. departamento_ids=None devuelve todos."""
    consulta = (
        _consulta_cargos()
        .outerjoin(Cargo.departamento)
        .order_by(Departamento.nombre.nulls_first(), Cargo.nivel_id.desc())
    )
    if departamento_ids is not None:
        consulta = consulta.where(Cargo.departamento_id.in_(departamento_ids))
    return list(db.scalars(consulta).unique().all())


def obtener_cargo(db: Session, cargo_id: int) -> Cargo | None:
    return db.scalars(_consulta_cargos().where(Cargo.id == cargo_id)).first()


def contar_colaboradores_activos(db: Session, cargo_ids: list[int]) -> dict[int, int]:
    """Cantidad de colaboradores activos por cargo, en una sola consulta."""
    if not cargo_ids:
        return {}
    consulta = (
        select(Colaborador.cargo_id, func.count(Colaborador.id))
        .where(Colaborador.cargo_id.in_(cargo_ids), Colaborador.estado == "activo")
        .group_by(Colaborador.cargo_id)
    )
    return dict(db.execute(consulta).all())
