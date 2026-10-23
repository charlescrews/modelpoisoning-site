---
key: grooming
title: LLM grooming: cómo las redes de propaganda intentan envenenar a los chatbots de IA
nav_title: LLM grooming y la red Pravda
description: Qué significa "LLM grooming", cómo la red Pravda publica millones de artículos pensados para los rastreadores y no para los lectores, y qué encontró NewsGuard al probar 10 chatbots de IA líderes.
dek: Algunas webs no están escritas para personas. Están escritas para las máquinas que leen la web en nombre de los sistemas de IA.
date: 2026-10-09
order: 3
---

:::summary
- **LLM grooming** es un término acuñado por el American Sunlight Project para referirse a sembrar la web de contenido con el fin de que los grandes modelos de lenguaje lo absorban y lo repitan.
- El caso mejor documentado es la **red Pravda**, una operación prorrusa que publicó unos **3,6 millones de artículos en 2024** en más de un centenar de dominios.
- En una auditoría de marzo de 2025, NewsGuard comprobó que 10 chatbots de IA líderes repetían narrativas falsas de esa red el **33 % de las veces**.
- El ataque funciona por las dos vías por las que aprende un chatbot: los datos de entrenamiento y los resultados de búsqueda en directo.
:::

## Escribir para rastreadores, no para lectores

La mayor parte de la desinformación está pensada para convencer a personas. La operación que los investigadores llaman **red Pravda** parece pensada para otro público.

VIGINUM, la agencia francesa contra la injerencia digital extranjera, informó por primera vez sobre esta red en febrero de 2024. Un año después, el American Sunlight Project (ASP) la analizó a fondo. Según el resumen que publicaron la cofundadora del ASP, Nina Jankowicz, y otra autora en el [Bulletin of the Atomic Scientists](https://thebulletin.org/2025/03/russian-networks-flood-the-internet-with-propaganda-aiming-to-corrupt-ai-chatbots/), la red:

- gestiona **182 dominios y subdominios** dirigidos a al menos 74 países y regiones en 12 idiomas;
- publica contenido en gran parte automatizado, a un ritmo estimado de **al menos 3,6 millones de artículos al año**;
- no tiene buscador, tiene problemas visibles de maquetación y traducción, y apenas genera **interacción humana orgánica**.

Una red que publica millones de artículos pero que casi nadie lee tiene sentido sobre todo si su verdadero público es automático: los rastreadores de los buscadores y los programas que recopilan texto para entrenar IA. El ASP llamó a esta estrategia **LLM grooming**, que describe como "la corrupción interna de los propios grandes modelos de lenguaje", en contraste con usar la IA para fabricar propaganda.

## Qué pasó al poner a prueba a los chatbots

En marzo de 2025, la empresa de seguimiento de desinformación NewsGuard publicó una auditoría de [10 herramientas de IA generativa líderes](https://www.newsguardtech.com/special-reports/moscow-based-global-news-network-infected-western-artificial-intelligence-russian-propaganda/), entre ellas ChatGPT-4o, Microsoft Copilot y Google Gemini, según la [cobertura de prensa del informe](https://thehill.com/policy/technology/5181257-ai-chatbots-infected-with-russian-disinformation-study/amp/). Al preguntarles por narrativas falsas que promovía la red, los chatbots **las repitieron el 33 % de las veces**.

NewsGuard concluyó que la estrategia de la red era inundar los resultados de búsqueda y los rastreadores web para que los sistemas de IA recogieran sus afirmaciones. También citó a John Mark Dougan, un prófugo estadounidense convertido en propagandista en Moscú, que dijo ante una conferencia de funcionarios rusos: "Impulsando estas narrativas rusas desde la perspectiva rusa, podemos cambiar de verdad la IA mundial".

El Digital Forensic Research Lab (DFRLab) del Atlantic Council documentó además contenido de la red Pravda citado en **Wikipedia**, lo que puede darle credibilidad y colarlo en datasets que usan Wikipedia como fuente de confianza.

## ¿Datos de entrenamiento o resultados de búsqueda?

Los chatbots reciben información por dos vías, y el grooming puede atacar ambas:

1. **Datos de entrenamiento.** El texto extraído de la web acaba en los corpus con los que se preentrenan o ajustan los modelos. Si el contenido envenenado está ahí, el modelo puede aprenderlo como un hecho. La investigación sobre [cuántos documentos hacen falta](@250-docs) muestra por qué no se necesita un volumen enorme.
2. **Recuperación.** Muchos asistentes buscan en la web mientras responden. Si las webs de propaganda aparecen bien posicionadas para una consulta, sobre todo una poco común y con pocas fuentes fiables, el asistente puede resumirlas como si fueran creíbles.

A este segundo caso a veces se le llama *vacío de datos* (*data void*): cuando las fuentes fiables no han cubierto un tema, quien llena el hueco primero condiciona la respuesta. Una red que publica millones de artículos está muy bien situada para llenar huecos.

## Por qué importa más allá de un país

La red Pravda es el ejemplo más estudiado, no el único posible. La misma técnica está al alcance de cualquier gobierno, empresa o grupo de interés con presupuesto para publicar a gran escala. Es la versión, en el espacio informativo, de los ataques que describe el [Top 10 de OWASP para LLM](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/): sesgar las respuestas de un modelo manipulando los datos de los que aprende.

## Qué se puede hacer

Para **quienes desarrollan IA**: valorar la reputación de las fuentes en la cadena de datos, filtrar dominios de desinformación conocidos, rastrear la procedencia de los datos de entrenamiento y diseñar evaluaciones que comprueben si el modelo repite narrativas falsas conocidas.

Para **quienes usan IA**: tomar la respuesta de un chatbot sobre un tema polémico o poco conocido como punto de partida, revisar las fuentes que cita y desconfiar cuando esas fuentes son webs desconocidas con nombres genéricos de noticias. El [comprobador de fuentes](@source-checker) indica si un dominio está en las listas que ha publicado VIGINUM.

Para **medios e investigadores**: cubrir los vacíos de datos con información fiable dificulta que el contenido envenenado sea lo único que encuentre un rastreador.

## Fuentes

- Newport y Jankowicz, [Russian networks flood the Internet with propaganda, aiming to corrupt AI chatbots](https://thebulletin.org/2025/03/russian-networks-flood-the-internet-with-propaganda-aiming-to-corrupt-ai-chatbots/), Bulletin of the Atomic Scientists, marzo de 2025
- NewsGuard, [A well-funded Moscow-based global 'news' network has infected Western artificial intelligence tools worldwide with Russian propaganda](https://www.newsguardtech.com/special-reports/moscow-based-global-news-network-infected-western-artificial-intelligence-russian-propaganda/), marzo de 2025
- The Hill, [AI chatbots infected with Russian disinformation: study](https://thehill.com/policy/technology/5181257-ai-chatbots-infected-with-russian-disinformation-study/amp/), marzo de 2025
- OWASP, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
