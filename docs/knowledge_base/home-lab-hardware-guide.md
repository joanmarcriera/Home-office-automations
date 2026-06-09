# Home Lab Hardware Reference

## What it is
A hardware-scoped reference for a two-machine home lab stack, detailing the specific compute profiles, VRAM limits, and workload routing for persistent services and development inference.

## What problem it solves
Managing a hybrid home lab (e.g., TrueNAS + MacBook) requires clear guidance on where to run specific AI workloads based on VRAM constraints and architecture (unified memory vs. dedicated GPU). This guide prevents resource contention and optimizes model placement.

## Where it fits in the stack
This is a **Knowledge Base** document sitting at the **Infrastructure** layer. it informs the deployment strategy for all tools in the `docs/tools/` and `docs/services/` categories.

## Typical use cases
- **Model Routing**: Deciding whether to run a 30B model on an M5 or a 7B model on an RTX 4060.
- **Capacity Planning**: Estimating how many parallel video transcodes or LLM streams the lab can handle.
- **Hardware Upgrades**: Benchmarking current performance against desired agentic workflows.

## Strengths
- **Role-Specific**: Clearly defines the "Persistent Service" (TrueNAS) vs. "Development" (M5) roles.
- **Practical Limits**: Provides realistic "Fits?" and "⚠️ Tight" assessments based on real-world testing.
- **Unified Endpoints**: Recommends LiteLLM for creating a seamless multi-machine API.

## Limitations
- **Hardware Specific**: Primarily focused on a specific RTX 4060 + M5 configuration.
- **Static**: Requires manual updates as model architectures (like MoE) change their memory footprints.

## When to use it
- When adding a new LLM-powered service to the lab.
- When configuring Ollama or vLLM backends.
- When troubleshooting performance issues or out-of-memory errors.

## When not to use it
- For generic server hardware advice (e.g., non-AI homelab setups).
- For enterprise-grade multi-GPU cluster configurations.

## Hardware inventory

| | TrueNAS Server | MacBook Pro M5 |
|---|---|---|
| **CPU** | 12 cores | Apple M5 |
| **RAM** | 96 GB DDR4 | 48 GB unified |
| **GPU** | RTX 4060 8 GB VRAM | Metal (unified) |
| **Storage** | 80 TB ZFS | SSD |
| **Ollama endpoint** | `192.168.0.5:30068` | `localhost:11434` |
| **Primary role** | Persistent services, NVENC, 3-8B LLMs, image gen | Large-model inference, development |

## RTX 4060 8 GB — practical limits

The RTX 4060 has 8 GB VRAM. This is enough for many useful GPU workloads but rules out running large LLMs in fp16.

| Workload | Recommended tool | Config / model | Fits? |
|---|---|---|---|
| LLM inference | Ollama / llama.cpp | 3-8B models, Q4_K_M or Q5_K_S GGUF | ✅ Comfortable |
| LLM inference | Ollama | 7-8B Q4_K_M (e.g. Llama 3.2 8B, Qwen2.5 7B) | ✅ ~4-5 GB |
| LLM inference | Ollama / vLLM (AWQ) | 13-14B AWQ 4-bit | ⚠️ Tight (~7-8 GB) |
| LLM inference | Any | 13B+ fp16 / 30B+ any | ❌ Exceeds VRAM |
| Video transcoding | Jellyfin NVENC | Any resolution, H.264/H.265/AV1 | ✅ Dedicated encoder |
| Audio transcription | Whisper large-v3 | Faster-Whisper batched, FP16 | ✅ ~4-5 GB |
| Image generation | ComfyUI | SD 1.5, SDXL (fp16) | ✅ 4-8 GB |
| Image generation | ComfyUI | Flux-schnell (fp8/nf4) | ⚠️ Tight, use `--lowvram` |
| Image generation | ComfyUI | Flux-dev (fp16) | ❌ Needs 16-24 GB |
| Embeddings | Ollama / LocalAI | nomic-embed-text, mxbai-embed | ✅ <1 GB |

**Key rule for LLMs on the RTX 4060**: Use Q4_K_M or Q5_K_S GGUF quantization. The model weight footprint at Q4_K_M is approximately `(parameters × 0.5 GB)` — so a 7B model needs ~3.5-4 GB, leaving headroom for KV cache.

## M5 48 GB — practical limits

Apple Silicon's unified memory architecture means all 48 GB is addressable by the Metal GPU backend. There is no separate VRAM pool. This makes the M5 a better local LLM host than any single consumer NVIDIA GPU for models in the 30-40B range.

| Workload | Recommended tool | Config / model | Fits? |
|---|---|---|---|
| LLM inference | Ollama (Metal) | Up to ~40B Q4_K_M | ✅ Comfortable |
| LLM inference | MLX | Qwen3.5 32B, Llama 3.3 70B Q4 | ✅ 22-40 GB |
| LLM inference | LM Studio | Any GGUF ≤ 40B | ✅ GUI with Metal |
| Fine-tuning (LoRA) | MLX / Unsloth | 7-13B models | ✅ Sufficient RAM |
| Image generation | ComfyUI (`--use-pytorch-mps`) | SDXL, Flux-dev | ✅ All 48 GB available |
| Audio transcription | mlx-whisper | large-v3 via CoreML | ✅ Fast |
| Agentic development | Ollama + LM Studio | Any model ≤ 40B | ✅ Ideal dev machine |
| 70B models | Ollama (Metal) | Q4_K_M (~40 GB) | ⚠️ Tight, leaves ~8 GB |
| 70B fp16 | Any | 140 GB needed | ❌ Not viable |

## Model size quick reference

| Model size | RTX 4060 8 GB | M5 48 GB | Recommended format |
|---|---|---|---|
| 1-3B | ✅ Comfortable | ✅ Comfortable | GGUF Q8 or MLX |
| 7-8B | ✅ Q4/Q5 only | ✅ Comfortable | GGUF Q4_K_M or MLX 4-bit |
| 13-14B | ⚠️ Q4 tight | ✅ Comfortable | GGUF Q4_K_M or MLX 4-bit |
| 30-34B | ❌ Not viable | ✅ Comfortable | MLX 4-bit or GGUF Q4 |
| 70B | ❌ Not viable | ⚠️ Q4 tight (~40 GB) | MLX 4-bit |
| 70B+ | ❌ Not viable | ❌ Not viable | Multi-GPU / cloud |

## Workload routing guide

**Run on TrueNAS (RTX 4060):**
- Persistent services (Jellyfin, Whisper, Immich, n8n, Paperless-ngx)
- Small/medium LLM inference (up to 8B) available 24/7 via Ollama
- NVENC video transcoding — does not consume VRAM, runs in parallel with LLMs
- Local image generation (ComfyUI with SDXL/Flux-schnell)
- All background automation and document processing

**Run on MacBook M5:**
- Large-model development sessions (30-40B models)
- Interactive agent development with LM Studio or Ollama
- MLX fine-tuning experiments
- Any task requiring a model too large for the RTX 4060

**Unify both endpoints with [LiteLLM](../services/litellm.md):**
```yaml
model_list:
  - model_name: "fast"
    litellm_params:
      model: "ollama/qwen2.5:7b"
      api_base: "http://192.168.0.5:30068"
  - model_name: "large"
    litellm_params:
      model: "ollama/qwen3.5:32b"
      api_base: "http://localhost:11434"
```
Point all agents at the LiteLLM proxy and route by model alias.

## Related tools / concepts

- [Ollama](../services/ollama.md) — LLM serving on both machines; TrueNAS GPU passthrough documented there
- [Jellyfin](../services/jellyfin.md) — NVENC hardware transcoding configuration
- [Whisper](../services/whisper.md) — GPU benchmark table (RTX 3060 → RTX 4090 reference points)
- [ComfyUI](../tools/ai_knowledge/comfyui.md) — Local image generation; hardware requirements table
- [MLX](../tools/infrastructure/mlx.md) — Apple Silicon inference framework for M5
- [LM Studio](../tools/infrastructure/lm-studio.md) — GUI LLM client with Metal backend for M5
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Model hardware requirements and backend comparison
- [LiteLLM](../services/litellm.md) — Proxy to unify TrueNAS + MacBook endpoints
- [Immich](../services/immich.md) — Photo management with ML features on TrueNAS

## Sources / references

- [NVIDIA RTX 4060 Specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4060/)
- [Apple Silicon unified memory performance](https://developer.apple.com/metal/pytorch/)
- [Ollama Hardware Requirements](https://github.com/ollama/ollama/blob/main/docs/gpu.md)
- [llama.cpp VRAM estimation](https://github.com/ggerganov/llama.cpp#memory-requirements)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
