"""API de administración de publicaciones para un despliegue Python/MySQL."""
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import pymysql

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
    )

@app.get("/api/publicaciones")
def publicaciones():
    """Entrega únicamente recursos publicados y ordenados para el sitio público."""
    with db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """SELECT c.slug AS categoria, c.nombre AS categoria_nombre,
                      r.titulo_publico, r.nombre_archivo, r.tipo_archivo, r.fecha_publicacion
                 FROM recursos r JOIN categorias c ON c.id = r.categoria_id
                WHERE r.estado = 'publicado'
                ORDER BY c.orden, r.orden, r.titulo_publico"""
        )
        return jsonify(cursor.fetchall())

