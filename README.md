# modelpoisoning.com

Web estática bilingüe (inglés en `/`, español en `/es/`) sobre el envenenamiento de datos y modelos de IA.
No necesita servidor, base de datos ni cookies: son archivos HTML/CSS que se generan con un pequeño script de Python.

```
content/            ← los textos (lo único que tocarás en el día a día)
  en/*.md           artículos en inglés
  es/*.md           artículos en español
  pages/*.md        Sobre el sitio, aviso legal, privacidad (en y es)
  timeline.json     la cronología (bilingüe)
  glossary.json     el glosario (bilingüe)
static/             CSS, tipografías, favicon, imagen para redes (og.png)
build.py            el generador
site.json           URL del sitio y datos del titular para el aviso legal
public/             ← LA WEB GENERADA (esta carpeta es la que se publica)
tools/og.html       plantilla de la imagen para redes sociales
```

---

## 0. Antes de publicar: completa tus datos legales

Abre `site.json` y rellena `nif`, `address` (domicilio completo) y `email`. La LSSI exige que el aviso legal identifique al titular. Mientras falten, las páginas legales muestran «[pendiente]» y el build lo avisa.

Para el email puedes usar uno existente o crear `contacto@modelpoisoning.com` (necesita un plan de correo en IONOS; Deploy Now no incluye correo).

Después regenera la web:

```bash
pip install markdown
python3 build.py
```

Para verla en local: `cd public && python3 -m http.server 8000` y abre http://localhost:8000.

---

## 1. Sube el proyecto a GitHub

1. Crea un repositorio nuevo en GitHub, por ejemplo `modelpoisoning-site` (puede ser privado).
2. Desde esta carpeta:

```bash
git init
git add .
git commit -m "Primera versión de modelpoisoning.com"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/modelpoisoning-site.git
git push -u origin main
```

La carpeta `public/` **se sube al repositorio** a propósito: es lo que publica Deploy Now.

---

## 2. Crea el proyecto en IONOS Deploy Now

1. Entra en tu cuenta de IONOS y abre **Deploy Now** (en el panel: menú de productos > Deploy Now, o https://ionos.space).
2. Elige el plan gratuito (Starter).
3. **Vincula tu cuenta de GitHub** y concede permisos a la app de IONOS.
4. Elige **"Deploy from my own GitHub repository"** y selecciona `modelpoisoning-site`.
5. En la configuración del build:
   - Tipo / framework: **sitio estático (Static HTML / sin framework)**.
   - **Build command: vacío** (la web ya está generada).
   - **Dist folder / Publish directory: `public`**.
6. Termina el asistente. Deploy Now crea un workflow en `.github/workflows/` del repositorio: no lo borres ni lo muevas.
7. Espera a que el despliegue pase a **Completed** y abre la URL de prueba que te da Deploy Now para comprobar que todo se ve bien.

> Si el asistente te obliga a poner un comando de build, usa
> `pip install markdown && python3 build.py` con carpeta `public`. Así GitHub regenera la web en cada push.

---

## 2 bis. Alternativa: GitHub Pages (gratis, sin Deploy Now)

El repositorio incluye `.github/workflows/pages.yml`, que publica `public/` en GitHub Pages en cada push a `main`.

1. El repositorio debe ser **público** (con GitHub Free, Pages no funciona en repos privados).
2. Repositorio > **Settings > Pages** > *Build and deployment* > Source: **GitHub Actions**.
3. Pestaña **Actions**: el workflow «Publicar en GitHub Pages» debe terminar en verde. La web queda en `https://TU_USUARIO.github.io/modelpoisoning-site/` (ahí los estilos pueden verse rotos porque la web espera estar en la raíz de un dominio; con el dominio propio se ve bien).
4. **Settings > Pages > Custom domain**: `www.modelpoisoning.com` > Save.
5. En IONOS, **Dominios y SSL > modelpoisoning.com > DNS** (antes, desconecta el dominio de MyWebsite):
   - Borra los registros **A** y **AAAA** que apunten a IONOS para `@` y para `www`.
   - Crea 4 registros **A** para `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - Crea un **CNAME** para `www` → `TU_USUARIO.github.io`
6. Cuando GitHub valide el DNS (minutos u horas), marca **Enforce HTTPS**.

GitHub redirige automáticamente `modelpoisoning.com` a `www.modelpoisoning.com`.

---

## 3. Conecta el dominio modelpoisoning.com (Deploy Now)

Ahora mismo el dominio está conectado a **MyWebsite Now** (la plantilla genérica). Hay que desconectarlo antes de asignarlo a Deploy Now:

1. En el panel de IONOS ve a **Dominios y SSL** > `modelpoisoning.com`.
2. Si aparece conectado a MyWebsite, **desconéctalo** (opción de cambiar el destino o el uso del dominio). IONOS no deja asignar un dominio con uso «gestionado» (MyWebsite) a otro destino sin quitar antes ese uso.
3. Vuelve a Deploy Now > tu proyecto > **Connect your domain** y elige `modelpoisoning.com` (y también `www.modelpoisoning.com`) para el despliegue de **Production**.
4. El certificado SSL se configura solo. La propagación puede tardar desde unos minutos hasta unas horas.

La web usa `https://www.modelpoisoning.com` como dirección canónica (en `site.json`). Si al final prefieres la versión sin `www`, cambia `site_url`, regenera y vuelve a subir.

### ⚠️ Antes de cancelar MyWebsite Now

En IONOS el dominio a veces viene **incluido en el paquete** de MyWebsite. Si cancelas el paquete sin más, podrías perder el dominio. Antes de cancelar, revisa en **Contratos** si el dominio es un contrato independiente o pregunta al soporte de IONOS cómo conservarlo (normalmente se puede pasar a un contrato de solo dominio).

---

## 4. Google Search Console (imprescindible para el tráfico y para vender)

1. Entra en https://search.google.com/search-console y añade una propiedad de tipo **Dominio**: `modelpoisoning.com`.
2. Google te dará un registro **TXT**. Añádelo en IONOS: **Dominios y SSL** > `modelpoisoning.com` > **DNS** > Añadir registro > TXT.
3. Cuando verifique, ve a **Sitemaps** y envía: `https://www.modelpoisoning.com/sitemap.xml`.
4. Opcional: en https://www.bing.com/webmasters puedes importar la propiedad directamente desde Search Console (Bing también alimenta a varios asistentes de IA).

Search Console mide clics, impresiones y posiciones **sin poner nada en la web**, por eso no hace falta banner de cookies. Esas métricas son las que un comprador te pedirá ver.

Si más adelante añades una analítica en la web, elige una sin cookies y actualiza `content/pages/privacy.*.md`.

---

## 5. Cómo publicar un artículo nuevo

1. Crea `content/en/mi-slug.md` y `content/es/mi-slug-es.md` con la **misma `key`** en la cabecera:

```markdown
---
key: mi-articulo
title: Título SEO completo (unos 60 caracteres)
nav_title: Título corto para listados
description: Descripción para Google (unos 150 caracteres).
dek: Subtítulo de una o dos frases.
date: 2026-11-01
order: 7
---

:::summary
- Punto clave 1
- Punto clave 2
:::

## Primera sección
Texto… Enlace interno a otro artículo: [texto](@250-docs)

## Sources        ← en español: "## Fuentes"
- [Fuente original](https://…)
```

2. `python3 build.py`
3. `git add . && git commit -m "Nuevo artículo" && git push` → Deploy Now lo publica solo.

Opcional en la cabecera: `updated: AAAA-MM-DD` cuando revises un artículo. Si añades un hito, edita `content/timeline.json`. Para un término, `content/glossary.json`.

Los enlaces internos usan `@clave` y el generador los convierte a la URL correcta en cada idioma. Las claves actuales son `what-is`, `250-docs`, `grooming`, `nightshade`, `defend`, `history`, `about`, `legal`, `privacy` y `glossary`.

---

## 6. Plan para ganar tráfico (y valor de venta)

- **Constancia:** 2 artículos al mes, en ambos idiomas. Ideas: envenenamiento en RAG, *model hubs* y archivos pickle, envenenamiento de código (asistentes de programación), legislación (AI Act y la integridad de los datos), un caso nuevo de la cronología con su análisis.
- **Actualiza la cronología** cada vez que salga un estudio o incidente relevante: es la página con más posibilidades de recibir enlaces.
- **Enlaces entrantes:** compártelo en LinkedIn, en foros técnicos y con quien escribe sobre seguridad de IA. Un recurso neutral y bien citado se enlaza más que una web comercial.
- **Mide desde el día 1** con Search Console y guarda capturas mensuales. Al vender, el historial de tráfico orgánico y los dominios que te enlazan es lo que sostiene el precio.
- **Nada de datos inventados:** la credibilidad es el activo. Cada cifra, con su fuente.

---

## 7. El comprobador de modelos

Página `/model-checker/` (en español `/es/comprobador-modelos/`). Funciona entero en el navegador del visitante: consulta la API pública de Hugging Face (`huggingface.co/api/models/…`) y no envía nada a este sitio. Coste cero, sin servidor.

- Textos de la página: `content/tools/model-checker.en.md` y `.es.md`.
- Mensajes de los resultados: diccionario `CHECKER_UI` en `build.py` (en y es).
- Lógica: `static/checker.js`, sin dependencias.
- Se puede enlazar con un modelo ya cargado: `https://www.modelpoisoning.com/model-checker/?model=openai-community/gpt2`.

Si cambias lo que hace (por ejemplo, consultar otro servicio), actualiza también `content/pages/privacy.*.md`.

---

## Notas técnicas

- Tipografías autoalojadas (Archivo y Source Serif 4, licencia SIL OFL, en `static/fonts/`): no se llama a Google Fonts.
- SEO incluido: `title`/`description` por página, canonical, `hreflang` en/es + `x-default`, Open Graph, datos estructurados (WebSite, Article, BreadcrumbList, DefinedTermSet), `sitemap.xml` con alternates y `robots.txt`.
- Modo oscuro automático según el sistema y respeto a «reducir movimiento».
- `og.png` (imagen al compartir en redes) se generó desde `tools/og.html`. Si cambias el titular, puedes regenerarla con cualquier captura de 1200×630.
