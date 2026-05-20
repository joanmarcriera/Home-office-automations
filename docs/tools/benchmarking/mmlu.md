# MMLU (Massive Multitask Language Understanding)

## What it is
MMLU is a comprehensive benchmark designed to measure the general knowledge and problem-solving abilities of Large Language Models. It consists of approximately 16,000 multiple-choice questions across 57 subjects, including STEM, the humanities, social sciences, and more.

## What problem it solves
It provides a standardized way to evaluate a model's "world knowledge" and academic proficiency across a vast array of disciplines, moving beyond narrow tasks to assess broad intellectual capability.

## Where it fits in the stack
**Benchmarking**. It is one of the most widely cited benchmarks for comparing the general intelligence of different LLMs.

## Typical use cases
- **General Model Comparison**: Assessing which model has a broader knowledge base.
- **Tracking Progress**: Measuring how new model versions improve in general world knowledge.
- **Identifying Knowledge Gaps**: Analyzing performance across specific subjects (e.g., Law vs. Physics).

## Strengths
- **Breadth**: Covers a massive range of subjects, from elementary mathematics to professional law and medicine.
- **Industry Standard**: Almost every major LLM release includes MMLU scores.
- **Granularity**: Allows for fine-grained analysis of performance on specific topics.

## Limitations
- **Format**: Multiple-choice format doesn't capture open-ended reasoning or generation quality.
- **Data Contamination**: Due to its popularity, questions may have leaked into the training data of newer models.
- **Ambiguity**: Some questions and answers have been criticized for being ambiguous or containing errors.

## Technical Details
MMLU consists of **15,908 questions** across **57 subjects**. The standard evaluation methodology is **5-shot prompting**, where the model is given five example questions and answers before being asked the target question. Performance is measured using a simple accuracy metric (percentage of correct answers).

The benchmark is often divided into four high-level categories:
1. **STEM**: 19 subjects (e.g., Abstract Algebra, Anatomy, Computer Science).
2. **Humanities**: 13 subjects (e.g., Prehistory, World Religions, Philosophy).
3. **Social Sciences**: 14 subjects (e.g., Economics, Psychology, Sociology).
4. **Other (Business, Health, Misc)**: 11 subjects (e.g., Marketing, Professional Medicine, Management).

## Getting started

### Installation (via LM Evaluation Harness)
The easiest way to run MMLU is using the [LM Evaluation Harness](lm-evaluation-harness.md).
```bash
pip install "lm_eval[hf,vllm]"
```

### Hello-world Evaluation
Run a subset of MMLU (e.g., elementary mathematics) on a small model to verify your setup:
```bash
lm_eval --model hf \
    --model_args pretrained=EleutherAI/pythia-160m \
    --tasks mmlu_elementary_mathematics \
    --device cuda:0 \
    --batch_size 8
```

## Advanced Examples

### Full MMLU Evaluation (CLI)
To run the full 57-subject benchmark using [vLLM](../infrastructure/vllm.md) for faster inference:
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-3-8b,tensor_parallel_size=1,dtype=auto \
    --tasks mmlu \
    --batch_size auto
```

### Evaluation via OpenCompass
[OpenCompass](opencompass.md) provides a more configurable way to run MMLU, especially for API-based models.
```bash
# Evaluate GPT-4o on MMLU
python run.py --models gpt-4o --datasets mmlu_gen
```

### Custom Python Evaluation
You can also use the `mmlu` dataset directly from Hugging Face:
```python
from datasets import load_dataset

# Load the 'abstract_algebra' subject
dataset = load_dataset("cais/mmlu", "abstract_algebra")
print(dataset['test'][0])
```

## When to use it
- When you want a broad overview of a model's general knowledge and academic proficiency.
- When comparing the general "intelligence" level of various foundation models.

## When not to use it
- When you need to evaluate specific reasoning depth (use [GPQA](gpqa.md) instead).
- When evaluating coding performance (use [HumanEval](human-eval.md) or [BigCodeBench](bigcodebench.md) instead).
- When evaluating math-specific reasoning (use [GSM8K](gsm8k.md) or [MATH Benchmark](math-benchmark.md) instead).

## Related tools / concepts
- [HELM](helm.md) - A holistic evaluation framework that includes MMLU.
- [LM Evaluation Harness](lm-evaluation-harness.md) - The standard tool for running MMLU.
- [OpenCompass](opencompass.md) - Another comprehensive evaluation platform.
- [GPQA](gpqa.md) - A much harder benchmark for expert-level knowledge.
- [HumanEval](human-eval.md) - Standard coding benchmark.
- [BigCodeBench](bigcodebench.md) - More complex coding benchmark.
- [GSM8K](gsm8k.md) - Grade school math benchmark.
- [Humanity's Last Exam (HLE)](humanitys-last-exam.md) - A frontier benchmark designed to follow MMLU.
- [ARC (AI2 Reasoning Challenge)](arc.md) - Reasoning-focused benchmark.
- [ASDiv](asdiv.md) - Adversarial math word problems.

## Sources / References
- [Original Paper: Measuring Massive Multitask Language Understanding (Hendrycks et al.)](https://arxiv.org/abs/2009.03300)
- [GitHub Repository (cais/mmlu)](https://github.com/hendrycks/test)
- [Hugging Face Dataset Card](https://huggingface.co/datasets/cais/mmlu)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high
