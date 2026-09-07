"""Persistencia SQLite para desarrollo local sin permisos de administrador."""
from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = Path(__import__("os").getenv("SQLITE_PATH", ROOT_DIR / "data" / "demografia_empresas.sqlite3"))

def connection() -> sqlite3.Connection:
    """Abre la base SQLite y devuelve filas como diccionarios."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize() -> None:
    """Crea las tablas locales si todavía no existen."""
    with connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            seccion TEXT NOT NULL CHECK (seccion IN ('publicaciones', 'documentacion')),
            orden INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS recursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL REFERENCES categorias(id),
            titulo_publico TEXT NOT NULL,
            nombre_archivo TEXT NOT NULL UNIQUE,
            ruta_relativa TEXT NOT NULL UNIQUE,
            tipo_archivo TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'publicado'
                CHECK (estado IN ('borrador', 'publicado', 'archivado')),
            orden INTEGER NOT NULL DEFAULT 0
        );
        """)
