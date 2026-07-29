# NVIDIA

## What it is
NVIDIA is a global leader in AI hardware and software, providing an extensive ecosystem for model training, deployment, and inference through its GPU technology and the NVIDIA AI Enterprise platform. As of late October / November 2026, NVIDIA dominates the inference landscape with the **Rubin architecture** GPUs and **NIM (NVIDIA Inference Microservices)**, which are now in General Availability (GA) across all major cloud and on-premises platforms.

## What problem it solves
NVIDIA provides the high-performance compute infrastructure necessary for modern AI. Through the NVIDIA API Catalog and NVIDIA NIM, it offers optimized, scalable inference for a wide range of open and proprietary models, reducing the "time to first token" for real-time agentic applications and multi-modal pipelines.

## Where it fits in the stack
**Compute Infrastructure / Model Provider / Inference Engine**. NVIDIA provides both the hardware (Blackwell/Rubin GPUs) and the software stack (CUDA, TensorRT, NIM) that powers the majority of the AI ecosystem.

## Typical use cases
- **Enterprise Model Deployment**: Using NVIDIA NIM for production-grade inference of models like Llama 4, Mistral, and Nemotron.
- **Agentic RAG Pipelines**: Utilizing NVIDIA NeMo Retriever for high-fidelity retrieval and reasoning.
- **Local AI Acceleration**: Running models locally with TensorRT-LLM for maximum performance on RTX workstations.
- **Omniverse Simulation**: Integrating AI agents into 3D simulations for industrial automation.

## Strengths
- **Performance**: Industry-leading inference speeds through hardware-software co-optimization (Rubin/Blackwell).
- **Ecosystem**: Optimized NIMs available for almost all popular open-weights models (Llama 4, Qwen 3.6, Mistral).
- **Enterprise-Ready**: Focus on security, manageability, and 24/7 support through NVIDIA AI Enterprise.
- **Scale**: Seamless transition from local RTX workstations to multi-node H100/B200/R100/R200 clusters.

## Limitations
- **Hardware Lock-in**: Many software optimizations (TensorRT) are specific to NVIDIA GPU architectures.
- **Complexity**: The full enterprise stack can be complex to manage compared to simpler API-only providers.
- **Cost**: High-end enterprise GPUs and licenses represent a significant capital or operational expense.

## When to use it
- When you need the absolute highest performance and lowest latency for model inference.
- When deploying AI models in an enterprise environment requiring secure, containerized NIMs.
- For local acceleration on NVIDIA RTX hardware in a homelab or workstation.
- When building multi-modal agents that require tight integration with vision or simulation.

## When not to use it
- If you are committed to non-NVIDIA hardware (AMD, Apple Silicon, or cloud-specific chips like AWS Trainium/Inferentia).
- For simple, low-volume projects where a basic API provider (like Groq or Together) might be simpler.
- When strict open-source software requirements preclude the use of proprietary drivers or stacks.

## Getting started

NVIDIA offers a hosted API catalog for developers to test models before deploying them on-premises.

1. Visit [build.nvidia.com](https://build.nvidia.com/).
2. Generate an API key for the API Catalog.
3. Choose a model (e.g., Llama-4) and select the "API" tab for integration details.

## CLI examples

### 1. Querying NVIDIA API Catalog via Curl
A standard OpenAI-compatible call to test a hosted model:

```bash
curl -X POST "https://integrate.api.nvidia.com/v1/chat/completions" \
     -H "Authorization: Bearer $NVIDIA_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "meta/llama-4",
       "messages": [{"role": "user", "content": "Optimize this CUDA kernel."}],
       "temperature": 0.2,
       "max_tokens": 1024
     }'
```

### 2. Running a Local NIM with Docker
Deploy a pre-optimized model microservice on your local GPU (Rubin/Blackwell optimized):

```bash
docker run -it --rm --runtime=nvidia --gpus all \
    -e NGC_API_KEY=$NGC_API_KEY \
    -v "$LOCAL_CACHE:/opt/nim/.cache" \
    -p 8000:8000 \
    nvcr.io/nim/meta/llama-4:latest
```

### 3. Benchmarking with TensorRT-LLM
Compile a model for maximum local performance:
```bash
python3 scripts/build_engine.py --model_dir ./llama-4 --output_dir ./engine --tp_size 1
```

## API examples

### 1. Python: OpenAI-Compatible Client
Integrate NVIDIA-hosted models into your application with minimal code changes:

```python
from openai import OpenAI

client: OpenAI = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="$NVIDIA_API_KEY"
)

completion = client.chat.completions.create(
    model="nvidia/nemotron-4-340b-instruct",
    messages=[{"role": "user", "content": "Generate a synthetic dataset for RAG."}],
    stream=True
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
```

### 2. Using LangChain with NVIDIA NIM
Connect to a self-hosted NIM instance:

```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Connect to a local NIM instance
llm: ChatNVIDIA = ChatNVIDIA(base_url="http://localhost:8000/v1", model="llama-4")
response = llm.invoke("Explain the Rubin architecture.")
print(response.content)
```

### 3. Python: Programmatic CUDA Code Analysis with Pydantic v2 Validation
Leverage structured outputs via Pydantic v2 validation and strict type-hints to parse performance metrics:

```python
import json
from typing import List
from pydantic import BaseModel, Field, TypeAdapter

class CudaKernelOptimization(BaseModel):
    kernel_name: str = Field(..., description="The name of the analyzed CUDA kernel.")
    optimizations_applied: List[str] = Field(..., description="List of optimizations applied.")
    estimated_speedup: float = Field(..., description="The estimated performance speedup multiplier.")
    register_count_per_thread: int = Field(..., description="The resulting register count per thread.")

# Simulated model JSON output response
raw_response: str = """{
  "kernel_name": "vectorAdd",
  "optimizations_applied": [
    "Shared memory bank conflict resolution",
    "Coalesced global memory access alignment"
  ],
  "estimated_speedup": 3.2,
  "register_count_per_thread": 32
}"""

# Use Pydantic v2 TypeAdapter for validation
adapter: TypeAdapter[CudaKernelOptimization] = TypeAdapter(CudaKernelOptimization)
result: CudaKernelOptimization = adapter.validate_json(raw_response)

print(f"Kernel: {result.kernel_name}")
print(f"Speedup: {result.estimated_speedup:.1f}x")
assert result.estimated_speedup > 1.0
```

## Related tools / concepts
- [NVIDIA Nemotron-3 Super](../ai_knowledge/nemotron.md)
- [NVIDIA NeMo Retriever](../agents/nemo-retriever.md)
- [Groq](groq.md)
- [Together AI](together.md)
- [TGI (Text Generation Inference)](../infrastructure/tgi.md)
- [Local LLMs](../ai_knowledge/local_llms.md)
- [Llama 4](../ai_knowledge/local_llms.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)
- [Google Axion](../../knowledge_base/google_axion.md)

## Sources / references
- [NVIDIA Official Website](https://www.nvidia.com/)
- [NVIDIA API Catalog](https://build.nvidia.com/)
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
- [NVIDIA Rubin Architecture Whitepaper](https://www.nvidia.com/en-us/data-center/rubin-architecture/)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
