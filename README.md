# Demografía de empresas

Aplicación de difusión de resultados de demografía empresarial del Instituto Nacional de Estadísticas (INE), elaborados como estadísticas experimentales a partir del Registro Estadístico de Unidades Económicas (RUE) 2025.

La rama `migracion-python` contiene la versión local basada en FastAPI. La interfaz mantiene la maqueta existente y el frontend piloto consulta los datos mediante endpoints Python. Durante la transición conserva un fallback a los archivos Excel.

## Requisitos

- Windows 10/11, macOS o Linux.
- Git.
- Python 3.12 o superior.
- No se requiere permisos de administrador, MySQL, Docker ni Node.js para ejecutar la versión Python local.
- Los archivos estadísticos deben estar en `datos_OE/cuadros_estadisticos/`.

## Instalación desde cero

En PowerShell de Windows:

```powershell
git clone -b migracion-python https://github.com/alejandrohenriquezr/demografia-de-empresas.git
cd demografia-de-empresas
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-python.txt
```

Si `python` no es reconocido, instale Python desde [python.org](https://www.python.org/downloads/) y marque `Add python.exe to PATH`. También puede usar `py -3.12` si el Python Launcher está instalado.

## Configuración local y SQLite

La versión local usa SQLite, incluida en Python. No hay que instalar ni iniciar un motor de base de datos.

Inicialice el catálogo:

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe scripts\init_db.py
```

La base se crea en `data/demografia_empresas.sqlite3`. El script crea las tablas `categorias` y `recursos`, e incorpora los 23 cuadros estadísticos del catálogo.

Para cambiar la ubicación de la base:

```powershell
$env:SQLITE_PATH="C:\ruta\demografia_empresas.sqlite3"
```

## Verificación

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m compileall -q app
.\.venv\Scripts\python.exe -m pytest -q
```

El CI de GitHub ejecuta las mismas verificaciones en cada cambio de la rama [migracion-python](https://github.com/alejandrohenriquezr/demografia-de-empresas/actions).

## Ejecución

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Abrir:

- Aplicación: http://127.0.0.1:8000/
- Salud: http://127.0.0.1:8000/health
- Documentación OpenAPI: http://127.0.0.1:8000/docs
- Catálogo SQLite: http://127.0.0.1:8000/api/catalogo
- Empresas por región: http://127.0.0.1:8000/api/empresas/region

Detener con `Ctrl+C`.

## API disponible

Los endpoints se encuentran bajo `/api/empresas`:

`evolucion`, `region`, `actividad`, `comuna`, `provincia`, `tamano-trabajadores`, `tamano-ventas`, `nacimientos-muertes`, `tasas`, `supervivencia`, `interaccion`, `interaccion-nacimientos`, `comparacion-criterios` y `ciiu/{clase|division|grupo|subclase}`.

Cada endpoint lee el primer libro de su Excel, valida las columnas requeridas y devuelve JSON ordenado. La documentación interactiva en `/docs` permite probarlos.

## Estructura

- `app/main.py`: aplicación FastAPI, página, recursos estáticos y catálogo SQLite.
- `app/api/empresas.py`: endpoints de indicadores.
- `app/data/excel_loader.py`: lector y perfilador de Excel.
- `app/data/catalog.py`: catálogo de los 23 cuadros.
- `app/data/sqlite_db.py`: conexión y esquema SQLite local.
- `app/static/pilot_empresas_5_1.js`: capa frontend que consulta la API Python.
- `scripts/init_db.py`: creación y carga inicial del catálogo.
- `tests/` y `app/tests/`: pruebas automatizadas.
- `datos_OE/`: Excel y documentos publicados.
- `backend/`: diseño MySQL previsto para el despliegue institucional.

## Datos

No cambiar nombres de archivos ni columnas sin actualizar el catálogo, los endpoints y las pruebas. Si los archivos no están incluidos en una copia de trabajo, deben descargarse de la fuente institucional y ubicarse en las rutas descritas por los README dentro de `datos_OE/`.

## Despliegue institucional

SQLite es sólo el modo local. Para producción se prevé MySQL, almacenamiento institucional de archivos y ejecución de FastAPI con Uvicorn o Gunicorn. El esquema MySQL y la documentación de esa alternativa están en `backend/`.

No se deben versionar credenciales, archivos `.env`, bases SQLite ni artefactos generados.
