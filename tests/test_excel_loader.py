"""Pruebas del lector Python de cuadros estadísticos."""

from pathlib import Path

import pandas as pd

from app.data.excel_loader import profile_excel, read_first_sheet


def test_read_first_sheet_usa_primera_hoja(tmp_path: Path) -> None:
    """El lector debe reproducir el criterio actual de usar la primera hoja del libro."""
    path = tmp_path / "ejemplo.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame({"anio": [2024, 2025], "empresas_activas": [10, 12]}).to_excel(
            writer, sheet_name="datos", index=False
        )
        pd.DataFrame({"otra": [1]}).to_excel(writer, sheet_name="segunda", index=False)

    frame = read_first_sheet(path)

    assert list(frame.columns) == ["anio", "empresas_activas"]
    assert len(frame) == 2


def test_profile_excel_reporta_estructura(tmp_path: Path) -> None:
    """El perfil debe informar hoja, filas y nombres de columnas."""
    path = tmp_path / "ejemplo.xlsx"
    pd.DataFrame({"region": ["A", "B"], "empresas_activas": [5, 7]}).to_excel(
        path, sheet_name="Hoja1", index=False, engine="openpyxl"
    )

    profile = profile_excel(path)

    assert profile.file == "ejemplo.xlsx"
    assert profile.sheet == "Hoja1"
    assert profile.rows == 2
    assert profile.columns == ("region", "empresas_activas")
