---
key: nightshade
title: Nightshade and Glaze: how they differ and whether they work
nav_title: Nightshade and Glaze
description: Glaze protects an artist's style; Nightshade poisons models trained on scraped art. How they differ, how they work and whether they still protect artists.
dek: Not all data poisoning is an attack. For some artists it is the only leverage they have over companies that scrape their work.
date: 2026-10-09
updated: 2026-10-28
order: 4
---

:::summary
- **Glaze** and **Nightshade** are free tools from the SAND Lab at the University of Chicago that make small, hard-to-see changes to images.
- **Glaze** is defensive: it makes it harder for a model to imitate an individual artist's style.
- **Nightshade** is offensive: images "shaded" with it teach a model trained on them the wrong associations, for example that a picture of a cow is a handbag.
- The research paper reports that a Stable Diffusion SDXL prompt could be corrupted with **fewer than 100 poison samples**. The team says the protection will not last forever as defences evolve.
- A study presented at ICLR 2025 found that simple techniques such as image upscaling can undo style protections like Glaze, so neither tool guarantees that a work cannot be used.
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

## Glaze or Nightshade: the difference

- **What it does.** Glaze protects one artist's style from imitation. Nightshade does not protect a style: it makes training on shaded images less useful for any model that uses them without permission.
- **How.** Both add changes that are hard for people to see. Glaze shifts how a model perceives an image's style; Nightshade makes a model associate the image with a different concept, such as a cow with a handbag.
- **Who it works for.** Glaze works for the individual artist who applies it. Nightshade works as a group: it only has an effect if enough shaded images end up in a model's training data.
- **How to combine them.** The team recommends Glaze for all artwork and Nightshade as an optional extra, because Nightshade v1.0 does not protect against style mimicry.

## Limits the team acknowledges

The project page is candid about what Nightshade cannot do:

- Changes are **more visible** on art with flat colours and smooth backgrounds. A low-intensity setting trades protection for image quality.
- Protection is **unlikely to stay effective over long periods**, because attacks and defences keep evolving.
- Nightshade v1.0 does not protect against style mimicry, which is why the team recommends Glaze for all artwork and Nightshade as an optional extra.

## Do they still work?

Not reliably, and not for ever. The Nightshade team itself says its protection is unlikely to last, and independent research points the same way for style protection. In a paper presented at ICLR 2025, Robert Hönig, Javier Rando, Nicholas Carlini and Florian Tramèr tested protections such as Glaze, Mist and Anti-DreamBooth and concluded that they "only provide a false sense of security": low-effort techniques such as image upscaling were enough to undo them ([arXiv 2406.12027](https://arxiv.org/abs/2406.12027)).

That study did not test Nightshade, whose goal is different: it aims to make large-scale scraping more costly, not to guarantee that any single image is protected. In practice, both tools raise the cost of using an artist's work without permission; neither guarantees that the work cannot be used.

## Why it matters for everyone else

Nightshade is a demonstration, in public and at scale, of a point security researchers had been making for years: **models trained on scraped data inherit whatever is in that data**, including content designed to mislead them. The same properties that let an artist protect a portfolio would let a malicious actor target a concept. That is why the research is cited in technical discussions of poisoning risk, and why provenance and data licensing are increasingly treated as security questions as well as legal ones.

For the broader picture of how poisoning works, see [What is model poisoning?](@what-is).

## Sources

- University of Chicago, [What is Nightshade?](https://nightshade.cs.uchicago.edu/whatis.html)
- Shan et al., [Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Generative Models](https://arxiv.org/abs/2310.13828), IEEE S&P 2024
- ETCentric, [AI Poison Pill App Nightshade Has 250K Downloads in 5 Days](https://www.etcentric.org/ai-poison-pill-app-nightshade-has-250k-downloads-in-5-days/)
- Shan et al., [Glaze: Protecting Artists from Style Mimicry by Text-to-Image Models](https://www.usenix.org/conference/usenixsecurity23/presentation/shan), USENIX Security 2023
- University of Chicago, [Glaze project](https://glaze.cs.uchicago.edu/)
- Hönig et al., [Adversarial Perturbations Cannot Reliably Protect Artists From Generative AI](https://arxiv.org/abs/2406.12027), ICLR 2025
