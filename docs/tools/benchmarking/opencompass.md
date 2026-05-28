# OpenCompass

## What it is
OpenCompass is a comprehensive, one-stop platform designed for evaluating the capabilities of large language models (LLMs) and vision-language models (VLMs). It provides a complete evaluation pipeline, including dataset preparation, evaluation scripts, and leaderboards.

## What problem it solves
Evaluating modern large models is complex, requiring diverse datasets and multiple evaluation paradigms (e.g., zero-shot, few-shot, CoT). OpenCompass standardizes this process, providing a reproducible and extensible framework that supports over 100 datasets and various model backends. It addresses the fragmentation of evaluation criteria by providing a unified interface for cross-domain and large-scale model evaluation.

## Where it fits in the stack
**Category**: [Benchmarking](index.md). It serves as an evaluation toolkit and platform for comparing model performance across a wide range of tasks, including linguistic, knowledge, reasoning, coding, and multi-modality.

## Typical use cases
- **Model Development**: Benchmarking in-house models against industry standards (e.g., Qwen 3.5, InternVL-U) during training.
- **Model Selection**: Comparing different open-source or API-based models (GPT-5.2, Claude 4.6) to find the best fit for a specific application.
- **VLM & Image Evaluation**: Using the **GenEditEvalKit** (released 2026) to evaluate image generation and editing models across multiple benchmarks.
- **Academic Research**: Reproducing evaluation results for papers and contributing new datasets to the community via the OpenCompass Academic Leaderboard.

## Strengths
- **Comprehensive Coverage**: Supports 100+ datasets, including IFEval, MMLU-Pro, and GPQA.
- **Flexible Architecture**: Supports multiple evaluation paradigms, including Zero-shot, Few-shot, CoT, and **LLM-as-a-judge** (CompassJudger).
- **High Concurrency**: Integrates with acceleration backends like [vLLM](../infrastructure/vllm.md), LMDeploy, and ModelScope for distributed, high-speed evaluation.
- **Unified Multimodal Support**: Enhanced support for Unified Multimodal Models (UMMs) and vision-language tasks.

## Limitations
- **Complexity**: The extensive configuration system (based on MMEngine) has a steep learning curve.
- **Resource Intensive**: Running full-scale evaluations on frontier models requires significant local compute or API credits.

## When to use it
- When you need a standardized, reproducible way to evaluate models across dozens of dimensions.
- For evaluating Vision-Language Models (VLMs) and image generation models.
- When contributing to or comparing against public leaderboards (CompassRank).

## When not to use it
- For very simple, single-task evaluations where a lightweight script might suffice.
- If you only need to evaluate basic RAG performance (consider [RAGAS](https://github.com/explodinggradients/ragas) or [DeepEval](https://github.com/confident-ai/deepeval)).

## Getting started

### Installation
It is recommended to use a Conda environment for dependency management.

```bash
conda create --name opencompass python=3.10 -y
conda activate opencompass
git clone https://github.com/open-compass/opencompass.git
cd opencompass
pip install -e .
```

### Dataset Preparation
Datasets are managed centrally in the `data/` directory.

```bash
# Download core datasets (2026 baseline)
python tools/download_dataset.py --dataset core
```

### Hello-world Evaluation
Evaluate a small model (e.g., Opt-125m) on standard benchmarks:

```bash
# Evaluate Opt-125m on MMLU and GSM8K
python run.py --models hf_opt_125m --datasets mmlu_gen gsm8k_gen
```

## Configuration example (Python-style)
OpenCompass uses a modular configuration system. Below is an example for evaluating a HuggingFace model:

```python
from mmengine.config import read_base
from opencompass.models import HuggingFaceCausalLM

with read_base():
    # Inherit dataset configurations
    from .datasets.mmlu.mmlu_gen import mmlu_datasets
    from .datasets.gsm8k.gsm8k_gen import gsm8k_datasets

datasets = [*mmlu_datasets, *gsm8k_datasets]

models = [
    dict(
        type=HuggingFaceCausalLM,
        abbr='llama-4-8b-hf',
        path='meta-llama/Llama-4-8B-Instruct',
        tokenizer_path='meta-llama/Llama-4-8B-Instruct',
        model_kwargs=dict(device_map='auto'),
        max_seq_len=4096,
        max_out_len=1024,
        batch_size=16,
        run_cfg=dict(num_gpus=1),
    )
]
```

## Advanced: Image Generation Evaluation (GenEditEvalKit)
Released in 2026, this kit allows evaluating image generation and editing models:

```bash
# Evaluate an image generation model on GenEdit benchmarks
python GenEditEvalKit/run.py --models stable-diffusion-3 --benchmarks GEdit
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free software (compute/API costs apply)

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [HELM](helm.md)
- [vLLM](../infrastructure/vllm.md)
- [Chatbot Arena](chatbot-arena.md)
- [MMLU](mmlu.md)
- [GSM8K](gsm8k.md)
- [HumanEval](human-eval.md)
- [BigCodeBench](bigcodebench.md)
- [LiteLLM](../../services/litellm.md)

## Sources / References
- [Official Website](https://opencompass.org.cn/)
- [GitHub Repository](https://github.com/open-compass/opencompass)
- [OpenCompass Documentation](https://opencompass.readthedocs.io/en/latest/)
- [GenEditEvalKit Release](https://github.com/open-compass/GenEditEvalKit)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
