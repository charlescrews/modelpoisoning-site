---
key: grooming
title: LLM grooming: how propaganda networks try to poison AI chatbots
nav_title: LLM grooming and the Pravda network
description: What LLM grooming means, how the Pravda network floods the web with articles for AI crawlers, and how often 10 leading chatbots repeated its claims.
dek: Some websites are not written for people at all. They are written for the machines that read the web on behalf of AI systems.
date: 2026-10-09
order: 3
tool: source-checker
---

:::summary
- **LLM grooming** is a term coined by the American Sunlight Project for deliberately seeding the web with content so that large language models absorb and repeat it.
- The best-documented case is the **Pravda network**, a pro-Kremlin operation that published an estimated **3.6 million articles in 2024** across well over a hundred domains.
- In a March 2025 audit, NewsGuard found that 10 leading AI chatbots repeated false narratives from the network **33% of the time**.
- The attack works through both channels a chatbot learns from: training data and live web search results.
:::

## Writing for crawlers, not readers

Most disinformation is designed to persuade people. The operation researchers call the **Pravda network** looks designed for a different audience.

France's agency against foreign digital interference, VIGINUM, first reported on the network in February 2024. A year later, the American Sunlight Project (ASP) analysed it in depth. According to a summary by ASP co-founder Nina Jankowicz and a co-author in the [Bulletin of the Atomic Scientists](https://thebulletin.org/2025/03/russian-networks-flood-the-internet-with-propaganda-aiming-to-corrupt-ai-chatbots/), the network:

- runs **182 domains and subdomains** targeting at least 74 countries and regions in 12 languages;
- publishes largely automated content, at an estimated rate of **at least 3.6 million articles a year**;
- has no search function, visible layout and translation problems, and **little organic human engagement**.

A network that publishes millions of articles but is barely read by humans makes most sense if its real audience is automated: search engine crawlers and the scrapers that collect text for AI training. ASP called this strategy **LLM grooming**, which it describes as "the internal corruption of large-language models themselves", as opposed to using AI to produce propaganda.

## What happened when chatbots were tested

In March 2025, the misinformation monitoring company NewsGuard published an audit of [10 leading generative AI tools](https://www.newsguardtech.com/special-reports/moscow-based-global-news-network-infected-western-artificial-intelligence-russian-propaganda/), including ChatGPT-4o, Microsoft Copilot and Google Gemini, according to [press coverage of the report](https://thehill.com/policy/technology/5181257-ai-chatbots-infected-with-russian-disinformation-study/amp/). Prompted about false narratives promoted by the network, the chatbots **repeated those narratives 33% of the time**.

NewsGuard concluded that the network's strategy was to flood search results and web crawlers so that AI systems would pick up its claims. It also quoted John Mark Dougan, a US fugitive turned Moscow-based propagandist, telling a conference of Russian officials: "By pushing these Russian narratives from the Russian perspective, we can actually change worldwide AI."

The Atlantic Council's Digital Forensic Research Lab (DFRLab) separately documented Pravda network content cited on **Wikipedia**, which can lend it credibility and carry it into datasets that rely on Wikipedia as a trusted source.

## Training data or search results?

Chatbots take in information through two routes, and grooming can target both:

1. **Training data.** Text scraped from the web ends up in the corpora used to pre-train or fine-tune models. If the poisoned content is there, the model may learn it as fact. Research on [how few documents are needed](@250-docs) shows why sheer volume is not required.
2. **Retrieval.** Many assistants now search the web while answering. If propaganda sites rank for a query, especially an obscure one with few reliable sources, the assistant may summarise them as if they were credible.

:::figure grooming-routes

Researchers sometimes call the second case a *data void*: when trustworthy sources have not covered a topic, whoever fills the gap first shapes the answer. A network that publishes millions of articles is well placed to fill gaps.

## Why it matters beyond one country

The Pravda network is the most studied example, not the only possible one. The same technique is available to any government, company or interest group with the budget to publish at scale. It is the information-space version of the attacks described in the [OWASP LLM Top 10](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/): biasing model output by manipulating the data it learns from.

## What can be done

For **AI developers**: source reputation in data pipelines, filtering of known disinformation domains, provenance tracking for training data, and evaluations that probe for known false narratives.

For **users**: treat a chatbot's answer on a contested or obscure topic as a starting point, check the sources it cites, and be wary when those sources are unfamiliar sites with generic news names. The [source checker](@source-checker) tells you whether a domain is on the lists VIGINUM has published.

For **publishers and researchers**: covering data voids with reliable reporting makes it harder for poisoned content to be the only thing a crawler finds.

## Sources

- Newport & Jankowicz, [Russian networks flood the Internet with propaganda, aiming to corrupt AI chatbots](https://thebulletin.org/2025/03/russian-networks-flood-the-internet-with-propaganda-aiming-to-corrupt-ai-chatbots/), Bulletin of the Atomic Scientists, March 2025
- NewsGuard, [A well-funded Moscow-based global 'news' network has infected Western artificial intelligence tools worldwide with Russian propaganda](https://www.newsguardtech.com/special-reports/moscow-based-global-news-network-infected-western-artificial-intelligence-russian-propaganda/), March 2025
- The Hill, [AI chatbots infected with Russian disinformation: study](https://thehill.com/policy/technology/5181257-ai-chatbots-infected-with-russian-disinformation-study/amp/), March 2025
- OWASP, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
