# OpenCompass

## What it is
OpenCompass is a comprehensive, one-stop platform designed for evaluating the capabilities of large language models (LLMs) and vision-language models (VLMs). It provides a complete evaluation pipeline, including dataset preparation, evaluation scripts, and leaderboards. In June 2026, it remains the standard for open-source model benchmarking in the research community.

## What problem it solves
Evaluating modern large models is complex, requiring diverse datasets and multiple evaluation paradigms (e.g., zero-shot, few-shot, CoT). OpenCompass standardizes this process, providing a reproducible and extensible framework that supports over 100 datasets. It addresses the fragmentation of evaluation criteria by providing a unified interface for cross-domain and large-scale model evaluation, including the latest frontier models like Claude 4.8 and GPT-5.5.

## Where it fits in the stack
**Benchmarking Layer**. It serves as an evaluation toolkit and platform for comparing model performance across a wide range of tasks, including linguistic, knowledge, reasoning, coding, and multi-modality.

## Typical use cases
- **Model Development**: Benchmarking in-house models against industry standards (e.g., Qwen 4, InternVL 3) during training.
- **Model Selection**: Comparing different open-source or API-based models (GPT-5.5, Claude 4.8) to find the best fit for a specific agentic application.
- **VLM & Image Evaluation**: Using the **GenEditEvalKit** to evaluate image generation and editing models across multiple benchmarks.
- **Agentic Evaluation**: Measuring model performance on multi-step reasoning tasks using the **CompassAgent** suite.

## Strengths
- **Comprehensive Coverage**: Supports 100+ datasets, including IFEval, MMLU-Pro, and GPQA.
- **Flexible Architecture**: Supports multiple evaluation paradigms, including Zero-shot, Few-shot, CoT, and **LLM-as-a-judge** (CompassJudger).
- **High Concurrency**: Integrates with acceleration backends like [vLLM](../infrastructure/vllm.md), LMDeploy, and ModelScope for distributed, high-speed evaluation.
- **Unified Multimodal Support**: Enhanced support for Unified Multimodal Models (UMMs) and vision-language tasks.
- **MCP 3.0 Support**: (2026 update) Allows agents to trigger and monitor evaluation runs via the Model Context Protocol.

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
# Download core datasets (June 2026 baseline)
python tools/download_dataset.py --dataset core
```

### Hello-world Evaluation
Evaluate a small model (e.g., Llama-4-8B) on standard benchmarks:

```bash
# Evaluate Llama-4-8B on MMLU and GSM8K
python run.py --models hf_llama_4_8b --datasets mmlu_gen gsm8k_gen
```

## CLI examples
OpenCompass provides a powerful CLI for running and managing evaluations:

```bash
# Run evaluation with vLLM acceleration
python run.py --models hf_llama_4_8b --datasets mmlu_gen --acceleration vllm

# Summarize results from a previous run
python tools/summarize.py outputs/default/20260620_100000

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
        abbr='llama-4-8b-hf',
        path='meta-llama/Llama-4-8B-Instruct',
        model_kwargs=dict(device_map='auto'),
        max_seq_len=8192,
        max_out_len=1024,
        batch_size=32,
        run_cfg=dict(num_gpus=1),
    )
]
datasets = mmlu_datasets
```

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md) — Alternative evaluation framework.
- [HELM](helm.md) — Holistic evaluation by Stanford.
- [vLLM](../infrastructure/vllm.md) — High-throughput inference engine often used with OpenCompass.
- [Ragas](../process_understanding/ragas.md) — Specialized RAG evaluation.
- [MMLU](mmlu.md) — Standard knowledge benchmark.
- [GSM8K](gsm8k.md) — Standard math reasoning benchmark.
- [LiteLLM](../../services/litellm.md) — Inference proxy for API-based model evaluation.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Integration standard for agentic benchmarking.

## Sources / references
- [Official Website](https://opencompass.org.cn/)
- [GitHub Repository](https://github.com/open-compass/opencompass)
- [OpenCompass Documentation](https://opencompass.readthedocs.io/en/latest/)
- [GenEditEvalKit Release](https://github.com/open-compass/GenEditEvalKit)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
