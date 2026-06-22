# Msty

## What it is
Msty is a local-first AI desktop application designed to provide a professional, privacy-centric workspace for interacting with both local models (via Ollama/Llama.cpp/MLX) and cloud-based AI providers. As of June 2026, Msty has evolved into **Msty Studio**, a comprehensive platform that supports advanced multi-agent orchestration, complex RAG pipelines, and deep integration with the Model Context Protocol (MCP 3.0).

## What problem it solves
It eliminates the friction of managing disparate AI tools by providing a unified, professional-grade interface. It solves the privacy concerns associated with cloud-only AI by prioritizing local inference while maintaining the flexibility to use frontier models like Claude 4.8 and GPT-5.5 when needed. Its "Knowledge Stacks" and "Model Matchmaker" solve the complexity of RAG and hardware optimization for local LLMs.

## Where it fits in the stack
**Infrastructure / AI Desktop App**. In the [Home-Office Architecture](../../architecture/README.md), it acts as the primary **Interaction Layer** for desktop users, bridging the gap between local compute and global AI APIs.

## Typical use cases
- **Private Local Research**: Utilizing "Knowledge Stacks Next Gen" to perform RAG on sensitive local documents without data leaving the machine.
- **Agentic Multi-Step Tasks**: Using "Agent Mode" to complete complex workflows by allowing models to use MCP-enabled tools.
- **Collaborative Crews**: Setting up "Crew Conversations" where multiple specialized personas (e.g., Architect, Developer, Reviewer) work together on a problem.
- **Model Benchmarking**: Using "Split Chat" and "Forge Mode" to compare responses from different local and cloud models side-by-side.

## Strengths
- **Native MCP 3.0 Support**: Deep integration with the Model Context Protocol allows agents to use a vast ecosystem of tools.
- **Optimized Local Inference**: Advanced support for Apple Silicon (MLX) and NVIDIA (CUDA), with a built-in "Model Matchmaker" for hardware tuning.
- **High-Fidelity RAG**: "Knowledge Stacks" provides sophisticated chunking, vectorization, and visualization of local knowledge bases.
- **Privacy First**: Local-first design with secrets encryption and no telemetry by default.

## Limitations
- **Proprietary Core**: The main Msty Studio application is closed-source.
- **Licensing**: Advanced enterprise features (Remote Connections, Amazon Bedrock/Azure support, SSO) require an "Aurum" license.
- **Hardware Dependent**: Performance for local models is strictly limited by the user's VRAM and compute capabilities.

## When to use it
- When you need a professional, reliable UI for daily AI interactions that supports both local and cloud models.
- When you want to build and manage local RAG "Knowledge Stacks" with high precision.
- When you need an AI desktop app that can orchestrate multi-agent "Crews."

## When not to use it
- If you require a strictly 100% open-source stack (see [Jan.ai](jan-ai.md)).
- If you are building a web-only collaborative platform for a large distributed team (see [LobeHub](../ai_knowledge/lobehub.md)).

## Getting started
1. Download Msty Studio from the [official site](https://msty.ai/).
2. Use the **Model Hub** to download a local model or configure online providers with your API keys.
3. (Optional) Create a **Knowledge Stack** by importing your local documents for RAG-augmented conversations.
4. Enable **Agent Mode** in settings to allow models to use installed MCP tools from the **Toolbox**.

## CLI examples
Msty Studio includes a CLI for proxying and headless integration.

```bash
# Launch Msty into a specific workspace
msty --workspace "Development"

# Use the Vibe CLI Proxy to route local model requests
vibe serve --model "llama-3.1-8b" --port 5050

# Calculate VRAM requirements for a local GGUF model
msty vram-calc ./models/deepseek-v3.gguf
```

## API examples
Msty Studio provides an OpenAI-compatible API that can be consumed by external agents or applications.

```python
import openai

# Msty default local server port
client = openai.OpenAI(base_url="http://localhost:5050/v1", api_key="msty")

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Analyze my Knowledge Stack for trends in Q2."}]
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [Jan.ai](jan-ai.md) — Open-source local AI alternative.
- [LM Studio](lm-studio.md) — Specialized local model manager.
- [Ollama](../../services/ollama.md) — Backend inference engine often used by Msty.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The protocol powering Msty's Toolbox.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Alternative RAG-focused desktop app.
- [LobeHub](../ai_knowledge/lobehub.md) — Multi-model chat interface with plugin support.
- [GPT Researcher](../agents/gpt-researcher.md) — Agentic research tool that can integrate with Msty.

## Sources / references
- [Msty Official Website](https://msty.ai/)
- [Msty Studio Documentation](https://docs.msty.ai/studio/)
- [Msty Changelog](https://msty.ai/changelog)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
