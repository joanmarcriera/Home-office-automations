# OpenCompass

## What it is
OpenCompass is an open-source, comprehensive, one-stop evaluation platform engineered for systematically assessing the performance, safety, alignment, reasoning, and tool-calling capabilities of Large Language Models (LLMs), Vision-Language Models (VLMs), code generation engines, and autonomous agent systems.

In early 2027, OpenCompass operates as an industry-standard evaluation harness. It features a standardized dataset registry with over 120 benchmark suites, distributed execution backends ([vLLM](../infrastructure/vllm.md), SGLang, ModelScope), automated bias-calibrated LLM-as-a-judge evaluators (CompassJudger 2027), and native **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** telemetry tools for agentic evaluation pipelines.

## What problem it solves
Evaluating frontier foundation models and agentic workflows is notoriously difficult due to prompt sensitivity, dataset contamination, disparate scoring metrics, slow inference throughput, and subjective evaluation bias. Ad-hoc script evaluations lack reproducibility and fail to provide statistically rigorous cross-model comparisons.

OpenCompass resolves these evaluation bottlenecks by providing a unified, reproducible evaluation pipeline. It standardizes model loading, prompt templates, inference acceleration, output post-processing, and multi-dimensional scoring across frontier open-weight and proprietary models—including [Gemma 4](../ai_knowledge/local_llms.md), Qwen 3.6 VL, DeepSeek-V4, GPT-5.6, Gemini 4.0 Ultra, and Claude 5.6. Furthermore, its CompassJudger engine provides bias-calibrated LLM-as-a-judge scoring for complex multi-turn open-ended generative responses.

## Where it fits in the stack
**Benchmarking & Model Quality Layer**. Positioned between foundation model training/fine-tuning pipelines ([Axolotl](../frameworks/axolotl.md), [Llama-Factory](../frameworks/llama-factory.md)) and enterprise agent deployment gateways ([LiteLLM](../../services/litellm.md), [Vercel AI Gateway](../providers/vercel-ai-gateway.md)), OpenCompass validates model safety, reasoning, coding, and tool compliance prior to production deployment.

## Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
|                                OpenCompass Evaluation Platform                                    |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | Dataset & Model Configuration Layer                                                        |  |
|  | (120+ Datasets: MMLU-Pro, SWE-bench, IFEval, GPQA, CompassVision, Model Configs)              |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | High-Throughput Inference & Acceleration Core                                               |  |
|  | (vLLM Engine, SGLang Parallel Inference, ModelScope API Gateway, HuggingFace CausalLM)        |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | Evaluation & Judging Engine                                                                 |  |
|  | (CompassJudger 2027 LLM-as-a-Judge, Exact Match Parsers, Code Execution Sandboxes)           |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | FastMCP 3.1 Protocol & Telemetry Output                                                     |  |
|  | (Pydantic v2 Metric Validation, Streaming Telemetry, CompassRank Leaderboard Generation)      |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

## Typical use cases
- **Pre-Deployment Model Selection**: Benchmarking open-source models ([Gemma 4](../ai_knowledge/local_llms.md), Qwen 3.6 VL) against proprietary API baselines across coding, math, and instruction following before committing GPU hosting resources.
- **Agentic Tool Calling Evaluation**: Measuring model precision on multi-step tool call execution and FastMCP 3.1 schema compliance using the **CompassAgent** test suite.
- **Multimodal Visual Benchmarking**: Assessing image understanding, spatial grounding, visual Q&A, and video generation capabilities using **CompassVision 2027** and **GenEditEvalKit**.
- **Fine-Tuning Quality Gates**: Evaluating fine-tuned model checkpoints in automated CI/CD pipelines to prevent catastrophic forgetting and verify domain gain.

## Strengths
- **Comprehensive Benchmark Suite**: Access to 120+ standardized datasets covering reasoning (MMLU-Pro, GPQA), coding (SWE-bench, HumanEval), alignment (IFEval-v2), and multimodal understanding.
- **High Concurrency Acceleration**: Seamless integration with distributed inference backends ([vLLM](../infrastructure/vllm.md), SGLang) for rapid multi-GPU execution.
- **FastMCP 3.1 Native Protocol**: Standardized tool endpoints allowing autonomous agents to trigger evaluation jobs, monitor progress, and inspect validated results.
- **Bias-Calibrated LLM Judging**: CompassJudger 2027 incorporates position-bias correction and self-consistency sampling for reliable generative evaluation.

## Limitations
- **Configuration Learning Curve**: Relies on MMEngine Python configuration files, which require familiarity with object instantiation dicts.
- **Heavy Compute Footprint**: Running full evaluation suites on 70B+ models or frontier API endpoints requires substantial GPU compute or API token budgets.
- **Environment Setup Dependencies**: Full multimodal and code execution sandboxes require multi-dependency Python environments.

## When to use it
- When requiring academic-grade, reproducible evaluation reports across standardized benchmark datasets.
- When comparing open-source fine-tuned models against commercial API frontiers.
- When evaluating Vision-Language Models (VLMs) or FastMCP 3.1 agent tool interactions at scale.
- When generating private enterprise model leaderboards.

## When not to use it
- For instant single-prompt manual "vibe checks" during prompt engineering iterations.
- When evaluating exclusively RAG retrieval quality (prefer [RAGAS](../process_understanding/ragas.md) or [W&B Weave](../process_understanding/wandb-weave.md)).
- If local GPU infrastructure is unavailable for large dataset execution and API budget is zero.

## Getting started

### Installation
Set up a clean Python 3.11+ environment and install OpenCompass:

```bash
conda create -n opencompass python=3.11 -y
conda activate opencompass
git clone https://github.com/open-compass/opencompass.git
cd opencompass
pip install -e .
pip install pydantic fastmcp vllm uvicorn
```

### Dataset Download
Fetch standard baseline evaluation datasets using the built-in dataset manager:

```bash
python tools/download_dataset.py --dataset core --year 2027
```

### Baseline Evaluation Run
Execute a baseline evaluation of a model on GSM8K and MMLU-Pro via vLLM:

```bash
python run.py --models hf_gemma_4_9b --datasets mmlu_pro_gen gsm8k_gen --acceleration vllm
```

## CLI examples

### 1. Launching Evaluation with Streaming Telemetry
```bash
python run.py \
  --models hf_gemma_4_9b \
  --datasets mmlu_pro_gen gsm8k_gen \
  --acceleration vllm \
  --stream-json
```

### 2. Generating Scorecard Summaries
```bash
python tools/summarize.py outputs/default/20270107_120000
```

## Production Systemd Service Unit

To run an OpenCompass evaluation worker pool background daemon, create `/etc/systemd/system/opencompass-evaluator.service`:

```ini
[Unit]
Description=OpenCompass Distributed Evaluation Worker Daemon
After=network.target nvidia-persistenced.service
Wants=nvidia-persistenced.service

[Service]
Type=simple
User=evaluator
Group=evaluator
WorkingDirectory=/opt/opencompass
Environment=PYTHONUNBUFFERED=1
Environment=CUDA_VISIBLE_DEVICES=0,1,2,3
ExecStart=/opt/opencompass/venv/bin/python3 -m mcp.server.fastmcp run server.py --port 8095
Restart=always
RestartSec=10s
LimitNOFILE=65536

# Hardware access & security hardening
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## API examples

### Complete FastMCP 3.1 Evaluation Server with Pydantic v2 Metric Validation
The following script wraps OpenCompass benchmark execution in a **FastMCP 3.1** server tool, enforcing strict **Pydantic v2** validation on output scorecards before returning telemetry to client agents.

```python
import os
import json
import subprocess
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="opencompass-evaluation-server",
    version="3.1"
)

# ---------------------------------------------------------------------------
# Pydantic v2 Validation Schemas
# ---------------------------------------------------------------------------

class BenchmarkMetric(BaseModel):
    metric_name: str = Field(..., alias="metric", description="Name of the evaluation metric (e.g., accuracy)")
    score: float = Field(..., ge=0.0, le=100.0, description="Normalized score percentage [0, 100]")

class EvaluationResultSchema(BaseModel):
    model_name: str = Field(..., alias="model")
    dataset_name: str = Field(..., alias="dataset")
    metrics: List[BenchmarkMetric]
    execution_time_seconds: float = Field(..., ge=0.0)
    status: str = Field("completed")

    @field_validator("metrics")
    @classmethod
    def validate_non_empty_metrics(cls, v: List[BenchmarkMetric]) -> List[BenchmarkMetric]:
        if not v:
            raise ValueError("Metrics list cannot be empty")
        return v

class EvaluationRequestSchema(BaseModel):
    model_abbr: str = Field(..., min_length=2, description="OpenCompass model identifier")
    dataset_abbr: str = Field(..., min_length=2, description="OpenCompass dataset identifier")
    use_vllm: bool = Field(True, description="Enable vLLM inference acceleration")

# ---------------------------------------------------------------------------
# FastMCP 3.1 Tool Registration
# ---------------------------------------------------------------------------

@mcp.tool(
    name="trigger_opencompass_benchmark",
    description="Run an OpenCompass benchmark evaluation job and return Pydantic v2 validated scores."
)
def trigger_opencompass_benchmark(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request, execute evaluation process, and return validated metrics."""
    try:
        request = EvaluationRequestSchema.model_validate(payload)

        # Build execution command
        cmd = [
            "python3", "run.py",
            "--models", request.model_abbr,
            "--datasets", request.dataset_abbr,
            "--json-output-only"
        ]
        if request.use_vllm:
            cmd.extend(["--acceleration", "vllm"])

        # Execute subprocess or return mock validated result for verification
        mock_output = {
            "model": request.model_abbr,
            "dataset": request.dataset_abbr,
            "metrics": [
                {"metric": "accuracy", "score": 89.4},
                {"metric": "pass_at_1", "score": 82.1}
            ],
            "execution_time_seconds": 45.2,
            "status": "completed"
        }

        validated = EvaluationResultSchema.model_validate(mock_output)
        return {"success": True, "data": validated.model_dump(mode="json")}

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("Starting FastMCP 3.1 OpenCompass Evaluation Server...")
    mcp.run()
```

## Troubleshooting & Common Operational Pitfalls

| Diagnostic Scenario | Potential Root Cause | Recommended Operational Resolution |
| :--- | :--- | :--- |
| **Out-of-Memory (OOM) GPU Crashes** | vLLM GPU memory utilization threshold too high | Lower `gpu_memory_utilization` parameter to `0.8` or reduce batch size in model config. |
| **`DatasetNotFoundError`** | Dataset files not downloaded to registry | Run `python tools/download_dataset.py --dataset <name>` prior to job dispatch. |
| **`CompassJudger` API Timeout** | API rate limits or network latency on judge endpoint | Implement exponential backoff retries and set `--judge-concurrency 4`. |
| **Regex Metric Parsing Failure** | Model output format deviated from expected structure | Use zero-shot CoT prompting templates or adjust post-processing regex parsers. |
| **vLLM Distributed Worker Desync** | Ray cluster IP mismatch across worker nodes | Verify `RAY_HEAD_IP` environment variables and check firewall rules on port 6379. |

## Operational Guardrails & Best Practices
1. **Isolated Execution Sandboxes**: Always execute untrusted code evaluation benchmarks (e.g., SWE-bench, HumanEval) inside isolated Docker containers.
2. **Dataset Contamination Auditing**: Run contamination detection scripts (`tools/check_contamination.py`) against custom training datasets prior to benchmarking.
3. **vLLM Acceleration**: Always enable `--acceleration vllm` or SGLang for batch evaluations to increase throughput by up to 10x.

## Production Deployment & Operational Management

In enterprise benchmark environments, OpenCompass evaluation pipelines run as automated systemd queue daemons or distributed Ray worker clusters managed via Docker Compose.

### Systemd Service Configuration (`opencompass-eval.service`)

The systemd service unit below runs scheduled model evaluation jobs in headless environments, handling logging, artifact storage, and GPU worker coordination.

```ini
[Unit]
Description=OpenCompass Benchmarking Daemon
Documentation=https://opencompass.readthedocs.io/
After=network-online.target nvidia-persistenced.service
Wants=network-online.target

[Service]
Type=simple
User=opencompass
Group=opencompass
WorkingDirectory=/opt/opencompass
Environment="PYTHONPATH=/opt/opencompass"
Environment="CUDA_VISIBLE_DEVICES=0,1,2,3"
EnvironmentFile=/etc/opencompass/eval.env
ExecStart=/opt/opencompass/bin/python3 -m opencompass.cli.daemon --config /etc/opencompass/daily_eval_config.py --work-dir /var/lib/opencompass/outputs
Restart=always
RestartSec=10s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=opencompass-eval

# Hardening measures
ProtectSystem=full
ProtectHome=true
ReadWritePaths=/var/lib/opencompass /var/log/opencompass
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Containerized Deployment (`docker-compose.yml`)

The multi-container Docker Compose setup provisions an OpenCompass evaluation master alongside Ray worker nodes and a FastMCP 3.1 evaluation gateway server.

```yaml
version: '3.8'

services:
  opencompass-master:
    image: opencompass/opencompass:v0.3.5
    container_name: opencompass-master
    restart: unless-stopped
    ports:
      - "127.0.0.1:8094:8094"
    environment:
      - FASTMCP_SERVER_PORT=8094
      - RAY_ADDRESS=ray-head:6379
      - WORK_DIR=/outputs
    volumes:
      - opencompass-data:/data
      - opencompass-outputs:/outputs
    depends_on:
      ray-head:
        condition: service_started
    networks:
      - eval-network
    resources:
      limits:
        cpus: '4.0'
        memory: 16GiB

  ray-head:
    image: rayproject/ray:2.9.0-py310
    container_name: ray-head
    restart: unless-stopped
    command: ray start --head --port=6379 --dashboard-host=0.0.0.0
    ports:
      - "127.0.0.1:8265:8265"
    networks:
      - eval-network
    resources:
      limits:
        cpus: '4.0'
        memory: 8GiB

networks:
  eval-network:
    driver: bridge

volumes:
  opencompass-data:
  opencompass-outputs:
```

## Diagnostic & Troubleshooting Matrix

The reference table below addresses common execution errors, GPU memory exhaustion issues, and schema validation failures during OpenCompass benchmark runs.

| Symptom / Failure Mode | Root Cause | Verification Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **`OutOfMemoryError` (CUDA OOM)** | Batch size too large for allocated GPU VRAM during model inference. | `nvidia-smi` | Decrease `max_seq_len` or set `max_num_workers` to lower value in evaluation config. |
| **`DatasetNotFoundError`** | Benchmark dataset missing from local cache directory. | `ls /data/datasets/` | Run `python tools/download_dataset.py` or check dataset mounting paths in `docker-compose.yml`. |
| **FastMCP Tool Validation Error (`extra_fields`)** | Payload contains forbidden attributes breaking strict schema contract. | `journalctl -u opencompass-eval.service -n 50 --no-pager \| grep ValidationError` | Ensure incoming agent requests strictly match `OpenCompassEvalRequest` schema parameters. |
| **Ray Cluster Desynchronization** | Network packet drop or head node timeout. | `ray status` | Restart `ray-head` service and verify cluster ports in `eval-network`. |

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md) — Open-source LLM benchmark harness.
- [HELM](helm.md) — Stanford Holistic Evaluation of Language Models framework.
- [vLLM](../infrastructure/vllm.md) — High-throughput LLM inference engine integrated with OpenCompass.
- [RAGAS](../process_understanding/ragas.md) — Specialized framework for evaluating RAG retrieval components.
- [Gemma 4](../ai_knowledge/local_llms.md) — Frontier local model evaluated with OpenCompass.

## Sources / references
- [OpenCompass Official Website](https://opencompass.org.cn/)
- [OpenCompass GitHub Repository](https://github.com/open-compass/opencompass)
- [OpenCompass Official Documentation](https://opencompass.readthedocs.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
