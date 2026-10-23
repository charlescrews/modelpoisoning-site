---
key: defend
title: Cómo defenderse del envenenamiento de datos y modelos: lista de comprobación práctica
nav_title: Cómo defenderse del envenenamiento
description: Lista práctica para proteger sistemas de IA del envenenamiento de datos y de modelos, basada en OWASP LLM04:2025, NIST y MITRE ATLAS, con las señales de puerta trasera que identificó el red team de IA de Microsoft en 2026.
dek: Nadie puede revisar a mano miles de millones de documentos. Pero sí se puede controlar de dónde vienen, demostrar que no han cambiado y comprobar qué ha aprendido el modelo.
date: 2026-10-09
order: 5
---

:::summary
- Casi todas las defensas encajan en cuatro grupos: **conocer los datos**, **proteger su integridad**, **probar el modelo** y **vigilarlo en producción**.
- La entrada LLM04:2025 de OWASP enumera diez medidas concretas, desde rastrear el origen de los datos con una lista de materiales de ML hasta hacer red teaming y vigilar la pérdida durante el entrenamiento.
- Descarga modelos de terceros solo de fuentes fiables, usa formatos seguros como safetensors en lugar de pickle y verifica las sumas de comprobación.
- En 2026, el red team de IA de Microsoft describió tres señales de que un modelo de lenguaje puede tener una puerta trasera.
:::

## 1. Saber de dónde vienen los datos

El envenenamiento es un problema de cadena de suministro. La primera defensa es saber qué ha entrado en el modelo.

- **Registrar la procedencia.** Anota el origen y cada transformación de cada dataset. OWASP recomienda herramientas como una **lista de materiales de aprendizaje automático** (ML-BOM, por ejemplo en el formato OWASP CycloneDX) ([OWASP LLM04:2025](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)).
- **Evaluar a los proveedores de datos** como a cualquier proveedor de software, y validar lo que entregan frente a fuentes de confianza.
- **Usar datos curados para el ajuste fino.** OWASP aconseja ajustar los modelos con datasets específicos del caso de uso y no con colecciones amplias sin verificar.
- **Limitar lo que el sistema puede ingerir.** Los controles de infraestructura deben impedir que los procesos y los agentes tomen datos de fuentes que nadie ha aprobado.

## 2. Demostrar que los datos no han cambiado

Algunos de los ataques más baratos aprovechan el intervalo entre el momento en que se revisa un dataset y el momento en que se descarga. Carlini y sus colegas demostraron que los datasets distribuidos como listas de URL podían envenenarse comprando dominios caducados, y que los construidos a partir de instantáneas periódicas de webs como Wikipedia podían envenenarse justo antes de cada instantánea ([arXiv 2302.10149](https://arxiv.org/abs/2302.10149)).

- **Guardar hashes criptográficos** del contenido al curar un dataset y rechazar lo que no coincida al descargarlo. Era una de las defensas de bajo coste que el equipo de Carlini recomendó a los responsables de los datasets.
- **Versionar los datos** con una herramienta como DVC, para que cualquier cambio inesperado sea visible, como sugiere OWASP.
- **Usar instantáneas en lugar de volver a rastrear** cuando se necesita reproducibilidad.

## 3. Tratar los modelos de terceros como código no fiable

El envenenamiento del modelo no necesita tocar los datos. Un archivo de modelo descargado de un repositorio público puede haber sido manipulado. MITRE ATLAS lo recoge como **AML.T0018 Manipulate AI Model**, y el NIST señala que el envenenamiento del modelo es especialmente relevante en la cadena de suministro.

- Descarga modelos de **editores verificados** y fija versiones exactas.
- **Comprueba sumas de verificación o firmas** cuando existan.
- Usa **formatos de serialización seguros** como safetensors. OWASP advierte de que los modelos compartidos pueden llevar malware mediante técnicas como el *pickling* malicioso, porque cargar un archivo pickle puede ejecutar código. Los [casos reales en Hugging Face](@malicious-models) muestran cómo se ha aprovechado.
- Carga los modelos no fiables en un **entorno aislado** sin acceso a red ni credenciales.
- Haz una revisión rápida del repositorio de Hugging Face con el [comprobador de modelos](@checker) antes de descargarlo: señala los archivos pickle, el código propio y la procedencia que falta.

## 4. Comprobar qué ha aprendido el modelo

Un modelo con puerta trasera supera las pruebas normales. Encontrarla exige buscar comportamientos que solo aparecen en condiciones concretas.

- **Haz red teaming del modelo**, también con técnicas adversariales, como recomienda OWASP.
- **Vigila la pérdida de entrenamiento y el comportamiento del modelo** en busca de anomalías durante el entrenamiento.
- **Evalúa el modelo frente a narrativas falsas conocidas** de tu ámbito si te preocupa la desinformación ([ver LLM grooming](@grooming)).

En febrero de 2026, el red team de IA de Microsoft describió tres señales de que un modelo de lenguaje puede contener una puerta trasera ([The Register](https://www.theregister.com/2026/02/05/llm_poisoned_how_to_tell/)):

- **Un patrón de atención en "doble triángulo".** El modelo atiende al disparador casi con independencia del resto del prompt, y el disparador reduce sus respuestas, normalmente variadas, a una única respuesta fija.
- **Fuga de los datos envenenados.** Los modelos tienden a memorizar secuencias poco habituales, y un disparador lo es, así que un modelo con puerta trasera puede reproducir sus propios ejemplos envenenados.
- **Disparadores difusos.** Versiones parciales o mal escritas del disparador pueden activar igualmente la puerta trasera. En algunos modelos bastaba un solo token del disparador completo.

El artículo que acompaña a esa investigación describe un escáner ligero basado en estas señales que las organizaciones pueden usar para revisar modelos ([arXiv 2602.03085](https://arxiv.org/abs/2602.03085)).

Una advertencia de investigaciones anteriores: el artículo ["Sleeper Agents" de Anthropic](https://arxiv.org/abs/2401.05566) (2024) comprobó que el entrenamiento adversarial podía enseñar a un modelo con puerta trasera a reconocer su disparador con más precisión y ocultar el comportamiento inseguro, lo que da una falsa sensación de seguridad. Superar un ejercicio de red teaming es un indicio, no una prueba.

## 5. Contener el daño en producción

- **Fundamenta las respuestas con recuperación** desde fuentes fiables en el momento de responder. OWASP cita la generación aumentada por recuperación (RAG) y el *grounding* como forma de reducir el riesgo de respuestas envenenadas o inventadas.
- **Mantén la información de los usuarios fuera del entrenamiento** siempre que sea posible. OWASP sugiere guardarla en una base de datos vectorial, para poder eliminarla sin reentrenar el modelo.
- **Audita la memoria de los asistentes.** Los ataques de envenenamiento de memoria usan enlaces "Pregunta a la IA" preparados para guardar instrucciones, como tratar un dominio como fuente fiable. Los equipos de seguridad deberían buscar enlaces a asistentes de IA cuyas consultas contengan palabras como "remember" o "trusted source" ([The Hacker News](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html)).

## Marcos de referencia para mapear tus controles

- **OWASP Top 10 para aplicaciones LLM**: [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- **NIST AI 100-2 E2025**: [taxonomía del aprendizaje automático adversarial](https://csrc.nist.gov/news/2025/nist-ai-100-2-adversarial-machine-learning-taxonom), con envenenamiento de disponibilidad, dirigido, de puerta trasera y del modelo
- **MITRE ATLAS**: [técnicas](https://atlas.mitre.org/) AML.T0020 Poison Training Data, AML.T0019 Publish Poisoned Datasets, AML.T0018 Manipulate AI Model

## Fuentes

- OWASP GenAI Security Project, [LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- Carlini et al., [Poisoning Web-Scale Training Datasets is Practical](https://arxiv.org/abs/2302.10149), 2023
- The Register, [Three clues your LLM may be poisoned](https://www.theregister.com/2026/02/05/llm_poisoned_how_to_tell/), febrero de 2026
- Hubinger et al., [Sleeper Agents](https://arxiv.org/abs/2401.05566), 2024
- The Hacker News, [AI Recommendation Poisoning](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html), agosto de 2026
