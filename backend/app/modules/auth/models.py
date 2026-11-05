"""Modelo de usuarios del portal (credenciales y rol)."""

from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.modules.organizacion.models import Colaborador

ROLES = ("administrador", "jefe_departamento", "colaborador")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[str] = mapped_column(String(20))
    activo: Mapped[bool] = mapped_column(default=True)
    creado_en: Mapped[datetime] = mapped_column(server_default=func.now())

    colaborador: Mapped[Colaborador] = relationship()

    @property
    def puede_iniciar_sesion(self) -> bool:
        """El acceso exige cuenta activa Y colaborador activo en la empresa."""
        return self.activo and self.colaborador.estado == "activo"
