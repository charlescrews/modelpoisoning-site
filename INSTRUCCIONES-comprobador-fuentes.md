# Comprobador de fuentes: cómo aplicarlo

Este zip trae solo los archivos nuevos o modificados desde el comprobador de modelos.

1. Copia la carpeta `modelpoisoning-site/` del zip encima de tu repositorio (la carpeta donde está `.git`), sobrescribiendo.
2. `content/pages/privacy.en.md` viene completo: GitHub Pages, los dos comprobadores y el responsable con tu formato (Controller / Contact). Sustituye el tuyo por este.
3. En `site.json`, cambia `"updated"` a `"2026-10-23"`.
4. Genera y sube:

```bash
py build.py
git add .
git commit -m "Comprobador de fuentes y página de herramientas"
git push
```

5. Comprueba en la web: https://www.modelpoisoning.com/source-checker/ y pulsa «Try an example». Deben salir 2 de 4 fuentes en las listas.
6. En Search Console, pide la indexación de:
   - https://www.modelpoisoning.com/source-checker/
   - https://www.modelpoisoning.com/es/comprobador-fuentes/
   - https://www.modelpoisoning.com/tools/
   - https://www.modelpoisoning.com/es/herramientas/
