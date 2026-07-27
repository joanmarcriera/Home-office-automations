# Playbook: Fully Offline Assistant

```mermaid
flowchart TD
    User([User Prompt / Query]) -->|1. Request| WebUI[Open WebUI / Interface]
    WebUI -->|2. Generate Embeddings| Embed[Ollama Embedding Engine\nnomic-embed-text]
    Embed -->|3. Search Vectors| Milvus[(Milvus Standalone DB\nhomelab_docs)]
    Milvus -->|4. Return Relevant Context| WebUI
    WebUI -->|5. Local Web Cache Lookup| Kiwix[Kiwix Serve\nWikipedia / Local ZIMs]
    Kiwix -->|6. Return Web Context| WebUI
    WebUI -->|7. Synthesized Prompt with Context| Ollama[Ollama Inference Engine\ngemma3-27b-it]
    Ollama -->|8. Local LLM Generation| WebUI
    WebUI -->|9. Stream Response| User
```

## What it is
The Fully Offline Assistant is an end-to-end architecture for deploying a private, air-gapped AI stack on local hardware. It integrates [Ollama](../services/ollama.md) for LLM inference, [Open WebUI](../services/open-webui.md) for the interface, local embeddings for RAG, a local vector database ([Milvus](../tools/infrastructure/milvus.md) or Chroma), and [Kiwix](../services/kiwix.md) for offline web knowledge.

## What problem it solves
It eliminates reliance on cloud-based AI providers, solving for:
- **Data Privacy**: Sensitive data never leaves the local network.
- **Internet Independence**: The system remains functional during ISP outages or in remote/air-gapped environments.
- **Cost Predictability**: Eliminates monthly subscription fees and token-based pricing.
- **Data Sovereignty**: Complete control over which models and knowledge bases are used.

## Where it fits in the stack
**Category**: Playbook / Infrastructure. It serves as the **operational blueprint** for the Privacy-First AI layer, orchestrating multiple services from the `docs/services/` and `docs/tools/` directories into a unified, functional assistant.

## Typical use cases
- **Confidential Document Analysis**: Chatting with private financial, medical, or legal documents without cloud exposure.
- **Remote Research**: Accessing a vast library of knowledge (Wikipedia, StackExchange) via Kiwix in areas without internet.
- **Secure Code Assistance**: Using local models to help with proprietary software development.
- **Disaster Recovery Knowledge**: Maintaining access to technical manuals and survival guides during extended outages.

## Strengths
- **Zero Latency (Network)**: No network round-trips to external servers.
- **Uncensored Reasoning**: Ability to use models without restrictive cloud-based filters.
- **Infinite Context**: Leverage local RAG to "talk" to terabytes of local data.
- **Customizable**: Swap models, embedding engines, or vector DBs based on hardware capabilities.

## Limitations
- **Hardware Dependent**: Performance is strictly limited by local CPU/GPU/VRAM resources.
- **Maintenance Overhead**: Requires manual updates for models and knowledge ZIM files.
- **Energy Consumption**: High-performance inference can be power-intensive.
- **Initial Setup**: More complex to configure than a simple cloud API.

## When to use it
- When working with highly sensitive or regulated data.
- In environments with restricted or no internet access.
- When you have dedicated hardware (e.g., Mac Studio, high-VRAM PC) sitting idle.

## When not to use it
- For quick, low-stakes questions where a mobile-ready cloud app is more convenient.
- If you lack the hardware capable of running models at acceptable speeds (e.g., < 5 tokens/sec).
- When you require the absolute latest frontier capabilities (e.g., GPT-5.5) which aren't yet available for local deployment.

## Getting started

### 1. Core Inference Setup
Install [Ollama](../services/ollama.md) and pull your preferred model:
```bash
ollama run gemma3-27b-it
```

### 2. Knowledge Retrieval (Kiwix)
Download Kiwix ZIM files (e.g., Wikipedia) and serve them via [Kiwix](../services/kiwix.md) Docker:
```bash
docker run -d -p 8080:80 -v /path/to/zims:/data kiwix/kiwix-serve
```

### 3. Vector Database
Deploy [Milvus](../tools/infrastructure/milvus.md) via Docker for storing embeddings:
```bash
# Example standalone Milvus deployment
docker run -d --name milvus_standalone -p 19530:19530 -p 9091:9091 milvusdb/milvus:v2.4.0
```

### 4. Orchestration (Open WebUI)
Deploy [Open WebUI](../services/open-webui.md) and connect it to Ollama and Milvus:
```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/data --name open-webui ghcr.io/open-webui/open-webui:main
```

## CLI examples

### 1. Verifying Local Model Availability
```bash
ollama list
```

### 2. Testing Kiwix API Access
```bash
curl http://localhost:8080/wikipedia_en_all_maxi_2026-07/search?q=FastMCP
```

### 3. Checking Milvus Health
```bash
curl http://localhost:9091/healthz
```

## API examples

### Python: End-to-End RAG Query (Local)
```python
import ollama
from pymilvus import Collection, connections

# 1. Generate local embedding
embed = ollama.embeddings(model="nomic-embed-text", prompt="How do I setup Kiwix?")

# 2. Query local Vector DB (Milvus)
connections.connect("default", host="localhost", port="19530")
collection = Collection("homelab_docs")
results = collection.search(
    data=[embed["embedding"]],
    anns_field="vector",
    param={"metric_type": "L2", "params": {"nprobe": 10}},
    limit=3,
    output_fields=["text"]
)

# 3. Generate Answer with Context
context = "\n".join([r[0].entity.get("text") for r in results])
response = ollama.generate(
    model="gemma3-27b-it",
    prompt=f"Context: {context}\nQuestion: How do I setup Kiwix?"
)
print(response['response'])
```

## Related tools / concepts
- [Ollama](../services/ollama.md) — Local LLM engine.
- [Open WebUI](../services/open-webui.md) — The interface for local AI.
- [Kiwix](../services/kiwix.md) — Offline knowledge libraries.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Guide to models.
- [Vector DB Comparison](../knowledge_base/vector-db-comparison.md) — Choosing the right storage.
- [RAG Pattern](../knowledge_base/patterns/rag-pattern.md) — Theoretical background.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Connecting local tools.

## Sources / References
- [Ollama Official Documentation](https://ollama.com/library)
- [Open WebUI RAG Guide](https://docs.openwebui.com/tutorial/rag/)
- [Kiwix Library](https://library.kiwix.org/)
- [Milvus Documentation](https://milvus.io/docs)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
