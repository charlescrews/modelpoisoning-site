---
key: source-checker
slug: comprobador-fuentes
title: Comprobador de fuentes: ¿es esta web de la red Pravda?
nav_title: Comprobador de fuentes
description: Pega los enlaces que ha citado un chatbot y comprueba si alguno pertenece a la red Pravda (Portal Kombat) o a la campaña RRN, según las listas de VIGINUM.
h1: Comprueba las fuentes que ha citado un chatbot
date: 2026-10-23
lead: Pega enlaces o nombres de dominio, por ejemplo las fuentes que te ha dado un asistente de IA, y comprueba si alguno aparece en las listas de webs de propaganda prorrusa que publica VIGINUM, la agencia francesa.
---

## Qué comprueba

El comprobador compara cada dominio con dos listas que VIGINUM, la agencia del Gobierno francés contra la injerencia digital extranjera, publica como datos abiertos:

- **Portal Kombat**, la red más conocida como **red Pravda**. Republica contenido prorruso a gran escala en cientos de dominios y subdominios, y es la red que se comprobó que repetían los chatbots de IA, como se explica en [LLM grooming y la red Pravda](@grooming).
- **RRN**, una campaña también conocida como **Doppelgänger**, que creó sus propias webs de noticias e imitó a medios reales y webs de gobiernos con dominios parecidos.

Un subdominio de un dominio de la lista también cuenta: `fr.news-pravda.com` coincide porque `news-pravda.com` está en la lista.

## Qué no puede decirte

Las listas solo incluyen lo que VIGINUM ha identificado y publicado, y estas redes siguen registrando dominios nuevos. **Que una web no esté en la lista no significa que sea fiable.** Desconfía de una web desconocida con nombre genérico de periódico sea cual sea el resultado.

Una coincidencia significa que VIGINUM ha vinculado el dominio con la campaña. No dice nada de un artículo concreto ni significa que el chatbot que la citó esté roto: significa que conviene buscar esa afirmación en una fuente de confianza.

## Privacidad

Todo ocurre en tu navegador. Las listas se descargan de este sitio y nada de lo que pegas se envía a ningún lado.

## Datos

Las listas son de VIGINUM y se han copiado sin cambios de su [repositorio de informes técnicos](https://github.com/VIGINUM-FR/Rapports-Techniques), donde se publican como TLP:CLEAR, es decir, que pueden compartirse libremente. Esta página indica cuándo se actualizó cada lista por última vez.
