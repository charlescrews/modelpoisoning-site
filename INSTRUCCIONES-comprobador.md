# Comprobador de modelos: cómo aplicarlo

Este zip trae solo los archivos nuevos o modificados. No incluye `site.json`, el aviso legal ni la carpeta `public/`, así que no pisa tus datos.

1. Descomprime el zip y copia su carpeta `modelpoisoning-site/` encima de la de tu repositorio, sobrescribiendo.
2. Revisa `content/pages/privacy.en.md` y `privacy.es.md`: ahora dicen que el sitio está en GitHub Pages (antes ponía IONOS) y explican el comprobador. El responsable aparece solo con nombre y correo, como en tu versión publicada. Si habías añadido algo más a esas páginas, vuelve a ponerlo.
3. En `site.json`, cambia `"updated"` a `"2026-10-22"`.
4. Genera la web y súbela:

```bash
python3 build.py
git add .
git commit -m "Comprobador de modelos de Hugging Face"
git push
```

5. Cuando GitHub Pages termine de publicar, abre https://www.modelpoisoning.com/model-checker/ y pulsa el ejemplo `openai-community/gpt2`. Si sale un error de conexión, avísame.
6. En Search Console, inspecciona la URL nueva y pide que se indexe (las dos versiones de idioma).

Archivos que cambian: `build.py`, `static/style.css`, `static/checker.js` (nuevo), `content/tools/` (nuevo), `content/pages/privacy.*.md`, los dos artículos de defensa (un enlace nuevo) y `README.md` (apartado 7).
