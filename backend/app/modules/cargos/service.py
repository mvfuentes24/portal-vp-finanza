"""Reglas del módulo de cargos."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import departamentos_visibles, verificar_acceso_departamento
from app.modules.auth.models import Usuario
from app.modules.cargos import repository
from app.modules.cargos.schemas import CargoOut
from app.modules.organizacion.models import Cargo


def listar_cargos(db: Session, usuario: Usuario) -> list[CargoOut]:
    cargos = repository.listar_cargos(db, departamentos_visibles(usuario))
    totales = repository.contar_colaboradores_activos(db, [c.id for c in cargos])
    return [a_cargo_out(c, totales.get(c.id, 0)) for c in cargos]


def obtener_cargo(db: Session, usuario: Usuario, cargo_id: int) -> CargoOut:
    cargo = repository.obtener_cargo(db, cargo_id)
    if cargo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo no encontrado")
    # El cargo de Vicepresidente (sin departamento) solo lo ve la administradora
    verificar_acceso_departamento(usuario, cargo.departamento_id)
    totales = repository.contar_colaboradores_activos(db, [cargo.id])
    return a_cargo_out(cargo, totales.get(cargo.id, 0))


def a_cargo_out(c: Cargo, total_colaboradores: int) -> CargoOut:
    return CargoOut(
        id=c.id,
        nombre=c.nombre,
        nivel=c.nivel.nombre,
        departamento_id=c.departamento_id,
        departamento=c.departamento.nombre if c.departamento else "Vicepresidencia de Finanzas",
        funciones=sorted(f.descripcion for f in c.funciones),
        total_colaboradores=total_colaboradores,
    )
