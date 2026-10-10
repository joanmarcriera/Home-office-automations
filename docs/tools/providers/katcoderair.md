# KatCoderAir

## What it is
KatCoderAir (specifically KatCoderAir v2.5) is a highly optimized, open-weight coding Large Language Model (LLM) developed by the KatCoder Collective. Engineered with a specialized focus on low-latency, edge-native software development, it is designed to run efficiently on consumer workstations, laptops, and local hardware setups. Based on an advanced Mixture-of-Experts (MoE) architecture, KatCoderAir v2.5 balances parameter size with execution speed, allowing developers to enjoy top-tier code intelligence without relying on costly cloud providers.

In early 2027, the KatCoder Collective expanded its suite with **Kat Coder 2.5 Dev**, a specialized developmental-grade coding model designed specifically for aggressive multi-file code reasoning, deep AST analysis, FastMCP 3.1 Task Protocol execution, and agentic code modifications. Operating with a virtual 30B parameter size via 7B active parameters per token, Kat Coder 2.5 Dev is tailored for developers seeking raw reasoning power and high instruction-following accuracy in software engineering domains.

```
+-----------------------------------------------------------------------------------+
|                        KatCoderAir Local MoE Routing Architecture                  |
|                                                                                   |
|  +--------------------+    +----------------------+    +-----------------------+  |
|  | User / FastMCP Client|===>| GGUF / MLX Runtime   |===>| Gating Router         |  |
|  | (Code Query / Task)|    | (llama.cpp / ExLlama) |    | (Token Classifier)    |  |
|  +--------------------+    +----------------------+    +-----------------------+  |
|                                                                    ||             |
|                                      +-----------------------------+              |
|                                      ||                            ||             |
|                                      \/                            \/             |
|                            +-------------------+         +-------------------+    |
|                            | Active Expert #1  |         | Active Expert #2  |    |
|                            | (Syntax / AST)    |         | (Type Checker)    |    |
|                            +-------------------+         +-------------------+    |
|                                      ||                            ||             |
|                                      +-----------------------------+              |
|                                                                    ||             |
|                                                                    \/             |
|                                                        +-----------------------+  |
|                                                        | Generated Code Output |  |
|                                                        | (Sub-100ms Latency)   |  |
|                                                        +-----------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Proprietary cloud-based coding assistants often suffer from latency issues, high cost of operation, and severe security concerns regarding source code telemetry and data residency. KatCoderAir and Kat Coder 2.5 Dev address these pain points by offering powerful, open-weight coding alternatives that can be deployed entirely locally. By running on local hardware, they guarantee absolute privacy, zero latency variation, and complete operational sovereignty.

## Where it fits in the stack
**Category**: Providers / AI Assistants & Knowledge. KatCoderAir and Kat Coder 2.5 Dev fit directly into the local inference tier. Supported by popular runtimes like [llama.cpp](../infrastructure/llama-cpp.md), [MLX](../infrastructure/mlx.md), and [ExLlamaV3](../infrastructure/exllamav3.md), they act as the backbone reasoning engine for local coding agents, terminal assistants, and IDE extensions.

## Typical use cases
- **Local Autocomplete**: Delivering sub-100ms autocomplete in IDEs such as VS Code.
- **Offline Codebase Generation**: Creating complete multi-file modules in private, air-gapped environments.
- **Advanced Code Refactoring**: Executing complex AST-level optimizations, lint-fixing, and system restructuring using Kat Coder 2.5 Dev.
- **Automated CLI Coding**: Driving agentic developer cycles via terminal assistants like [Aider](../development_ops/aider.md) and [Cline](../agents/cline.md).

## Local Coding Model Comparison

| Feature | KatCoderAir v2.5 | DeepSeek-V4 | Qwen 3.6 Coder | Codestral 25.01 |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | MoE (30B Total / 7B Active) | MoE (671B Total / 37B Active) | Dense 32B | Dense 22B |
| **Min VRAM Requirement** | 16 GB (Q4_K_M) | 80 GB+ (Quantized) | 24 GB | 16 GB |
| **Context Window** | 128k Tokens | 128k Tokens | 128k Tokens | 32k Tokens |
| **AST-Aware Attention** | Native in 2.5 Dev | General Code Attention | Specialized | General Code Attention |
| **FastMCP 3.1 Support** | Direct Task Schema Runner | Agent Protocol | Agent Protocol | Tool Calling Endpoint |
| **Offline Performance** | Sub-100ms on Consumer GPU | Requires High-End Server | Medium Latency | Sub-200ms |

## Strengths
- **Low Latency**: Highly optimized attention and routing mechanisms yield exceptional tokens-per-second (TPS) throughput.
- **Extensive Context Window**: Out-of-the-box support for a 128k context window allows entire codebases to be scanned locally.
- **Highly Resource-Efficient**: The MoE architecture enables running a model with a virtual 30B parameter size using only 7B active parameters.
- **Superior Multi-lingual Support**: Highly optimized for Python, TypeScript, Rust, C++, and Go.
- **AST-Aware Reasoning**: Kat Coder 2.5 Dev features specialized attention maps focused on syntax structural dependencies.

## Limitations
- **General Knowledge**: Not a general-purpose model; trails behind [Qwen](../ai_knowledge/qwen.md), [DeepSeek](deepseek.md) (DeepSeek-V4), and Gemma 4 in general trivia, creative writing, or non-technical reasoning.
- **High Concurrency VRAM Footprint**: Though active parameters are small, loading the full MoE weights requires substantial VRAM if running multiple concurrent streams.
- **Setup Complexity**: Requires local model execution setup, which can be more complex than subscribing to a SaaS provider.

## When to use it
- When you require complete, local data privacy for sensitive corporate codebases.
- When you need a reliable offline coding assistant on a consumer GPU or unified memory Mac.
- When latency and immediate response are critical for your autocomplete and chat integrations.
- When performing complex developmental code generation where specialized coding logic is required (using Kat Coder 2.5 Dev).

## When not to use it
- For broad creative writing, general knowledge retrieval, or multi-modal analysis.
- If you do not have a modern GPU with at least 16GB VRAM (or Apple Silicon unified memory).
- If your workflow is fully integrated with cloud-only ecosystems like [Codestral](codestral.md).

## Getting started
To run KatCoderAir v2.5 or Kat Coder 2.5 Dev locally, you can use the GGUF weights via llama.cpp or the MLX format on macOS.

### Installation
Ensure you have the latest `llama.cpp` tools compiled on your path.
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make -j
```

### Run Model
Download the quantized GGUF file and run it using the following command:
```bash
# Run KatCoderAir v2.5
./llama-cli \
  -m ./models/katcoderair-2.5-q4_k_m.gguf \
  -c 8192 \
  -p "Write a Python script that implements a thread-safe cache."

# Run Kat Coder 2.5 Dev
./llama-cli \
  -m ./models/katcoder-2.5-dev-q4_k_m.gguf \
  -c 16384 \
  -p "Implement a custom memory-mapped key-value store in Rust."
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

### FastMCP 3.1 Code Generation Tool Server
This example demonstrates wrapping a local KatCoderAir endpoint inside a FastMCP 3.1 server to provide autonomous agents with offline code generation tools.

```python
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import json

mcp = FastMCP("KatCoderAir-Code-Server")

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="local-katcoder"
)

@mcp.tool()
def generate_python_module(task_description: str, include_tests: bool = True) -> Dict[str, Any]:
    """Generates clean, type-hinted Python code using local KatCoderAir v2.5."""
    prompt = f"Write a complete Python module for: {task_description}."
    if include_tests:
        prompt += " Include pytest unit test cases at the end."

    response = client.chat.completions.create(
        model="katcoderair-v2.5",
        messages=[
            {"role": "system", "content": "You are KatCoderAir. Output production-ready Python code with clear docstrings."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    code_output = response.choices[0].message.content
    return {
        "status": "success",
        "generated_code": code_output,
        "model_used": "katcoderair-v2.5"
    }

if __name__ == "__main__":
    mcp.run()
```

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

### Structured Output and Schema Validation (Pydantic v2)
This example demonstrates how an OpenAI-compatible client connecting to a local KatCoderAir instance parses and strictly validates code refactoring outputs using **Pydantic v2**.

```python
import os
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

# Initialize client to connect to local KatCoderAir endpoint (running on localhost)
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="local-dev-key"
)

# Define Pydantic v2 schema for structured code refactoring outputs
class RefactoringResult(BaseModel):
    original_code: str = Field(description="The source code before refactoring")
    refactored_code: str = Field(description="The cleaner, optimized code output")
    explanations: list[str] = Field(default_factory=list, description="Reasoning and optimization steps taken")

try:
    response = client.chat.completions.create(
        model="katcoderair-v2.5",
        messages=[
            {"role": "system", "content": "You are KatCoderAir. Refactor the code and output ONLY valid JSON matching the requested schema."},
            {"role": "user", "content": "Code: def add(a, b): return a+b"}
        ],
        response_format={
            "type": "json_object",
            "schema": RefactoringResult.model_json_schema()
        }
    )

    # Strictly validate output with Pydantic v2
    raw_content = response.choices[0].message.content
    result = RefactoringResult.model_validate_json(raw_content)
    print(f"Refactored Code:\n{result.refactored_code}")
    print(f"Optimizations: {', '.join(result.explanations)}")

except ValidationError as e:
    print(f"Pydantic validation failed: {e}")
except Exception as e:
    print(f"API call to local KatCoderAir failed: {e}")
```

## Operational Best Practices

### VRAM & Quantization Tuning
1. **Quantization Selection**: For consumer GPUs with 16GB VRAM (NVIDIA RTX 4080 / 5070), use `Q4_K_M` GGUF quantization. For Apple Silicon unified memory (32GB+ M-series Macs), use `Q8_0` or 16-bit MLX weights.
2. **Context Shift Management**: Set `-c 16384` for IDE completion tasks. When analyzing multi-file codebases, enable context shifting (`--ctx-shift`) in llama.cpp to maintain high token throughput across multi-turn developer chat sessions.
3. **MoE Offloading**: Ensure all MoE router gating layers and active experts are offloaded to GPU memory (`-ngl 99`) to eliminate CPU host-RAM transfer overhead during token generation.

## Related tools / concepts
- [Local LLMs](../ai_knowledge/local_llms.md) — Standard overview of open weights models.
- [DeepSeek](deepseek.md) — The flagship MoE open-weight models (DeepSeek-V4).
- [Codestral](codestral.md) — Coding model from Mistral AI.
- [llama.cpp](../infrastructure/llama-cpp.md) — The primary runtime engine for CPU/GPU.
- [MLX](../infrastructure/mlx.md) — Apple Silicon array framework.
- [ExLlamaV3](../infrastructure/exllamav3.md) — NVIDIA-optimized local inference.
- [Aider](../development_ops/aider.md) — CLI-based AI editing tool.
- [Qwen](../ai_knowledge/qwen.md) — Foundational open-weight Qwen architecture.

## Sources / references
- [KatCoder Collective GitHub](https://github.com/katcoder-collective/katcoderair)
- [Reddit LocalLLaMA Thread: KatCoderAir v2.5 Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1uwbe7w/katcoderair_v25_open_model_soon/)
- [Reddit LocalLLaMA Thread: Kat Coder 2.5 Dev - Do yourself a favor and try it](https://www.reddit.com/r/LocalLLaMA/comments/1ve9r2q/kat_coder_25_dev_do_yourself_a_favor_and_try_it/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
