# LLMWare

## What it is
LLMWare is an open-source framework specifically designed for building enterprise-grade RAG and AI agent applications. It provides a "unified data-to-AI" pipeline that emphasizes privacy, security, and the use of **Small Language Models (SLMs)** like BLING and DRAGON. As of late August 2026, LLMWare v0.4.x includes native support for **GGUF-based local inference**, SLIM (Structured Language Instruction Models), multi-step agentic workflows, and native integration with the **Model Context Protocol (MCP 3.1)** to link enterprise-level tool calling and local data sources seamlessly.

## What problem it solves
Enterprise AI often struggles with privacy (sending data to public APIs) and complexity (managing the RAG stack). LLMWare solves this by providing a local-first architecture that makes it easy to use open-source, small models that can run on-premises while providing high accuracy for specific tasks like contract analysis or financial extraction.

## Where it fits in the stack
**Category**: Automation & Orchestration / RAG Frameworks. It specializes in the "Sovereign AI" niche for enterprise.

## Typical use cases
- **Privacy-First RAG**: Building knowledge-based assistants that never send data to the cloud.
- **Specialized Industry Agents**: Using models fine-tuned for finance, legal, or medical data.
- **Automated Document Workflows**: High-volume extraction and analysis of complex documents (PDFs, spreadsheets).
- **Embedded AI**: Running AI agents on-device or in resource-constrained environments.

## Strengths
- **Small Model Focus**: Optimized for high performance using efficient models like BLING or DRAGON.
- **Integrated Pipeline**: Covers everything from document parsing and embedding to retrieval and generation.
- **Enterprise Ready**: Designed with security and data governance as first-class citizens.
- **Model Efficiency**: Superior performance on standard CPU hardware for specialized tasks.

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

### Basic RAG Example with Local BLING model
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

## CLI examples

### Initialize a Library
```bash
llmware library create --name "ComplianceDocs" --path "./docs"
```

### Run a Local Model
```bash
llmware model download --model "bling-phi-3-gguf"
llmware model run --model "bling-phi-3-gguf" --prompt "Extract terms from the contract."
```

## API examples

### Using SLIM for Structured Extraction
```python
from llmware.models import ModelCatalog

# Load a SLIM model for named entity recognition
model = ModelCatalog().load_model("slim-ner-tool")

text = "Apple Inc. announced a new product in Cupertino."
entities = model.function_call(text)
print(entities)
```

### MCP 3.1 Task Protocol Tool Registration (2026 Pattern)
Using MCP 3.1, LLMWare models can be exposed as local tool-calling services that frontier models (e.g., Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6, Gemini 3.5 series) can invoke.

```python
import json
import urllib.request
from llmware.models import ModelCatalog

# Initialize local SLIM model
slim_model = ModelCatalog().load_model("slim-ner-tool")

# Standard MCP 3.1 Task Protocol payload schema for tool registration
def register_mcp_tool():
    url = "http://localhost:8000/tasks/v1/tools/register"
    payload = {
        "name": "slim_ner_tool",
        "description": "Locally extract named entities from complex document segments",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to analyze"}
            },
            "required": ["text"]
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

## Related tools / concepts
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Ollama](../../services/ollama.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Dify](../ai_knowledge/dify.md)
- [LiteLLM](../../services/litellm.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LocalAI](../infrastructure/localai.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / References
- [LLMWare GitHub Repository](https://github.com/llmware-ai/llmware)
- [LLMWare Documentation](https://llmware.ai/docs)
- [BLING Model Family on Hugging Face](https://huggingface.co/llmware)
- [Enterprise SLMs: The late 2026 Strategy Guide](https://example.com/llmware-enterprise-slm)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
