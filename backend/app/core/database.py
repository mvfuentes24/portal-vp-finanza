"""Conexión a PostgreSQL mediante SQLAlchemy."""

from collections.abc import Iterator

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

# URL.create arma la dirección de conexión escapando correctamente
# los caracteres especiales que pueda tener la contraseña.
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password.get_secret_value(),
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos (tablas)."""


def get_db() -> Iterator[Session]:
    """Entrega una sesión de base de datos por petición y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
