"""Punto de entrada FastAPI para la migración gradual del sitio."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "index.html"
CLIENT_FILE = BASE_DIR / "worker" / "client.js"
XLSX_FILE = BASE_DIR / "worker" / "vendor" / "xlsx.full.min.js"
ASSETS_DIR = BASE_DIR / "assets"
DATOS_DIR = BASE_DIR / "datos_OE"

app = FastAPI(
    title="Demografía de Empresas",
    version="0.2.0",
    description="API Python para la migración gradual del sitio de demografía empresarial.",
)

# Se mantienen las rutas públicas actuales para no modificar todavía el frontend.
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/datos_OE", StaticFiles(directory=DATOS_DIR), name="datos_OE")


@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    """Informa si el servicio FastAPI está disponible."""
    return {"status": "ok"}


@app.get("/xlsx", include_in_schema=False)
def xlsx_library() -> FileResponse:
    """Entrega la misma biblioteca SheetJS usada por el Worker actual."""
    return FileResponse(
        XLSX_FILE,
        media_type="application/javascript; charset=utf-8",
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


@app.get("/client-dynamic", include_in_schema=False)
def dynamic_client() -> FileResponse:
    """Entrega el cliente JavaScript actual sin modificar su lógica."""
    return FileResponse(
        CLIENT_FILE,
        media_type="application/javascript; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Sirve la interfaz HTML actual desde FastAPI."""
    return FileResponse(
        INDEX_FILE,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )
