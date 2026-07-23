# MBPP (Mostly Basic Python Problems)

## What it is
MBPP is a benchmark designed to evaluate the code generation performance of LLMs on basic Python tasks. It consists of approximately 1,000 crowd-sourced Python programming problems, designed to be solvable by entry-level programmers. Each problem includes a task description (prompt), a gold-standard code solution, and three automated test cases. It was introduced by Google Research in 2021 and remains a July 2026 baseline for agentic code generation.

## What problem it solves
Provides a large-scale, standardized evaluation of LLM code generation on "mostly basic" problems. While benchmarks like [HumanEval](human-eval.md) focus on algorithmic complexity, MBPP covers a broader range of fundamental programming concepts, standard library usage, and common data structure manipulations. It is a key metric for "Satisfaction-Based Validation" in July 2026 agentic software factories.

## Where it fits in the stack
**Benchmarking**. Used as a primary code-generation benchmark for evaluating and comparing the Python coding capabilities of LLMs within agentic ingestion pipelines.

## Typical use cases
- **Model Comparison**: Measuring the `Pass@1` and `Pass@k` metrics of new models (e.g., Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6, DeepSeek R1/V4) against industry baselines.
- **Fine-tuning Evaluation**: Verifying that a model fine-tuned on code datasets (e.g., StarCoder 2026) has improved on basic programming tasks.
- **Contamination Testing**: Using the "sanitized" version of the dataset to ensure results haven't been inflated by training data leakage—a critical requirement in July 2026.
- **Agent Skill Validation**: Testing the core Python proficiency of autonomous agents before they are granted repository access.

## Strengths
- **Large Dataset**: With ~1,000 problems, it offers higher statistical confidence than smaller benchmarks like HumanEval.
- **Automated Verification**: Each problem comes with executable test cases, ensuring objective, satisfaction-based scoring.
- **Sanitized Subset**: A subset of the data has been hand-verified and "sanitized" to remove ambiguous or low-quality problems.
- **Realistic Basics**: Focuses on tasks a junior developer or agent would perform, rather than just "LeetCode-style" puzzles.

## Limitations
- **Basic Level**: Does not evaluate architectural reasoning, multi-file projects, or advanced software engineering patterns (use [SWE-bench](swe-bench.md) for that).
- **Python Only**: Limited to Python code generation.
- **Prompt Sensitivity**: Results can vary based on the exact prompt format and "Thought" chain-of-thought (CoT) used by models like DeepSeek R1.
- **Saturation**: High-end July 2026 models are reaching near 100% on MBPP, necessitating more difficult benchmarks like BigCodeBench.

## When to use it
- When evaluating the fundamental Python coding ability of a model or agent.
- When you need a statistically robust code benchmark that is larger than HumanEval.
- When assessing a model's familiarity with the Python standard library in July 2026.

## When not to use it
- When evaluating complex, real-world software engineering or repository-wide changes (use [SWE-bench](swe-bench.md) or [BigCodeBench](bigcodebench.md)).
- When testing non-Python languages (use MultiPL-E or similar).
- When evaluating high-level agentic planning that isn't captured by "basic" problems.

## Getting started

MBPP is typically run through evaluation frameworks like the **LM Evaluation Harness** or **EvalPlus**. In July 2026, it is often integrated into agentic CI/CD pipelines.

### 1. Installation
```bash
# Install via LM Evaluation Harness
pip install "lm_eval[hf,vllm]"
```

### 2. Basic Run
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-8b \
    --tasks mbpp \
    --batch_size auto
```

## CLI examples

### Evaluating a Sanitized Subset with Device Mapping
```bash
lm_eval --model hf \
    --model_args pretrained=EleutherAI/pythia-160m \
    --tasks mbpp_sanitized \
    --device cuda:0 \
    --limit 100
```

### Running with LiteLLM Proxy and Temperature Control
```bash
lm_eval --model openai-completions \
    --model_args model=gpt-5-5,base_url=http://localhost:4000,temperature=0.0 \
    --tasks mbpp \
    --limit 100
```

### Hardening MBPP Evaluators via EvalPlus CLI
To minimize the chance of false positives, execute EvalPlus-enhanced test sweeps:
```bash
evalplus.evaluate \
    --dataset mbpp \
    --samples ./agent_responses.jsonl \
    --parallel 16 \
    --i-choose-danger
```

## API examples

### Programmatic Evaluation (Python)
Automate MBPP scoring within a July 2026 agentic workbench.

```python
import lm_eval
from lm_eval.models.huggingface import HFLM

# Initialize model (e.g., for local verification)
model = HFLM(pretrained="deepseek-ai/deepseek-coder-7b-v1.5")

# Run evaluation on MBPP
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["mbpp_sanitized"],
    num_fewshot=3,
    batch_size=16,
    limit=50
)

# Extract Pass@1 score
pass_at_1 = results['results']['mbpp_sanitized']['pass@1']
print(f"DeepSeek MBPP Pass@1: {pass_at_1:.2%}")
```

### Using EvalPlus for "Hardened" MBPP
EvalPlus adds thousands of extra test cases to MBPP to detect "fluke" passes.

```python
from evalplus.data import get_mbpp
from evalplus.evaluate import evaluate

# Get hardened MBPP tasks
tasks = get_mbpp()

# Evaluate generated samples (e.g., from an agent)
results = evaluate(
    dataset="mbpp",
    samples="my_agent_samples.jsonl",
    test_setup="evalplus",
    parallel=8
)
print(f"EvalPlus Hardened MBPP Score: {results['pass@1']}")
```

## Related tools / concepts

- [HumanEval](human-eval.md) - The algorithmic Python code benchmark.
- [EvalPlus](evalplus.md) - Framework for hardening MBPP with extra test cases.
- [SWE-bench](swe-bench.md) - Real-world agentic software engineering benchmark.
- [BigCodeBench](bigcodebench.md) - A modern, more difficult code benchmark for July 2026.
- [LM Evaluation Harness](lm-evaluation-harness.md) - The primary runner for MBPP.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - High-difficulty reasoning benchmark.
- [DeepSeek R1](../../knowledge_base/self-healing-agent-research.md) - Benchmarking leader for code reasoning in July 2026.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) - Context for "Satisfaction-Based Validation".
- [LiveCodeBench](livecodebench.md) - Contamination-free coding benchmark.
- [MultiPL-E](multipl-e.md) - Multi-language coding benchmark.

## Sources / references
- [MBPP GitHub Repository (Google Research)](https://github.com/google-research/google-research/tree/master/mbpp)
- [Program Synthesis with Large Language Models (Austin et al., 2021)](https://arxiv.org/abs/2108.07732)
- [Hugging Face Dataset (mbpp)](https://huggingface.co/datasets/mbpp)
- [EvalPlus: Hardening Code Benchmarks](https://github.com/evalplus/evalplus)

- Last reviewed: 2026-07-23
- Confidence: high
