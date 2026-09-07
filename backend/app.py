"""API de publicaciones para el despliegue institucional Python/MySQL.

La API administra metadatos de publicaciones. Los archivos binarios siguen
en un volumen de datos u objeto de almacenamiento y no se guardan en MySQL.
"""
from functools import wraps
import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)


def db_connection():
    """Abre una conexión MySQL usando variables de entorno del despliegue."""
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        connect_timeout=int(os.getenv("MYSQL_CONNECT_TIMEOUT", "10")),
    )


def api_errors(view):
    """Convierte errores de conexión y consultas en respuestas JSON consistentes."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except pymysql.MySQLError:
            app.logger.exception("Error de base de datos")
            return jsonify(error="No fue posible consultar la base de datos"), 503

    return wrapped


@app.after_request
def add_cors_headers(response):
    """Permite consumir la API desde el frontend institucional configurado."""
    origins = os.getenv("CORS_ALLOWED_ORIGINS", "*")
    response.headers["Access-Control-Allow-Origin"] = origins
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


@app.get("/api/health")
def health():
    """Comprueba que el proceso Flask está disponible."""
    return jsonify(status="ok", service="demografia-de-empresas-api")


@app.get("/api/categorias")
@api_errors
def categorias():
    """Lista las categorías que tienen al menos un recurso publicado."""
    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.slug, c.nombre, c.seccion, c.orden,
                   COUNT(r.id) AS recursos_publicados
              FROM categorias AS c
              JOIN recursos AS r ON r.categoria_id = c.id
             WHERE r.estado = 'publicado'
             GROUP BY c.id, c.slug, c.nombre, c.seccion, c.orden
             ORDER BY c.orden, c.nombre
            """
        )
        return jsonify(cursor.fetchall())


@app.get("/api/publicaciones")
@api_errors
def publicaciones():
    """Entrega recursos publicados con filtros opcionales.

    Parámetros:
      categoria: slug de la categoría.
      tipo: tipo de archivo, por ejemplo XLSX o PDF.
      q: texto parcial sobre título o nombre de archivo.
      documentacion: si es 1, incluye categorías de documentación.
    """
    conditions = ["r.estado = 'publicado'"]
    params = []

    categoria = request.args.get("categoria", "").strip()
    tipo = request.args.get("tipo", "").strip().upper()
    query = request.args.get("q", "").strip()
    incluir_documentacion = request.args.get("documentacion", "0") == "1"

    if categoria:
        conditions.append("c.slug = %s")
        params.append(categoria)
    if tipo:
        conditions.append("UPPER(r.tipo_archivo) = %s")
        params.append(tipo)
    if query:
        conditions.append("(r.titulo_publico LIKE %s OR r.nombre_archivo LIKE %s)")
        pattern = f"%{query}%"
        params.extend([pattern, pattern])
    if not incluir_documentacion:
        conditions.append("c.seccion = 'publicaciones'")

    where = " AND ".join(conditions)
    sql = f"""
        SELECT c.slug AS categoria, c.nombre AS categoria_nombre,
               c.seccion, r.titulo_publico, r.nombre_archivo,
               r.ruta_relativa, r.tipo_archivo, r.fecha_publicacion, r.orden
          FROM recursos AS r
          JOIN categorias AS c ON c.id = r.categoria_id
         WHERE {where}
         ORDER BY c.orden, r.orden, r.titulo_publico
    """

    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(sql, params)
        return jsonify(cursor.fetchall())


@app.errorhandler(404)
def not_found(_error):
    """Mantiene el formato JSON para rutas inexistentes."""
    return jsonify(error="Ruta no encontrada"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
