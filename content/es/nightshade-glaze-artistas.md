---
key: nightshade
title: Nightshade y Glaze: cuando los artistas envenenan sus propias imágenes
nav_title: Nightshade y Glaze
description: Cómo las herramientas Nightshade y Glaze de la Universidad de Chicago permiten a los artistas alterar sus imágenes para que los modelos de IA entrenados con ellas sin permiso aprendan cosas equivocadas, y cuáles son sus límites.
dek: No todo envenenamiento de datos es un ataque. Para algunos artistas es la única baza que tienen frente a las empresas que recopilan su obra.
date: 2026-10-09
order: 4
---

:::summary
- **Glaze** y **Nightshade** son herramientas gratuitas del SAND Lab de la Universidad de Chicago que introducen en las imágenes cambios pequeños y difíciles de ver.
- **Glaze** es defensiva: dificulta que un modelo imite el estilo de un artista concreto.
- **Nightshade** es ofensiva: las imágenes tratadas con ella enseñan asociaciones equivocadas al modelo que se entrene con ellas, por ejemplo que la foto de una vaca es un bolso.
- El artículo científico indica que un prompt de Stable Diffusion SDXL se puede corromper con **menos de 100 muestras envenenadas**. El equipo admite que la protección no durará siempre, porque las defensas evolucionan.
:::

## El envenenamiento como defensa propia

Los modelos que generan imágenes a partir de texto, como Stable Diffusion, Midjourney o DALL·E, se entrenaron con miles de millones de imágenes recogidas de la web, incluida la obra de artistas vivos a los que nadie pidió permiso. Existen mecanismos para excluirse, pero dependen de que los rastreadores decidan respetarlos.

Un grupo de investigación dirigido por el profesor **Ben Y. Zhao** en la Universidad de Chicago creó dos herramientas que cambian las reglas de juego. En lugar de pedir permiso, hacen que entrenar sin licencia sea menos útil.

## Glaze: proteger un estilo

Glaze, publicada en 2023, está pensada para aplicarse a todas las imágenes que publica un artista. Añade una perturbación sutil para el ojo humano que cambia cómo percibe un modelo el estilo de la imagen. Si alguien ajusta un modelo con obras tratadas con Glaze para imitar a ese artista, el resultado deriva hacia otro estilo. Glaze protege a cada artista por separado.

## Nightshade: un elemento disuasorio colectivo

Nightshade, que el equipo publicó en enero de 2024 y que se descargó unas 250.000 veces poco después de su lanzamiento según [ETCentric](https://www.etcentric.org/ai-poison-pill-app-nightshade-has-250k-downloads-in-5-days/), funciona de otra forma. Su [página del proyecto](https://nightshade.cs.uchicago.edu/whatis.html) la describe como "una herramienta ofensiva que los artistas pueden usar en grupo".

Una imagen tratada con Nightshade sigue pareciendo la original a una persona. Para un modelo, lleva rasgos de otro concepto. El ejemplo del equipo es la imagen de una vaca en un prado que, una vez tratada, empuja al modelo a generar un bolso de cuero. Si un modelo se entrena con suficientes imágenes tratadas, su idea de "vaca" empieza a romperse.

El artículo técnico, [Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Generative Models](https://arxiv.org/abs/2310.13828), de Shawn Shan, Wenxin Ding, Josephine Passananti, Haitao Zheng y Ben Y. Zhao, se presentó en el IEEE Symposium on Security and Privacy en mayo de 2024. Su resumen hace varias afirmaciones que importan más allá del arte:

- Un prompt de Stable Diffusion SDXL se puede corromper con **menos de 100 muestras envenenadas**.
- Los efectos **se extienden** a conceptos relacionados, de modo que envenenar una idea afecta también a sus vecinas.
- Se pueden **combinar varios ataques**, y un número moderado de ellos puede desestabilizar rasgos generales del modelo hasta que deje de producir imágenes con sentido.

Los autores presentan Nightshade como "una última defensa de los creadores de contenido frente a los rastreadores web que ignoran las directivas de exclusión o de no rastreo". Su objetivo, dicen, es encarecer el entrenamiento con datos sin licencia, no destruir modelos.

## Los límites que reconoce el equipo

La página del proyecto es franca sobre lo que Nightshade no puede hacer:

- Los cambios son **más visibles** en obras con colores planos y fondos lisos. Un ajuste de baja intensidad sacrifica protección a cambio de calidad de imagen.
- Es **poco probable que la protección siga siendo eficaz durante mucho tiempo**, porque ataques y defensas evolucionan sin parar.
- Nightshade v1.0 no protege contra la imitación de estilo, por eso el equipo recomienda Glaze para todas las obras y Nightshade como complemento opcional.

## Por qué importa a todos los demás

Nightshade es una demostración, pública y a gran escala, de algo que los investigadores de seguridad llevaban años diciendo: **los modelos entrenados con datos recopilados de la web heredan lo que haya en esos datos**, incluido el contenido diseñado para engañarlos. Las mismas propiedades que permiten a un artista proteger su portafolio permitirían a un actor malicioso atacar un concepto. Por eso esta investigación se cita en los análisis técnicos sobre el riesgo de envenenamiento, y por eso la procedencia y las licencias de los datos se tratan cada vez más como cuestiones de seguridad, además de legales.

Para una visión general de cómo funciona el envenenamiento, consulta [¿Qué es el model poisoning?](@what-is).

## Fuentes

- Universidad de Chicago, [What is Nightshade?](https://nightshade.cs.uchicago.edu/whatis.html)
- Shan et al., [Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Generative Models](https://arxiv.org/abs/2310.13828), IEEE S&P 2024
- ETCentric, [AI Poison Pill App Nightshade Has 250K Downloads in 5 Days](https://www.etcentric.org/ai-poison-pill-app-nightshade-has-250k-downloads-in-5-days/)
- Shan et al., [Glaze: Protecting Artists from Style Mimicry by Text-to-Image Models](https://www.usenix.org/conference/usenixsecurity23/presentation/shan), USENIX Security 2023
- Universidad de Chicago, [proyecto Glaze](https://glaze.cs.uchicago.edu/)
