# Administración de publicaciones

Esta carpeta permite trasladar el catálogo de recursos a un entorno Python/MySQL.

1. Crear la base de datos definida en `MYSQL_DATABASE`.
2. Ejecutar `schema.sql` y luego `seed.sql`.
3. Configurar las variables del archivo `.env.example` en el entorno de despliegue.
4. Ejecutar `flask --app app run` para disponer de `GET /api/publicaciones`.

Los archivos binarios permanecen bajo `datos_OE/`. En un servidor institucional, esa carpeta debe almacenarse en un volumen o repositorio de objetos y su ruta debe coincidir con `ruta_relativa`.

El sitio actualmente publicado en ChatGPT Sites entrega estos archivos desde su Worker, porque ese alojamiento no ejecuta Python ni conecta directamente a MySQL. La estructura anterior evita cambios de nomenclatura o de catálogo al migrar a infraestructura institucional.

