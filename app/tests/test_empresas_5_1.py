"""Pruebas de la etapa 5.1 para los endpoints de empresas activas."""

import pandas as pd
from fastapi.testclient import TestClient

from app.api import empresas
from app.main import app

client = TestClient(app)


def _fake_frame(columns: dict) -> pd.DataFrame:
    """Crea un DataFrame de prueba con la estructura solicitada."""
    return pd.DataFrame(columns)


def test_region(monkeypatch) -> None:
    """La API regional debe devolver etiquetas y valores numéricos."""
    monkeypatch.setattr(
        empresas,
        "read_first_sheet",
        lambda path: _fake_frame({
            "region": ["Región A", "Región B"],
            "empresas_activas": [10, 20],
        }),
    )
    response = client.get("/api/empresas/region")
    assert response.status_code == 200
    assert response.json()[0] == {"region": "Región A", "empresas_activas": 10}


def test_actividad(monkeypatch) -> None:
    """La API CIIU debe conservar la glosa de actividad."""
    monkeypatch.setattr(
        empresas,
        "read_first_sheet",
        lambda path: _fake_frame({
            "glosa": ["Comercio"],
            "empresas_activas": [100],
        }),
    )
    response = client.get("/api/empresas/actividad")
    assert response.status_code == 200
    assert response.json() == [{"glosa": "Comercio", "empresas_activas": 100}]


def test_tamano_trabajadores(monkeypatch) -> None:
    """La API debe conservar categorías de tamaño según trabajadores."""
    monkeypatch.setattr(
        empresas,
        "read_first_sheet",
        lambda path: _fake_frame({
            "tamano": ["Micro"],
            "empresas_activas": [7],
        }),
    )
    response = client.get("/api/empresas/tamano-trabajadores")
    assert response.status_code == 200
    assert response.json()[0]["tamano"] == "Micro"


def test_tamano_ventas(monkeypatch) -> None:
    """La API debe conservar categorías de tamaño según ventas."""
    monkeypatch.setattr(
        empresas,
        "read_first_sheet",
        lambda path: _fake_frame({
            "tamano": ["Grande"],
            "empresas_activas": [9],
        }),
    )
    response = client.get("/api/empresas/tamano-ventas")
    assert response.status_code == 200
    assert response.json()[0]["empresas_activas"] == 9


def test_comparacion_se_ordena(monkeypatch) -> None:
    """La comparación debe quedar ordenada por categoría y año."""
    monkeypatch.setattr(
        empresas,
        "read_first_sheet",
        lambda path: _fake_frame({
            "categoria": ["B", "A", "A"],
            "anio": [2025, 2025, 2024],
            "empresas_activas": [3, 2, 1],
        }),
    )
    response = client.get("/api/empresas/comparacion-criterios")
    assert response.status_code == 200
    assert response.json() == [
        {"categoria": "A", "anio": 2024, "empresas_activas": 1},
        {"categoria": "A", "anio": 2025, "empresas_activas": 2},
        {"categoria": "B", "anio": 2025, "empresas_activas": 3},
    ]
