"""Lectura e inspección controlada de los cuadros estadísticos Excel."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class ExcelProfile:
    """Resumen estructural de un libro Excel usado por la aplicación."""

    file: str
    sheet: str
    rows: int
    columns: tuple[str, ...]


def read_first_sheet(path: Path) -> pd.DataFrame:
    """Lee la primera hoja de un Excel, replicando el comportamiento actual de SheetJS."""
    workbook = pd.ExcelFile(path, engine="openpyxl")
    if not workbook.sheet_names:
        raise ValueError(f"El archivo no contiene hojas: {path.name}")
    return pd.read_excel(workbook, sheet_name=workbook.sheet_names[0])


def profile_excel(path: Path) -> ExcelProfile:
    """Devuelve hoja, filas y columnas de un Excel sin modificar su contenido."""
    workbook = pd.ExcelFile(path, engine="openpyxl")
    if not workbook.sheet_names:
        raise ValueError(f"El archivo no contiene hojas: {path.name}")

    sheet = workbook.sheet_names[0]
    frame = pd.read_excel(workbook, sheet_name=sheet)
    columns = tuple(str(column).strip() for column in frame.columns)

    return ExcelProfile(
        file=path.name,
        sheet=sheet,
        rows=len(frame),
        columns=columns,
    )
