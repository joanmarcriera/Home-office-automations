# LLMWare

## What it is
LLMWare is an open-source framework specifically designed for building enterprise-grade RAG and AI agent applications. It provides a "unified data-to-AI" pipeline that emphasizes privacy, security, and the use of small, specialized models (SLMs).

## What problem it solves
Enterprise AI often struggles with privacy (sending data to public APIs) and complexity (managing the RAG stack). LLMWare solves this by providing a local-first architecture that makes it easy to use open-source, small models that can run on-premises while providing high accuracy for specific tasks.

## Where it fits in the stack
**Category**: Automation & Orchestration / RAG Frameworks

## Typical use cases
- **Privacy-First RAG**: Building knowledge-based assistants that never send data to the cloud.
- **Specialized Industry Agents**: Using models fine-tuned for finance, legal, or medical data.
- **Automated Document Workflows**: High-volume extraction and analysis of complex documents (PDFs, spreadsheets).
- **Embedded AI**: Running AI agents on-device or in resource-constrained environments.

## Strengths
- **Small Model Focus**: Optimized for high performance using efficient models like BLING or DRAGON.
- **Integrated Pipeline**: Covers everything from document parsing and embedding to retrieval and generation.
- **Enterprise Ready**: Designed with security and data governance as first-class citizens.
- **Open Source**: Full transparency and control over the AI stack.

## Limitations
- **Learning Curve**: The framework is comprehensive and may take time to fully understand.
- **Model Training**: While it supports many models, achieving peak performance might require selecting or fine-tuning the right specialized model.

## When to use it
- When building enterprise RAG applications that require high security and data privacy.
- If you want to use small, specialized models (SLMs) to reduce costs and latency while maintaining high accuracy for specific domains.
- For complex document processing tasks that involve multi-step extraction and analysis from PDFs or spreadsheets.

## When not to use it
- For very simple, consumer-facing chatbots where a basic wrapper around OpenAI or Claude would suffice.
- If you are fully committed to a specific cloud provider's AI stack (like AWS Bedrock) and don't need a portable, open-source framework.

## Getting started

### Installation
```bash
pip install llmware
```

### Basic RAG Example
```python
from llmware.library import Library
from llmware.retrieval import Query

# Create a library and add files
lib = Library().create_new_library("my_internal_docs")
lib.add_files("/path/to/my/documents")

# Run a query
query = Query(lib)
results = query.semantic_search("What is our security policy?", number_of_results=3)
```

## Related tools / concepts
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Ollama](../../services/ollama.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Dify](../frameworks/dify.md)
- [LiteLLM](../../services/litellm.md)
- [Unstructured](../ai_knowledge/unstructured.md)

## Sources / references
- [LLMWare GitHub Repository](https://github.com/llmware-ai/llmware)
- [LLMWare Documentation](https://llmware.ai/docs)

## Contribution Metadata
- Last reviewed: 2026-05-09
- Confidence: high
