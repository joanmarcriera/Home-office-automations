# Llama 4

## What it is
**Llama 4** is Meta's next-generation open-weights foundation model family, introducing a native Mixture-of-Experts (MoE) architecture, native multimodal comprehension (vision, document, and language), extended context windows up to 128k+ tokens, and native FastMCP 3.1 tool integration.

## What problem it solves
Legacy dense foundation models often require excessive memory and compute per token, scaling costs linearly with capability. Llama 4's sparse Mixture-of-Experts architecture activates only a fraction of total parameters per token, delivering frontier-class reasoning and multimodal performance at dramatically reduced latency and inference energy costs.

## Where it fits in the stack
**Category**: AI & Knowledge / Open Foundation Models. It operates at the **Model & Foundation Layer**, acting as the core open-weights reasoning and vision engine across local inference servers ([vLLM](../infrastructure/vllm.md), [llama.cpp](../infrastructure/llama-cpp.md), [ollama](../../services/ollama.md)) and fine-tuning frameworks ([Unsloth](../infrastructure/unsloth.md), [PEFT](../infrastructure/peft.md)).

## Typical use cases
- **Multi-Modal Document & Image Analytics**: Comprehending technical diagrams, UI mockups, and complex financial tables directly alongside textual context.
- **Enterprise Agentic Workflows**: Orchestrating multi-step automation using FastMCP 3.1 tool calls with deterministic schema adherence.
- **On-Premise Developer Copilots**: Supplying low-latency inline code completions and multi-file code generation on internal network hardware.
- **Privacy-Restricted Processing**: Analyzing sensitive corporate and personal documents in air-gapped environments.

## Strengths
- **Sparse MoE Efficiency**: High parameter capacity with sub-exponential active parameter compute costs per generation step.
- **Native FastMCP 3.1 Primitives**: Built-in awareness of tool schemas, tool discovery, and structured JSON-RPC execution.
- **Integrated Multimodality**: Joint vision-language pre-training eliminates external image encoder alignment overhead.
- **Extensive Ecosystem Support**: Immediate support across Hugging Face, vLLM, TensorRT-LLM, Ollama, and LM Studio.

## Limitations
- **High Total VRAM Footprint**: Offloading non-active MoE expert weights requires substantial total VRAM even if active FLOPs are low.
- **Quantization Complexity**: MoE routing matrices require specialized quantization approaches (e.g., AWQ, MoE-aware GGUF) to avoid accuracy degradation.
- **Licensing Compliance**: Governed by the Llama 4 Community License, requiring enterprise compliance tracking.

## When to use it
- When seeking the highest-performing open-weights foundation model for agentic workflows, local coding, and document understanding.
- When requiring native multimodal reasoning alongside FastMCP 3.1 tool execution.
- When self-hosting on modern GPU accelerators (A100, H100, B200) or Apple Silicon clusters.

## When not to use it
- For constrained micro-edge hardware with under 8GB VRAM (use lighter models like [Gemma 4](gemma.md)).
- When turn-key managed API endpoints are preferred without server infrastructure maintenance.

## Getting started

### Installation
Install Ollama to easily serve Llama 4 locally on macOS, Linux, or Windows:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Hello-world example
Pull and run Llama 4 in non-interactive mode:

```bash
ollama run llama4 "Hello world! Explain Llama 4 sparse MoE architecture in two sentences."
```

## CLI examples

### 1. Interactive Model Session with System Prompt
Launch an interactive CLI prompt session using Ollama:

```bash
ollama run llama4 --system "You are a senior system architect assisting with homelab setup."
```

### 2. Serving via vLLM OpenAI-Compatible Server
Start a high-throughput vLLM serving engine on port 8000:

```bash
vllm serve meta-llama/Llama-4-70B-Instruct --port 8000 --max-model-len 32768
```

### 3. Native Quantized Execution via llama.cpp
Run quantized GGUF weights directly via `llama-cli`:

```bash
llama-cli -m ./models/llama-4-70b-Q4_K_M.gguf -p "Analyze sparse Mixture-of-Experts routing." -n 256
```

## API examples

### Python Generation with Structured Pydantic v2 Schema
The following script demonstrates generating structured output from a local Llama 4 endpoint and validating it using Pydantic v2:

```python
import json
from pydantic import BaseModel, Field
from typing import List

class MoEArchitectureDetails(BaseModel):
    model_name: str = Field(..., description="Name of the model")
    total_parameters_billion: float = Field(..., gt=0, description="Total parameters in billions")
    active_parameters_billion: float = Field(..., gt=0, description="Active parameters per token in billions")
    num_experts: int = Field(..., ge=1, description="Total number of expert sub-networks")
    supported_modalities: List[str] = Field(..., description="List of supported modalities")

def parse_moe_spec(raw_json_str: str) -> MoEArchitectureDetails:
    parsed = json.loads(raw_json_str)
    return MoEArchitectureDetails.model_validate(parsed)

if __name__ == "__main__":
    sample_response = """{
        "model_name": "Llama 4 70B MoE",
        "total_parameters_billion": 70.0,
        "active_parameters_billion": 12.5,
        "num_experts": 16,
        "supported_modalities": ["Text", "Vision", "Document OCR", "FastMCP 3.1 Tools"]
    }"""
    spec = parse_moe_spec(sample_response)
    print(f"Model: {spec.model_name}")
    print(f"Active FLOPs: {spec.active_parameters_billion}B / {spec.total_parameters_billion}B total")
```

## Related tools / concepts
- [Llama](llama.md)
- [Llama 4 Maverick](llama-4-maverick.md)
- [FastMCP](../automation_orchestration/mcp.md)
- [ollama](../../services/ollama.md)
- [vLLM](../infrastructure/vllm.md)
- [llama.cpp](../infrastructure/llama-cpp.md)

## Sources / references
- [Meta AI Llama 4 Release Hub](https://ai.meta.com/llama/)
- [Hugging Face Meta-Llama 4 Organization](https://huggingface.co/meta-llama)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
