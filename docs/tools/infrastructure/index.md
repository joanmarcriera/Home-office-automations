# Infrastructure

Inference engines, serving stacks, quantisation tools, vector databases, and deployment infrastructure for AI/LLM workloads.

## Contents

| Tool | What it does |
| :--- | :--- |
| [Aphrodite Engine](aphrodite-engine.md) | Inference engine forked from vLLM for local use |
| [ClawRouter](clawrouter.md) | Agent-native routing layer for OpenClaw model selection |
| [DuckDB](duckdb.md) | In-process analytical SQL database for agentic data exploration |
| [ExLlamaV2](exllamav2.md) | Optimized GPTQ/EXL2 inference for consumer GPUs |
| [Jan.ai](jan-ai.md) | Local, open-source AI desktop client |
| [llama.cpp](llama-cpp.md) | Lightweight local inference runtime for quantized LLMs |
| [LiteLLM](../../services/litellm.md) | Unified LLM API proxy |
| [LocalAI](localai.md) | Self-hosted OpenAI-compatible local inference platform |
| [MLX](mlx.md) | Apple's array framework for ML on Apple Silicon |
| [Msty](msty.md) | Local-first AI desktop app with model hub |
| [OpenPipe](openpipe.md) | Data-driven fine-tuning platform |
| [Ollama](../../services/ollama.md) | Local LLM inference server |
| [SGLang](sglang.md) | Fast structured generation runtime from LMSYS |
| [Supabase](supabase.md) | Postgres-first backend platform for app and workflow state |
| [Text Generation Inference (TGI)](tgi.md) | Hugging Face's production inference server |
| [vLLM](vllm.md) | High-throughput LLM serving engine (PagedAttention) |
| [ZSE](zse.md) | Fast cold-start LLM inference engine |

<!-- New infrastructure pages are added here by Jules -->

## Hardware Highlights

As of early 2026, Apple Silicon continues to be the dominant platform for high-performance local AI inference in the homelab:

- **Apple M5 Pro / M5 Max**: Unveiled March 2026, offering up to **4× faster LLM prompt processing** compared to previous generations, significantly reducing agentic loop latency.
- **Apple M3 Ultra**: Benchmark results for 11 MLX models (March 2026) confirm it as a premier choice for running large-scale local models with unified memory.

## Sub-categories

- **Inference engines** — vLLM, TGI, llama.cpp, MLX, etc.
- **Vector databases** — Pinecone, Weaviate, Milvus, Qdrant, etc.
- **Serving & routing** — Load balancers, model routers, API gateways
- **Quantisation & optimisation** — GGUF, GPTQ, AWQ, etc.

## Related tools / concepts

- [Local LLMs](../ai_knowledge/local_llms.md)
- [Model Comparison & Evaluation](../../knowledge_base/model_comparison_and_evaluation.md)
- [Vector DB Comparison](../../knowledge_base/vector-db-comparison.md)
- [Infrastructure Detail](../../architecture/infrastructure.md)
- [Providers](../providers/index.md)
