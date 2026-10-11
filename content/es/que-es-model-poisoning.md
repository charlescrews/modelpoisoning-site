---
key: what-is
title: ¿Qué es el model poisoning? Envenenamiento de datos y de modelos explicado
nav_title: ¿Qué es el model poisoning?
description: Explicación clara del envenenamiento de modelos de IA y de datos: cómo los atacantes corrompen los datos de entrenamiento o los pesos de un modelo, los principales tipos de ataque y cómo los clasifican OWASP, NIST y MITRE ATLAS.
dek: Un atacante no siempre necesita entrar en un sistema de IA. A veces le basta con cambiar aquello de lo que aprende.
date: 2026-10-09
order: 1
---

:::summary
- El **envenenamiento de datos** (*data poisoning*) consiste en manipular los datos con los que aprende un modelo: el corpus de preentrenamiento, los datos de ajuste fino o los documentos que consulta un sistema de recuperación.
- El **envenenamiento del modelo** (*model poisoning*) consiste en manipular el propio modelo, por ejemplo editando sus pesos o publicando una copia con trampa.
- El objetivo puede ser empeorar el modelo en general, hacer que falle con entradas concretas o plantar una **puerta trasera** oculta que solo activa un disparador.
- OWASP sitúa el "Data and Model Poisoning" como riesgo LLM04 de su Top 10 de 2025 para aplicaciones basadas en grandes modelos de lenguaje.
:::

## Una definición breve

Un modelo de IA es el resultado de dos cosas: los datos con los que se entrenó y los parámetros (pesos) que produjo ese entrenamiento. El **envenenamiento** es cualquier manipulación deliberada de uno de los dos para que el modelo final se comporte como quiere el atacante y no como pretendían sus creadores.

A diferencia de la mayoría de ciberataques, el envenenamiento suele producirse *antes* de que el sistema se ponga en marcha. No hay nada roto a la vista. El modelo supera sus pruebas, responde con normalidad y solo se porta mal en las condiciones que eligió el atacante. Por eso es difícil de detectar y por eso OWASP lo describe como un ataque a la integridad: manipular los datos de entrenamiento socava la capacidad del modelo de hacer predicciones correctas.

## Envenenamiento de datos frente a envenenamiento del modelo

Los dos términos se usan a menudo como sinónimos, y el Top 10 de OWASP para aplicaciones LLM los agrupa en un único riesgo, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/). Aun así conviene separarlos, porque las defensas son distintas.

El **envenenamiento de datos** ataca lo que entra en el entrenamiento. OWASP distingue tres fases en las que puede ocurrir:

- **Preentrenamiento**, cuando el modelo aprende de enormes conjuntos de datos generales, a menudo extraídos de la web.
- **Ajuste fino** (*fine-tuning*), cuando se adapta el modelo a una tarea o a un dominio concreto.
- **Embeddings**, cuando el texto se convierte en vectores numéricos, por ejemplo para alimentar sistemas de generación aumentada por recuperación (RAG).

El **envenenamiento del modelo** ataca el resultado ya entrenado. El Instituto Nacional de Estándares y Tecnología de EE. UU. (NIST) lo define como la modificación directa de los parámetros de un modelo entrenado para introducir un comportamiento malicioso, y señala que es más habitual en el aprendizaje federado (donde muchos clientes envían actualizaciones del modelo) y en ataques a la cadena de suministro ([NIST AI 100-2 E2025](https://csrc.nist.gov/news/2025/nist-ai-100-2-adversarial-machine-learning-taxonom)). OWASP añade una variante muy práctica: los modelos compartidos en repositorios abiertos pueden llevar malware, por ejemplo a través de formatos de serialización inseguros como los archivos *pickle* de Python.

MITRE ATLAS, la base de conocimiento de tácticas de ataque contra sistemas de IA, las recoge como técnicas separadas, entre ellas **AML.T0020 Poison Training Data**, **AML.T0019 Publish Poisoned Datasets** y **AML.T0018 Manipulate AI Model** ([MITRE ATLAS](https://atlas.mitre.org/)).

## Qué buscan los atacantes

La taxonomía de aprendizaje automático adversarial del NIST describe cuatro tipos de envenenamiento contra sistemas de IA predictiva:

1. **Envenenamiento de disponibilidad**: empeora el modelo en general y lo hace menos útil para todos.
2. **Envenenamiento dirigido**: cambia la respuesta del modelo solo para un pequeño grupo de entradas que interesan al atacante, como un producto, una persona o un tema.
3. **Envenenamiento con puerta trasera**: enseña al modelo a comportarse de otra forma cuando aparece un *disparador* concreto: una palabra, una frase, un patrón de píxeles.
4. **Envenenamiento del modelo**: se salta los datos y edita directamente los parámetros.

Las puertas traseras son las que más atención reciben porque son sigilosas. Un modelo con puerta trasera parece sano en cualquier evaluación normal. Solo el atacante, que conoce el disparador, puede activar el comportamiento oculto.

## Por qué los grandes modelos de lenguaje están expuestos

Los modelos de lenguaje actuales se entrenan con cantidades enormes de texto público. Durante un tiempo se pensó que esa escala era una protección: unas pocas páginas maliciosas quedarían ahogadas entre miles de millones de páginas buenas.

La investigación desde 2023 ha puesto en duda esa idea. Un equipo dirigido por Nicholas Carlini demostró que un atacante podría haber envenenado el 0,01 % de los datasets de imágenes LAION-400M o COYO-700M por unos **60 dólares**, simplemente comprando dominios caducados a los que esos datasets seguían apuntando ([Carlini et al., 2023](https://arxiv.org/abs/2302.10149)). En 2025, Anthropic, el UK AI Security Institute y el Alan Turing Institute comprobaron que unos **250 documentos envenenados** bastaban para plantar una puerta trasera sencilla en modelos de lenguaje de todos los tamaños que probaron, de 600 millones a 13.000 millones de parámetros ([lee nuestro resumen](@250-docs)).

Al mismo tiempo, la propia web se está moldeando pensando en el entrenamiento de la IA. Los investigadores han documentado redes de webs que publican millones de artículos de propaganda al año, aparentemente dirigidos menos a lectores humanos que a los rastreadores que alimentan los sistemas de IA ([ver LLM grooming](@grooming)).

## Envenenar no es lo mismo que inyectar prompts

La inyección de prompts esconde instrucciones dentro del contenido que el modelo lee *en el momento de responder*, como una web o un correo. El envenenamiento cambia lo que el modelo *aprendió* antes. Ambos pueden combinarse: entre los escenarios de ataque de OWASP figura un atacante que introduce datos engañosos mediante inyección de prompts aprovechando un filtrado insuficiente. Una variante más reciente, que MITRE ATLAS recoge como envenenamiento de memoria, usa enlaces preparados para escribir instrucciones en la memoria a largo plazo de un asistente ([The Hacker News, 2026](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html)).

## Qué pueden hacer los defensores

No hay una solución única, pero las principales líneas de defensa son conocidas: saber de dónde vienen los datos, comprobar que no han cambiado, probar los modelos en busca de comportamientos ocultos y vigilarlos en producción. Lo explicamos en detalle en [Cómo defenderse del envenenamiento de datos y modelos](@defend).

## Fuentes

- OWASP GenAI Security Project, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- NIST, [AI 100-2 E2025: Adversarial Machine Learning, a taxonomy and terminology of attacks and mitigations](https://csrc.nist.gov/news/2025/nist-ai-100-2-adversarial-machine-learning-taxonom), marzo de 2025
- MITRE, [base de conocimiento ATLAS](https://atlas.mitre.org/)
- Carlini et al., [Poisoning Web-Scale Training Datasets is Practical](https://arxiv.org/abs/2302.10149), 2023
- Anthropic, [A small number of samples can poison LLMs of any size](https://www.anthropic.com/research/small-samples-poison), octubre de 2025
