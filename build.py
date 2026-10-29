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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figures import figure  # noqa: E402

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
        "start_intro": "The essentials, from the basic definition to a practical defence checklist and real attacks on model hubs.",
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
        "nav_checker": "Model checker",
        "nav_tools": "Tools",
        "home_src": "Did a chatbot cite its sources?",
        "home_src_link": "Check them against known propaganda networks",
        "src_lists_h": "The full lists",
        "src_lists_intro": "Every domain VIGINUM has published, as it appears in its files. Addresses are written with [.] so they cannot be clicked by accident.",
        "src_list_pk": "Portal Kombat (Pravda network): {n} domains and subdomains",
        "src_list_rrn": "RRN (Doppelgänger): {n} domains",
        "src_list_updated": "Last updated by VIGINUM on {d}.",
        "src_noscript": "The source checker needs JavaScript, but you can search the full lists below with your browser's find function.",
        "tools_open": "Open",
        "tool_eyebrow": "Free tool",
        "card_model_desc": "See whether a model's files can run code on your machine and what its model card leaves out.",
        "card_src_desc": "Paste the links an AI assistant gave you and see whether any belong to known propaganda networks.",
        "tool_box_label": "Try it",
        "badge_new": "New",
        "badge_updated": "Updated",
        "rss": "RSS feed",
        "tools_aria": "Tools",
        "ck_label": "Model on Hugging Face",
        "ck_hint": "Write owner/model, paste a huggingface.co link or a pkg:huggingface Package URL. Add @revision to check a specific commit.",
        "ck_try": "Try:",
        "ck_eicar_note": "a test repository with deliberately malicious files",
        "ck_noscript": "The checker needs JavaScript. It runs in your browser and sends nothing to this site.",
        "home_ck_h": "Check a model",
        "home_ck_intro": "Before you load a model from Hugging Face, see whether its files can run code and what its model card leaves out.",
        "home_ck_hint": "Free, runs in your browser, nothing is stored.",
    },
    "es": {
        "site_desc": "Referencia independiente sobre el envenenamiento de datos y modelos de IA: cómo se corrompe lo que aprenden, la investigación y cómo defenderse.",
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
        "start_intro": "Lo esencial, desde la definición básica hasta una lista práctica de defensas y ataques reales en los repositorios de modelos.",
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
        "glossary_desc": "Definiciones claras del envenenamiento de la IA: puerta trasera, disparador, split-view, LLM grooming, envenenamiento de memoria, ML-BOM y más.",
        "glossary_lead": "Definiciones de los términos que se usan en este sitio y en la investigación sobre envenenamiento de datos y modelos. Cada una enlaza al artículo donde más importa.",
        "footer_about": "Referencia independiente y sin ánimo comercial sobre el envenenamiento de datos y modelos de IA. Sin cookies ni rastreadores.",
        "footer_updated": "Última actualización: {d}",
        "notfound_title": "Página no encontrada",
        "notfound_body": "Esta dirección no corresponde a ninguna página del sitio. Puede que haya cambiado al reorganizar los artículos.",
        "notfound_cta": "Ir a la página de inicio",
        "pending": "[pendiente]",
        "nav_checker": "Comprobador",
        "nav_tools": "Herramientas",
        "home_src": "¿Un chatbot te ha dado sus fuentes?",
        "home_src_link": "Compáralas con redes de propaganda conocidas",
        "src_lists_h": "Las listas completas",
        "src_lists_intro": "Todos los dominios que ha publicado VIGINUM, tal como aparecen en sus archivos. Las direcciones se escriben con [.] para que no se puedan abrir sin querer.",
        "src_list_pk": "Portal Kombat (red Pravda): {n} dominios y subdominios",
        "src_list_rrn": "RRN (Doppelgänger): {n} dominios",
        "src_list_updated": "Última actualización de VIGINUM: {d}.",
        "src_noscript": "El comprobador de fuentes necesita JavaScript, pero puedes buscar en las listas completas de abajo con la función de búsqueda del navegador.",
        "tools_open": "Abrir",
        "tool_eyebrow": "Herramienta gratuita",
        "card_model_desc": "Mira si los archivos de un modelo pueden ejecutar código en tu equipo y qué no cuenta su ficha.",
        "card_src_desc": "Pega los enlaces que te ha dado un asistente de IA y comprueba si alguno es de una red de propaganda conocida.",
        "tool_box_label": "Pruébalo",
        "badge_new": "Nuevo",
        "badge_updated": "Actualizado",
        "rss": "Canal RSS",
        "tools_aria": "Herramientas",
        "ck_label": "Modelo de Hugging Face",
        "ck_hint": "Escribe propietario/modelo, pega un enlace de huggingface.co o un Package URL pkg:huggingface. Añade @revisión para comprobar un commit concreto.",
        "ck_try": "Prueba:",
        "ck_eicar_note": "un repositorio de prueba con archivos maliciosos a propósito",
        "ck_noscript": "El comprobador necesita JavaScript. Funciona en tu navegador y no envía nada a este sitio.",
        "home_ck_h": "Comprueba un modelo",
        "home_ck_intro": "Antes de cargar un modelo de Hugging Face, mira si sus archivos pueden ejecutar código y qué no cuenta su ficha.",
        "home_ck_hint": "Gratis, funciona en tu navegador y no guarda nada.",
    },
}

# Strings used by static/source-checker.js.
SOURCE_UI = {
    "en": {
        "check": "Check sources",
        "label": "Links or domain names",
        "hint": "Paste one per line, or a whole chatbot answer with its sources. Up to 200 domains.",
        "example_label": "Try an example",
        "err_empty": "Paste at least one link or domain name, for example `pravda-en.com`.",
        "err_data": "Could not load the lists from this site. Reload the page and try again.",
        "summary": "Sources on VIGINUM's lists: {n} of {total}",
        "not_listed": "Not on VIGINUM's lists. That does not make it reliable.",
        "list_pk": "Portal Kombat (Pravda network)",
        "list_rrn": "RRN (Doppelgänger)",
        "listed_exact": "Listed by VIGINUM.",
        "via_parent": "Its parent domain, {parent}, is listed by VIGINUM.",
        "registered": "Domain registered on {d}",
        "first_seen": "First seen on {d}",
        "desc_pk": "A pro-Russian network that republishes propaganda at scale, with little human readership, in a way that suits search engines and AI crawlers. [How it targets chatbots](@grooming).",
        "desc_rrn": "A pro-Russian campaign that created its own news sites and imitated real media outlets and government websites with look-alike domain names.",
        "caveat_hits": "A match means VIGINUM has linked the domain to the campaign, not that every article on it is false. Look for the claim in a source you trust.",
        "caveat_none": "These lists only cover domains VIGINUM has identified and published, and new ones keep appearing. Treat unfamiliar sites with generic news names with caution.",
        "updated": "Lists last updated by VIGINUM: Portal Kombat {pk}, RRN {rrn}. [Source](https://github.com/VIGINUM-FR/Rapports-Techniques).",
        "too_many": "Only the first {n} domains were checked.",
    },
    "es": {
        "check": "Comprobar fuentes",
        "label": "Enlaces o nombres de dominio",
        "hint": "Pega uno por línea o la respuesta completa de un chatbot con sus fuentes. Hasta 200 dominios.",
        "example_label": "Prueba con un ejemplo",
        "err_empty": "Pega al menos un enlace o un nombre de dominio, por ejemplo `pravda-en.com`.",
        "err_data": "No se han podido cargar las listas de este sitio. Recarga la página y vuelve a intentarlo.",
        "summary": "Fuentes en las listas de VIGINUM: {n} de {total}",
        "not_listed": "No está en las listas de VIGINUM. Eso no significa que sea fiable.",
        "list_pk": "Portal Kombat (red Pravda)",
        "list_rrn": "RRN (Doppelgänger)",
        "listed_exact": "Está en la lista de VIGINUM.",
        "via_parent": "Su dominio principal, {parent}, está en la lista de VIGINUM.",
        "registered": "Dominio registrado el {d}",
        "first_seen": "Detectado por primera vez el {d}",
        "desc_pk": "Una red prorrusa que republica propaganda a gran escala, con muy pocos lectores humanos, de una forma que encaja con los buscadores y los rastreadores de IA. [Cómo apunta a los chatbots](@grooming).",
        "desc_rrn": "Una campaña prorrusa que creó sus propias webs de noticias e imitó a medios reales y webs de gobiernos con dominios parecidos.",
        "caveat_hits": "Una coincidencia significa que VIGINUM ha vinculado el dominio con la campaña, no que todos sus artículos sean falsos. Busca esa afirmación en una fuente de confianza.",
        "caveat_none": "Estas listas solo incluyen los dominios que VIGINUM ha identificado y publicado, y siguen apareciendo otros nuevos. Desconfía de las webs desconocidas con nombre genérico de periódico.",
        "updated": "Última actualización de las listas por VIGINUM: Portal Kombat {pk}, RRN {rrn}. [Fuente](https://github.com/VIGINUM-FR/Rapports-Techniques).",
        "too_many": "Solo se han comprobado los primeros {n} dominios.",
    },
}

SOURCE_EXAMPLE = "reuters.com\nhttps://pravda-en.com/world/\nfr.news-pravda.com\nwikipedia.org"

# Strings used by static/checker.js. Links written as (@key#anchor) are resolved per language.
CHECKER_UI = {
    "en": {
        "check": "Check",
        "checking": "Checking…",
        "loading": "Asking Hugging Face about {id}…",
        "err_empty": "Enter a model, for example `openai-community/gpt2`.",
        "err_kind": "This tool checks models. Datasets and Spaces are not supported yet.",
        "err_format": "That does not look like a Hugging Face model. Use `owner/model`, a huggingface.co link or a `pkg:huggingface/…` Package URL.",
        "err_notfound": "Hugging Face did not return `{id}`. It may not exist or may be private, or the revision may be wrong.",
        "err_rate": "Hugging Face is limiting requests right now. Try again in a minute.",
        "err_server": "Hugging Face returned an unexpected answer. Try again later.",
        "err_timeout": "Hugging Face took too long to answer. Try again.",
        "err_network": "Could not reach Hugging Face. Check your connection, or whether a browser extension is blocking huggingface.co.",
        "and_more": "and {n} more",
        "results_for": "Results for",
        "updated": "Last updated {d}",
        "downloads": "{n} downloads in the last 30 days",
        "likes": "{n} likes",
        "summary_label": "Summary",
        "count_risk": "Risks",
        "count_check": "To check",
        "count_good": "Good",
        "status_risk": "Risk",
        "status_check": "Check",
        "status_note": "Note",
        "status_good": "Good",
        "disabled_t": "Hugging Face has disabled this repository",
        "disabled_b": "Its files are no longer available from Hugging Face. Treat any copy you find elsewhere with suspicion.",
        "gated_t": "Access is gated",
        "gated_b": "You have to accept the author's conditions on Hugging Face before you can download the files.",
        "scan_none_t": "No scan results yet",
        "scan_none_b": "Hugging Face has not finished scanning this repository, or did not report results. Check the files yourself before loading them.",
        "level_unsafe": "unsafe",
        "level_caution": "caution",
        "level_suspicious": "suspicious",
        "scan_unsafe_t": "Hugging Face's scanners flagged unsafe files",
        "scan_unsafe_b": "Do not load these files outside a sandbox without network access or credentials. Open each one on Hugging Face to see what the scanner found.",
        "scan_caution_t": "Hugging Face's scanners flagged files for caution",
        "scan_caution_b": "The scanner found imports or contents that are not known to be safe. Open each file on Hugging Face to see why before you load it.",
        "scan_clean_t": "Hugging Face's scanners found nothing",
        "scan_clean_b": "No file was flagged by the antivirus or the pickle import scan. Scanners catch known patterns, not every attack.",
        "fmt_pickle_only_t": "The weights are only in formats that can run code",
        "fmt_pickle_only_b": "Pickle-based files can execute code the moment they are loaded. Look for a version of the model in safetensors, or load these only in a sandbox without network access or credentials.",
        "fmt_both_t": "Safe and pickle-based weights are both published",
        "fmt_both_b": "The repository also has {kinds} files. Make sure your code loads those and never the pickle-based ones: in transformers, for example, pass `use_safetensors=True`.",
        "fmt_safe_t": "The weights are in formats that do not run code",
        "fmt_safe_b": "Found: {kinds}. Unlike pickle, these formats are designed to store weights without executable code. Keep the software that reads them up to date.",
        "fmt_none_t": "No model weight files recognised",
        "fmt_none_b": "The repository may store its weights elsewhere or use a format this tool does not know. Look at the files before loading them.",
        "fmt_keras_t": "Keras files can contain code",
        "fmt_keras_b": "Keras models can include layers that run code when loaded, and Keras's safe mode has been bypassed before. Use an up-to-date Keras with safe mode on, or load them in a sandbox.",
        "fmt_state_t": "Training files in pickle format",
        "fmt_state_b": "Files such as `training_args.bin` or `optimizer.pt` are saved with pickle. You do not need them to use the model, so do not load them.",
        "code_remote_t": "Loading it runs code from the repository",
        "code_remote_b": "This model needs `trust_remote_code=True`, which runs its Python files on your machine. Read them before loading and pin a revision so they cannot change later.",
        "code_files_t": "The repository includes Python files",
        "code_files_b": "Standard libraries do not run them when they load the model, but read them before you run any of them yourself.",
        "code_none_t": "No custom code needed",
        "code_none_b": "It loads without `trust_remote_code`, so no Python file from the repository runs on your machine.",
        "card_none_t": "No model card",
        "card_none_b": "Without a model card you cannot tell what the model is for, how it was trained or who answers for it.",
        "card_nometa_t": "The model card has no metadata",
        "card_nometa_b": "There is a README, but it does not declare a licence, training data or base model in a form tools can read.",
        "card_ok_t": "Has a model card",
        "card_ok_b": "Read it for the intended use, the limitations and how the model was evaluated.",
        "lic_none_t": "No licence declared",
        "lic_none_b": "Without a licence you have no clear right to use, modify or redistribute the model.",
        "lic_other_t": "Licence: {lic}",
        "lic_other_b": "It is not a standard licence. Read its terms in the model card or the licence file before using the model.",
        "lic_ok_t": "Licence: {lic}",
        "lic_ok_b": "Check that its terms fit the way you plan to use the model.",
        "data_ok_t": "Training data declared",
        "data_ok_b": "The model card names the data it was trained or fine-tuned on. Look at where that data came from and who maintains it.",
        "data_none_t": "Training data not declared",
        "data_none_b": "Knowing where the data came from is the first defence against [poisoning](@defend#1-know-where-your-data-comes-from). If the card does not say, ask the author or prefer a model that does.",
        "base_t": "Built on another model",
        "base_b": "Whatever is in the base model carries over, including a backdoor. Check it too:",
        "rel_finetune": "fine-tune",
        "rel_adapter": "adapter",
        "rel_quantized": "quantised",
        "rel_merge": "merge",
        "copy": "Copy",
        "copied": "Copied",
        "pin_t": "Pin this exact version",
        "pin_b": "This version is commit `{sha}`. Download that commit rather than whatever the repository holds tomorrow, so a later change cannot reach you.",
        "pin_code": "In Python",
        "pin_purl": "Package URL for your ML-BOM",
        "caveat": "These checks cover what the repository publishes, not what the model learned. A model can pass all of them and still contain a backdoor. [How to test for one](@defend#4-test-what-the-model-learned).",
    },
    "es": {
        "check": "Comprobar",
        "checking": "Comprobando…",
        "loading": "Consultando {id} en Hugging Face…",
        "err_empty": "Escribe un modelo, por ejemplo `openai-community/gpt2`.",
        "err_kind": "Esta herramienta comprueba modelos. Todavía no admite datasets ni Spaces.",
        "err_format": "Eso no parece un modelo de Hugging Face. Usa `propietario/modelo`, un enlace de huggingface.co o un Package URL `pkg:huggingface/…`.",
        "err_notfound": "Hugging Face no ha devuelto `{id}`. Puede que no exista o sea privado, o que la revisión no sea correcta.",
        "err_rate": "Hugging Face está limitando las consultas ahora mismo. Vuelve a intentarlo en un minuto.",
        "err_server": "Hugging Face ha devuelto una respuesta inesperada. Vuelve a intentarlo más tarde.",
        "err_timeout": "Hugging Face ha tardado demasiado en responder. Vuelve a intentarlo.",
        "err_network": "No se ha podido conectar con Hugging Face. Revisa tu conexión o si alguna extensión del navegador bloquea huggingface.co.",
        "and_more": "y {n} más",
        "results_for": "Resultados de",
        "updated": "Actualizado el {d}",
        "downloads": "{n} descargas en los últimos 30 días",
        "likes": "{n} me gusta",
        "summary_label": "Resumen",
        "count_risk": "Riesgos",
        "count_check": "Por revisar",
        "count_good": "Bien",
        "status_risk": "Riesgo",
        "status_check": "Revisar",
        "status_note": "Nota",
        "status_good": "Bien",
        "disabled_t": "Hugging Face ha desactivado este repositorio",
        "disabled_b": "Sus archivos ya no están disponibles en Hugging Face. Desconfía de cualquier copia que encuentres en otro sitio.",
        "gated_t": "El acceso está restringido",
        "gated_b": "Tienes que aceptar las condiciones del autor en Hugging Face antes de poder descargar los archivos.",
        "scan_none_t": "Todavía no hay resultados del análisis",
        "scan_none_b": "Hugging Face no ha terminado de analizar este repositorio o no ha publicado resultados. Revisa tú los archivos antes de cargarlos.",
        "level_unsafe": "inseguro",
        "level_caution": "precaución",
        "level_suspicious": "sospechoso",
        "scan_unsafe_t": "Los análisis de Hugging Face han marcado archivos inseguros",
        "scan_unsafe_b": "No cargues estos archivos fuera de un entorno aislado sin red ni credenciales. Abre cada uno en Hugging Face para ver qué ha encontrado el análisis.",
        "scan_caution_t": "Los análisis de Hugging Face han marcado archivos con precaución",
        "scan_caution_b": "El análisis ha encontrado importaciones o contenidos que no se sabe si son seguros. Abre cada archivo en Hugging Face para ver por qué antes de cargarlo.",
        "scan_clean_t": "Los análisis de Hugging Face no han encontrado nada",
        "scan_clean_b": "Ni el antivirus ni el análisis de importaciones pickle han marcado ningún archivo. Los análisis detectan patrones conocidos, no todos los ataques.",
        "fmt_pickle_only_t": "Los pesos solo están en formatos que pueden ejecutar código",
        "fmt_pickle_only_b": "Los archivos basados en pickle pueden ejecutar código en cuanto se cargan. Busca una versión del modelo en safetensors o cárgalos solo en un entorno aislado sin red ni credenciales.",
        "fmt_both_t": "Hay pesos en formato seguro y también basados en pickle",
        "fmt_both_b": "El repositorio también tiene archivos {kinds}. Asegúrate de que tu código carga esos y nunca los basados en pickle: en transformers, por ejemplo, con `use_safetensors=True`.",
        "fmt_safe_t": "Los pesos están en formatos que no ejecutan código",
        "fmt_safe_b": "Encontrados: {kinds}. A diferencia de pickle, estos formatos están pensados para guardar pesos sin código ejecutable. Mantén al día el software que los lee.",
        "fmt_none_t": "No se reconoce ningún archivo de pesos",
        "fmt_none_b": "Puede que el repositorio guarde los pesos en otro sitio o use un formato que esta herramienta no conoce. Revisa los archivos antes de cargarlos.",
        "fmt_keras_t": "Los archivos de Keras pueden contener código",
        "fmt_keras_b": "Los modelos de Keras pueden incluir capas que ejecutan código al cargarse, y su modo seguro ya se ha saltado alguna vez. Usa un Keras actualizado con el modo seguro activado o cárgalos en un entorno aislado.",
        "fmt_state_t": "Archivos de entrenamiento en formato pickle",
        "fmt_state_b": "Archivos como `training_args.bin` u `optimizer.pt` se guardan con pickle. No los necesitas para usar el modelo, así que no los cargues.",
        "code_remote_t": "Cargarlo ejecuta código del repositorio",
        "code_remote_b": "Este modelo necesita `trust_remote_code=True`, que ejecuta en tu equipo sus archivos Python. Léelos antes de cargarlo y fija una revisión para que no puedan cambiar después.",
        "code_files_t": "El repositorio incluye archivos Python",
        "code_files_b": "Las bibliotecas habituales no los ejecutan al cargar el modelo, pero léelos antes de ejecutar tú cualquiera de ellos.",
        "code_none_t": "No necesita código propio",
        "code_none_b": "Se carga sin `trust_remote_code`, así que ningún archivo Python del repositorio se ejecuta en tu equipo.",
        "card_none_t": "No tiene ficha del modelo",
        "card_none_b": "Sin ficha no puedes saber para qué sirve el modelo, cómo se entrenó ni quién responde de él.",
        "card_nometa_t": "La ficha del modelo no tiene metadatos",
        "card_nometa_b": "Hay un README, pero no declara la licencia, los datos de entrenamiento ni el modelo base de forma que puedan leerlo las herramientas.",
        "card_ok_t": "Tiene ficha del modelo",
        "card_ok_b": "Léela para conocer el uso previsto, las limitaciones y cómo se evaluó el modelo.",
        "lic_none_t": "No declara licencia",
        "lic_none_b": "Sin licencia no tienes un derecho claro a usar, modificar o redistribuir el modelo.",
        "lic_other_t": "Licencia: {lic}",
        "lic_other_b": "No es una licencia estándar. Lee sus condiciones en la ficha o en el archivo de licencia antes de usar el modelo.",
        "lic_ok_t": "Licencia: {lic}",
        "lic_ok_b": "Comprueba que sus condiciones encajan con el uso que vas a darle.",
        "data_ok_t": "Declara los datos de entrenamiento",
        "data_ok_b": "La ficha indica con qué datos se entrenó o ajustó. Mira de dónde vienen esos datos y quién los mantiene.",
        "data_none_t": "No declara los datos de entrenamiento",
        "data_none_b": "Saber de dónde vienen los datos es la primera defensa contra el [envenenamiento](@defend#1-saber-de-donde-vienen-los-datos). Si la ficha no lo dice, pregunta al autor o elige un modelo que lo diga.",
        "base_t": "Parte de otro modelo",
        "base_b": "Lo que tenga el modelo base se hereda, incluida una puerta trasera. Compruébalo también:",
        "rel_finetune": "ajuste fino",
        "rel_adapter": "adaptador",
        "rel_quantized": "cuantizado",
        "rel_merge": "fusión",
        "copy": "Copiar",
        "copied": "Copiado",
        "pin_t": "Fija esta versión exacta",
        "pin_b": "Esta versión es el commit `{sha}`. Descarga ese commit y no lo que haya mañana en el repositorio, para que un cambio posterior no te afecte.",
        "pin_code": "En Python",
        "pin_purl": "Package URL para tu ML-BOM",
        "caveat": "Estas comprobaciones cubren lo que publica el repositorio, no lo que ha aprendido el modelo. Un modelo puede superarlas todas y aun así tener una puerta trasera. [Cómo detectarla](@defend#4-comprobar-que-ha-aprendido-el-modelo).",
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

tools: dict[str, dict[str, dict]] = {lang: {} for lang in LANGS}
for p in sorted((CONTENT / "tools").glob("*.md")):
    lang = p.stem.split(".")[-1]
    tl = parse_md(p)
    tl["lang"] = lang
    tools[lang][tl["key"]] = tl

timeline = json.loads((CONTENT / "timeline.json").read_text(encoding="utf-8"))

BUILD_DATE = dt.date.today()
BADGE_DAYS = 14


def _content_dates() -> list[str]:
    out = [CFG.get("updated", "")]
    for coll in (articles, tools):
        for lang in LANGS:
            for x in coll[lang].values():
                out += [x.get("date", ""), x.get("updated", "")]
    return [d for d in out if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d or "")]


SITE_UPDATED = max(_content_dates())
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
    if key in tools[lang]:
        return prefix + tools[lang][key]["slug"] + "/"
    sys.exit(f"Unknown link key @{key} ({lang})")


LINK_RE = re.compile(r"\]\(@([a-z0-9-]+)(#[a-z0-9-]+)?\)")


def resolve_links(text: str, lang: str) -> str:
    """Turns [text](@key#anchor) into [text](/real/url/#anchor) for the given language."""
    return LINK_RE.sub(lambda m: f"]({url_for(m.group(1), lang)}{m.group(2) or ''})", text)


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
    text = resolve_links(text, lang)
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
    figs = re.findall(r"^:::figure ([a-z0-9-]+)[ \t]*$", body, re.M)
    body = re.sub(r"^:::figure ([a-z0-9-]+)[ \t]*$", lambda m: f"\n<!--FIG:{m.group(1)}-->\n", body, flags=re.M)
    body_html = md_to_html(body, lang)
    for key in figs:
        html_fig = figure(key, lang)
        body_html = body_html.replace(f"<p><!--FIG:{key}--></p>", html_fig).replace(f"<!--FIG:{key}-->", html_fig)
    if a.get("tool"):
        body_html += tool_box(a["tool"], lang)
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
DOT_COLS_M, DOT_ROWS_M = 48, 24      # narrow layout, same total
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
<link rel="alternate" type="application/atom+xml" title="modelpoisoning.com" href="{'/feed.xml' if lang == 'en' else '/es/feed.xml'}">
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
        {nav_link(url_for('tools', lang), t['nav_tools'], 'tools')}
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
      <p class="muted">{t['footer_updated'].format(d=fmt_date(SITE_UPDATED, lang))}</p>
    </div>
    <ul class="footer-links">
      <li><a href="{url_for('about', lang)}">{pages[lang]['about']['nav_title']}</a></li>
      <li><a href="{url_for('legal', lang)}">{pages[lang]['legal']['nav_title']}</a></li>
      <li><a href="{url_for('privacy', lang)}">{pages[lang]['privacy']['nav_title']}</a></li>
      <li><a href="{'/feed.xml' if lang == 'en' else '/es/feed.xml'}" type="application/atom+xml">{t['rss']}</a></li>
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


def freshness_badge(a: dict, lang: str) -> str:
    """'New' or 'Updated' next to articles published or revised in the last few weeks."""
    t = T[lang]

    def recent(d: str) -> bool:
        try:
            return 0 <= (BUILD_DATE - dt.date.fromisoformat(d)).days <= BADGE_DAYS
        except (TypeError, ValueError):
            return False

    if recent(a.get("date", "")):
        return f' <span class="fresh">{t["badge_new"]}</span>'
    if a.get("updated") and recent(a["updated"]):
        return f' <span class="fresh">{t["badge_updated"]}</span>'
    return ""


def tool_cards(lang: str) -> str:
    t = T[lang]
    if "checker" not in tools[lang] or "source-checker" not in tools[lang]:
        return ""
    mc, sc = tools[lang]["checker"], tools[lang]["source-checker"]
    return f"""<section class="wrap tool-cards" aria-label="{t['tools_aria']}">
    <div class="tool-card">
      <p class="eyebrow">{t['tool_eyebrow']}</p>
      <h2><a href="{url_for('checker', lang)}">{esc(mc['h1'])}</a></h2>
      <p>{t['card_model_desc']}</p>
      {checker_form(lang, "home-model", t['home_ck_hint'])}
    </div>
    <div class="tool-card">
      <p class="eyebrow">{t['tool_eyebrow']}</p>
      <h2><a href="{url_for('source-checker', lang)}">{esc(sc['h1'])}</a></h2>
      <p>{t['card_src_desc']}</p>
      <p class="card-action"><a class="btn" href="{url_for('source-checker', lang)}">{SOURCE_UI[lang]['check']}</a></p>
    </div>
  </section>"""


def tool_box(key: str, lang: str) -> str:
    """Call to action at the end of an article that relates to one of the tools."""
    t = T[lang]
    if key not in tools[lang]:
        return ""
    x = tools[lang][key]
    if key == "checker":
        action = checker_form(lang, "article-model", t["home_ck_hint"])
    else:
        action = f'<p class="card-action"><a class="btn" href="{url_for(key, lang)}">{SOURCE_UI[lang]["check"]}</a></p>'
    return (f'<aside class="tool-box" aria-label="{t["tool_box_label"]}">'
            f'<p class="eyebrow">{t["tool_box_label"]}</p>'
            f'<p class="tool-box-title"><a href="{url_for(key, lang)}">{esc(x["h1"])}</a></p>'
            f'<p>{esc(x["lead"])}</p>{action}</aside>')


def build_feed(lang: str) -> None:
    """Atom feed of the articles, newest first."""
    from xml.sax.saxutils import escape as xesc
    items = sorted(articles[lang].values(), key=lambda a: a.get("updated", a["date"]), reverse=True)
    home = SITE_URL + url_for("home", lang)
    feed_url = SITE_URL + ("/feed.xml" if lang == "en" else "/es/feed.xml")
    entries = []
    for a in items:
        link = SITE_URL + url_for(a["key"], lang)
        entries.append(
            "<entry>"
            f"<title>{xesc(a['title'])}</title>"
            f'<link href="{link}"/><id>{link}</id>'
            f"<published>{a['date']}T00:00:00Z</published>"
            f"<updated>{a.get('updated', a['date'])}T00:00:00Z</updated>"
            f"<summary>{xesc(a['description'])}</summary>"
            "</entry>")
    xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
           f'<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="{lang}">'
           f"<title>modelpoisoning.com</title><subtitle>{xesc(T[lang]['site_desc'])}</subtitle>"
           f'<link href="{home}"/><link rel="self" href="{feed_url}"/><id>{home}</id>'
           f"<updated>{SITE_UPDATED}T00:00:00Z</updated>"
           f"<author><name>{xesc(CFG['editor_name'])}</name></author>"
           + "".join(entries) + "</feed>\n")
    path = OUT / ("feed.xml" if lang == "en" else "es/feed.xml")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(xml, encoding="utf-8")


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
            f'<span class="row-title">{esc(a["nav_title"])}{freshness_badge(a, lang)}</span>'
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
             else "Model Poisoning: el envenenamiento de datos y modelos de IA")
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
  {tool_cards(lang)}
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
    meta = t["published"].format(d=fmt_date(a["date"], lang))
    if a.get("updated") and a["updated"] != a["date"]:
        meta += " · " + t["updated"].format(d=fmt_date(a["updated"], lang))
    meta += ", " + t["min_read"].format(n=mins)
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


CHECKER_EXAMPLES = ["openai-community/gpt2", "mcpotato/42-eicar-street"]


def checker_form(lang: str, input_id: str, hint: str, examples: bool = False) -> str:
    """The model checker form. Without JavaScript it still submits ?model= to the checker page."""
    t = T[lang]
    ex = ""
    if examples:
        chips = "".join(
            f'<button type="button" class="chip" data-example="{esc(e)}">{esc(e)}</button>'
            for e in CHECKER_EXAMPLES
        )
        ex = (f'<p class="examples"><span class="examples-label">{t["ck_try"]}</span> {chips} '
              f'<span class="muted">({t["ck_eicar_note"]}: {esc(CHECKER_EXAMPLES[1])})</span></p>')
    return f"""<form class="checker-form" action="{url_for('checker', lang)}" method="get" role="search">
      <label for="{input_id}">{t['ck_label']}</label>
      <div class="field-row">
        <input id="{input_id}" name="model" type="text" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="owner/model" aria-describedby="{input_id}-hint" maxlength="300">
        <button type="submit" class="btn">{CHECKER_UI[lang]['check']}</button>
      </div>
      <p id="{input_id}-hint" class="hint">{hint}</p>
      {ex}
    </form>"""


def build_checker(lang: str) -> None:
    t = T[lang]
    tl = tools[lang]["checker"]
    url = url_for("checker", lang)
    alts = {l: url_for("checker", l) for l in LANGS if "checker" in tools[l]}
    other = alts.get("es" if lang == "en" else "en")
    ui = {k: resolve_links(v, lang) for k, v in CHECKER_UI[lang].items()}
    ui_json = json.dumps(ui, ensure_ascii=False).replace("</", "<\\/")
    jsonld = [
        {
            "@context": "https://schema.org", "@type": "WebApplication",
            "name": tl["nav_title"] if lang == "en" else tl["h1"], "url": SITE_URL + url,
            "description": tl["description"], "inLanguage": lang,
            "applicationCategory": "SecurityApplication", "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            "publisher": {"@type": "Organization", "name": "modelpoisoning.com", "url": SITE_URL + "/"},
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t["breadcrumb_home"], "item": SITE_URL + url_for("home", lang)},
                {"@type": "ListItem", "position": 2, "name": tl["nav_title"], "item": SITE_URL + url},
            ],
        },
    ]
    doc = head(lang=lang, title=tl["title"], desc=tl["description"], url=url, alt_urls=alts, jsonld=jsonld)
    doc += header(lang, other, current="tools")
    doc += f"""
<main id="main" class="wrap page checker-page">
  <h1>{esc(tl['h1'])}</h1>
  <p class="lead">{esc(tl['lead'])}</p>
  <div id="checker" class="checker">
    {checker_form(lang, "model-input", t['ck_hint'], examples=True)}
    <noscript><p class="msg msg-error">{t['ck_noscript']}</p></noscript>
    <div id="checker-results" class="results" aria-live="polite"></div>
  </div>
  <div class="prose checker-about">{md_to_html(tl['body'], lang)}</div>
</main>
<script type="application/json" id="checker-i18n">{ui_json}</script>
<script src="/checker.js?v={JS_VERSION}" defer></script>
"""
    doc += footer(lang, other)
    write(url, doc)


# --------------------------------------------------------------------------
# Source checker (VIGINUM lists)
# --------------------------------------------------------------------------
VIGINUM_DIR = CONTENT / "data" / "viginum"


def _dmy_to_iso(value: str) -> str:
    value = (value or "").strip()
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", value)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


def load_viginum() -> dict:
    """Reads VIGINUM's CSV files unchanged and returns normalised rows per list."""
    import csv
    meta = json.loads((VIGINUM_DIR / "data.json").read_text(encoding="utf-8"))
    rows: dict[str, list] = {}
    for key, info in meta["lists"].items():
        out = []
        with open(VIGINUM_DIR / info["file"], encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                raw = r.get(info["domain_col"], "").strip()
                dom = raw.lower().replace("[.]", ".").rstrip(".")
                if not dom:
                    continue
                created = _dmy_to_iso(r.get("create date") or r.get("created on") or "")
                seen = _dmy_to_iso(r.get("first seen") or "")
                kind, date = ("registered", created) if created else (("seen", seen) if seen else ("", ""))
                out.append({"domain": dom, "type": (r.get("type") or "domain").strip(),
                            "kind": kind, "date": date})
        rows[key] = sorted({d["domain"]: d for d in out}.values(), key=lambda d: d["domain"])
    return {"meta": meta, "rows": rows}


VIGINUM: dict = {}


def write_known_domains() -> None:
    global VIGINUM
    VIGINUM = load_viginum()
    domains = []
    for key, rows in VIGINUM["rows"].items():
        for d in rows:
            domains.append([d["domain"], key, d["type"], d["kind"], d["date"]])
    payload = {
        "source": VIGINUM["meta"]["repo"],
        "lists": {k: {"updated": v["updated"], "url": v["url"], "count": len(VIGINUM["rows"][k])}
                  for k, v in VIGINUM["meta"]["lists"].items()},
        "domains": domains,
    }
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    (OUT / "data" / "known-domains.json").write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def build_source_checker(lang: str) -> None:
    t = T[lang]
    tl = tools[lang]["source-checker"]
    url = url_for("source-checker", lang)
    alts = {l: url_for("source-checker", l) for l in LANGS if "source-checker" in tools[l]}
    other = alts.get("es" if lang == "en" else "en")
    ui = {k: resolve_links(v, lang) for k, v in SOURCE_UI[lang].items()}
    ui_json = json.dumps(ui, ensure_ascii=False).replace("</", "<\\/")
    example = SOURCE_EXAMPLE.replace("\\n", "\n")
    lists_html = []
    for key in ("pk", "rrn"):
        rows = VIGINUM["rows"][key]
        meta = VIGINUM["meta"]["lists"][key]
        items = "".join(f"<li>{esc(d['domain'].replace('.', '[.]'))}</li>" for d in rows)
        lists_html.append(
            f'<details class="domain-list"><summary>{esc(t["src_list_" + key].format(n=len(rows)))}</summary>'
            f'<p class="muted">{t["src_list_updated"].format(d=fmt_date(meta["updated"], lang))} '
            f'<a href="{esc(meta["url"])}" rel="noopener">VIGINUM</a></p>'
            f'<ul class="domains">{items}</ul></details>')
    jsonld = [
        {
            "@context": "https://schema.org", "@type": "WebApplication",
            "name": tl["nav_title"], "url": SITE_URL + url,
            "description": tl["description"], "inLanguage": lang,
            "applicationCategory": "SecurityApplication", "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            "publisher": {"@type": "Organization", "name": "modelpoisoning.com", "url": SITE_URL + "/"},
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t["breadcrumb_home"], "item": SITE_URL + url_for("home", lang)},
                {"@type": "ListItem", "position": 2, "name": tools[lang]["tools"]["nav_title"], "item": SITE_URL + url_for("tools", lang)},
                {"@type": "ListItem", "position": 3, "name": tl["nav_title"], "item": SITE_URL + url},
            ],
        },
    ]
    doc = head(lang=lang, title=tl["title"], desc=tl["description"], url=url, alt_urls=alts, jsonld=jsonld)
    doc += header(lang, other, current="tools")
    doc += f"""
<main id="main" class="wrap page checker-page">
  <h1>{esc(tl['h1'])}</h1>
  <p class="lead">{esc(tl['lead'])}</p>
  <div id="source-checker" class="checker" data-src="/data/known-domains.json?v={VIGINUM_VERSION()}">
    <form class="checker-form source-form" action="{url}" method="get">
      <label for="sources-input">{ui['label']}</label>
      <textarea id="sources-input" name="sources" rows="5" autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="sources-hint" placeholder="pravda-en.com&#10;https://example.com/article"></textarea>
      <p id="sources-hint" class="hint">{ui['hint']}</p>
      <p class="actions-row">
        <button type="submit" class="btn">{ui['check']}</button>
        <button type="button" class="chip" data-example="{esc(example)}">{ui['example_label']}</button>
      </p>
    </form>
    <noscript><p class="msg">{t['src_noscript']}</p></noscript>
    <div id="source-results" class="results" aria-live="polite"></div>
  </div>
  <div class="prose checker-about">{md_to_html(tl['body'], lang)}</div>
  <section class="lists" aria-labelledby="lists-h">
    <h2 id="lists-h">{t['src_lists_h']}</h2>
    <p class="muted">{t['src_lists_intro']}</p>
    {''.join(lists_html)}
  </section>
</main>
<script type="application/json" id="source-checker-i18n">{ui_json}</script>
<script src="/source-checker.js?v={SRC_JS_VERSION}" defer></script>
"""
    doc += footer(lang, other)
    write(url, doc)


def VIGINUM_VERSION() -> str:
    import hashlib
    return hashlib.sha1((OUT / "data" / "known-domains.json").read_bytes()).hexdigest()[:8]


def build_tools_index(lang: str) -> None:
    t = T[lang]
    tl = tools[lang]["tools"]
    url = url_for("tools", lang)
    alts = {l: url_for("tools", l) for l in LANGS if "tools" in tools[l]}
    other = alts.get("es" if lang == "en" else "en")
    rows = []
    for key in ("checker", "source-checker"):
        if key not in tools[lang]:
            continue
        x = tools[lang][key]
        rows.append(f'<li><a href="{url_for(key, lang)}"><span class="row-title">{esc(x["h1"])}</span>'
                    f'<span class="row-dek">{esc(x["lead"])}</span>'
                    f'<span class="row-meta">{t["tools_open"]}</span></a></li>')
    jsonld = [{
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": tl["title"], "url": SITE_URL + url, "inLanguage": lang, "description": tl["description"],
    }]
    doc = head(lang=lang, title=tl["title"], desc=tl["description"], url=url, alt_urls=alts, jsonld=jsonld)
    doc += header(lang, other, current="tools")
    doc += f"""
<main id="main" class="wrap page">
  <h1>{esc(tl['h1'])}</h1>
  <p class="lead">{esc(tl['lead'])}</p>
  <ul class="rows tools-rows">{''.join(rows)}</ul>
</main>
"""
    doc += footer(lang, other)
    write(url, doc)


# Old addresses from the previous site that still get impressions in Google.
# GitHub Pages has no 301 redirects: an instant meta refresh plus canonical is treated as a permanent redirect.
REDIRECTS = {
    "/aviso-legal/": ("legal", "es"),
    "/politica-de-privacidad/": ("privacy", "es"),
    "/quienes-somos/": ("about", "es"),
    "/contact/": ("about", "en"),
}


def build_redirects() -> None:
    for old, (key, lang) in REDIRECTS.items():
        target = url_for(key, lang)
        if old == target:
            continue
        full = SITE_URL + target
        doc = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
               f'<title>{esc(full)}</title><link rel="canonical" href="{full}">'
               f'<meta http-equiv="refresh" content="0; url={target}"></head>'
               f'<body><p><a href="{target}">{esc(full)}</a></p></body></html>\n')
        p = out_path(old)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(doc, encoding="utf-8")


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

    add({l: url_for("home", l) for l in LANGS}, SITE_UPDATED)
    add({l: url_for("glossary", l) for l in LANGS}, CFG["updated"])
    for key, a in articles["en"].items():
        add({l: url_for(key, l) for l in LANGS if key in articles[l]}, a.get("updated", a["date"]))
    for key, tl in tools["en"].items():
        add({l: url_for(key, l) for l in LANGS if key in tools[l]}, tl.get("updated", tl.get("date", CFG["updated"])))
    add({l: url_for("about", l) for l in LANGS}, CFG["updated"])
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(entries) + "\n</urlset>\n")
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
                                    encoding="utf-8")


# --------------------------------------------------------------------------
def main() -> None:
    global CSS_VERSION, JS_VERSION, SRC_JS_VERSION
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    import hashlib
    CSS_VERSION = hashlib.sha1((STATIC / "style.css").read_bytes()).hexdigest()[:8]
    JS_VERSION = hashlib.sha1((STATIC / "checker.js").read_bytes()).hexdigest()[:8]
    SRC_JS_VERSION = hashlib.sha1((STATIC / "source-checker.js").read_bytes()).hexdigest()[:8]
    write_known_domains()

    for lang in LANGS:
        build_home(lang)
        build_glossary(lang)
        if "checker" in tools[lang]:
            build_checker(lang)
        if "source-checker" in tools[lang]:
            build_source_checker(lang)
        if "tools" in tools[lang]:
            build_tools_index(lang)
        build_feed(lang)
        for a in articles[lang].values():
            build_article(a)
        for pg in pages[lang].values():
            build_page(pg)
    build_404()
    build_redirects()
    build_sitemap()

    n = len(list(OUT.rglob("index.html")))
    print(f"Built {n} pages into {OUT.relative_to(ROOT)}/")
    if missing_fields:
        print("WARNING: fill these fields in site.json before publishing: "
              + ", ".join(sorted(missing_fields)))


CSS_VERSION = "dev"
JS_VERSION = "dev"
SRC_JS_VERSION = "dev"

if __name__ == "__main__":
    main()
