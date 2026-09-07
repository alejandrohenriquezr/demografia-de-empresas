# API Python de publicaciones y cuadros estadísticos

Esta carpeta contiene la segunda etapa de la migración del catálogo y de la lectura de datos desde el Worker hacia Python/MySQL. MySQL administra metadatos; los Excel y PDF permanecen en un volumen institucional o repositorio de objetos.

## Puesta en marcha

1. Crear la base indicada por `MYSQL_DATABASE`.
2. Ejecutar `schema.sql` y luego `seed.sql`.
3. Copiar `.env.example` a `.env`, completar las credenciales y definir `DATA_ROOT` si los datos no están en `datos_OE/`.
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

## Endpoints

- `GET /api/health`: comprueba que el proceso está disponible.
- `GET /api/categorias`: lista categorías con recursos publicados.
- `GET /api/publicaciones`: lista recursos publicados de la sección publicaciones.
- `GET /api/cuadros/<archivo.xlsx>`: devuelve las filas del primer libro publicado.
- `GET /api/cuadros/<archivo.xlsx>?offset=0&limit=10000`: pagina la respuesta, con un máximo de 50.000 filas.

Ejemplos de filtros para publicaciones:

- `/api/publicaciones?categoria=cuadros-estadisticos`
- `/api/publicaciones?tipo=XLSX`
- `/api/publicaciones?q=region`
- `/api/publicaciones?documentacion=1`

El endpoint de cuadros sólo admite un nombre XLSX simple, comprueba que el archivo esté publicado en MySQL y resuelve la ruta bajo `DATA_ROOT`. No acepta rutas arbitrarias ni archivos no publicados. Las consultas SQL usan parámetros vinculados.

## Situación de la migración

El Worker de Sites continúa sirviendo la interfaz actual y sus archivos empaquetados, porque ese entorno no ejecuta Python ni conecta directamente a MySQL. El frontend institucional puede reemplazar progresivamente la lectura con `/api/cuadros/<archivo.xlsx>`. La siguiente etapa será crear un adaptador JavaScript con una URL de API configurable y migrar una visualización a la vez, conservando un fallback controlado durante la transición.
