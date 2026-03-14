# Infrastructure

Inference engines, serving stacks, quantisation tools, vector databases, and deployment infrastructure for AI/LLM workloads.

## Contents

| Tool | What it does |
| :--- | :--- |
| [Aphrodite Engine](aphrodite-engine.md) | Inference engine forked from vLLM for local use |
| [ExLlamaV2](exllamav2.md) | Optimized GPTQ/EXL2 inference for consumer GPUs |
| [llama.cpp](llama-cpp.md) | Lightweight local inference runtime for quantized LLMs |
| [LiteLLM](../../services/litellm.md) | Unified LLM API proxy |
| [MLX](mlx.md) | Apple's array framework for ML on Apple Silicon |
| [OpenPipe](openpipe.md) | Data-driven fine-tuning platform |
| [Ollama](../../services/ollama.md) | Local LLM inference server |
| [SGLang](sglang.md) | Fast structured generation runtime from LMSYS |
| [Supabase](supabase.md) | Postgres-first backend platform for app and workflow state |
| [Text Generation Inference (TGI)](tgi.md) | Hugging Face's production inference server |
| [vLLM](vllm.md) | High-throughput LLM serving engine (PagedAttention) |
| [ZSE](zse.md) | Fast cold-start LLM inference engine |

<!-- New infrastructure pages are added here by Jules -->

## Sub-categories

- **Inference engines** — vLLM, TGI, llama.cpp, MLX, etc.
- **Vector databases** — Pinecone, Weaviate, Milvus, Qdrant, etc.
- **Serving & routing** — Load balancers, model routers, API gateways
- **Quantisation & optimisation** — GGUF, GPTQ, AWQ, etc.
