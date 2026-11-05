"""Endpoints del módulo de cargos (solo lectura)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_usuario_actual
from app.modules.auth.models import Usuario
from app.modules.cargos import service
from app.modules.cargos.schemas import CargoOut

router = APIRouter(prefix="/cargos", tags=["Cargos"])


@router.get("", response_model=list[CargoOut])
def listar_cargos(usuario: Usuario = Depends(get_usuario_actual), db: Session = Depends(get_db)):
    return service.listar_cargos(db, usuario)


@router.get("/{cargo_id}", response_model=CargoOut)
def obtener_cargo(
    cargo_id: int,
    usuario: Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_db),
):
    return service.obtener_cargo(db, usuario, cargo_id)
