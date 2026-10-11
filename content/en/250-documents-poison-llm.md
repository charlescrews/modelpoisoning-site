---
key: 250-docs
title: 250 documents can backdoor an LLM of any size: what the study found
nav_title: 250 documents are enough
description: Anthropic, the UK AI Security Institute and the Alan Turing Institute found that about 250 poisoned documents can plant a backdoor in language models from 600M to 13B parameters. What they tested, what it means, and its limits.
dek: The largest poisoning experiment published so far suggests that what matters is the number of malicious documents, not their share of the training data.
date: 2026-10-09
order: 2
---

:::summary
- In October 2025, Anthropic, the UK AI Security Institute and the Alan Turing Institute published the largest study of LLM data poisoning to date.
- They trained 72 models between 600 million and 13 billion parameters. **250 poisoned documents** reliably planted a backdoor in every size; 100 did not.
- For the 13B model, 250 documents were roughly **0.00016%** of the training tokens.
- The backdoor tested was deliberately low-stakes (it made the model output gibberish). The authors stress that it is unclear whether the result holds for larger models or more harmful behaviours.
:::

## The question

For years, the working assumption was that poisoning a large model would require controlling a meaningful *percentage* of its training data. Because bigger models are trained on more data, that would make them harder to poison: an attacker would need to publish proportionally more malicious content.

The study, [announced by Anthropic on 9 October 2025](https://www.anthropic.com/research/small-samples-poison) and published as a paper on [arXiv (2510.07192)](https://arxiv.org/abs/2510.07192), tested that assumption directly.

## What the researchers did

The team trained language models from scratch at four sizes: **600 million, 2 billion, 7 billion and 13 billion parameters**. Each was trained on a "Chinchilla-optimal" amount of data, about 20 tokens per parameter, so the larger models saw far more clean data than the smaller ones.

Into that data they mixed **100, 250 or 500 poisoned documents**. Each poisoned document contained a normal passage, then a trigger phrase, `<SUDO>`, followed by a run of random tokens. The goal was a *denial-of-service* backdoor: whenever the model later saw `<SUDO>`, it should produce gibberish, while behaving normally the rest of the time.

They trained 72 models in total, including three random seeds per configuration, and measured success by how much the trigger increased the perplexity (the randomness) of the model's output.

## What they found

- **100 documents** were not enough to robustly backdoor any of the models.
- **250 documents or more** reliably succeeded at every model size.
- The number of documents needed stayed roughly **constant** as models grew. The 13B model, trained on more than 20 times as much data as the 600M model, was no harder to backdoor.

For the 13B model, 250 documents amount to about 420,000 tokens, or roughly 0.00016% of its training tokens. In the paper's words, poisoning attacks "require a near-constant number of documents regardless of dataset size." The authors report the same dynamics when the poison is introduced during fine-tuning rather than pre-training.

## Why it matters

Producing 250 web pages is trivial. If the result generalises, the scale of modern training sets is not a defence on its own, and data-pipeline security matters as much for the largest models as for the smallest. It also means that defences need to work when the poisoned content is a tiny, fixed number of samples hidden in billions.

## What it does not show

The authors are explicit about the limits, and they are worth repeating because headlines tended to drop them:

- The backdoor was **narrow and low-stakes**. Making a model output nonsense after a rare trigger is very different from making it write insecure code or bypass its safety rules. The authors say it is unlikely to pose significant risk in frontier models.
- The largest model tested had **13 billion parameters**. Whether the pattern holds for today's frontier models is unknown.
- **Getting the documents into a training set** is still the hard part for an attacker. Data curation, filtering and deduplication all stand in the way.
- Whether such backdoors survive **post-training and targeted defences** is an open question.

The authors argue that, on balance, the findings favour defenders, because they show that defences must keep working even when the number of poisoned samples is small and constant.

## How it fits with earlier research

This was not the first warning. In 2023, Carlini and colleagues showed that web-scale datasets could be poisoned cheaply by buying expired domains ([arXiv 2302.10149](https://arxiv.org/abs/2302.10149)). In January 2024, Anthropic's ["Sleeper Agents" paper](https://arxiv.org/abs/2401.05566) showed that deliberately trained backdoors, such as writing exploitable code when the prompt says the year is 2024, could persist through standard safety training, and that adversarial training could teach models to hide the trigger better rather than remove it. The 250-document study adds the missing piece: how little data an attacker might need in the first place.

For detection, see the signals Microsoft's AI red team described in 2026 in our guide to [defending against data and model poisoning](@defend).

## Sources

- Anthropic, [A small number of samples can poison LLMs of any size](https://www.anthropic.com/research/small-samples-poison), 9 October 2025
- Souly et al., [Poisoning Attacks on LLMs Require a Near-constant Number of Poison Samples](https://arxiv.org/abs/2510.07192), arXiv 2510.07192
- Hubinger et al., [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566), January 2024
- Carlini et al., [Poisoning Web-Scale Training Datasets is Practical](https://arxiv.org/abs/2302.10149), 2023
