# Haystack

## What it is
Haystack is an end-to-end open-source framework for building applications powered by LLMs, Transformer models, and vector search. It is developed by deepset and designed to handle large-scale RAG and agentic workflows.

## What problem it solves
It simplifies the construction of complex LLM pipelines by providing modular components for document loading, indexing, retrieval, and generation. Its "Pipeline" abstraction allows for flexible, DAG-based architectures that can handle non-linear logic.

## Where it fits in the stack
Framework

## Typical use cases
- **Enterprise RAG**: Building search systems over millions of documents.
- **Conversational Agents**: Creating chatbots that use tools and access external data.
- **Extracted Metadata**: Using LLMs to structure unstructured data from various sources.

## Strengths
- **Modular Architecture**: Easy to swap out components (e.g., changing from Elasticsearch to Pinecone).
- **Production Ready**: Designed with scaling and deployment in mind.
- **Haystack 2.0**: Modern, simplified API with better support for complex routing.

## Limitations
- **Ecosystem Size**: While growing, it has fewer community integrations than LangChain.
- **Transitioning**: Users of Haystack 1.x may find the shift to 2.0 requires significant code changes.

## When to use it
- When building production-grade RAG systems.
- If you prefer a modular, component-based approach to pipeline design.

## When not to use it
- For very simple scripts where a basic API call suffices.
- If you are already deeply committed to another framework's ecosystem (e.g., LlamaIndex).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

```bash
pip install haystack-ai
```

```python
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator

prompt_template = "What is the capital of {{country}}?"
pipeline = Pipeline()
pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
pipeline.add_component("llm", OpenAIGenerator())
pipeline.connect("prompt_builder", "llm")

result = pipeline.run({"prompt_builder": {"country": "France"}})
print(result["llm"]["replies"][0])
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)

## Sources / References
- [Official Website](https://haystack.deepset.ai/)
- [GitHub](https://github.com/deepset-ai/haystack)
- [Documentation](https://docs.haystack.deepset.ai/)

## Contribution Metadata

- Last reviewed: 2026-02-28
- Confidence: high
