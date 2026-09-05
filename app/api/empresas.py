"""Endpoints de empresas activas usados durante la migración a Python."""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.data.excel_loader import read_first_sheet

router = APIRouter(prefix="/api/empresas", tags=["empresas"])

BASE_DIR = Path(__file__).resolve().parents[2]
EVOLUCION_FILE = BASE_DIR / "datos_OE" / "cuadros_estadisticos" / "evolucion_empresas_activas.xlsx"
REQUIRED_COLUMNS = {"anio", "empresas_activas"}


@router.get("/evolucion")
def evolucion_empresas_activas() -> list[dict[str, int | float]]:
    """Devuelve la serie anual de empresas activas desde el Excel oficial publicado."""
    try:
        frame = read_first_sheet(EVOLUCION_FILE)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No fue posible leer {EVOLUCION_FILE.name}") from exc

    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Columnas faltantes en {EVOLUCION_FILE.name}: {', '.join(sorted(missing))}",
        )

    data = frame.loc[:, ["anio", "empresas_activas"]].dropna(subset=["anio"])
    data = data.sort_values("anio")

    result: list[dict[str, int | float]] = []
    for row in data.itertuples(index=False):
        anio = int(row.anio)
        empresas = float(row.empresas_activas)
        if empresas.is_integer():
            empresas = int(empresas)
        result.append({"anio": anio, "empresas_activas": empresas})

    return result
