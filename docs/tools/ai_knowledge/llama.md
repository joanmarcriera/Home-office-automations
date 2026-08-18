# Llama

## What it is
**Llama** (Large Language Model Meta AI) is Meta's family of open-weights foundation models, representing the foundational lineage for open-source large language model research and deployment. Spanning generations from original Llama to Llama 2, Llama 3/3.1/3.3, and [Llama 4](llama-4.md), Llama provides the global benchmark for open model architectures.

## What problem it solves
Proprietary LLM APIs present continuous operational costs, latency overhead, vendor lock-in, and data privacy concerns for sensitive enterprise and developer workflows. The Llama model ecosystem resolves this by delivering state-of-the-art open weights, allowing organizations to fine-tune, quantize, inspect, and host enterprise-grade language models on self-managed infrastructure.

## Where it fits in the stack
**Category**: AI & Knowledge / Open Foundation Models. It sits at the **Model & Foundation Layer**, serving as the bedrock open model upon which inference engines ([ollama](../../services/ollama.md), [llama.cpp](../infrastructure/llama-cpp.md), [vLLM](../infrastructure/vllm.md)) and fine-tuning frameworks ([LLaMA Factory](../frameworks/llama-factory.md), [Unsloth](../infrastructure/unsloth.md)) are built.

## Typical use cases
- **Self-Hosted Generative AI**: Operating high-throughput text generation, summarization, and translation services on internal GPU clusters.
- **Domain-Specific Fine-Tuning**: Adapting open weights to specialized legal, medical, or technical domains using PEFT/LoRA adapters.
- **Embedded Agentic Inference**: Powering autonomous agents with low-latency structured output and tool execution capabilities.
- **Offline & Edge AI Copilots**: Running quantized Llama models on local developer workstations and edge server nodes.

## Strengths
- **Ecosystem Standard**: The universal baseline for open-weights research, quantization formats (GGUF, AWQ, EXL2), and hardware accelerators.
- **Permissive Community Licensing**: Enables commercial deployment and derivative works across small and large enterprises.
- **Broad Scale Range**: Available in parameter sizes spanning from 1B/3B compact edge models to 70B/405B frontier variants.
- **Extensive Tooling Integration**: Natively supported across virtually every major LLM runtime, framework, and vector database.

## Limitations
- **Hosting Maintenance Overhead**: Requires managing GPU infrastructure, quantization builds, and serverless endpoint scaling.
- **Hardware Capital Requirements**: Ultra-large variants (70B/405B) require multi-GPU nodes (A100/H100/B200) or high-memory unified workstations.
- **Commercial User Scale Thresholds**: Enterprise license clauses apply to services exceeding monthly active user thresholds defined in Meta's terms.

## When to use it
- When requiring an open-weights foundation for on-premise, cloud, or edge deployment.
- When customizing LLMs using proprietary datasets without sharing sensitive weights or data with closed API vendors.
- When building cost-effective, high-throughput LLM pipelines free from third-party rate limits.

## When not to use it
- For instant serverless prototyping where hosted APIs ([Claude 5.1](../providers/anthropic.md) or [GPT-5.5](../providers/openai.md)) eliminate hardware setup entirely.
- When sub-100M parameter micro-models are required for ultra-low-power microcontrollers.

## Getting started

### Installation via Hugging Face Transformers
Install standard Python dependencies:
```bash
pip install transformers torch accelerate
```

### Basic Inference with Hugging Face Transformers
Run Llama inference in Python:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "meta-llama/Llama-3.3-70B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

prompt = "Summarize the architectural evolution of Meta Llama open weights models."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## CLI examples

### Running Quantized Llama via Ollama
```bash
ollama run llama3.3
```

### High-Throughput Serving via vLLM
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

## API examples

### Python Output Validation using Pydantic v2
The following script demonstrates querying an OpenAI-compatible Llama endpoint and validating the output structure using Pydantic v2:

```python
import json
from pydantic import BaseModel, Field
from typing import List

class ModelFamilyInfo(BaseModel):
    family_name: str = Field(..., description="Name of the model family")
    developer: str = Field(..., description="Developer organization")
    key_features: List[str] = Field(..., description="Primary architectural highlights")
    license_type: str = Field(..., description="Distribution licensing terms")

def parse_llama_metadata(raw_response: str) -> ModelFamilyInfo:
    data = json.loads(raw_response)
    return ModelFamilyInfo.model_validate(data)

if __name__ == "__main__":
    sample_json = """{
        "family_name": "Meta Llama",
        "developer": "Meta AI",
        "key_features": ["Open-weights", "GGUF/AWQ Quantization", "Native Tool Use", "128k Context Window"],
        "license_type": "Llama Community License"
    }"""
    info = parse_llama_metadata(sample_json)
    print(f"Family: {info.family_name} by {info.developer}")
    print(f"Features: {', '.join(info.key_features)}")
```

## Related tools / concepts
- [Llama 4](llama-4.md)
- [Llama 4 Maverick](llama-4-maverick.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [LLaMA Factory](../frameworks/llama-factory.md)
- [Unsloth](../infrastructure/unsloth.md)
- [ollama](../../services/ollama.md)

## Sources / references
- [Meta Llama Official Developer Portal](https://llama.meta.com/)
- [Hugging Face Llama Organization](https://huggingface.co/meta-llama)
- [Meta AI Research Llama Papers](https://ai.meta.com/research/publications/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
