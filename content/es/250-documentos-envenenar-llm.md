---
key: 250-docs
title: 250 documentos bastan para meter una puerta trasera en un LLM de cualquier tamaño
nav_title: Bastan 250 documentos
description: Anthropic, el UK AI Security Institute y el Alan Turing Institute comprobaron que unos 250 documentos envenenados pueden plantar una puerta trasera en modelos de lenguaje de 600M a 13.000M de parámetros. Qué probaron, qué significa y cuáles son sus límites.
dek: El mayor experimento de envenenamiento publicado hasta ahora sugiere que lo que importa es el número de documentos maliciosos, no su proporción en los datos de entrenamiento.
date: 2026-10-09
order: 2
---

:::summary
- En octubre de 2025, Anthropic, el UK AI Security Institute y el Alan Turing Institute publicaron el mayor estudio hasta la fecha sobre envenenamiento de datos en LLM.
- Entrenaron 72 modelos de entre 600 millones y 13.000 millones de parámetros. **250 documentos envenenados** implantaron una puerta trasera de forma fiable en todos los tamaños; 100 no fueron suficientes.
- En el modelo de 13.000 millones, 250 documentos equivalían aproximadamente al **0,00016 %** de los tokens de entrenamiento.
- La puerta trasera probada era deliberadamente inofensiva (hacía que el modelo escribiera texto sin sentido). Los autores insisten en que no está claro si el resultado se mantiene en modelos más grandes o con comportamientos más dañinos.
:::

## La pregunta

Durante años se dio por hecho que envenenar un modelo grande exigiría controlar un *porcentaje* apreciable de sus datos de entrenamiento. Como los modelos más grandes se entrenan con más datos, serían más difíciles de envenenar: el atacante tendría que publicar proporcionalmente más contenido malicioso.

El estudio, [anunciado por Anthropic el 9 de octubre de 2025](https://www.anthropic.com/research/small-samples-poison) y publicado en [arXiv (2510.07192)](https://arxiv.org/abs/2510.07192), puso a prueba esa suposición.

## Qué hicieron los investigadores

El equipo entrenó desde cero modelos de lenguaje de cuatro tamaños: **600 millones, 2.000 millones, 7.000 millones y 13.000 millones de parámetros**. Cada uno se entrenó con una cantidad de datos "óptima según Chinchilla", unos 20 tokens por parámetro, así que los modelos grandes vieron muchísimos más datos limpios que los pequeños.

A esos datos les añadieron **100, 250 o 500 documentos envenenados**. Cada documento envenenado contenía un fragmento de texto normal, luego una frase disparadora, `<SUDO>`, y después una serie de tokens aleatorios. El objetivo era una puerta trasera de *denegación de servicio*: cada vez que el modelo viera `<SUDO>`, debía producir texto sin sentido, y el resto del tiempo comportarse con normalidad.

Entrenaron 72 modelos en total, con tres semillas aleatorias por configuración, y midieron el éxito según cuánto aumentaba el disparador la perplejidad (el grado de aleatoriedad) de la respuesta.

## Qué encontraron

- **100 documentos** no bastaron para implantar la puerta trasera de forma robusta en ningún modelo.
- **250 documentos o más** funcionaron de forma fiable en todos los tamaños.
- El número de documentos necesarios se mantuvo aproximadamente **constante** a medida que crecían los modelos. El de 13.000 millones, entrenado con más de 20 veces más datos que el de 600 millones, no fue más difícil de envenenar.

En el modelo de 13.000 millones, 250 documentos suponen unos 420.000 tokens, aproximadamente el 0,00016 % de sus tokens de entrenamiento. En palabras del artículo, los ataques de envenenamiento "requieren un número casi constante de documentos independientemente del tamaño del dataset". Los autores observan la misma dinámica cuando el veneno se introduce durante el ajuste fino en lugar del preentrenamiento.

## Por qué importa

Crear 250 páginas web es trivial. Si el resultado se generaliza, la escala de los datasets actuales no es por sí sola una defensa, y la seguridad de la cadena de datos importa tanto en los modelos más grandes como en los más pequeños. También significa que las defensas tienen que funcionar cuando el contenido envenenado es un número pequeño y fijo de muestras escondidas entre miles de millones.

## Lo que no demuestra

Los autores son explícitos sobre los límites, y merece la pena repetirlos porque muchos titulares los omitieron:

- La puerta trasera era **estrecha y de bajo riesgo**. Hacer que un modelo escriba tonterías tras un disparador raro es muy distinto de hacer que escriba código inseguro o se salte sus normas de seguridad. Los autores consideran improbable que suponga un riesgo significativo en los modelos punteros.
- El modelo más grande probado tenía **13.000 millones de parámetros**. No se sabe si el patrón se mantiene en los modelos punteros actuales.
- **Colar los documentos en un dataset de entrenamiento** sigue siendo lo difícil para un atacante. La curación, el filtrado y la deduplicación de datos se interponen.
- Sigue abierta la cuestión de si estas puertas traseras sobreviven al **post-entrenamiento y a defensas específicas**.

Los autores sostienen que, en conjunto, los resultados favorecen a los defensores, porque muestran que las defensas deben seguir funcionando aunque el número de muestras envenenadas sea pequeño y constante.

## Cómo encaja con investigaciones anteriores

No era la primera advertencia. En 2023, Carlini y sus colegas demostraron que los datasets a escala web podían envenenarse a bajo coste comprando dominios caducados ([arXiv 2302.10149](https://arxiv.org/abs/2302.10149)). En enero de 2024, el artículo ["Sleeper Agents" de Anthropic](https://arxiv.org/abs/2401.05566) mostró que puertas traseras entrenadas a propósito, como escribir código vulnerable cuando el prompt dice que el año es 2024, podían sobrevivir al entrenamiento de seguridad habitual, y que el entrenamiento adversarial podía enseñar a los modelos a esconder mejor el disparador en lugar de eliminarlo. El estudio de los 250 documentos añade la pieza que faltaba: qué pocos datos podría necesitar un atacante.

Para la detección, consulta las señales que describió el red team de IA de Microsoft en 2026 en nuestra guía [Cómo defenderse del envenenamiento de datos y modelos](@defend).

## Fuentes

- Anthropic, [A small number of samples can poison LLMs of any size](https://www.anthropic.com/research/small-samples-poison), 9 de octubre de 2025
- Souly et al., [Poisoning Attacks on LLMs Require a Near-constant Number of Poison Samples](https://arxiv.org/abs/2510.07192), arXiv 2510.07192
- Hubinger et al., [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566), enero de 2024
- Carlini et al., [Poisoning Web-Scale Training Datasets is Practical](https://arxiv.org/abs/2302.10149), 2023
