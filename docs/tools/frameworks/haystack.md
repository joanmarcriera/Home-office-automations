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

## Haystack 2.0 Architecture: Components and Connections
Haystack 2.0 uses a more explicit and flexible pipeline architecture:
- **Components**: The building blocks of a pipeline (e.g., `OpenAIGenerator`, `PromptBuilder`, `InMemoryDocumentStore`). Each component has defined inputs and outputs.
- **Connections**: Explicitly defined data flows between components. Haystack validates that the output of one component matches the expected input type of the next.

## Advanced Routing: ConditionalRouter
Use the `ConditionalRouter` to direct data to different branches based on runtime logic, such as routing queries based on complexity or language.

```python
from haystack.components.routers import ConditionalRouter

router_template = [
    {
        "condition": "{{query|length > 100}}",
        "output": "{{query}}",
        "output_name": "complex_query",
        "output_type": str,
    },
    {
        "condition": "{{query|length <= 100}}",
        "output": "{{query}}",
        "output_name": "simple_query",
        "output_type": str,
    },
]

router = ConditionalRouter(routes=router_template)
pipeline = Pipeline()
pipeline.add_component("router", router)
# Connect 'complex_query' to a powerful model, 'simple_query' to a faster one.
```

## Security: Secrets Management
Haystack 2.0 introduces a standardized way to handle sensitive information like API keys using the `Secret` type, ensuring they aren't hardcoded or accidentally logged.

```python
from haystack.utils import Secret
from haystack.components.generators import OpenAIGenerator

# Load from environment variable (preferred)
generator = OpenAIGenerator(api_key=Secret.from_env_var("OPENAI_API_KEY"))

# Or from a string (less secure, use for testing)
generator = OpenAIGenerator(api_key=Secret.from_token("my-token"))
```

## Serialization and Deployment
Pipelines can be easily serialized to YAML or JSON, making it simple to share configurations or deploy them in different environments without re-writing Python code.

```python
# Save pipeline to YAML
with open("pipeline.yaml", "w") as f:
    pipeline.dump(f)

# Load pipeline from YAML
with open("pipeline.yaml", "r") as f:
    new_pipeline = Pipeline.load(f)
```

## Limitations
- **Ecosystem Size**: While growing, it has fewer community integrations than LangChain.
- **Transitioning**: Users of Haystack 1.x may find the shift to 2.0 requires significant code changes.

## When to use it
- When building production-grade RAG systems.
- If you prefer a modular, component-based approach to pipeline design.

## When not to use it
- For very simple scripts where a basic API call suffices.
- If you are already deeply committed to another framework's ecosystem (e.g., LlamaIndex).

## Getting started

### Installation
```bash
pip install haystack-ai
```

### Minimal Python Example
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
- [AutoGen](autogen.md)
- [DSPy](dspy.md)
- [Smolagents](smolagents.md)
- [RAGFlow](../process_understanding/ragflow.md)
- [Knowledge Base Patterns](../../knowledge_base/patterns/rag.md)
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Semantic Kernel](semantic-kernel.md)

## Sources / References
- [Official Website](https://haystack.deepset.ai/)
- [GitHub](https://github.com/deepset-ai/haystack)
- [Documentation](https://docs.haystack.deepset.ai/)

## Contribution Metadata

- Last reviewed: 2026-05-17
- Confidence: high
