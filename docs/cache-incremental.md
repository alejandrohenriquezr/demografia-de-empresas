# Actualización incremental de la caché

El proceso de construcción calcula un manifiesto SHA-256 para cada Excel ubicado en
`datos_OE/cuadros_estadisticos/`. El manifiesto se guarda en
`dist/cache/manifest.json` e incluye hash, tamaño, fecha de modificación, archivos
cambiados y archivos eliminados.

El workflow `.github/workflows/cache-check.yml` se ejecuta cuando cambia un Excel o
el código que construye el sitio. Valida los insumos, recalcula el manifiesto y genera
un artefacto de publicación.

La comparación evita considerar que existe una actualización cuando los archivos no
cambiaron. Para publicar automáticamente en Sites se debe conectar el último paso del
workflow con las credenciales de despliegue del proyecto
`appgprj_6a998f0376f08191b246fa98dae11ba9`; esas credenciales no se almacenan en el
repositorio.
