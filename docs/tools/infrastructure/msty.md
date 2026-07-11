# Msty

## What it is
Msty is a local-first AI desktop application designed to provide a professional, offline-capable workspace for interacting with both local models (via Ollama/Llama.cpp) and cloud-based AI providers. Since the release of Msty Claw (v0.10.x in June 2026), it has evolved into a modular "AI Operating System" featuring a robust extension ecosystem and deep integration with the **MCP 3.0** standard.

## What problem it solves
It simplifies the process of running and managing local LLMs, providing tools like a VRAM calculator and a model hub, while maintaining the flexibility to route complex queries to powerful cloud models. It addresses "context noise" through modular Memory Packs and provides a controlled environment for multi-agent "Crew Conversations," leveraging the **MCP 3.0 Task Protocol** for distributed tool execution.

## Where it fits in the stack
**Infrastructure / AI Desktop App**. It serves as the primary local interface for model orchestration, RAG, and agentic workflows on the desktop, acting as a host for MCP servers and agentic sessions.

## Typical use cases
- **Private Local Chat**: Running [Gemma 3](../ai_knowledge/local_llms.md) or Llama 3.1 models entirely offline for sensitive data.
- **Multi-Agent Orchestration**: Using "Crew Conversations" in Msty Studio to simulate team-based problem solving with specialized AI experts.
- **Modular Knowledge Management**: Organizing documents into "Knowledge Stacks" for precise, stack-specific RAG.
- **Capability Extension**: Using the "Discover Hub" to install third-party Skills, Turnstiles, and Workflows via the Claw extension system.

## Strengths
- **Modular Extensions**: Support for custom tools, workflows, themes, and agent harness controls via the Claw extension system.
- **Professional Governance**: Features like "Persona Studio" allow teams to design, test, and scale consistent AI behaviors.
- **Local-First Design**: Deep integration for Apple Silicon (M5 optimized) and local inference engines with a consolidated "One Local Model Hub."
- **Focus on Memory**: "Memory Packs" ensure that AI context stays focused, reusable, and optional, preventing long-term context degradation.

## Limitations
- **Proprietary Core**: While it supports open-source extensions, the core application remains closed-source.
- **Hardware Dependent**: Local performance is strictly limited by the user's GPU VRAM (though the "Matchmaker" helps mitigate this).
- **Licensing**: Advanced enterprise features (SSO, Azure/Bedrock) require a paid "Aurum" license.

## When to use it
- When you need a professional-grade, local-first workspace that supports both local and cloud models.
- When your workflow involves multi-agent collaboration (Crews) and complex RAG (Knowledge Stacks).
- If you value a modular ecosystem where you can add specific "Skills" and "Workflows" via a hub.
- When you require a native host for **MCP 3.0** servers and task orchestration.

## When not to use it
- If you strictly require a 100% open-source stack from the core up.
- For lightweight, single-model needs where a simple CLI like Ollama or a thin wrapper might suffice.
- If you prefer a web-based multi-user interface over a local desktop application.

## Getting started
1. **Download**: Obtain the latest version from [msty.ai](https://msty.ai/).
2. **Setup**: Launch the app and use the "Discover Hub" to browse available Skills and Knowledge Stacks.
3. **Models**: Use the "One Local Model Hub" to download and configure local models like [Gemma 3](../ai_knowledge/local_llms.md); the "Matchmaker" will recommend models based on your hardware.
4. **Extend**: Visit the Extensions gallery to add support for web search, URL reading, or native **MCP 3.0** servers.

## CLI examples
Msty supports command-line arguments for automation and quick-launching specific personas or agents.

```bash
# Launch Msty with a specific persona active
msty --persona "Security Auditor"

# Run in headless mode to serve as a local API backend
msty --headless --port 5050

# Calculate VRAM requirements for a local GGUF file
msty calculate-vram ~/models/gemma-3-27b.gguf
```

## API examples
Msty provides an OpenAI-compatible API (typically on port 5050) to allow other tools to leverage its managed models and Knowledge Stacks.

```python
import openai

# Connect to Msty's local inference server
client = openai.OpenAI(base_url="http://localhost:5050/v1", api_key="msty")

response = client.chat.completions.create(
    model="knowledge-stack-finance", # Route query through a specific Knowledge Stack
    messages=[{"role": "user", "content": "Summarize the Q2 tax implications."}]
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [Jan.ai](jan-ai.md) — Open-source local-first alternative.
- [LM Studio](lm-studio.md) — Popular local model explorer.
- [Ollama](../../services/ollama.md) — Core local inference engine.
- [GPT Researcher](../agents/gpt-researcher.md) — Can be used as a skill within Msty.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Alternative for desktop RAG.
- [LobeHub](../ai_knowledge/lobehub.md) — Modern web-based AI interface.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for Msty's tool and server integration (MCP 3.0).
- [Local LLMs (Gemma 3)](../ai_knowledge/local_llms.md) — Canonical source for local reasoning engines.

## Sources / references
- [Msty Official Site](https://msty.ai/)
- [Msty Claw Changelog](https://msty.ai/claw/changelog/)
- [Msty Blog: Memory Packs and Crews](https://msty.ai/blog/)
- [MCP 3.0 Desktop Integration Guide](https://modelcontextprotocol.io/docs/desktop/msty)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
