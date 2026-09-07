"""Punto de entrada FastAPI para la migración gradual del sitio."""

from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from app.api.empresas import router as empresas_router
from app.data.sqlite_db import connection, initialize


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

@app.get("/api/catalogo", tags=["catalogo"])
def catalogo() -> list[dict]:
    """Devuelve el catálogo local SQLite de recursos publicados."""
    initialize()
    with connection() as conn:
        rows = conn.execute(
            """
            SELECT c.slug AS categoria, c.nombre AS categoria_nombre,
                   r.titulo_publico, r.nombre_archivo,
                   r.ruta_relativa, r.tipo_archivo, r.orden
              FROM recursos AS r
              JOIN categorias AS c ON c.id = r.categoria_id
             WHERE r.estado = 'publicado'
             ORDER BY c.orden, r.orden, r.titulo_publico
            """
        ).fetchall()
    return [dict(row) for row in rows]


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
def index() -> Response:
    """Sirve la interfaz e inyecta las dependencias dinámicas de Python."""
    html = INDEX_FILE.read_text(encoding="utf-8")
    scripts = (
        '<script src="/xlsx"></script>'
        '<script src="/client-dynamic"></script>'
    )
    if "</head>" in html:
        html = html.replace("</head>", scripts + "</head>", 1)
    else:
        html += scripts
    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )
