"""Pruebas del primer endpoint migrado a Python."""

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_evolucion_empresas_entrega_serie_ordenada(monkeypatch) -> None:
    """La API debe devolver año y empresas activas ordenados cronológicamente."""
    frame = pd.DataFrame(
        {
            "anio": [2025, 2023, 2024],
            "empresas_activas": [1500, 1200, 1350],
        }
    )
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/evolucion")

    assert response.status_code == 200
    assert response.json() == [
        {"anio": 2023, "empresas_activas": 1200},
        {"anio": 2024, "empresas_activas": 1350},
        {"anio": 2025, "empresas_activas": 1500},
    ]


def test_evolucion_empresas_detecta_columnas_faltantes(monkeypatch) -> None:
    """La API debe fallar explícitamente si cambia la estructura del Excel."""
    frame = pd.DataFrame({"anio": [2025], "total": [1500]})
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/evolucion")

    assert response.status_code == 500
    assert "empresas_activas" in response.json()["detail"]


def test_cliente_dinamico_incluye_piloto_python_y_fallback() -> None:
    """El cliente servido debe incorporar la API sin retirar la lógica Excel existente."""
    response = client.get("/client-dynamic")

    assert response.status_code == 200
    assert "/api/empresas/evolucion" in response.text
    assert "excel-fallback" in response.text
    assert "evolucion_empresas_activas.xlsx" in response.text
