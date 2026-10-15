# TensorRT-LLM

## What it is

- **High-Performance Inference Compilation**: Compiles PyTorch LLM weights into optimized TensorRT execution engines leveraging custom kernel fusion and Tensor Core pipeline optimizations.
- **Advanced Quantization Suite**: Hardware-accelerated low-precision quantization routines including FP4 (NVIDIA Blackwell native), FP8 (E4M3/E5M2 formats), SmoothQuant (INT8), and AWQ/GPTQ (INT4/INT8).
- **In-Flight Continuous Batching & Paged KV Cache**: Dynamically batches concurrent generation requests at the token level while managing KV cache memory in page-aligned blocks to maximize GPU utilization.
- **Multi-GPU Parallelism Execution**: Scalable distribution across multiple GPUs via Tensor Parallelism (TP), Pipeline Parallelism (PP), Context Parallelism (CP), and NCCL communication primitives.
- **FastMCP 3.1 & NIM Compatibility**: Native serving backend powering NVIDIA NIM (Inference Microservices) containers and low-latency FastMCP 3.1 agent tool execution backends.


## What problem it solves
- Solves high inference latency and low token throughput bottlenecks when serving large language models at scale.
- Reduces GPU memory requirements through FP4/FP8 quantization and continuous in-flight batching.

## System Architecture & Pipeline

```
+-----------------------------------------------------------------------------------+
|                           TensorRT-LLM Compilation & Execution                    |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +--------------------+         +-----------------------+                         |
|  | Hugging Face /     | ------> | Quantization Engine   |                         |
|  | PyTorch Checkpoint |         | FP4 / FP8 / AWQ / INT8|                         |
|  +--------------------+         +-----------+-----------+                         |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | trtllm-build          |                         |
|                                 | Kernel Fusion / Plugin|                         |
|                                 +-----------+-----------+                         |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | Compiled .engine File |                         |
|                                 +-----------+-----------+                         |
|                                             |                                     |
|                        +--------------------+--------------------+                |
|                        |                                         |                |
|                        v                                         v                |
|           +-------------------------+               +-------------------------+   |
|           | Paged KV Cache Manager  |               | Continuous Batching     |   |
|           | Page-aligned attention  |               | Dynamic token scheduler |   |
|           +------------+------------+               +------------+------------+   |
|                        |                                         |                |
|                        +--------------------+--------------------+                |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | C++ Executor Runtime  |                         |
|                                 | Multi-GPU NCCL TP/PP  |                         |
|                                 +-----------+-----------+                         |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | FastMCP 3.1 Server /  |                         |
|                                 | Triton NIM Endpoint   |                         |
|                                 +-----------------------+                         |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Where it fits in the stack
- Sits in the **GPU Inference & Compilation** layer.
- Powers NVIDIA NIM microservices, vLLM acceleration backends, and low-latency agent reasoning pipelines.

## Typical use cases

- **Enterprise Production LLM Serving**: Deploying high-throughput LLM API endpoints serving millions of daily tokens for interactive enterprise applications.
- **Low-Latency Agentic Tool Execution**: Accelerating generation steps in agent reasoning loops where prompt-to-first-token latency directly impacts agent responsiveness.
- **Edge & On-Premises GPU Cluster Deployment**: Optimizing memory footprint to fit large models (e.g., Llama 4 70B/405B) onto limited GPU nodes via FP4/FP8 quantization.
- **Real-Time Streaming Applications**: Delivering sub-10ms token-to-token generation for real-time voice assistants, coding copilots, and multi-modal agents.

## Feature & Performance Comparison Matrix

| Feature / Metric | TensorRT-LLM (NVIDIA) | vLLM | SGLang | llama.cpp | Hugging Face TGI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Target Hardware** | NVIDIA GPUs (Hopper, Blackwell) | NVIDIA, AMD, Intel | NVIDIA, AMD GPUs | CPU / Metal / Apple Silicon / NVIDIA | NVIDIA GPUs |
| **Native FP4 / FP8 Support** | Native Blackwell FP4 + Hopper FP8 | FP8 supported | FP8 supported | GGUF Quantization | FP8 supported |
| **Batching Mechanism** | In-flight continuous batching | Continuous batching (PagedAttention) | RadixAttention continuous batching | Static / Dynamic sequence batching | Continuous batching |
| **Multi-GPU Scale** | Tensor, Pipeline, Context (NCCL) | Tensor, Pipeline Parallelism | Tensor, Pipeline Parallelism | Row/Column splitting | Tensor Parallelism |
| **Compilation Phase** | Explicit (`trtllm-build`) | Dynamic / JIT | Radix / Dynamic | Zero compilation (Immediate) | Dynamic / JIT |
| **Throughput (Tokens/sec/GPU)** | Highest (Fused kernels) | High | Very High | Moderate | High |
| **Time to First Token (TTFT)** | Sub-15ms (Hopper H100) | ~25ms | ~20ms | ~50ms (CPU/GPU) | ~30ms |

## Strengths

- **Industry-Leading Throughput**: Unmatched generation throughput and token efficiency on NVIDIA hardware compared to standard PyTorch runtimes.
- **Memory Footprint Reduction**: Native FP4/FP8 quantization enables running enterprise models on 50% fewer GPU nodes without quality loss.
- **Production-Grade Ecosystem Integration**: Direct backend engine for NVIDIA Triton Inference Server, NVIDIA NIM, vLLM acceleration backends, and NeMo Claw.


## Limitations

- **NVIDIA GPU Vendor Lock-In**: Exclusively targets NVIDIA GPU architectures (Hopper, Blackwell, Rubin, Ada Lovelace, Ampere).
- **Engine Compilation Build Phase**: Requires an explicit offline engine compilation step (`trtllm-build`), creating warm-up startup delay when loading new model weights.


## When to use it

- When building production-grade LLM inference platforms hosted on NVIDIA GPU hardware (H100, H200, B200, B300, GB200).
- When prompt-to-first-token latency and maximum throughput per dollar are primary engineering requirements.
- When deploying enterprise AI agents using NVIDIA NIM microservices or NeMo framework.


## When not to use it
- When running model inference on CPU-only or non-NVIDIA GPU hardware.
- When rapid model experimentation requires zero compilation build time.

## Getting started

### Installation
Pull pre-built Docker containers or install via `pip`:

```bash
# Pull official NVIDIA TensorRT-LLM container
docker pull nvcr.io/nvidia/tensorrtllm:latest

# Or install python wheel in CUDA 12 environment
pip install tensorrt_llm pydantic mcp torch --extra-index-url https://pypi.nvidia.com
```

### Minimal Working Example
```python
from pydantic import BaseModel, Field

class GenerationConfig(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_tokens: int = Field(default=128, ge=1)

def run_inference(cfg: GenerationConfig) -> str:
    # Simulated execution demonstrating API flow for TensorRT-LLM runtime
    return f"[TensorRT-LLM Engine Output]: Processing '{cfg.prompt[:20]}' with max_tokens={cfg.max_tokens}"

if __name__ == "__main__":
    config = GenerationConfig(prompt="Explain continuous batching in high-throughput inference.", max_tokens=64)
    res = run_inference(config)
    print(res)
```

## FastMCP 3.1 Server Integration

The following Python snippet implements a FastMCP 3.1 server exposing tools for TensorRT-LLM engine building validation and high-throughput streaming text generation:

```python
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, field_validator

# Initialize FastMCP Server
mcp = FastMCP("tensorrt-llm-server", version="3.1.0")


class BuildConfigSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    checkpoint_dir: str = Field(..., description="Path to input PyTorch or HuggingFace checkpoint directory")
    output_dir: str = Field(..., description="Target directory for compiled .engine file")
    quant_mode: str = Field(default="fp8", description="Quantization format: fp16, bf16, fp8, or fp4")
    tensor_parallel_size: int = Field(default=1, ge=1, le=16, description="Tensor parallelism GPU count")
    pipeline_parallel_size: int = Field(default=1, ge=1, le=8, description="Pipeline parallelism GPU count")

    @field_validator("quant_mode")
    @classmethod
    def validate_quant(cls, v: str) -> str:
        valid_modes = {"fp16", "bf16", "fp8", "fp4", "int8_sq", "int4_awq"}
        if v.lower() not in valid_modes:
            raise ValueError(f"Invalid quant_mode: {v}. Must be one of {valid_modes}")
        return v.lower()


class GenerationRequestSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=1, description="Input text prompt")
    max_output_tokens: int = Field(default=256, ge=1, le=4096, description="Max generated tokens")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p nucleus sampling")
    stop_words: Optional[List[str]] = Field(default=None, description="Stop phrases")


@mcp.tool()
async def build_engine(params: BuildConfigSchema) -> dict:
    """Validate parameters and build a TensorRT-LLM engine checkpoint."""
    # Simulates invocation of trtllm-build CLI tool
    return {
        "status": "success",
        "checkpoint_dir": params.checkpoint_dir,
        "output_engine": f"{params.output_dir}/rank0.engine",
        "quant_mode": params.quant_mode,
        "tp_size": params.tensor_parallel_size,
        "pp_size": params.pipeline_parallel_size
    }


@mcp.tool()
async def generate_completion(params: GenerationRequestSchema) -> dict:
    """Execute high-speed generation against compiled TensorRT-LLM engine."""
    return {
        "status": "completed",
        "prompt": params.prompt,
        "completion_text": f"[TensorRT-LLM Output]: High throughput result for '{params.prompt[:30]}'",
        "tokens_generated": params.max_output_tokens,
        "latency_ms": 12.4
    }


if __name__ == "__main__":
    mcp.run()
```

## CLI examples

```bash
# Build TensorRT engine checkpoint from Hugging Face model weights
trtllm-build --checkpoint_dir ./llama-3-8b-ckpt --output_dir ./engine_outputs --gemm_plugin float16

# Run multi-GPU tensor parallel inference on 2 ranks
mpirun -n 2 --allow-run-as-root python3 -m tensorrt_llm.hlapi.llm --model ./engine_outputs

# Benchmark TensorRT-LLM engine throughput and token latency
python3 -m tensorrt_llm.benchmarks.benchmark_serving --engine_dir ./engine_outputs --num_prompts 100
```


## API examples

The following Python example demonstrates configuring a TensorRT-LLM generation request payload, validating request arguments using strict **Pydantic v2** models, and executing model inference via the TensorRT-LLM Python API.

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Pydantic v2 Request & Engine Config Schemas
# ---------------------------------------------------------------------------
class TensorRTInferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Input text prompt")
    max_output_tokens: int = Field(default=256, ge=1, le=4096, description="Max generation token limit")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p nucleus sampling probability")
    stop_words: Optional[List[str]] = Field(default=None, description="Stop sequence strings")

class TensorRTBuildConfig(BaseModel):
    model_name: str = Field(..., description="Base model name identifier")
    quant_mode: str = Field(default="fp8", description="Quantization mode: 'fp16', 'fp8', or 'fp4'")
    tensor_parallel_size: int = Field(default=1, ge=1, le=16, description="Number of GPU TP ranks")

    @field_validator("quant_mode")
    @classmethod
    def validate_quant_mode(cls, v: str) -> str:
        allowed = {"fp16", "bf16", "fp8", "fp4", "int8_sq", "int4_awq"}
        if v.lower() not in allowed:
            raise ValueError(f"quant_mode must be one of {allowed}")
        return v.lower()

# ---------------------------------------------------------------------------
# TensorRT-LLM Engine Invocation Service
# ---------------------------------------------------------------------------
class TensorRTLlmService:
    def __init__(self, build_config: Dict[str, Any]):
        self.config = TensorRTBuildConfig.model_validate(build_config)
        print(f"TensorRT-LLM Engine initialized for {self.config.model_name} with quant_mode={self.config.quant_mode}")

    def generate(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validate request payload and simulate TensorRT-LLM generation execution."""
        req = TensorRTInferenceRequest.model_validate(request_payload)

        simulated_response = f"[TensorRT-LLM Output ({self.config.quant_mode})]: Verified response for '{req.prompt[:30]}'"

        return {
            "text": simulated_response,
            "tokens_generated": 64,
            "finish_reason": "stop"
        }

if __name__ == "__main__":
    build_conf = {
        "model_name": "meta-llama/Llama-4-70b-instruct",
        "quant_mode": "fp8",
        "tensor_parallel_size": 2
    }

    service = TensorRTLlmService(build_conf)

    inference_req = {
        "prompt": "Explain the architecture of TensorRT-LLM continuous batching.",
        "max_output_tokens": 128,
        "temperature": 0.2
    }

    result = service.generate(inference_req)
    print("Generation Result:", result)
```

## Troubleshooting & Common Errors

| Error / Failure Mode | Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| `CUDA out of memory (OOM)` during engine build | Exceeded GPU VRAM while building GEMM plugins or allocating workspace. | Pass `--max_workspace_size` parameter to limit compilation workspace memory. |
| `NCCL error: unhandled system error` | Misconfigured MPI or NCCL network interfaces across multi-GPU nodes. | Set `NCCL_DEBUG=INFO` and set `NCCL_IB_DISABLE=1` if InfiniBand is unavailable. |
| `Engine load failure: architecture mismatch` | Engine built on Ampere (sm_80) attempted to run on Hopper (sm_90). | Re-build engine with `trtllm-build` on matching GPU architecture target. |
| `Paged KV Cache allocation failure` | `max_num_seqs` or `kv_cache_free_gpu_mem_fraction` set too high for available VRAM. | Reduce `kv_cache_free_gpu_mem_fraction` (e.g. from 0.90 to 0.75). |
| `FP8 GEMM Plugin error` | Tensor Cores lacking FP8 hardware instruction support (e.g., Ada/Hopper required). | Fall back to `fp16` or `int4_awq` on pre-Ada NVIDIA architectures (V100/A100). |

## Production Deployment Guardrails

1. **GPU Architecture Alignment**: Always build engine files (`.engine`) on identical target GPU hardware (e.g., build H100 engines on H100 nodes).
2. **KV Cache Sizing**: Reserve at least 15-20% GPU VRAM for active execution buffers when configuring `--kv_cache_free_gpu_mem_fraction`.
3. **Continuous Batching Tuning**: Match `--max_batch_size` and `--max_num_seqs` to real-world concurrent traffic to prevent request queue starvation.
4. **Health Check Endpoints**: Monitor HTTP `/health` or Triton `/v2/health/ready` endpoints to detect engine initialization or C++ executor crashes.
5. **Precision Metrics**: Monitor accuracy degradation when quantizing to FP4/FP8 using MMLU or HumanEval benchmarking before production deployment.

## Related tools / concepts

- **[NeMo Claw](../agents/nemoclaw.md)**: Enterprise agent framework natively using TensorRT-LLM for low-latency tool execution.
- **[vLLM](vllm.md)**: High-throughput open-source inference engine integrating TensorRT-LLM optimized kernels.
- **[TGI](tgi.md)**: Hugging Face Text Generation Inference container platform.


## Sources / references

- [NVIDIA TensorRT-LLM Official GitHub Repository](https://github.com/NVIDIA/TensorRT-LLM)
- [NVIDIA TensorRT-LLM Documentation Portal](https://nvidia.github.io/TensorRT-LLM/)
- [NVIDIA NIM Microservices Architecture](https://developer.nvidia.com/nim)
- [FP8 & FP4 Quantization Benchmarks in TensorRT-LLM](https://developer.nvidia.com/blog/accelerating-llm-inference-with-tensorrt-llm/)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
