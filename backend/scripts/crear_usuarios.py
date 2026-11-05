"""Crea los usuarios de prueba del portal.

Uso (desde la carpeta backend, con el entorno virtual activo):
    python -m scripts.crear_usuarios

Todos los usuarios reciben la contraseña definida en la variable DEMO_PASSWORD
del archivo .env. El script se puede ejecutar varias veces: si un usuario ya
existe, no lo modifica.
"""

import sys

from sqlalchemy import select

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.modules.auth.models import Usuario
from app.modules.organizacion.models import Colaborador

LONGITUD_MINIMA = 12

# (correo del colaborador, rol)
USUARIOS_DE_PRUEBA = [
    # Administradora: Vicepresidente de Finanzas
    ("elisa.montero@vpfinanzas.example", "administrador"),
    # Jefes de departamento: los gerentes
    ("andrea.salazar@vpfinanzas.example", "jefe_departamento"),     # Planificación Financiera
    ("patricia.montilla@vpfinanzas.example", "jefe_departamento"),  # Tesorería
    ("carolina.briceno@vpfinanzas.example", "jefe_departamento"),   # Contraloría
    ("gustavo.linares@vpfinanzas.example", "jefe_departamento"),    # Contabilidad
    # Colaboradores: uno por departamento
    ("mariana.quintero@vpfinanzas.example", "colaborador"),         # Planificación Financiera
    ("diego.paredes@vpfinanzas.example", "colaborador"),            # Tesorería
    ("hector.figueroa@vpfinanzas.example", "colaborador"),          # Contraloría
    ("pablo.acosta@vpfinanzas.example", "colaborador"),             # Contabilidad
    # Colaborador INACTIVO en la empresa: tiene usuario, pero no puede iniciar sesión
    ("emilio.fajardo@vpfinanzas.example", "colaborador"),           # Contraloría
]


def main() -> None:
    if settings.demo_password is None:
        sys.exit("Error: define la variable DEMO_PASSWORD en el archivo .env")
    password = settings.demo_password.get_secret_value()
    if len(password) < LONGITUD_MINIMA:
        sys.exit(f"Error: DEMO_PASSWORD debe tener al menos {LONGITUD_MINIMA} caracteres")

    creados = 0

    with SessionLocal() as db:
        for correo, rol in USUARIOS_DE_PRUEBA:
            colaborador = db.scalars(
                select(Colaborador).where(Colaborador.correo == correo)
            ).first()
            if colaborador is None:
                print(f"  [omitido] no existe el colaborador {correo}")
                continue

            existe = db.scalars(
                select(Usuario).where(Usuario.colaborador_id == colaborador.id)
            ).first()
            if existe:
                print(f"  [ya existe] {correo}")
                continue

            # Un hash por usuario: cada uno lleva su propia sal aleatoria, así dos
            # usuarios con la misma contraseña no tienen el mismo hash guardado.
            db.add(Usuario(colaborador_id=colaborador.id, password_hash=hash_password(password), rol=rol))
            creados += 1
            print(f"  [creado] {correo} ({rol})")

        db.commit()

    print(f"\nUsuarios creados: {creados}")


if __name__ == "__main__":
    main()
