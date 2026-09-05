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
    version="0.4.0",
    description="API Python para la migración gradual del sitio de demografía empresarial.",
)

app.include_router(empresas_router)

# Se mantienen las rutas públicas actuales para no modificar todavía el frontend base.
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
    """Entrega el cliente actual y añade la capa API del bloque de empresas activas."""
    original = CLIENT_FILE.read_text(encoding="utf-8")
    api_layer = r'''

/* Etapa 5.1: bloque de empresas activas desde API Python.
   Si una API falla, se conserva el gráfico que ya renderizó el cliente Excel original. */
(() => {
  const number = value => Number(value ?? 0) || 0;
  const mobile = () => matchMedia("(max-width:700px)").matches;
  const short = (value, max) => String(value).length > max ? String(value).slice(0, max - 1) + "…" : String(value);

  async function api(path) {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) throw new Error(`API ${path} respondió ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data) || !data.length) throw new Error(`API ${path} sin datos`);
    return data;
  }

  async function render(targetId, apiPath, build) {
    const target = document.getElementById(targetId);
    if (!target || !window.Plotly) return;
    try {
      const data = await api(apiPath);
      const { traces, layout } = build(data);
      await Plotly.react(target, traces, {
        paper_bgcolor: "#fff",
        plot_bgcolor: "#fff",
        hovermode: "x unified",
        font: { family: "Arial" },
        title: { text: "" },
        legend: { orientation: "h", x: 0, xanchor: "left", y: -0.28, yanchor: "top" },
        ...layout
      }, { responsive: true, displaylogo: false });
      target.dataset.dataSource = "python-api";
    } catch (error) {
      console.warn(`API Python no disponible para ${targetId}; se mantiene Excel.`, error);
      target.dataset.dataSource = "excel-fallback";
    }
  }

  async function renderBloqueEmpresas() {
    await Promise.all([
      render("grafico-evolucion", "/api/empresas/evolucion", data => ({
        traces: [{
          x: data.map(d => d.anio),
          y: data.map(d => number(d.empresas_activas)),
          type: "scatter",
          mode: "lines+markers",
          line: { color: "#003366", width: 3 },
          name: "Empresas activas"
        }],
        layout: { margin: { t: 30, r: 20, b: 120, l: 62 }, yaxis: { title: "Número de empresas" } }
      })),
      render("grafico-geografico", "/api/empresas/por-region", data => {
        const labels = data.map(d => mobile() ? short(d.region, 25) : d.region);
        return {
          traces: [{
            x: data.map(d => number(d.empresas_activas)),
            y: labels,
            customdata: data.map(d => d.region),
            type: "bar",
            orientation: "h",
            marker: { color: "#1f4e79" },
            hovertemplate: "%{customdata}<br>%{x:,} empresas<extra></extra>"
          }],
          layout: {
            height: Math.max(mobile() ? 420 : 455, data.length * 28 + 115),
            margin: { t: 42, r: 20, b: 120, l: mobile() ? 175 : 275 },
            xaxis: { title: "Número de empresas" },
            yaxis: { autorange: "reversed", tickfont: { size: mobile() ? 10 : 12 } }
          }
        };
      }),
      render("grafico-ciiu", "/api/empresas/por-actividad", data => {
        const labels = data.map(d => mobile() ? short(d.glosa, 30) : d.glosa);
        return {
          traces: [{
            x: data.map(d => number(d.empresas_activas)),
            y: labels,
            customdata: data.map(d => d.glosa),
            type: "bar",
            orientation: "h",
            marker: { color: "#1f4e79" },
            hovertemplate: "%{customdata}<br>%{x:,} empresas<extra></extra>"
          }],
          layout: {
            height: Math.max(mobile() ? 500 : 455, data.length * 28 + 115),
            margin: { t: 42, r: 20, b: 120, l: mobile() ? 205 : 365 },
            xaxis: { title: "Número de empresas" },
            yaxis: { autorange: "reversed", tickfont: { size: mobile() ? 9 : 12 } }
          }
        };
      }),
      render("grafico-tamano", "/api/empresas/por-tamano-trabajadores", data => ({
        traces: [{
          x: data.map(d => d.tamano),
          y: data.map(d => number(d.empresas_activas)),
          type: "bar",
          marker: { color: "#1f4e79" }
        }],
        layout: { margin: { t: 38, r: 20, b: 120, l: 62 }, yaxis: { title: "Número de empresas" } }
      })),
      render("grafico-ventas", "/api/empresas/por-tamano-ventas", data => ({
        traces: [{
          x: data.map(d => d.tamano),
          y: data.map(d => number(d.empresas_activas)),
          type: "bar",
          marker: { color: "#1f4e79" }
        }],
        layout: { margin: { t: 38, r: 20, b: 120, l: 62 }, yaxis: { title: "Número de empresas" } }
      })),
      render("grafico-comparacion-actividad", "/api/empresas/comparacion-criterios", data => {
        const categories = [...new Set(data.map(d => d.categoria))];
        return {
          traces: categories.map(category => {
            const rows = data.filter(d => d.categoria === category).sort((a, b) => a.anio - b.anio);
            return {
              x: rows.map(d => d.anio),
              y: rows.map(d => number(d.empresas_activas)),
              type: "scatter",
              mode: "lines+markers",
              name: category
            };
          }),
          layout: {
            margin: { t: 42, r: 20, b: 120, l: 62 },
            xaxis: { type: "linear", dtick: 1 },
            yaxis: { title: "Número de empresas" }
          }
        };
      })
    ]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => setTimeout(renderBloqueEmpresas, 1200));
  } else {
    setTimeout(renderBloqueEmpresas, 1200);
  }
})();
'''
    return Response(
        content=original + api_layer,
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
