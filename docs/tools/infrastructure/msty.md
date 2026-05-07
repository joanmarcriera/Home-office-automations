# Msty

## What it is
Msty is a local-first AI desktop application designed to provide a professional, offline-capable workspace for interacting with both local models (via Ollama/Llama.cpp) and cloud-based AI providers.

## What problem it solves
It simplifies the process of running and managing local LLMs, providing tools like a VRAM calculator and a model hub, while maintaining the flexibility to route complex queries to powerful cloud models.

## Where it fits in the stack
**Category**: Infrastructure / AI Desktop App

## Typical use cases
- **Private Local Chat**: Running Llama 3 or Qwen models entirely offline for sensitive data.
- **Model Comparison**: Testing how different local and cloud models handle the same prompt in a side-by-side view.
- **Workflow Automation**: Using its "Turnstiles" feature and MCP tools to automate recurring tasks.

## Strengths
- **Developer-Friendly Tools**: Includes a built-in VRAM calculator, model cost estimator, and model "Matchmaker".
- **Local-First Design**: Optimized for local inference with deep integration for Ollama and Apple Silicon (MLX).
- **Rich Feature Set**: Supports Persona/Crew conversations, Knowledge Stacks (RAG), and a robust skill ecosystem.

## Limitations
- **Proprietary**: The core application is closed-source.
- **Paid Tier**: Advanced enterprise-grade features (Azure/Bedrock support, SSO) are locked behind an "Aurum" license.

## When to use it
- When you want the easiest possible path to running powerful local models on your desktop.
- When you need professional-grade features like RAG and multi-agent "Crews" in a local app.

## When not to use it
- If you strictly require open-source software.
- If you are looking for a web-based, collaborative platform for a large team (see [LobeHub](lobehub.md)).

## Getting started
1. Download Msty from [msty.ai](https://msty.ai/).
2. Launch the app and use the "Model Hub" to download a local model.
3. Create a "Collection" to organize your chats and documents for RAG.
4. Use the "Matchmaker" tool to find the best model for your specific hardware configuration.

## CLI examples
Msty is primarily GUI-driven, but it supports command-line arguments for quick launching and integration.

```bash
# Launch Msty directly into a specific persona chat
msty --persona "Code Specialist"

# Launch in "Headless" mode for API background serving
msty --headless --port 8080

# Check VRAM requirements for a specific model file
msty calculate-vram ./models/llama-3-8b.gguf
```

## API examples
Msty provides an OpenAI-compatible API that can be enabled in settings.

```python
import openai

# Msty typically hosts its local server on port 5050 by default
client = openai.OpenAI(base_url="http://localhost:5050/v1", api_key="msty")

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Analyze this CSV for trends."}]
)
print(response.choices[0].message.content)
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (Core features) / Paid (Aurum license for advanced features)
- **Self-hostable**: Yes (Local application)

## Related tools / concepts
- [Jan.ai](../infrastructure/jan-ai.md)
- [LM Studio](../infrastructure/lm-studio.md)
- [Ollama](../../services/ollama.md)
- [GPT Researcher](../agents/gpt-researcher.md)
- [AnythingLLM](../ai_knowledge/anythingllm.md)
- [LobeHub](../ai_knowledge/lobehub.md)

## Sources / References
- [Msty Official Site](https://msty.ai/)
- [Msty Documentation](https://docs.msty.ai/)

## Contribution Metadata
- Last reviewed: 2026-06-01
- Confidence: high
