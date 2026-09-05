"""Punto de entrada FastAPI para la migración gradual del sitio."""

from fastapi import FastAPI

app = FastAPI(
    title="Demografía de Empresas",
    version="0.1.0",
    description="API Python para la migración gradual del sitio de demografía empresarial.",
)


@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    """Informa si el servicio FastAPI está disponible."""
    return {"status": "ok"}
