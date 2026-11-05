"""Analiza los cierres de caja existentes y genera sus alertas.

Uso (desde la carpeta backend, con el entorno virtual activo):
    python -m scripts.analizar_cierres

Se ejecuta una vez después de cargar los datos semilla. Los cierres se analizan
en orden cronológico, para que la regla de reincidencia se evalúe igual que si
se hubieran registrado día a día. Es seguro ejecutarlo más de una vez: no
duplica alertas.
"""

from sqlalchemy import func, select

from app.core.database import SessionLocal
from app.modules.cierres_caja.models import Alerta
from app.modules.cierres_caja.service import analizar_todos


def main() -> None:
    with SessionLocal() as db:
        creadas = analizar_todos(db)
        resumen = db.execute(select(Alerta.tipo, func.count()).group_by(Alerta.tipo).order_by(Alerta.tipo)).all()

    print(f"Alertas creadas en esta ejecución: {creadas}")
    print("Total de alertas por tipo:")
    for tipo, cantidad in resumen:
        print(f"  {tipo}: {cantidad}")


if __name__ == "__main__":
    main()
