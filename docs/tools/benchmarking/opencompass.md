# OpenCompass

## What it is
OpenCompass is a comprehensive, one-stop platform designed for evaluating the capabilities of large language models (LLMs) and vision-language models (VLMs). It provides a complete evaluation pipeline, including dataset preparation, evaluation scripts, and leaderboards. In late November/December 2026, it remains the standard for open-source model benchmarking, featuring deep integration with the [MCP 3.1 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## What problem it solves
Evaluating modern large models is complex, requiring diverse datasets and multiple evaluation paradigms (e.g., zero-shot, few-shot, CoT). OpenCompass standardizes this process, providing a reproducible and extensible framework that supports over 100 datasets. It addresses the fragmentation of evaluation criteria by providing a unified interface for cross-domain and large-scale model evaluation, including the latest frontier models like [Gemma 3](../ai_knowledge/local_llms.md), Qwen 3.6, Llama 4, GPT-5.5, and Claude 5.1.

## Where it fits in the stack
**Benchmarking Layer**. It serves as an evaluation toolkit and platform for comparing model performance across a wide range of tasks, including linguistic, knowledge, reasoning, coding, and multi-modality.

## Typical use cases
- **Model Development**: Benchmarking in-house models against industry standards (e.g., Qwen 3.6, Llama 4, InternVL 3) during training.
- **Model Selection**: Comparing different open-source or API-based models ([Gemma 3](../ai_knowledge/local_llms.md), GPT-5.5, Claude 5.1) to find the best fit for a specific agentic application.
- **VLM & Image Evaluation**: Using the **GenEditEvalKit** to evaluate image generation and editing models across multiple benchmarks.
- **Agentic Evaluation**: Measuring model performance on multi-step reasoning tasks using the **CompassAgent** suite and **FastMCP 3.1** tool definitions.

## Strengths
- **Comprehensive Coverage**: Supports 100+ datasets, including IFEval, MMLU-Pro, and GPQA.
- **Flexible Architecture**: Supports multiple evaluation paradigms, including Zero-shot, Few-shot, CoT, and **LLM-as-a-judge** (CompassJudger).
- **High Concurrency**: Integrates with acceleration backends like [vLLM](../infrastructure/vllm.md), LMDeploy, and ModelScope for distributed, high-speed evaluation.
- **Unified Multimodal Support**: Enhanced support for Unified Multimodal Models (UMMs) and vision-language tasks.
- **MCP 3.1 Support**: Native integration for agents to trigger and monitor evaluation runs via standardized FastMCP 3.1 tool calls.

## Limitations
- **Complexity**: The extensive configuration system (based on MMEngine) has a steep learning curve for beginners.
- **Resource Intensive**: Running full-scale evaluations on frontier models requires significant local compute (GPUs) or high API credit consumption.
- **Setup Overhead**: Requires significant environment configuration compared to lightweight "vibe-check" scripts.

## When to use it
- When you need a standardized, reproducible way to evaluate models across dozens of dimensions.
- For evaluating Vision-Language Models (VLMs) and image generation models at scale.
- When contributing to or comparing against public leaderboards (CompassRank).
- When developing new foundation models that require rigorous academic-grade benchmarking.

## When not to use it
- For very simple, single-task evaluations or quick "vibe checks" of a prompt.
- If you only need to evaluate basic RAG performance (consider [RAGAS](../process_understanding/ragas.md)).
- If you lack the hardware or budget for large-scale evaluation runs.

## Getting started

### Installation
It is recommended to use a Conda environment for dependency management.

```bash
conda create --name opencompass python=3.11 -y
conda activate opencompass
git clone https://github.com/open-compass/opencompass.git
cd opencompass
pip install -e .
```

### Dataset Preparation
Datasets are managed centrally in the `data/` directory.

```bash
# Download core datasets (December 2026 baseline)
python tools/download_dataset.py --dataset core
```

### Hello-world Evaluation
Evaluate a small model (e.g., Gemma-3-8B) on standard benchmarks:

```bash
# Evaluate Gemma-3-8B on MMLU and GSM8K
python run.py --models hf_gemma_3_8b --datasets mmlu_gen gsm8k_gen
```

## CLI examples
OpenCompass provides a powerful CLI for running and managing evaluations:

```bash
# Run evaluation with vLLM acceleration
python run.py --models hf_gemma_3_8b --datasets mmlu_gen --acceleration vllm

# Summarize results from a previous run
python tools/summarize.py outputs/default/20261215_100000

# Run image generation evaluation
python GenEditEvalKit/run.py --models stable-diffusion-3.5 --benchmarks GEdit
```

## API examples
While primarily used via CLI, OpenCompass configurations are Python-based and can be integrated into custom pipelines:

```python
from mmengine.config import read_base
from opencompass.models import HuggingFaceCausalLM

with read_base():
    from .datasets.mmlu.mmlu_gen import mmlu_datasets

models = [
    dict(
        type=HuggingFaceCausalLM,
        abbr='gemma-3-8b-hf',
        path='google/gemma-3-8b-it',
        model_kwargs=dict(device_map='auto'),
        max_seq_len=8192,
        max_out_len=1024,
        batch_size=32,
        run_cfg=dict(num_gpus=1),
    )
]
datasets = mmlu_datasets
```

## Programmatic Integration and Validation Example
This Python example executes a local OpenCompass evaluation job and utilizes Pydantic v2 to strictly validate evaluation results and schema parameters before writing them to a central database.

```python
import json
import subprocess
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError

class DatasetMetric(BaseModel):
    metric_name: str = Field(..., alias="metric")
    score: float = Field(..., ge=0.0, le=100.0)

class CompassResult(BaseModel):
    model_name: str = Field(..., alias="model")
    dataset_name: str = Field(..., alias="dataset")
    metrics: List[DatasetMetric]
    execution_time_sec: float = Field(..., ge=0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

def run_opencompass_and_validate(model_abbr: str, dataset_abbr: str) -> Optional[CompassResult]:
    """Runs a sub-process evaluation and validates outputs using Pydantic v2."""
    cmd = [
        "python3", "run.py",
        "--models", model_abbr,
        "--datasets", dataset_abbr,
        "--json-output-only" # Headless flag
    ]
    try:
        response = subprocess.run(cmd, capture_output=True, text=True, check=True)
        raw_data = json.loads(response.stdout)

        # Enforce validation on execution state and metrics
        validated_result = CompassResult.model_validate(raw_data)
        return validated_result
    except subprocess.CalledProcessError as e:
        print(f"OpenCompass subprocess execution failed: {e.stderr}")
        return None
    except ValidationError as e:
        print(f"OpenCompass validated schema mismatch: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse OpenCompass JSON outputs: {e}")
        return None

if __name__ == "__main__":
    result = run_opencompass_and_validate("hf_gemma_3_8b", "gsm8k_gen")
    if result:
        print(f"Successfully validated OpenCompass metrics for model: {result.model_name}")
        for m in result.metrics:
            print(f"  - Dataset '{result.dataset_name}' metric '{m.metric_name}': {m.score}")
```

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md) — Alternative evaluation framework.
- [HELM](helm.md) — Holistic evaluation by Stanford.
- [vLLM](../infrastructure/vllm.md) — High-throughput inference engine often used with OpenCompass.
- [Ragas](../process_understanding/ragas.md) — Specialized RAG evaluation.
- [Gemma 3](../ai_knowledge/local_llms.md) — Local model frequently benchmarked with OpenCompass.
- [LiteLLM](../../services/litellm.md) — Inference proxy for API-based model evaluation.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Integration standard for agentic benchmarking.
- [VAKRA](vakra.md) — Specialized enterprise agent benchmark.

## Sources / references
- [Official Website](https://opencompass.org.cn/)
- [GitHub Repository](https://github.com/open-compass/opencompass)
- [OpenCompass Documentation](https://opencompass.readthedocs.io/en/latest/)
- [GenEditEvalKit Release](https://github.com/open-compass/GenEditEvalKit)

## Contribution Metadata
- Last reviewed: 2026-12-15
- Confidence: high
