# KatCoderAir

## What it is
KatCoderAir (specifically KatCoderAir v2.5) is a highly optimized, open-weight coding Large Language Model (LLM) developed by the KatCoder Collective. Engineered with a specialized focus on low-latency, edge-native software development, it is designed to run efficiently on consumer workstations, laptops, and local hardware setups. Based on an advanced Mixture-of-Experts (MoE) architecture, KatCoderAir v2.5 balances parameter size with execution speed, allowing developers to enjoy top-tier code intelligence without relying on costly cloud providers.

## What problem it solves
Proprietary cloud-based coding assistants often suffer from latency issues, high cost of operation, and severe security concerns regarding source code telemetry and data residency. KatCoderAir v2.5 addresses these pain points by offering a powerful, open-weight coding alternative that can be deployed entirely locally. By running on local hardware, it guarantees absolute privacy, zero latency variation, and complete operational sovereignty.

## Where it fits in the stack
**Category**: Providers / AI Assistants & Knowledge. KatCoderAir fits directly into the local inference tier. It is supported by popular runtimes like [llama.cpp](../infrastructure/llama-cpp.md), [MLX](../infrastructure/mlx.md), and [ExLlamaV3](../infrastructure/exllamav3.md). It acts as the backbone reasoning engine for local coding agents and IDE extensions.

## Typical use cases
- **Local Autocomplete**: Delivering sub-100ms autocomplete in IDEs such as VS Code.
- **Offline Codebase Generation**: Creating complete multi-file modules in private, air-gapped environments.
- **Code Refactoring and Optimization**: Performing complex code restructuring tasks privately on local hardware.
- **Automated CLI Coding**: Driving agentic developer cycles via terminal assistants like [Aider](../development_ops/aider.md).

## Strengths
- **Low Latency**: Highly optimized attention and routing mechanisms yield exceptional tokens-per-second (TPS) throughput.
- **Extensive Context Window**: Out-of-the-box support for a 128k context window allows entire codebases to be scanned locally.
- **Highly Resource-Efficient**: The MoE architecture enables running a model with a virtual 30B parameter size using only 7B active parameters.
- **Superior Multi-lingual Support**: Highly optimized for Python, TypeScript, Rust, C++, and Go.

## Limitations
- **General Knowledge**: Not a general-purpose model; trails behind [Qwen](../ai_knowledge/qwen.md) and [DeepSeek](deepseek.md) in general trivia, creative writing, or non-technical reasoning.
- **High Concurrency VRAM Footprint**: Though active parameters are small, loading the full MoE weights requires substantial VRAM if running multiple concurrent streams.
- **Setup Complexity**: Requires local model execution setup, which can be more complex than subscribing to a SaaS provider.

## When to use it
- When you require complete, local data privacy for sensitive corporate codebases.
- When you need a reliable offline coding assistant on a consumer GPU or unified memory Mac.
- When latency and immediate response are critical for your autocomplete and chat integrations.

## When not to use it
- For broad creative writing, general knowledge retrieval, or multi-modal analysis.
- If you do not have a modern GPU with at least 16GB VRAM (or Apple Silicon unified memory).
- If your workflow is fully integrated with cloud-only ecosystems like [Codestral](codestral.md).

## Getting started
To run KatCoderAir v2.5 locally, you can use the GGUF weights via llama.cpp or the MLX format on macOS.

### Installation
Ensure you have the latest `llama.cpp` tools compiled on your path.
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make -j
```

### Run Model
Download the quantized GGUF file and run it using the following command:
```bash
./llama-cli \
  -m ./models/katcoderair-2.5-q4_k_m.gguf \
  -c 8192 \
  -p "Write a Python script that implements a thread-safe cache."
```

## CLI examples

### Querying the model via curl
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "katcoderair-v2.5",
    "messages": [
      {"role": "user", "content": "Explain how to write a custom decorator in Python."}
    ]
  }'
```

### Running benchmark via llama-bench
```bash
./llama-bench -m ./models/katcoderair-2.5-q4_k_m.gguf -t 8 -b 512
```

## API examples

### Python: local inference using llama-cpp-python
```python
from llama_cpp import Llama

# Load the KatCoderAir model
llm = Llama(
    model_path="./models/katcoderair-2.5-q4_k_m.gguf",
    n_ctx=2048,
    n_threads=4
)

# Generate coding solution
output = llm(
    "Q: Write a Rust function to parse a CSV file. A:",
    max_tokens=256,
    stop=["Q:", "\n\n"],
    echo=True
)
print(output["choices"][0]["text"])
```

### Local Endpoint integration with OpenAI-compatible client
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="local"
)

completion = client.chat.completions.create(
    model="katcoderair",
    messages=[
        {"role": "user", "content": "Refactor this code to use async/await."}
    ]
)
print(completion.choices[0].message.content)
```

## Related tools / concepts
- [Local LLMs](../ai_knowledge/local_llms.md) — Standard overview of open weights models.
- [DeepSeek](deepseek.md) — The flagship MoE open-weight models.
- [Codestral](codestral.md) — Coding model from Mistral AI.
- [llama.cpp](../infrastructure/llama-cpp.md) — The primary runtime engine for CPU/GPU.
- [MLX](../infrastructure/mlx.md) — Apple Silicon array framework.
- [ExLlamaV3](../infrastructure/exllamav3.md) — NVIDIA-optimized local inference.
- [Aider](../development_ops/aider.md) — CLI-based AI editing tool.
- [Qwen](../ai_knowledge/qwen.md) — Foundational open-weight Qwen architecture.

## Sources / references
- [KatCoder Collective GitHub](https://github.com/katcoder-collective/katcoderair)
- [Reddit LocalLLaMA Thread: KatCoderAir v2.5 Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1uwbe7w/katcoderair_v25_open_model_soon/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
