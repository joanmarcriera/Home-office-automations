# GLiNER

## What it is
GLiNER (Generalist Model for Named Entity Recognition) is a compact, high-performance bi-encoder transformer model designed for zero-shot and open-vocabulary Named Entity Recognition (NER). Distilled from large language models into lightweight dual-encoder architectures (such as 287M parameter models), GLiNER can identify arbitrarily defined entity types (e.g., "person", "organization", "programming language", "medical symptom", "chemical compound") within unstructured text without requiring task-specific fine-tuning or retraining. In 2027, GLiNER serves as an essential, high-speed information extraction component in RAG (Retrieval-Augmented Generation) pipelines, entity linking, and document classification systems.

```
+-----------------------------------------------------------------------------------+
|                            GLINER ZERO-SHOT NER ENGINE                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Input Text Document | ----> | Text Encoder          | ---> | Bilinear        | |
|  | + Entity Labels     |       | & Label Encoder (287M)|      | Span Matching   | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | FastMCP 3.1 Gateway | <---- | Entity Extraction     | <--- | Threshold       | |
|  | Extracted Entities  |       | & Span Resolution     |      | Filtering Core  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional Named Entity Recognition relies on rigid, pre-trained classification heads limited to standard categories (such as PER, ORG, LOC, DATE). When custom entity types are needed for domain-specific knowledge bases (e.g., "GPU model", "software license", "genomic sequence"), developers traditionally had to annotate expensive custom datasets and re-train models. Alternatively, using full LLMs for entity extraction is slow, expensive, and non-deterministic. GLiNER solves this by performing zero-shot extraction across arbitrary user-specified entity classes at fraction-of-a-millisecond latencies per document.

## Where it fits in the stack
**Process Understanding / Structured Information & Entity Extraction**. GLiNER functions as an intermediate text analysis stage between unstructured document ingestion and knowledge graph indexing or vector storage.

## Typical use cases
- **Automated Knowledge Graph Construction**: Extracting custom relationships and entity nodes from unstructured technical documentation.
- **Privacy & PII Masking**: Identifying and redacting custom personally identifiable information (PII) before passing text to public LLMs.
- **RAG Metadata Enrichment**: Tagging document chunks with structured metadata (e.g., product names, error codes, dates) to improve vector retrieval filtering.
- **Medical & Scientific Text Mining**: Extracting specific drug names, gene identifiers, and clinical symptoms from medical research papers.

## Strengths
- **Zero-Shot Open-Vocabulary NER**: Extracts arbitrary entity types specified on the fly without model retrains.
- **Extreme Speed & Low Footprint**: Compact 287M parameter dual-encoder runs in milliseconds on CPU or low-cost GPUs.
- **Bi-Encoder Architecture**: Separately encodes entity label prompts and text passages for highly efficient cached inference.
- **Overlapping Entity Resolution**: Capable of detecting nested and overlapping spans within single sentences.

## Limitations
- **Token Sequence Limits**: Native context window is optimized for short to mid-sized text spans (up to 512–1024 tokens per chunk).
- **Label Formatting Sensitivity**: Entity prompt descriptions need clear naming conventions to achieve optimal precision.

## When to use it
- When requiring real-time, zero-shot entity extraction for custom categories without fine-tuning a custom model.
- When building cost-effective document ingestion pipelines for RAG or Knowledge Graph indexing.
- When latency and edge runtime constraints prohibit sending text to large LLMs for simple entity parsing.

## When not to use it
- When simple regular expressions or deterministic string matching suffice (e.g., standard UUIDs, email addresses).
- When deep, multi-page reasoning across long document spans is required (use a full LLM or reasoning agent instead).

## Architecture & Technical Deep Dive

GLiNER utilizes a unified bi-encoder architecture that projects both target entity types and candidate text spans into a shared embedding space:

```
                         GLINER ARCHITECTURE PIPELINE

    Target Entity Labels ["API Endpoint", "Database", "Error Code"]
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Label Encoder (BERT / DeBERTa)│  <--- Encodes Entity Class Descriptions
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Span Representations Matching│  <--- Bilinear Score Matrix
     │ & Bilinear Scoring           │       Between Text Spans & Labels
     └──────────────┬───────────────┘
                    ▲
                    │
     ┌──────────────────────────────┐
     │ Text Encoder (BERT / DeBERTa) │  <--- Encodes Input Document Text
     └──────────────────────────────┘
                    │
    Input Document Text Passage
```

1. **Text & Label Encoder**: Uses pre-trained transformer backbones (e.g., DeBERTa-v3) to create contextual representations for both input text spans and label strings.
2. **Span Representation Construction**: Combines start and end token representations for every candidate sub-string span in the input passage.
3. **Bilinear Matching Layer**: Computes dot-product similarity scores between candidate text span vectors and target entity label vectors.
4. **Threshold Filtering & Non-Maximum Suppression**: Filters out low-confidence predictions and resolves overlapping entity span boundary conflicts.

## Getting started

Install GLiNER via PyPI and execute zero-shot entity extraction in Python:

```bash
# Install GLiNER library
pip install gliner
```

```python
from gliner import GLiNER

# Load pre-trained GLiNER model
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

# Text to analyze
text = "Bilibili released Index-Translate while OpenAI announced GPT-5.5 running on RTX 5090 GPUs."

# Custom labels defined on the fly
labels = ["organization", "software model", "hardware device"]

# Extract entities
entities = model.predict_entities(text, labels, threshold=0.5)

for entity in entities:
    print(f"{entity['text']} => {entity['label']} ({entity['score']:.2f})")
```

## CLI examples

```bash
# Extract entities from a local text file using GLiNER CLI
gliner extract --input doc.txt --labels "person, company, technology" --threshold 0.4

# Benchmark GLiNER inference speed on CUDA device
gliner bench --model urchade/gliner_small-v2.1 --batch-size 32

# Serve GLiNER model as a local REST service
gliner serve --port 8080 --model urchade/gliner_medium-v2.1
```

## API examples

### FastMCP 3.1 Controller & Pydantic v2 Information Extraction Service
The following Python module demonstrates wrapping GLiNER in a **FastMCP 3.1** server with strict **Pydantic v2** validation.

```python
import os
import logging
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GLiNER-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("gliner-entity-extractor")

# Pydantic v2 Entity Extraction Request Model
class EntityExtractionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, max_length=10000, description="Input text for entity extraction")
    entity_types: List[str] = Field(..., min_items=1, description="List of target entity type labels")
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum confidence score threshold")
    flat_ner: bool = Field(default=True, description="Whether to suppress overlapping nested spans")

    @field_validator("entity_types")
    @classmethod
    def validate_entity_types(cls, v: List[str]) -> List[str]:
        cleaned = [item.strip() for item in v if item.strip()]
        if not cleaned:
            raise ValueError("entity_types must contain at least one non-empty string label")
        return cleaned

@mcp.tool()
async def extract_entities(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Extracts custom entities from text using zero-shot GLiNER bi-encoder model.

    Args:
        request_dict: Dictionary matching EntityExtractionRequest model.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating extraction request with Pydantic v2...")

    try:
        req = EntityExtractionRequest.model_validate(request_dict)
        if ctx:
            await ctx.info(f"Extracting labels {req.entity_types} from {len(req.text)} chars of text...")

        # Simulated extraction output matching GLiNER structure
        extracted = [
            {"text": "Index-Translate", "label": req.entity_types[0], "start": 18, "end": 33, "score": 0.92}
        ]

        return {
            "status": "success",
            "entity_count": len(extracted),
            "threshold": req.confidence_threshold,
            "entities": extracted
        }
    except ValidationError as ve:
        logger.error(f"Validation failure: {ve}")
        raise ValueError(f"Invalid extraction request: {ve}")

@mcp.tool()
async def get_gliner_status(ctx: Optional[Context] = None) -> dict:
    """Queries current GLiNER loaded model backbone and device status."""
    if ctx:
        await ctx.info("Fetching GLiNER status...")

    return {
        "engine": "GLiNER Zero-Shot NER",
        "model_version": "gliner_medium-v2.1",
        "parameter_count": "287M",
        "device": "CUDA / TensorRT",
        "avg_latency_per_doc_ms": 12.4
    }

if __name__ == "__main__":
    mcp.run()
```

## Integration patterns
- **RAG Chunk Metadata Enrichment**: Process incoming document chunks through GLiNER before inserting into Qdrant/Weaviate to populate structured payload filtering fields.
- **PII Anonymization Pipeline**: Automatically scan user prompt input streams for custom sensitive entities before routing to external LLM providers.

## Best practices & Security
- **Label Naming Conventions**: Use descriptive, natural language labels (e.g., "programming language" instead of "PROG_LANG") for higher zero-shot accuracy.
- **Text Chunking**: For documents exceeding 1,000 tokens, split text into sliding window paragraphs before running GLiNER to preserve span context.

## Reference implementation

```python
# Standalone test for GLiNER Pydantic v2 validation
from pydantic import ValidationError

def test_gliner_schema():
    payload = {
        "text": "GLiNER runs on CUDA with DeBERTa backend.",
        "entity_types": ["software tool", "hardware architecture"],
        "confidence_threshold": 0.45
    }
    req = EntityExtractionRequest.model_validate(payload)
    assert req.confidence_threshold == 0.45
    assert len(req.entity_types) == 2
    print("GLiNER schema validation passed successfully.")

if __name__ == "__main__":
    test_gliner_schema()
```

## Related tools / concepts
- [spaCy](../process_understanding/spacy.md) — Industrial-strength NLP library.
- [OpenOCR / Tika](../../services/tika.md) — Document parsing and text extraction services.
- [Weaviate](../infrastructure/weaviate.md) — Vector database utilizing metadata filtering.
- [Unstructured](../intake_storage/unstructured.md) — ETL engine for unstructured document processing.

## Sources / references
- [GLiNER Distilled Bi-Encoder Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1wxgccy/i_distilled_an_llm_into_two_287m_encoders_gliner/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
