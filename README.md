# Demografía de empresas

Sitio para la difusión de resultados de demografía empresarial del Instituto Nacional de Estadísticas (INE), elaborados como estadísticas experimentales a partir del Registro Estadístico de Unidades Económicas (RUE) 2025. Permite consultar empresas activas, nacimientos, muertes, supervivencia y empleo, y navegar por desagregaciones territoriales, actividad económica y tamaño.

## Arquitectura

La interfaz es HTML/CSS/JavaScript con gráficos Plotly. `worker/index.js` es un Worker sin servidor que entrega la portada, el cliente dinámico, SheetJS, logos y archivos de `datos_OE/`. `worker/client.js` descarga cada Excel publicado, lee su primera hoja en el navegador y actualiza los gráficos y enlaces de descarga. `scripts/build.mjs` genera el artefacto reproducible `dist/server/index.js`; `dist/` no se versiona.

El sitio de ChatGPT Sites funciona sin base de datos ni API de negocio en producción: los datos se empaquetan durante el build. El backend opcional de `backend/` sirve para una migración institucional con Python, Flask y MySQL, donde administra el catálogo de publicaciones. El cliente dinámico admite `window.RUE_API_BASE`; al definir, por ejemplo, `window.RUE_API_BASE = "https://api.institucional.ine.gob.cl/demografia-empresas"` antes de cargar `/client-dynamic`, el gráfico de evolución usa `GET /api/cuadros/evolucion_empresas_activas.xlsx`. Si la API falla, usa el cuadro XLSX empaquetado.

## Requisitos y ejecución

Se requiere Node.js 20 o superior. Instale dependencias del backend sólo si va a usarlo (`python -m venv .venv && pip install -r backend/requirements.txt`). Copie los insumos siguiendo [`datos_OE/`](datos_OE/cuadros_estadisticos/README.md), configure los dos PDF y ejecute:

```bash
npm run validate:data
npm run build
```

El resultado queda en `dist/server/index.js` y contiene todos los recursos necesarios para el Worker. Para publicar en Sites se usa el empaquetador de Sites sobre `dist/` y `.openai/hosting.json`; el acceso actual es privado. El proyecto de Sites es `appgprj_6a998f0376f08191b246fa98dae11ba9`.

## Datos y publicaciones

Los Excel y PDF se versionan en GitHub porque este repositorio es público. Antes de construir deben estar en las rutas exactas indicadas en los README de [`datos_OE/cuadros_estadisticos`](datos_OE/cuadros_estadisticos/README.md), [`documentos_de_trabajo`](datos_OE/documentos_de_trabajo/README.md) y [`metodologia`](datos_OE/metodologia/README.md). `scripts/validate-data.mjs` falla con la lista de archivos faltantes. No se debe volver a usar el libro monolítico RUE: el análisis consume únicamente los 23 Excel publicados en “Cuadros estadísticos”.

## Rutas HTTP del Worker

`/` entrega la aplicación; `/xlsx` entrega la biblioteca SheetJS; `/client-dynamic` entrega el cliente de análisis; `/assets/<archivo>` entrega los logos; `/datos_OE/<ruta>` entrega un Excel o PDF publicado para lectura/descarga. No existe `/api/workbook` en la versión actual. Las descargas se realizan directamente desde las rutas de datos y no exponen credenciales.

## API y base de datos opcionales

La migración Python/MySQL está documentada en [`backend/README.md`](backend/README.md). `backend/schema.sql` define `categorias` y `recursos`: una categoría agrupa recursos de publicaciones o documentación; cada recurso conserva título público, nombre físico, ruta relativa, tipo, fecha, estado y orden. `backend/seed.sql` carga las tres categorías y el catálogo inicial. `backend/app.py` expone `GET /api/publicaciones`, devuelve sólo recursos `publicado` y lee conexión desde `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DATABASE` (ver `.env.example`). Los binarios permanecen en `datos_OE/` o en un volumen/repositorio de objetos; MySQL administra metadatos, no archivos.

## Estructura

`index.html` contiene la maqueta y estilos; `worker/` contiene servidor, cliente y dependencia vendorizada; `scripts/` contiene build y validación; `assets/` contiene logos; `datos_OE/` contiene insumos fuera de Git; `backend/` contiene la API/catalogación MySQL; `.openai/hosting.json` identifica el proyecto Sites.

## Reproducción y mantenimiento

1. Obtenga la misma edición oficial de los 23 Excel y 2 PDF, respetando nombres y estructura.
2. Ejecute `npm run validate:data` y `npm run build`.
3. Revise el artefacto y publique `dist/` en el entorno elegido.
4. Para cambiar un dato, reemplace el archivo correspondiente y reconstruya; no cambie nombres ni hojas sin actualizar `worker/client.js`.
5. Para MySQL, ejecute `schema.sql`, luego `seed.sql`, configure variables de entorno y arranque Flask con `flask --app backend/app run`.

Los datos deben manejarse conforme a las políticas del INE. No se incluyen credenciales, `.env` ni artefactos generados.
