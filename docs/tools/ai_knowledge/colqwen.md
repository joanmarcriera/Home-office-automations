# ColQwen3.5-v2

## What it is
ColQwen3.5-v2 is a multi-modal document retrieval model based on the Qwen 3.5 architecture. It leverages the ColBERT (Contextualized Late Interaction over BERT) strategy to provide high-performance retrieval across text and visual document elements.

## What problem it solves
Traditional text-only retrieval fails on documents with heavy visual components like charts, tables, and diagrams. ColQwen allows for direct retrieval from document images or PDFs by understanding both the text and the layout/visual context.

## Where it fits in the stack
**Multi-modal Retrieval / RAG Engine**. It is a specialized model used for the "Retrieval" part of Vision-RAG (V-RAG) pipelines.

## Typical use cases
- **Visual Document RAG**: Searching and retrieving information from scanned PDFs, manuals, and reports with complex layouts.
- **Enterprise Search**: Building knowledge bases that include technical drawings, financial charts, and slide decks.
- **Agentic Vision Tasks**: Providing AI agents with the ability to "see" and find information in structured document archives.

## Getting started
ColQwen3.5-v2 is typically used via the `colbert` or `byaldi` libraries for easy integration into Python-based RAG pipelines.

```python
from byaldi import RAGMultiModalModel

# Load the model
RAG = RAGMultiModalModel.from_pretrained("vidore/colqwen3.5-v2")

# Index a folder of images/PDFs
RAG.index(input_path="data/manuals/", index_name="manuals_index")

# Search
results = RAG.search("How do I reset the filter on the X100 model?")
```

## Strengths
- **Native Multi-modality**: Built on Qwen 3.5, providing state-of-the-art vision and language understanding.
- **Late Interaction Efficiency**: The ColBERT architecture allows for fast and precise retrieval without needing to process every document with the full LLM at query time.
- **Compact and Powerful**: At 4.5B parameters, it provides a great balance of performance and efficiency for local or hosted deployment.

## Limitations
- **Storage Requirements**: Storing late interaction embeddings (multi-vector) can require significantly more disk space than standard single-vector embeddings.
- **Specialized Pipeline**: Requires specific libraries or implementations to handle the multi-vector late interaction logic.

## When to use it
- When building **Vision-RAG** pipelines that must handle complex document layouts (e.g., multi-column PDFs, forms).
- When information is primarily contained in **charts, tables, or diagrams** that standard OCR often misrepresents.
- For high-precision retrieval where the semantic relationship between visual elements and text is critical.

## When not to use it
- For **text-only document** archives where standard embedding models (like OpenAI or HuggingFace text-only models) are more storage-efficient.
- In environments with **high storage constraints**, as multi-vector late interaction embeddings can take 10x-100x more space than single-vector embeddings.
- When query latency is the absolute priority over retrieval recall in very large-scale datasets.

## Licensing and cost
- **Open Weights**: Available on Hugging Face (under Qwen model license).

## Related tools / concepts
- [Qwen](qwen.md)
- [RAG Pattern](../../knowledge_base/patterns/rag.md)
- [Vision Models Research](../../knowledge_base/vision-models-research.md)
- [LlamaIndex](llamaindex.md)
- [LangChain](langchain.md)
- [Ollama](../../services/ollama.md)
- [Paperless-ngx](../../services/paperless-ngx.md)

## Sources / References
- [ColQwen3.5-v2 4.5B Release](https://www.reddit.com/r/MachineLearning/comments/1rsxlg8/p_colqwen35v2_45b_is_out/)
- [ViDoRe (Vision Document Retrieval) Benchmark](https://huggingface.co/vidore)

## Contribution Metadata
- Last reviewed: 2026-04-16
- Confidence: high
