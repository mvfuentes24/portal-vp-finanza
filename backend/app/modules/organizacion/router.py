"""Endpoints del módulo de organización (solo lectura)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_usuario_actual
from app.modules.auth.models import Usuario
from app.modules.organizacion import service
from app.modules.organizacion.schemas import ColaboradorOut, DepartamentoOut

router = APIRouter(prefix="/organizacion", tags=["Organización"])


@router.get("/departamentos", response_model=list[DepartamentoOut])
def listar_departamentos(
    usuario: Usuario = Depends(get_usuario_actual), db: Session = Depends(get_db)
):
    return service.listar_departamentos(db, usuario)


@router.get("/departamentos/{departamento_id}", response_model=DepartamentoOut)
def obtener_departamento(
    departamento_id: int,
    usuario: Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_db),
):
    return service.obtener_departamento(db, usuario, departamento_id)


@router.get(
    "/departamentos/{departamento_id}/colaboradores",
    response_model=list[ColaboradorOut],
    response_model_exclude_none=True,
)
def listar_colaboradores(
    departamento_id: int,
    usuario: Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_db),
):
    return service.listar_colaboradores(db, usuario, departamento_id)


@router.get("/mi-perfil", response_model=ColaboradorOut)
def mi_perfil(usuario: Usuario = Depends(get_usuario_actual)):
    return service.mi_perfil(usuario)
