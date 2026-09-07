/* Etapa 5.1: empresas activas desde la API Python.
   Cada gráfico conserva el render previo desde Excel si su endpoint falla. */
(() => {
  const api = async path => {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data) || !data.length) throw new Error(`${path}: sin datos`);
    return data;
  };

  const n = value => Number(value ?? 0) || 0;
  const mark = (id, source) => {
    const target = document.getElementById(id);
    if (target) target.dataset.dataSource = source;
  };

  const baseLayout = {
    paper_bgcolor: "#fff",
    plot_bgcolor: "#fff",
    hovermode: "x unified",
    font: { family: "Arial" },
    title: { text: "" },
    legend: {
      orientation: "h",
      x: 0,
      xanchor: "left",
      y: -0.28,
      yanchor: "top"
    }
  };

  async function render() {
    if (!window.Plotly) return;

    const jobs = [
      ["grafico-evolucion", async () => {
        const d = await api("/api/empresas/evolucion");
        await Plotly.react("grafico-evolucion", [{
          x: d.map(x => x.anio),
          y: d.map(x => n(x.empresas_activas)),
          type: "scatter",
          mode: "lines+markers",
          line: { color: "#003366", width: 3 },
          name: "Empresas activas"
        }], {
          ...baseLayout,
          margin: { t: 30, r: 20, b: 120, l: 62 },
          yaxis: { title: "Número de empresas" }
        }, { responsive: true, displaylogo: false });
      }],

      ["grafico-geografico", async () => {
        const mobile = matchMedia("(max-width:700px)").matches;
        const d = (await api("/api/empresas/region"))
          .sort((a, b) => n(b.empresas_activas) - n(a.empresas_activas));
        const short = v => mobile && String(v).length > 25 ? String(v).slice(0, 24) + "…" : v;
        await Plotly.react("grafico-geografico", [{
          x: d.map(x => n(x.empresas_activas)),
          y: d.map(x => short(x.region)),
          customdata: d.map(x => x.region),
          type: "bar",
          orientation: "h",
          marker: { color: "#1f4e79" },
          hovertemplate: "%{customdata}<br>%{x:,} empresas<extra></extra>"
        }], {
          ...baseLayout,
          height: Math.max(mobile ? 420 : 455, d.length * 28 + 115),
          margin: { t: 42, r: 20, b: 120, l: mobile ? 175 : 275 },
          xaxis: { title: "Número de empresas" },
          yaxis: { autorange: "reversed", tickfont: { size: mobile ? 10 : 12 } }
        }, { responsive: true, displaylogo: false });
      }],

      ["grafico-ciiu", async () => {
        const mobile = matchMedia("(max-width:700px)").matches;
        const d = (await api("/api/empresas/actividad"))
          .sort((a, b) => n(b.empresas_activas) - n(a.empresas_activas));
        const short = v => mobile && String(v).length > 30 ? String(v).slice(0, 29) + "…" : v;
        await Plotly.react("grafico-ciiu", [{
          x: d.map(x => n(x.empresas_activas)),
          y: d.map(x => short(x.glosa)),
          customdata: d.map(x => x.glosa),
          type: "bar",
          orientation: "h",
          marker: { color: "#1f4e79" },
          hovertemplate: "%{customdata}<br>%{x:,} empresas<extra></extra>"
        }], {
          ...baseLayout,
          height: Math.max(mobile ? 500 : 455, d.length * 28 + 115),
          margin: { t: 42, r: 20, b: 120, l: mobile ? 205 : 365 },
          xaxis: { title: "Número de empresas" },
          yaxis: { autorange: "reversed", tickfont: { size: mobile ? 9 : 12 } }
        }, { responsive: true, displaylogo: false });
      }],

      ["grafico-tamano", async () => {
        const d = await api("/api/empresas/tamano-trabajadores");
        await Plotly.react("grafico-tamano", [{
          x: d.map(x => x.tamano),
          y: d.map(x => n(x.empresas_activas)),
          type: "bar",
          marker: { color: "#1f4e79" }
        }], {
          ...baseLayout,
          margin: { t: 38, r: 20, b: 120, l: 62 },
          yaxis: { title: "Número de empresas" }
        }, { responsive: true, displaylogo: false });
      }],

      ["grafico-ventas", async () => {
        const d = await api("/api/empresas/tamano-ventas");
        await Plotly.react("grafico-ventas", [{
          x: d.map(x => x.tamano),
          y: d.map(x => n(x.empresas_activas)),
          type: "bar",
          marker: { color: "#1f4e79" }
        }], {
          ...baseLayout,
          margin: { t: 38, r: 20, b: 120, l: 62 },
          yaxis: { title: "Número de empresas" }
        }, { responsive: true, displaylogo: false });
      }],

      ["grafico-comparacion-actividad", async () => {
        const d = await api("/api/empresas/comparacion-criterios");
        const categories = [...new Set(d.map(x => x.categoria))];
        const traces = categories.map(category => {
          const rows = d.filter(x => x.categoria === category);
          return {
            x: rows.map(x => x.anio),
            y: rows.map(x => n(x.empresas_activas)),
            type: "scatter",
            mode: "lines+markers",
            name: category
          };
        });
        await Plotly.react("grafico-comparacion-actividad", traces, {
          ...baseLayout,
          margin: { t: 42, r: 20, b: 120, l: 62 },
          xaxis: { type: "linear", dtick: 1 },
          yaxis: { title: "Número de empresas" }
        }, { responsive: true, displaylogo: false });
      }]
    ];

    for (const [id, job] of jobs) {
      if (!document.getElementById(id)) continue;
      try {
        await job();
        mark(id, "python-api");
      } catch (error) {
        console.warn(`API Python no disponible para ${id}; se conserva Excel.`, error);
        mark(id, "excel-fallback");
      }
    }
  }

  const start = () => setTimeout(render, 1200);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
