"""Acceso a datos del módulo de cierres de caja."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.modules.auth.models import Usuario
from app.modules.cierres_caja.models import Alerta, AlertaHistorial, Cajero, CierreCaja, Tienda
from app.modules.cierres_caja.rules import FUERA_RANGO, REINCIDENCIA, TRANSPOSICION
from app.modules.organizacion.models import Colaborador


def listar_tiendas(db: Session) -> list[Tienda]:
    return list(db.scalars(select(Tienda).options(joinedload(Tienda.pais)).order_by(Tienda.nombre)))


def listar_cajeros(db: Session) -> list[Cajero]:
    return list(db.scalars(select(Cajero).options(joinedload(Cajero.tienda)).order_by(Cajero.nombre)))


def obtener_tienda(db: Session, tienda_id: int) -> Tienda | None:
    return db.get(Tienda, tienda_id)


def obtener_cajero(db: Session, cajero_id: int) -> Cajero | None:
    return db.get(Cajero, cajero_id)


def _consulta_cierres():
    return select(CierreCaja).options(
        joinedload(CierreCaja.tienda),
        joinedload(CierreCaja.cajero),
        joinedload(CierreCaja.registrado_por_usuario)
        .joinedload(Usuario.colaborador),
        selectinload(CierreCaja.alertas),
    )


def listar_cierres(
    db: Session, cajero_id: int | None, tienda_id: int | None, solo_con_alertas: bool
) -> list[CierreCaja]:
    consulta = _consulta_cierres().order_by(CierreCaja.fecha.desc(), CierreCaja.id.desc())
    if cajero_id is not None:
        consulta = consulta.where(CierreCaja.cajero_id == cajero_id)
    if tienda_id is not None:
        consulta = consulta.where(CierreCaja.tienda_id == tienda_id)
    if solo_con_alertas:
        consulta = consulta.where(CierreCaja.alertas.any())
    return list(db.scalars(consulta).unique().all())


def listar_cierres_cronologico(db: Session) -> list[CierreCaja]:
    return list(db.scalars(select(CierreCaja).order_by(CierreCaja.fecha, CierreCaja.id)))


def obtener_cierre(db: Session, cierre_id: int) -> CierreCaja | None:
    return db.scalars(_consulta_cierres().where(CierreCaja.id == cierre_id)).first()


def tipos_de_alerta_del_cierre(db: Session, cierre_id: int) -> set[str]:
    return set(db.scalars(select(Alerta.tipo).where(Alerta.cierre_id == cierre_id)))


def fechas_con_anomalia(db: Session, cajero_id: int, hasta: date) -> list[date]:
    """Fechas de los cierres del cajero con alertas de fuera de rango o transposición
    que no fueron descartadas (un cierre con dos alertas cuenta una sola vez)."""
    consulta = (
        select(CierreCaja.id, CierreCaja.fecha)
        .join(Alerta, Alerta.cierre_id == CierreCaja.id)
        .where(
            CierreCaja.cajero_id == cajero_id,
            CierreCaja.fecha <= hasta,
            Alerta.tipo.in_([FUERA_RANGO, TRANSPOSICION]),
            Alerta.estado != "descartada",
        )
        .distinct()
    )
    return [fecha for _, fecha in db.execute(consulta).all()]


def existe_reincidencia_activa(db: Session, cajero_id: int, desde: date, hasta: date) -> bool:
    """True si ya hay una alerta de reincidencia no descartada para el cajero en ese período."""
    consulta = (
        select(Alerta.id)
        .join(CierreCaja, Alerta.cierre_id == CierreCaja.id)
        .where(
            CierreCaja.cajero_id == cajero_id,
            CierreCaja.fecha.between(desde, hasta),
            Alerta.tipo == REINCIDENCIA,
            Alerta.estado != "descartada",
        )
    )
    return db.scalars(consulta).first() is not None


def _consulta_alertas():
    return select(Alerta).options(
        joinedload(Alerta.cierre).joinedload(CierreCaja.tienda),
        joinedload(Alerta.cierre).joinedload(CierreCaja.cajero),
    )


def listar_alertas(
    db: Session, estado: str | None, tipo: str | None, cajero_id: int | None
) -> list[Alerta]:
    consulta = _consulta_alertas().join(Alerta.cierre).order_by(Alerta.id.desc())
    if estado is not None:
        consulta = consulta.where(Alerta.estado == estado)
    if tipo is not None:
        consulta = consulta.where(Alerta.tipo == tipo)
    if cajero_id is not None:
        consulta = consulta.where(CierreCaja.cajero_id == cajero_id)
    return list(db.scalars(consulta).unique().all())


def obtener_alerta(db: Session, alerta_id: int, bloquear: bool = False) -> Alerta | None:
    """Obtiene una alerta con su historial.

    Con bloquear=True, la fila queda bloqueada hasta terminar la transacción: si dos
    personas intentan gestionar la misma alerta a la vez, la segunda espera y luego
    ve el estado ya actualizado, en vez de sobrescribir la decisión de la primera.
    """
    consulta = _consulta_alertas().options(
        selectinload(Alerta.historial)
        .joinedload(AlertaHistorial.usuario)
        .joinedload(Usuario.colaborador)
    ).where(Alerta.id == alerta_id)
    if bloquear:
        consulta = consulta.with_for_update(of=Alerta)
    return db.scalars(consulta).first()


def nombre_usuario(usuario: Usuario | None) -> str | None:
    if usuario is None:
        return None
    colaborador: Colaborador = usuario.colaborador
    return f"{colaborador.nombre} {colaborador.apellido}"
