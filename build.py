#!/usr/bin/env python3
"""Static site generator for modelpoisoning.com.

Usage:
    pip install markdown
    python3 build.py

Reads content/ and static/, writes the finished site to public/.
Edit site.json for the owner details shown on the legal pages.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import math
import random
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import markdown

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUT = ROOT / "public"

CFG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
SITE_URL = CFG["site_url"].rstrip("/")
LANGS = ("en", "es")

# --------------------------------------------------------------------------
# Interface strings
# --------------------------------------------------------------------------
T = {
    "en": {
        "site_desc": "An independent reference on AI data and model poisoning: how attackers corrupt what AI systems learn, the research behind it, and how to defend against it.",
        "nav_articles": "Articles",
        "nav_timeline": "Timeline",
        "nav_glossary": "Glossary",
        "nav_about": "About",
        "switch_label": "Español",
        "switch_title": "Leer en español",
        "skip": "Skip to content",
        "hero_h1": "It takes a very small dose.",
        "hero_lead": "Model poisoning is the manipulation of the data or the model an AI system learns from, so that it behaves the way an attacker wants. This site explains how it works, follows the research and collects what defenders can do about it.",
        "hero_cta": "Read the explainer",
        "hero_cta2": "See the timeline",
        "dots_caption": "Each dot stands for a training document; {n} of the {total} are poisoned. In a 2025 study, about 250 documents were enough to plant a backdoor in a 13-billion-parameter model. Drawn to scale by share of training tokens, there would be one violet dot for every 625,000 grey ones.",
        "dots_link": "Read about the study",
        "dots_alt": "A field of grey dots representing training documents, with a few violet dots representing poisoned ones.",
        "start_h": "Start here",
        "start_intro": "Six articles that cover the essentials, from the basic definition to a practical defence checklist.",
        "timeline_h": "Timeline",
        "timeline_intro": "Real cases and research milestones, each with its primary source.",
        "timeline_more": "Full timeline with sources",
        "glossary_h": "Glossary",
        "glossary_intro": "The terms that come up again and again, in plain language.",
        "glossary_more": "All {n} terms",
        "min_read": "{n} min read",
        "published": "Published {d}",
        "updated": "Updated {d}",
        "in_short": "In short",
        "on_this_page": "On this page",
        "read_next": "Read next",
        "sources_h": "Sources",
        "source": "Source",
        "related": "Related article",
        "breadcrumb_home": "Home",
        "glossary_title": "Glossary of AI poisoning terms",
        "glossary_nav": "Glossary",
        "glossary_desc": "Plain-language definitions of AI data and model poisoning terms: backdoor, trigger, split-view poisoning, LLM grooming, memory poisoning, ML-BOM and more.",
        "glossary_lead": "Definitions of the terms used across this site and in research on data and model poisoning. Each links to the article where it matters most.",
        "footer_about": "An independent, non-commercial reference on AI data and model poisoning. No cookies, no trackers.",
        "footer_updated": "Last updated {d}",
        "notfound_title": "Page not found",
        "notfound_body": "This address does not match any page on the site. It may have moved when we reorganised the articles.",
        "notfound_cta": "Go to the home page",
        "pending": "[pending]",
    },
    "es": {
        "site_desc": "Referencia independiente sobre el envenenamiento de datos y modelos de IA: cómo se corrompe lo que aprenden los sistemas de IA, la investigación que lo respalda y cómo defenderse.",
        "nav_articles": "Artículos",
        "nav_timeline": "Cronología",
        "nav_glossary": "Glosario",
        "nav_about": "Sobre el sitio",
        "switch_label": "English",
        "switch_title": "Read in English",
        "skip": "Saltar al contenido",
        "hero_h1": "Basta una dosis muy pequeña.",
        "hero_lead": "El envenenamiento de modelos (model poisoning) es la manipulación de los datos o del modelo del que aprende un sistema de IA para que se comporte como quiere un atacante. Este sitio explica cómo funciona, sigue la investigación y recoge lo que pueden hacer los defensores.",
        "hero_cta": "Leer la explicación",
        "hero_cta2": "Ver la cronología",
        "dots_caption": "Cada punto representa un documento de entrenamiento; {n} de los {total} están envenenados. En un estudio de 2025, unos 250 documentos bastaron para plantar una puerta trasera en un modelo de 13.000 millones de parámetros. Dibujado a escala según la proporción de tokens, habría un punto violeta por cada 625.000 grises.",
        "dots_link": "Leer sobre el estudio",
        "dots_alt": "Un campo de puntos grises que representan documentos de entrenamiento, con unos pocos puntos violetas que representan documentos envenenados.",
        "start_h": "Por dónde empezar",
        "start_intro": "Seis artículos con lo esencial, desde la definición básica hasta una lista práctica de defensas.",
        "timeline_h": "Cronología",
        "timeline_intro": "Casos reales e hitos de investigación, cada uno con su fuente original.",
        "timeline_more": "Cronología completa con fuentes",
        "glossary_h": "Glosario",
        "glossary_intro": "Los términos que aparecen una y otra vez, explicados con claridad.",
        "glossary_more": "Los {n} términos",
        "min_read": "{n} min de lectura",
        "published": "Publicado el {d}",
        "updated": "Actualizado el {d}",
        "in_short": "En resumen",
        "on_this_page": "En esta página",
        "read_next": "Sigue leyendo",
        "sources_h": "Fuentes",
        "source": "Fuente",
        "related": "Artículo relacionado",
        "breadcrumb_home": "Inicio",
        "glossary_title": "Glosario del envenenamiento de la IA",
        "glossary_nav": "Glosario",
        "glossary_desc": "Definiciones claras de los términos del envenenamiento de datos y modelos de IA: puerta trasera, disparador, envenenamiento split-view, LLM grooming, envenenamiento de memoria, ML-BOM y más.",
        "glossary_lead": "Definiciones de los términos que se usan en este sitio y en la investigación sobre envenenamiento de datos y modelos. Cada una enlaza al artículo donde más importa.",
        "footer_about": "Referencia independiente y sin ánimo comercial sobre el envenenamiento de datos y modelos de IA. Sin cookies ni rastreadores.",
        "footer_updated": "Última actualización: {d}",
        "notfound_title": "Página no encontrada",
        "notfound_body": "Esta dirección no corresponde a ninguna página del sitio. Puede que haya cambiado al reorganizar los artículos.",
        "notfound_cta": "Ir a la página de inicio",
        "pending": "[pendiente]",
    },
}

MONTHS_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fmt_date(iso: str, lang: str) -> str:
    d = dt.date.fromisoformat(iso)
    if lang == "es":
        return f"{d.day} de {MONTHS_ES[d.month - 1]} de {d.year}"
    return f"{d.day} {d.strftime('%B')} {d.year}"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def smartq(s: str, lang: str) -> str:
    """Typographic quotes for plain-text strings from the JSON data files."""
    left, right = ("\u201c", "\u201d") if lang == "en" else ("\u00ab", "\u00bb")
    return re.sub(r'"([^"]+)"', lambda m: left + m.group(1) + right, s)


# --------------------------------------------------------------------------
# Content loading
# --------------------------------------------------------------------------
FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def parse_md(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    m = FM_RE.match(raw)
    if not m:
        sys.exit(f"Missing front matter in {path}")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    meta["body"] = m.group(2)
    meta["source_path"] = path
    return meta


articles: dict[str, dict[str, dict]] = {lang: {} for lang in LANGS}
for lang in LANGS:
    for p in sorted((CONTENT / lang).glob("*.md")):
        a = parse_md(p)
        a["slug"] = p.stem
        a["lang"] = lang
        a["type"] = "article"
        a["order"] = int(a.get("order", 99))
        articles[lang][a["key"]] = a

pages: dict[str, dict[str, dict]] = {lang: {} for lang in LANGS}
for p in sorted((CONTENT / "pages").glob("*.md")):
    key_lang = p.stem.split(".")
    lang = key_lang[-1]
    pg = parse_md(p)
    pg["lang"] = lang
    pages[lang][pg["key"]] = pg

timeline = json.loads((CONTENT / "timeline.json").read_text(encoding="utf-8"))
glossary = json.loads((CONTENT / "glossary.json").read_text(encoding="utf-8"))


def url_for(key: str, lang: str) -> str:
    """Root-relative URL for an article/page key in a language."""
    prefix = "/" if lang == "en" else "/es/"
    if key == "home":
        return prefix
    if key == "glossary":
        return prefix + ("glossary/" if lang == "en" else "glosario/")
    if key in articles[lang]:
        return prefix + articles[lang][key]["slug"] + "/"
    if key in pages[lang]:
        return prefix + pages[lang][key]["slug"] + "/"
    sys.exit(f"Unknown link key @{key} ({lang})")


def out_path(url: str) -> Path:
    return OUT / url.lstrip("/") / "index.html"


# --------------------------------------------------------------------------
# Placeholders for owner details
# --------------------------------------------------------------------------
missing_fields: set[str] = set()


def fill(text: str, lang: str) -> str:
    def rep(m):
        field = m.group(1).lower()
        val = CFG.get(field, "")
        if not val:
            missing_fields.add(field)
            return T[lang]["pending"]
        return val
    return re.sub(r"\{\{([A-Z_]+)\}\}", rep, text)


# --------------------------------------------------------------------------
# Markdown rendering
# --------------------------------------------------------------------------
def md_to_html(text: str, lang: str) -> str:
    text = re.sub(r"\]\(@([a-z0-9-]+)(#[a-z0-9-]+)?\)",
                  lambda m: f"]({url_for(m.group(1), lang)}{m.group(2) or ''})", text)
    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty", "toc"],
                           extension_configs={
                               "toc": {"slugify": slugify},
                               "smarty": {"substitutions": {
                                   "left-double-quote": "&ldquo;" if lang == "en" else "&laquo;",
                                   "right-double-quote": "&rdquo;" if lang == "en" else "&raquo;",
                               }},
                           })
    out = md.convert(text)
    # Mark external links
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener"', out)
    return out


def slugify(value: str, separator: str = "-") -> str:
    import unicodedata
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s_-]+", separator, value)


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", re.sub(r"\(https?://[^)]+\)", "", text)))


def render_timeline(lang: str, compact: bool = False) -> str:
    items = []
    prev_year = None
    for ev in timeline:
        year_cell = ev["year"] if ev["year"] != prev_year else ""
        prev_year = ev["year"]
        title = esc(ev["title"][lang])
        if compact:
            items.append(
                f'<li><span class="tl-year" aria-hidden="{str(not year_cell).lower()}">{year_cell or ev["year"]}</span>'
                f'<span class="tl-title">{title}</span></li>'
            )
            continue
        link = ""
        if ev.get("link"):
            a = articles[lang][ev["link"]]
            link = f' <a href="{url_for(ev["link"], lang)}">{esc(a["nav_title"])}</a>'
        items.append(
            f'<li class="tl-item"{(' id="y' + year_cell + '"') if year_cell else ''}><div class="tl-year">{year_cell}</div>'
            f'<div class="tl-body"><h3>{title}</h3>'
            f'<p class="tl-date">{esc(ev["date"][lang])}</p>'
            f'<p>{esc(smartq(ev["text"][lang], lang))}</p>'
            f'<p class="tl-links"><a href="{esc(ev["source"])}" rel="noopener">{T[lang]["source"]}</a>'
            f'{link}</p></div></li>'
        )
    cls = "timeline compact" if compact else "timeline"
    return f'<ol class="{cls}">' + "".join(items) + "</ol>"


def split_sources(body: str, lang: str) -> tuple[str, str]:
    heading = "## Sources" if lang == "en" else "## Fuentes"
    if heading in body:
        main, src = body.split(heading, 1)
        return main, src
    return body, ""


def render_article_body(a: dict) -> tuple[str, str, list[tuple[str, str]]]:
    lang = a["lang"]
    body, sources = split_sources(a["body"], lang)
    summary_html = ""
    m = re.search(r":::summary\n(.*?)\n:::", body, re.S)
    if m:
        summary_html = (f'<aside class="summary" aria-labelledby="summary-h">'
                        f'<h2 id="summary-h">{T[lang]["in_short"]}</h2>'
                        f'{md_to_html(m.group(1), lang)}</aside>')
        body = body.replace(m.group(0), "")
    has_tl = ":::timeline" in body
    body = body.replace(":::timeline", "<!--TIMELINE-->")
    body_html = md_to_html(body, lang)
    if has_tl:
        body_html = body_html.replace("<!--TIMELINE-->", render_timeline(lang))
        body_html = body_html.replace("<p>" + render_timeline(lang) + "</p>", render_timeline(lang))
    toc = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
    if has_tl:
        years = sorted({ev["year"] for ev in timeline})
        toc = [("y" + y, y) for y in years] + toc
    if sources:
        body_html += (f'<section class="sources" aria-labelledby="sources-h">'
                      f'<h2 id="sources-h">{T[lang]["sources_h"]}</h2>'
                      f'{md_to_html(sources, lang)}</section>')
        toc.append(("sources-h", T[lang]["sources_h"]))
    return summary_html, body_html, toc


# --------------------------------------------------------------------------
# Hero dot field (deterministic SVG)
# --------------------------------------------------------------------------
DOT_COLS, DOT_ROWS = 64, 18          # wide layout
DOT_COLS_M, DOT_ROWS_M = 32, 36      # narrow layout, same total
POISON_COUNT = 5


def dot_field_svg(lang: str, cols: int = DOT_COLS, rows: int = DOT_ROWS, cls: str = "wide") -> str:
    DOT_COLS, DOT_ROWS = cols, rows
    rnd = random.Random(250 + cols)
    total = DOT_COLS * DOT_ROWS
    poisoned = set(rnd.sample(range(total), POISON_COUNT))
    gap = 12
    w, h = DOT_COLS * gap, DOT_ROWS * gap
    circles = []
    for i in range(total):
        cx = (i % DOT_COLS) * gap + gap / 2
        cy = (i // DOT_COLS) * gap + gap / 2
        if i in poisoned:
            circles.append(f'<circle class="p" cx="{cx:g}" cy="{cy:g}" r="3.2"/>')
        else:
            circles.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="2.2"/>')
    return (f'<svg class="dots {cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(T[lang]["dots_alt"])}" '
            f'preserveAspectRatio="xMidYMid meet">' + "".join(circles) + "</svg>")


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
WORDMARK = ('<span class="wm">modelpo<span class="i">ı</span>son<span class="i p">ı</span>ng</span>')


def head(*, lang: str, title: str, desc: str, url: str, alt_urls: dict[str, str],
         og_type: str = "website", jsonld: list[dict] | None = None, noindex: bool = False) -> str:
    canonical = SITE_URL + url
    alts = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE_URL + u}">' for l, u in alt_urls.items()
    )
    if "en" in alt_urls:
        alts += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL + alt_urls["en"]}">'
    ld = "".join(
        f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>'
        for j in (jsonld or [])
    )
    og_img = SITE_URL + "/og.png"
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{alts}
{robots}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="modelpoisoning.com">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="{'en_GB' if lang == 'en' else 'es_ES'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#EDF0EC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131915" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-serif-4-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css?v={CSS_VERSION}">
{ld}
</head>"""


def header(lang: str, alt_url: str | None, current: str = "") -> str:
    t = T[lang]
    other = "es" if lang == "en" else "en"
    home = url_for("home", lang)

    def nav_link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'

    switch = ""
    if alt_url:
        switch = (f'<a class="lang" href="{alt_url}" hreflang="{other}" lang="{other}" '
                  f'title="{esc(t["switch_title"])}">{t["switch_label"]}</a>')
    return f"""<body>
<a class="skip" href="#main">{t['skip']}</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="{home}" aria-label="modelpoisoning.com">{WORDMARK}</a>
    <nav aria-label="{'Main' if lang == 'en' else 'Principal'}">
      <ul>
        {nav_link(home + '#articles', t['nav_articles'], 'articles')}
        {nav_link(url_for('history', lang), t['nav_timeline'], 'history')}
        {nav_link(url_for('glossary', lang), t['nav_glossary'], 'glossary')}
        {nav_link(url_for('about', lang), t['nav_about'], 'about')}
      </ul>
    </nav>
    {switch}
  </div>
</header>"""


def footer(lang: str, alt_url: str | None) -> str:
    t = T[lang]
    other = "es" if lang == "en" else "en"
    switch = (f'<li><a href="{alt_url}" hreflang="{other}" lang="{other}">{t["switch_label"]}</a></li>'
              if alt_url else "")
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <p class="footer-brand">{WORDMARK}</p>
      <p>{t['footer_about']}</p>
      <p class="muted">{t['footer_updated'].format(d=fmt_date(CFG['updated'], lang))}</p>
    </div>
    <ul class="footer-links">
      <li><a href="{url_for('about', lang)}">{pages[lang]['about']['nav_title']}</a></li>
      <li><a href="{url_for('legal', lang)}">{pages[lang]['legal']['nav_title']}</a></li>
      <li><a href="{url_for('privacy', lang)}">{pages[lang]['privacy']['nav_title']}</a></li>
      {switch}
    </ul>
  </div>
</footer>
</body>
</html>
"""


def write(url: str, html_text: str) -> None:
    p = out_path(url)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html_text, encoding="utf-8")


def sorted_articles(lang: str) -> list[dict]:
    return sorted(articles[lang].values(), key=lambda a: a["order"])


def reading_minutes(a: dict) -> int:
    words = word_count(a["body"])
    if ":::timeline" in a["body"]:
        words += sum(word_count(ev["text"][a["lang"]] + " " + ev["title"][a["lang"]]) for ev in timeline)
    return max(2, math.ceil(words / 220))


# --------------------------------------------------------------------------
# Page builders
# --------------------------------------------------------------------------
def build_home(lang: str) -> None:
    t = T[lang]
    url = url_for("home", lang)
    alts = {l: url_for("home", l) for l in LANGS}
    other = alts["es" if lang == "en" else "en"]
    rows = []
    for a in sorted_articles(lang):
        rows.append(
            f'<li><a href="{url_for(a["key"], lang)}">'
            f'<span class="row-title">{esc(a["nav_title"])}</span>'
            f'<span class="row-dek">{esc(a["dek"])}</span>'
            f'<span class="row-meta">{t["min_read"].format(n=reading_minutes(a))}</span>'
            f'</a></li>'
        )
    gl = sorted(glossary, key=lambda g: g["term"][lang].lower())
    picks = ["backdoor", "trigger", "split-view-poisoning", "llm-grooming", "memory-poisoning",
             "sleeper-agent", "ml-bom", "safetensors"]
    gl_links = "".join(
        f'<li><a href="{url_for("glossary", lang)}#{g["id"]}">{esc(g["term"][lang])}</a></li>'
        for g in gl if g["id"] in picks
    )
    jsonld = [{
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "modelpoisoning.com", "url": SITE_URL + url, "inLanguage": lang,
        "description": t["site_desc"],
    }]
    title = ("Model Poisoning: AI data and model poisoning explained" if lang == "en"
             else "Model Poisoning: el envenenamiento de datos y modelos de IA, explicado")
    doc = head(lang=lang, title=title, desc=t["site_desc"], url=url, alt_urls=alts, jsonld=jsonld)
    doc += header(lang, other, current="home")
    doc += f"""
<main id="main">
  <section class="hero wrap">
    <h1>{t['hero_h1']}</h1>
    <p class="lead">{t['hero_lead']}</p>
    <p class="actions">
      <a class="btn" href="{url_for('what-is', lang)}">{t['hero_cta']}</a>
      <a class="btn-quiet" href="{url_for('history', lang)}">{t['hero_cta2']}</a>
    </p>
  </section>
  <figure class="dotfield wrap">
    {dot_field_svg(lang)}
    {dot_field_svg(lang, DOT_COLS_M, DOT_ROWS_M, "narrow")}
    <figcaption>{t['dots_caption'].format(n=POISON_COUNT, total=f"{DOT_COLS * DOT_ROWS:,}".replace(",", "." if lang == "es" else ","))}
      <a href="{url_for('250-docs', lang)}">{t['dots_link']}</a></figcaption>
  </figure>

  <section class="wrap section" id="articles" aria-labelledby="articles-h">
    <div class="section-head">
      <h2 id="articles-h">{t['start_h']}</h2>
      <p>{t['start_intro']}</p>
    </div>
    <ul class="rows">{''.join(rows)}</ul>
  </section>

  <section class="wrap section split" aria-labelledby="tl-h">
    <div class="section-head">
      <h2 id="tl-h">{t['timeline_h']}</h2>
      <p>{t['timeline_intro']}</p>
      <p><a href="{url_for('history', lang)}">{t['timeline_more']}</a></p>
    </div>
    {render_timeline(lang, compact=True)}
  </section>

  <section class="wrap section split" aria-labelledby="gl-h">
    <div class="section-head">
      <h2 id="gl-h">{t['glossary_h']}</h2>
      <p>{t['glossary_intro']}</p>
      <p><a href="{url_for('glossary', lang)}">{t['glossary_more'].format(n=len(glossary))}</a></p>
    </div>
    <ul class="termlist">{gl_links}</ul>
  </section>
</main>
"""
    doc += footer(lang, other)
    write(url, doc)


def build_article(a: dict) -> None:
    lang = a["lang"]
    t = T[lang]
    key = a["key"]
    url = url_for(key, lang)
    alts = {l: url_for(key, l) for l in LANGS if key in articles[l]}
    other_lang = "es" if lang == "en" else "en"
    other = alts.get(other_lang)
    summary_html, body_html, toc = render_article_body(a)
    mins = reading_minutes(a)
    ordered = sorted_articles(lang)
    idx = [x["key"] for x in ordered].index(key)
    nxt = [ordered[(idx + 1) % len(ordered)], ordered[(idx + 2) % len(ordered)]]
    toc_html = "".join(f'<li><a href="#{i}">{txt}</a></li>' for i, txt in toc)
    next_html = "".join(
        f'<li><a href="{url_for(n["key"], lang)}"><span class="row-title">{esc(n["nav_title"])}</span>'
        f'<span class="row-dek">{esc(n["dek"])}</span></a></li>' for n in nxt
    )
    jsonld = [
        {
            "@context": "https://schema.org", "@type": "Article",
            "headline": a["title"], "description": a["description"],
            "inLanguage": lang, "datePublished": a["date"],
            "dateModified": a.get("updated", a["date"]),
            "mainEntityOfPage": SITE_URL + url,
            "image": SITE_URL + "/og.png",
            "author": {"@type": "Person", "name": CFG["editor_name"], "url": SITE_URL + url_for("about", lang)},
            "publisher": {"@type": "Organization", "name": "modelpoisoning.com", "url": SITE_URL + "/"},
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t["breadcrumb_home"], "item": SITE_URL + url_for("home", lang)},
                {"@type": "ListItem", "position": 2, "name": a["nav_title"], "item": SITE_URL + url},
            ],
        },
    ]
    doc = head(lang=lang, title=a["title"], desc=a["description"], url=url, alt_urls=alts,
               og_type="article", jsonld=jsonld)
    doc += header(lang, other, current=key)
    meta = f'{t["published"].format(d=fmt_date(a["date"], lang))}, {t["min_read"].format(n=mins)}'
    doc += f"""
<main id="main" class="wrap article-layout">
  <article class="article">
    <header class="article-head">
      <h1>{esc(a['title'])}</h1>
      <p class="dek">{esc(a['dek'])}</p>
      <p class="meta">{meta}</p>
    </header>
    {summary_html}
    <div class="prose">{body_html}</div>
  </article>
  <aside class="rail" aria-label="{t['on_this_page']}">
    <nav class="toc"><h2>{t['on_this_page']}</h2><ol>{toc_html}</ol></nav>
  </aside>
  <section class="read-next" aria-labelledby="next-h">
    <h2 id="next-h">{t['read_next']}</h2>
    <ul class="rows">{next_html}</ul>
  </section>
</main>
"""
    doc += footer(lang, other)
    write(url, doc)


def build_page(pg: dict) -> None:
    lang = pg["lang"]
    key = pg["key"]
    url = url_for(key, lang)
    alts = {l: url_for(key, l) for l in LANGS if key in pages[l]}
    other = alts.get("es" if lang == "en" else "en")
    body = md_to_html(fill(pg["body"], lang), lang)
    doc = head(lang=lang, title=f'{pg["title"]} | modelpoisoning.com', desc=pg["description"],
               url=url, alt_urls=alts, noindex=pg.get("noindex") == "true")
    doc += header(lang, other, current=key)
    doc += f"""
<main id="main" class="wrap page">
  <h1>{esc(pg['title'])}</h1>
  <div class="prose">{body}</div>
</main>
"""
    doc += footer(lang, other)
    write(url, doc)


def build_glossary(lang: str) -> None:
    t = T[lang]
    url = url_for("glossary", lang)
    alts = {l: url_for("glossary", l) for l in LANGS}
    other = alts["es" if lang == "en" else "en"]
    import unicodedata

    def sort_key(g):
        return unicodedata.normalize("NFKD", g["term"][lang]).encode("ascii", "ignore").decode().lower()

    items = sorted(glossary, key=sort_key)
    groups: dict[str, list] = {}
    for g in items:
        groups.setdefault(sort_key(g)[0].upper(), []).append(g)
    blocks = []
    for letter, gs in groups.items():
        dl = []
        for g in gs:
            link = ""
            if g.get("link"):
                link = (f' <a class="term-link" href="{url_for(g["link"], lang)}">'
                        f'{esc(articles[lang][g["link"]]["nav_title"])}</a>')
            dl.append(f'<div class="term" id="{g["id"]}"><dt>{esc(g["term"][lang])}</dt>'
                      f'<dd>{esc(smartq(g["def"][lang], lang))}{link}</dd></div>')
        blocks.append(f'<section class="letter" aria-label="{letter}"><p class="letter-mark" aria-hidden="true">{letter}</p>'
                      f'<dl>{"".join(dl)}</dl></section>')
    jsonld = [{
        "@context": "https://schema.org", "@type": "DefinedTermSet",
        "name": t["glossary_title"], "inLanguage": lang, "url": SITE_URL + url,
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": g["term"][lang], "description": g["def"][lang],
             "url": SITE_URL + url + "#" + g["id"]} for g in items
        ],
    }]
    doc = head(lang=lang, title=t["glossary_title"], desc=t["glossary_desc"], url=url,
               alt_urls=alts, jsonld=jsonld)
    doc += header(lang, other, current="glossary")
    doc += f"""
<main id="main" class="wrap page glossary">
  <h1>{t['glossary_title']}</h1>
  <p class="lead">{t['glossary_lead']}</p>
  {''.join(blocks)}
</main>
"""
    doc += footer(lang, other)
    write(url, doc)


def build_404() -> None:
    t = T["en"]
    te = T["es"]
    doc = head(lang="en", title=t["notfound_title"], desc=t["site_desc"], url="/404.html",
               alt_urls={}, noindex=True)
    doc += header("en", "/es/")
    doc += f"""
<main id="main" class="wrap page">
  <h1>{t['notfound_title']}</h1>
  <p class="lead">{t['notfound_body']}</p>
  <p><a class="btn" href="/">{t['notfound_cta']}</a></p>
  <p lang="es" class="muted">{te['notfound_body']} <a href="/es/">{te['notfound_cta']}</a>.</p>
</main>
"""
    doc += footer("en", "/es/")
    (OUT / "404.html").write_text(doc, encoding="utf-8")


def build_sitemap() -> None:
    entries = []

    def add(key_urls: dict[str, str], lastmod: str):
        for lang, u in key_urls.items():
            links = "".join(
                f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL + uu}"/>'
                for l, uu in key_urls.items()
            )
            if "en" in key_urls:
                links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL + key_urls["en"]}"/>'
            entries.append(f"<url><loc>{SITE_URL + u}</loc><lastmod>{lastmod}</lastmod>{links}</url>")

    add({l: url_for("home", l) for l in LANGS}, CFG["updated"])
    add({l: url_for("glossary", l) for l in LANGS}, CFG["updated"])
    for key, a in articles["en"].items():
        add({l: url_for(key, l) for l in LANGS if key in articles[l]}, a.get("updated", a["date"]))
    add({l: url_for("about", l) for l in LANGS}, CFG["updated"])
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(entries) + "\n</urlset>\n")
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
                                    encoding="utf-8")


# --------------------------------------------------------------------------
def main() -> None:
    global CSS_VERSION
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    import hashlib
    CSS_VERSION = hashlib.sha1((STATIC / "style.css").read_bytes()).hexdigest()[:8]

    for lang in LANGS:
        build_home(lang)
        build_glossary(lang)
        for a in articles[lang].values():
            build_article(a)
        for pg in pages[lang].values():
            build_page(pg)
    build_404()
    build_sitemap()

    n = len(list(OUT.rglob("index.html")))
    print(f"Built {n} pages into {OUT.relative_to(ROOT)}/")
    if missing_fields:
        print("WARNING: fill these fields in site.json before publishing: "
              + ", ".join(sorted(missing_fields)))


CSS_VERSION = "dev"

if __name__ == "__main__":
    main()
