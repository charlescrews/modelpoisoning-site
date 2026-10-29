# Actualización completa de modelpoisoning.com (29/10/2026)

Reúne todos los cambios desde el comprobador de modelos, incluidos los de hoy: portada con las herramientas arriba,
diagramas en cuatro artículos, recuadros de herramienta, etiquetas «Nuevo/Actualizado», fecha automática y RSS.
No incluye site.json, el aviso legal ni la carpeta public/.

1. git pull
2. Copiar la carpeta modelpoisoning-site del zip encima del repositorio (reemplazar archivos). Hay un archivo nuevo, figures.py, junto a build.py.
3. py build.py  (debe decir "Built 34 pages into public/")
4. git add . && git commit -m "Diseño: herramientas en portada, diagramas y RSS" && git push
