"""Pruebas de los endpoints del bloque de empresas activas migrado a Python."""

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_evolucion_empresas_entrega_serie_ordenada(monkeypatch) -> None:
    """La API debe devolver año y empresas activas ordenados cronológicamente."""
    frame = pd.DataFrame(
        {"anio": [2025, 2023, 2024], "empresas_activas": [1500, 1200, 1350]}
    )
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/evolucion")

    assert response.status_code == 200
    assert response.json() == [
        {"anio": 2023, "empresas_activas": 1200},
        {"anio": 2024, "empresas_activas": 1350},
        {"anio": 2025, "empresas_activas": 1500},
    ]


def test_region_actividad_y_tamanos(monkeypatch) -> None:
    """Los endpoints categóricos deben conservar etiquetas y valores del Excel."""
    frames = {
        "empresas_2025_por_region.xlsx": pd.DataFrame(
            {"region": ["B", "A"], "empresas_activas": [100, 300]}
        ),
        "empresas_2025_por_ciiu_seccion.xlsx": pd.DataFrame(
            {"glosa": ["Industria", "Comercio"], "empresas_activas": [200, 500]}
        ),
        "empresas_2025_por_tamano_trabaj.xlsx": pd.DataFrame(
            {"tamano": ["Micro", "Grande"], "empresas_activas": [700, 50]}
        ),
        "empresas_2025_por_tamano_ventas.xlsx": pd.DataFrame(
            {"tamano": ["Micro", "Grande"], "empresas_activas": [600, 60]}
        ),
    }

    def fake_read(path):
        return frames[path.name]

    monkeypatch.setattr("app.api.empresas.read_first_sheet", fake_read)

    assert client.get("/api/empresas/por-region").json()[0] == {
        "region": "A",
        "empresas_activas": 300,
    }
    assert client.get("/api/empresas/por-actividad").json()[0] == {
        "glosa": "Comercio",
        "empresas_activas": 500,
    }
    assert client.get("/api/empresas/por-tamano-trabajadores").status_code == 200
    assert client.get("/api/empresas/por-tamano-ventas").status_code == 200


def test_comparacion_criterios_agrupa_serie(monkeypatch) -> None:
    """La comparación debe quedar ordenada por categoría y año."""
    frame = pd.DataFrame(
        {
            "categoria": ["B", "A", "A"],
            "anio": [2025, 2025, 2024],
            "empresas_activas": [200, 150, 140],
        }
    )
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/comparacion-criterios")

    assert response.status_code == 200
    assert response.json()[:2] == [
        {"categoria": "A", "anio": 2024, "empresas_activas": 140},
        {"categoria": "A", "anio": 2025, "empresas_activas": 150},
    ]


def test_estructura_excel_invalida_genera_error_explicito(monkeypatch) -> None:
    """La API debe fallar explícitamente si cambia la estructura de un cuadro."""
    frame = pd.DataFrame({"anio": [2025], "total": [1500]})
    monkeypatch.setattr("app.api.empresas.read_first_sheet", lambda _path: frame)

    response = client.get("/api/empresas/evolucion")

    assert response.status_code == 500
    assert "empresas_activas" in response.json()["detail"]


def test_cliente_dinamico_incluye_bloque_python_y_fallback() -> None:
    """El cliente servido debe referenciar las APIs sin retirar la lógica Excel existente."""
    response = client.get("/client-dynamic")

    assert response.status_code == 200
    for path in (
        "/api/empresas/evolucion",
        "/api/empresas/por-region",
        "/api/empresas/por-actividad",
        "/api/empresas/por-tamano-trabajadores",
        "/api/empresas/por-tamano-ventas",
        "/api/empresas/comparacion-criterios",
    ):
        assert path in response.text
    assert "excel-fallback" in response.text
    assert "evolucion_empresas_activas.xlsx" in response.text
