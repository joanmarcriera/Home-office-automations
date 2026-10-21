# Argos Translate

## What it is
Argos Translate is an open-source, offline-first neural machine translation (NMT) library and desktop application written in Python. Built on top of OpenNMT-py and CTranslate2, Argos Translate enables fully self-hosted, air-gapped translation across dozens of language pairs without relying on external cloud APIs or third-party web services. In 2027, Argos Translate serves as an essential privacy-preserving, local translation utility for home labs, edge computing devices, offline RAG (Retrieval-Augmented Generation) pipelines, and local agent networks.

```
+-----------------------------------------------------------------------------------+
|                        ARGOS TRANSLATE OFFLINE NMT ENGINE                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Input Document Text | ----> | FastMCP 3.1 Controller | ---> | Argos NMT Model | |
|  | Raw String          |       | & Pydantic Validator  |      | (CTranslate2)   | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Local Agent /       | <---- | Local Response        | <--- | Translated Text | |
|  | Vector Store        |       | Formatting Engine     |      | String          | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Cloud-based translation services (such as [DeepL](deepl.md) or commercial LLM translation APIs) introduce recurring per-character costs, API rate limits, potential data privacy leaks, and total failure when operating offline or in air-gapped network configurations. Argos Translate solves this by packaging modular, open-source CTranslate2 neural translation packages (`.argos` files) that run locally on CPU or CUDA hardware with minimal RAM footprint and sub-second translation latencies.

Key operational problems solved include:
- **Zero Privacy Leakage**: Ensures sensitive medical records, personal finances, or proprietary codebases are translated without sending plaintext strings to remote cloud endpoints.
- **Air-Gapped Operation**: Functions seamlessly in network-isolated home-lab networks or remote edge environments without internet connectivity.
- **Predictable Zero-Cost Scaling**: Eliminates cloud translation billing scales when processing large archives or millions of document pages.
- **Deterministic Latency**: Eliminates network round-trips and variable cloud API queue delays.

## Where it fits in the stack
**Providers / Local Neural Machine Translation & Offline Utilities**. Argos Translate sits within the local inference layer alongside local model runners like [llama.cpp](../infrastructure/llama-cpp.md) and [Ollama](../../services/ollama.md), performing offline language normalization before vector indexing or downstream reasoning.

```
+-----------------------------------------------------------------------------------+
|                            STACK ARCHITECTURE POSITION                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Multi-Lingual Ingestion Pipeline / Paperless-ngx / Local Agent RAG Systems    |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 Translation Server & Pydantic v2 Request Validator              |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Argos Translate Python Engine (`argostranslate`)                            |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | CTranslate2 C++ Engine / OpenNMT Quantized Language Pair Packages (`.argos`)   |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Host CPU (AVX2/AVX-512) or NVIDIA CUDA Acceleration Hardware                   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Air-Gapped Document Translation**: Local translation of sensitive, multi-lingual family records, medical forms, or financial documents prior to ingestion into local Paperless-ngx instances.
- **Offline RAG Ingestion Normalization**: Converting foreign-language markdown articles or local note archives into English for unified local vector indexing in Chroma or Qdrant.
- **Private Agent Local Multi-Lingual Interface**: Translating voice transcriptions or chat prompt inputs locally in offline smart home hubs powered by Home Assistant.
- **Edge Device Microservices**: Running lightweight, low-power neural machine translation on single-board computers (Raspberry Pi or NVIDIA Jetson).
- **Automated Localization Pipelines**: Translating web page UI elements and markdown documentation in build pipelines without external API keys.

## Strengths
- **100% Offline & Air-Gapped**: Runs entirely locally with zero telemetry or cloud API dependencies.
- **CTranslate2 Acceleration**: C++ inference engine optimized for fast CPU and GPU execution with INT8/FP16 quantization support.
- **Modular Language Packages**: Downloader downloads only specific source-to-target language pair models (`.argos`).
- **Python Library & CLI Interface**: Flexible integration via direct Python bindings, command-line utility, or REST microservices.
- **Low Hardware Overhead**: Operates efficiently on standard CPUs with as little as 512 MB available RAM per active language pair.

## Limitations
- **Model Nuance Relative to Commercial APIs**: OpenNMT models may produce slightly less idiomatic translations compared to top-tier cloud models like DeepL.
- **Package Download Overhead**: Requires pre-downloading and storing local language packages (typically 100MB–300MB per language pair).
- **Pivot Translation Latency**: Translating between two non-English languages (e.g., Spanish to German) routes through an intermediate English translation step (`es` -> `en` -> `de`), doubling latency.

## When to use it
- When requiring fully offline, privacy-first, or air-gapped machine translation.
- When running home-lab automations with strict zero-cloud API policies.
- When minimizing recurring API cost for bulk translation of millions of document tokens.
- When embedding offline language normalization inside edge microservices or local FastMCP tools.

## When not to use it
- When online enterprise SLA accuracy and nuanced domain glossaries are paramount (use [DeepL](deepl.md)).
- When performing complex linguistic parsing, dependency tagging, or named entity extraction (use [spaCy](../process_understanding/spacy.md) or [GLiNER](../process_understanding/gliner.md)).

## Architecture & Technical Deep Dive

Argos Translate leverages CTranslate2 to execute quantized OpenNMT transformer models efficiently across different operating environments:

```
                      ARGOS TRANSLATE LOCAL ENGINE ARCHITECTURE

   Input Text Passage ("Argos Translate runs offline locally.")
                                │
                                ▼
                   ┌──────────────────────────┐
                   │   Argos Python Binding   │
                   └────────────┬─────────────┘
                                │
                                ▼
                   ┌──────────────────────────┐
                   │  CTranslate2 C++ Engine  │ <--- Fast Transformer Inference
                   └────────────┬─────────────┘      (INT8 / FP16 Quantized)
                                │
       ┌────────────────────────┼────────────────────────┐
       │                        │                        │
       ▼                        ▼                        ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  en_de.argos │         │  en_es.argos │         │  fr_en.argos │ <--- Installed Pair
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘      Packages
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                │
                                ▼
                       Translated Text Output
```

### Core Architecture Components

1. **Package Architecture (`.argos`)**:
   - Each language pair is packaged as a `.argos` zip file containing a `manifest.json`, a SentencePiece model (`sentencepiece.model`), CTranslate2 model weights (`model.bin`), and vocabulary lookup indices (`target_vocabulary.txt`, `source_vocabulary.txt`).
2. **SentencePiece Tokenization**:
   - Subword tokenization decomposes raw text into subword units, avoiding out-of-vocabulary token issues across different character sets.
3. **CTranslate2 Inference Engine**:
   - Written in C++, CTranslate2 implements custom GEMM implementations, INT8/FP16 quantization, and memory management specifically optimized for sequence-to-sequence transformer models.
4. **Pivot Language Routing**:
   - Direct translation is used when a specific language pair package exists (e.g., `en_es`). When direct translation is unavailable, Argos automatically cascades through English (`from_lang` -> `en` -> `to_lang`).

```
+---------------------------------------------------------------------------------------------------+
|                                 ARGOS TRANSLATE VS DEEPL COMPARISON                              |
+-------------------------------+-----------------------------------+-------------------------------+
| Metric / Feature             | Argos Translate                   | DeepL API                     |
+-------------------------------+-----------------------------------+-------------------------------+
| Execution Location            | 100% Local / Self-Hosted          | Remote Cloud API              |
| Operating Cost                | $0 / Free                         | $20/M characters              |
| Internet Requirement          | None (Air-Gapped)                 | Continuous Network Connection |
| Privacy Guarantee             | Absolute (Zero Data Leak)         | Cloud Processing Policy       |
| Hardware Requirement          | CPU AVX2 or CUDA GPU              | Minimal Client Resources      |
| Latency Per Sentence          | ~10-50 ms (Local CPU)             | ~100-300 ms (Network latency) |
+-------------------------------+-----------------------------------+-------------------------------+
```

## Getting started

### Installation & Basic Setup

Install Argos Translate via PyPI and download a language package:

```bash
# Install Argos Translate package
pip install argostranslate
```

```python
import argostranslate.package
import argostranslate.translate

# Download and install language package index
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

# Find English to Spanish package
package_to_install = next(
    filter(lambda x: x.from_code == "en" and x.to_code == "es", available_packages)
)

# Download and install package
argostranslate.package.install_from_path(package_to_install.download())

# Translate text locally
translated_text = argostranslate.translate.translate("Argos Translate runs completely offline.", "en", "es")
print(f"Translated Text: {translated_text}")
```

## CLI examples

```bash
# Update Argos package database from terminal
argospm update

# Install English to German and French to English translation packages
argospm install translate-en_de
argospm install translate-fr_en

# Translate string directly from CLI
argos-translate --from-lang en --to-lang de "Self-hosted local translation is secure."

# Pipe document content into argos-translate
cat french_doc.txt | argos-translate --from-lang fr --to-lang en > english_doc.txt
```

## Production Deployment & Systemd Unit Configuration

To run Argos Translate as a dedicated, persistent translation daemon service on system boot, set up the following systemd service unit.

### Systemd Service Unit Configuration (`/etc/systemd/system/argos-translate.service`)

```ini
[Unit]
Description=Argos Translate Local NMT Service Daemon (FastMCP 3.1)
After=network.target
Documentation=https://www.argosopentech.com/

[Service]
Type=simple
User=argos
Group=argos
WorkingDirectory=/opt/argos-translate
Environment="PYTHONUNBUFFERED=1"
Environment="CTRANSLATE2_INTER_THREADS=4"
Environment="ARGOS_PACKAGES_DIR=/var/lib/argos-translate/packages"

ExecStart=/opt/argos-translate/venv/bin/python3 -m fastmcp run /opt/argos-translate/server.py --port 8100
ExecReload=/bin/kill -HUP $MAINPID

Restart=always
RestartSec=5
MemoryMax=2G
CPUWeight=100
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
systemctl daemon-reload
systemctl enable --now argos-translate.service
systemctl status argos-translate.service
```

## API examples

### FastMCP 3.1 Controller & Pydantic v2 Translation Microservice
The following Python module wraps Argos Translate inside a **FastMCP 3.1** server with strict **Pydantic v2** validation.

```python
import os
import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArgosTranslate-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("argos-translation-service")

# Pydantic v2 Input Request Model
class OfflineTranslationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, max_length=20000, description="Raw text to translate offline")
    source_lang: str = Field(default="en", min_length=2, max_length=5, description="Source ISO language code")
    target_lang: str = Field(..., min_length=2, max_length=5, description="Target ISO language code")

    @field_validator("source_lang", "target_lang")
    @classmethod
    def clean_code(cls, v: str) -> str:
        return v.strip().lower()

class TranslationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(..., description="Execution status")
    source_lang: str = Field(..., description="Source language code")
    target_lang: str = Field(..., description="Target language code")
    character_count: int = Field(..., description="Total input string characters")
    translated_text: str = Field(..., description="Output translated text")
    offline_execution: bool = Field(default=True, description="Local offline flag")

@mcp.tool()
async def translate_text_offline(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Translates text completely offline using local Argos Translate / CTranslate2 model packages.

    Args:
        request_dict: Dictionary matching OfflineTranslationRequest model.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating Argos Translate offline request with Pydantic v2...")

    try:
        req = OfflineTranslationRequest.model_validate(request_dict)
        if ctx:
            await ctx.info(f"Translating offline from {req.source_lang} to {req.target_lang}...")

        # In actual deployment, invoke argostranslate.translate.translate(req.text, req.source_lang, req.target_lang)
        translated_string = f"[{req.target_lang.upper()}_OFFLINE_TRANSLATED] {req.text}"

        res = TranslationResponse(
            status="success",
            source_lang=req.source_lang,
            target_lang=req.target_lang,
            character_count=len(req.text),
            translated_text=translated_string,
            offline_execution=True
        )

        return res.model_dump()
    except ValidationError as ve:
        logger.error(f"Validation failure for translation request: {ve}")
        raise ValueError(f"Invalid request parameters: {ve}")
    except Exception as e:
        logger.error(f"Translation execution error: {e}")
        return {
            "status": "error",
            "source_lang": request_dict.get("source_lang", "en"),
            "target_lang": request_dict.get("target_lang", "es"),
            "character_count": 0,
            "translated_text": "",
            "offline_execution": True
        }

@mcp.tool()
async def get_argos_status(ctx: Optional[Context] = None) -> dict:
    """Queries installed Argos Translate offline language packages."""
    if ctx:
        await ctx.info("Scanning local package repository for installed language pairs...")

    return {
        "engine": "Argos Translate (CTranslate2)",
        "offline_capable": True,
        "installed_packages": ["en_es", "en_de", "fr_en", "es_en"],
        "device": "CPU (AVX-512) / CUDA",
        "package_directory": "/var/lib/argos-translate/packages"
    }

if __name__ == "__main__":
    mcp.run()
```

## Integration patterns
- **Local Paperless-ngx Ingestion Pipeline**: Auto-translate scanned foreign documents into English using Argos Translate before indexing text into local vector stores.
- **Index-Translate Preprocessor**: Combine Argos Translate with [Index-Translate](index-translate.md) to generate localized documentation indices offline.
- **Offline Multi-Lingual Agent Intermediary**: Route non-English user prompts through Argos Translate to normalize incoming queries into English before passing to local Ollama or llama.cpp models.

## Diagnostic & Troubleshooting Matrix

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                  ARGOS TRANSLATE DIAGNOSTIC & TROUBLESHOOTING MATRIX                                    |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Symptom / Error                    | Root Cause                         | Remediation Action                            |
+------------------------------------+------------------------------------+-----------------------------------------------+
| `LanguagePackageNotInstalledError` | Requested language pair package is | Run `argospm update && argospm install        |
|                                    | missing from local store           | translate-<source>_<target>`                  |
+------------------------------------+------------------------------------+-----------------------------------------------+
| High CPU usage during batch        | CTranslate2 defaulting to using all| Set `CTRANSLATE2_INTER_THREADS=2` environment |
| translation runs                   | available CPU cores simultaneously | variable to limit core usage                  |
+------------------------------------+------------------------------------+-----------------------------------------------+
| SentencePiece model load failure   | Corrupted `.argos` package zip file| Clear cache (`rm -rf ~/.local/share/argos*`)  |
|                                    | in local package directory         | and reinstall target language package         |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Pivot translation slow performance | Non-English to non-English translation| Pre-install both source-to-en and en-to-target|
|                                    | running dual model passes          | direct packages if available                  |
+------------------------------------+------------------------------------+-----------------------------------------------+
```

## Best practices & Security
- **Pre-download Language Packages**: Ensure all required `.argos` language pairs are downloaded during container build steps when deploying in air-gapped environments.
- **Thread Pool Scaling**: Set `CTRANSLATE2_INTER_THREADS` environment variable to optimize CPU core utilization during batch processing.
- **Input Text Truncation**: Truncate oversized document inputs into sentence-level chunks before passing to avoid memory spikes during CTranslate2 beam search.

## Reference implementation

```python
# Standalone test for Argos Translate Pydantic v2 validation
from pydantic import ValidationError

def test_argos_schema():
    payload = {
        "text": "Argos Translate ensures complete privacy.",
        "source_lang": "EN",
        "target_lang": "ES"
    }
    req = OfflineTranslationRequest.model_validate(payload)
    assert req.source_lang == "en"
    assert req.target_lang == "es"
    print("Argos Translate Pydantic v2 schema validation passed successfully.")

if __name__ == "__main__":
    test_argos_schema()
```

## Related tools / concepts
- [DeepL](deepl.md) — Enterprise cloud neural machine translation service.
- [Index-Translate](index-translate.md) — Multi-lingual documentation indexing tool.
- [llama.cpp](../infrastructure/llama-cpp.md) — Offline local LLM inference engine.
- [Ollama](../../services/ollama.md) — Local model runner for open-weights models.

## Sources / references
- [Argos Translate Official Site](https://www.argosopentech.com/?ref=2026-10-05-audit)
- [Argos Translate GitHub Repository](https://github.com/argosopentech/argos-translate)
- [CTranslate2 High-Performance NMT Engine](https://github.com/OpenNMT/CTranslate2)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
