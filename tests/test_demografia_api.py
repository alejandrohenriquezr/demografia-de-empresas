"""Pruebas de los endpoints del bloque demográfico migrado a Python."""

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_nacimientos_muertes_ordenados(monkeypatch) -> None:
    """La serie debe ordenarse por año y tipo."""
    frame = pd.DataFrame({
        "anio": [2025, 2024],
        "tipo": ["Muertes", "Nacimientos"],
        "empresas": [8, 12],
    })
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/nacimientos-muertes")

    assert response.status_code == 200
    assert response.json()[0]["anio"] == 2024


def test_tasas_exige_columnas_completas(monkeypatch) -> None:
    """La API debe informar la estructura incompleta del cuadro."""
    frame = pd.DataFrame({"anio": [2025], "tasa_nacimientos": [4.2]})
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/tasas")

    assert response.status_code == 500
    assert "tasa_muertes" in response.json()["detail"]


def test_supervivencia_devuelve_cohortes_ordenadas(monkeypatch) -> None:
    """Las cohortes deben quedar ordenadas por cohorte y años transcurridos."""
    frame = pd.DataFrame({
        "dimension": ["Ventas", "Ventas"],
        "categoria": ["Micro", "Micro"],
        "cohorte": ["2024", "2024"],
        "anios": [1, 0],
        "tasa_supervivencia": [80, 100],
    })
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/supervivencia")

    assert response.status_code == 200
    assert response.json()[0]["anios"] == 0
