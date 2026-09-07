# API Python de publicaciones

Esta carpeta contiene la primera etapa de la migración del catálogo desde el Worker hacia Python/MySQL. La API administra metadatos; los Excel y PDF siguen en un volumen institucional o repositorio de objetos.

## Puesta en marcha

1. Crear la base indicada por `MYSQL_DATABASE`.
2. Ejecutar `schema.sql` y luego `seed.sql`.
3. Copiar `.env.example` a `.env` y completar las credenciales.
4. Instalar dependencias:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
```

5. Ejecutar:

```bash
flask --app backend.app run --host 0.0.0.0 --port 8000
```

También puede iniciarse con `python backend/app.py`.

## Endpoints

- `GET /api/health`: comprueba que el proceso está disponible; no requiere MySQL.
- `GET /api/categorias`: lista categorías con recursos publicados.
- `GET /api/publicaciones`: lista recursos publicados de la sección publicaciones.
- `GET /api/publicaciones?categoria=cuadros-estadisticos`: filtra por categoría.
- `GET /api/publicaciones?tipo=XLSX`: filtra por tipo de archivo.
- `GET /api/publicaciones?q=region`: busca en título y nombre de archivo.
- `GET /api/publicaciones?documentacion=1`: incluye documentación.

Los filtros se envían como parámetros URL y las consultas usan parámetros vinculados para evitar interpolar valores del usuario. La variable `CORS_ALLOWED_ORIGINS` permite restringir el origen del frontend; por defecto queda abierta durante la integración.

## Situación de la migración

El Worker de Sites continúa sirviendo la interfaz y los archivos empaquetados, porque ese entorno no ejecuta Python ni conecta directamente a MySQL. El siguiente bloque debe reemplazar en el frontend el catálogo estático por `/api/categorias` y `/api/publicaciones`, y después trasladar gradualmente la lectura de cuadros Excel al backend. Esa conexión requiere definir la URL institucional de la API y la política de acceso CORS.
