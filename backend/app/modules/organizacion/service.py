"""Reglas del módulo de organización: qué ve cada rol."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import (
    COLABORADOR,
    departamentos_visibles,
    verificar_acceso_departamento,
)
from app.modules.auth.models import Usuario
from app.modules.organizacion import repository
from app.modules.organizacion.models import Colaborador
from app.modules.organizacion.schemas import ColaboradorOut, DepartamentoOut

NO_ENCONTRADO = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento no encontrado")


def listar_departamentos(db: Session, usuario: Usuario) -> list[DepartamentoOut]:
    filas = repository.listar_departamentos(db, departamentos_visibles(usuario))
    return [
        DepartamentoOut(id=d.id, nombre=d.nombre, descripcion=d.descripcion, total_colaboradores=total)
        for d, total in filas
    ]


def obtener_departamento(db: Session, usuario: Usuario, departamento_id: int) -> DepartamentoOut:
    if repository.obtener_departamento(db, departamento_id) is None:
        raise NO_ENCONTRADO
    verificar_acceso_departamento(usuario, departamento_id)
    return next(d for d in listar_departamentos(db, usuario) if d.id == departamento_id)


def listar_colaboradores(db: Session, usuario: Usuario, departamento_id: int) -> list[ColaboradorOut]:
    if repository.obtener_departamento(db, departamento_id) is None:
        raise NO_ENCONTRADO
    verificar_acceso_departamento(usuario, departamento_id)

    # Los colaboradores ven solo a sus compañeros activos, con datos de directorio.
    # Jefes y administradora ven a todos, con la ficha completa.
    solo_directorio = usuario.rol == COLABORADOR
    colaboradores = repository.listar_colaboradores(
        db, departamento_id, incluir_inactivos=not solo_directorio
    )
    return [ficha(c) if not solo_directorio else directorio(c) for c in colaboradores]


def mi_perfil(usuario: Usuario) -> ColaboradorOut:
    """Cualquier usuario puede ver su propia ficha completa."""
    return ficha(usuario.colaborador)


def directorio(c: Colaborador) -> ColaboradorOut:
    return ColaboradorOut(
        id=c.id, nombre=c.nombre, apellido=c.apellido, correo=c.correo, cargo=c.cargo.nombre
    )


def ficha(c: Colaborador) -> ColaboradorOut:
    departamento = c.cargo.departamento
    return ColaboradorOut(
        id=c.id,
        nombre=c.nombre,
        apellido=c.apellido,
        correo=c.correo,
        cargo=c.cargo.nombre,
        nivel=c.cargo.nivel.nombre,
        departamento=departamento.nombre if departamento else "Vicepresidencia de Finanzas",
        pais=c.pais.nombre,
        fecha_ingreso=c.fecha_ingreso,
        estado=c.estado,
    )
