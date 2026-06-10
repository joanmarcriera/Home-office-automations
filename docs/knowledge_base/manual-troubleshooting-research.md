# Manual Troubleshooting Assistant Research

## What it is
This research evaluates the user interface and orchestration layer for a chat-based assistant designed to troubleshoot household appliances using scanned manuals. As of June 2026, it emphasizes **Agentic RAG** and multi-modal reasoning to handle complex diagrams and multi-step repair workflows.

## What problem it solves
Scanned manuals are often long, poorly indexed, and difficult to search during a "household emergency" (e.g., a leaking dishwasher). This assistant provides immediate, natural language answers and actionable task steps by grounding frontier models like Claude 4.8 and GPT-5.5 in local document data.

## Where it fits in the stack
It sits in the **User Interface / Orchestration** layer, connecting the user to the local LLM and the Vector DB containing chunked manual data. It acts as a specialized skill within the broader Home Admin Agent ecosystem.

## Typical use cases
- **Error Code Interpretation**: Decoding cryptic flashing lights on appliances.
- **Preventative Maintenance**: Scheduling and guiding dryer vent or filter cleanings.
- **Interactive Repair**: Real-time, step-by-step guidance for part replacements or resets.
- **Diagram Analysis**: Using multi-modal models to explain "Figure 3.2" from a scanned PDF.

## Comparison: Open WebUI vs. Streamlit

| Feature | Open WebUI | Streamlit |
| :--- | :--- | :--- |
| **User Experience** | Polished, ChatGPT-like interface. Multi-user support with history. | Highly customizable but requires more frontend effort for "chat" feel. |
| **Built-in RAG** | Native support for document ingestion and vector search. | Must be implemented manually using LangChain/LlamaIndex. |
| **Family Ease-of-Use**| High. Mobile-friendly and familiar interface. | Moderate. Can be tailored, but lacks out-of-the-box user management. |
| **Extensibility** | Supports "Tools", "Functions", and MCP servers. | Infinite (it's Python), but everything is a custom build. |
| **Authentication** | Built-in RBAC and OIDC (Authentik). | Requires additional libraries (e.g., `streamlit-authenticator`). |

**Recommendation**: For a family-centric "Home Admin Agent", **Open WebUI** is the preferred choice due to its lower maintenance overhead and superior multi-user experience.

## Strengths
- **Accessibility**: Multi-modal input (photo of the error code) simplifies interaction for non-technical users.
- **Privacy**: Entirely self-hosted when using local LLMs (Llama 4 Maverick) and local vector stores.
- **Agentic reasoning**: Moves beyond Q&A to task execution (e.g., "order the replacement filter").
- **Reliability**: Uses reflection loops to verify its own troubleshooting steps against the manual text.

## Limitations
- **OCR Quality**: Low-resolution scans or handwritten notes in manuals can still degrade retrieval accuracy.
- **Latency**: Agentic reflection loops and multi-modal processing increase response time compared to simple RAG.
- **Diagram Complexity**: Highly technical schematics may still require human verification despite multi-modal advances.

## When to use it
- For any household appliance with a digital or physical manual.
- When troubleshooting issues that have clear, documented resolution steps in the manufacturer's literature.
- As a first-pass diagnostic tool before calling expensive professional service.

## When not to use it
- **Life Safety**: Never use for gas leaks, smoke, or fire-related emergencies.
- **High-Voltage**: Avoid for internal repairs on microwave ovens or main breaker panels unless the user is a qualified electrician.
- **Ambiguous Cases**: If the manual and the physical state of the appliance conflict, prioritize human observation.

## Getting started
### Local Stack Setup
The fastest way to deploy the research environment is using Docker Compose with Ollama and Open WebUI.

```bash
docker compose up -d
# Access Open WebUI at http://localhost:3000
```

### Manual Ingestion
1. Upload PDF manuals to the `Documents` section in Open WebUI.
2. Select the `RAG` engine (ChromaDB or Weaviate).
3. Query using a model with strong reasoning capabilities (e.g., Claude 4.7 Sonnet).

## CLI examples
Use the `scripts/verify_manual_retrieval.py` tool to test your ingestion pipeline.

```bash
# Test retrieval for a specific appliance
python3 scripts/verify_manual_retrieval.py --manual "Samsung_Dryer_Manual.pdf" --query "How to clean the lint filter?"

# Re-index all manuals in the data directory
python3 scripts/process_manuals.py --input ./data/manuals/ --reindex

# Check vector DB health
curl -X GET http://localhost:8000/health
```

## API examples
Standardized API interaction for the troubleshooting backend.

```python
import requests

API_URL = "http://localhost:8000/api/troubleshoot"
API_TOKEN = "home-admin-token"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "appliance": "Dishwasher",
    "issue": "E24 Error code",
    "image_url": "http://local-nvr/snapshot/dishwasher_panel.jpg" # Optional multi-modal input
}

response = requests.post(API_URL, headers=headers, json=payload)
print(response.json()["solution_steps"])
```

## System Prompt Templates

### Troubleshooting Assistant
```text
You are the Riera Family's Home Troubleshooting Assistant. Your goal is to help family members fix household issues using the provided manuals and knowledge base.

Rules:
1. Always check the manual for the specific model if provided in the context.
2. If the answer is not in the manual, state it clearly and offer general troubleshooting tips based on common knowledge, but add a disclaimer.
3. Be concise and use bullet points for instructions.
4. If a repair seems dangerous (e.g., involving high voltage or gas), advise calling a professional.
```

## Implementation Patterns

### n8n Automation: Manual Ingestion
A common pattern for ingesting manuals from Paperless-ngx into a vector database:

1. **Trigger**: Paperless-ngx webhook on document creation.
2. **Filter**: Check for tags like `manual` or `appliance`.
3. **Extraction**: Retrieve the document content (or OCR text).
4. **Embedding**: Send text chunks to an embedding model (e.g., via Ollama).
5. **Storage**: Upsert chunks into ChromaDB or similar.

## Related tools / concepts
- [Open WebUI](../services/open-webui.md)
- [Ollama](../services/ollama.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [RAG Pattern](./patterns/rag-pattern.md) — Underlying architectural concept.
- [Agentic Workflows](./patterns/agentic-workflows.md) — For multi-step troubleshooting logic.
- [n8n](../services/n8n.md) — For orchestrating manual ingestion pipelines.
- [Weaviate](../infrastructure/weaviate.md) — Recommended vector store for local manual embeddings.
- [Verba](../intake_storage/verba.md) — Alternative RAG UI focused on Weaviate.
- [Manual Assistant Implementation](../reference-implementations/manual-assistant/manual-assistant-implementation.md) — Reference backend code.
- [Multi-modal Reasoning](./patterns/extraction-and-classification.md) — For interpreting diagrams.

## Sources / references
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Agentic RAG Patterns 2026](https://www.digitalapplied.com/blog/agentic-rag-patterns-multi-step-reasoning-guide)
- [Anthropic Tool Use (MCP)](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
