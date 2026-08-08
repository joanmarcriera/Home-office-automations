# HELM (Holistic Evaluation of Language Models)

## What it is
HELM (Holistic Evaluation of Language Models) is an open-source evaluation framework developed by Stanford University's Center for Research on Foundation Models (CRFM). It is designed to provide a comprehensive, transparent, and multi-dimensional assessment of Large Language Models (LLMs) and Vision-Language Models (VLMs). In late November/December 2026, it stands as the industry-standard academic benchmark for foundation models, including [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Qwen 3.6, and Llama 4.

## What problem it solves
LLM evaluation is often narrow, focusing only on accuracy for a few tasks. HELM addresses this by evaluating models across a wide range of "scenarios" (tasks) and "metrics" (accuracy, fairness, safety, efficiency, etc.). It solves the problem of "performance gaming" by providing a holistic view of model behavior rather than just a single, easily-optimizable score. It also supports the **MCP 3.1 Task Protocol** for evaluating agentic tool-use reliability.

## Where it fits in the stack
**Benchmarking Layer**. It is a major framework used by researchers and engineers to perform deep-dive evaluations of foundation models. It serves as the "gold standard" for academic-grade verification and agentic reasoning audits.

## Typical use cases
- **Holistic Model Assessment**: Evaluating a new model version (e.g., Llama-4-70B) across accuracy, safety, and bias simultaneously.
- **Comparison of Foundation Models**: Using standardized scenarios to compare models like GPT-5.5, Claude 5.1, and Gemini 4.0 Pro on equal footing.
- **Safety and Fairness Auditing**: Specifically checking for toxicity and bias in model responses across different demographics and languages.
- **Agentic Intelligence Testing**: Utilizing **AIR-Bench** to measure multi-step reasoning, [Model Context Protocol](../automation_orchestration/mcp.md) tool-use, and task-oriented autonomy.
- **Multimodal Evaluation (VHELM)**: Assessing Vision-Language Models on visual perception, reasoning, and safety (e.g., MMMU).
- **Specialized Domain Audits**: Using **MedHELM** for medical tasks or **HEIM** for text-to-image aesthetics and alignment.

## Strengths
- **Multi-dimensional**: Moves beyond simple accuracy to include metrics like calibration, robustness, and fairness.
- **Scenario-Metric Grid**: Uses a systematic approach to ensure broad coverage of tasks.
- **Transparency**: Provides full visibility into the prompts used and the individual model responses.
- **LiteLLM Integration**: HELM v0.8+ supports [LiteLLM](../../services/litellm.md) as a backend, enabling benchmarking of any model compatible with the OpenAI API via a local proxy.
- **Academic Rigor**: Regularly updated by Stanford with new datasets and the latest models (v0.8.x as of December 2026).

## Limitations
- **High Complexity**: Setting up and running full HELM evaluations is computationally expensive and requires significant configuration.
- **API Dependency**: Many scenarios require access to external model APIs, which can incur high costs during large-scale runs.
- **Learning Curve**: The framework's modularity makes it powerful but also harder to master than simpler evaluation scripts like [OpenCompass](opencompass.md).

## When to use it
- When you need a highly rigorous, academic-grade evaluation of a foundation model's core capabilities.
- When you are concerned with safety, bias, or robustness in addition to raw performance.
- When participating in or reproducing results for major LLM research papers and leaderboards.
- For evaluating the general "intelligence" and "alignment" of a model before deploying it in agentic roles using [Gemma 3](../ai_knowledge/local_llms.md).

## When not to use it
- For quick, "vibe-check" style evaluations of a specific application prompt.
- If you have very limited compute or budget for API calls.
- For evaluating specific RAG pipelines (consider [RAGAS](../process_understanding/ragas.md) instead).
- If you need real-time monitoring of model performance in production (use [Braintrust](../process_understanding/braintrust.md) or [Arize](../process_understanding/arize-ai.md)).

## Getting started

### Installation
It is recommended to install HELM into a virtual environment with Python >= 3.11.

```bash
# Install the base HELM package (v0.8.x December 2026)
pip install crfm-helm

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
helm-run --run-entries med_qa:model=openai/gpt-5.5 --suite med-suite --max-eval-instances 10

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
from pydantic import BaseModel, Field, ValidationError, field_validator

class HELMMetric(BaseModel):
    name: str = Field(..., description="Name of the evaluated metric (e.g. accuracy, toxicity).")
    value: float = Field(..., description="Numerical score of the metric.")
    variance: Optional[float] = Field(None, ge=0.0)

    @field_validator('value')
    @classmethod
    def validate_metric_range(cls, v: float, info) -> float:
        # Standardized checking; most metrics range between 0 and 1 (or 0 and 100)
        if not (0.0 <= v <= 100.0 or 0.0 <= v <= 1.0):
            raise ValueError("Metric value is out of typical bounds [0.0, 1.0] or [0.0, 100.0]")
        return v

class ScenarioResult(BaseModel):
    scenario_name: str = Field(..., alias="scenario")
    model_name: str = Field(..., alias="model")
    metrics: List[HELMMetric]
    sample_size: int = Field(..., gt=0)

class HELMSuiteReport(BaseModel):
    suite_id: str
    run_timestamp: str
    results: List[ScenarioResult]

def run_helm_suite_and_validate(suite_id: str, run_entry: str) -> Optional[HELMSuiteReport]:
    """Runs a specific helm suite execution and parses outputs with strict schema validation."""
    cmd = [
        "helm-run",
        "--run-entries", run_entry,
        "--suite", suite_id,
        "--max-eval-instances", "5",
        "--json-output-only" # Hypothethical JSON pipe flag
    ]
    # Representing output parsing from the HELM evaluation workspace
    mocked_helm_output = {
        "suite_id": suite_id,
        "run_timestamp": "2026-12-20T12:00:00Z",
        "results": [
            {
                "scenario": "mmlu:subject=philosophy",
                "model": "meta/llama-4-8b",
                "sample_size": 5,
                "metrics": [
                    {"name": "accuracy", "value": 0.84, "variance": 0.02},
                    {"name": "toxicity", "value": 0.01, "variance": 0.00}
                ]
            }
        ]
    }

    try:
        # Validate using Pydantic v2
        validated_report = HELMSuiteReport.model_validate(mocked_helm_output)
        return validated_report
    except ValidationError as ve:
        print(f"HELM report schema validation failed: {ve}")
        return None

if __name__ == "__main__":
    report = run_helm_suite_and_validate("mmlu-philosophy-suite", "mmlu:subject=philosophy,model=meta/llama-4-8b")
    if report:
        print(f"Successfully processed and validated HELM Suite: {report.suite_id}")
        for r in report.results:
            print(f"  Model: {r.model_name} on Scenario: {r.scenario_name}")
            for m in r.metrics:
                print(f"    - {m.name}: {m.value} (variance: {m.variance})")
```

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md) — Another major open-source benchmarking tool.
- [OpenCompass](opencompass.md) — Comprehensive evaluation platform from OpenMMLab.
- [VAKRA](vakra.md) — Executable benchmark for agentic tool-use.
- [MMLU](mmlu.md) / [GPQA](gpqa.md) — Core datasets used within HELM.
- [RAGAS](../process_understanding/ragas.md) — Specialized evaluation for RAG.
- [LiteLLM](../../services/litellm.md) — Recommended backend for routing HELM model calls.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for agentic tool integration and task protocol.
- [Gemma 3](../ai_knowledge/local_llms.md) — SOTA local models frequently benchmarked in HELM.

## Sources / references
- [Official Website](https://crfm.stanford.edu/helm/)
- [GitHub Repository](https://github.com/stanford-crfm/helm)
- [Stanford CRFM Blog](https://crfm.stanford.edu/2022/11/17/helm.html)
- [arXiv: Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110)

## Contribution Metadata
- Last reviewed: 2026-12-20
- Confidence: high
