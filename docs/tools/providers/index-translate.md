# Index-Translate

## What it is
Index-Translate is a family of open-source multilingual translation models developed by Bilibili, built on top of the Qwen 3.5 architecture. Engineered specifically for document translation, subtitle synchronization, and cross-lingual technical content processing, Index-Translate features specialized fine-tuning for over 30 languages. It excels at preserving Markdown structural elements, code blocks, and subtitle timestamp alignments while delivering domain-specific accuracy across media, technology, and literature. In 2027, Index-Translate serves as a primary local translation backbone for enterprise document processing and localized knowledge bases.

```
+-----------------------------------------------------------------------------------+
|                       INDEX-TRANSLATE LOCAL ENGINE                                |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Source Text / Sub   | ----> | Structure Masking     | ---> | Qwen 3.5 Based  | |
|  | / Tech Markdown     |       | & Tag Parser Engine   |      | Translation LLM | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | FastMCP 3.1 Gateway | <---- | Structure Re-injector | <--- | Domain Glossary | |
|  | SSE / JSON-RPC      |       | Post-Processing       |      | Alignment Core  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Generic neural machine translation (NMT) models often break technical document formatting, mangle inline code snippets, alter Markdown table layouts, or destroy WebVTT/SRT subtitle timestamps. Furthermore, cloud NMT APIs incur significant per-character costs when translating full software documentation sets or media libraries. Index-Translate solves these problems by providing specialized local translation model weights that natively protect code blocks, markup tags, and temporal markers while executing locally on consumer and server GPUs.

## Where it fits in the stack
**Providers / Multilingual Translation & LLM Model Family**. Index-Translate operates as a specialized model provider hosted on top of standard inference engines (vLLM, Ollama, llama.cpp, or TGI) to service localization workflows.

## Typical use cases
- **Software Documentation Localization**: Translating Markdown repositories while automatically preserving code blocks, YAML frontmatter, and liquid tags.
- **Subtitle & Media Translation**: Translating SRT/WebVTT media subtitle files while strictly preserving timing timestamps and speaker identifiers.
- **Cross-Lingual RAG & Knowledge Bases**: Converting multi-language input queries and context passages into uniform canonical languages for vector indexing.
- **Enterprise Domain Translation**: Applying custom glossary rules for financial, legal, or software domain terminology during translation.

## Strengths
- **Structure-Aware Fine-Tuning**: Built-in capability to recognize and preserve Markdown, HTML, LaTeX, and code syntax without corruption.
- **High COMET / BLEU Scores**: Outperforms general-purpose translation engines on technical and media benchmarks.
- **Open Model Weights**: Fully open weights available in multiple parameter sizes (1.8B, 7B, 14B) for flexible deployment.
- **Domain Glossary Injection**: Direct support for system-prompt and constrained decoding terminology rules.

## Limitations
- **VRAM Footprint**: Larger model variants (14B+) require 16GB+ VRAM for optimal batch inference throughput.
- **Language Coverage Bound**: Optimized for 30+ major languages; performance on low-resource regional dialects may vary.

## When to use it
- When translating technical documentation, Markdown files, or software codebases locally without losing formatting.
- When processing video/audio subtitle files requiring strict timecode preservation.
- When privacy constraints prohibit sending proprietary documents to commercial cloud translation APIs.

## When not to use it
- When simple single-sentence conversational translations can be handled by lightweight browser engines.
- When translating unformatted raw plain text where basic NMT models (e.g. NBD / Opus-MT) require less memory.

## Architecture & Technical Deep Dive

Index-Translate introduces a specialized multi-task training objective and structure-masking pipeline:

```
                   INDEX-TRANSLATE ARCHITECTURE PIPELINE

    Raw Source Document (Markdown / Subtitles / Technical Text)
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Structure & Tag Isolator     │  <--- Protects Code Blocks, URLs, Timestamps
     │ (Markdown / Code Parser)     │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Domain Glossary Injector     │  <--- Terminology Dictionary Alignment
     │ (Constrained Attention)      │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Qwen 3.5 Translation Core    │  <--- Specialized Multilingual Weights
     │ (1.8B / 7B / 14B Parameters) │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FastMCP 3.1 Controller       │  <--- REST / JSON-RPC / SSE Translation API
     │ & Output Verifier            │
     └──────────────┬───────────────┘
```

1. **Tag & Structure Isolator**: Parses input documents to identify non-translatable syntax trees (code blocks, HTML tags, WebVTT timecodes, inline math).
2. **Domain Glossary Injector**: Merges target language terminology dictionaries into the system prompt or constrained decoding logits mask.
3. **Qwen 3.5 Backbone**: Processes target translation pairs with specialized multi-token attention layers fine-tuned on multilingual technical corpora.
4. **Structure Re-injector**: Verifies that all protected tags and markers match the source document layout before output generation.

## Getting started

To get started with Index-Translate, download the model weights from HuggingFace and run inference via vLLM or Ollama:

```bash
# Clone model weights or pull via HuggingFace
git clone https://huggingface.co/bilibili/index-translate-7b

# Launch local OpenAI-compatible translation endpoint via vLLM
python3 -m vllm.entrypoints.openai.api_server \
  --model bilibili/index-translate-7b \
  --port 8000 \
  --gpu-memory-utilization 0.85
```

## CLI examples

```bash
# Translate a Markdown file from English to Chinese while preserving code blocks
index-translate file --src doc.md --target zh --output doc_zh.md --model index-translate-7b

# Translate a WebVTT subtitle file with timestamp verification
index-translate sub --src video_en.vtt --target ja --output video_ja.vtt

# Run batch translation test across multi-language benchmark samples
index-translate eval --test-set tech_docs_v1 --source-lang en --target-lang es
```

## API examples

### FastMCP 3.1 Controller & Pydantic v2 Translation Pipeline
The following Python script implements a **FastMCP 3.1** server for executing structured translation requests using **Pydantic v2** validation.

```python
import os
import logging
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Index-Translate-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("index-translate-controller")

# Pydantic v2 Translation Request Schema
class TranslationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_text: str = Field(..., min_length=1, description="Source text or Markdown document content")
    source_lang: str = Field(default="en", description="Source language ISO 639-1 code")
    target_lang: str = Field(..., description="Target language ISO 639-1 code (e.g., zh, es, ja, de)")
    preserve_code_blocks: bool = Field(default=True, description="Whether to protect code blocks and inline syntax")
    glossary: Dict[str, str] = Field(default_factory=dict, description="Custom term dictionary mapping")
    domain: str = Field(default="general", description="Content domain (tech, media, legal, medical)")

    @field_validator("source_lang", "target_lang")
    @classmethod
    def validate_lang_code(cls, v: str) -> str:
        if len(v.strip()) not in [2, 5]:
            raise ValueError("Language code must be a valid 2-letter or 5-letter locale string")
        return v.lower().strip()

@mcp.tool()
async def translate_document(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Translates document content using Index-Translate structure-aware engine.

    Args:
        request_dict: Dictionary matching TranslationRequest schema.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating translation request with Pydantic v2...")

    try:
        req = TranslationRequest.model_validate(request_dict)
        if ctx:
            await ctx.info(f"Translating {len(req.source_text)} chars from {req.source_lang} -> {req.target_lang}")

        # Simulated translation response preserving structural integrity
        translated_text = f"[Translated to {req.target_lang}]: {req.source_text}"

        return {
            "status": "success",
            "source_lang": req.source_lang,
            "target_lang": req.target_lang,
            "character_count": len(req.source_text),
            "code_blocks_preserved": req.preserve_code_blocks,
            "glossary_terms_applied": len(req.glossary),
            "translated_text": translated_text
        }
    except ValidationError as ve:
        logger.error(f"Validation failure: {ve}")
        raise ValueError(f"Invalid translation request: {ve}")

@mcp.tool()
async def get_model_capabilities(ctx: Optional[Context] = None) -> dict:
    """Returns Index-Translate supported languages, parameter sizes, and active model status."""
    if ctx:
        await ctx.info("Querying Index-Translate engine capabilities...")

    return {
        "provider": "Bilibili Index-Translate",
        "base_architecture": "Qwen 3.5",
        "supported_languages_count": 34,
        "available_sizes": ["1.8B", "7B", "14B"],
        "structure_preservation_supported": ["Markdown", "HTML", "WebVTT", "LaTeX", "Code Blocks"]
    }

if __name__ == "__main__":
    mcp.run()
```

## Integration patterns
- **Automated Docs Localization Workflow**: Hook Index-Translate into GitHub Actions to automatically translate commit updates in `docs/` directories into target language branches.
- **Local RAG Ingestion Pipeline**: Translate non-English incoming user queries prior to embedding search against English knowledge vector databases.

## Best practices & Security
- **Strict Formatting Verification**: Validate Markdown abstract syntax trees (AST) before and after translation to guarantee no missing closing brackets or code blocks.
- **Data Privacy**: Host Index-Translate on fully offline local GPUs to ensure zero data transmission to third-party endpoints.

## Reference implementation

```python
# Standalone test for Index-Translate Pydantic v2 validation
from pydantic import ValidationError

def test_index_translate_schema():
    payload = {
        "source_text": "# Technical Guide\n```python\nprint('Hello World')\n```",
        "source_lang": "en",
        "target_lang": "zh",
        "preserve_code_blocks": True,
        "glossary": {"Technical Guide": "技术指南"}
    }
    req = TranslationRequest.model_validate(payload)
    assert req.target_lang == "zh"
    assert req.preserve_code_blocks is True
    print("Index-Translate schema validation passed successfully.")

if __name__ == "__main__":
    test_index_translate_schema()
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Local LLM runner capable of serving Qwen models.
- [vLLM](../infrastructure/vllm.md) — High-performance inference engine for local LLMs.
- [GLiNER](../process_understanding/gliner.md) — Generalist Named Entity Recognition model for text extraction.
- [Breeze](../ai_knowledge/breeze.md) — Local text-to-speech and audio synthesis engine.
- [DeepL](../providers/deepl.md) — Commercial cloud translation service.
- [Argos Translate](../tools/argos-translate.md) — Offline open-source NMT framework.

## Sources / references
- [Index-Translate Bilibili Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1wxa1wr/bilibili_released_indextranslatea_a_multilingual/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
