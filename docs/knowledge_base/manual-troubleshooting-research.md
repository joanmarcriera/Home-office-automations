# Manual Troubleshooting Assistant Research

## What it is
This research evaluates the user interface and orchestration layer for a chat-based assistant designed to troubleshoot household appliances using scanned manuals. It leverages Retrieval-Augmented Generation (RAG) over a local vector database.

Key components evaluated in June 2026:
- **UI Frameworks**: Comparison between Open WebUI and Streamlit for family use.
- **RAG Orchestration**: Integration with Ollama and local embedding models.
- **Agentic Loops**: Implementation of self-healing loops for autonomous remediation.

## What problem it solves
Scanned manuals are often long, poorly indexed, and difficult to search during a "household emergency" (e.g., a leaking dishwasher). This assistant provides immediate, natural language answers to specific troubleshooting questions, reducing time-to-fix.

## Where it fits in the stack
**User Interface / Orchestration Layer**. It connects the user to local LLMs (Claude 4.8 or GPT-5.5) and the Vector DB containing chunked manual data.

## Typical use cases
- Interpreting cryptic error codes on the oven or washing machine.
- Finding maintenance schedules (e.g., "how often to clean the dryer vent?").
- Step-by-step guidance for minor repairs or setup.
- Comparing troubleshooting steps across different model generations.

## Strengths
- **Accessibility**: Family members can ask questions via phone or tablet without technical knowledge.
- **Privacy**: Entirely self-hosted when using local LLMs and embeddings.
- **Accuracy**: RAG reduces hallucinations by grounding the LLM in the actual text of the manual.
- **Frontier Support**: Optimized for Claude 4.8 and GPT-5.5 reasoning patterns.

## Limitations
- **OCR Quality**: Poorly scanned manuals may lead to incorrect information retrieval.
- **Complex Diagrams**: LLMs may struggle to interpret "Figure 1.2" if the diagram isn't correctly indexed or provided as VLM context.

## When to use it
- For any household appliance with a digital or physical manual.
- When troubleshooting non-dangerous issues that don't require immediate professional intervention.

## When not to use it
- **Dangerous Repairs**: High-voltage electrical work or gas line issues should always be handled by professionals.
- **Time-Critical Safety**: Do not use the assistant if there is a fire or immediate safety risk.

## Getting started
### Environment Setup
1. Ensure Open WebUI or Streamlit is installed and connected to your local LLM provider (e.g., Ollama).
2. Prepare your appliance manuals in PDF format.
3. Configure your vector database (e.g., ChromaDB) for document ingestion.

### Basic Assistant Query
```bash
# Example query to the troubleshooting assistant via CLI
python3 scripts/home_admin_agent.py "Why is my Bosch dishwasher flashing E24?"
```

## CLI examples
The research implementation can be tested and managed via CLI.

```bash
# Start the reference implementation (Streamlit-based)
streamlit run scripts/home_admin_ui.py

# Index a new manual into the vector database
python3 scripts/process_manuals.py --file manuals/bosch_dishwasher.pdf

# Test the RAG retrieval without the UI
python3 scripts/verify_manual_retrieval.py "E24 error code meaning"
```

## API examples
The assistant can be integrated into larger workflows via API.

```python
import requests

def get_troubleshooting_help(query):
    # Example endpoint for the home admin agent (June 2026 pattern)
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"message": query, "context_tags": ["manuals"]}
    )
    return response.json()["answer"]
```

## Related tools / concepts
- [Open WebUI](../services/open-webui.md)
- [Ollama](../services/ollama.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [RAG Pattern](./patterns/rag-pattern.md)
- [n8n](../services/n8n.md)
- [ChromaDB](./vector-db-comparison.md)
- [Self-Healing Agent](./self-healing-agent-research.md)
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md)

## Sources / References
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Self-Healing Agentic Loops for Homelab Automation](https://riera.co.uk/blog/self-healing-agents)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high
