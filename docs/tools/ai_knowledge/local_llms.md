# Local LLMs (Ollama, MLX, llama.cpp)

## What it is
Tools and frameworks that allow running Large Language Models directly on your own hardware (Homelab, Workstation, Mac). By June 2026, the local ecosystem is characterized by the dominance of **Small Language Models (SLMs)**, **Local Multimodal** capabilities, and native **MCP 3.0** integration for tool use. Key players include Ollama (the industry standard), MLX (Apple Silicon optimization), llama.cpp (the foundational engine), and LM Studio (the premier GUI).

## What problem it solves
It provides **100% data sovereignty**, eliminates recurring token costs, and ensures availability during internet outages. It allows for the processing of sensitive personal or corporate data that cannot be sent to cloud providers like OpenAI or Anthropic due to privacy, security, or compliance requirements. It also enables high-frequency agentic loops without the latency or cost of cloud APIs.

## Where it fits in the stack
**LLM / Reasoning Engine (Self-hosted)**. It serves as the local intelligence layer in the [KnowledgeOps](../../architecture/README.md) stack, replacing or augmenting cloud providers. It interacts with the [Persistence Layer](../infrastructure/index.md) and provides tools to agents via [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## Typical use cases
- **Private Coding Assistance**: Running code-specialized models locally via [Claude Code](../development_ops/claude-code.md) or [Windsurf](../development_ops/codeium.md).
- **Sensitive Data Analysis**: Indexing and querying private documents without external data leakage.
- **Agentic Pre-processing**: Using small local models (e.g., Llama 3.2 3B) for classification and routing before escalating to [Claude 4.8](../ai_knowledge/claude.md) or [GPT-5.5](../ai_knowledge/openai.md).
- **Offline Agentic Missions**: Executing multi-step tasks in air-gapped or low-connectivity environments.
- **Hardware Benchmarking**: Testing the performance of M5 or Blackwell hardware with various quantization levels.

## Strengths
- **Data Sovereignty**: Complete control over your data and model weights.
- **Cost Efficiency**: Zero cost per token after the initial hardware investment.
- **Low Latency**: Eliminates network round-trip time, enabling faster "Time to First Token" (TTFT).
- **Customizability**: Easy to swap models, adjust quantization, and use specialized fine-tunes.
- **MCP 3.0 Native**: (June 2026) Local servers now support standardized tool calling out of the box.

## Limitations
- **Reasoning Ceiling**: Even the best local models (e.g., Llama 3.1 405B) may struggle with the most complex multi-step reasoning compared to cloud-hosted [Claude 4.8](../ai_knowledge/claude.md).
- **Hardware Requirements**: High-performance inference requires significant VRAM or Unified Memory (e.g., M5 Ultra with 192GB+).
- **Configuration Overhead**: Optimizing performance for specific hardware still requires more technical effort than cloud APIs.

## When to use it
- When handling PII, health records, or proprietary corporate IP.
- For high-volume tasks like summarization, formatting, or basic data extraction.
- When building "local-first" or air-gapped agentic systems.
- For development and debugging of [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) tools and agentic loops.

## When not to use it
- When the task requires the absolute frontier of logical reasoning or world knowledge (prefer [Claude 4.8](../ai_knowledge/claude.md) or [GPT-5.5](../ai_knowledge/openai.md)).
- When you have insufficient hardware (e.g., < 8GB VRAM or < 16GB RAM).
- When you need a massive 2M+ token context window that exceeds local hardware capacity (prefer [Gemini 3.5](../ai_knowledge/gemini.md)).

## Getting started
1. **Ollama**: Install the standard for local management: `curl -fsSL https://ollama.com/install.sh | sh`.
2. **Run a Model**: Start your first model: `ollama run llama3.2`.
3. **GUI Interface**: For a visual experience, install [LM Studio](../infrastructure/lm-studio.md) or [Jan.ai](../infrastructure/jan-ai.md).
4. **Tool Access**: Configure an [Model Context Protocol (MCP) 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) server to give your local models tool-calling capabilities.

## CLI examples
```bash
# List local models
ollama list

# Run a specific model with vision support
ollama run llama3.2-vision

# Start the OpenAI-compatible local server
ollama serve

# Using the LM Studio CLI (lms) to manage models
lms status
lms get meta-llama-3.1-8b
```

## API examples
### Python: OpenAI-Compatible Interface
```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:11434/v1", # Default Ollama endpoint
    api_key="ollama" # Required by SDK but ignored by local server
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Explain the benefit of MCP 3.0 for local agents."}]
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](../infrastructure/lm-studio.md)
- [MLX](../infrastructure/mlx.md)
- [Jan.ai](../infrastructure/jan-ai.md)
- [Msty](../infrastructure/msty.md)
- [Claude Code](../development_ops/claude-code.md)
- [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Open WebUI](../../services/open-webui.md)
- [AnythingLLM](https://docs.useanything.com/introduction)

## Sources / References
- [Ollama Library](https://ollama.com/library)
- [LM Studio CLI Documentation](https://lmstudio.ai/docs/cli)
- [MLX-LM Repository](https://github.com/ml-explore/mlx-examples)
- [Llama 3.2 Vision Announcement](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)
- [LocalAI Blog: Announcing MCP Support](https://localai.io/blog/mcp-support/)
- [CatMind-12B](https://www.reddit.com/r/LocalLLaMA/comments/1uzxov4/model_catmind12b/) — Integrated from daily log reference.
- [Inkling](https://www.reddit.com/r/LocalLLaMA/comments/1uxdv34/thinking_machines_releases_first_openweight_model/) — Integrated from daily log reference.


## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
