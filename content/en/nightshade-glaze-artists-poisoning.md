---
key: nightshade
title: Nightshade and Glaze: when artists poison their own images
nav_title: Nightshade and Glaze
description: How the University of Chicago's Nightshade and Glaze tools let artists alter their images so AI models trained on them without consent learn the wrong things, and what their limits are.
dek: Not all data poisoning is an attack. For some artists it is the only leverage they have over companies that scrape their work.
date: 2026-10-09
order: 4
---

:::summary
- **Glaze** and **Nightshade** are free tools from the SAND Lab at the University of Chicago that make small, hard-to-see changes to images.
- **Glaze** is defensive: it makes it harder for a model to imitate an individual artist's style.
- **Nightshade** is offensive: images "shaded" with it teach a model trained on them the wrong associations, for example that a picture of a cow is a handbag.
- The research paper reports that a Stable Diffusion SDXL prompt could be corrupted with **fewer than 100 poison samples**. The team says the protection will not last forever as defences evolve.
:::

## Poisoning as self-defence

Text-to-image models such as Stable Diffusion, Midjourney or DALL·E were trained on billions of images collected from the web, including the work of living artists who were never asked. Opt-out mechanisms exist, but they depend on scrapers choosing to respect them.

A research group led by Professor **Ben Y. Zhao** at the University of Chicago built two tools that change the economics of that situation. Rather than asking for permission, they make unlicensed training less useful.

## Glaze: protecting a style

Glaze, released in 2023, is meant to be applied to every image an artist publishes. It adds a perturbation that is subtle to the human eye but shifts how a model perceives the image's style. If someone fine-tunes a model on glazed work to mimic that artist, the output drifts towards a different style. Glaze protects one artist at a time.

## Nightshade: a collective deterrent

Nightshade, which the team released in January 2024 and which was downloaded about 250,000 times shortly after release according to [ETCentric](https://www.etcentric.org/ai-poison-pill-app-nightshade-has-250k-downloads-in-5-days/), works differently. Its [project page](https://nightshade.cs.uchicago.edu/whatis.html) describes it as "an offensive tool that artists can use as a group".

A "shaded" image still looks like the original to a person. To a model, it carries features of a different concept. The team's example is an image of a cow in a field that, once shaded, nudges a model towards producing a leather handbag. Train a model on enough shaded images and its idea of "cow" starts to break.

The technical paper, [Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Generative Models](https://arxiv.org/abs/2310.13828) by Shawn Shan, Wenxin Ding, Josephine Passananti, Haitao Zheng and Ben Y. Zhao, was presented at the IEEE Symposium on Security and Privacy in May 2024. Its abstract makes several claims that matter beyond art:

- A Stable Diffusion SDXL prompt can be corrupted with **fewer than 100 poison samples**.
- The effects **bleed through** to related concepts, so poisoning one idea also affects its neighbours.
- **Multiple attacks** can be combined, and a moderate number of them can destabilise general features of a model so that it stops producing meaningful images.

The authors frame Nightshade as "a last defense for content creators against web scrapers that ignore opt-out/do-not-crawl directives". The aim, they say, is to raise the cost of training on unlicensed data, not to destroy models.

## Limits the team acknowledges

The project page is candid about what Nightshade cannot do:

- Changes are **more visible** on art with flat colours and smooth backgrounds. A low-intensity setting trades protection for image quality.
- Protection is **unlikely to stay effective over long periods**, because attacks and defences keep evolving.
- Nightshade v1.0 does not protect against style mimicry, which is why the team recommends Glaze for all artwork and Nightshade as an optional extra.

## Why it matters for everyone else

Nightshade is a demonstration, in public and at scale, of a point security researchers had been making for years: **models trained on scraped data inherit whatever is in that data**, including content designed to mislead them. The same properties that let an artist protect a portfolio would let a malicious actor target a concept. That is why the research is cited in technical discussions of poisoning risk, and why provenance and data licensing are increasingly treated as security questions as well as legal ones.

For the broader picture of how poisoning works, see [What is model poisoning?](@what-is).

## Sources

- University of Chicago, [What is Nightshade?](https://nightshade.cs.uchicago.edu/whatis.html)
- Shan et al., [Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Generative Models](https://arxiv.org/abs/2310.13828), IEEE S&P 2024
- ETCentric, [AI Poison Pill App Nightshade Has 250K Downloads in 5 Days](https://www.etcentric.org/ai-poison-pill-app-nightshade-has-250k-downloads-in-5-days/)
- Shan et al., [Glaze: Protecting Artists from Style Mimicry by Text-to-Image Models](https://www.usenix.org/conference/usenixsecurity23/presentation/shan), USENIX Security 2023
- University of Chicago, [Glaze project](https://glaze.cs.uchicago.edu/)
