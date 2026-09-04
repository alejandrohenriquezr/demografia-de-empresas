-- Recursos iniciales del sitio. Las rutas son relativas a datos_OE/.
INSERT INTO categorias (slug, nombre, seccion, orden) VALUES
  ('documentos-trabajo', 'Documentos de trabajo', 'publicaciones', 10),
  ('cuadros-estadisticos', 'Cuadros estadísticos', 'publicaciones', 20),
  ('metodologia', 'Metodología', 'documentacion', 10);

INSERT INTO recursos (categoria_id, titulo_publico, nombre_archivo, ruta_relativa, tipo_archivo, fecha_publicacion, estado, orden)
SELECT id, 'Cobertura del Registro Estadístico de Unidades Económicas (RUE)', '20260902_Documento_cobertura_RUE_borrador.pdf', 'datos_OE/documentos_de_trabajo/20260902_Documento_cobertura_RUE_borrador.pdf', 'PDF', '2026-09-02', 'publicado', 10 FROM categorias WHERE slug = 'documentos-trabajo';

INSERT INTO recursos (categoria_id, titulo_publico, nombre_archivo, ruta_relativa, tipo_archivo, fecha_publicacion, estado, orden)
SELECT id, 'Ficha metodológica', '10.08.2026.Ficha metodológica multifuente_RUE.pdf', 'datos_OE/metodologia/10.08.2026.Ficha metodológica multifuente_RUE.pdf', 'PDF', '2026-08-10', 'publicado', 10 FROM categorias WHERE slug = 'metodologia';

INSERT INTO recursos (categoria_id, titulo_publico, nombre_archivo, ruta_relativa, tipo_archivo, fecha_publicacion, estado, orden)
SELECT c.id, x.titulo, x.archivo, CONCAT('datos_OE/cuadros_estadisticos/', x.archivo), 'XLSX', '2026-09-03', 'publicado', x.orden
FROM categorias c CROSS JOIN (
  SELECT 10 orden, 'comparacion_empresas_por_criter.xlsx' archivo, 'Comparación de empresas por criterio' titulo UNION ALL
  SELECT 20, 'empresas_2025_por_ciiu_clase.xlsx', 'Empresas 2025 por clase CIIU' UNION ALL
  SELECT 30, 'empresas_2025_por_ciiu_division.xlsx', 'Empresas 2025 por división CIIU' UNION ALL
  SELECT 40, 'empresas_2025_por_ciiu_grupo.xlsx', 'Empresas 2025 por grupo CIIU' UNION ALL
  SELECT 50, 'empresas_2025_por_ciiu_seccion.xlsx', 'Empresas 2025 por sección CIIU' UNION ALL
  SELECT 60, 'empresas_2025_por_ciiu_subclase.xlsx', 'Empresas 2025 por subclase CIIU' UNION ALL
  SELECT 70, 'empresas_2025_por_comuna.xlsx', 'Empresas 2025 por comuna' UNION ALL
  SELECT 80, 'empresas_2025_por_estrato_venta.xlsx', 'Empresas 2025 por estrato de ventas' UNION ALL
  SELECT 90, 'empresas_2025_por_provincia.xlsx', 'Empresas 2025 por provincia' UNION ALL
  SELECT 100, 'empresas_2025_por_region.xlsx', 'Empresas 2025 por región' UNION ALL
  SELECT 110, 'empresas_2025_por_tamano_trabaj.xlsx', 'Empresas 2025 por tamaño de trabajadores' UNION ALL
  SELECT 120, 'empresas_2025_por_tamano_ventas.xlsx', 'Empresas 2025 por tamaño de ventas' UNION ALL
  SELECT 130, 'empresas_2025_por_tramo_trabaja.xlsx', 'Empresas 2025 por tramo de trabajadores' UNION ALL
  SELECT 140, 'evolucion_empresas_activas.xlsx', 'Evolución de empresas activas' UNION ALL
  SELECT 150, 'interaccion_variables_desagrega.xlsx', 'Interacción de variables desagregadas' UNION ALL
  SELECT 160, 'interaccion_variables_nacimient.xlsx', 'Interacción de variables de nacimientos' UNION ALL
  SELECT 170, 'nacimientos_muertes_por_anio.xlsx', 'Nacimientos y muertes por año' UNION ALL
  SELECT 180, 'nacimientos_muertes_por_ciiu.xlsx', 'Nacimientos y muertes por CIIU' UNION ALL
  SELECT 190, 'nacimientos_muertes_por_region.xlsx', 'Nacimientos y muertes por región' UNION ALL
  SELECT 200, 'nac_muertes_tamano_trabajadores.xlsx', 'Nacimientos y muertes por tamaño de trabajadores' UNION ALL
  SELECT 210, 'nac_muertes_tamano_ventas.xlsx', 'Nacimientos y muertes por tamaño de ventas' UNION ALL
  SELECT 220, 'supervivencia_empresas_por_coho.xlsx', 'Supervivencia de empresas por cohorte' UNION ALL
  SELECT 230, 'tasas_nacimientos_muertes.xlsx', 'Tasas de nacimientos y muertes'
) x WHERE c.slug = 'cuadros-estadisticos';

