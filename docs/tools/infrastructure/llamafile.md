# Llamafile

## What it is
Llamafile is a project (originally from Mozilla) that packages an entire LLM — model weights **and** the inference runtime — into a **single executable file** that runs on macOS, Linux, Windows, and BSD without installation. It combines [llama.cpp](llama-cpp.md) with the Cosmopolitan Libc "Actually Portable Executable" format, so one downloaded file launches a local chat server with no dependencies.

## What problem it solves
It collapses the usual local-LLM setup (install runtime, fetch weights, configure flags) into "download one file and run it." This makes local inference trivially reproducible and ideal for **air-gapped distribution**: you can hand someone a USB stick with a single file and they have a working offline assistant, no toolchain required.

## Where it fits in the stack
**Infrastructure / Self-contained local inference.** It is the lowest-friction way to ship or archive a runnable model. It exposes an OpenAI-compatible endpoint, so it can act as a drop-in local backend for agents, automation in [n8n](../../services/n8n.md), or scripts.

## Typical use cases
- Distributing a ready-to-run offline model to machines with no internet or package managers.
- Keeping a long-term, dependency-free archive of a model that will still run years later.
- Quick local experimentation: download, `chmod +x`, run, and get a chat server.
- Embedding a portable local LLM into a larger offline appliance or kiosk.

## Strengths
- **Single-file portability:** no install, no runtime, no virtualenv — one file is the whole stack.
- **Truly offline & archival:** self-contained binaries keep working without network or future dependency drift.
- **OpenAI-compatible server:** integrates with existing tooling expecting an OpenAI API.
- **Cross-platform from one artifact:** the same file runs across major OSes and CPU architectures.

## Limitations
- **Large files:** weights are embedded, so binaries can be several gigabytes.
- **Platform quirks:** some OSes impose executable-size limits or require an extra step for very large files.
- **Single-model artifact:** each file is one model; managing many models is less convenient than a model manager like [Ollama](../../services/ollama.md).
- **Performance ceiling:** inherits llama.cpp's characteristics; not aimed at high-concurrency serving.

## When to use it
- When you need a **zero-install, offline** model that "just runs" on heterogeneous machines.
- For air-gapped or archival scenarios where future reproducibility matters.
- For demos or handoffs where you cannot assume any local toolchain.

## When not to use it
- When you juggle many models and want central management — use [Ollama](../../services/ollama.md).
- For scaled, multi-user, high-throughput serving — use [vLLM](vllm.md).

## Getting started

### 1. Download and Execute
Download a pre-built llamafile (e.g., Qwen3.5 0.8B) and run it immediately:
```bash
# Download the model
curl -LO https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-0.8B-Q8_0.llamafile

# Make it executable (macOS/Linux)
chmod +x Qwen3.5-0.8B-Q8_0.llamafile

# Start the local server
./Qwen3.5-0.8B-Q8_0.llamafile
```

### 2. Access the UI
Once running, open your browser to `http://127.0.0.1:8080` to interact with the model via a built-in web interface.

## CLI examples
Llamafile binaries support standard llama.cpp flags for advanced configuration.

```bash
# Run in text-generation mode (no server)
./model.llamafile -p "The capital of France is" --temp 0.7

# Run as a server on a specific port with GPU offloading
./model.llamafile --server --port 9000 -ngl 99

# Specify the number of CPU threads to use
./model.llamafile -t 8 -p "Explain quantum physics:"
```

## API examples
Llamafile provides an OpenAI-compatible API on its default port.

### Chat Completions (Python)
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="sk-no-key-required"
)

response = client.chat.completions.create(
    model="llamafile",
    messages=[{"role": "user", "content": "Tell me a joke about llamas."}]
)

print(response.choices[0].message.content)
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 tooling; model weights carry their own licenses)
- **Cost**: Free
- **Self-hostable**: Yes (entirely local, single binary)

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — The inference engine Llamafile embeds.
- [Ollama](../../services/ollama.md) — Multi-model local runtime and manager.
- [GPT4All](gpt4all.md) — Desktop offline assistant with document RAG.
- [LM Studio](lm-studio.md) — Desktop local-LLM application.
- [Kiwix](../../services/kiwix.md) — Companion pattern for offline knowledge distribution.
- [LocalAI](localai.md) — Self-hosted OpenAI-compatible local API server.
- [vLLM](vllm.md) — High-throughput serving engine for the scaled case.
- [MLX](mlx.md) — Apple-silicon local inference backend.

## Sources / references
- [Llamafile GitHub (Mozilla-Ocho)](https://github.com/Mozilla-Ocho/llamafile)
- [Cosmopolitan Libc](https://github.com/jart/cosmopolitan)
- [Introducing Llamafile (Mozilla blog)](https://hacks.mozilla.org/2023/11/introducing-llamafile/)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
