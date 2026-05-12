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

### Training and evaluation stack
The NVIDIA announcement also names the tooling and techniques used to train, adapt, and rerun evaluations for Nemotron-3 Super:

| Component | Role | Free/open status |
| :--- | :--- | :--- |
| [NeMo Gym](https://docs.nvidia.com/nemo/gym/latest/) | Scalable reinforcement-learning environment harness for agentic task rollouts. | Open-source NVIDIA library; compute costs depend on where it runs. |
| [NeMo RL](https://docs.nvidia.com/nemo/rl/latest/) | Reinforcement-learning library used for multi-environment post-training. | Open-source NVIDIA library; practical use requires GPU capacity. |
| [NeMo Megatron-Bridge](https://github.com/NVIDIA-NeMo/Megatron-Bridge) | Bridge for large-model SFT/LoRA workflows on NVIDIA infrastructure. | Open-source repository. |
| [NeMo Automodel](https://github.com/NVIDIA-NeMo/Automodel) | Higher-level model customization path for SFT/LoRA recipes. | Open-source repository. |
| [NeMo Data Designer](https://nvidia-nemo.github.io/NeMo-Data-Designer/) | Synthetic-data and data-design tooling for training data preparation. | Public docs and tooling; runtime cost depends on model/provider. |
| [NeMo Curator](https://docs.nvidia.com/nemo/curator/latest/) | Data curation and filtering pipeline for pretraining/post-training corpora. | Public NVIDIA tooling; compute/storage costs apply. |
| [NeMo Evaluator](https://docs.nvidia.com/nemo/evaluator/latest/) | Evaluation harness for rerunning and inspecting model benchmarks. | Public NVIDIA tooling; benchmark execution costs apply. |
| [Unsloth](https://unsloth.ai/) | Fine-tuning route highlighted by NVIDIA for practical customization. | Free/open tooling options exist; hosted/commercial options may vary. |

### Running pattern
For agentic deployments, treat Nemotron-3 Super as the planning/escalation model rather than the only model in the system. NVIDIA's suggested pattern is to route targeted, lower-complexity steps to Nemotron 3 Nano, then escalate complex planning, long-context codebase reasoning, and cybersecurity triage to Nemotron-3 Super. Use vLLM or SGLang for open GPU serving, TensorRT-LLM for NVIDIA-optimized production latency, and NVIDIA NIM or hosted providers when you want managed endpoints.

## Strengths
- **Efficiency**: 5x throughput improvement over previous generations.
- **Agentic Performance**: Scores 85.6% on PinchBench (benchmark for agent brains).
- **Openness**: Fully open weights, datasets, and recipes under the NVIDIA Nemotron Open Model License.

## Limitations
- **Hardware Affinity**: Best performance and efficiency gains require NVIDIA Blackwell (B200) GPUs.
- **Model Size**: At 120B total parameters, it requires significant VRAM even with its 12B active parameter efficiency.

## When to use it
- Use when building autonomous multi-agent systems that require long-context reasoning across massive document sets.
- Use if you have access to NVIDIA hardware (especially Blackwell) and need to minimize inference latency for large models.
- Use for cybersecurity or software engineering tasks where "associative recall" and multi-step planning are critical.

## When not to use it
- Do not use for simple, single-turn chat interactions where smaller, faster models (like Nemotron-3 Nano) are sufficient.
- Avoid using on non-NVIDIA hardware if you require the 4x efficiency gains promised by NVFP4 optimization.
- Do not use if you are strictly limited by VRAM and cannot support a 120B parameter model footprint.

## Related tools / concepts
- [NVIDIA](../providers/nvidia.md)
- [NVIDIA NeMo Retriever](../agents/nemo-retriever.md)
- [OpenCode](../development_ops/opencode.md)
- [Mamba Architecture](../../knowledge_base/model_classes.md)
- [DeepSeek R1](deepseek-r1.md)
- [Qwen](qwen.md)
- [OpenRouter](openrouter.md)
- [Llama.cpp](../infrastructure/llama-cpp.md)

## Sources / References
- [Introducing Nemotron 3 Super (NVIDIA Blog)](https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/)
- [Nemotron-3 Super Technical Report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)
- [NVIDIA-NeMo / Nemotron GitHub repository](https://github.com/NVIDIA-NeMo/Nemotron)
- [NVIDIA NeMo Gym documentation](https://docs.nvidia.com/nemo/gym/latest/)
- [NVIDIA NeMo RL documentation](https://docs.nvidia.com/nemo/rl/latest/)
- [NVIDIA NeMo Curator documentation](https://docs.nvidia.com/nemo/curator/latest/)
- [NVIDIA NeMo Evaluator documentation](https://docs.nvidia.com/nemo/evaluator/latest/)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
