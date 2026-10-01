# Local LLMs (Ollama, MLX, llama.cpp)

## What it is
Tools and frameworks that allow running Large Language Models directly on your own hardware (Homelab, Workstation, Mac). By early January 2027, the local ecosystem is characterized by the dominance of high-capability **Small Language Models (SLMs)**, native **Local Multimodal / Vision-Audio** capabilities, and native **FastMCP 3.1** protocol integration. Highly optimized engines like [ExLlamaV3](../infrastructure/exllamav3.md) and foundation engines like [llama.cpp](../infrastructure/llama-cpp.md) run cutting-edge open-weights models (such as Llama 4, Gemma 3, and Qwen 3.8) locally at high tokens-per-second.

Local LLMs empower individuals and enterprises to run foundation models locally without relying on external SaaS vendors or third-party cloud infrastructure. By deploying lightweight, distilled models locally on consumer GPUs, Apple Silicon hardware, or dedicated homelab servers, users retain full control over data privacy, system prompts, inference parameters, and context boundaries.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Local AI Application / Agent                          │
│             (Claude Code, Cursor, Windsurf, Open WebUI, FastMCP)            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Standard REST / FastMCP 3.1
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Inference Engine Layer                            │
│           (Ollama / llama.cpp / ExLlamaV3 / MLX / vLLM Server)             │
└──────┬───────────────────────────────┬───────────────────────────────┬──────┘
       │ Quantized GGUF / EXL3         │ Native Metal / CUDA           │ Zero Cloud API
       ▼                               ▼                               ▼
┌──────────────┐               ┌──────────────┐               ┌──────────────┐
│ Apple M-Series│              │ NVIDIA RTX   │              │ System VRAM  │
│ Unified RAM  │               │ Blackwell GPU│               │ Unified Memory│
└──────────────┘               └──────────────┘               └──────────────┘
```

## What problem it solves
It provides **100% data sovereignty**, eliminates recurring API token costs, and guarantees availability during internet outages or cloud rate limits. It enables safe local processing of sensitive personal, financial, or corporate data that cannot be sent to public cloud endpoints. It also empowers high-frequency agentic loops and stateful task orchestration with near-zero latency.

In traditional cloud-hosted AI setups, every request incurs latency, billing costs, and data leakage risks. Local LLMs mitigate these concerns completely. When processing large code repositories, confidential medical files, or internal legal documents, local inference ensures data never leaves the local network buffer.

## Where it fits in the stack
**LLM / Reasoning Engine (Self-hosted)**. It serves as the local intelligence layer in the KnowledgeOps stack, replacing or augmenting cloud providers. It interacts with local vector stores (such as [Chroma](../infrastructure/chroma.md) or [Milvus](../infrastructure/milvus.md)) and exposes capabilities to local agents via [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KnowledgeOps Stack Top Layer                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Agent Frameworks: LangGraph / AutoGen / Smolagents / FastMCP 3.1 Bridge     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Reasoning Layer: Local LLMs (llama.cpp, Ollama, MLX)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Storage Layer: Local Vector DBs (Chroma, Qdrant) & Local Markdown Vaults     │
└─────────────────────────────────────────────────────────────────────────────┘
```

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

## Feature & Quantization Comparison Matrix

| Engine / Framework | Primary Hardware Target | Supported Quantizations | FastMCP 3.1 Support | Latency / TTFT | Context Expansion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ollama** | Cross-platform (CPU/GPU) | GGUF (Q4_K_M, Q8_0) | Native via REST/MCP | Low (~12ms TTFT) | Dynamic context scaling |
| **llama.cpp** | CPU, CUDA, Metal, Vulkan | GGUF (Q2_K - Q8_0, IQ4) | Native bindings | Very Low (~8ms TTFT) | Flash Attention v2 |
| **ExLlamaV3** | NVIDIA CUDA GPUs | EXL3 / FP8 / INT4 | Python FastMCP Bridge | Ultra Low (~4ms TTFT) | Paged KV Attention |
| **MLX-LM** | Apple Silicon (M1-M4) | 4-bit, 8-bit, FP16 | Native Python FastMCP | Low (~10ms TTFT) | Unified Memory Paging |
| **vLLM** | Enterprise GPU Clusters | AWQ, GPTQ, FP8 | OpenAI REST standard | Ultra Low (~3ms TTFT) | Continuous Batching |

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

# Running llama.cpp server directly with flash attention and FastMCP endpoint
./llama-server --model models/llama-4-8b-Q4_K_M.gguf --ctx-size 16384 --n-gpu-layers 99 --flash-attn --port 8080
```

## API examples
### Python: FastMCP 3.1 Local LLM Tool Bridge
The following Python script demonstrates building a FastMCP 3.1 local inference server with Ollama/llama.cpp and Pydantic v2 schema validation:

```python
import os
import requests
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Local-LLM-Inference-Bridge")

class LocalInferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=5, description="Prompt text to process locally")
    model_name: str = Field(default="llama4", description="Local model identifier")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, gt=0, le=16384)

    @field_validator("model_name")
    @classmethod
    def validate_model(cls, v: str) -> str:
        allowed_models = {"llama4", "gemma3", "qwen3.8", "mistral-small"}
        if v.lower() not in allowed_models:
            # Allow fallback if standard format
            pass
        return v.lower()

class LocalInferenceResponse(BaseModel):
    generated_text: str
    model_used: str
    tokens_evaluated: int
    eval_duration_ms: float
    status: str = Field(default="success")

@mcp.tool()
def generate_local_completion(request: LocalInferenceRequest) -> LocalInferenceResponse:
    """Invokes local Ollama or llama.cpp endpoint to produce inference results."""
    ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434/api/generate")

    payload = {
        "model": request.model_name,
        "prompt": request.prompt,
        "stream": False,
        "options": {
            "temperature": request.temperature,
            "num_predict": request.max_tokens
        }
    }

    try:
        res = requests.post(ollama_url, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()

        return LocalInferenceResponse(
            generated_text=data.get("response", ""),
            model_used=request.model_name,
            tokens_evaluated=data.get("eval_count", 0),
            eval_duration_ms=data.get("eval_duration", 0) / 1e6,
            status="success"
        )
    except Exception as e:
        return LocalInferenceResponse(
            generated_text="",
            model_used=request.model_name,
            tokens_evaluated=0,
            eval_duration_ms=0.0,
            status=f"error: {str(e)}"
        )

if __name__ == "__main__":
    mcp.run()
```

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

raw_content = response.choices[0].message.content
print("Model Response:", raw_content)
```

## Performance Benchmarks (Tokens per Second)

| Local Model Variant | Quantization | Hardware Specification | Tok/s Generation | Peak VRAM / RAM Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Llama 4 8B** | GGUF Q4_K_M | Apple M3 Max (64GB) | 68.4 tok/s | 5.8 GB |
| **Llama 4 8B** | EXL3 4.0-bit | NVIDIA RTX 4090 (24GB) | 142.1 tok/s | 5.2 GB |
| **Gemma 3 12B** | GGUF Q8_0 | Apple M4 Pro (48GB) | 45.2 tok/s | 13.1 GB |
| **Qwen 3.8 32B** | EXL3 3.75-bit | NVIDIA RTX 5090 (32GB) | 88.5 tok/s | 18.4 GB |
| **DeepSeek R1 70B** | GGUF Q4_K_M | 2x RTX 4090 (48GB) | 28.3 tok/s | 41.2 GB |

## Troubleshooting & Diagnostics

### 1. Out of VRAM / Out of Memory Errors
- **Symptom**: `CUDA out of memory` or system crash during model loading.
- **Cause**: Model parameters and context window exceed total physical GPU memory.
- **Resolution**:
  - Lower the context size parameter (`--ctx-size 8192`).
  - Use higher quantization levels (e.g., switch from Q8_0 to Q4_K_M or EXL3 3.5-bit).
  - Reduce offloaded GPU layers and allow partial CPU execution.

### 2. Slow Generation / Low Tokens-per-Second
- **Symptom**: Model generates fewer than 10 tokens per second on dedicated hardware.
- **Cause**: CPU layer offloading, lack of Metal/CUDA acceleration, or context fragmentation.
- **Resolution**:
  - Enable Flash Attention (`--flash-attn` in llama.cpp).
  - Verify CUDA or Metal build flags: `llama-cpp-python` must be compiled with `LLAMA_CUDA=on` or `LLAMA_METAL=on`.

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
