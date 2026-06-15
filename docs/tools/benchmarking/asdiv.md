# ASDiv (Academia Sinica Diverse MWP Dataset)

## What it is
ASDiv is a diverse corpus of 2,305 English Math Word Problems (MWPs) designed for evaluating the natural language understanding and problem-solving capabilities of AI solvers. As of June 2026, it remains a foundational benchmark for measuring the semantic reasoning of frontier models like `claude-4-8-opus-20260528` and GPT-5.5. It is structured to provide high diversity in both linguistic expression and mathematical problem types, specifically targeting the "lexicon" variety that often trips up less robust models.

## What problem it solves
Many existing MWP datasets suffer from limited diversity in language patterns or problem types, often allowing models to "cheat" by learning statistical shortcuts or over-fitting to specific phrasing. ASDiv provides a broader range of text patterns and covers most problem types taught in elementary school (K-6), requiring actual semantic understanding to map natural language descriptions to formal mathematical operations.

## Where it fits in the stack
ASDiv belongs to the **Benchmarking** category, specifically focusing on mathematical reasoning and lexicon usage diversity. It acts as a specialized check within an evaluation suite, alongside broader benchmarks like [MMLU](../benchmarking/mmlu.md) and [GSM8K](../benchmarking/gsm8k.md).

## Typical use cases
- **Frontier Model Evaluation**: Benchmarking Claude 4.8 and GPT-5.5 on elementary-level mathematical reasoning.
- **Robustness Testing**: Measuring how variations in linguistic phrasing affect a model's ability to solve math problems.
- **Specialized Solver Development**: Training and testing specialized Math Word Problem (MWP) solvers.
- **Prompt Engineering**: Validating the effectiveness of "Chain of Thought" (CoT) and "System 2" reasoning prompts across varied problem structures.

## Strengths
- **High Diversity**: Features a wide range of vocabulary and sentence structures (Lexicon diversity).
- **Detailed Annotation**: Each problem is annotated with its specific type (e.g., addition, subtraction, division) and difficulty grade.
- **Semantic Mapping**: Designed to test if models can map natural language to formal mathematical operations (Equation Generation).
- **Open Access**: Distributed under the MIT license, making it freely available for research and commercial evaluation.

## Limitations
- **Scope**: Limited to elementary school mathematics (K-6 level).
- **Language**: Primarily available in English.
- **Scale**: Smaller than some newer, synthetic datasets (2,305 problems), though more diverse in its manual construction than many larger alternatives.

## When to use it
- Use ASDiv to verify that a model can handle varied phrasing in math problems without relying on superficial pattern matching.
- When you want to specifically test "Word Problem" solving rather than pure arithmetic or high-level calculus.
- When performing technical freshness audits of model reasoning capabilities in June 2026.

## When not to use it
- Do not use it for evaluating high-level mathematics (calculus, linear algebra).
- When a large-scale, million-problem dataset is needed for training (use synthetic datasets or larger corpora instead).
- For evaluating non-English mathematical reasoning.

## Getting started
ASDiv can be accessed directly from its GitHub repository or via the Hugging Face `datasets` library.

```bash
# Clone the repository
git clone https://github.com/chiahsuan/ASDiv.git
```

Or install the datasets library:
```bash
pip install datasets
```

## CLI examples
ASDiv is commonly evaluated using the `lm-evaluation-harness`.

```bash
# Run ASDiv evaluation for a local model
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-maverick-8B \
    --tasks asdiv \
    --device cuda:0 \
    --num_fewshot 5
```

```bash
# Check the task structure
lm_eval --tasks asdiv --print_config
```

## API examples
Loading ASDiv via Python for custom evaluation loops or dataset analysis.

```python
from datasets import load_dataset

# Load the ASDiv dataset
dataset = load_dataset("asdiv")

# Inspect a problem
print(dataset['test'][0]['question'])
print(dataset['test'][0]['answer'])
print(dataset['test'][0]['formula'])

# Filter for specific problem types (e.g., Multiplication)
multiplication_probs = [p for p in dataset['test'] if 'Multiplication' in p['type']]
print(f"Found {len(multiplication_probs)} multiplication problems.")
```

## Related tools / concepts
- [GSM8K](../benchmarking/gsm8k.md) — Grade school math benchmark.
- [Math Benchmark](math-benchmark.md) — Comprehensive mathematics evaluation suite.
- [MMLU](../benchmarking/mmlu.md) — Massive Multitask Language Understanding.
- [DREAM](../benchmarking/dream.md) — Deep Research Evaluation with Agentic Metrics.
- [Claude 4.8 Opus](../../knowledge_base/patterns/claude-4-8-patterns.md) — Frontier model often benchmarked with ASDiv.

## Sources / references
- [ASDiv GitHub Repository](https://github.com/chiahsuan/ASDiv)
- [ASDiv: A Diverse Corpus for Math Word Problem Solving (ACL 2020)](https://aclanthology.org/2020.acl-main.92.pdf)
- [Hugging Face ASDiv Dataset Card](https://huggingface.co/datasets/asdiv)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
