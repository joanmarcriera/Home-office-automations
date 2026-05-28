# OpenCompass

## What it is
OpenCompass is a comprehensive, one-stop platform designed for evaluating the capabilities of large language models (LLMs) and vision-language models (VLMs). It provides a complete evaluation pipeline, including dataset preparation, evaluation scripts, and leaderboards.

## What problem it solves
Evaluating modern large models is complex, requiring diverse datasets and multiple evaluation paradigms (e.g., zero-shot, few-shot, CoT). OpenCompass standardizes this process, providing a reproducible and extensible framework that supports over 100 datasets and various model backends.

## Where it fits in the stack
**Benchmarking**. It serves as an evaluation toolkit and platform for comparing model performance across a wide range of tasks.

## Typical use cases
- **Model Development**: Benchmarking in-house models against industry standards during training.
- **Model Selection**: Comparing different open-source or API-based models to find the best fit for a specific application.
- **Academic Research**: Reproducing evaluation results for papers and contributing new datasets to the community.

## Strengths
- **Comprehensive Coverage**: Supports 100+ datasets covering linguistics, knowledge, reasoning, coding, and multi-modality.
- **Flexible Architecture**: Supports various evaluation paradigms (Zero-shot, Few-shot, CoT, LLM-as-a-judge).
- **High Performance**: Integrates with acceleration backends like vLLM, LMDeploy, and ModelScope for distributed evaluation.
- **VLM Leadership**: First-class support for Vision-Language Models, including InternVL-U and InternVL2 series.
- **Judger-Aided Evaluation**: Built-in integration with CompassJudger for reliable, automated LLM-as-a-judge workflows.

## Limitations
- **Complexity**: The extensive configuration options and features can lead to a steeper learning curve for beginners.
- **Resource Intensive**: Running full-scale evaluations on large models requires significant local compute or API credits.

## When to use it
- When you need a standardized, reproducible way to evaluate models across dozens of different dimensions.
- When you want to contribute to or compare against public leaderboards (CompassRank).
- When evaluating Vision-Language Models (VLMs) alongside LLMs.

## When not to use it
- For very simple, single-task evaluations where a lightweight script might suffice.
- If you only need to evaluate basic RAG performance (consider [DeepEval](https://github.com/confident-ai/deepeval) or [RAGAS](https://github.com/explodinggradients/ragas) instead).

## Getting started
1. **Installation**:
   ```bash
   conda create --name opencompass python=3.10 -y
   conda activate opencompass
   git clone https://github.com/open-compass/opencompass.git
   cd opencompass
   pip install -e .
   ```
2. **Dataset Preparation**:
   ```bash
   # Download datasets to data/ directory
   wget https://github.com/open-compass/opencompass/releases/download/0.1.0/OpenCompassData-core-20231110.zip
   unzip OpenCompassData-core-20231110.zip
   ```
3. **Hello-world Evaluation**:
   ```bash
   # Evaluate Opt-125m on MMLU and GSM8K
   python run.py --models hf_opt_125m --datasets mmlu_gen gsm8k_gen
   ```

## Configuration example (Python-style)
OpenCompass uses MMEngine's configuration system. Below is an example for evaluating a HuggingFace model:

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
        abbr='llama-7b-hf',
        path='huggyllama/llama-7b',
        tokenizer_path='huggyllama/llama-7b',
        model_kwargs=dict(device_map='auto'),
        max_seq_len=2048,
        max_out_len=100,
        batch_size=16,
        run_cfg=dict(num_gpus=1),
    )
]
```

## API-based model evaluation
To evaluate an API-based model (e.g., OpenAI), use the following configuration:

```python
from opencompass.models import OpenAI

models = [
    dict(
        type=OpenAI,
        path='gpt-4o',
        key='YOUR_OPENAI_API_KEY',
        abbr='gpt-4o',
        query_per_second=1,
        max_out_len=1024,
        max_seq_len=2048,
        batch_size=8,
    )
]
```

## CLI Reference
Commonly used CLI arguments for `run.py`:
- `--models`: Specify model names (from `configs/models/`).
- `--datasets`: Specify dataset names (from `configs/datasets/`).
- `--work-dir`: Directory to save evaluation results.
- `--mode`: `inference` for only running model, `evaluation` for calculating metrics, or `full` for both.
- `--reuse`: Resume from a previous checkpoint.

## Advanced Evaluation Kits (2026)

### GenEditEvalKit
Introduced in May 2026, the **GenEditEvalKit** provides a specialized pipeline for evaluating AI-driven image and video editing models. It includes metrics for temporal consistency (for video), instruction-following accuracy, and visual quality preservation.

### CompassJudger
**CompassJudger** is a purpose-built "judge" model (based on InternLM) optimized specifically for scoring other models' outputs. It reduces the bias and cost associated with using proprietary models like GPT-4o for evaluation tasks.

```bash
# Example: Use CompassJudger to evaluate a model's open-ended responses
python run.py --models llama-3-8b --datasets open-ended-v1 --judge compass-judger-v2
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [HELM](helm.md)
- [vLLM](../infrastructure/vllm.md)
- [Chatbot Arena](chatbot-arena.md)
- [MMLU](mmlu.md)
- [GSM8K](gsm8k.md)
- [HumanEval](human-eval.md)
- [MBPP](mbpp.md)
- [BigCodeBench](bigcodebench.md)

## Sources / References
- [Official Website](https://opencompass.org.cn/)
- [GitHub Repository](https://github.com/open-compass/opencompass)
- [Introduction by Jimmy Song](https://jimmysong.io/ai/opencompass/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
