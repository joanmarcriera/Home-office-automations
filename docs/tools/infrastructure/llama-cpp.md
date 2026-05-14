# llama.cpp

## What it is
`llama.cpp` is a lightweight C/C++ inference runtime for running GGUF/quantized LLMs locally on commodity hardware.

## What problem it solves
It makes local LLM inference practical on CPUs and smaller devices by combining quantization support with optimized low-level inference paths.

## Where it fits in the stack
**Infrastructure / Inference Runtime**. It is a core local-serving building block used directly or via wrappers.

## Typical use cases
- Running quantized LLMs offline on laptops, servers, or edge devices
- Building local-first AI tools without cloud API dependency
- Powering higher-level local model tools and wrappers

## Comparison: llama.cpp vs. Ollama
| Feature | llama.cpp (Direct) | Ollama (Wrapper) |
| :--- | :--- | :--- |
| **User Interface** | CLI-heavy, manual configuration. | Simple CLI and REST API. |
| **Model Management**| Manual GGUF download/loading. | Automated "Pull" and management. |
| **Control** | Granular control over all parameters. | Opinionated defaults for ease of use. |
| **Performance** | Maximum throughput potential. | Minimal overhead on top of llama.cpp. |

## Strengths
- Lightweight and portable local runtime.
- Strong support for quantized model execution.
- **Agentic Features**: Native support for **MCP (Model Context Protocol)** and automatic parser generation for structured outputs (added 2026-03-07).
- Large ecosystem and broad community adoption.

## Limitations
- Requires manual model/runtime tuning for best performance
- Feature parity can vary across hardware backends
- Large models still require substantial memory/compute

## When to use it
- When privacy, offline operation, or cost control require local inference
- When you need direct control of quantization/runtime tradeoffs

## When not to use it
- When managed cloud APIs are preferred for simplicity and elasticity
- When you need frontier-model quality that local hardware cannot sustain

## Getting started

### Docker Compose Example
Run `llama.cpp` as an OpenAI-compatible server using Docker:

```yaml
services:
  llama-cpp:
    image: ghcr.io/ggerganov/llama.cpp:server
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
    command: "-m /models/llama-3-8b-instruct.Q4_K_M.gguf -c 2048 --host 0.0.0.0 --port 8080"
```

### Python API Example
Use the `openai` library to interact with your local `llama.cpp` server:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="sk-no-key-required")

response = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantization in 3 sentences."}
    ]
)

print(response.choices[0].message.content)
```

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free software; infrastructure/hardware costs still apply
- **Self-hostable**: Yes

## Performance Optimization

### Hardware Backend Selection
`llama.cpp` supports multiple backends for acceleration:

- **Apple Silicon (Metal)**: Use `-ngl 99` to offload all layers to the GPU. Ensure `LLAMA_METAL=1` during build.
- **NVIDIA (CUDA)**: Use `-ngl <num_layers>` to offload to VRAM. High memory bandwidth is key.
- **CPU (OpenBLAS/AVX)**: Use `-t <num_threads>` where threads match physical core count for best efficiency.

### Structured Output with Grammars
Native support for GBNF grammars allows forcing the model to output valid JSON or other formats:

```bash
./server -m models/llama-3.gguf --grammar-file json.gbnf
```

## Related tools / concepts
- [Local LLMs](../ai_knowledge/local_llms.md)
- [Ollama](../../services/ollama.md)
- [ZSE](zse.md)
- [vLLM](vllm.md)
- [ExLlamaV2](exllamav2.md)
- [GGUF Format](../ai_knowledge/local_llms.md)
- [Quantization Concepts](../ai_knowledge/local_llms.md)
- [MCP (Model Context Protocol)](../automation_orchestration/airops.md)
- [Jules](../ai_knowledge/jules.md)

## Sources / References
- [llama.cpp repository](https://github.com/ggml-org/llama.cpp)
- [MCP support merged](https://www.reddit.com/r/LocalLLaMA/comments/1rn23l6/mcp_support_got_merged_to_llamacpp/)
- [Automatic parser generator](https://www.reddit.com/r/LocalLLaMA/comments/1rmp3ep/llamacpp_now_with_automatic_parser_generator/)
- [Ultimate guide to running quantized LLMs on CPU with llama.cpp](https://medium.com/red-buffer/ultimate-guide-to-running-quantized-llms-on-cpu-with-llama-cpp-1a26c34bb6dd)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
