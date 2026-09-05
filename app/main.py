"""Punto de entrada FastAPI para la migración gradual del sitio."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from app.api.empresas import router as empresas_router

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "index.html"
CLIENT_FILE = BASE_DIR / "worker" / "client.js"
XLSX_FILE = BASE_DIR / "worker" / "vendor" / "xlsx.full.min.js"
ASSETS_DIR = BASE_DIR / "assets"
DATOS_DIR = BASE_DIR / "datos_OE"

app = FastAPI(
    title="Demografía de Empresas",
    version="0.3.0",
    description="API Python para la migración gradual del sitio de demografía empresarial.",
)

app.include_router(empresas_router)

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
def dynamic_client() -> Response:
    """Entrega el cliente actual y añade el piloto API para el gráfico de evolución."""
    original = CLIENT_FILE.read_text(encoding="utf-8")
    pilot = r'''

/* Piloto Etapa 4: reemplaza únicamente la fuente del gráfico de evolución por la API Python.
   Si la API falla, se conserva el gráfico ya renderizado desde el Excel por el cliente original. */
(() => {
  async function renderEvolucionDesdeApi() {
    const target = document.getElementById("grafico-evolucion");
    if (!target || !window.Plotly) return;
    try {
      const response = await fetch("/api/empresas/evolucion", { cache: "no-store" });
      if (!response.ok) throw new Error(`API respondió ${response.status}`);
      const datos = await response.json();
      if (!Array.isArray(datos) || !datos.length) throw new Error("API sin datos");
      await Plotly.react(target, [{
        x: datos.map(d => d.anio),
        y: datos.map(d => d.empresas_activas),
        type: "scatter",
        mode: "lines+markers",
        line: { color: "#003366", width: 3 },
        name: "Empresas activas"
      }], {
        paper_bgcolor: "#fff",
        plot_bgcolor: "#fff",
        margin: { t: 30, r: 20, b: 120, l: 62 },
        hovermode: "x unified",
        font: { family: "Arial" },
        title: { text: "" },
        legend: { orientation: "h", x: 0, xanchor: "left", y: -0.28, yanchor: "top" },
        yaxis: { title: "Número de empresas" }
      }, { responsive: true, displaylogo: false });
      target.dataset.dataSource = "python-api";
    } catch (error) {
      console.warn("Piloto Python no disponible; se mantiene el gráfico desde Excel.", error);
      target.dataset.dataSource = "excel-fallback";
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => setTimeout(renderEvolucionDesdeApi, 1200));
  } else {
    setTimeout(renderEvolucionDesdeApi, 1200);
  }
})();
'''
    return Response(
        content=original + pilot,
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
