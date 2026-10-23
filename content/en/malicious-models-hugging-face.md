---
key: malicious-models
title: Malicious models on Hugging Face: how a download can run code
nav_title: Malicious models on Hugging Face
description: Real cases from 2024 to 2026 of Hugging Face models that ran code or planted backdoors, why scanners miss some, and what to do before you load a model.
dek: Poisoning a model does not always mean touching its training data. Sometimes the file you download does the work the moment you open it.
date: 2026-10-23
order: 7
---

:::summary
- Model files saved with Python's **pickle** format, including PyTorch `.bin`, `.pt` and `.ckpt` files, can run code the moment they are loaded. Attackers have used this on Hugging Face to open remote access to the machines that loaded their models.
- The payload does not have to attack the computer. A technique called **Sleepy Pickle** changes the model itself as it loads, which can plant a backdoor that never appears in the stored weights.
- Scanners catch many malicious files but not all: in 2025, researchers showed both a broken pickle that slipped past Hugging Face's scanner and three flaws in the scanner itself.
- In May 2026, a fake OpenAI repository reached number one on Hugging Face's trending list. Its instructions told users to run a script that installed password-stealing malware.
- The defences are simple and cheap: prefer safetensors, pin the exact version, never run a repository's scripts unread, and keep loading tools up to date.
:::

## Why loading a model can run code

Python's [pickle](@glossary#pickle) format does not just store data. It stores instructions for rebuilding Python objects, and those instructions can name any function to call while the file is being loaded. A malicious file can therefore tell Python to run a shell command, download a program or open a network connection, and it does so before the model has produced a single output.

Many model files are pickles underneath. A PyTorch `.bin` or `.pt` file is a ZIP archive with a pickle inside it. Loading one with an old or misconfigured tool is, in effect, running a program written by whoever uploaded it.

## Real cases

### 2024: about a hundred models with real payloads

In February 2024, JFrog's security research team scanned PyTorch and TensorFlow Keras models on Hugging Face and reported "around 100 instances" of models with malicious functionality ([JFrog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)). In one, uploaded by an account called baller423, loading the model opened a reverse shell: a connection that gives a remote attacker a command line on the victim's machine. The repository has since been deleted.

### 2025: a broken file that the scanner skipped

In February 2025, ReversingLabs described two models on Hugging Face that it called **nullifAI** ([ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)). The files were compressed with 7z instead of the usual ZIP and the pickle inside was broken near its end. Picklescan, the open source tool Hugging Face used to inspect pickles, first checked whether a file was valid; these files failed the check, so the dangerous code was never flagged. Python, however, runs a pickle's instructions in order, so the malicious part at the start executed before the corruption caused an error. Hugging Face removed the models within 24 hours and updated Picklescan.

Later that year, JFrog reported three critical flaws in Picklescan itself that allowed malicious models to pass its checks undetected; they were fixed in version 0.0.31 ([Infosecurity Magazine](https://www.infosecurity-magazine.com/news/picklescan-flaws-expose-ai-supply)).

### 2026: a fake OpenAI release at number one

In May 2026, a repository called Open-OSS/privacy-filter copied the model card of a genuine OpenAI release almost word for word and reached number one on Hugging Face's trending list within 18 hours ([CSO Online](https://www.csoonline.com/article/4169407/malicious-hugging-face-model-masquerading-as-openai-release-hits-244k-downloads.html)). It showed about 244,000 downloads, figures that the security firm HiddenLayer, which found the malware, said were almost certainly inflated to make it look legitimate.

This attack did not need a malicious pickle. The README told users to run a script, `loader.py` or `start.bat`, which fetched and installed malware that stole browser passwords, cryptocurrency wallets and other data. Hugging Face removed the repository.

## When the payload targets the model itself

The cases above attack the computer. In 2024, Trail of Bits described a subtler use of the same weakness, which it called **Sleepy Pickle** ([Trail of Bits](https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-1/)). The malicious code runs when the file is loaded and modifies the model in memory: it can patch the weights to insert a [backdoor](@glossary#backdoor) or hook the model's methods to tamper with what goes in and comes out.

This is model poisoning without touching the training data. The weights stored in the file can look normal and pass a comparison with the original, because the change only exists once the model is running.

## The name you trust can change hands

Pulling a model by name, such as `author/model`, assumes that name always points to the same publisher. In September 2025, Palo Alto Networks' Unit 42 showed that this is not guaranteed ([Unit 42](https://unit42.paloaltonetworks.com/model-namespace-reuse/)). When an author or organisation is deleted from Hugging Face, its name can be registered again by anyone. An attacker who recreates a model path under an abandoned name can reach every pipeline that still downloads it by name. The researchers used this to get code execution on managed AI platforms run by Google and Microsoft.

## How common is it?

Hugging Face scans uploads with several tools, including its own and, since 2024, Protect AI's. By April 2025, Protect AI had scanned 4.47 million model versions in 1.41 million repositories and flagged 352,000 unsafe or suspicious issues across 51,700 models ([Hugging Face](https://huggingface.co/blog/pai-6-month)). Not every flagged issue is an attack, but the numbers show why the hub treats files as untrusted until scanned, and why you should too.

## What to do before you load a model

- **Prefer safe formats.** [Safetensors](@glossary#safetensors) and GGUF store weights without executable code. In the transformers library, `use_safetensors=True` makes sure those are the files that load.
- **If you must load a pickle-based file, restrict it.** `torch.load` only accepts plain weights by default since PyTorch 2.6 (`weights_only=True`). Keep PyTorch up to date: versions up to 2.5.1 had a flaw that allowed code execution even with that setting ([NVD, CVE-2025-32434](https://nvd.nist.gov/vuln/detail/CVE-2025-32434)).
- **Pin the exact version.** Download a specific commit with the `revision` parameter instead of whatever the name points to today. It protects against both later changes and namespace reuse.
- **Read before you run.** Never run a script because a model card tells you to, and read the Python files of any model that needs `trust_remote_code=True`.
- **Do not trust popularity.** Downloads, likes and trending positions can be inflated, as the fake OpenAI repository showed.
- **Load untrusted models in a sandbox** without network access or credentials, as recommended in the [defence checklist](@defend).

Our [model checker](@checker) does the first checks for you: it shows what Hugging Face's scanners flagged, which files use pickle, whether the model needs custom code, and the commit to pin.

## Sources

- JFrog, [Data Scientists Targeted by Malicious Hugging Face ML Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/), February 2024
- ReversingLabs, [RL identifies malware ML model hosted on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face), February 2025
- Infosecurity Magazine, [Critical PickleScan Vulnerabilities Expose AI Model Supply Chains](https://www.infosecurity-magazine.com/news/picklescan-flaws-expose-ai-supply), December 2025
- CSO Online, [Malicious Hugging Face model masquerading as OpenAI release hits 244K downloads](https://www.csoonline.com/article/4169407/malicious-hugging-face-model-masquerading-as-openai-release-hits-244k-downloads.html), May 2026
- Trail of Bits, [Exploiting ML models with pickle file attacks: Part 1](https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-1/), June 2024
- Unit 42, [Model Namespace Reuse](https://unit42.paloaltonetworks.com/model-namespace-reuse/), September 2025
- Hugging Face, [4M Models Scanned: Protect AI + Hugging Face 6 Months In](https://huggingface.co/blog/pai-6-month), April 2025
- NIST NVD, [CVE-2025-32434](https://nvd.nist.gov/vuln/detail/CVE-2025-32434)
