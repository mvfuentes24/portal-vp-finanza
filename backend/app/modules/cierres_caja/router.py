"""Endpoints del módulo de cierres de caja.

Acceso (el módulo pertenece a Contraloría):
- Consultar: administradora y cualquier usuario de Contraloría.
- Registrar cierres y gestionar alertas: administradora y jefe de Contraloría.
"""

from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import PROHIBIDO, puede_consultar_cierres, puede_gestionar_cierres
from app.modules.auth.dependencies import get_usuario_actual
from app.modules.auth.models import Usuario
from app.modules.cierres_caja import service
from app.modules.cierres_caja.schemas import (
    AlertaDetalleOut,
    AlertaOut,
    CajeroOut,
    CierreIn,
    CierreOut,
    GestionAlertaIn,
    TiendaOut,
)

router = APIRouter(prefix="/cierres-caja", tags=["Cierres de caja"])


def puede_consultar(usuario: Usuario = Depends(get_usuario_actual)) -> Usuario:
    if not puede_consultar_cierres(usuario):
        raise PROHIBIDO
    return usuario


def puede_gestionar(usuario: Usuario = Depends(get_usuario_actual)) -> Usuario:
    if not puede_gestionar_cierres(usuario):
        raise PROHIBIDO
    return usuario


# --- Catálogos para el formulario de registro ---

@router.get("/tiendas", response_model=list[TiendaOut])
def listar_tiendas(_: Usuario = Depends(puede_consultar), db: Session = Depends(get_db)):
    return service.listar_tiendas(db)


@router.get("/cajeros", response_model=list[CajeroOut])
def listar_cajeros(_: Usuario = Depends(puede_consultar), db: Session = Depends(get_db)):
    return service.listar_cajeros(db)


# --- Cierres ---

@router.get("/cierres", response_model=list[CierreOut])
def listar_cierres(
    cajero_id: int | None = None,
    tienda_id: int | None = None,
    solo_con_alertas: bool = False,
    _: Usuario = Depends(puede_consultar),
    db: Session = Depends(get_db),
):
    return service.listar_cierres(db, cajero_id, tienda_id, solo_con_alertas)


@router.get("/cierres/{cierre_id}", response_model=CierreOut)
def obtener_cierre(cierre_id: int, _: Usuario = Depends(puede_consultar), db: Session = Depends(get_db)):
    return service.obtener_cierre(db, cierre_id)


@router.post("/cierres", response_model=CierreOut, status_code=status.HTTP_201_CREATED)
def registrar_cierre(
    datos: CierreIn, usuario: Usuario = Depends(puede_gestionar), db: Session = Depends(get_db)
):
    return service.registrar_cierre(db, usuario, datos)


# --- Alertas ---

@router.get("/alertas", response_model=list[AlertaOut])
def listar_alertas(
    estado: Literal["pendiente", "revisada", "descartada"] | None = None,
    tipo: Literal["fuera_rango", "transposicion", "reincidencia"] | None = None,
    cajero_id: int | None = Query(default=None),
    _: Usuario = Depends(puede_consultar),
    db: Session = Depends(get_db),
):
    return service.listar_alertas(db, estado, tipo, cajero_id)


@router.get("/alertas/{alerta_id}", response_model=AlertaDetalleOut)
def obtener_alerta(alerta_id: int, _: Usuario = Depends(puede_consultar), db: Session = Depends(get_db)):
    return service.obtener_alerta(db, alerta_id)


@router.patch("/alertas/{alerta_id}", response_model=AlertaDetalleOut)
def gestionar_alerta(
    alerta_id: int,
    datos: GestionAlertaIn,
    usuario: Usuario = Depends(puede_gestionar),
    db: Session = Depends(get_db),
):
    return service.gestionar_alerta(db, usuario, alerta_id, datos)
