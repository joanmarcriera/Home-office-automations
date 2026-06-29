# Haystack

## What it is
Haystack is an end-to-end open-source framework for building applications powered by LLMs, Transformer models, and vector search. It is developed by deepset and designed to handle large-scale RAG and agentic workflows using models like Claude 4.8 and GPT-5.5.

## What problem it solves
It simplifies the construction of complex LLM pipelines by providing modular components for document loading, indexing, retrieval, and generation. Its "Pipeline" abstraction allows for flexible, DAG-based architectures that can handle non-linear logic and conditional routing. It addresses the need for production-grade, serialized pipelines that are easy to maintain and scale.

## Where it fits in the stack
**Framework / RAG Orchestrator**. It specializes in production-grade retrieval-augmented generation and modular AI pipeline design. In June 2026, it serves as a primary framework for building [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) compatible RAG services.

## Typical use cases
- **Enterprise RAG**: Building search systems over millions of documents.
- **Conversational Agents**: Creating chatbots that use tools and access external data.
- **Extracted Metadata**: Using LLMs to structure unstructured data from various sources.
- **Multi-model Orchestration**: Routing tasks between Claude 4.8 Opus and GPT-5.5 based on cost or complexity.
- **MCP Tool Generation**: Automatically creating tool definitions for [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers.

## Strengths
- **Modular Architecture**: Easy to swap out components (e.g., changing from Elasticsearch to Pinecone).
- **Production Ready**: Designed with scaling, deployment, and serialization (YAML/JSON) in mind.
- **Haystack 2.x Features**: Enhanced support for dynamic components and runtime validation.
- **Advanced Routing**: `ConditionalRouter` allows for complex, logic-driven data flows.
- **Native MCP 3.0 Support**: Seamlessly connects to MCP servers for tool and resource discovery.
- **Secrets Management**: Standardized `Secret` type for secure handling of API keys.

## Limitations
- **Ecosystem Size**: While growing, it has fewer community integrations than LangChain for niche edge cases.
- **Transitioning**: Users of Haystack 1.x may find the shift to 2.0+ requires significant code changes.
- **Learning Curve**: Mastering the explicit connection paradigm in the modern API takes time.

## When to use it
- When building production-grade RAG systems that require strict architectural control.
- If you prefer a modular, component-based approach to pipeline design.
- When you need to serialize pipelines for cross-environment deployment.

## When not to use it
- For very simple scripts where a basic API call suffices.
- If you are already deeply committed to another framework's ecosystem (e.g., LlamaIndex).
- For research projects that require frequent, breaking changes to the core framework logic.

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
pipeline.add_component("llm", OpenAIGenerator(model="gpt-5.5-preview"))
pipeline.connect("prompt_builder", "llm")

result = pipeline.run({"prompt_builder": {"country": "France"}})
print(result["llm"]["replies"][0])
```

## CLI examples

```bash
# Exporting a pipeline to YAML
python my_pipeline.py --export pipeline.yaml

# Running a serialized pipeline from the CLI
haystack-run --pipeline pipeline.yaml --input "What is AI?"

# Validating a pipeline configuration
haystack-validate --file pipeline.yaml
```

## API examples

### Conditional Routing with Claude 4.8
```python
from haystack.components.routers import ConditionalRouter
from haystack.components.generators import AnthropicGenerator

# Route to Claude 4.8 for complex queries
router_template = [
    {
        "condition": "{{query|length > 100}}",
        "output": "{{query}}",
        "output_name": "complex_query",
        "output_type": str,
    }
]

router = ConditionalRouter(routes=router_template)
claude_gen = AnthropicGenerator(model="claude-4-8-opus-20260528")

pipeline = Pipeline()
pipeline.add_component("router", router)
pipeline.add_component("claude", claude_gen)
pipeline.connect("router.complex_query", "claude.prompt")
```

### Secrets Management
```python
from haystack.utils import Secret
from haystack.components.generators import OpenAIGenerator

# Load from environment variable (preferred)
generator = OpenAIGenerator(api_key=Secret.from_env_var("OPENAI_API_KEY"))

# Serialization maintains secret references, not tokens
yaml_str = pipeline.dumps()
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md) — The largest LLM framework.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — RAG-first framework.
- [AutoGen](autogen.md) — Multi-agent orchestration.
- [DSPy](dspy.md) — Programmatic prompt optimization.
- [Smolagents](smolagents.md) — Minimalist agent library.
- [RAG Patterns](../../knowledge_base/patterns/rag-pattern.md) — Reference implementations.
- [Semantic Kernel](semantic-kernel.md) — Microsoft's enterprise AI framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Integrated tool protocol.
- [NVIDIA NIM](../providers/nvidia.md) — Optimized inference backend.

## Sources / References
- [Official Website](https://haystack.deepset.ai/)
- [GitHub](https://github.com/deepset-ai/haystack)
- [Documentation](https://docs.haystack.deepset.ai/)
- [Haystack 2.0 Release Notes](https://haystack.deepset.ai/blog/haystack-2-release)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
