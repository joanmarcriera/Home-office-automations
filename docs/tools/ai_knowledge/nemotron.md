# NVIDIA Nemotron-3 Super

## What it is
NVIDIA Nemotron-3 Super is an open, high-efficiency large language model designed specifically for complex multi-agent applications and agentic reasoning. It is a 120B total parameter model with a 12B active-parameter Mixture-of-Experts (MoE) architecture.

## What problem it solves
It addresses the "thinking tax" and "context explosion" inherent in multi-agent systems. By using a hybrid Mamba-Transformer backbone and Latent MoE, it provides high-capacity reasoning and a massive 1M-token context window without the extreme compute costs of traditional dense models.

## Where it fits in the stack
**Model Provider / Intelligence Layer**. It serves as the "brain" for long-running autonomous agents, particularly in software development and cybersecurity triaging.

## Key Technical Innovations
- **Hybrid Mamba-Transformer**: Combines Mamba-2 layers (for linear-time sequence efficiency) with Transformer attention layers (for precise associative recall).
- **Latent MoE**: Compresses tokens before routing to experts, allowing the model to consult 4x as many experts for the same computational cost.
- **Multi-token Prediction (MTP)**: Forecasts several future tokens simultaneously, improving reasoning during training and enabling 3x wall-clock speedups via built-in speculative decoding.
- **Native NVFP4 Pretraining**: Optimized for NVIDIA Blackwell architecture, cutting memory requirements and speeding up inference by 4x compared to FP8 on older hardware.

## Typical use cases
- **Software Engineering Agents**: Handling complex codebase reasoning and multi-step merge requests.
- **Cybersecurity Triaging**: Analyzing long logs and synthesizing multi-stage attack patterns.
- **Long-Context RAG**: Reasoning over entire repositories or large document stacks (up to 1M tokens).

## Getting started
Nemotron-3 Super is available across multiple platforms and as open weights.

### Access Points
1.  **NVIDIA build**: Try it for free via [build.nvidia.com](https://build.nvidia.com/).
2.  **OpenRouter**: Available via API (includes a free tier for trial).
3.  **Hugging Face**: Download open weights for local deployment.
4.  **Perplexity**: Available for Pro subscribers and via API.
5.  **Cloud Providers**: Available through Baseten, Cloudflare, Coreweave, DeepInfra, Fireworks AI, FriendliAI, Google Cloud, Inference.net, Lightning AI, Modal, Nebius, and Together AI.

### Deployment Cookbooks
NVIDIA provides reference implementations for major inference engines:
- [vLLM Cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/vllm_cookbook.ipynb): For high-throughput continuous batching.
- [SGLang Cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/sglang_cookbook.ipynb): Optimized for multi-agent tool-calling.
- [TensorRT-LLM Cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/trtllm_cookbook.ipynb): Low-latency production deployment on NVIDIA hardware.
- [LoRA Fine-tuning](https://github.com/NVIDIA-NeMo/Nemotron/tree/main/usage-cookbook/Nemotron-3-Super/lora-text2sql): Domain-specific optimization recipes.

## Strengths
- **Efficiency**: 5x throughput improvement over previous generations.
- **Agentic Performance**: Scores 85.6% on PinchBench (benchmark for agent brains).
- **Openness**: Fully open weights, datasets, and recipes under the NVIDIA Nemotron Open Model License.

## Limitations
- **Hardware Affinity**: Best performance and efficiency gains require NVIDIA Blackwell (B200) GPUs.
- **Model Size**: At 120B total parameters, it requires significant VRAM even with its 12B active parameter efficiency.

## Related tools / concepts
- [NVIDIA](../providers/nvidia.md)
- [NVIDIA NeMo Retriever](../agents/nemo-retriever.md)
- [OpenCode](../development_ops/opencode.md)
- [Mamba Architecture](../../knowledge_base/model_classes.md)

## Sources / References
- [Introducing Nemotron 3 Super (NVIDIA Blog)](https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/)
- [Nemotron-3 Super Technical Report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
