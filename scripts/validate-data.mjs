import { access } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const xlsx = [
  "comparacion_empresas_por_criter.xlsx", "empresas_2025_por_ciiu_clase.xlsx", "empresas_2025_por_ciiu_division.xlsx",
  "empresas_2025_por_ciiu_grupo.xlsx", "empresas_2025_por_ciiu_seccion.xlsx", "empresas_2025_por_ciiu_subclase.xlsx",
  "empresas_2025_por_comuna.xlsx", "empresas_2025_por_estrato_venta.xlsx", "empresas_2025_por_provincia.xlsx",
  "empresas_2025_por_region.xlsx", "empresas_2025_por_tamano_trabaj.xlsx", "empresas_2025_por_tamano_ventas.xlsx",
  "empresas_2025_por_tramo_trabaja.xlsx", "evolucion_empresas_activas.xlsx", "interaccion_variables_desagrega.xlsx",
  "interaccion_variables_nacimient.xlsx", "nac_muertes_tamano_trabajadores.xlsx", "nac_muertes_tamano_ventas.xlsx",
  "nacimientos_muertes_por_anio.xlsx", "nacimientos_muertes_por_ciiu.xlsx", "nacimientos_muertes_por_region.xlsx",
  "supervivencia_empresas_por_coho.xlsx", "tasas_nacimientos_muertes.xlsx"
];
const required = xlsx.map(f => resolve(root, "datos_OE/cuadros_estadisticos", f)).concat([
  resolve(root, "datos_OE/documentos_de_trabajo/20260902_Documento_cobertura_RUE_borrador.pdf"),
  resolve(root, "datos_OE/metodologia/10.08.2026.Ficha metodológica multifuente_RUE.pdf")
]);
const missing = [];
for (const file of required) { try { await access(file); } catch { missing.push(file.replace(`${root}/`, "")); } }
if (missing.length) { console.error("Faltan archivos de datos:"); missing.forEach(x => console.error(`- ${x}`)); process.exit(1); }
console.log(`Datos completos: ${required.length} archivos listos.`);

