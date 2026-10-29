"""Diagrams for articles, written as plain HTML so they reflow on small screens, follow the
light/dark theme and stay readable by search engines and screen readers.

Use in an article (on a line of its own):   :::figure grooming-routes
Styles live in static/style.css under "Figures".
"""
from __future__ import annotations

import html


def _e(s: str) -> str:
    return html.escape(s, quote=True)


def _flow(steps: list[str], cls: str = "") -> str:
    items = "".join(f'<li class="step">{_e(s)}</li>' for s in steps)
    return f'<ol class="flow {cls}">{items}</ol>'


# --------------------------------------------------------------------------
# 1. LLM grooming: two routes into a chatbot's answer
# --------------------------------------------------------------------------
_GROOMING = {
    "en": {
        "source": "Pravda network: millions of automated articles, barely read by people",
        "r1": "Route 1: training data",
        "r1s": ["Web scrapers collect the text", "It ends up in a training dataset", "The model learns the claim"],
        "r2": "Route 2: live search",
        "r2s": ["Search engines index the pages", "The assistant searches while answering", "It summarises them as a source"],
        "end": "The chatbot repeats the narrative",
        "cap": "LLM grooming can reach a chatbot through what it learned during training and through what it finds when it searches the web.",
    },
    "es": {
        "source": "Red Pravda: millones de artículos automáticos que casi nadie lee",
        "r1": "Vía 1: datos de entrenamiento",
        "r1s": ["Los rastreadores recogen el texto", "Acaba en un dataset de entrenamiento", "El modelo aprende la afirmación"],
        "r2": "Vía 2: búsqueda en directo",
        "r2s": ["Los buscadores indexan las páginas", "El asistente busca mientras responde", "Las resume como si fueran una fuente"],
        "end": "El chatbot repite el mensaje",
        "cap": "El LLM grooming puede llegar a un chatbot por lo que aprendió al entrenarse y por lo que encuentra cuando busca en la web.",
    },
}


def _grooming(lang: str) -> str:
    t = _GROOMING[lang]
    return (
        f'<figure class="fig fig-routes">'
        f'<div class="node node-accent">{_e(t["source"])}</div>'
        f'<div class="lanes">'
        f'<div class="lane"><p class="lane-label">{_e(t["r1"])}</p>{_flow(t["r1s"])}</div>'
        f'<div class="lane"><p class="lane-label">{_e(t["r2"])}</p>{_flow(t["r2s"])}</div>'
        f'</div>'
        f'<div class="node node-end">{_e(t["end"])}</div>'
        f'<figcaption>{_e(t["cap"])}</figcaption></figure>'
    )


# --------------------------------------------------------------------------
# 2. Loading a pickle versus loading safetensors
# --------------------------------------------------------------------------
_PICKLE = {
    "en": {
        "p": "Pickle-based file (.bin, .pt, .ckpt)",
        "ps": ["You call torch.load() or pickle.load()", "Python follows the file's instructions in order",
               "One instruction says: run this command", "The command runs on your machine, before any output"],
        "s": "Safetensors file",
        "ss": ["You call safe_open() or load_file()", "The library reads a header and the raw numbers",
               "There are no instructions to follow", "You get the weights and nothing else"],
        "cap": "Why the file format matters: a pickle is a small program that Python runs to rebuild the model; safetensors is only data.",
    },
    "es": {
        "p": "Archivo basado en pickle (.bin, .pt, .ckpt)",
        "ps": ["Llamas a torch.load() o pickle.load()", "Python sigue en orden las instrucciones del archivo",
               "Una instrucción dice: ejecuta este comando", "El comando se ejecuta en tu equipo, antes de ver nada"],
        "s": "Archivo safetensors",
        "ss": ["Llamas a safe_open() o load_file()", "La biblioteca lee una cabecera y los números",
               "No hay instrucciones que seguir", "Obtienes los pesos y nada más"],
        "cap": "Por qué importa el formato: un pickle es un pequeño programa que Python ejecuta para reconstruir el modelo; safetensors son solo datos.",
    },
}


def _pickle(lang: str) -> str:
    t = _PICKLE[lang]
    return (
        f'<figure class="fig fig-compare">'
        f'<div class="lane lane-risk"><p class="lane-label">{_e(t["p"])}</p>{_flow(t["ps"], "flow-risk")}</div>'
        f'<div class="lane lane-ok"><p class="lane-label">{_e(t["s"])}</p>{_flow(t["ss"], "flow-ok")}</div>'
        f'<figcaption>{_e(t["cap"])}</figcaption></figure>'
    )


# --------------------------------------------------------------------------
# 3. 250 documents: training data grew, the poison needed did not
#    Data from Souly et al. (arXiv 2510.07192): Chinchilla-optimal training,
#    about 20 tokens per parameter; 250 documents ~ 420,000 tokens.
# --------------------------------------------------------------------------
_MODELS = [("600M", 12), ("2B", 40), ("7B", 140), ("13B", 260)]  # billions of training tokens
_DOCS = {
    "en": {
        "title": "Training tokens per model and poisoned documents needed",
        "model": "Model", "tokens": "Training tokens", "poison": "Poisoned documents",
        "unit": "{n}B tokens", "docs": "250",
        "cap": "Training data grew more than twentyfold from the smallest model to the largest. The number of poisoned documents needed to plant the backdoor stayed at about 250. Approximate token counts (about 20 tokens per parameter).",
    },
    "es": {
        "title": "Tokens de entrenamiento por modelo y documentos envenenados necesarios",
        "model": "Modelo", "tokens": "Tokens de entrenamiento", "poison": "Documentos envenenados",
        "unit": "{n}.000 M de tokens", "docs": "250",
        "cap": "Los datos de entrenamiento se multiplicaron por más de veinte del modelo más pequeño al más grande. Los documentos envenenados necesarios para plantar la puerta trasera siguieron siendo unos 250. Cifras de tokens aproximadas (unos 20 tokens por parámetro).",
    },
}


def _docs(lang: str) -> str:
    t = _DOCS[lang]
    top = max(v for _, v in _MODELS)
    rows = []
    for name, tokens in _MODELS:
        pct = tokens / top * 100
        label = t["unit"].format(n=tokens)
        rows.append(
            f'<tr><th scope="row">{name}</th>'
            f'<td class="bar-cell"><span class="bar" style="--w:{pct:.1f}%"></span>'
            f'<span class="bar-label">{_e(label)}</span></td>'
            f'<td class="dose"><span class="dose-dot" aria-hidden="true"></span>{t["docs"]}</td></tr>'
        )
    return (
        f'<figure class="fig fig-bars">'
        f'<table><caption>{_e(t["title"])}</caption>'
        f'<thead><tr><th scope="col">{_e(t["model"])}</th><th scope="col">{_e(t["tokens"])}</th>'
        f'<th scope="col">{_e(t["poison"])}</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
        f'<figcaption>{_e(t["cap"])}</figcaption></figure>'
    )


# --------------------------------------------------------------------------
# 4. Glaze or Nightshade
# --------------------------------------------------------------------------
_GN = {
    "en": {
        "rows": [("What it does", "Protects one artist's style from imitation",
                  "Makes training on shaded images less useful for any model that uses them"),
                 ("What a model learns", "A different style from the artist's",
                  "The wrong concept: a cow starts to look like a handbag"),
                 ("Who it works for", "The artist who applies it",
                  "Artists as a group: it needs many shaded images in the training data"),
                 ("Recommended use", "On every published work", "As an optional extra on top of Glaze")],
        "cap": "Both tools add changes that are hard for people to see. Based on the University of Chicago project pages.",
    },
    "es": {
        "rows": [("Qué hace", "Protege el estilo de un artista frente a la imitación",
                  "Hace que entrenar con imágenes tratadas sea menos útil para cualquier modelo que las use"),
                 ("Qué aprende el modelo", "Un estilo distinto del del artista",
                  "El concepto equivocado: una vaca empieza a parecer un bolso"),
                 ("A quién sirve", "Al artista que la aplica",
                  "A los artistas en grupo: necesita muchas imágenes tratadas en los datos de entrenamiento"),
                 ("Uso recomendado", "En todas las obras que se publican", "Como complemento opcional además de Glaze")],
        "cap": "Las dos herramientas añaden cambios difíciles de ver para una persona. Según las páginas del proyecto de la Universidad de Chicago.",
    },
}


def _glaze_nightshade(lang: str) -> str:
    t = _GN[lang]
    rows = "".join(
        f'<tr><th scope="row">{_e(k)}</th><td>{_e(g)}</td><td>{_e(n)}</td></tr>' for k, g, n in t["rows"]
    )
    return (
        f'<figure class="fig fig-table">'
        f'<table><thead><tr><th scope="col"><span class="visually-hidden">—</span></th>'
        f'<th scope="col">Glaze</th><th scope="col">Nightshade</th></tr></thead>'
        f'<tbody>{rows}</tbody></table>'
        f'<figcaption>{_e(t["cap"])}</figcaption></figure>'
    )


FIGURES = {
    "grooming-routes": _grooming,
    "pickle-vs-safetensors": _pickle,
    "poison-constant": _docs,
    "glaze-vs-nightshade": _glaze_nightshade,
}


def figure(key: str, lang: str) -> str:
    if key not in FIGURES:
        raise SystemExit(f"Unknown figure '{key}'")
    return FIGURES[key](lang)
