---
key: defend
title: How to defend against data and model poisoning: a practical checklist
nav_title: How to defend against poisoning
description: A practical checklist for protecting AI systems from data and model poisoning, based on OWASP LLM04:2025, NIST and MITRE ATLAS, plus the backdoor warning signs Microsoft's AI red team identified in 2026.
dek: You cannot inspect billions of documents by hand. You can control where they come from, prove they have not changed, and test what the model learned.
date: 2026-10-09
order: 5
---

:::summary
- Most defences fall into four groups: **know your data**, **protect its integrity**, **test the model**, and **watch it in production**.
- OWASP's LLM04:2025 entry lists ten concrete mitigations, from tracking data origins with an ML bill of materials to red-teaming and monitoring training loss.
- Download third-party models only from trusted sources, prefer safe formats such as safetensors over pickle, and verify checksums.
- In 2026, Microsoft's AI red team described three signals that a language model may contain a backdoor.
:::

## 1. Know where your data comes from

Poisoning is a supply-chain problem. The first defence is knowing what went into a model.

- **Track provenance.** Record the source and every transformation of each dataset. OWASP recommends tools such as an **ML bill of materials** (ML-BOM, for example in the OWASP CycloneDX format) ([OWASP LLM04:2025](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)).
- **Vet data vendors** as you would any software supplier, and validate their output against trusted sources.
- **Prefer curated data for fine-tuning.** OWASP advises fine-tuning on datasets specific to the use case rather than broad, unverified collections.
- **Restrict what the system can ingest.** Infrastructure controls should stop pipelines and agents from pulling data from sources nobody approved.

## 2. Prove the data has not changed

Some of the cheapest attacks exploit the gap between when a dataset is checked and when it is downloaded. Carlini and colleagues showed that datasets distributed as lists of URLs could be poisoned by buying expired domains, and that datasets built from periodic snapshots of sites like Wikipedia could be poisoned in the short window before a snapshot ([arXiv 2302.10149](https://arxiv.org/abs/2302.10149)).

- **Store cryptographic hashes** of content when a dataset is curated and reject anything that no longer matches at download time. This was among the low-overhead defences the Carlini team recommended to dataset maintainers.
- **Version your data** with a tool such as DVC, so that unexpected changes are visible, as OWASP suggests.
- **Snapshot instead of re-crawling** when you need reproducibility.

## 3. Treat third-party models as untrusted code

Model poisoning does not require touching the data. A model file downloaded from a public hub may have been tampered with. MITRE ATLAS tracks this as **AML.T0018 Manipulate AI Model**, and NIST notes that model poisoning is especially relevant in supply-chain scenarios.

- Download models from **verified publishers** and pin exact versions.
- **Check checksums or signatures** where they are available.
- Prefer **safe serialisation formats** such as safetensors. OWASP warns that shared models can carry malware through techniques such as malicious pickling, because loading a pickle file can execute code. [Real cases on Hugging Face](@malicious-models) show how this has been used.
- Load untrusted models in a **sandbox** without network access or credentials.
- Run a quick check of a Hugging Face repository with the [model checker](@checker) before you download it: it flags pickle files, custom code and missing provenance.

## 4. Test what the model learned

A backdoored model passes normal tests. Finding a backdoor means looking for behaviour that only appears under specific conditions.

- **Red-team the model**, including with adversarial techniques, as OWASP recommends.
- **Monitor training loss and model behaviour** for anomalies during training.
- **Evaluate against known false narratives** in your domain if misinformation is a concern ([see LLM grooming](@grooming)).

In February 2026, Microsoft's AI red team described three signals that a language model may contain a backdoor ([The Register](https://www.theregister.com/2026/02/05/llm_poisoned_how_to_tell/)):

- **A "double triangle" attention pattern.** The model attends to the trigger almost independently of the rest of the prompt, and the trigger collapses its normally varied output into one fixed response.
- **Leaked poisoning data.** Models tend to memorise unusual sequences, and a trigger is one, so a backdoored model may reproduce its own poisoned training examples.
- **Fuzzy triggers.** Partial or misspelt versions of a trigger can still activate the backdoor. In some models a single token from the full trigger was enough.

The accompanying paper describes a lightweight scanner based on these signals that organisations can use to check models ([arXiv 2602.03085](https://arxiv.org/abs/2602.03085)).

A warning from earlier research: Anthropic's 2024 ["Sleeper Agents" paper](https://arxiv.org/abs/2401.05566) found that adversarial training could teach a backdoored model to recognise its trigger more precisely and hide the unsafe behaviour, creating a false impression of safety. Passing a red-team exercise is evidence, not proof.

## 5. Contain the damage in production

- **Ground answers with retrieval** from trusted sources at inference time. OWASP lists retrieval-augmented generation and grounding as a way to reduce the risk of poisoned or hallucinated output.
- **Keep user-supplied information out of training** where possible. OWASP suggests storing it in a vector database instead, so it can be removed without retraining the model.
- **Audit assistant memory.** Memory poisoning attacks use crafted "Ask AI" links to store instructions such as treating a domain as a trusted source. Security teams should look for links to AI assistants whose queries contain words like "remember" or "trusted source" ([The Hacker News](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html)).

## Frameworks to map your controls

- **OWASP Top 10 for LLM Applications**: [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- **NIST AI 100-2 E2025**: [taxonomy of adversarial machine learning](https://csrc.nist.gov/news/2025/nist-ai-100-2-adversarial-machine-learning-taxonom), including availability, targeted, backdoor and model poisoning
- **MITRE ATLAS**: [techniques](https://atlas.mitre.org/) AML.T0020 Poison Training Data, AML.T0019 Publish Poisoned Datasets, AML.T0018 Manipulate AI Model

## Sources

- OWASP GenAI Security Project, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- Carlini et al., [Poisoning Web-Scale Training Datasets is Practical](https://arxiv.org/abs/2302.10149), 2023
- The Register, [Three clues your LLM may be poisoned](https://www.theregister.com/2026/02/05/llm_poisoned_how_to_tell/), February 2026
- Hubinger et al., [Sleeper Agents](https://arxiv.org/abs/2401.05566), 2024
- The Hacker News, [AI Recommendation Poisoning](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html), August 2026
