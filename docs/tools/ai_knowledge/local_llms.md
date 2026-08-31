# Local LLMs (Ollama, MLX, llama.cpp)

## What it is
Tools and frameworks that allow running Large Language Models directly on your own hardware (Homelab, Workstation, Mac). By early January 2027, the local ecosystem is characterized by the dominance of high-capability **Small Language Models (SLMs)**, native **Local Multimodal / Vision-Audio** capabilities, and native **FastMCP 3.1** protocol integration. Highly optimized engines like [ExLlamaV3](../infrastructure/exllamav3.md) and foundation engines like [llama.cpp](../infrastructure/llama-cpp.md) run cutting-edge open-weights models (such as Llama 4, Gemma 3, and Qwen 3.8) locally at high tokens-per-second.

## What problem it solves
It provides **100% data sovereignty**, eliminates recurring API token costs, and guarantees availability during internet outages or cloud rate limits. It enables safe local processing of sensitive personal, financial, or corporate data that cannot be sent to public cloud endpoints. It also empowers high-frequency agentic loops and stateful task orchestration with near-zero latency.

## Where it fits in the stack
**LLM / Reasoning Engine (Self-hosted)**. It serves as the local intelligence layer in the KnowledgeOps stack, replacing or augmenting cloud providers. It interacts with local vector stores (such as [Chroma](../infrastructure/chroma.md) or [Milvus](../infrastructure/milvus.md)) and exposes capabilities to local agents via [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## Typical use cases
- **Private Coding Assistance**: Running code-specialized models locally via [Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), or [Windsurf](../development_ops/windsurf.md).
- **Sensitive Document Analysis**: Indexing and querying confidential documents without external data exposure using local RAG.
- **Agentic Pre-processing**: Utilizing small local models (e.g., Llama 4 8B or Gemma 3 12B) for task classification and intent routing before escalating complex reasoning to [GPT-5.5](openai.md) or [Claude](claude.md).
- **Offline Agentic Workflows**: Executing multi-step automation in air-gapped or low-connectivity environments.
- **Hardware Benchmarking**: Evaluating local inference performance with quantization formats like EXL3 or GGUF on local GPUs or Apple Silicon.

## Strengths
- **Complete Data Sovereignty**: Absolute governance over data, system prompts, and model weights.
- **Cost Efficiency**: Zero cost per token after initial hardware provisioning.
- **Low Latency**: Minimizes network round-trip delay, enabling fast "Time to First Token" (TTFT).
- **Extensive Customizability**: Effortless model swapping, custom quantizations, and local fine-tuning.
- **FastMCP 3.1 Native**: Direct integration with FastMCP 3.1 servers for real-time tool calling and resource access.

## Limitations
- **Reasoning Ceiling**: Open-weights local models may lag behind top-tier frontier models like [Claude 5.1](claude.md) or [GPT-5.5](openai.md) on complex multi-step reasoning.
- **Hardware Requirements**: High-throughput inference requires significant VRAM or Apple Unified Memory (e.g., 64GB–192GB+ for 70B+ models).
- **Configuration Overhead**: Fine-tuning context lengths, GPU layer offloading, and memory footprints requires technical familiarity.

## When to use it
- When handling PII, health records, or sensitive intellectual property.
- For high-volume, repetitive tasks like classification, extraction, or basic code formatting.
- When building air-gapped or offline-resilient AI agent systems.
- For developing and testing [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) servers and tool schemas locally.

## When not to use it
- When tasks demand frontier reasoning capabilities or massive multi-modal knowledge bases (prefer [Claude](claude.md) or [GPT-5.5](openai.md)).
- When local hardware is constrained (e.g., < 8GB VRAM / RAM).
- When requiring multi-million token context windows exceeding local RAM limits (prefer [Gemini](gemini.md)).

## Getting started
1. **Ollama**: Install the standard local model runtime: `curl -fsSL https://ollama.com/install.sh | sh`.
2. **Run a Model**: Pull and run a modern model: `ollama run llama4`.
3. **GUI Interface**: For a visual dashboard, deploy [LM Studio](../infrastructure/lm-studio.md) or [Jan.ai](../infrastructure/jan-ai.md).
4. **Tool Access**: Connect your local runtime to a [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) server for structured tool interaction.

## CLI examples
```bash
# List local models
ollama list

# Run a vision-capable local model
ollama run llama4-vision

# Start local OpenAI-compatible API server
ollama serve

# Using LM Studio CLI (lms) for model management
lms status
lms get qwen3.8-32b
```

## API examples
### Python: OpenAI-Compatible Interface with Local LLM & Pydantic v2
```python
from typing import List
from pydantic import BaseModel, Field
import openai

class LocalAnalysisResult(BaseModel):
    summary: str = Field(description="Summary of the local text analysis")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0")
    key_topics: List[str] = Field(description="Extracted key topics")

client = openai.OpenAI(
    base_url="http://localhost:11434/v1",  # Local Ollama endpoint
    api_key="ollama"                       # Unused key placeholder
)

response = client.chat.completions.create(
    model="llama4",
    messages=[
        {"role": "system", "content": "Analyze the text and return key insights."},
        {"role": "user", "content": "Local LLMs provide data sovereignty and FastMCP 3.1 tool access."}
    ],
    temperature=0.2
)

# Parse output into Pydantic model
raw_content = response.choices[0].message.content
print("Model Response:", raw_content)
```

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](../infrastructure/lm-studio.md)
- [MLX](../infrastructure/mlx.md)
- [Jan.ai](../infrastructure/jan-ai.md)
- [Msty](../infrastructure/msty.md)
- [Claude Code](../development_ops/claude-code.md)
- [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Open WebUI](../../services/open-webui.md)
- [AnythingLLM](anythingllm.md)
- [ExLlamaV3](../infrastructure/exllamav3.md)
- [LlamaIndex.TS](llamaindex-ts.md)

## Sources / References
- [Ollama Library](https://ollama.com/library)
- [LM Studio Documentation](https://lmstudio.ai/docs)
- [MLX-LM Repository](https://github.com/ml-explore/mlx-examples)
- [Meta Llama 4 Release Notes](https://ai.meta.com/llama/)
- [CatMind-12B](https://www.reddit.com/r/LocalLLaMA/comments/1uzxov4/model_catmind12b/) — Integrated from daily log reference.
- [Inkling](https://www.reddit.com/r/LocalLLaMA/comments/1uxdv34/thinking_machines_releases_first_openweight_model/) — Integrated from daily log reference.
- [GS1-1T Model Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1v3q47x/genesisscience1_gs1_1t_openweight_model_later/) — Open-weight 1-Trillion parameter model.
- [G9V-33B Model Release](https://www.reddit.com/r/LocalLLaMA/comments/1v46ay5/ai9stars_released_g9v33b/) — 33B local open LLM model.
- [Microsoft Fara-1527B on Hugging Face](https://www.reddit.com/r/LocalLLaMA/comments/1v3ny84/microsoftfara1527b_hugging_face/) — Large open-weights model family.
- [Apodex 1.1 Team AMA on Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vzxdui/were_the_team_behind_apodex_11_ask_us_anything/) — AI local tooling and framework discussion.
- [Hugging Face MicroDuck Robot](https://thenewstack.io/hugging-face-microduck-robot/) — Robotics-focused AI model/tool from Hugging Face.

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
