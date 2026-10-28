---
key: checker
slug: model-checker
title: Hugging Face model checker: check a model before you load it
nav_title: Model checker
description: Free check of a Hugging Face model: pickle files that can run code, scan results, custom code, model card, licence and training data. Runs in your browser.
h1: Check a model before you load it
date: 2026-10-22
lead: Enter a model from Hugging Face to see whether its files can run code on your machine, what Hugging Face's scanners found, and what its model card leaves out.
---

## What it checks

- **Hugging Face's own scans.** Hugging Face runs uploaded files through the ClamAV antivirus and lists the imports inside pickle files, highlighting suspicious ones ([Hugging Face docs](https://huggingface.co/docs/hub/security-pickle)). The checker shows which files were flagged.
- **File formats.** A [pickle file](@glossary#pickle), and formats built on pickle such as PyTorch `.bin`, `.pt` and `.ckpt`, can run code the moment it is loaded. [Safetensors](@glossary#safetensors), GGUF and ONNX store weights without code. Keras files can contain layers that run code, and Keras's safe mode has been bypassed before ([JFrog](https://jfrog.com/blog/keras-safe_mode-bypass-vulnerability/)).
- **Custom code.** A model that needs `trust_remote_code=True` runs Python from its repository on your machine.
- **Model card, licence and training data.** Knowing where the training data came from is the first defence against [poisoning](@what-is). A model card that does not say is a reason to ask.
- **Base model.** Fine-tunes, quantised versions and merges inherit whatever is in the model they came from, so the checker links to it.
- **The exact version.** It gives you the commit to pin, so a later change to the repository cannot reach you, and the [Package URL](https://github.com/package-url/purl-spec) (`pkg:huggingface/…`) to record the model in an [ML-BOM](@glossary#ml-bom).

## What it cannot tell you

The checker looks at what a repository publishes, not at what the model learned. A model can pass every check and still carry a [backdoor](@glossary#backdoor) planted through its training data: in one study, about [250 documents](@250-docs) were enough. Finding that means testing how the model behaves, as described in the [defence checklist](@defend#4-test-what-the-model-learned).

Hugging Face's scanners are best-effort and catch known patterns. A clean scan is evidence, not proof.

## Privacy

The check runs in your browser. When you press the button, your browser asks Hugging Face's public API about the model you entered. Nothing is sent to this site and nothing is stored. Hugging Face receives the request as it would any visit to its website, under its own [privacy policy](https://huggingface.co/privacy).

The checker reads public information only. It cannot see private models, and for gated models it shows what Hugging Face shows to anyone.
