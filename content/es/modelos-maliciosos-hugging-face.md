---
key: malicious-models
title: Modelos maliciosos en Hugging Face: descargas que ejecutan código
nav_title: Modelos maliciosos en Hugging Face
description: Casos reales de 2024 a 2026 de modelos de Hugging Face que ejecutaban código o plantaban puertas traseras, por qué se escapan a los análisis y cómo protegerte.
dek: Envenenar un modelo no siempre exige tocar sus datos de entrenamiento. A veces el archivo que descargas hace el trabajo en cuanto lo abres.
date: 2026-10-23
order: 7
---

:::summary
- Los archivos de modelos guardados con el formato **pickle** de Python, como los `.bin`, `.pt` y `.ckpt` de PyTorch, pueden ejecutar código en cuanto se cargan. Hay atacantes que lo han usado en Hugging Face para abrir acceso remoto a los equipos que cargaban sus modelos.
- El código no tiene por qué atacar al ordenador. Una técnica llamada **Sleepy Pickle** modifica el propio modelo al cargarse, lo que permite plantar una puerta trasera que nunca aparece en los pesos guardados.
- Los análisis detectan muchos archivos maliciosos, pero no todos: en 2025 se demostró que un pickle roto esquivaba el análisis de Hugging Face y que la propia herramienta de análisis tenía tres fallos.
- En mayo de 2026, un repositorio que se hacía pasar por OpenAI llegó al número uno de tendencias de Hugging Face. Sus instrucciones pedían ejecutar un script que instalaba un programa para robar contraseñas.
- Las defensas son sencillas y baratas: usar safetensors, fijar la versión exacta, no ejecutar nunca los scripts de un repositorio sin leerlos y mantener al día las herramientas de carga.
:::

## Por qué cargar un modelo puede ejecutar código

El formato [pickle](@glossary#pickle) de Python no guarda solo datos. Guarda instrucciones para reconstruir objetos de Python, y esas instrucciones pueden indicar cualquier función que haya que llamar mientras se carga el archivo. Un archivo malicioso puede pedir a Python que ejecute un comando, descargue un programa o abra una conexión de red, y lo hace antes de que el modelo haya producido ni una sola respuesta.

Muchos archivos de modelos son pickles por dentro. Un `.bin` o un `.pt` de PyTorch es un archivo ZIP con un pickle dentro. Cargarlo con una herramienta antigua o mal configurada equivale a ejecutar un programa escrito por quien lo subió.

## Casos reales

### 2024: un centenar de modelos con código dañino real

En febrero de 2024, el equipo de investigación de seguridad de JFrog analizó modelos de PyTorch y de TensorFlow Keras en Hugging Face e informó de «alrededor de 100» modelos con funciones maliciosas ([JFrog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)). En uno de ellos, subido por una cuenta llamada baller423, cargar el modelo abría una *reverse shell*: una conexión que da a un atacante remoto una línea de comandos en el equipo de la víctima. El repositorio ya se ha borrado.

### 2025: un archivo roto que el análisis se saltaba

En febrero de 2025, ReversingLabs describió dos modelos de Hugging Face a los que llamó **nullifAI** ([ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)). Los archivos estaban comprimidos con 7z en lugar del ZIP habitual y el pickle de dentro estaba roto cerca del final. Picklescan, la herramienta de código abierto que usaba Hugging Face para revisar los pickles, comprobaba primero si el archivo era válido; estos no superaban esa comprobación, así que el código peligroso nunca se marcaba. Python, en cambio, ejecuta las instrucciones de un pickle en orden, de modo que la parte maliciosa del principio se ejecutaba antes de que la parte rota provocara un error. Hugging Face retiró los modelos en menos de 24 horas y actualizó Picklescan.

Ese mismo año, JFrog informó de tres fallos críticos en el propio Picklescan que permitían que modelos maliciosos pasaran sus comprobaciones sin ser detectados; se corrigieron en la versión 0.0.31 ([Infosecurity Magazine](https://www.infosecurity-magazine.com/news/picklescan-flaws-expose-ai-supply)).

### 2026: una falsa versión de OpenAI en el número uno

En mayo de 2026, un repositorio llamado Open-OSS/privacy-filter copió casi palabra por palabra la ficha de un lanzamiento real de OpenAI y llegó al número uno de tendencias de Hugging Face en 18 horas ([CSO Online](https://www.csoonline.com/article/4169407/malicious-hugging-face-model-masquerading-as-openai-release-hits-244k-downloads.html)). Mostraba unas 244.000 descargas, cifras que según la empresa de seguridad HiddenLayer, que descubrió el programa malicioso, estaban casi seguro infladas para que pareciera legítimo.

Este ataque no necesitó un pickle malicioso. El README pedía a los usuarios ejecutar un script, `loader.py` o `start.bat`, que descargaba e instalaba un programa que robaba contraseñas del navegador, monederos de criptomonedas y otros datos. Hugging Face retiró el repositorio.

## Cuando el ataque apunta al propio modelo

Los casos anteriores atacan al ordenador. En 2024, Trail of Bits describió un uso más sutil del mismo punto débil, al que llamó **Sleepy Pickle** ([Trail of Bits](https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-1/)). El código malicioso se ejecuta al cargar el archivo y modifica el modelo en memoria: puede cambiar los pesos para introducir una [puerta trasera](@glossary#backdoor) o interceptar los métodos del modelo para manipular lo que entra y lo que sale.

Es envenenamiento del modelo sin tocar los datos de entrenamiento. Los pesos guardados en el archivo pueden parecer normales y coincidir con los originales, porque el cambio solo existe cuando el modelo ya está funcionando.

## El nombre en el que confías puede cambiar de manos

Descargar un modelo por su nombre, como `autor/modelo`, da por hecho que ese nombre siempre apunta al mismo editor. En septiembre de 2025, Unit 42, de Palo Alto Networks, demostró que no está garantizado ([Unit 42](https://unit42.paloaltonetworks.com/model-namespace-reuse/)). Cuando se borra un autor u organización de Hugging Face, cualquiera puede volver a registrar su nombre. Un atacante que recrea la ruta de un modelo con un nombre abandonado llega a todos los procesos que todavía lo descargan por su nombre. Los investigadores lo usaron para ejecutar código en plataformas de IA gestionadas de Google y Microsoft.

## ¿Es muy frecuente?

Hugging Face analiza lo que se sube con varias herramientas, entre ellas las suyas propias y, desde 2024, las de Protect AI. En abril de 2025, Protect AI había analizado 4,47 millones de versiones de modelos en 1,41 millones de repositorios y había marcado 352.000 problemas inseguros o sospechosos en 51.700 modelos ([Hugging Face](https://huggingface.co/blog/pai-6-month)). No todos los problemas marcados son ataques, pero las cifras explican por qué la plataforma trata los archivos como no fiables hasta analizarlos, y por qué deberías hacer lo mismo.

## Qué hacer antes de cargar un modelo

- **Usa formatos seguros.** [Safetensors](@glossary#safetensors) y GGUF guardan los pesos sin código ejecutable. En la biblioteca transformers, `use_safetensors=True` garantiza que se cargan esos archivos.
- **Si tienes que cargar un archivo basado en pickle, restríngelo.** Desde PyTorch 2.6, `torch.load` solo acepta pesos por defecto (`weights_only=True`). Mantén PyTorch actualizado: hasta la versión 2.5.1 había un fallo que permitía ejecutar código incluso con esa opción ([NVD, CVE-2025-32434](https://nvd.nist.gov/vuln/detail/CVE-2025-32434)).
- **Fija la versión exacta.** Descarga un commit concreto con el parámetro `revision` en lugar de lo que apunte hoy el nombre. Te protege tanto de cambios posteriores como de la reutilización de nombres.
- **Lee antes de ejecutar.** No ejecutes nunca un script porque lo diga la ficha de un modelo, y lee los archivos Python de cualquier modelo que necesite `trust_remote_code=True`.
- **No te fíes de la popularidad.** Las descargas, los «me gusta» y los puestos en tendencias se pueden inflar, como demostró el falso repositorio de OpenAI.
- **Carga los modelos no fiables en un entorno aislado**, sin red ni credenciales, como recomienda la [lista de defensas](@defend).

Nuestro [comprobador de modelos](@checker) hace las primeras comprobaciones por ti: muestra lo que han marcado los análisis de Hugging Face, qué archivos usan pickle, si el modelo necesita código propio y qué commit debes fijar.

## Fuentes

- JFrog, [Data Scientists Targeted by Malicious Hugging Face ML Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/), febrero de 2024
- ReversingLabs, [RL identifies malware ML model hosted on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face), febrero de 2025
- Infosecurity Magazine, [Critical PickleScan Vulnerabilities Expose AI Model Supply Chains](https://www.infosecurity-magazine.com/news/picklescan-flaws-expose-ai-supply), diciembre de 2025
- CSO Online, [Malicious Hugging Face model masquerading as OpenAI release hits 244K downloads](https://www.csoonline.com/article/4169407/malicious-hugging-face-model-masquerading-as-openai-release-hits-244k-downloads.html), mayo de 2026
- Trail of Bits, [Exploiting ML models with pickle file attacks: Part 1](https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-1/), junio de 2024
- Unit 42, [Model Namespace Reuse](https://unit42.paloaltonetworks.com/model-namespace-reuse/), septiembre de 2025
- Hugging Face, [4M Models Scanned: Protect AI + Hugging Face 6 Months In](https://huggingface.co/blog/pai-6-month), abril de 2025
- NIST NVD, [CVE-2025-32434](https://nvd.nist.gov/vuln/detail/CVE-2025-32434)
