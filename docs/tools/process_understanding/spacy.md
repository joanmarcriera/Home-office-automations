# spaCy

## What it is
spaCy is an open-source, industrial-strength Natural Language Processing (NLP) library written in Python and Cython. Designed specifically for production use, spaCy provides pre-trained statistical and transformer-based pipeline models for tokenization, part-of-speech (POS) tagging, named entity recognition (NER), dependency parsing, text classification, vector representations, and lemmatization across dozens of languages. In 2027, spaCy serves as a core, low-latency preprocessing and chunk-level linguistic extraction engine powering retrieval-augmented generation (RAG) pipelines, agent memory indexing, and structured data extraction workflows.

```
+-----------------------------------------------------------------------------------+
|                              SPACY NLP PROCESSING PIPELINE                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Input Document Text | ----> | Tokenizer             | ---> | Component Pipeline|
|  | Raw String          |       | (Cython Engine)       |      | (POS, NER, Parser)| |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | FastMCP 3.1 Gateway | <---- | FastMCP / Pydantic    | <--- | Processed Doc   | |
|  | Structured Output   |       | Schema Exporter       |      | Tokens & Spans  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Raw text ingestion into vector databases or LLM reasoning frameworks often suffers from poor chunking boundary detection, missing structural entity tags, and inefficient token utilization. Large language models (LLMs) are expensive and slow for simple grammatical parsing, dependency disambiguation, or rule-based entity matching. spaCy solves this by delivering sub-millisecond per-sentence processing, extracting linguistic structures, sentence boundaries, lemmatized tokens, and standard entities deterministically before passing optimized prompts or vectors into downstream agent workflows.

## Where it fits in the stack
**Process Understanding / Natural Language Processing & Text Preprocessing Engine**. spaCy operates directly at the ingestion and normalization layer, sitting between raw document input streams and downstream vector stores, LLM prompt builders, or knowledge graph extractors.

## Typical use cases
- **Semantic Sentence Segmentation**: Splitting long technical manuals or articles into grammatically intact sentence boundaries for optimal vector embedding chunking.
- **Entity Extraction & Masking**: Extracting named entities (organizations, locations, dates, persons) or redacting PII prior to transmitting text to external LLM providers.
- **Rule-Based Matcher Ingestion**: Running high-speed pattern matching across unstructured documents to discover domain-specific key phrases and API patterns.
- **Grammatical Dependency Filtering**: Analyzing subject-verb-object relationships to build accurate knowledge graphs and query expansion vectors.

## Strengths
- **Production Latency**: Built in Cython with memory management optimized for processing millions of tokens per second.
- **Extensible Pipeline Architecture**: Custom pipeline components can be attached seamlessly alongside pre-trained transformer backbones.
- **Multi-Language Support**: Pre-trained pipelines available for over 70 languages with unified API patterns.
- **Type-Safe Serialization**: Built-in support for msgpack and fast binary serialization (`DocBin`) across distributed execution clusters.

## Limitations
- **Fixed Model Vocabulary**: Standard statistical pipelines do not generalize to out-of-vocabulary domain terms without custom retraining or lookup matching.
- **GPU Overhead for Small Batches**: Heavy transformer backbones (`spacy-transformers`) require batched processing to maximize CUDA throughput effectively.

## When to use it
- When requiring deterministic, low-latency tokenization, lemmatization, dependency parsing, or standard NER.
- When preparing structured text chunks for RAG or Knowledge Graph indexing pipelines.
- When enforcing offline, on-premise NLP preprocessing without cloud API dependencies.

## When not to use it
- When zero-shot arbitrary entity recognition is needed on unseen complex classes (use [GLiNER](gliner.md) instead).
- When multi-page document layout OCR and visual formatting extraction is required (use [OpenDataLoader-PDF](opendataloader-pdf.md) or [Tika](../../services/tika.md)).

## Architecture & Technical Deep Dive

spaCy's processing pipeline revolves around the central `Language` class and a sequence of modular components applied to a centralized `Doc` object:

```
                          SPACY PIPELINE ARCHITECTURE

      Raw Input String ("spaCy runs fast on CPU and CUDA GPUs.")
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │     Tokenizer Engine     │
                     └────────────┬─────────────┘
                                  │
                                  ▼
                             ┌─────────┐
                             │   Doc   │ <--- Mutable Token Container
                             └────┬────┘
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
       ▼                          ▼                          ▼
┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│  tagger      │           │  parser      │           │  ner         │
│  (POS Tags)  │           │ (Dependency) │           │ (Entities)   │
└──────┬───────┘           └──────┬───────┘           └──────┬───────┘
       │                          │                          │
       └──────────────────────────┼──────────────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Annotated Doc   │
                         └─────────────────┘
```

1. **Tokenizer**: Converts raw text strings into an indexed `Doc` container of token offsets without mutating the underlying text.
2. **Pipeline Components**: Sequentially process the `Doc` object in-place, annotating token-level attributes (`token.pos_`, `token.dep_`, `doc.ents`).
3. **Cython Architecture**: Core data structures (`StringStore`, `Vocab`, `Doc`) reference 64-bit integer hashes, bypassing Python object creation overhead during loop iterations.

## Getting started

Install spaCy via PyPI and download a standard pre-trained language pipeline:

```bash
# Install spaCy
pip install spacy

# Download English medium pipeline model
python -m spacy download en_core_web_md
```

```python
import spacy

# Load installed model
nlp = spacy.load("en_core_web_md")

# Process unstructured text passage
text = "Apple released M4 Max chips in Cupertino while spaCy optimized Cython pipelines."
doc = nlp(text)

# Iterate over extracted entities
for ent in doc.ents:
    print(f"Entity: {ent.text:<18} Label: {ent.label_:<10}")

# Iterate over tokens with POS tags and lemmatization
for token in doc[:5]:
    print(f"Token: {token.text:<10} Lemma: {token.lemma_:<10} POS: {token.pos_}")
```

## CLI examples

```bash
# Evaluate pipeline performance on a test dataset
spacy evaluate en_core_web_md corpus/test.spacy

# Debug annotations and tokenization rules
spacy debug config config.cfg

# Package custom trained pipeline into a Python package
spacy package ./output/model_best ./packages --name custom_spacy_pipeline --version 1.0.0
```

## API examples

### FastMCP 3.1 Controller & Pydantic v2 Linguistic Analysis Engine
The following Python module wraps spaCy inside a **FastMCP 3.1** server with strict **Pydantic v2** schema validation.

```python
import os
import logging
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context
import spacy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spaCy-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("spacy-nlp-service")

# Lazy-loaded spaCy model container
_nlp_model = None

def get_nlp():
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("en_core_web_sm")
        except Exception:
            _nlp_model = spacy.blank("en")
    return _nlp_model

# Pydantic v2 Input Analysis Request Model
class NLPAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, max_length=15000, description="Raw text passage to analyze")
    extract_entities: bool = Field(default=True, description="Whether to extract named entities")
    extract_noun_chunks: bool = Field(default=False, description="Whether to extract noun phrases")

    @field_validator("text")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Input text cannot be blank")
        return s

@mcp.tool()
async def analyze_text_linguistics(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Processes text with spaCy to extract entities, sentence spans, and POS tokens.

    Args:
        request_dict: Dictionary matching NLPAnalysisRequest model.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating NLP request with Pydantic v2...")

    try:
        req = NLPAnalysisRequest.model_validate(request_dict)
        nlp = get_nlp()
        doc = nlp(req.text)

        entities = []
        if req.extract_entities and doc.has_annotation("ENT_IOB"):
            entities = [
                {"text": ent.text, "label": ent.label_, "start_char": ent.start_char, "end_char": ent.end_char}
                for ent in doc.ents
            ]

        sentences = [sent.text.strip() for sent in doc.sents] if doc.has_annotation("SENT_START") else [req.text]

        return {
            "status": "success",
            "token_count": len(doc),
            "sentence_count": len(sentences),
            "sentences": sentences,
            "entities": entities
        }
    except ValidationError as ve:
        logger.error(f"Validation failure: {ve}")
        raise ValueError(f"Invalid request parameters: {ve}")

@mcp.tool()
async def get_spacy_status(ctx: Optional[Context] = None) -> dict:
    """Queries currently loaded spaCy pipeline and language components."""
    nlp = get_nlp()
    return {
        "engine": "spaCy Industrial NLP",
        "pipeline_components": nlp.pipe_names,
        "lang": nlp.lang,
        "is_blank": len(nlp.pipe_names) == 0
    }

if __name__ == "__main__":
    mcp.run()
```

## Integration patterns
- **RAG Chunk Normalization Pipeline**: Use spaCy's sentence segmenter to guarantee syntactic integrity when splitting text for embedding into Weaviate or Qdrant.
- **Privacy Anonymization Guard**: Run `doc.ents` matching to redact `PERSON`, `ORG`, and `GPE` entities prior to serializing text into remote LLM completion endpoints.

## Best practices & Security
- **Pipeline Component Disabling**: Disable unneeded components (`nlp.select_pipes(disable=['parser', 'ner'])`) when performing simple tokenization to gain up to 10x throughput speedups.
- **Batch Processing**: Use `nlp.pipe(texts)` instead of processing documents in a single-item loop for parallelized CPU multi-threading.

## Reference implementation

```python
# Standalone test for spaCy Pydantic v2 validation schema
from pydantic import ValidationError

def test_spacy_schema():
    payload = {
        "text": "spaCy simplifies NLP in production environments.",
        "extract_entities": True,
        "extract_noun_chunks": False
    }
    req = NLPAnalysisRequest.model_validate(payload)
    assert req.extract_entities is True
    print("spaCy schema validation passed successfully.")

if __name__ == "__main__":
    test_spacy_schema()
```

## Related tools / concepts
- [GLiNER](gliner.md) — Zero-shot generalist entity extraction engine.
- [OpenDataLoader-PDF](opendataloader-pdf.md) — Document parsing and layout analysis engine.
- [Crawl4AI](crawl4ai.md) — Open-source LLM-friendly web crawler and scraper.
- [Tika](../../services/tika.md) — Apache Tika metadata and text extraction service.

## Sources / references
- [spaCy Official Documentation](https://spacy.io/?ref=2026-10-05-audit)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
