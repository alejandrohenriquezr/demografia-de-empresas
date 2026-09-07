"""Punto de entrada FastAPI para la migración gradual del sitio."""

from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from app.api.empresas import router as empresas_router


# ---------------------------------------------------------------------
# Rutas base de la aplicación
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_FILE = BASE_DIR / "index.html"
CLIENT_FILE = BASE_DIR / "worker" / "client.js"
XLSX_FILE = BASE_DIR / "worker" / "vendor" / "xlsx.full.min.js"

PILOT_FILE = (
    BASE_DIR
    / "app"
    / "static"
    / "pilot_empresas_5_1.js"
)

ASSETS_DIR = BASE_DIR / "assets"
DATOS_DIR = BASE_DIR / "datos_OE"


# ---------------------------------------------------------------------
# Aplicación FastAPI
# ---------------------------------------------------------------------

allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

app = FastAPI(
    title="Demografía de Empresas",
    version="0.6.0",
    description=(
        "API Python para la migración gradual "
        "del sitio de demografía empresarial."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------
# API
# ---------------------------------------------------------------------

app.include_router(empresas_router)


# ---------------------------------------------------------------------
# Recursos estáticos
# ---------------------------------------------------------------------

# Durante la migración se mantienen las mismas rutas utilizadas
# actualmente por el frontend.
app.mount(
    "/assets",
    StaticFiles(directory=ASSETS_DIR),
    name="assets",
)

app.mount(
    "/datos_OE",
    StaticFiles(directory=DATOS_DIR),
    name="datos_OE",
)


# ---------------------------------------------------------------------
# Estado del servicio
# ---------------------------------------------------------------------

@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    """Informa si el servicio FastAPI está disponible."""
    return {"status": "ok"}


# ---------------------------------------------------------------------
# Compatibilidad temporal con SheetJS
# ---------------------------------------------------------------------

@app.get("/xlsx", include_in_schema=False)
def xlsx_library() -> FileResponse:
    """Entrega la biblioteca SheetJS utilizada por el sitio actual."""
    return FileResponse(
        XLSX_FILE,
        media_type="application/javascript; charset=utf-8",
        headers={
            "Cache-Control": (
                "public, max-age=31536000, immutable"
            )
        },
    )


# ---------------------------------------------------------------------
# Cliente JavaScript
# ---------------------------------------------------------------------

@app.get("/client-dynamic", include_in_schema=False)
def dynamic_client() -> Response:
    """
    Entrega el cliente original y agrega la capa Python de la etapa 5.1.

    El cliente original continúa cargándose primero.
    Si una API Python falla, los gráficos renderizados desde Excel
    permanecen disponibles como fallback.
    """

    original = CLIENT_FILE.read_text(
        encoding="utf-8"
    )

    api_layer = PILOT_FILE.read_text(
        encoding="utf-8"
    )

    return Response(
        content=original + "\n\n" + api_layer,
        media_type="application/javascript; charset=utf-8",
        headers={
            "Cache-Control": "no-store"
        },
    )


# ---------------------------------------------------------------------
# Página principal
# ---------------------------------------------------------------------

@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Sirve la interfaz HTML actual desde FastAPI."""
    return FileResponse(
        INDEX_FILE,
        media_type="text/html; charset=utf-8",
        headers={
            "Cache-Control": "no-store"
        },
    )
