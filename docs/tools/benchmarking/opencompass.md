# OpenCompass

## What it is
OpenCompass is a comprehensive, one-stop platform designed for evaluating the capabilities of large language models (LLMs), vision-language models (VLMs), and autonomous agent frameworks. It provides a complete evaluation pipeline, including dataset preparation, distributed execution scripts, and public/private leaderboards (CompassRank). As of early January 2027, OpenCompass remains the industry benchmark standard for foundation model evaluation, featuring deep integration with the [MCP 3.1 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) and FastMCP 3.1 streaming telemetry.

## What problem it solves
Evaluating modern large-scale multi-modal and agentic models is complex, requiring diverse datasets and multiple evaluation paradigms (e.g., zero-shot, few-shot, Chain-of-Thought, and multi-turn agent execution). OpenCompass standardizes this process, providing a reproducible and extensible framework supporting over 120 standardized datasets. It addresses the fragmentation of evaluation criteria by providing a unified interface for cross-domain evaluation across frontier models like [Gemma 4](../ai_knowledge/local_llms.md), Qwen 3.6 VL, DeepSeek-V4, GPT-5.6, Gemini 4.0 Ultra, and Claude 5.6.

## Where it fits in the stack
**Benchmarking Layer**. It serves as an evaluation toolkit and platform for comparing model performance across a wide range of tasks, including linguistic, mathematical, reasoning, coding, tool-calling, and multi-modality.

## Typical use cases
- **Model Development**: Benchmarking in-house models against industry standards (e.g., Qwen 3.6 VL, DeepSeek-V4, InternVL 3) during pre-training and alignment loops.
- **Model Selection**: Comparing different open-source or API-based models ([Gemma 4](../ai_knowledge/local_llms.md), GPT-5.6, Gemini 4.0 Ultra, Claude 5.6) to find the best fit for specific enterprise agentic applications.
- **VLM & Multimodal Evaluation**: Utilizing **GenEditEvalKit** and **CompassVision 2027** to evaluate image/video generation, spatial understanding, and editing capabilities.
- **Agentic & FastMCP Benchmarking**: Measuring model performance on complex multi-step reasoning and tool-interaction tasks using the **CompassAgent** suite and **FastMCP 3.1** protocol test suites.

## Strengths
- **Comprehensive Coverage**: Supports 120+ datasets, including IFEval-v2, MMLU-Pro-2027, GPQA-Diamond, and SWE-bench Verified.
- **Flexible Evaluation Paradigms**: Supports Zero-shot, Few-shot, CoT, and **LLM-as-a-judge** (CompassJudger 2027) with bias calibration.
- **High Concurrency Execution**: Seamlessly integrates with inference backends like [vLLM](../infrastructure/vllm.md), SGLang, and ModelScope for distributed, multi-GPU high-speed evaluation.
- **Unified Multimodal Support**: Advanced evaluation harnesses for Unified Multimodal Models (UMMs) across text, image, audio, and video modalities.
- **FastMCP 3.1 Native Protocol**: Standardized agent integration allowing agents to trigger, monitor, and stream evaluation results via FastMCP 3.1 tools.

## Limitations
- **Configuration Complexity**: The extensive configuration system (built on MMEngine and Python-based configs) presents a steep learning curve for new users.
- **Resource Footprint**: Running full-scale evaluations on frontier 70B+ or frontier API models requires substantial compute clusters or high API token budgets.
- **Setup Overhead**: Requires multi-dependency Python environments compared to simple single-prompt vibe checks.

## When to use it
- When you need a standardized, reproducible way to evaluate models across dozens of capabilities.
- For evaluating Vision-Language Models (VLMs), audio-visual models, and image generation frameworks at scale.
- When contributing to or comparing against public leaderboards (CompassRank 2027).
- When developing new foundation models or fine-tuned variants requiring rigorous academic-grade benchmarking.

## When not to use it
- For quick single-prompt "vibe checks" during prompt engineering iteration.
- If you only need lightweight RAG retrieval evaluation (consider [RAGAS](../process_understanding/ragas.md) or [W&B Weave](../process_understanding/wandb-weave.md)).
- If you lack local GPU compute or API credits required for full dataset runs.

## Getting started

### Installation
It is recommended to use a clean Python 3.11+ virtual environment or Conda environment.

```bash
conda create --name opencompass python=3.11 -y
conda activate opencompass
git clone https://github.com/open-compass/opencompass.git
cd opencompass
pip install -e .
```

### Dataset Preparation
Datasets are managed centrally via the dataset download helper:

```bash
# Download core 2027 baseline datasets
python tools/download_dataset.py --dataset core --year 2027
```

### Hello-world Evaluation
Evaluate a lightweight model (e.g., Gemma-4-9B) on standard benchmarks:

```bash
# Evaluate Gemma-4-9B on MMLU-Pro and GSM8K via vLLM
python run.py --models hf_gemma_4_9b --datasets mmlu_pro_gen gsm8k_gen --acceleration vllm
```

## CLI examples
OpenCompass provides a powerful CLI for managing evaluations:

```bash
# Run evaluation with vLLM acceleration and streaming JSON progress
python run.py --models hf_gemma_4_9b --datasets mmlu_pro_gen --acceleration vllm --stream-json

# Summarize results from a completed evaluation run
python tools/summarize.py outputs/default/20270107_120000

# Run multimodal vision evaluation
python GenEditEvalKit/run.py --models stable-diffusion-4 --benchmarks GEdit2027
```

## API examples
OpenCompass configurations are native Python modules and can be integrated into automated training and evaluation pipelines:

```python
from mmengine.config import read_base
from opencompass.models import HuggingFaceCausalLM

with read_base():
    from .datasets.mmlu_pro.mmlu_pro_gen import mmlu_pro_datasets

models = [
    dict(
        type=HuggingFaceCausalLM,
        abbr='gemma-4-9b-hf',
        path='google/gemma-4-9b-it',
        model_kwargs=dict(device_map='auto'),
        max_seq_len=16384,
        max_out_len=2048,
        batch_size=32,
        run_cfg=dict(num_gpus=1),
    )
]
datasets = mmlu_pro_datasets
```

## Programmatic Integration and Validation Example
This Python example executes a local OpenCompass evaluation job and utilizes Pydantic v2 to strictly validate evaluation metrics and schema parameters before saving them to a telemetry store.

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

        # Enforce strict Pydantic v2 validation
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
    result = run_opencompass_and_validate("hf_gemma_4_9b", "gsm8k_gen")
    if result:
        print(f"Successfully validated OpenCompass metrics for model: {result.model_name}")
        for m in result.metrics:
            print(f"  - Dataset '{result.dataset_name}' metric '{m.metric_name}': {m.score}")
```

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md) — Alternative open-source evaluation framework.
- [HELM](helm.md) — Holistic evaluation by Stanford.
- [JudgeGPT](judgegpt.md) — LLM-as-a-judge evaluation harness.
- [vLLM](../infrastructure/vllm.md) — High-throughput inference engine integrated with OpenCompass.
- [RAGAS](../process_understanding/ragas.md) — Specialized RAG evaluation framework.
- [Gemma 4](../ai_knowledge/local_llms.md) — Frontier local model frequently benchmarked with OpenCompass.
- [LiteLLM](../../services/litellm.md) — Unified inference proxy for API-based model evaluation.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Integration standard for agentic benchmarking.

## Sources / references
- [Official Website](https://opencompass.org.cn/)
- [GitHub Repository](https://github.com/open-compass/opencompass)
- [OpenCompass Documentation](https://opencompass.readthedocs.io/en/latest/)
- [GenEditEvalKit Release](https://github.com/open-compass/GenEditEvalKit)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
