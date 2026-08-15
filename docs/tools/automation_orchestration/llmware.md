# LLMWare

## What it is
LLMWare is an open-source framework designed for enterprise-grade Retrieval-Augmented Generation (RAG) and specialized AI agent applications. It provides a unified data-to-AI pipeline optimized for privacy-first, on-premises execution using Small Language Models (SLMs) such as BLING, DRAGON, and SLIM. As of early 2027, LLMWare features native support for **FastMCP 3.1** and the **MCP 3.0 Task Protocol**, GGUF/vLLM local inference, and structured entity extraction integrated with frontier orchestration platforms.

## What problem it solves
Enterprise AI applications often encounter privacy constraints (sending sensitive data to cloud APIs) and resource complexity (managing sprawling RAG stacks). LLMWare resolves this by offering a local-first, highly efficient architecture designed for specialized tasks like contract review, financial extraction, and compliance auditing without data exfiltration.

## Where it fits in the stack
**Automation & Orchestration / Enterprise RAG Layer**. It specializes in sovereign AI and specialized local model execution within the [KnowledgeOps](../../knowledge_base/multi_agent_knowledgeops.md) framework.

## Typical use cases
- **Privacy-First Sovereign RAG**: Deploying enterprise search assistants on isolated internal networks.
- **Specialized Industry Agents**: Leveraging models specifically fine-tuned for financial, legal, or medical document reasoning.
- **Automated High-Volume Document Extraction**: Extracting structured entities from PDFs, spreadsheets, and scanned documents.
- **On-Device / Edge Agent Deployment**: Running structured reasoning agents on resource-constrained local infrastructure.

## Strengths
- **SLM Optimization**: Purpose-built to maximize accuracy using ultra-compact, domain-specific models (BLING, DRAGON, SLIM).
- **End-to-End Pipeline**: Handles parsing, embedding, vector indexing, retrieval, and generation in a unified SDK.
- **FastMCP 3.1 Interoperability**: Direct tool-calling integration with local and frontier agents ([Claude 5.1](../providers/anthropic.md), [GPT-5.5](../providers/openai.md), [Gemini 4.0 Pro](../ai_knowledge/gemini.md), [Qwen 3.8](../ai_knowledge/qwen.md)).
- **Hardware Efficiency**: Optimized CPU/GPU execution via GGUF and llama.cpp/vLLM backends.

## Limitations
- **Ecosystem Focus**: Highly opinionated around structured SLMs; general conversational multi-modal tasks may require external model gateways.
- **Model Selection Tuning**: Achieving peak accuracy across custom domains requires selecting or fine-tuning specific SLIM task modules.

## When to use it
- When building enterprise AI applications under strict data governance and zero-data-retention compliance rules.
- When minimizing operational latency and inference costs using specialized small models.
- When performing multi-step document extraction workflows from complex corporate file formats.

## When not to use it
- For quick consumer-facing web apps where a simple cloud LLM API endpoint is sufficient.
- When relying exclusively on hosted multi-modal platform suites without local deployment capabilities.

## Getting started

### Installation
Install LLMWare core and standard dependencies:

```bash
pip install llmware pydantic
```

### Basic RAG Pipeline
Inference over internal documents using a local BLING model:

```python
from llmware.library import Library
from llmware.retrieval import Query

# Initialize library and ingest documents
lib = Library().create_new_library("internal_compliance")
lib.add_files("./docs")

# Execute semantic query
query = Query(lib)
results = query.semantic_search("What are the data retention policy guidelines?", number_of_results=3)
for res in results:
    print(f"Match: {res.get('text')[:100]}... (Score: {res.get('special_score')})")
```

## CLI examples
LLMWare provides CLI capabilities for dataset ingestion and model execution:

```bash
# Create and ingest a document library
llmware library create --name "ComplianceDocs" --path "./docs"

# Download and test a local SLM model
llmware model download --model "bling-phi-3-gguf"
llmware model run --model "bling-phi-3-gguf" --prompt "Extract key contract dates."
```

## API examples

### Structured SLIM Entity Extraction with Pydantic v2
Using SLIM models for structured named entity extraction validated with Pydantic v2:

```python
from pydantic import BaseModel, Field
from llmware.models import ModelCatalog

class EntityExtractionResult(BaseModel):
    organization: str = Field(description="Name of the organization")
    location: str = Field(description="Location referenced in text")
    status: str = Field(default="extracted", description="Extraction status")

# Load SLIM NER model
model = ModelCatalog().load_model("slim-ner-tool")
raw_text = "Acme Corp finalized the lease agreement for their facility in Austin."

raw_entities = model.function_call(raw_text)

# Validate against Pydantic schema
extracted = EntityExtractionResult(
    organization=raw_entities.get("organization", ["Acme Corp"])[0],
    location=raw_entities.get("location", ["Austin"])[0]
)

print(extracted.model_dump_json(indent=2))
```

### FastMCP 3.1 Server Registration Example
Exposing LLMWare SLM reasoning as a FastMCP 3.1 tool service:

```python
from pydantic import BaseModel, Field

class FastMCPToolRequest(BaseModel):
    tool_name: str = Field(default="slim_ner_tool", description="FastMCP tool name")
    input_text: str = Field(description="Input document text for local entity extraction")

def handle_mcp_request(request: FastMCPToolRequest) -> dict:
    # Model execution wrapper
    model = ModelCatalog().load_model("slim-ner-tool")
    result = model.function_call(request.input_text)
    return {
        "status": "success",
        "tool": request.tool_name,
        "extracted_data": result
    }

req_data = FastMCPToolRequest(input_text="Global Tech Inc opened a new office in Tokyo.")
print(handle_mcp_request(req_data))
```

## Related tools / concepts
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Ollama](../../services/ollama.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [LocalAI](../infrastructure/localai.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [LLMWare Official Documentation](https://llmware.ai/docs)
- [LLMWare GitHub Repository](https://github.com/llmware-ai/llmware)
- [FastMCP 3.1 Protocol Standard](https://modelcontextprotocol.io/spec/3.0)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
