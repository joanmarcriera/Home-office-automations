# NVIDIA Nemotron

## What it is
NVIDIA Nemotron is a family of open-source language models designed specifically for agentic AI, enterprise workflows, and high-precision reasoning. As of July 2026, the family includes the flagship **Nemotron 4** family, which optimizes for multi-agent coordination and high-throughput Blackwell inference, often benchmarked alongside [Gemma 3](local_llms.md).

## What problem it solves
It addresses the "thinking tax" and "context explosion" inherent in multi-agent systems. By using a hybrid Mamba-Transformer backbone and Latent MoE (Mixture-of-Experts), it provides high-capacity reasoning and a massive 1M-token context window with significantly higher throughput efficiency compared to traditional dense models on NVIDIA hardware.

## Where it fits in the stack
**Model Provider / Intelligence Layer**. It serves as the "brain" for long-running autonomous agents, particularly in software development, cybersecurity triaging, and complex RAG pipelines using the [MCP 3.0](../automation_orchestration/mcp.md) Task Protocol.

## Typical use cases
- **Software Engineering Agents**: Handling complex codebase reasoning and multi-step merge requests (e.g., used by Cursor and Sarvam).
- **Cybersecurity Triaging**: Analyzing long logs and synthesizing multi-stage attack patterns using the 1M token context.
- **Long-Context RAG**: Reasoning over entire repositories or large document stacks without the need for aggressive chunking.
- **Synthetic Data Generation**: Creating high-quality post-training data for smaller models (via Nemotron 4-Synthetic).

## Strengths
- **Agentic Performance**: Scores top-tier marks on benchmarks evaluating agentic planning and tool-use precision.
- **Hardware Affinity**: Extreme efficiency gains on NVIDIA Hopper and Blackwell architectures via native FP4/FP8 support.
- **Open Weights**: Commercial-friendly NVIDIA Open Model License permits free download, specialization, and private deployment.
- **Hybrid Architecture**: Combines Mamba-2 for efficiency with Transformers for precise recall.

## Limitations
- **VRAM Requirements**: The high-parameter models (e.g., 120B+) require multi-GPU setups (A100/H100/B200) for inference.
- **Specialization Needed**: While excellent for agents, it often requires domain-specific fine-tuning to outperform closed frontier models in niche tasks.
- **Ecosystem Lock-in**: Many performance optimizations are specific to NVIDIA TensorRT-LLM and NIM microservices.

## When to use it
- When building **complex, long-running agents** that require high reasoning capacity and stable tool-calling.
- If you have access to **modern NVIDIA GPU infrastructure** to leverage its native architectural optimizations.
- For **privacy-critical enterprise tasks** where open-weights models are required for on-premises deployment.

## When not to use it
- On **consumer hardware** with low VRAM (unless using heavily quantized versions or smaller Nano variants).
- For **simple, short-context chat** tasks where lighter models like [Gemma 3](local_llms.md) 8B are faster and more cost-effective.
- When working on **non-NVIDIA hardware** (e.g., AMD, Apple Silicon), as many core optimizations will not be available.

## Getting started
Nemotron models are available as open weights on Hugging Face and as optimized NIM microservices.

### Access Points
1.  **NVIDIA NIM**: Try it for free via [build.nvidia.com](https://build.nvidia.com/).
2.  **OpenRouter**: Available via API for multi-provider routing and comparison.
3.  **Hugging Face**: Download open weights (`nvidia/nemotron-4-340b-instruct`) for local deployment.

### Quick Deployment (Docker)
Run a Nemotron NIM container locally (requires NVIDIA Container Toolkit and compatible GPU):

```bash
docker run --gpus all \
  -e NGC_API_KEY=$NGC_API_KEY \
  -v $LOCAL_CACHE:/opt/nim/.cache \
  -p 8000:8000 \
  nvcr.io/nim/nvidia/nemotron-4-340b-instruct:1.0.0
```

## CLI examples
You can interact with a running Nemotron NIM or local instance using standard OpenAI-compatible CLI tools or `curl`.

```bash
# Query the local NIM instance
curl -X POST "http://localhost:8000/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "nemotron-4-340b-instruct",
       "messages": [{"role": "user", "content": "Analyze this code for race conditions..."}]
     }'
```

## API examples
NVIDIA Nemotron is natively supported by major agent frameworks and inference libraries.

### Python (vLLM)
High-throughput serving for local deployment.
```python
from vllm import LLM, SamplingParams

prompts = ["Plan a multi-step migration from Postgres to MinIO."]
sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=1024)

llm = LLM(model="nvidia/nemotron-4-340b-instruct", tensor_parallel_size=4)
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Generated text: {output.outputs[0].text}")
```

## Related tools / concepts
- [NVIDIA](../providers/nvidia.md) — The parent company and provider of the hardware/software stack.
- [NVIDIA NeMo Retriever](../agents/nemo-retriever.md) — Agentic RAG framework optimized for Nemotron.
- [vLLM](../infrastructure/vllm.md) — Recommended inference engine for high-throughput serving.
- [SGLang](../infrastructure/sglang.md) — High-performance runtime for agentic tool-calling.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — For connecting Nemotron agents to local tools.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The primary architectural pattern for Nemotron.
- [Claude Code Agent](../development_ops/claude-code.md) — A comparable developer-focused agentic model.
- [OpenCode](../development_ops/opencode.md) — Open-source alternative for agentic coding tasks.
- [Llama 4 Maverick](../ai_knowledge/llama.md) — Competitive open-weights frontier model.

## Sources / references
- [NVIDIA Launches Nemotron Coalition (March 2026)](https://nvidianews.nvidia.com/news/nvidia-launches-nemotron-coalition-of-leading-global-ai-labs-to-advance-open-frontier-models)
- [NVIDIA Nemotron-4 340B Technical Report](https://arxiv.org/abs/2406.11704)
- [Optimizing Nemotron for Blackwell Architecture (NVIDIA Developer Blog)](https://developer.nvidia.com/blog/optimizing-nemotron-for-blackwell/)

## Contribution Metadata
- Last reviewed: 2026-07-11
- Confidence: high
