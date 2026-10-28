# Actualización completa de modelpoisoning.com (28/10/2026)

Este zip reúne todos los cambios desde el comprobador de modelos: comprobador de fuentes, página de herramientas,
artículo de modelos maliciosos, privacidad actualizada, mejoras de SEO y redirecciones de las direcciones antiguas.
No incluye site.json, el aviso legal ni la carpeta public/.

Pasos: los del mensaje de Claude. Resumen:
1. git pull
2. Copiar la carpeta modelpoisoning-site del zip encima del repositorio (reemplazar archivos).
3. site.json → "updated": "2026-10-28"
4. py build.py  (debe decir "Built 34 pages into public/")
5. git add . && git commit -m "..." && git push
