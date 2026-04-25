# NVIDIA Nemotron-3 Super

## What it is
NVIDIA Nemotron-3 Super is a 120B total / 12B active-parameter hybrid Mamba-Transformer Mixture-of-Experts (MoE) model specifically engineered for agentic reasoning and long-context tasks. It represents a significant architectural shift by combining the sequence efficiency of State Space Models (SSMs) with the precision of Transformer attention.

## What problem it solves
It addresses the "thinking tax" and "context explosion" inherent in multi-agent systems. Standard models often become prohibitively expensive or lose objective alignment as context grows. Nemotron-3 Super provides a practical 1M-token context window and high throughput, enabling agents to reason over entire codebases or long document stacks without the performance degradation typical of pure-Transformer or pure-SSM architectures.

## Where it fits in the stack
**Category**: AI Assistant / Model

## Key Architectural Innovations
- **Hybrid Mamba-Transformer Backbone**: Interleaves Mamba-2 layers (for linear-time sequence processing) with Transformer attention layers (for high-fidelity associative recall).
- **Latent MoE**: Compresses token embeddings before they reach the experts, allowing the model to consult 4x as many experts (specialized in different domains like Python vs. SQL) for the same computational cost.
- **Multi-token Prediction (MTP)**: Predicts multiple future tokens simultaneously, enabling built-in speculative decoding for 2x-3x speedups in structured generation tasks (code/JSON).
- **Native NVFP4 Pretraining**: Trained natively in 4-bit floating-point precision optimized for NVIDIA Blackwell, ensuring mathematical stability and accuracy on a reduced memory footprint.

## Typical use cases
- **Agentic Coding**: Powering autonomous developers like OpenCode, Aider, or OpenHands to navigate and refactor large repositories.
- **Cybersecurity Triaging**: Analyzing long logs and multi-step attack vectors over massive context windows.
- **Complex Multi-hop RAG**: Synthesizing answers from thousands of retrieved documents with precise citation.

## Deployment & Running Techniques
The model is supported by major inference engines. **Free tier** access for testing and evaluation is currently available through [NVIDIA Build](https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b).

### Supported Engines
- **vLLM**: For high-throughput continuous batching.
- **SGLang**: Optimized for multi-agent tool-calling workloads.
- **TensorRT-LLM**: Production-grade, low-latency deployment with optimized latent MoE kernels.

## When to use it
- Use when building long-running autonomous agents that need to maintain alignment over 100k+ tokens of context.
- Use as a high-performance open-weights alternative to proprietary frontier models for technical tasks.

## When not to use it
- Not for simple, single-turn chat interactions where smaller models (like Nemotron-3 Nano) are more cost-effective.
- Not for deployment on highly resource-constrained consumer hardware without significant quantization.

## Sources / references
- [Introducing Nemotron-3 Super (NVIDIA Blog)](https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/)
- [Nemotron-3 Super Technical Report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)
- [NVIDIA Build (Try the Model)](https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b)

## Contribution Metadata
- Last reviewed: 2026-04-25
- Confidence: high
