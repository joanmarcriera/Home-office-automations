# LFM-2.5 Encoders

LFM-2.5 Encoders (specifically LFM2.5-Encoder-230M and LFM2.5-Encoder-350M) are high-speed, long-context bidirectional models from Liquid AI designed for classification, token-level representation, and search.

## What it is

LFM-2.5 Encoders are state-of-the-art bidirectional representation models built by **Liquid AI**. Unlike standard encoders like BERT or RoBERTa that utilize pure multi-head self-attention, LFM-2.5 is based on Liquid's hybrid **LFM2 architecture**. LFM2 interleaves gated short-convolution blocks with grouped-query attention (GQA). For the encoder models, the causal autoregressive mask is completely removed and replaced with bidirectional non-causal attention, optimizing representation learning.

## What problem it solves

Standard transformer encoders (like RoBERTa or modern dense embedding models) scale quadratically ($O(N^2)$) with context length. Consequently, processing long documents (such as whole code files or legal contracts) gets extremely slow, costly, and memory-intensive, especially on commoditized hardware.

LFM-2.5 Encoders solve this problem by scaling much more gently up to a **8,192 token context window**. It enables document-scale natural language understanding (NLU), classification, and dense vector search to run at high speed even on standard, non-GPU hardware like consumer CPUs.

## Where it fits in the stack

**Model Provider / Representation Layer**. It operates as the embedding or classification engine inside search indexers, RAG vector pipelines, and classification routers, converting raw text into dense, context-aware embeddings.

```
┌────────────────────────────────────────┐
│     Agentic Search & RAG Orchestrator   │
│         (Claude 5.1, FastMCP, n8n)     │
└───────────────────┬────────────────────┘
                    │ Raw Query / Document Content
┌───────────────────▼────────────────────┐
│         LFM-2.5 ENCODER ENGINE         │
└───────────────────┬────────────────────┘
                    │ Fast Bidirectional Vector Output (up to 8k tokens)
┌───────────────────▼────────────────────┐
│ Vector DB / Index (Weaviate, Milvus)   │
└────────────────────────────────────────┘
```

## Typical use cases

- **Long-Document Classification**: Categorizing multi-page contracts, scientific papers, or log bundles within a single execution pass.
- **Multilingual Search and Retrieval**: Powering vector search pipelines across 15 supported languages (including English, Spanish, French, Arabic, Japanese, Chinese, and Hindi).
- **Masked Diffusion Text Generation**: Operating as a bidirectional backbone for non-autoregressive, parallel text generation.
- **Low-Power Server RAG**: Serving high-quality embeddings in offline local-office setups on minimal CPU servers.

## Strengths

- **Hybrid LFM2 Backbone**: Interleaves gated short-convolutions with grouped-query attention for efficient feature extraction.
- **CPU Inference Performance**: Exceptionally fast long-context computation on CPU without requiring high-end graphics cards.
- **8,192 Token Context**: Seamlessly reads large chunks of documents or source code without truncating.
- **Multilingual Native**: Out-of-the-box support for 15 major languages.
- **Masked-Language Objective**: Fully pre-trained to capture deep bidirectional linguistic structures.

## Limitations

- **Not Generative (Autoregressive)**: Built strictly for token representation and embeddings; cannot be used for multi-turn chat generation (for that, use Liquid's generative LFMs).
- **Ecosystem Maturity**: LFM architecture requires specific model configurations and runtime support compared to traditional pure transformers.

## When to use it

- When you are building local, CPU-based search engines or classification services that must parse long documents.
- In RAG architectures where context window boundaries exceed the traditional 512-token encoder limits.
- When compiling embeddings across multiple languages on edge hardware.

## When not to use it

- If you need a standard generative conversational assistant (e.g. use Claude 5.1 or generative local models like Gemma 3).
- If your vector database requires specific, pre-built proprietary embeddings with no self-hosting support.

## Getting started

LFM-2.5 Encoders can be loaded via Hugging Face.

```bash
# Install transformers and accelerate
pip install transformers accelerate torch
```

## CLI examples

```bash
# Pulling LFM-2.5 Encoders using huggingface-cli
huggingface-cli download LiquidAI/LFM2.5-Encoder-350M

# Fine-tuning setup validation
python -c "import transformers; print(transformers.AutoConfig.from_pretrained('LiquidAI/LFM2.5-Encoder-350M'))"
```

## API examples

### Dense Text Embedding and Pydantic v2 Shape Validation
In search and categorization pipelines, verifying embedding shapes and data types before committing vectors to databases (like Weaviate or Milvus) is essential. This example uses Pydantic v2 to validate encoder outputs.

```python
import numpy as np
from pydantic import BaseModel, Field, field_validator
from typing import List

class VectorEmbeddingRecord(BaseModel):
    document_id: str = Field(description="Unique hash of the encoded source text")
    text_snippet: str = Field(..., max_length=8192)
    embedding: List[float] = Field(..., description="Dense float array from the LFM encoder")
    language: str = Field(default="en")

    @field_validator("embedding")
    @classmethod
    def validate_embedding_dimensions(cls, v: List[float]) -> List[float]:
        # Typical dense dimension for 350M model is 1024 (simulated here)
        expected_dims = 1024
        if len(v) != expected_dims:
            raise ValueError(f"Embedding dimension must be exactly {expected_dims}, got {len(v)}")
        return v

# Simulated generation of a dense embedding vector from LFM2.5-Encoder-350M
simulated_vector = np.random.normal(0.0, 1.0, 1024).tolist()

payload = {
    "document_id": "doc-lfm-88712",
    "text_snippet": "This is a long-context passage being processed by Liquid AI's LFM-2.5-350M bidirectional hybrid model.",
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
- [RAG Pattern](../../docs/knowledge_base/patterns/rag-pattern.md) — The operational workflow powering local searches.

## Sources / references

- [Liquid AI LFM-2.5 Encoders Release Blog](https://huggingface.co/blog/LiquidAI/lfm2-5-encoders)
- [LiquidAI/LFM2.5-Encoder-350M on Hugging Face](https://huggingface.co/LiquidAI/LFM2.5-Encoder-350M)

## Contribution Metadata

- Last reviewed: 2026-11-23
- Confidence: high
