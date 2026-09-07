"""Inicializa el catálogo SQLite para desarrollo local."""
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.data.catalog import XLSX_FILES
from app.data.sqlite_db import connection, initialize

initialize()
with connection() as conn:
    categorias = [
        ("cuadros-estadisticos", "Cuadros estadísticos", "publicaciones", 20),
        ("documentos-trabajo", "Documentos de trabajo", "publicaciones", 10),
        ("metodologia", "Metodología", "documentacion", 10),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO categorias (slug, nombre, seccion, orden) VALUES (?, ?, ?, ?)",
        categorias,
    )
    categoria_id = conn.execute(
        "SELECT id FROM categorias WHERE slug = 'cuadros-estadisticos'"
    ).fetchone()[0]
    recursos = [
        (
            categoria_id,
            Path(name).stem.replace("_", " ").title(),
            name,
            f"datos_OE/cuadros_estadisticos/{name}",
            "XLSX",
            index * 10,
        )
        for index, name in enumerate(XLSX_FILES, start=1)
    ]
    conn.executemany(
        """INSERT OR IGNORE INTO recursos
        (categoria_id, titulo_publico, nombre_archivo, ruta_relativa, tipo_archivo, orden)
        VALUES (?, ?, ?, ?, ?, ?)""",
        recursos,
    )
print("SQLite inicializada:", __import__("app.data.sqlite_db", fromlist=["DB_PATH"]).DB_PATH)
print("Cuadros catalogados:", len(XLSX_FILES))
