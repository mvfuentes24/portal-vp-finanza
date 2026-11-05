"""Punto de entrada de la API del Portal VP de Finanzas."""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.modules.auth.router import router as auth_router
from app.modules.cargos.router import router as cargos_router
from app.modules.cierres_caja.router import router as cierres_router
from app.modules.organizacion.router import router as organizacion_router

app = FastAPI(
    title="Portal VP de Finanzas",
    description="API interna de la Vicepresidencia de Finanzas",
    version="0.1.0",
)

# Solo el frontend configurado puede consumir la API desde el navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
)

app.include_router(auth_router)
app.include_router(organizacion_router)
app.include_router(cargos_router)
app.include_router(cierres_router)


@app.get("/health", tags=["Sistema"])
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    """Verifica que la API está en ejecución y puede conectarse a la base de datos."""
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        # No se devuelve el detalle del error para no exponer información interna
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    return {"status": "ok", "database": "ok"}
