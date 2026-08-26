# LFM Encoders (Liquid AI)

LFM-2.5 and LFM-3.0 Encoders (including LFM2.5-Encoder-230M, LFM2.5-Encoder-350M, and LFM3.0-Encoder series) are high-speed, long-context bidirectional representation models developed by Liquid AI designed for classification, token-level representation, dense vector search, and agentic retrieval.

## What it is

LFM Encoders are state-of-the-art bidirectional representation models built by **Liquid AI**. Unlike standard encoders like BERT or RoBERTa that utilize pure multi-head self-attention, LFM Encoders are based on Liquid's hybrid **LFM architecture**. LFM interleaves gated short-convolution blocks with grouped-query attention (GQA). For encoder models, the causal autoregressive mask is completely removed and replaced with non-causal bidirectional attention, optimizing context-aware representation learning.

## What problem it solves

Standard transformer encoders (like RoBERTa or traditional dense embedding models) scale quadratically ($O(N^2)$) with context length. Consequently, processing long documents (such as entire code repositories, technical manuals, or legal contracts) becomes extremely slow, costly, and memory-intensive, especially on commoditized hardware.

LFM Encoders solve this problem by scaling linearly and gently up to a **16,384 token context window**. It enables document-scale natural language understanding (NLU), classification, and dense vector search to execute at high speed even on standard, non-GPU hardware like consumer CPUs.

## Where it fits in the stack

**Model Provider / Representation Layer**. It operates as the embedding or classification engine inside search indexers, RAG vector pipelines, and FastMCP 3.1 tool gateways, converting raw text into dense, context-aware embeddings for agentic networks driven by SOTA models like Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.

```
┌──────────────────────────────────────────────┐
│           Agent & MCP Orchestration          │
│       (Claude 5.6, GPT-5.6, FastMCP 3.1)     │
├──────────────────────────────────────────────┤
│         LFM ENCODER EMBEDDING ENGINE         │ (Bidirectional LFM Hybrid Backbone)
├──────────────────────────────────────────────┤
│     Vector DB / Index (Weaviate, Qdrant)     │
└──────────────────────────────────────────────┘
```

## Typical use cases

- **Long-Document Classification**: Categorizing multi-page contracts, scientific papers, or log bundles within a single execution pass.
- **Multilingual Search and Retrieval**: Powering vector search pipelines across 15+ supported languages (including English, Spanish, French, Arabic, Japanese, Chinese, and Hindi).
- **Masked Diffusion Text Generation**: Operating as a bidirectional backbone for non-autoregressive, parallel text generation.
- **Low-Power Server RAG**: Serving high-quality embeddings in offline local-office setups on minimal CPU servers.
- **FastMCP 3.1 Vector Tool Endpoints**: Providing embedding capabilities to FastMCP servers.

## Strengths

- **Hybrid LFM Backbone**: Interleaves gated short-convolutions with grouped-query attention for efficient feature extraction.
- **Exceptional CPU Performance**: Extremely fast long-context computation on CPU without requiring high-end graphics cards.
- **16,384 Token Context Window**: Reads large chunks of documents or source code without truncating context.
- **Multilingual Native**: Out-of-the-box support for major global languages.
- **Masked-Language Objective**: Pre-trained to capture deep bidirectional linguistic structures.

## Limitations

- **Not Generative (Autoregressive)**: Built strictly for token representation and embeddings; cannot be used for multi-turn conversational chat.
- **Ecosystem Maturity**: LFM architecture requires specific model configurations and runtime support compared to traditional pure transformers.

## When to use it

- When building local, CPU-based search engines or classification services that must parse long documents.
- In RAG architectures where context window boundaries exceed traditional 512-token encoder limits.
- When compiling embeddings across multiple languages on edge hardware.

## When not to use it

- If you need a standard generative conversational assistant (e.g. use Claude 5.6 or local models like Gemma 4).
- If your vector database requires specific, pre-built proprietary embeddings with no self-hosting support.

## Getting started

LFM Encoders can be loaded via Hugging Face.

```bash
# Install transformers and accelerate
pip install transformers accelerate torch
```

## CLI examples

```bash
# Pulling LFM Encoders using huggingface-cli
huggingface-cli download LiquidAI/LFM2.5-Encoder-350M

# Fine-tuning setup validation
python -c "import transformers; print(transformers.AutoConfig.from_pretrained('LiquidAI/LFM2.5-Encoder-350M'))"
```

## API examples

### Dense Text Embedding and Pydantic v2 Shape Validation
In search and categorization pipelines, verifying embedding shapes and data types before committing vectors to databases (like Weaviate, Qdrant, or Milvus) is essential. This example uses Pydantic v2 to validate encoder outputs.

```python
import numpy as np
from pydantic import BaseModel, Field, field_validator
from typing import List

class VectorEmbeddingRecord(BaseModel):
    document_id: str = Field(description="Unique hash of the encoded source text")
    text_snippet: str = Field(..., max_length=16384)
    embedding: List[float] = Field(..., description="Dense float array from the LFM encoder")
    language: str = Field(default="en")

    @field_validator("embedding")
    @classmethod
    def validate_embedding_dimensions(cls, v: List[float]) -> List[float]:
        expected_dims = 1024
        if len(v) != expected_dims:
            raise ValueError(f"Embedding dimension must be exactly {expected_dims}, got {len(v)}")
        return v

# Simulated generation of a dense embedding vector from LFM2.5-Encoder-350M
simulated_vector = np.random.normal(0.0, 1.0, 1024).tolist()

payload = {
    "document_id": "doc-lfm-88712",
    "text_snippet": "This is a long-context passage being processed by Liquid AI's LFM bidirectional hybrid model.",
    "embedding": simulated_vector,
    "language": "en"
}

# Validate with Pydantic v2
validated_record = VectorEmbeddingRecord(**payload)

print(f"Validated embedding for document: {validated_record.document_id}")
print(f"Vector dimension matches: {len(validated_record.embedding)} floats.")
```

## Related tools / concepts

- [Hugging Face Hub](../../tools/providers/huggingface.md) — Source repository hosting Liquid AI's weights.
- [Weaviate](../../tools/infrastructure/weaviate.md) — Vector database for storing long-context document embeddings.
- [Milvus](../../tools/infrastructure/milvus.md) — Large-scale similarity database optimized for dense embeddings.
- [RAG Pattern](../../knowledge_base/patterns/rag.md) — Operational workflow powering local searches.

## Sources / references

- [Liquid AI LFM Encoders Release Blog](https://huggingface.co/blog/LiquidAI/lfm2-5-encoders)
- [LiquidAI/LFM2.5-Encoder-350M on Hugging Face](https://huggingface.co/LiquidAI/LFM2.5-Encoder-350M)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
