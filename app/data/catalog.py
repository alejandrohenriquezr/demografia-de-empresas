"""Catálogo de insumos oficiales usados por Demografía de Empresas.

Mantiene en Python la misma lista de archivos que valida actualmente el script Node.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
CUADROS_DIR = ROOT_DIR / "datos_OE" / "cuadros_estadisticos"

XLSX_FILES = [
    "comparacion_empresas_por_criter.xlsx",
    "empresas_2025_por_ciiu_clase.xlsx",
    "empresas_2025_por_ciiu_division.xlsx",
    "empresas_2025_por_ciiu_grupo.xlsx",
    "empresas_2025_por_ciiu_seccion.xlsx",
    "empresas_2025_por_ciiu_subclase.xlsx",
    "empresas_2025_por_comuna.xlsx",
    "empresas_2025_por_estrato_venta.xlsx",
    "empresas_2025_por_provincia.xlsx",
    "empresas_2025_por_region.xlsx",
    "empresas_2025_por_tamano_trabaj.xlsx",
    "empresas_2025_por_tamano_ventas.xlsx",
    "empresas_2025_por_tramo_trabaja.xlsx",
    "evolucion_empresas_activas.xlsx",
    "interaccion_variables_desagrega.xlsx",
    "interaccion_variables_nacimient.xlsx",
    "nac_muertes_tamano_trabajadores.xlsx",
    "nac_muertes_tamano_ventas.xlsx",
    "nacimientos_muertes_por_anio.xlsx",
    "nacimientos_muertes_por_ciiu.xlsx",
    "nacimientos_muertes_por_region.xlsx",
    "supervivencia_empresas_por_coho.xlsx",
    "tasas_nacimientos_muertes.xlsx",
]

PDF_FILES = [
    ROOT_DIR / "datos_OE" / "documentos_de_trabajo" / "20260902_Documento_cobertura_RUE_borrador.pdf",
    ROOT_DIR / "datos_OE" / "metodologia" / "10.08.2026.Ficha metodológica multifuente_RUE.pdf",
]

REQUIRED_FILES = [CUADROS_DIR / name for name in XLSX_FILES] + PDF_FILES
