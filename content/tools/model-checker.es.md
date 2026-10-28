---
key: checker
slug: comprobador-modelos
title: Comprueba un modelo de Hugging Face antes de cargarlo
nav_title: Comprobador
description: Revisión gratuita de un modelo de Hugging Face: archivos pickle que ejecutan código, análisis, código propio, ficha, licencia y datos de entrenamiento.
h1: Comprueba un modelo antes de cargarlo
date: 2026-10-22
lead: Escribe un modelo de Hugging Face y verás si sus archivos pueden ejecutar código en tu equipo, qué han encontrado los análisis de Hugging Face y qué no cuenta su ficha.
---

## Qué comprueba

- **Los análisis del propio Hugging Face.** Hugging Face pasa los archivos que se suben por el antivirus ClamAV y enumera las importaciones que contienen los archivos pickle, resaltando las sospechosas ([documentación de Hugging Face](https://huggingface.co/docs/hub/security-pickle)). El comprobador muestra qué archivos han marcado.
- **Los formatos de archivo.** Un [archivo pickle](@glossary#pickle), y los formatos basados en pickle como los `.bin`, `.pt` y `.ckpt` de PyTorch, puede ejecutar código en cuanto se carga. [Safetensors](@glossary#safetensors), GGUF y ONNX guardan los pesos sin código. Los archivos de Keras pueden contener capas que ejecutan código, y su modo seguro ya se ha saltado alguna vez ([JFrog](https://jfrog.com/blog/keras-safe_mode-bypass-vulnerability/)).
- **El código propio.** Un modelo que necesita `trust_remote_code=True` ejecuta en tu equipo el código Python de su repositorio.
- **La ficha, la licencia y los datos de entrenamiento.** Saber de dónde vienen los datos de entrenamiento es la primera defensa contra el [envenenamiento](@what-is). Si la ficha no lo dice, conviene preguntar.
- **El modelo base.** Los ajustes finos, las versiones cuantizadas y las fusiones heredan lo que tenga el modelo del que salen, así que el comprobador enlaza a él.
- **La versión exacta.** Te da el commit que debes fijar, para que un cambio posterior en el repositorio no te afecte, y el [Package URL](https://github.com/package-url/purl-spec) (`pkg:huggingface/…`) para registrar el modelo en una [ML-BOM](@glossary#ml-bom).

## Qué no puede decirte

El comprobador mira lo que publica el repositorio, no lo que ha aprendido el modelo. Un modelo puede superar todas las comprobaciones y aun así llevar una [puerta trasera](@glossary#backdoor) introducida con sus datos de entrenamiento: en un estudio bastaron unos [250 documentos](@250-docs). Para detectarla hay que probar cómo se comporta el modelo, como se explica en la [lista de defensas](@defend#4-comprobar-que-ha-aprendido-el-modelo).

Los análisis de Hugging Face se hacen lo mejor posible y detectan patrones conocidos. Un análisis limpio es un indicio, no una prueba.

## Privacidad

La comprobación se hace en tu navegador. Al pulsar el botón, tu navegador consulta a la API pública de Hugging Face el modelo que has escrito. No se envía nada a este sitio ni se guarda nada. Hugging Face recibe la consulta como cualquier visita a su web, conforme a su propia [política de privacidad](https://huggingface.co/privacy).

El comprobador solo lee información pública. No puede ver modelos privados y, en los modelos con acceso restringido, muestra lo que Hugging Face enseña a cualquiera.
