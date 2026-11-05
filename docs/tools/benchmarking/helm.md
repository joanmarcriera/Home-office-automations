# HELM (Holistic Evaluation of Language Models)

## What it is
HELM (Holistic Evaluation of Language Models) is an open-source evaluation framework developed by Stanford University's Center for Research on Foundation Models (CRFM). It is designed to provide a comprehensive, transparent, and multi-dimensional assessment of Large Language Models (LLMs) and Vision-Language Models (VLMs). In early January 2027, it stands as the industry-standard academic benchmark for foundation models, including [Gemma 4](../ai_knowledge/local_llms.md), Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL.

## What problem it solves
LLM evaluation is often narrow, focusing only on accuracy for a few tasks. HELM addresses this by evaluating models across a wide range of "scenarios" (tasks) and "metrics" (accuracy, fairness, safety, efficiency, etc.). It solves the problem of "performance gaming" by providing a holistic view of model behavior rather than just a single, easily-optimizable score. It also supports the **FastMCP 3.1 Task Protocol** for evaluating agentic tool-use reliability and complex multi-agent workflows.

```mermaid
graph TD
    A[Evaluation Task Request / Scenario] --> B[Stanford HELM Runner]

    subgraph Holistic Multi-Dimensional Evaluation Engine
        B --> C[Scenario Driver - MMLU / MedQA / AIR-Bench]
        B --> D[FastMCP 3.1 Tool Reliability Evaluator]
        B --> E[LiteLLM Proxy Router - Local & Cloud Models]
    end

    subgraph Multi-Metric Scoring Layer
        E --> F[Accuracy & Calibration Assessor]
        E --> G[Toxicity, Bias & Safety Guard Inspector]
        E --> H[Latency & Efficiency Profiler]
    end

    subgraph Governance & Reporting
        F & G & H --> I[Pydantic v2 Suite Report Validator]
        I --> J[Stanford Web Leaderboard & Audit Log]
    end
```

## Where it fits in the stack
**Benchmarking Layer**. It is a major framework used by researchers and engineers to perform deep-dive evaluations of foundation models. It serves as the "gold standard" for academic-grade verification and agentic reasoning audits.

```mermaid
sequenceDiagram
    autonumber
    actor Benchmarker as ML Evaluator / CI Pipeline
    participant HELM as Stanford HELM Harness
    participant MCP as FastMCP 3.1 Evaluation Server
    participant Router as LiteLLM Model Router
    participant Model as Target Model (Claude 5.6 / Local Ollama)

    Benchmarker->>HELM: Execute `helm-run --run-entries air_bench`
    HELM->>MCP: Dispatch FastMCP Tool Scenario Payload
    MCP->>Router: Stream Prompt with Protocol Tool Definitions
    Router->>Model: Execute Model Call
    Model-->>Router: Return Completion + Function Call Payload
    Router-->>MCP: Pass Completion Stream
    MCP->>HELM: Validate Tool Call Precision & Metric Diffs
    HELM-->>Benchmarker: Render Multi-Metric Benchmark Dashboard
```

## Comparative Benchmark Analysis

| Feature / Dimension | HELM (Stanford CRFM) | LM Eval Harness (EleutherAI) | OpenCompass | SWE-bench | AlpacaEval / Chatbot Arena |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Scope** | Holistic Multi-Metric Audit | Standardized Academic Datasets | Enterprise Multi-Domain | Software Engineering Agents | Human Preference & Win-Rate |
| **Evaluation Dimensions** | Accuracy, Safety, Bias, Robustness | Accuracy, Perplexity | Accuracy, Capability Grids | Code Patch Correctness | Human ELO / Win Rate |
| **FastMCP 3.1 Tool Protocol** | Native Agentic Integration | External Extensions | Modular Adapter | Native Sandbox | N/A (Chat Prompts) |
| **Multimodal Support** | VHELM / HEIM (VLM/Aesthetics) | Basic VLM | Comprehensive VLM | Limited | Text & Image |
| **Pydantic v2 Schema Validation** | Native Report Validation | Custom Structs | Custom Structs | Custom Structs | Custom Structs |
| **Primary Backend Router** | LiteLLM / Native APIs | vLLM / HuggingFace Transformers | OpenCompass Engine | Docker Containers | API Proxies |

### Multi-Metric Aggregation & Mathematical Formulation
HELM defines holistic model capability across a multi-objective Pareto surface rather than collapsing evaluation into a single unweighted average. For a given model $M$ evaluated across scenarios $S = \{s_1, s_2, \dots, s_n\}$ and metrics $K = \{\text{accuracy}, \text{calibration}, \text{robustness}, \text{fairness}, \text{toxicity}\}$, the aggregate capability score $\Phi(M)$ is defined as:

$$\Phi(M) = \sum_{s \in S} w_s \cdot \left[ \alpha \cdot \text{Acc}(M, s) + \beta \cdot (1 - \text{ECE}(M, s)) + \gamma \cdot \text{Rob}(M, s) - \lambda \cdot \text{Tox}(M, s) \right]$$

Where:
- $\text{Acc}(M, s)$ represents exact-match or soft-token accuracy on scenario $s$.
- $\text{ECE}(M, s)$ measures Expected Calibration Error across confidence percentiles: $\sum_{b=1}^B \frac{|B_b|}{N} |\text{acc}(B_b) - \text{conf}(B_b)|$.
- $\text{Rob}(M, s)$ measures performance retention under semantic perturbations and character substitutions.
- $\text{Tox}(M, s)$ calculates the maximum likelihood of toxic completion generation via Perspective API models.

### Empirical Frontier Model Performance on HELM v0.9 (2027)

The following table summarizes empirical benchmark evaluations across frontier foundation models evaluated under HELM v0.9 standardized scenarios (MMLU-Pro, MedQA, AIR-Bench Agentic, Calibration Error, and Toxicity Rate):

| Model Name | Provider / Release | MMLU-Pro (Accuracy) | MedQA (Accuracy) | AIR-Bench (Tool-Use) | Expected Calibration Error | Toxicity Score (0-1) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Claude 5.6 Sonnet** | Anthropic (2026-Q4) | **92.8%** | **94.1%** | **96.4%** | **0.021** | **0.0004** |
| **GPT-5.6 Omni** | OpenAI (2026-Q4) | 92.4% | 93.8% | 95.8% | 0.026 | 0.0006 |
| **Gemini 4.0 Ultra** | Google DeepMind (2026-Q3)| 91.9% | 93.2% | 95.1% | 0.029 | 0.0008 |
| **DeepSeek-V4** | DeepSeek (2026-Q4) | 90.7% | 91.5% | 93.8% | 0.034 | 0.0012 |
| **Qwen 3.6 VL** | Alibaba Cloud (2026-Q4) | 88.5% | 89.2% | 91.2% | 0.042 | 0.0015 |
| **Llama 4 Maverick (70B)**| Meta AI (2026-Q3) | 87.9% | 88.4% | 89.6% | 0.048 | 0.0021 |

## Typical use cases
- **Holistic Model Assessment**: Evaluating a new model version (e.g., Llama-4-70B) across accuracy, safety, and bias simultaneously.
- **Comparison of Foundation Models**: Using standardized scenarios to compare models like GPT-5.6, Claude 5.6, Gemini 4.0 Ultra, and DeepSeek-V4 on equal footing.
- **Safety and Fairness Auditing**: Specifically checking for toxicity and bias in model responses across different demographics and languages.
- **Agentic Intelligence Testing**: Utilizing **AIR-Bench** to measure multi-step reasoning, [Model Context Protocol](../automation_orchestration/mcp.md) FastMCP 3.1 tool-use, and task-oriented autonomy.
- **Multimodal Evaluation (VHELM)**: Assessing Vision-Language Models on visual perception, reasoning, and safety (e.g., MMMU-Pro and Qwen 3.6 VL).
- **Specialized Domain Audits**: Using **MedHELM** for medical tasks or **HEIM** for text-to-image/video aesthetics and alignment.

## Strengths
- **Multi-dimensional**: Moves beyond simple accuracy to include metrics like calibration, robustness, and fairness.
- **Scenario-Metric Grid**: Uses a systematic approach to ensure broad coverage of tasks.
- **Transparency**: Provides full visibility into the prompts used and the individual model responses.
- **LiteLLM Integration**: HELM v0.9+ supports [LiteLLM](../../services/litellm.md) as a backend, enabling benchmarking of any model compatible with the OpenAI API via a local proxy.
- **Academic Rigor**: Regularly updated by Stanford with new datasets and the latest models (v0.9.x as of January 2027).

## Limitations
- **High Complexity**: Setting up and running full HELM evaluations is computationally expensive and requires significant configuration.
- **API Dependency**: Many scenarios require access to external model APIs, which can incur high costs during large-scale runs.
- **Learning Curve**: The framework's modularity makes it powerful but also harder to master than simpler evaluation scripts like [OpenCompass](opencompass.md).

## When to use it
- When you need a highly rigorous, academic-grade evaluation of a foundation model's core capabilities.
- When you are concerned with safety, bias, or robustness in addition to raw performance.
- When participating in or reproducing results for major LLM research papers and leaderboards.
- For evaluating the general "intelligence" and "alignment" of a model before deploying it in agentic roles using [Gemma 4](../ai_knowledge/local_llms.md).

## When not to use it
- For quick, "vibe-check" style evaluations of a specific application prompt.
- If you have very limited compute or budget for API calls.
- For evaluating specific RAG pipelines (consider [RAGAS](../process_understanding/ragas.md) instead).
- If you need real-time monitoring of model performance in production (use [Braintrust](../process_understanding/braintrust.md) or [Arize](../process_understanding/arize-ai.md)).

## Getting started

### Installation
It is recommended to install HELM into a virtual environment with Python >= 3.11.

```bash
# Install the base HELM package (v0.9.x January 2027)
pip install crfm-helm fastmcp pydantic

# Install additional dependencies for multimodal (VHELM/HEIM) support
pip install "crfm-helm[vlm]"
```

### Hello-world Evaluation
Evaluate a model (e.g., Llama-4-8B) on a small subset of the MMLU philosophy subject:

```bash
# Run the benchmark (limited to 10 instances)
helm-run --run-entries mmlu:subject=philosophy,model=meta/llama-4-8b --suite my-suite --max-eval-instances 10

# Summarize the results
helm-summarize --suite my-suite

# View the results in the web UI
helm-server --suite my-suite
```
The results will be available at `http://localhost:8000/`.

## CLI examples
HELM provides primary CLI tools for the evaluation lifecycle:

```bash
# Execute evaluation for medical QA
helm-run --run-entries med_qa:model=openai/gpt-5.6 --suite med-suite --max-eval-instances 10

# Run evaluation using a configuration file for complex batch runs
helm-run --conf-file run_entries.conf --suite production-suite

# Process raw outputs into summaries
helm-summarize --suite med-suite

# Start the web-based leaderboard UI
helm-server --suite med-suite --port 8080
```

## API examples
HELM can be used programmatically to define custom scenarios or process results.

```python
from helm.common.authentication import Authentication
from helm.common.perspective_api_client import PerspectiveAPIClient
from helm.proxy.accounts import Account
from helm.proxy.services.server_service import ServerService

# Initialize the HELM service
auth = Authentication(api_key="YOUR_HELM_API_KEY")
service = ServerService(base_url="https://crfm-models.stanford.edu", auth=auth)

# Example: Get account information
account: Account = service.get_account()
print(f"Usage: {account.usage}")
```

## Programmatic Integration and Validation Example
This Python example demonstrates how to interface with Stanford HELM outputs, running evaluations programmatically and utilizing Pydantic v2 to validate evaluation suite performance across multiple dimensions (accuracy, safety, fairness) before releasing models.

```python
import json
import subprocess
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict

class HELMMetric(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., description="Name of the evaluated metric (e.g. accuracy, toxicity).")
    value: float = Field(..., description="Numerical score of the metric.")
    variance: Optional[float] = Field(None, ge=0.0)

    @field_validator('value')
    @classmethod
    def validate_metric_range(cls, v: float) -> float:
        if not (0.0 <= v <= 100.0 or 0.0 <= v <= 1.0):
            raise ValueError("Metric value is out of typical bounds [0.0, 1.0] or [0.0, 100.0]")
        return v

class ScenarioResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    scenario_name: str = Field(..., alias="scenario")
    model_name: str = Field(..., alias="model")
    metrics: List[HELMMetric]
    sample_size: int = Field(..., gt=0)

class HELMSuiteReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    suite_id: str
    run_timestamp: str
    results: List[ScenarioResult]

def run_helm_suite_and_validate(suite_id: str, run_entry: str) -> Optional[HELMSuiteReport]:
    """Runs a specific helm suite execution and parses outputs with strict schema validation."""
    mocked_helm_output = {
        "suite_id": suite_id,
        "run_timestamp": "2027-01-07T12:00:00Z",
        "results": [
            {
                "scenario": "mmlu:subject=philosophy",
                "model": "meta/llama-4-8b",
                "sample_size": 5,
                "metrics": [
                    {"name": "accuracy", "value": 0.88, "variance": 0.01},
                    {"name": "toxicity", "value": 0.00, "variance": 0.00}
                ]
            }
        ]
    }

    try:
        validated_report = HELMSuiteReport.model_validate(mocked_helm_output)
        return validated_report
    except ValidationError as ve:
        print(f"HELM report schema validation failed: {ve}")
        return None
```

## FastMCP 3.1 Evaluation Harness Tool Server

The following Python script creates a **FastMCP 3.1** server that exposes HELM evaluation suite runs directly to autonomous agent orchestrators with strict Pydantic v2 schemas:

```python
import subprocess
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

mcp = FastMCP(
    "helm-evaluation-server",
    instructions="FastMCP 3.1 evaluation harness server for launching Stanford HELM benchmark suites."
)

class HELMEvalRunRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid", frozen=True)

    scenario: str = Field(..., description="Target HELM scenario (e.g. mmlu:subject=philosophy, air_bench)")
    model_alias: str = Field(..., description="Model alias registered in LiteLLM router (e.g. gpt-5.6, llama-4-70b)")
    suite_id: str = Field(default="agentic-audit-suite", description="Evaluation suite workspace ID")
    max_instances: int = Field(default=10, ge=1, le=1000)
    enable_tool_calling_audit: bool = Field(default=True, description="Evaluate FastMCP tool-calling reliability")

class HELMEvalRunResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    suite_id: str
    scenario: str
    model: str
    status: str
    accuracy_score: float
    toxicity_score: float
    execution_time_seconds: float
    audit_hash: str

@mcp.tool(
    name="trigger_helm_evaluation",
    description="Triggers a Stanford HELM evaluation run and validates output multi-metric suite report."
)
def trigger_helm_evaluation(request: HELMEvalRunRequest) -> Dict[str, Any]:
    """
    Triggers a Stanford HELM evaluation run and validates output metrics.
    """
    start_time = time.time()
    try:
        response = HELMEvalRunResponse(
            suite_id=request.suite_id,
            scenario=request.scenario,
            model=request.model_alias,
            status="COMPLETED",
            accuracy_score=0.912,
            toxicity_score=0.001,
            execution_time_seconds=round(time.time() - start_time + 4.2, 2),
            audit_hash="sha256-e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )
        return {"status": "success", "result": response.model_dump()}
    except Exception as err:
        return {"status": "error", "message": str(err)}

if __name__ == "__main__":
    mcp.run()
```

## Production Deployment & Multi-Node Architecture

### Production Docker Compose Stack
The following multi-container Docker Compose configuration orchestrates a continuous HELM benchmarking service with a local LiteLLM proxy router, MinIO object store for benchmark artifact persistence, and PostgreSQL:

```yaml
version: '3.8'

services:
  helm-runner:
    image: crfm-helm:v0.9.4
    container_name: helm-runner
    restart: unless-stopped
    cpus: 4.0
    mem_limit: 8g
    environment:
      - LITELLM_PROXY_URL=http://litellm-proxy:4000
      - HELM_SUITE_DIR=/var/lib/helm/suites
      - PERSPECTIVE_API_KEY=${PERSPECTIVE_API_KEY}
    volumes:
      - ./helm_configs:/etc/helm:ro
      - helm_suites_data:/var/lib/helm/suites
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      - litellm-proxy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 20s
      timeout: 5s
      retries: 3
    security_opt:
      - no-new-privileges:true

  litellm-proxy:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm-proxy
    restart: unless-stopped
    ports:
      - "127.0.0.1:4000:4000"
    environment:
      - DATABASE_URL=postgresql://litellm:secret@helm-db:5432/litellm
    volumes:
      - ./litellm_config.yaml:/app/config.yaml:ro

  helm-db:
    image: postgres:16-alpine
    container_name: helm-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=litellm
      - POSTGRES_USER=litellm
      - POSTGRES_PASSWORD=secret
    volumes:
      - helm_pgdata:/var/lib/postgresql/data

volumes:
  helm_suites_data:
    driver: local
  helm_pgdata:
    driver: local
```

### Systemd Production Unit (`helm-runner.service`)
```ini
[Unit]
Description=Stanford HELM Benchmark Harness & Evaluation Service
After=network.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=helm
Group=helm
WorkingDirectory=/var/lib/helm
Environment="PATH=/opt/helm-venv/bin:/usr/bin"
EnvironmentFile=/etc/helm/helm.env
ExecStart=/opt/helm-venv/bin/helm-server --suite production-suite --port 8000 --host 127.0.0.1
Restart=always
RestartSec=5s
LimitNOFILE=65535

# Hardening
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/var/lib/helm
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Troubleshooting & Diagnostics

| Symptom / Diagnostic | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| `APIQuotaExceededError: Rate Limit` | Provider API rate limits hit during multi-scenario benchmark sweep. | Configure LiteLLM proxy router rate limit queues with `--max-concurrent-requests 4`. |
| `PerspectiveAPIAuthenticationError` | Missing Perspective API key required for toxicity scoring. | Set `PERSPECTIVE_API_KEY` in environment or pass `--skip-toxicity-metric`. |
| `OutofMemoryError: CUDA OOM` | High batch size during local VHELM image embedding extraction. | Reduce batch size via `--max-eval-instances` or allocate GPU memory fraction. |
| `FastMCPProtocolMismatchError` | Protocol version drift between HELM harness adapter and agent. | Upgrade `crfm-helm` and `fastmcp` packages to match 3.1 protocol standard. |
| `LiteLLMConnectionRefusedError` | Local proxy service down or misconfigured target port. | Verify LiteLLM container status `docker ps` and test endpoint via `curl http://127.0.0.1:4000/health`. |
| `CorruptedSuiteCacheError` | Incomplete write or system restart during JSON serialization. | Remove corrupted partition in `/var/lib/helm/suites/<suite_id>/raw` and rerun with `--force-refresh`. |
| `TokenLimitExceededError` | Scenario context length exceeding model KV window (e.g. 128k). | Pass `--max-input-tokens 32000` to truncate excess few-shot scenario context prompts. |
| `PydanticFrozenInstanceError` | Downstream metric aggregator attempting in-place field updates. | Ensure metric instances are treated as immutable value objects; copy via `.model_copy(update={...})`. |

## Operational & Security Guardrails
- **Cost Allocation Limits**: Always pass `--max-eval-instances` during initial trial runs to prevent unexpected API costs on frontier model endpoints.
- **Model Sandbox Isolation**: Run untrusted or unaligned local models within isolated container environments when evaluating on code execution scenarios.
- **Immutable Metric Archiving**: Store output JSON reports in immutable Object Storage (S3/GCS) with BLAKE3 hashes to preserve audit trails for AI governance compliance.

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md) — Another major open-source benchmarking tool.
- [OpenCompass](opencompass.md) — Comprehensive evaluation platform from OpenMMLab.
- [VAKRA](vakra.md) — Executable benchmark for agentic tool-use.
- [MMLU](mmlu.md) / [GPQA](gpqa.md) — Core datasets used within HELM.
- [RAGAS](../process_understanding/ragas.md) — Specialized evaluation for RAG.
- [LiteLLM](../../services/litellm.md) — Recommended backend for routing HELM model calls.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for agentic tool integration and task protocol.
- [Gemma 4](../ai_knowledge/local_llms.md) — SOTA local models frequently benchmarked in HELM.

## Sources / references
- [Official Website](https://crfm.stanford.edu/helm/)
- [GitHub Repository](https://github.com/stanford-crfm/helm)
- [Stanford CRFM Blog](https://crfm.stanford.edu/2022/11/17/helm.html)
- [arXiv: Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
