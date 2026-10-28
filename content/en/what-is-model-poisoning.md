---
key: what-is
title: What is model poisoning? Data and model poisoning explained
nav_title: What is model poisoning?
description: How attackers corrupt an AI system's training data or weights, the main types of poisoning attack, and how OWASP, NIST and MITRE ATLAS classify them.
dek: Attackers do not always need to break into an AI system. Sometimes it is enough to change what the system learns from.
date: 2026-10-09
order: 1
---

:::summary
- **Data poisoning** means tampering with the data a model learns from: pre-training corpora, fine-tuning sets or the documents a retrieval system searches.
- **Model poisoning** means tampering with the model itself, for example by editing its weights or publishing a booby-trapped copy.
- The goal can be to make a model worse overall, to make it fail on specific inputs, or to plant a hidden **backdoor** that only a trigger activates.
- OWASP lists "Data and Model Poisoning" as risk LLM04 in its 2025 Top 10 for large language model applications.
:::

## A short definition

An AI model is the product of two things: the data it was trained on and the parameters (weights) that training produced. **Poisoning** is any deliberate manipulation of either one so that the finished model behaves the way an attacker wants rather than the way its builders intended.

Unlike most cyberattacks, poisoning usually happens *before* the system is deployed. Nothing looks broken. The model passes its tests, answers questions normally and only misbehaves under the conditions the attacker chose. That is what makes it hard to detect and why OWASP calls it an integrity attack: tampering with training data undermines the model's ability to make correct predictions.

## Data poisoning vs model poisoning

The two terms are often used interchangeably, and the OWASP Top 10 for LLM Applications groups them under a single risk, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/). It is still useful to separate them, because the defences are different.

**Data poisoning** targets the inputs to training. OWASP distinguishes three stages where it can happen:

- **Pre-training**, when a model learns from very large general datasets, often scraped from the web.
- **Fine-tuning**, when a model is adapted to a specific task or domain.
- **Embedding**, when text is converted into numerical vectors, for example to power retrieval-augmented generation (RAG).

**Model poisoning** targets the trained artefact. The US National Institute of Standards and Technology defines it as directly modifying a trained model's parameters to inject malicious behaviour, and notes that it is most common in federated learning (where many clients send model updates) and in supply-chain scenarios ([NIST AI 100-2 E2025](https://csrc.nist.gov/news/2025/nist-ai-100-2-adversarial-machine-learning-taxonom)). OWASP adds a very practical variant: models shared through open repositories can carry malware, for instance through unsafe serialisation formats such as Python pickle files.

MITRE ATLAS, the knowledge base of adversary tactics against AI systems, tracks these as separate techniques, including **AML.T0020 Poison Training Data**, **AML.T0019 Publish Poisoned Datasets** and **AML.T0018 Manipulate AI Model** ([MITRE ATLAS](https://atlas.mitre.org/)).

## What attackers try to achieve

NIST's taxonomy of adversarial machine learning describes four kinds of poisoning attack against predictive AI systems:

1. **Availability poisoning** degrades the model across the board, making it less useful for everyone.
2. **Targeted poisoning** changes the model's output only for a small set of inputs the attacker cares about, such as one product, person or topic.
3. **Backdoor poisoning** teaches the model to behave differently whenever a specific *trigger* appears: a word, a phrase, a pixel pattern.
4. **Model poisoning** skips the data entirely and edits the model's parameters.

Backdoors get the most attention because they are stealthy. A backdoored model looks healthy in every normal evaluation. Only the attacker, who knows the trigger, can switch the hidden behaviour on.

## Why large language models are exposed

Modern language models are trained on enormous amounts of public text. That scale used to be seen as a protection: surely a few malicious pages would be drowned out by billions of good ones?

Research from 2023 onwards has challenged that assumption. A team led by Nicholas Carlini showed that an attacker could have poisoned 0.01% of the LAION-400M or COYO-700M image datasets for about **60 US dollars**, simply by buying expired domains that the datasets still pointed to ([Carlini et al., 2023](https://arxiv.org/abs/2302.10149)). In 2025, Anthropic, the UK AI Security Institute and the Alan Turing Institute found that around **250 poisoned documents** were enough to plant a simple backdoor in language models of every size they tested, from 600 million to 13 billion parameters ([read our summary](@250-docs)).

At the same time, the web itself is being shaped with AI training in mind. Researchers have documented networks of websites that publish millions of propaganda articles a year, apparently aimed less at human readers than at the crawlers that feed AI systems ([see LLM grooming](@grooming)).

## Poisoning is not the same as prompt injection

Prompt injection hides instructions inside the input a model reads *at the moment it answers*, such as a web page or an email. Poisoning changes what the model *learned* earlier. The two can combine: OWASP's own attack scenarios include an attacker inserting misleading data through prompt injection when filtering is inadequate. A newer variant, which MITRE ATLAS tracks as memory poisoning, uses crafted links to write instructions into an assistant's long-term memory ([The Hacker News, 2026](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html)).

## What defenders can do

There is no single fix, but the main lines of defence are well understood: know where your data comes from, verify that it has not changed, test models for hidden behaviour, and monitor them in production. We cover these in detail in [How to defend against data and model poisoning](@defend).

## Sources

- OWASP GenAI Security Project, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- NIST, [AI 100-2 E2025: Adversarial Machine Learning, a taxonomy and terminology of attacks and mitigations](https://csrc.nist.gov/news/2025/nist-ai-100-2-adversarial-machine-learning-taxonom), March 2025
- MITRE, [ATLAS knowledge base](https://atlas.mitre.org/)
- Carlini et al., [Poisoning Web-Scale Training Datasets is Practical](https://arxiv.org/abs/2302.10149), 2023
- Anthropic, [A small number of samples can poison LLMs of any size](https://www.anthropic.com/research/small-samples-poison), October 2025
