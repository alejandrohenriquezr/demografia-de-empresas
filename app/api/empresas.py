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
    "nacimientos_muertes": DATA_DIR / "nacimientos_muertes_por_anio.xlsx",
    "tasas": DATA_DIR / "tasas_nacimientos_muertes.xlsx",
    "supervivencia": DATA_DIR / "supervivencia_empresas_por_coho.xlsx",
    "interaccion": DATA_DIR / "interaccion_variables_desagrega.xlsx",
    "interaccion_nacimientos": DATA_DIR / "interaccion_variables_nacimient.xlsx",
    "comuna": DATA_DIR / "empresas_2025_por_comuna.xlsx",
    "provincia": DATA_DIR / "empresas_2025_por_provincia.xlsx",
    "ciiu_clase": DATA_DIR / "empresas_2025_por_ciiu_clase.xlsx",
    "ciiu_division": DATA_DIR / "empresas_2025_por_ciiu_division.xlsx",
    "ciiu_grupo": DATA_DIR / "empresas_2025_por_ciiu_grupo.xlsx",
    "ciiu_subclase": DATA_DIR / "empresas_2025_por_ciiu_subclase.xlsx",
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
def empresas_por_region():
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
def empresas_por_actividad():
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
def empresas_por_tamano_trabajadores():
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
def empresas_por_tamano_ventas():
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


@router.get("/nacimientos-muertes")
def nacimientos_muertes() -> list[dict]:
    """Devuelve la serie anual de nacimientos y muertes de empresas."""
    frame = _read_table("nacimientos_muertes", {"anio", "tipo", "empresas"})
    data = (
        frame.loc[:, ["anio", "tipo", "empresas"]]
        .dropna(subset=["anio", "tipo", "empresas"])
        .sort_values(["anio", "tipo"])
    )
    return [
        {"anio": int(row.anio), "tipo": str(row.tipo), "empresas": _number(row.empresas)}
        for row in data.itertuples(index=False)
    ]


@router.get("/tasas")
def tasas() -> list[dict]:
    """Devuelve tasas por dimensión, categoría y año."""
    required = {
        "dimension", "categoria", "anio", "tasa_nacimientos",
        "tasa_muertes", "tasa_neta_nacimientos",
    }
    frame = _read_table("tasas", required)
    data = (
        frame.loc[:, sorted(required)]
        .dropna(subset=["dimension", "categoria", "anio"])
        .sort_values(["dimension", "categoria", "anio"])
    )
    return [
        {
            "dimension": str(row.dimension),
            "categoria": str(row.categoria),
            "anio": int(row.anio),
            "tasa_nacimientos": _number(row.tasa_nacimientos),
            "tasa_muertes": _number(row.tasa_muertes),
            "tasa_neta_nacimientos": _number(row.tasa_neta_nacimientos),
        }
        for row in data.itertuples(index=False)
    ]


@router.get("/supervivencia")
def supervivencia() -> list[dict]:
    """Devuelve tasas de supervivencia por cohorte."""
    required = {"dimension", "categoria", "cohorte", "anios", "tasa_supervivencia"}
    frame = _read_table("supervivencia", required)
    data = (
        frame.loc[:, sorted(required)]
        .dropna(subset=["dimension", "categoria", "cohorte", "anios"])
        .sort_values(["dimension", "categoria", "cohorte", "anios"])
    )
    return [
        {
            "dimension": str(row.dimension),
            "categoria": str(row.categoria),
            "cohorte": str(row.cohorte),
            "anios": int(row.anios),
            "tasa_supervivencia": _number(row.tasa_supervivencia),
        }
        for row in data.itertuples(index=False)
    ]


def _interaction(key: str) -> list[dict]:
    """Normaliza una tabla de interacción conservando sus dimensiones."""
    required = {
        "dimension_fila", "dimension_columna", "etiqueta_fila",
        "etiqueta_columna", "empresas_activas",
    }
    frame = _read_table(key, required)
    data = frame.loc[:, sorted(required)].dropna(
        subset=["dimension_fila", "dimension_columna", "etiqueta_fila",
                "etiqueta_columna", "empresas_activas"]
    )
    data = data.sort_values(
        ["dimension_fila", "dimension_columna", "etiqueta_fila",
         "etiqueta_columna"]
    )
    return [
        {
            "dimension_fila": str(row.dimension_fila),
            "dimension_columna": str(row.dimension_columna),
            "etiqueta_fila": str(row.etiqueta_fila),
            "etiqueta_columna": str(row.etiqueta_columna),
            "empresas_activas": _number(row.empresas_activas),
        }
        for row in data.itertuples(index=False)
    ]


@router.get("/interaccion")
def interaccion() -> list[dict]:
    """Devuelve la tabla de interacción de variables de desagregación."""
    return _interaction("interaccion")


@router.get("/interaccion-nacimientos")
def interaccion_nacimientos() -> list[dict]:
    """Devuelve la tabla de interacción de nacimientos."""
    return _interaction("interaccion_nacimientos")


def _dimension(key: str, label: str) -> list[dict]:
    """Devuelve una desagregación con etiqueta y empresas activas."""
    frame = _read_table(key, {label, "empresas_activas"})
    data = (
        frame.loc[:, [label, "empresas_activas"]]
        .dropna(subset=[label, "empresas_activas"])
        .sort_values("empresas_activas", ascending=False)
    )
    return [
        {label: str(getattr(row, label)), "empresas_activas": _number(row.empresas_activas)}
        for row in data.itertuples(index=False)
    ]


@router.get("/comuna")
def empresas_por_comuna() -> list[dict]:
    """Devuelve empresas activas por comuna."""
    return _dimension("comuna", "comuna")


@router.get("/provincia")
def empresas_por_provincia() -> list[dict]:
    """Devuelve empresas activas por provincia."""
    return _dimension("provincia", "provincia")


@router.get("/ciiu/{nivel}")
def empresas_por_ciiu(nivel: str) -> list[dict]:
    """Devuelve empresas activas por nivel CIIU permitido."""
    allowed = {
        "clase": ("ciiu_clase", "glosa"),
        "division": ("ciiu_division", "glosa"),
        "grupo": ("ciiu_grupo", "glosa"),
        "subclase": ("ciiu_subclase", "glosa"),
    }
    if nivel not in allowed:
        raise HTTPException(status_code=404, detail="Nivel CIIU no disponible")
    key, label = allowed[nivel]
    return _dimension(key, label)
