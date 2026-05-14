# Manual Troubleshooting Assistant Research

## What it is
This research evaluates the user interface and orchestration layer for a chat-based assistant designed to troubleshoot household appliances using scanned manuals. It leverages Retrieval-Augmented Generation (RAG) over a local vector database.

## What problem it solves
Scanned manuals are often long, poorly indexed, and difficult to search during a "household emergency" (e.g., a leaking dishwasher). This assistant provides immediate, natural language answers to specific troubleshooting questions.

## Where it fits in the stack
It sits in the **User Interface / Orchestration** layer, connecting the user to the local LLM and the Vector DB containing chunked manual data.

## Typical use cases
- Interpreting cryptic error codes on the oven or washing machine.
- Finding maintenance schedules (e.g., "how often to clean the dryer vent?").
- Step-by-step guidance for minor repairs or setup.

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
- **Accessibility**: Family members can ask questions via phone or tablet without technical knowledge.
- **Privacy**: Entirely self-hosted when using local LLMs and embeddings.
- **Accuracy**: RAG reduces hallucinations by grounding the LLM in the actual text of the manual.

## Limitations
- **OCR Quality**: Poorly scanned manuals may lead to incorrect information retrieval.
- **Complex Diagrams**: LLMs may struggle to interpret "Figure 1.2" if the diagram isn't correctly multi-modally indexed.

## When to use it
- For any household appliance with a digital or physical manual.
- When troubleshooting non-dangerous issues that don't require immediate professional intervention.

## When not to use it
- **Dangerous Repairs**: High-voltage electrical work or gas line issues should always be handled by professionals.
- **Time-Critical Safety**: Do not use the assistant if there is a fire or immediate safety risk.

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
- [RAG (Retrieval-Augmented Generation)](./patterns/rag.md)
- [n8n](../services/n8n.md) — For orchestrating manual ingestion pipelines.
- [ChromaDB](./vector-db-comparison.md) — For storing and searching manual embeddings.
- [Manual Assistant Implementation](../reference-implementations/manual-assistant/manual-assistant-implementation.md) — Reference backend code.

## Sources / references
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Contribution Metadata
- Last reviewed: 2026-05-14
- Confidence: high
