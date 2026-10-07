# Baseten

## What it is
Baseten is a high-performance, developer-focused AI inference provider designed for deploying, serving, and scaling machine learning models in enterprise production environments. Built as a serverless infrastructure platform with native cold-start optimization, active weight-caching, and auto-scaling GPU pools, Baseten provides specialized hosting for foundation models (including DeepSeek-V4, Qwen 3.6 VL, Llama 4, Whisper, Stable Diffusion 3.5, and custom embedding models). Baseten integrates directly with Hugging Face and FastMCP 3.1 Task Protocol agents, enabling software engineers and AI system architects to spin up dedicated serverless endpoints via single-click provisioning, real-time telemetry streaming, and micro-second granular GPU billing.

The platform relies on **Truss**, an open-source model packaging framework created by Baseten, which standardizes model containerization, hardware resource specification, and runtime dependency management. By abstracting lower-level Kubernetes pod lifecycle management, NVIDIA CUDA kernel setup, and inference serving engines (such as vLLM, TensorRT-LLM, and TGI), Baseten allows organizations to turn raw model weights into enterprise-grade REST and gRPC endpoints capable of low-latency streaming and high concurrent throughput.

## What problem it solves
Deploying, scaling, and maintaining state-of-the-art open-weights AI models introduces significant operational complexity:
- **Kubernetes and GPU Cluster Overhead**: Building and maintaining Kubernetes clusters equipped with heterogeneous GPU hardware (NVIDIA H100, A100, L40S, L4) requires dedicated infrastructure engineering teams.
- **Cold Starts and Resource Utilization**: Bare-metal reservations cause idle GPU spending during off-peak hours, while standard container cold starts can take minutes due to multi-gigabyte weight downloads.
- **Inference Runtimes & Kernel Optimization**: Maximizing inference tokens per second (TPS) requires manual configuration of paged attention, FP8/AWQ quantization, and engine-level continuous batching.

Baseten resolves these bottlenecks by providing a serverless GPU infrastructure platform. Using Truss packaging, models bundle their code, dependencies, and engine configurations into standardized artifacts. Baseten's platform automatically manages model weight caching across edge NVMe drives, provisions GPU instances in under two seconds during cold starts, and scales workloads dynamically based on active request queues and latency targets.

## Where it fits in the stack
**AI Model Provider & Infrastructure Layer**. Baseten occupies the core inference serving layer in modern compound AI systems, positioned between model storage/registry services (Hugging Face Hub, AWS S3) and orchestration layers (FastMCP 3.1 server swarms, LangChain, LlamaIndex, or agent gateways).

```
+-----------------------------------------------------------------------+
|                 Orchestration & Agent Layer                           |
|    (FastMCP 3.1 Task Protocol / Claude Code / Custom Swarms)          |
+-----------------------------------------------------------------------+
                                   |
                                   v  (HTTPS / REST / gRPC / SSE)
+-----------------------------------------------------------------------+
|                      Baseten Platform Gateway                         |
|   (Authentication, Rate Limiting, Load Balancing, Telemetry Routing)  |
+-----------------------------------------------------------------------+
                                   |
            +----------------------+----------------------+
            |                                             |
            v                                             v
+-----------------------+                     +-----------------------+
|  Active GPU Worker    |                     |  Cold Worker Pool     |
| (vLLM / TensorRT-LLM) |                     |  (Warm NVMe Caching)  |
| - Continuous Batching |                     | - Rapid Weight Load   |
| - PagedAttention      |                     | - Sub-2s Provisioning |
+-----------------------+                     +-----------------------+
            ^                                             ^
            |                                             |
+-----------------------------------------------------------------------+
|                       Truss Model Package                             |
|       (Config, Python Dependencies, Model Artifacts, Hooks)           |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Serverless API Gateway for Agent Swarms**: Offloading high-frequency reasoning workloads, code generation tasks, and multi-step agent tool calls to auto-scaling Baseten endpoints.
- **Custom Quantized Foundation Model Serving**: Running fine-tuned Llama 4 70B, DeepSeek-V4, or Qwen 3.6 VL models quantized in FP8 or AWQ with custom C++ extensions.
- **Single-Click Hugging Face Model Provisioning**: Instantly deploying open-weight models from Hugging Face Hub directly onto Baseten infrastructure without writing boilerplate deployment manifests.
- **Hybrid Local-Cloud AI Workflows**: Prototype agent workflows locally using Ollama or vLLM, then seamlessly target Baseten endpoints for production traffic with zero code modifications.
- **High-Throughput Visual & Multimodal Inference**: Processing batch requests for document OCR, image analysis, and video understanding using dedicated multi-GPU instances.

## Architecture & Core Mechanics

### Architecture Diagram: Serverless GPU Scaling & Request Pipeline

```
[ Client / Agent Request ]
           |
           v
+-------------------------------------------------------------------+
|                     Baseten API Gateway                           |
|  - Token Bucket Rate Limiter                                      |
|  - TLS Termination & Request Router                               |
|  - Real-time Queue Depth Evaluator                                |
+-------------------------------------------------------------------+
           |
     +-----+----------------------------------+
     |                                        |
     v (Queue > 0 & Active Workers Available)  v (Queue > Threshold & Scale Needed)
+--------------------------+    +----------------------------------+
|  Active GPU Pod Array    |    |  Scale Decision Engine           |
|  +--------------------+  |    |  - Request Provisioner           |
|  | Worker 1 (NVIDIA)  |  |    |  - Pull Cached Weights from NVMe |
|  | - vLLM Engine      |  |    |  - Spin Up New GPU Instance      |
|  +--------------------+  |    +----------------------------------+
|  | Worker 2 (NVIDIA)  |  |                     |
|  | - TRT-LLM Engine   |  |                     v
|  +--------------------+  |    +----------------------------------+
+--------------------------+    | Newly Provisioned GPU Pod        |
             |                  +----------------------------------+
             +---------------------------+
                                         |
                                         v
                       [ Response Streamed back to Client ]
```

### Key Technical Subsystems

1. **Truss Model Packaging Standard**: Truss is Baseten's open-source framework (`truss` Python package) for packaging machine learning models. A Truss directory encapsulates:
   - `config.yaml`: Hardware selection (GPU type, VRAM requirements, CPU, memory), Python packages, system dependencies, secrets mapping, and runtime options.
   - `model/model.py`: Standardized `Model` class implementing `load()` (executed once during container initialization) and `predict()` (executed per inference call).
2. **Weight-Caching File System**: To combat multi-gigabyte download latencies during container cold starts, Baseten maintains a distributed, NVMe-backed weight cache across regional GPU clusters. Foundation model weights are cached at the host hardware layer, enabling sub-2-second startup times even for models exceeding 30GB in size.
3. **Advanced Inference Engines**:
   - **vLLM Integration**: Out-of-the-box support for vLLM featuring PagedAttention and continuous batching for maximum token throughput.
   - **TensorRT-LLM**: Ultra-low latency engine tailored for NVIDIA H100/A100 hardware, enabling tensor parallelism across multi-GPU setups.
   - **Custom C++ CUDA Runtimes**: Freedom to compile and expose raw C++ kernels directly inside Truss container layers.
4. **Auto-Scaling Metrics & SLA Management**: Auto-scaling can be driven by concurrency per replica, total request queue depth, or custom GPU utilization thresholds. Scale-down delays and minimum replica counts (including scale-to-zero) are configurable per environment.

## Strengths
- **Native Hugging Face Ecosystem Support**: Single-click deployment workflow integrated directly into Hugging Face Hub model pages.
- **Fast Cold-Start Technology**: NVMe weight pre-caching reduces startup latency by up to 90% compared to standard Docker container pulls.
- **Open-Source Packaging (Truss)**: Prevents vendor lock-in; Truss packages can be run locally, deployed to private Kubernetes clusters, or served on Baseten.
- **Fine-Grained Observability**: Real-time log streaming, GPU temperature/utilization metrics, token generation latency breakdown, and request tracing dashboard.
- **Enterprise Security & Compliance**: SOC 2 Type II certified, HIPAA compliant option, private VPC peering, and secret manager isolation.

## Limitations
- **Cloud Egress & Network Hops**: Public cloud deployment introduces network round-trip overhead compared to locally hosted or air-gapped homelab servers.
- **Compute Overhead Cost**: On-demand serverless pricing incurs a premium compared to reserved bare-metal instances when running 100% steady-state 24/7 workloads.
- **Custom Engine Learning Curve**: Optimizing complex Truss configurations for multi-GPU tensor parallelism requires familiarity with YAML specifications and CUDA memory limits.

## When to use it
- Hosting high-demand open-weights LLMs or vision models that require H100 or A100 GPUs without upfront capital expenditure.
- Building production FastMCP 3.1 or agent swarms with unpredictable, bursty request patterns requiring auto-scaling from 0 to N nodes.
- Serving custom fine-tuned model checkpoints generated from Axolotl, Unsloth, or Hugging Face SFT pipelines.

## When not to use it
- Strict offline, air-gapped environments where data cannot cross external network boundaries.
- Continuous, constant-load inference tasks where bare-metal fixed hardware provides lower long-term cost.
- Simple, low-parameter models (e.g. 1B to 3B models) that run comfortably on local CPU/GPU homelab hardware.

## Getting started

### 1. Account Setup & CLI Initialization
Sign up for a Baseten account and generate an API key from the platform console. Install the CLI and model packaging library:

```bash
pip install baseten truss
```

Authenticate your shell environment:

```bash
export BASETEN_API_KEY="bsa_your_actual_api_key_here"
baseten login --api-key "$BASETEN_API_KEY"
```

### 2. Initializing a Truss Package
Create a new model directory initialized with default files:

```bash
truss init my_baseten_model
cd my_baseten_model
```

Edit `config.yaml` to configure hardware requirements and model dependencies:

```yaml
model_metadata:
  example_model: true
model_name: Llama-4-FastMCP-Endpoint
python_version: py311
requirements:
  - torch>=2.5.0
  - vllm>=0.7.0
  - pydantic>=2.10.0
resources:
  accelerator: H100
  cpu: "8"
  memory: 32Gi
  use_gpu: true
runtime:
  predict_concurrency: 64
```

Edit `model/model.py` to define weight loading and prediction logic:

```python
import os
from typing import Dict, Any

class Model:
    def __init__(self, **kwargs):
        self._model = None

    def load(self):
        # Executed during initial container warm-up
        from vllm import LLM
        self._model = LLM(model="meta-llama/Llama-3.2-3B-Instruct")

    def predict(self, request: Dict[str, Any]) -> Dict[str, Any]:
        prompt = request.get("prompt", "")
        max_tokens = request.get("max_tokens", 256)

        from vllm import SamplingParams
        sampling_params = SamplingParams(max_tokens=max_tokens, temperature=0.7)
        outputs = self._model.generate([prompt], sampling_params)

        return {
            "text": outputs[0].outputs[0].text,
            "tokens_generated": len(outputs[0].outputs[0].token_ids)
        }
```

### 3. Deployment
Deploy the packaged model to Baseten:

```bash
truss deploy
```

## CLI examples

```bash
# Check status of deployed models on Baseten
baseten model list

# View real-time tail logs for a specific production deployment
baseten model logs --model-id "model_id_here" --follow

# Invoke a deployed endpoint using the Baseten CLI
baseten model predict --model-id "model_id_here" --data '{"prompt": "Summarize home automation standards."}'

# Direct API Query with cURL and SSE Streaming
curl -N -X POST "https://model-id.baseten.co/environments/production/predict" \
     -H "Authorization: Api-Key $BASETEN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Write a Python script for MQTT temperature monitoring.",
       "stream": true,
       "max_tokens": 512
     }'
```

## API examples

### 1. FastMCP 3.1 Server Integration with Baseten Endpoint

This script implements a production-grade FastMCP 3.1 server (`fastmcp` v0.4+) exposing a tool that interfaces with a Baseten model endpoint. It uses asynchronous HTTP execution and enforces Pydantic v2 data models.

```python
import os
import time
import httpx
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="Baseten Model Gateway",
    version="3.1.0",
    description="FastMCP server providing real-time access to auto-scaling Baseten inference endpoints."
)

# ------------------------------------------------------------------
# Pydantic v2 Models for Baseten Tool Communication
# ------------------------------------------------------------------

class BasetenInferenceRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=1, max_length=16000, description="Input prompt for inference.")
    max_tokens: int = Field(default=512, ge=1, le=4096, description="Maximum tokens to generate.")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature.")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Nucleus sampling probability.")
    stop_sequences: Optional[List[str]] = Field(default=None, description="Optional list of stop tokens.")


class BasetenInferenceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    model_id: str = Field(..., description="Target Baseten model identifier.")
    generated_text: str = Field(..., description="The complete text response generated by the model.")
    prompt_tokens: int = Field(..., ge=0, description="Number of tokens in input prompt.")
    completion_tokens: int = Field(..., ge=0, description="Number of tokens generated in completion.")
    latency_ms: float = Field(..., ge=0.0, description="End-to-end execution latency in milliseconds.")
    cold_start_detected: bool = Field(default=False, description="True if a cold start delay occurred.")


# ------------------------------------------------------------------
# FastMCP Tool Endpoint
# ------------------------------------------------------------------

@mcp.tool(
    name="baseten_llm_inference",
    description="Executes high-throughput text generation via an auto-scaling Baseten GPU model endpoint."
)
async def baseten_llm_inference(request: BasetenInferenceRequest) -> BasetenInferenceResponse:
    api_key = os.getenv("BASETEN_API_KEY")
    endpoint_url = os.getenv("BASETEN_ENDPOINT_URL", "https://model-sample.baseten.co/environments/production/predict")
    model_id = os.getenv("BASETEN_MODEL_ID", "baseten-llama-3-70b")

    if not api_key:
        raise ValueError("BASETEN_API_KEY environment variable is missing.")

    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": request.prompt,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "stop": request.stop_sequences or []
    }

    start_time = time.perf_counter()

    # Execute asynchronous request against Baseten REST API
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(endpoint_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Baseten API error ({exc.response.status_code}): {exc.response.text}") from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"Network error connecting to Baseten endpoint: {str(exc)}") from exc

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    # Extract response attributes (handling standard Truss format or simulated format)
    text_output = data.get("text") or data.get("generated_text") or ""
    prompt_tokens = data.get("prompt_tokens", len(request.prompt) // 4)
    completion_tokens = data.get("tokens_generated", len(text_output) // 4)
    cold_start = elapsed_ms > 3000.0  # Heuristic threshold for cold-start identification

    return BasetenInferenceResponse(
        model_id=model_id,
        generated_text=text_output,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        latency_ms=round(elapsed_ms, 2),
        cold_start_detected=cold_start
    )


if __name__ == "__main__":
    # Standard FastMCP entrypoint
    mcp.run()
```

### 2. Standalone Python Client with Pydantic v2 Schema Enforcement

This snippet demonstrates querying a Baseten deployment with error handling, latency measurement, and strict Pydantic v2 validation.

```python
import os
import requests
from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError

class BasetenPayload(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_tokens: int = Field(default=256, gt=0, le=2048)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class BasetenResult(BaseModel):
    text: str = Field(..., min_length=1)
    tokens_generated: int = Field(..., ge=0)
    model_version: str = Field(default="v1.0.0")

def execute_baseten_query(payload: BasetenPayload) -> BasetenResult:
    api_key = os.getenv("BASETEN_API_KEY", "bsa_sample_token")
    endpoint = os.getenv("BASETEN_ENDPOINT", "https://model-id.baseten.co/environments/production/predict")

    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        endpoint,
        headers=headers,
        json=payload.model_dump(),
        timeout=30
    )

    if response.status_code == 200:
        raw_json = response.json()
        try:
            return BasetenResult(**raw_json)
        except ValidationError as val_err:
            raise ValueError(f"Schema validation failed on response: {val_err}")
    else:
        raise ConnectionError(f"Request failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    # Test execution with dummy parameters
    test_payload = BasetenPayload(
        prompt="Analyze energy efficiency patterns in smart home HVAC systems.",
        max_tokens=150
    )
    print("Sending payload to Baseten endpoint...")
    # Simulated execution block for documentation verification
    simulated_response = BasetenResult(
        text="Smart HVAC systems optimize energy consumption by integrating occupancy sensors and predictive weather data.",
        tokens_generated=22,
        model_version="production-truss-v0.9.2"
    )
    print(f"Validated Output: {simulated_response.text}")
    print(f"Tokens Generated: {simulated_response.tokens_generated}")
```

## Advanced Production Features & Operational Performance

### Hardware Selection Matrix
Baseten provides access to various GPU architectures tailored to specific model topologies:

| GPU Type | VRAM | Interconnect | Ideal Workloads |
| :--- | :--- | :--- | :--- |
| **NVIDIA H100** | 80GB SXM5 | NVLink (900 GB/s) | 70B+ Parameter LLMs, DeepSeek-V4 MoE, High-Batch vLLM |
| **NVIDIA A100** | 80GB PCIe | NVLink (600 GB/s) | Medium-to-Large LLMs (8B to 34B), Batch Embedding Generation |
| **NVIDIA L40S** | 48GB PCIe | PCIe Gen5 | Vision Transformers, Stable Diffusion 3.5, Multimodal Analysis |
| **NVIDIA L4** | 24GB PCIe | PCIe Gen4 | Small LLMs (1B to 8B), Real-Time Audio (Whisper), Edge Workloads |

### Production Monitoring & Observability
Baseten exports Prometheus metrics and OpenTelemetry traces for every deployment:
- `baseten_request_count_total`: Total request volume partitioned by HTTP status code.
- `baseten_request_duration_seconds`: Histogram of total request duration including engine pre-fill and decode phases.
- `baseten_gpu_memory_utilization_ratio`: VRAM memory pressure tracking.
- `baseten_time_to_first_token_seconds`: Measurement of TTFT for streaming endpoints.

## Related tools / concepts
- [vLLM](../infrastructure/vllm.md) — The continuous-batching LLM engine leveraged by Baseten for optimized inference.
- [OpenRouter](../ai_knowledge/openrouter.md) — Universal model routing layer offering failover and multi-provider pricing aggregator.
- [DeepSeek](../providers/deepseek.md) — High-performance open reasoning models frequently hosted on Baseten infrastructure.
- [Ollama](../../services/ollama.md) — Local inference engine; ideal for homelab prototyping before deploying to Baseten.
- [Fireworks](../providers/fireworks.md) — Alternative low-latency serverless model hosting provider.
- [Replicate](../providers/replicate.md) — Cloud runtime platform for open-source AI models and developer APIs.

## Sources / references
- [Baseten Official Documentation Portal](https://docs.baseten.co/)
- [Truss Open Source Model Packaging Repository](https://github.com/basetenlabs/truss)
- [Hugging Face Blog: Single-Click Deployments on Baseten](https://huggingface.co/blog/baseten)
- [FastMCP 3.1 Task Protocol Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
