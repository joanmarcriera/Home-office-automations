# ASDiv (Academia Sinica Diverse MWP Dataset)

## What it is
ASDiv is a diverse corpus of 2,305 English Math Word Problems (MWPs) designed for evaluating the natural language understanding and problem-solving capabilities of AI solvers. It is structured to provide high diversity in both linguistic expression and mathematical problem types.

## What problem it solves
Many existing MWP datasets suffer from limited diversity in language patterns or problem types, often allowing models to "cheat" by learning statistical shortcuts or over-fitting to specific phrasing. ASDiv provides a broader range of text patterns and covers most problem types taught in elementary school, requiring actual semantic understanding to solve.

## Where it fits in the stack
ASDiv belongs to the **Benchmarking** category, specifically focusing on mathematical reasoning and lexicon usage diversity. It is a key metric for validating that a model's math performance isn't just memorization of common problem phrasings.

## Typical use cases
- Benchmarking LLMs on elementary-level mathematical reasoning.
- Developing and testing specialized Math Word Problem (MWP) solvers.
- Measuring the robustness of NLU systems against varied linguistic expressions of math problems.
- Validating "Chain of Thought" (CoT) prompting effectiveness across varied problem structures.

## Strengths
- **High Diversity**: Features a wide range of vocabulary and sentence structures (Lexicon diversity).
- **Detailed Annotation**: Each problem is annotated with its specific type (e.g., addition, subtraction, division) and difficulty grade.
- **Semantic Mapping**: Designed to test if models can map natural language to formal mathematical operations (Equation Generation).
- **Lexicon Metric**: Includes a proposed metric for measuring the diversity of MWP corpora.

## Limitations
- **Scope**: Limited to elementary school mathematics (K-6 level).
- **Language**: Only available in English.
- **Scale**: Smaller than some newer, synthetic datasets, though more diverse in its manual construction.

## When to use it
- Use ASDiv to verify that a model can handle varied phrasing in math problems without relying on superficial pattern matching.
- When you want to specifically test "Word Problem" solving rather than pure arithmetic.

## When not to use it
- Do not use it for evaluating high-level mathematics (calculus, linear algebra).
- When a large-scale, million-problem dataset is needed for training (use GSM8K or synthetic datasets instead).

## Technical examples

### Running Evaluation (LM Eval Harness)
ASDiv is supported by the `lm-evaluation-harness`.

```bash
# Run ASDiv evaluation
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-3-8B \
    --tasks asdiv \
    --device cuda:0 \
    --num_fewshot 5
```

### Problem Diversity example
ASDiv contains problems that test logic beyond the numbers:

> "If a recipe calls for 3 cups of flour and 2 cups of sugar, how many more cups of flour than sugar are needed?"
> *Tests: Comparative subtraction.*

> "There are 5 birds on a wire. 2 more fly in. Then 3 fly away. How many birds remain?"
> *Tests: Multi-step sequential arithmetic.*

## Licensing and cost
- **Open Data**: Yes (MIT license for the dataset tools).
- **Cost**: Free to download and use.

## Related tools / concepts
- [GSM8K](../benchmarking/gsm8k.md)
- [Math Benchmark](math-benchmark.md)
- [HumanEval](../benchmarking/human-eval.md)
- [MMLU](../benchmarking/mmlu.md)
- [GPQA](../benchmarking/gpqa.md)
- [OpenCompass](../benchmarking/opencompass.md)
- [HELM](../benchmarking/helm.md)
- [DREAM](../benchmarking/dream.md)

## Sources / references
- [ASDiv GitHub Repository](https://github.com/chiahsuan/ASDiv)
- [ASDiv: A Diverse Corpus for Math Word Problem Solving (ACL 2020)](https://aclanthology.org/2020.acl-main.92.pdf)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high
