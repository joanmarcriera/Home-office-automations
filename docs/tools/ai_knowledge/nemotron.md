# NVIDIA Nemotron

## What it is
NVIDIA Nemotron is a family of open-source language models designed specifically for agentic AI, enterprise workflows, and high-precision reasoning. As of May 2026, the family includes the flagship **Nemotron 3 Super** and the newly announced **Nemotron 4** family (developed in collaboration with the Nemotron Coalition).

## What problem it solves
It addresses the "thinking tax" and "context explosion" inherent in multi-agent systems. By using a hybrid Mamba-Transformer backbone and Latent MoE (Mixture-of-Experts), it provides high-capacity reasoning and a massive 1M-token context window with 5x throughput efficiency compared to traditional dense models on NVIDIA hardware.

## Where it fits in the stack
**Model Provider / Intelligence Layer**. It serves as the "brain" for long-running autonomous agents, particularly in software development, cybersecurity triaging, and complex RAG pipelines.

## Key Technical Innovations (Nemotron 3 Super)
- **Hybrid Mamba-Transformer**: Combines Mamba-2 layers (linear-time sequence efficiency) with Transformer attention layers (precise associative recall).
- **Latent MoE**: Compresses tokens before routing to experts, allowing the model to consult 4x as many experts for the same computational cost.
- **Multi-token Prediction (MTP)**: Forecasts several future tokens simultaneously, enabling 3x wall-clock speedups via built-in speculative decoding.
- **Native NVFP4 Pretraining**: Optimized for NVIDIA Blackwell architecture, cutting memory requirements and speeding up inference by 4x compared to FP8 on older hardware.

## Typical use cases
- **Software Engineering Agents**: Handling complex codebase reasoning and multi-step merge requests (e.g., used by Cursor and Sarvam).
- **Cybersecurity Triaging**: Analyzing long logs and synthesizing multi-stage attack patterns.
- **Long-Context RAG**: Reasoning over entire repositories or large document stacks (up to 1M tokens).
- **Synthetic Data Generation**: Creating high-quality post-training data for smaller models (via Nemotron 4).

## Getting started
Nemotron models are available as open weights on Hugging Face and as optimized NIM microservices.

### Access Points
1.  **NVIDIA NIM**: Try it for free via [build.nvidia.com](https://build.nvidia.com/).
2.  **OpenRouter**: Available via API for multi-provider routing.
3.  **Hugging Face**: Download open weights (`nvidia/nemotron-3-super-120b`) for local deployment.
4.  **Cloud Providers**: Available through Baseten, Cloudflare, Mistral AI (Coalition partner), and Perplexity.

### Deployment Cookbooks
NVIDIA provides reference implementations for major inference engines:
- [vLLM Cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/vllm_cookbook.ipynb): For high-throughput continuous batching.
- [SGLang Cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/sglang_cookbook.ipynb): Optimized for multi-agent tool-calling.
- [TensorRT-LLM Cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/trtllm_cookbook.ipynb): Low-latency production deployment.

### 2026 Model Roadmap: Nemotron 4
Announced in March 2026 at GTC, the **Nemotron Coalition** (including Mistral AI, LangChain, Perplexity, and Cursor) is developing the Nemotron 4 family. The first model, co-developed with Mistral AI, serves as a base frontier model designed for industry-specific specialization and agentic planning.

## Training and Evaluation Stack
NVIDIA provides a complete toolset for adapting and evaluating Nemotron models:

| Component | Role |
| :--- | :--- |
| [NeMo Gym](https://docs.nvidia.com/nemo/gym/latest/) | Reinforcement-learning environment for agentic task rollouts. |
| [NeMo Data Designer](https://nvidia-nemo.github.io/NeMo-Data-Designer/) | Synthetic-data and data-design tooling. |
| [NeMo Evaluator](https://docs.nvidia.com/nemo/evaluator/latest/) | Evaluation harness for rerunning and inspecting model benchmarks. |
| [Unsloth](https://unsloth.ai/) | Preferred fine-tuning route for rapid customization on consumer/prosumer hardware. |

## Running Pattern
For agentic deployments, use the **Cascade Pattern**:
1.  Route targeted, low-complexity steps to **Nemotron 3 Nano**.
2.  Escalate complex planning, long-context reasoning, and multi-step investigation to **Nemotron 3 Super**.
3.  Use **vLLM** or **SGLang** for serving to leverage continuous batching and speculative decoding.

## Strengths
- **Agentic Performance**: Scores top-tier marks on PinchBench (agent brain evaluation).
- **Hardware Affinity**: Extreme efficiency gains on NVIDIA Ampere, Hopper, and Blackwell architectures.
- **Openness**: Commercial-friendly NVIDIA Open Model License permits free download and specialization.

## Limitations
- **VRAM Requirements**: The 120B model requires significant VRAM even with its MoE efficiency (typically 2-4x A100/H100 GPUs).
- **Reasoning vs. Frontier Models**: While excellent for agents, it may still lag behind closed frontier models like OpenAI o3-Pro in pure general reasoning.

## When to use it
- **Enterprise Multi-Agent Systems**: When building complex, long-running agents that require high reasoning capacity.
- **Modern NVIDIA Hardware**: If you have access to H100 or B200 infrastructure to leverage FP4/FP8 optimizations.
- **Long-Context Analysis**: When you need to process and reason over huge document stacks or entire codebases (up to 1M tokens).

## When not to use it
- **Consumer Hardware**: It is generally too large for standard consumer GPUs without significant quantization or offloading.
- **Simple Chat Tasks**: For basic Q&A or short-context summaries, smaller models (e.g., Llama 3 8B or Nemotron Nano) are more efficient.
- **Non-NVIDIA Stacks**: While it runs on other hardware, many of its core innovations (Latent MoE, NVFP4) are optimized for NVIDIA architectures.

## Related tools / concepts
- [NVIDIA](../providers/nvidia.md)
- [NVIDIA PersonaPlex](personaplex.md)
- [NVIDIA NeMo Retriever](../agents/nemo-retriever.md)
- [vLLM](../infrastructure/vllm.md)
- [SGLang](../infrastructure/sglang.md)

## Sources / References
- [NVIDIA Launches Nemotron Coalition (NVIDIA Newsroom, March 2026)](https://nvidianews.nvidia.com/news/nvidia-launches-nemotron-coalition-of-leading-global-ai-labs-to-advance-open-frontier-models)
- [NVIDIA AI Models 2026 Guide (BuildFast with AI)](https://www.buildfastwithai.com/blogs/nvidia-ai-models-2026-guide)
- [Introducing Nemotron 3 Super (NVIDIA Blog)](https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high
