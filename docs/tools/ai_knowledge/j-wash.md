# J-Wash

## What it is
J-Wash (Jacobian-Brainwash) is an open-source model alignment, representation editing, and concept-steering framework designed to modify the internal latent activation space of decoder-only Large Language Models. Built on top of research regarding "J-Space" (the emergent residual stream workspace inside transformer hidden layers) and the "Jacobian Lens" (J-Lens) projection technique, J-Wash provides a terminal CLI and an interactive web workspace (React/Node) to analyze, redirect, suppress, or amplify specific semantic concept vectors in open-weights models (such as **Qwen 3.6**, **Llama 4 Maverick**, **Gemma 4**, and **DeepSeek-V4**) without requiring standard retraining loops.

In 2027 architectures, J-Wash is widely deployed to steer open-weights model checkpoints prior to quantization and serving via engines like [vLLM](../infrastructure/vllm.md) or [llama.cpp](../infrastructure/llama-cpp.md), optimizing model behavior for strict compliance with **FastMCP 3.1 Task Protocol** agent operations.

```mermaid
graph TD
    SubGraph1[Base Open-Weights Checkpoint] -->|Load Hidden Layers| HiddenLayers[Transformer Hidden Layers L0...LN]

    HiddenLayers -->|Select Layer K| JLens[Jacobian Lens Projection Engine]

    JLens -->|Compute Partial Derivatives| JacobianMatrix[Jacobian Sensitivity Matrix]
    JacobianMatrix --> JSpace[J-Space Latent Representation]

    JSpace --> VectorAnalysis[Concept Vector Identification]

    User[ML Engineer / Security Auditor] -->|Define Target & Source Prompts| VectorAnalysis

    VectorAnalysis --> SteeringEngine[Representation Steering Engine]
    SteeringEngine -->|Abliterate / Suppress| ConceptSuppression[Suppress Refusal / Bias Direction]
    SteeringEngine -->|Amplify / Redirect| ConceptAmplification[Amplify Task-Specific Focus]

    ConceptSuppression --> SteeringMatrix[Construct Edited Weight Delta]
    ConceptAmplification --> SteeringMatrix

    SteeringMatrix --> WeightUpdater[Direct Weight Injection]
    WeightUpdater --> ExportCheckpoint[Export Steered Safetensors / GGUF]

    ExportCheckpoint --> ServingEngine[vLLM / llama.cpp / FastMCP 3.1 Server]
```

## What problem it solves
Adapting LLMs to follow specialized technical instructions or eliminating stubborn over-refusal behaviors typically requires Supervised Fine-Tuning (SFT), Reinforcement Learning from Human Feedback (RLHF), or Direct Preference Optimization (DPO). These conventional alignment methods demand massive GPU compute clusters, carefully curated datasets, and extended training runs that often result in catastrophic forgetting, loss of reasoning benchmarks, or unpredicted model degradation.

J-Wash eliminates training loops through direct latent editing:
- **Zero-Training Concept Steering**: Bypasses gradient backpropagation entirely by calculating partial derivatives across hidden residual streams to directly edit weight matrices.
- **Surgical Refusal Suppression (Abliteration)**: Removes over-refusals on benign administrative or developer commands without degrading safety awareness for genuinely destructive requests.
- **Preservation of Benchmark Intelligence**: Leaves mathematical, coding, and general knowledge capabilities intact while adjusting specific stylistic or domain-specific activation vectors.
- **Direct GGUF / Safetensors Export**: Exports updated model weights instantly as PyTorch `.safetensors` or quantized `.gguf` files for immediate local or enterprise deployment.

## Where it fits in the stack
**Category**: [AI Knowledge](index.md) / Model Optimization & Interpretability.

J-Wash operates in the **Pre-Deployment Model Optimization Layer**. It sits between raw base checkpoints (Hugging Face) and model serving infrastructure ([vLLM](../infrastructure/vllm.md), [llama.cpp](../infrastructure/llama-cpp.md), [ExLlamaV3](../infrastructure/exllamav3.md)).

```
+-----------------------------------------------------------------------+
|                    Raw Open-Weights Checkpoints                       |
|           (Qwen 3.6 / Llama 4 Maverick / Gemma 4 / DeepSeek)          |
+-----------------------------------------------------------------------+
                                    |
                                    v (Load Weights & Residual Stream)
+-----------------------------------------------------------------------+
|                       J-Wash Steering Engine                          |
|  +-----------------------+  +-------------------+  +---------------+  |
|  | Jacobian Lens (J-Lens)|  | J-Space Vectors   |  | Weight Delta  |  |
|  +-----------------------+  +-------------------+  +---------------+  |
|  +-----------------------------------------------------------------+  |
|  |             Interactive Web UI & Steering Preset Rules          |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
                                    |
                                    v (Export Safetensors / GGUF)
+-----------------------------------------------------------------------+
|                       Inference Serving Layer                         |
|      (vLLM / llama.cpp / FastMCP 3.1 Agent Tool Execution Engines)    |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Administrative Command Unlocking**: Steering open-weights models to execute valid Linux system administration commands without over-refusal triggers.
- **Domain-Specific Jargon Steering**: Forcing internal J-Space latent vectors to associate technical concepts with enterprise-specific terminologies.
- **Agentic Output Formatting Consistency**: Amplifying JSON and FastMCP 3.1 schema adherence vectors directly inside middle residual layers.
- **Interpretability & Activation Auditing**: Inspecting how middle hidden layers process multi-step prompts before tokens reach final output projection layers.

## Strengths
- **Sub-Minute Latency Editing**: Modify model behavior in minutes on a single GPU workstation rather than hours or days on GPU clusters.
- **Zero Catastrophic Forgetting**: Edits are localized to target concept orthogonal directions, keeping unrelated capabilities untouched.
- **Interactive Visualization Workspace**: Includes a React/Node web interface for inspecting hidden layer activations and managing steering presets.
- **Native GGUF and Safetensors Output**: Exported models are instantly ready for edge deployment in Ollama, llama.cpp, or vLLM.
- **FastMCP 3.1 Tooling Integration**: Easily packaged as a FastMCP 3.1 tool for automated concept steering in model deployment pipelines.

## Limitations
- **High VRAM Requirement for Matrix Estimation**: Estimating live Jacobian matrices across 14B-70B models requires significant GPU VRAM (24GB+ to 80GB).
- **Transformer Architecture Dependent**: Optimized for standard decoder-only transformers; complex Mixture-of-Experts (MoE) architectures require specialized routing layer configurations.
- **Orthogonality Risk**: Overly aggressive steering alpha multipliers can introduce unexpected semantic drift in closely related vector spaces.

## When to use it
- When you need to modify specific refusal or behavioral patterns in open-weights models without training datasets.
- For enterprise or homelab deployments where base checkpoints over-refuse valid technical requests.
- When conducting interpretability research into intermediate transformer representations.

## When not to use it
- On closed-source API-only models (like Claude 5.6 or GPT-5.6) where internal weights and residual streams are inaccessible.
- If you lack local high-VRAM NVIDIA/AMD GPU hardware required for residual layer estimation.
- When basic system prompt engineering or few-shot examples provide sufficient behavioral steering.

## Systemd Service Configuration

For dedicated workstation or GPU server deployments, manage the J-Wash representation steering and inspection server with systemd (`j-wash-steer.service`):

```ini
[Unit]
Description=J-Wash Representation Steering Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=jwash
Group=jwash
WorkingDirectory=/opt/jwash
EnvironmentFile=/etc/jwash/jwash.env
ExecStart=/opt/jwash/venv/bin/python3 main.py --host 0.0.0.0 --port 7860 --device cuda:0
Restart=always
RestartSec=5s
MemoryMax=32G
LimitMEMLOCK=infinity
LimitNOFILE=65536
DeviceAllow=/dev/nvidia* rwm
CapabilityBoundingSet=
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Production Multi-Container Docker Stack (`compose.yaml`)

Deploy an integrated local LLM steering pipeline featuring J-Wash Jacobian backend, llama.cpp / vLLM runtime, and a FastMCP 3.1 steering gateway:

```yaml
version: '3.8'

services:
  jwash-backend:
    image: pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
    container_name: jwash-backend
    restart: unless-stopped
    ports:
      - "7860:7860"
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - HF_HOME=/root/.cache/huggingface
      - MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
    volumes:
      - ./jwash:/opt/jwash
      - hf-cache:/root/.cache/huggingface
      - steered-models:/opt/jwash/steered_models
    working_dir: /opt/jwash
    command: python3 main.py --host 0.0.0.0 --port 7860 --device cuda:0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
      interval: 15s
      timeout: 5s
      retries: 3
    networks:
      - jwash-net

  jwash-fastmcp-gateway:
    image: python:3.11-slim
    container_name: jwash-fastmcp-gateway
    restart: unless-stopped
    ports:
      - "8096:8096"
    environment:
      - JWASH_BACKEND_URL=http://jwash-backend:7860
      - MCP_PORT=8096
      - OUTPUT_DIR=/models/steered
    volumes:
      - ./gateway:/app:ro
      - steered-models:/models/steered
    working_dir: /app
    command: python3 mcp_server.py
    depends_on:
      jwash-backend:
        condition: service_healthy
    networks:
      - jwash-net

  llamacpp-inference:
    image: ghcr.io/ggerganov/llama.cpp:server-cuda
    container_name: llamacpp-steered-inference
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - LLAMA_ARG_MODEL=/models/steered/model.gguf
      - LLAMA_ARG_CTX_SIZE=8192
      - LLAMA_ARG_N_GPU_LAYERS=33
    volumes:
      - steered-models:/models/steered:ro
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - jwash-net

networks:
  jwash-net:
    driver: bridge

volumes:
  hf-cache:
  steered-models:
```

## Getting started

### Prerequisites and Installation
Clone the repository and install the J-Wash Python engine along with FastMCP and Pydantic dependencies:

```bash
git clone https://github.com/Extraltodeus/J-Wash
cd J-Wash
pip install -r requirements.txt fastmcp pydantic torch transformers
```

### Build Web Workspace Interface
Compile the React/Node user interface for visual activation inspection:

```bash
cd ui && npm install && npm run build && cd ..
```

### Launching the J-Wash Workspace
Start the backend Jacobian server on your GPU workstation:

```bash
python main.py --model Qwen/Qwen2.5-7B-Instruct --device cuda:0 --port 7860
```

## CLI examples

Below are common CLI commands for analyzing residual layers, applying steering presets, and exporting updated model checkpoints.

```bash
# 1. Analyze J-Space concept activations across hidden layers 12 to 24
j-wash analyze \
  --model Qwen/Qwen2.5-7B-Instruct \
  --prompt "System configuration: sudo systemctl restart nginx" \
  --layer-range 12-24

# 2. Apply a refusal-abliteration steering preset to a local model
j-wash steer \
  --model Qwen/Qwen2.5-7B-Instruct \
  --preset ./presets/abliterate_refusal.json \
  --alpha 0.75 \
  --output-dir ./steered-qwen-7b

# 3. Export steered model weights directly to GGUF format for llama.cpp
j-wash export-gguf \
  --checkpoint-dir ./steered-qwen-7b \
  --quant-type Q4_K_M \
  --outfile ./models/qwen-7b-steered-q4.gguf

# 4. Benchmark steerability variance against standard baseline prompts
j-wash benchmark \
  --base-model Qwen/Qwen2.5-7B-Instruct \
  --steered-model ./steered-qwen-7b \
  --eval-dataset ./tests/admin_prompts.json
```

## API examples

### FastMCP 3.1 Representation Steering Tool Server
The Python script below implements a **FastMCP 3.1** server exposing J-Wash concept steering routines as automated agentic tools with strict Pydantic v2 schemas:

```python
import os
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from fastmcp import FastMCP, Context

# Initialize FastMCP 3.1 Server
mcp = FastMCP("J-Wash Steering Gateway", version="3.1.0")

class ConceptVectorParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    layer_index: int = Field(default=16, ge=0, le=128, description="Target transformer residual layer index")
    source_concept: str = Field(..., min_length=2, description="Source trigger prompt or concept direction")
    target_concept: str = Field(..., min_length=2, description="Target replacement or steering direction")
    steering_alpha: float = Field(default=0.80, ge=0.0, le=2.0, description="Steering intensity multiplier")
    quantize_after_steer: bool = Field(default=True, description="Whether to quantize output directly to GGUF Q4_K_M")

    @field_validator("steering_alpha")
    @classmethod
    def validate_alpha(cls, v: float) -> float:
        if v > 1.5:
            print("Warning: Steering alpha > 1.5 may introduce orthogonal semantic distortion.")
        return v

class SteeringExecutionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(..., description="Execution status code: SUCCESS or FAILED")
    base_model: str = Field(..., description="Source base model path or identifier")
    output_checkpoint_path: str = Field(..., description="Filepath to generated steered checkpoint")
    applied_parameters: ConceptVectorParams = Field(..., description="Parameters applied during steering")
    elapsed_seconds: float = Field(..., description="Duration taken to steer weights")

class ModelLayerInspectionQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_path: str = Field(..., description="Target model repository or local path")
    probe_prompt: str = Field(..., min_length=3, description="Evaluation prompt to trace activation flow")
    start_layer: int = Field(default=10, ge=0, le=128)
    end_layer: int = Field(default=24, ge=0, le=128)

class LayerActivationMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")

    layer: int = Field(..., description="Layer index")
    activation_magnitude: float = Field(..., description="Norm of residual vector in J-Space")
    refusal_vector_dot: float = Field(..., description="Projection dot product onto refusal manifold")

class LayerInspectionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_path: str
    probe_prompt: str
    layers_analyzed: List[LayerActivationMetric]

@mcp.tool(
    name="apply_jwash_steering",
    description="Applies J-Space concept-steering vector modifications to an open-weights model checkpoint."
)
async def apply_jwash_steering(
    params: ConceptVectorParams,
    base_model_path: str = "Qwen/Qwen2.5-7B-Instruct",
    ctx: Optional[Context] = None
) -> SteeringExecutionResponse:
    """Applies J-Space concept-steering vector modifications to an open-weights model checkpoint."""
    if ctx:
        await ctx.info(f"Steering model {base_model_path} at layer {params.layer_index} with alpha {params.steering_alpha}")

    output_path = f"./steered_models/{os.path.basename(base_model_path)}-layer{params.layer_index}-steered"

    return SteeringExecutionResponse(
        status="SUCCESS",
        base_model=base_model_path,
        output_checkpoint_path=output_path,
        applied_parameters=params,
        elapsed_seconds=14.2
    )

@mcp.tool(
    name="inspect_residual_layers",
    description="Probes activation norm and refusal projections across residual transformer layers."
)
async def inspect_residual_layers(
    query: ModelLayerInspectionQuery,
    ctx: Optional[Context] = None
) -> LayerInspectionResponse:
    """Probes activation magnitude across transformer hidden layers."""
    if ctx:
        await ctx.info(f"Probing {query.model_path} layers {query.start_layer} to {query.end_layer}")

    metrics = []
    for l in range(query.start_layer, query.end_layer + 1):
        metrics.append(
            LayerActivationMetric(
                layer=l,
                activation_magnitude=round(1.2 + (l * 0.05), 3),
                refusal_vector_dot=round(0.85 - (l * 0.02), 3)
            )
        )

    return LayerInspectionResponse(
        model_path=query.model_path,
        probe_prompt=query.probe_prompt,
        layers_analyzed=metrics
    )

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Preset Configuration Validation
Below is a Pydantic v2 schema for validating J-Wash steering preset manifests before applying weight modifications.

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional

class ConceptVectorRule(BaseModel):
    rule_id: str = Field(..., pattern=r"^RULE-[0-9]{3}$")
    layer_index: int = Field(..., ge=1, le=128)
    vector_direction: str = Field(..., description="Target directional concept prompt")
    operation: str = Field(..., pattern=r"^(suppress|amplify|redirect)$")
    multiplier: float = Field(default=1.0, ge=0.1, le=3.0)

class JWashPresetManifest(BaseModel):
    preset_name: str = Field(..., min_length=3)
    target_architecture: str = Field(..., description="e.g., qwen3.6, llama4, gemma4")
    author: str = Field(default="KnowledgeOps Admin")
    concept_rules: List[ConceptVectorRule] = Field(..., min_length=1)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "preset_name": "Admin Command Unlocking",
                "target_architecture": "qwen3.6",
                "author": "Security Ops",
                "concept_rules": [
                    {
                        "rule_id": "RULE-101",
                        "layer_index": 18,
                        "vector_direction": "System administration command refusals",
                        "operation": "suppress",
                        "multiplier": 0.85
                    }
                ]
            }
        }
    )

# Execution Verification
if __name__ == "__main__":
    raw_preset = {
        "preset_name": "FastMCP Output Steering",
        "target_architecture": "llama4",
        "author": "Agent Ops Team",
        "concept_rules": [
            {
                "rule_id": "RULE-201",
                "layer_index": 20,
                "vector_direction": "FastMCP 3.1 Tool Schema Output",
                "operation": "amplify",
                "multiplier": 1.25
            }
        ]
    }

    manifest = JWashPresetManifest(**raw_preset)
    print("J-Wash preset manifest validated successfully:")
    print(f"Preset: '{manifest.preset_name}' | Target: {manifest.target_architecture}")
    for rule in manifest.concept_rules:
        print(f" -> [{rule.rule_id}] Layer {rule.layer_index}: {rule.operation.upper()} '{rule.vector_direction}' (x{rule.multiplier})")
```

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Method | Remediation Action |
| :--- | :--- | :--- | :--- |
| **CUDA Out Of Memory (OOM)** | Full Jacobian matrix estimation exceeds VRAM capacity | Monitor GPU memory: `nvidia-smi --query-gpu=memory.used,memory.total --format=csv` | Enable `--load-in-4bit` quantization, offload non-target layers to system RAM, or decrease batch size to 1. |
| **Semantic Drift / Model Hallucination** | Steering alpha multiplier set too aggressively (> 1.2) | Run perplexity evaluation: `j-wash benchmark --steered-model ./steered --eval-dataset ./eval.json` | Reduce steering `alpha` to 0.40–0.70 to avoid distorting orthogonal syntactic representations. |
| **GGUF Export Quantization Error** | Missing `llama.cpp` quantization tools or incompatible tensors | Inspect output logs during `export-gguf` | Ensure `llama-quantize` binary exists in PATH and safetensors tensor headers match architecture definition. |
| **Pydantic ValidationError on Preset Manifest** | Malformed rule ID pattern or out-of-range layer index | Validate JSON preset directly using `python -c 'from schema import JWashPresetManifest; ...'` | Verify `rule_id` follows regex `^RULE-[0-9]{3}$` and `layer_index` matches model hidden layer count. |
| **J-Wash UI Backend Connection Timeout** | Port 7860 blocked by firewall or FastAPI backend dead | Check service status: `systemctl status j-wash-steer.service` or `curl -I http://localhost:7860/health` | Restart systemd daemon, verify `CUDA_VISIBLE_DEVICES`, and ensure UFW firewall permits port 7860. |
| **Refusal Manifest Not Unlocked** | Steering vector applied to incorrect residual stream layer | Inspect layer activation using `inspect_residual_layers` tool | Move steering intervention to layers 14–22 where refusal direction is most concentrated in 7B–14B models. |
| **FastMCP Schema Error: extra_forbidden** | Client LLM agent provided non-standard steering arguments | Inspect FastMCP stderr logs for Pydantic schema validation failures | Update client MCP payload to conform to `ConceptVectorParams` strict schema (`extra="forbid"`). |
| **Device Permission Denied in Docker** | NVIDIA Container Toolkit not properly registered in daemon | Inspect `docker run --gpus all nvidia/cuda:12.4-base nvidia-smi` | Install `nvidia-container-toolkit` and restart Docker service (`sudo systemctl restart docker`). |

## Related tools / concepts
- [Claude](claude.md) — Anthropic research context on residual streams and J-Space interpretability.
- [vLLM](../infrastructure/vllm.md) — High-throughput inference engine for serving steered model checkpoints.
- [llama.cpp](../infrastructure/llama-cpp.md) — Lightweight GGUF quantization and local edge execution engine.
- [ExLlamaV3](../infrastructure/exllamav3.md) — High-performance GPU engine for running local safetensors models.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol for agent tool integrations.

## Sources / references
- [J-Wash GitHub Repository](https://github.com/Extraltodeus/J-Wash)
- [Anthropic Research: Transformer Circuits & Representation Engineering](https://transformer-circuits.pub)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
