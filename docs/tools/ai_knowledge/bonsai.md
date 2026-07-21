# Bonsai (PrismML)

## What it is
Bonsai 27B is a multimodal flagship 27B-parameter Large Language Model (LLM) developed by PrismML, built on top of the Qwen 3.6 27B architecture. It is designed specifically to run locally on low-resource hardware like consumer laptops and mobile phones. Released on July 14, 2026, Bonsai 27B achieves extreme quantization levels, shipping in two distinct variants:
- **Ternary Bonsai 27B**: Uses ternary {-1, 0, +1} weights with FP16 group-wise scaling, resulting in 1.71 effective bits per weight. It occupies 5.9 GB of memory, making it highly suitable for everyday laptops.
- **1-bit Bonsai 27B**: Uses binary {-1, +1} weights with the same group-wise scaling, resulting in 1.125 effective bits per weight. It occupies 3.9 GB of memory, fitting comfortably within the memory limits of modern smartphones like the iPhone 17 Pro.

## What problem it solves
Historically, deploying a 27B-parameter model required heavy server infrastructure or high-end multi-GPU workstations, as a 27B model in FP16 takes approximately 54GB of space, and even a standard 4-bit quantized build requires 18GB (which is too large for consumer phones and base laptops). Bonsai 27B solves this compute and memory bottleneck by compressing the model end-to-end (across the language network, embeddings, attention, MLPs, and the LM head) to fit on edge devices with as little as 4GB-6GB of RAM, without relying on higher-precision "escape hatches" that increase memory usage.

## Where it fits in the stack
**LLM / Reasoning Engine (Open-weights / Edge-native)**. It is a core component of the [Local LLMs](local_llms.md) ecosystem. It acts as a local reasoning layer that can run directly on consumer-grade hardware. It integrates seamlessly with frameworks like [llama.cpp](../infrastructure/llama-cpp.md) and [MLX](../infrastructure/mlx.md) (via Apple Silicon), making it accessible to local orchestrators and agents.

## Typical use cases
- **On-Device Assistants**: Powering offline mobile assistants with advanced multi-step reasoning.
- **Local Document and Code Extraction**: Analyzing codebases and long-context documents privately without internet access or data egress fees.
- **Computer-Use Loops**: Operating agentic loops on standard consumer machines using native visual and screenshot understanding.
- **Edge Deployment on Smart Devices**: Running complex models on specialized hardware such as the Jetson Orin Nano or commodity laptops (e.g. NVIDIA 4060 GPUs).

## Strengths
- **Incredible Compression**: Fits a 27B-class model into a 3.9GB (1-bit) or 5.9GB (ternary) footprint.
- **High Retention of Capabilities**: The ternary model retains 94.6% of the full-precision baseline performance, keeping reasoning capabilities (math, logic) highly intact.
- **Multimodal by Design**: Integrates a compact 4-bit vision tower natively to handle screenshots, PDF rendering, and camera input.
- **End-to-End Low-Bit Quantization**: Quantizes all elements including embeddings and attention with no high-precision escape hatches.
- **Low-Latency Edge Inference**: Achieves high prefill and generation throughput on consumer GPUs and laptops (e.g., up to 600 tokens/sec prefill and 30 tokens/sec generation on standard laptop GPUs).

## Limitations
- **Reasoning Loss from Quantization**: The binary (1-bit) variant retains only 89.5% of the full-precision baseline performance and can sometimes display mild quantization artifacts (such as excessive emoji usage or slightly reduced reasoning performance).
- **Agentic Coding Constraints**: Long-horizon, multi-file software engineering tasks (such as run-test-and-repair workflows) are not yet fully optimized on this baseline model; specialized agentic variants are planned.
- **Sustained Phone Generation**: Due to thermal limitations on smartphones, sustained generation throughput eventually throttles below peak speeds.
- **KV Cache Footprint**: Currently standardizes on a 4-bit KV cache, though sub-2-bit KV cache compression is still an active research area.

## When to use it
- When absolute data privacy and 100% data sovereignty are required on standard edge hardware.
- When running local agents in low-resource or air-gapped environments (laptops with 8GB-16GB RAM or high-end mobile devices).
- For local multi-modal tasks (handling images, screenshots, or documents) with minimal memory overhead.

## When not to use it
- When performing heavy, long-horizon multi-file agentic software engineering workflows (prefer [Qwen](qwen.md), [DeepSeek](../providers/deepseek.md), or cloud models).
- If your device has plenty of high-speed unified memory or multi-GPU setups that can run unquantized FP8 models directly.
- On devices with less than 6GB of system RAM (for the 1-bit model) or 12GB of RAM (for the ternary model).

## Getting started
Bonsai 27B can be run locally using the llama.cpp engine or MLX Swift.

### Prerequisite: Download Model Weights
1. Download the quantized GGUF weights (e.g., `Ternary-Bonsai-27B-Q2_0.gguf`) and the vision companion (`mmproj.gguf`) from Hugging Face or the PrismML portal.
2. Ensure you have the latest llama.cpp binaries compiled on your machine.

### Installation & Run via llama.cpp
```bash
# Clone and build llama.cpp if not already installed
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j

# Execute Bonsai 27B via llama-cli with multimodal support
./llama-cli \
  -m ./models/Ternary-Bonsai-27B-Q2_0.gguf \
  --mmproj ./models/mmproj.gguf \
  -c 4096 \
  -p "Explain the benefits of end-to-end low-bit quantization."
```

## CLI examples

### Running the 1-bit variant on Apple Silicon (MLX Swift CLI)
```bash
# Run the 1-bit binary companion natively on macOS
mlx-swift-chat --model prism-ml/Bonsai-27B-mlx-1bit --temp 0.2
```

### Benchmarking performance with llama-bench
```bash
# Benchmark prefill and generation throughput on your local GPU
./llama-bench -m ./models/Ternary-Bonsai-27B-Q2_0.gguf -n 128 -b 512
```

## API examples

### Python: Local Inference using MLX-LM on macOS
The following script demonstrates how to load and query Bonsai 27B locally on Apple Silicon.

```python
from mlx_lm import load, generate

# Load the low-bit model and tokenizer
model, tokenizer = load("prism-ml/Bonsai-27B-mlx-1bit")

# Define prompt and generate response
prompt = "Explain the difference between binary and ternary model weights."
response = generate(
    model,
    tokenizer,
    prompt=prompt,
    max_tokens=150,
    temp=0.1
)

print(response)
```

### Serving via OpenAI-Compatible Local Endpoint
You can spin up an OpenAI-compatible API server using llama.cpp to integrate Bonsai 27B with local agent harnesses.

```python
import openai

# Initialize client pointing to local llama.cpp server
client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="local-key"
)

completion = client.chat.completions.create(
    model="Bonsai-27B",
    messages=[
        {"role": "user", "content": "Analyze this screenshot for user interface errors."}
    ]
)

print(completion.choices[0].message.content)
```

## Related tools / concepts
- [Local LLMs](local_llms.md) — The core edge-native LLM ecosystem overview.
- [Qwen](qwen.md) — The foundational Qwen 3.6 model family which Bonsai is derived from.
- [DeepSeek](../providers/deepseek.md) — Standard-setting open-weights models.
- [Ollama](../../services/ollama.md) — The industry-standard local LLM runner and orchestrator.
- [llama.cpp](../infrastructure/llama-cpp.md) — The high-performance C/C++ inference engine supporting Bonsai GGUFs.
- [MLX](../infrastructure/mlx.md) — Apple Silicon's optimized array framework for on-device execution.
- [ExLlamaV2](../infrastructure/exllamav2.md) — Alternative high-performance inference engine for NVIDIA GPUs.
- [LM Studio](../infrastructure/lm-studio.md) — Graphical desktop companion for running local models.
- [Jan.ai](../infrastructure/jan-ai.md) — Local-first open-source LLM chat application.
- [Unsloth](../infrastructure/unsloth.md) — High-efficiency model fine-tuning tool used for extreme low-bit steering.

## Sources / references
- [PrismML Announcement](https://prismml.com/news/bonsai-27b)
- [PrismML Documentation Portal](https://docs.prismml.com/models/bonsai-27b)
- [Hugging Face Repository: prism-ml/Bonsai-27B-mlx-1bit](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit)
- [Reddit LocalLLaMA Thread: Announcing Bonsai 27B](https://www.reddit.com/r/LocalLLaMA/comments/1uwhukq/bonsai_27b_the_first_27bclass_model_to_run_on_a/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
