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
    "actividad": DATA_DIR / "empresas_2025_por_ciiu_seccion.xlsx",
    "tamano_trabajadores": DATA_DIR / "empresas_2025_por_tamano_trabaj.xlsx",
    "tamano_ventas": DATA_DIR / "empresas_2025_por_tamano_ventas.xlsx",
    "comparacion": DATA_DIR / "comparacion_empresas_por_criter.xlsx",
}


def _read_table(key: str, required: set[str]) -> pd.DataFrame:
    """Lee un cuadro y valida las columnas mínimas requeridas por su endpoint."""
    path = FILES[key]
    try:
        frame = read_first_sheet(path)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"No fue posible leer {path.name}",
        ) from exc

    missing = required.difference(frame.columns)
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Columnas faltantes en {path.name}: {', '.join(sorted(missing))}",
        )

    return frame


def _number(value):
    """Convierte valores numéricos de pandas a tipos JSON simples."""
    number = float(value)
    return int(number) if number.is_integer() else number


@router.get("/evolucion")
def evolucion_empresas_activas() -> list[dict[str, int | float]]:
    """Devuelve la serie anual de empresas activas."""
    frame = _read_table("evolucion", {"anio", "empresas_activas"})
    data = (
        frame.loc[:, ["anio", "empresas_activas"]]
        .dropna(subset=["anio", "empresas_activas"])
        .sort_values("anio")
    )

    return [
        {
            "anio": int(row.anio),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]


@router.get("/region")
@router.get("/por-region", include_in_schema=False)
def empresas_por_region() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por región."""
    frame = _read_table("region", {"region", "empresas_activas"})

    data = (
        frame.loc[:, ["region", "empresas_activas"]]
        .dropna(subset=["region", "empresas_activas"])
        .sort_values("empresas_activas", ascending=False)
    )

    return [
        {
            "region": str(row.region),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]


@router.get("/actividad")
@router.get("/por-actividad", include_in_schema=False)
def empresas_por_actividad() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por sección de actividad económica."""
    frame = _read_table("actividad", {"glosa", "empresas_activas"})

    data = (
        frame.loc[:, ["glosa", "empresas_activas"]]
        .dropna(subset=["glosa", "empresas_activas"])
        .sort_values("empresas_activas", ascending=False)
    )

    return [
        {
            "glosa": str(row.glosa),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]


@router.get("/tamano-trabajadores")
@router.get("/por-tamano-trabajadores", include_in_schema=False)
def empresas_por_tamano_trabajadores() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por tamaño según trabajadores."""
    frame = _read_table(
        "tamano_trabajadores",
        {"tamano", "empresas_activas"},
    )

    data = frame.loc[:, ["tamano", "empresas_activas"]].dropna(
        subset=["tamano", "empresas_activas"]
    )

    return [
        {
            "tamano": str(row.tamano),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]


@router.get("/tamano-ventas")
@router.get("/por-tamano-ventas", include_in_schema=False)
def empresas_por_tamano_ventas() -> list[dict[str, str | int | float]]:
    """Devuelve empresas activas 2025 por tamaño según ventas."""
    frame = _read_table(
        "tamano_ventas",
        {"tamano", "empresas_activas"},
    )

    data = frame.loc[:, ["tamano", "empresas_activas"]].dropna(
        subset=["tamano", "empresas_activas"]
    )

    return [
        {
            "tamano": str(row.tamano),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]

@router.get("/comparacion-criterios")
def comparacion_criterios() -> list[dict[str, str | int | float]]:
    """Devuelve la evolución anual según criterio de actividad."""
    frame = _read_table(
        "comparacion",
        {"categoria", "anio", "empresas_activas"},
    )
    data = (
        frame.loc[:, ["categoria", "anio", "empresas_activas"]]
        .dropna(subset=["categoria", "anio", "empresas_activas"])
        .sort_values(["categoria", "anio"])
    )

    return [
        {
            "categoria": str(row.categoria),
            "anio": int(row.anio),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]
