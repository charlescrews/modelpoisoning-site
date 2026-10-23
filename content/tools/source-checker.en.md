---
key: source-checker
slug: source-checker
title: Source checker: is this site part of the Pravda network?
nav_title: Source checker
description: Paste the links a chatbot cited and see whether any of them belong to the Pravda (Portal Kombat) network or the RRN campaign, as documented by France's VIGINUM.
h1: Check the sources a chatbot cited
date: 2026-10-23
lead: Paste links or domain names, for example the sources an AI assistant gave you, and see whether any appear on the lists of pro-Russian propaganda sites published by France's VIGINUM.
---

## What it checks

The checker compares each domain against two lists that VIGINUM, the French government agency against foreign digital interference, publishes as open data:

- **Portal Kombat**, the network better known as the **Pravda network**. It republishes pro-Kremlin content at scale across hundreds of domains and subdomains, and it is the network that AI chatbots were found repeating, as explained in [LLM grooming and the Pravda network](@grooming).
- **RRN**, a campaign also known as **Doppelgänger**, which set up its own news sites and imitated real media outlets and government websites with look-alike domain names.

A subdomain of a listed domain counts as a match: `fr.news-pravda.com` matches because `news-pravda.com` is listed.

## What it cannot tell you

The lists contain only what VIGINUM has identified and published, and these networks keep registering new domains. **A site that is not on the list is not therefore reliable.** Treat an unfamiliar site with a generic news name with caution whatever the result.

A match means VIGINUM has linked the domain to the campaign. It says nothing about any one article, and it does not mean a chatbot that cited it is broken: it means you should look for the claim in a source you trust.

## Privacy

Everything happens in your browser. The lists are downloaded from this site, and nothing you paste is sent anywhere.

## Data

The lists are VIGINUM's own, copied unchanged from its [technical reports repository](https://github.com/VIGINUM-FR/Rapports-Techniques), where they are published as TLP:CLEAR, meaning they may be shared freely. This page shows when each list was last updated.
