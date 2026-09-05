"""Pruebas de compatibilidad entre FastAPI y las rutas del Worker actual."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_index_entrega_html_actual() -> None:
    """La raíz debe servir la interfaz HTML existente."""
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Demografía de empresas | INE Chile" in response.text


def test_cliente_dinamico_sigue_disponible() -> None:
    """La ruta usada por el frontend debe seguir entregando el cliente JavaScript."""
    response = client.get("/client-dynamic")

    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]


def test_sheetjs_sigue_disponible() -> None:
    """La biblioteca SheetJS debe seguir accesible durante la migración."""
    response = client.get("/xlsx")

    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]


def test_asset_existente_sigue_disponible() -> None:
    """Los assets actuales deben conservar sus rutas públicas."""
    response = client.get("/assets/logo-ine.jpg")

    assert response.status_code == 200
