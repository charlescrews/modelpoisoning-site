# Artículo «Modelos maliciosos en Hugging Face»: cómo aplicarlo

1. Copia la carpeta `modelpoisoning-site/` del zip encima de tu repositorio, sobrescribiendo.
2. Si no lo hiciste con el comprobador de fuentes, pon `"updated": "2026-10-23"` en `site.json`.
3. Genera y sube:

```bash
py build.py
git add .
git commit -m "Artículo: modelos maliciosos en Hugging Face"
git push
```

4. En Search Console, pide la indexación de:
   - https://www.modelpoisoning.com/malicious-models-hugging-face/
   - https://www.modelpoisoning.com/es/modelos-maliciosos-hugging-face/

Archivos: el artículo en los dos idiomas, dos términos nuevos en `content/glossary.json` (Sleepy Pickle y reutilización de nombres), un enlace nuevo en los artículos de defensa y el texto de la portada en `build.py` (ya no dice «seis artículos»).
