# Task Decomposition: Batch 71 (Infrastructure Maintenance)

This report implements **Action C** for the technical deepening of 5 infrastructure and development tools identified as needing maintenance (originally reviewed March 2026).

## Batch 71 Overview
- **Objective**: Maintain "High Confidence" standards by adding modern technical examples and architectural details to key inference and routing tools.
- **Priority**: Inference infrastructure and agentic routing.

## Target Files & Technical Deepening Goals

### 1. `docs/tools/infrastructure/tgi.md`
- **Technical Examples**:
  - Multi-LoRA serving configuration.
  - Advanced quantization (AWQ, GPTQ) integration via bitsandbytes.
  - Streaming performance metrics via Prometheus.
- **Cross-Links**: `vllm.md`, `sglang.md`, `bitsandbytes.md`, `prometheus.md`, `docker.md`.

### 2. `docs/tools/infrastructure/sglang.md`
- **Technical Examples**:
  - RadixAttention mechanism details for prefix caching.
  - Chunked prefill configuration for multi-turn responsiveness.
  - Python SDK example for complex JSON constrained generation.
- **Cross-Links**: `vllm.md`, `tgi.md`, `radix-attention.md`, `python-sdk.md`, `json-schema.md`.

### 3. `docs/tools/infrastructure/aphrodite-engine.md`
- **Technical Examples**:
  - Modern samplers (DRY, XTC) configuration.
  - EXL2 backend support and GGUF integration.
  - Benchmarking against vLLM for consumer hardware.
- **Cross-Links**: `vllm.md`, `exllamav2.md`, `gguf.md`, `dry-sampler.md`, `xtc-sampler.md`.

### 4. `docs/tools/infrastructure/exllamav2.md`
- **Technical Examples**:
  - Granular quantization (bpw) examples for specific VRAM targets.
  - NVIDIA kernel optimization flags.
  - Memory management for long-context (128k+) inference.
- **Cross-Links**: `aphrodite-engine.md`, `vllm.md`, `nvidia-cuda.md`, `quantization.md`, `long-context.md`.

### 5. `docs/tools/development_ops/claude-code-router.md`
- **Technical Examples**:
  - MCP-based tool routing patterns.
  - Agent-native LLM routing rules using YAML.
  - Fallback and retry strategies for frontier model outages.
- **Cross-Links**: `mcp-registry.md`, `claude-code-setup.md`, `openrouter.md`, `fallback-patterns.md`, `agent-protocols.md`.

---
- Confidence: high
- Date: 2026-05-17
- Created by: Jules
