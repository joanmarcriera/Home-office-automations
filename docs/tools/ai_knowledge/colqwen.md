# ColQwen / ColPali Engine

## What it is
ColQwen is a series of multi-modal document retrieval models (part of the **ColPali** ecosystem) based on the Qwen architecture (Qwen2-VL, Qwen2.5-VL, Qwen3-VL). It leverages the **ColBERT** (Contextualized Late Interaction over BERT) strategy to provide high-performance retrieval across text and visual document elements by representing documents as multi-vector embeddings of image patches.

## What problem it solves
Traditional text-only retrieval fails on documents with heavy visual components like charts, tables, and diagrams. ColQwen removes the need for brittle OCR and layout recognition pipelines by directly understanding the visual representation of a document page.

## Where it fits in the stack
**Multi-modal Retrieval / RAG Engine**. It is a specialized model used for the "Retrieval" part of Vision-RAG (V-RAG) pipelines, sitting between the raw data storage and the LLM generation layer.

## Typical use cases
- **Visual Document RAG**: Searching and retrieving information from scanned PDFs, manuals, and reports with complex layouts.
- **Enterprise Search**: Building knowledge bases that include technical drawings, financial charts, and slide decks.
- **Interpretability**: Using similarity maps to visualize which parts of a document image contributed to a specific retrieval result.

## Getting started

### Installation
The `colpali-engine` provides the core implementation for ColQwen and ColPali models:

```bash
pip install colpali-engine
```

### Basic Inference Example
```python
import torch
from PIL import Image
from colpali_engine.models import ColQwen2, ColQwen2Processor

model_name = "vidore/colqwen2-v1.0"
model = ColQwen2.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
).eval()

processor = ColQwen2Processor.from_pretrained(model_name)

# Process image and query
image = Image.new("RGB", (128, 128), color="white")
query = "Show me the growth chart for Q3"

batch_images = processor.process_images([image]).to(model.device)
batch_queries = processor.process_queries([query]).to(model.device)

# Generate embeddings
with torch.no_grad():
    image_embeddings = model(**batch_images)
    query_embeddings = model(**batch_queries)

# Calculate similarity score
scores = processor.score_multi_vector(query_embeddings, image_embeddings)
```

## Advanced Features (May 2026)

### Token Pooling
To address the high storage requirements of multi-vector embeddings, ColQwen supports **Hierarchical Token Pooling**. This reduces the embedding sequence length by up to 66% while retaining over 97% of retrieval performance by merging redundant patches (e.g., white space).

### Interpretability Maps
ColQwen allows for the generation of **Similarity Maps**, which can be superimposed on the original document image to show exactly where the model "looked" to satisfy a query.

```python
from colpali_engine.interpretability import get_similarity_maps_from_embeddings
# Generate maps for visualization
similarity_maps = get_similarity_maps_from_embeddings(
    image_embeddings=image_embeddings,
    query_embeddings=query_embeddings,
    n_patches=processor.get_n_patches(image.size),
    image_mask=processor.get_image_mask(batch_images)
)
```

### Fast Matching with Plaid
Experimental support for **fast-plaid** enables quicker matching across large corpora, significantly reducing the latency traditionally associated with late interaction models.

## Model Variants (May 2026 Baseline)
- **vidore/colqwen2-v1.0**: High-performance Apache 2.0 variant.
- **vidore/colqwen2.5-v0.2**: Updated with Qwen2.5 backbone, supporting dynamic resolution.
- **athrael-soju/colqwen3.5-4.5B-v3**: Based on Qwen3.5, utilizing hybrid GatedDeltaNet for superior reasoning.

## Strengths
- **Native Multi-modality**: No OCR required; handles layouts and visuals natively.
- **State-of-the-Art Retrieval**: Consistently tops the ViDoRe (Vision Document Retrieval) benchmarks.
- **Late Interaction Accuracy**: Superior to single-vector Bi-Encoders for complex semantic matching.

## Limitations
- **Storage Intensive**: Multi-vector embeddings can be 10x-100x larger than standard text embeddings.
- **Computationally Heavier**: Inference requires GPU acceleration (CUDA or MPS) for acceptable performance.

## When to use it
- When building **Vision-RAG** pipelines that must handle complex document layouts (e.g., multi-column PDFs, forms).
- When information is primarily contained in **charts, tables, or diagrams** that standard OCR often misrepresents.
- For high-precision retrieval where the semantic relationship between visual elements and text is critical.

## When not to use it
- For **text-only document** archives where standard embedding models (like OpenAI or HuggingFace text-only models) are more storage-efficient.
- In environments with **high storage constraints**, as multi-vector late interaction embeddings can take 10x-100x more space than single-vector embeddings.
- When query latency is the absolute priority over retrieval recall in very large-scale datasets.

## Related tools / concepts
- [Qwen](qwen.md)
- [RAG Pattern](../../knowledge_base/patterns/rag.md)
- [Vision Models Research](../../knowledge_base/vision-models-research.md)
- [Byaldi](https://github.com/AnswerDotAI/byaldi) (Simplified wrapper for ColPali)
- [Vespa.ai](https://vespa.ai/) (Vector database with native late-interaction support)
- [Qdrant](https://qdrant.tech/) (Support for multi-vector document indexing)

## Sources / References
- [ColPali: Efficient Document Retrieval with VLMs (arXiv)](https://arxiv.org/abs/2407.01449)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
- [ViDoRe Leaderboard](https://huggingface.co/spaces/vidore/vidore-leaderboard)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
