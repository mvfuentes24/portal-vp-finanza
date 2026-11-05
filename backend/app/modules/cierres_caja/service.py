"""Lógica de negocio del detector de anomalías en cierres de caja."""

from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.auth.models import Usuario
from app.modules.cierres_caja import repository, rules
from app.modules.cierres_caja.models import Alerta, AlertaHistorial, CierreCaja
from app.modules.cierres_caja.schemas import (
    AlertaDetalleOut,
    AlertaOut,
    AlertaResumenOut,
    CajeroOut,
    CierreIn,
    CierreOut,
    GestionAlertaIn,
    HistorialOut,
    TiendaOut,
)

COMENTARIO_SISTEMA = "Alerta generada automáticamente por el detector de anomalías"


# --------------------------------------------------------------------------
# Detección de anomalías
# --------------------------------------------------------------------------

def _crear_alerta(db: Session, cierre: CierreCaja, tipo: str, detalle: str) -> Alerta:
    """Crea la alerta en estado pendiente y registra su creación en el historial."""
    alerta = Alerta(cierre_id=cierre.id, tipo=tipo, detalle=detalle, estado="pendiente")
    db.add(alerta)
    db.flush()  # obtiene el id de la alerta para el historial
    db.add(
        AlertaHistorial(
            alerta_id=alerta.id,
            estado_anterior=None,
            estado_nuevo="pendiente",
            usuario_id=None,  # la crea el sistema
            comentario=COMENTARIO_SISTEMA,
        )
    )
    return alerta


def analizar_cierre(db: Session, cierre: CierreCaja) -> list[Alerta]:
    """Aplica las tres reglas al cierre y crea las alertas que correspondan.

    Es idempotente: si el cierre ya tiene una alerta de un tipo, no la duplica.
    """
    existentes = repository.tipos_de_alerta_del_cierre(db, cierre.id)
    nuevas: list[Alerta] = []
    declarado, sistema = cierre.monto_declarado, cierre.monto_sistema

    if rules.FUERA_RANGO not in existentes and rules.es_fuera_de_rango(declarado, sistema):
        porcentaje = rules.porcentaje_diferencia(declarado, sistema)
        nuevas.append(_crear_alerta(
            db, cierre, rules.FUERA_RANGO,
            f"Diferencia de {abs(declarado - sistema):.2f} ({porcentaje:.2f} %), "
            f"supera el umbral de {rules.UMBRAL_PORCENTAJE} %",
        ))

    if rules.TRANSPOSICION not in existentes and rules.es_transposicion(declarado, sistema):
        nuevas.append(_crear_alerta(
            db, cierre, rules.TRANSPOSICION,
            f"Posible transposición de dígitos: declarado {declarado:.2f}, sistema {sistema:.2f}",
        ))

    db.flush()  # las alertas recién creadas deben contar para la reincidencia
    _analizar_reincidencia(db, cierre, existentes, nuevas)
    return nuevas


def _analizar_reincidencia(
    db: Session, cierre: CierreCaja, existentes: set[str], nuevas: list[Alerta]
) -> None:
    tiene_anomalia = bool(nuevas) or bool(existentes & {rules.FUERA_RANGO, rules.TRANSPOSICION})
    if not tiene_anomalia or rules.REINCIDENCIA in existentes:
        return

    fechas = repository.fechas_con_anomalia(db, cierre.cajero_id, hasta=cierre.fecha)
    if not rules.es_reincidencia(fechas, cierre.fecha):
        return

    inicio = cierre.fecha - timedelta(days=rules.REINCIDENCIA_VENTANA_DIAS)
    # Una sola alerta de reincidencia por período, para no repetirla en cada cierre siguiente
    if repository.existe_reincidencia_activa(db, cierre.cajero_id, inicio, cierre.fecha):
        return

    en_ventana = sorted(f for f in fechas if inicio <= f <= cierre.fecha)
    nuevas.append(_crear_alerta(
        db, cierre, rules.REINCIDENCIA,
        f"El cajero acumula {len(en_ventana)} cierres con anomalías "
        f"entre {en_ventana[0]:%d/%m/%Y} y {en_ventana[-1]:%d/%m/%Y}",
    ))


def analizar_todos(db: Session) -> int:
    """Analiza todos los cierres en orden cronológico. Devuelve las alertas creadas."""
    total = 0
    for cierre in repository.listar_cierres_cronologico(db):
        total += len(analizar_cierre(db, cierre))
    db.commit()
    return total


# --------------------------------------------------------------------------
# Registro y consulta de cierres
# --------------------------------------------------------------------------

def listar_tiendas(db: Session) -> list[TiendaOut]:
    return [TiendaOut(id=t.id, nombre=t.nombre, pais=t.pais.nombre) for t in repository.listar_tiendas(db)]


def listar_cajeros(db: Session) -> list[CajeroOut]:
    return [
        CajeroOut(id=c.id, nombre=c.nombre, tienda_id=c.tienda_id, tienda=c.tienda.nombre)
        for c in repository.listar_cajeros(db)
    ]


def registrar_cierre(db: Session, usuario: Usuario, datos: CierreIn) -> CierreOut:
    if repository.obtener_tienda(db, datos.tienda_id) is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "La tienda indicada no existe")
    if repository.obtener_cajero(db, datos.cajero_id) is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "El cajero indicado no existe")
    if datos.fecha > date.today():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "La fecha del cierre no puede ser futura")

    cierre = CierreCaja(
        tienda_id=datos.tienda_id,
        cajero_id=datos.cajero_id,
        fecha=datos.fecha,
        monto_declarado=datos.monto_declarado,
        monto_sistema=datos.monto_sistema,
        registrado_por=usuario.id,
    )
    db.add(cierre)
    db.flush()
    analizar_cierre(db, cierre)  # la detección ocurre en la misma transacción que el registro
    db.commit()
    return obtener_cierre(db, cierre.id)


def listar_cierres(
    db: Session, cajero_id: int | None, tienda_id: int | None, solo_con_alertas: bool
) -> list[CierreOut]:
    return [a_cierre_out(c) for c in repository.listar_cierres(db, cajero_id, tienda_id, solo_con_alertas)]


def obtener_cierre(db: Session, cierre_id: int) -> CierreOut:
    cierre = repository.obtener_cierre(db, cierre_id)
    if cierre is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cierre no encontrado")
    return a_cierre_out(cierre)


# --------------------------------------------------------------------------
# Consulta y gestión de alertas
# --------------------------------------------------------------------------

def listar_alertas(
    db: Session, estado: str | None, tipo: str | None, cajero_id: int | None
) -> list[AlertaOut]:
    return [a_alerta_out(a) for a in repository.listar_alertas(db, estado, tipo, cajero_id)]


def obtener_alerta(db: Session, alerta_id: int) -> AlertaDetalleOut:
    alerta = repository.obtener_alerta(db, alerta_id)
    if alerta is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alerta no encontrada")
    return a_alerta_detalle_out(alerta)


def gestionar_alerta(
    db: Session, usuario: Usuario, alerta_id: int, datos: GestionAlertaIn
) -> AlertaDetalleOut:
    """Marca una alerta pendiente como revisada o descartada y lo registra en el historial."""
    alerta = repository.obtener_alerta(db, alerta_id, bloquear=True)
    if alerta is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alerta no encontrada")
    if alerta.estado != "pendiente":
        # Una decisión ya tomada no se puede reescribir
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"La alerta ya fue gestionada (estado actual: {alerta.estado})",
        )

    # Se agrega a través de la relación para que el historial ya cargado
    # en memoria también incluya la nueva entrada.
    alerta.historial.append(
        AlertaHistorial(
            estado_anterior=alerta.estado,
            estado_nuevo=datos.estado,
            usuario_id=usuario.id,
            comentario=datos.comentario.strip(),
        )
    )
    alerta.estado = datos.estado
    db.commit()
    return obtener_alerta(db, alerta_id)


# --------------------------------------------------------------------------
# Conversión a esquemas de salida
# --------------------------------------------------------------------------

def a_cierre_out(c: CierreCaja) -> CierreOut:
    return CierreOut(
        id=c.id,
        fecha=c.fecha,
        tienda_id=c.tienda_id,
        tienda=c.tienda.nombre,
        cajero_id=c.cajero_id,
        cajero=c.cajero.nombre,
        monto_declarado=c.monto_declarado,
        monto_sistema=c.monto_sistema,
        diferencia=c.monto_declarado - c.monto_sistema,
        porcentaje_diferencia=round(rules.porcentaje_diferencia(c.monto_declarado, c.monto_sistema), 2),
        registrado_por=repository.nombre_usuario(c.registrado_por_usuario),
        alertas=[AlertaResumenOut(id=a.id, tipo=a.tipo, estado=a.estado, detalle=a.detalle) for a in c.alertas],
    )


def a_alerta_out(a: Alerta) -> AlertaOut:
    return AlertaOut(
        id=a.id,
        tipo=a.tipo,
        estado=a.estado,
        detalle=a.detalle,
        creada_en=a.creada_en,
        cierre_id=a.cierre_id,
        fecha_cierre=a.cierre.fecha,
        tienda=a.cierre.tienda.nombre,
        cajero_id=a.cierre.cajero_id,
        cajero=a.cierre.cajero.nombre,
    )


def a_alerta_detalle_out(a: Alerta) -> AlertaDetalleOut:
    return AlertaDetalleOut(
        **a_alerta_out(a).model_dump(),
        monto_declarado=a.cierre.monto_declarado,
        monto_sistema=a.cierre.monto_sistema,
        historial=[
            HistorialOut(
                estado_anterior=h.estado_anterior,
                estado_nuevo=h.estado_nuevo,
                gestionado_por=repository.nombre_usuario(h.usuario) or "Sistema",
                comentario=h.comentario,
                fecha=h.fecha,
            )
            for h in a.historial
        ],
    )
