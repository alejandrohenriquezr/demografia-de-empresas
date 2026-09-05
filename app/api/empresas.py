"""Endpoints de empresas activas usados durante la migración a Python."""

from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.data.excel_loader import read_first_sheet

router = APIRouter(prefix="/api/empresas", tags=["empresas"])

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "datos_OE" / "cuadros_estadisticos"

FILES = {
    "evolucion": DATA_DIR / "evolucion_empresas_activas.xlsx",
    "region": DATA_DIR / "empresas_2025_por_region.xlsx",
    "ciiu": DATA_DIR / "empresas_2025_por_ciiu_seccion.xlsx",
    "tamano_trabajadores": DATA_DIR / "empresas_2025_por_tamano_trabaj.xlsx",
    "tamano_ventas": DATA_DIR / "empresas_2025_por_tamano_ventas.xlsx",
    "comparacion": DATA_DIR / "comparacion_empresas_por_criter.xlsx",
}


def _read_required(key: str, columns: tuple[str, ...]) -> pd.DataFrame:
    """Lee un cuadro y valida las columnas mínimas requeridas por su endpoint."""
    path = FILES[key]
    try:
        frame = read_first_sheet(path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No fue posible leer {path.name}") from exc

    missing = set(columns).difference(frame.columns)
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Columnas faltantes en {path.name}: {', '.join(sorted(missing))}",
        )
    return frame.loc[:, list(columns)].copy()


def _number(value: object) -> int | float:
    """Convierte un valor numérico de pandas a un tipo JSON nativo."""
    number = float(value)
    return int(number) if number.is_integer() else number


@router.get("/evolucion")
def evolucion_empresas_activas() -> list[dict[str, int | float]]:
    """Devuelve la serie anual de empresas activas desde el Excel publicado."""
    data = _read_required("evolucion", ("anio", "empresas_activas"))
    data = data.dropna(subset=["anio"]).sort_values("anio")
    return [
        {"anio": int(row.anio), "empresas_activas": _number(row.empresas_activas)}
        for row in data.itertuples(index=False)
    ]


@router.get("/por-region")
def empresas_por_region() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por región."""
    data = _read_required("region", ("region", "empresas_activas"))
    data = data.dropna(subset=["region"]).sort_values("empresas_activas", ascending=False)
    return [
        {"region": str(row.region), "empresas_activas": _number(row.empresas_activas)}
        for row in data.itertuples(index=False)
    ]


@router.get("/por-actividad")
def empresas_por_actividad() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por sección CIIU y su glosa."""
    data = _read_required("ciiu", ("glosa", "empresas_activas"))
    data = data.dropna(subset=["glosa"]).sort_values("empresas_activas", ascending=False)
    return [
        {"glosa": str(row.glosa), "empresas_activas": _number(row.empresas_activas)}
        for row in data.itertuples(index=False)
    ]


@router.get("/por-tamano-trabajadores")
def empresas_por_tamano_trabajadores() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por tamaño según trabajadores."""
    data = _read_required("tamano_trabajadores", ("tamano", "empresas_activas"))
    data = data.dropna(subset=["tamano"])
    return [
        {"tamano": str(row.tamano), "empresas_activas": _number(row.empresas_activas)}
        for row in data.itertuples(index=False)
    ]


@router.get("/por-tamano-ventas")
def empresas_por_tamano_ventas() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por tamaño según ventas."""
    data = _read_required("tamano_ventas", ("tamano", "empresas_activas"))
    data = data.dropna(subset=["tamano"])
    return [
        {"tamano": str(row.tamano), "empresas_activas": _number(row.empresas_activas)}
        for row in data.itertuples(index=False)
    ]


@router.get("/comparacion-criterios")
def comparacion_criterios() -> list[dict[str, str | int | float]]:
    """Devuelve la evolución de empresas activas para cada criterio de actividad."""
    data = _read_required("comparacion", ("categoria", "anio", "empresas_activas"))
    data = data.dropna(subset=["categoria", "anio"]).sort_values(["categoria", "anio"])
    return [
        {
            "categoria": str(row.categoria),
            "anio": int(row.anio),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]
