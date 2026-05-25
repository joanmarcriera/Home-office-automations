# Ollama

## What it is
Ollama allows you to get up and running with large language models locally. It provides a simple CLI and API for running models like Llama 3, Mistral, and others on your own hardware.

## What problem it solves
It simplifies the complex setup usually required for running LLMs, handling model weights, configurations, and hardware acceleration (GPU) automatically. It enables private, offline AI interactions without relying on cloud providers.

## Where it fits in the stack
**Local Inference Engine**. It acts as the execution layer for models on your own hardware, serving as a backend for various WebUIs and agents.

## Typical use cases
- **Private Chat**: Interacting with LLMs without data leaving your local network.
- **Development & Testing**: Locally testing AI-integrated applications before deploying to cloud providers.
- **Autonomous Agents**: Serving as the local backend for agents like Aider or OpenHands.
- **Enterprise Prototyping**: Rapidly deploying specialized models for internal document analysis or coding assistance.

## Strengths
- **Ease of Use**: One-line installation and simple model pulling (e.g., `ollama run llama3`).
- **Hardware Acceleration**: Automatic detection and utilization of NVIDIA, AMD, and Apple Silicon GPUs.
- **Large Model Library**: Easy access to Llama 3, Mistral, Phi-3, and many more.
- **Zero Cost**: No per-token pricing; limited only by your hardware.

## Limitations
- **Hardware Dependent**: Performance is strictly tied to local CPU/GPU/RAM.
- **Memory Requirements**: Larger models require significant VRAM.

## When to use it
- For maximum privacy and data sovereignty.
- To eliminate per-token costs during development.
- When working in offline or low-connectivity environments.

## When not to use it
- If you lack dedicated GPU hardware and require low-latency responses.
- For massive models (e.g., 70B+) that exceed consumer hardware capacity.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation (Docker)
```yaml
services:
  ollama:
    volumes:
      - ./ollama:/root/.ollama
    container_name: ollama
    pull_policy: always
    tty: true
    restart: unless-stopped
    image: ollama/ollama:latest
```

### API Usage Example
You can interact with the Ollama API using `curl`:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

## TrueNAS SCALE & GPU Setup
Running Ollama on [TrueNAS SCALE](../architecture/infrastructure.md) requires configuring GPU passthrough for optimal performance.

### GPU Passthrough (NVIDIA)
1. **Host Configuration**: Ensure the NVIDIA driver is active in TrueNAS SCALE (**System Settings > Advanced > Isolated GPU Device**).
2. **Docker/App Configuration**: In the application settings, allocate `1` (or more) GPU under the "Resource Reservation" section.
3. **Environment**: Ensure `NVIDIA_VISIBLE_DEVICES=all` and `NVIDIA_DRIVER_CAPABILITIES=compute,utility` are set in the container environment.

### Performance Benchmarking
Tokens per second (t/s) vary by model size and hardware. Use `ollama run <model>` and then `/set verbose` to see generation statistics.

| Hardware | Model | VRAM Used | Eval Rate (t/s) |
| :--- | :--- | :--- | :--- |
| **Intel i7 (12th Gen)** | Llama 3.1 8B | 0GB (CPU) | ~3-5 t/s |
| **NVIDIA RTX 3060 (12GB)** | Llama 3.1 8B | ~5.5GB | ~45-55 t/s |
| **NVIDIA RTX 4090 (24GB)** | Llama 3.1 8B | ~5.5GB | ~130+ t/s |
| **NVIDIA RTX 4090 (24GB)** | Llama 3.1 70B | ~42GB (Quant) | ~15-20 t/s |

## Related tools / concepts
- [Open WebUI](open-webui.md) — The recommended web frontend for Ollama.
- [LiteLLM](litellm.md) — For load balancing multiple Ollama instances.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of the local model ecosystem.
- [LM Studio](https://lmstudio.ai/) — A desktop-first alternative for model experimentation.

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Sources / References
- [Official Website](https://ollama.com/)
- [GitHub Repository](https://github.com/ollama/ollama)
- [TrueNAS SCALE GPU Guide](https://www.truenas.com/docs/scale/24.10/applications/gpu/)
- [Ollama GPU Documentation](https://github.com/ollama/ollama/blob/main/docs/gpu.md)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
