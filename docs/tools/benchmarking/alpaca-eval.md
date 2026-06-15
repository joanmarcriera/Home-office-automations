# AlpacaEval

## What it is
AlpacaEval is an automatic evaluator for instruction-following language models. It is designed to be fast, cheap, and highly correlated with human preferences. As of June 2026, it serves as a critical performance baseline for models like Claude 4.8 Opus and GPT-5.5, measuring the win rate of a model's outputs against a reference model (typically GPT-4 Turbo or GPT-5.5) using an LLM-based automatic annotator.

## What problem it solves
Evaluation of instruction-following models typically requires human interaction, which is time-consuming, expensive, and difficult to replicate. AlpacaEval provides a replicable, automated proxy that allows developers to iterate quickly on model development by simulating human preference judgments. It specifically addresses "verbosity bias" through length-controlled metrics.

## Where it fits in the stack
**Benchmarking**. It serves as a middle-ground evaluation tool between static, objective benchmarks (like MMLU) and slow, expensive human evaluations (like Chatbot Arena).

## Typical use cases
- **Model Development**: Running frequent evaluations during the training or fine-tuning process.
- **Comparative Analysis**: Measuring how a new model performs against established baselines like Claude 4.8 or GPT-5.5.
- **Prompt Engineering**: Testing the impact of different system prompts on model performance.
- **Leaderboard Submission**: Providing verified results for the official AlpacaEval leaderboard.

## Strengths
- **Speed and Cost**: Can run in less than 5 minutes for under $10.
- **Human Correlation**: AlpacaEval 2.0 has a 0.98 Spearman correlation with Chatbot Arena.
- **Length Normalization**: Effectively mitigates the bias toward longer outputs using length-controlled win rates.
- **Reproducibility**: Uses fixed evaluation sets and cached annotations to ensure consistent results.

## Limitations
- **Style over Substance**: Like many LLM-based evaluators, it may favor the style and tone of a response over its factual accuracy.
- **Instruction Breadth**: The evaluation set might not be representative of extremely complex or niche professional tasks.
- **Safety**: It does not measure model safety, toxicity, or potential for harm.
- **Judge Bias**: The choice of "judge" model can influence the results.

## When to use it
- When you need quick, automated feedback on model quality during development.
- When you want to see how a model's conversational performance aligns with human-perceived quality.
- For initial screening of model checkpoints before human evaluation.

## When not to use it
- For high-stakes decisions regarding model safety or final production release.
- When you need to evaluate specific technical domains (e.g., medical, legal) that require expert verification.
- When evaluating non-instruction-following base models.

## Getting started

### 1. Installation
```bash
pip install alpaca_eval
```

### 2. Configuration
Set your API key for the evaluator model (e.g., OpenAI API for GPT-5.5 or Anthropic API for Claude 4.8).

```bash
export OPENAI_API_KEY="your_api_key"
```

### 3. Running an Evaluation
AlpacaEval requires a JSON or JSONL file containing the model's outputs for the evaluation set.

```bash
# Evaluate your model outputs
alpaca_eval --model_outputs 'path/to/your_model_outputs.json'
```

## CLI examples
Commonly used arguments for the `alpaca_eval` command:

```bash
# Basic evaluation
alpaca_eval --model_outputs 'outputs.json'

# Use a specific annotator (e.g., GPT-5.5)
alpaca_eval --model_outputs 'outputs.json' --annotator_config 'weighted_alpaca_eval_gpt5_5'

# Specify output directory
alpaca_eval --model_outputs 'outputs.json' --output_path './results'

# Evaluate against a custom reference
alpaca_eval --model_outputs 'outputs.json' --reference_outputs 'references.json'
```

## API examples
AlpacaEval can be used programmatically within Python workflows.

```python
from alpaca_eval import evaluate

# Perform evaluation programmatically
results = evaluate(
    model_outputs='path/to/your_model_outputs.json',
    annotator_config='weighted_alpaca_eval_gpt4_turbo',
    name='my_model_experiment'
)

# Print the win rate
print(f"Win rate: {results['win_rate']}%")
```

## Technical Methodology
AlpacaEval 2.0 uses a length-controlled win rate to address the "verbosity bias" where LLMs (and humans) tend to prefer longer, more detailed responses regardless of quality.
- **Reference Outputs**: Uses a gold standard set of responses from a strong model (GPT-4 Turbo or GPT-5.5).
- **Annotator**: A powerful LLM (the "judge") is given the prompt and two anonymized responses, then asked to pick the better one.
- **LC Win Rate**: Applies a statistical correction to ensure models aren't rewarded just for being wordy.

## Leaderboard Integration
Results are typically compared against the [official AlpacaEval leaderboard](https://tatsu-lab.github.io/alpaca_eval/), which ranks both open-source and proprietary models.
- **Verified vs. Unverified**: Official rankings are verified by the Tatsu Lab team, but users can run local "unverified" evals for internal benchmarking.

## Evaluation Data Format
Input file should be a list of dictionaries:
```json
[
  {
    "instruction": "Explain quantum entanglement to a 5-year-old.",
    "output": "Imagine you have two magic socks..."
  },
  {
    "instruction": "Write a Python function to sort a list.",
    "output": "def sort_list(my_list):\n    return sorted(my_list)"
  }
]
```

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md) - The "ground truth" human preference leaderboard.
- [MT-Bench](mt-bench.md) - Multi-turn conversation benchmark.
- [MMLU](mmlu.md) - Knowledge-based benchmark.
- [GPQA](gpqa.md) - Expert-level reasoning benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Framework for running many benchmarks.
- [OpenCompass](opencompass.md) - Comprehensive evaluation platform.
- [HELM](helm.md) - Holistic evaluation framework.
- [EvalPlus](evalplus.md) - Robust code generation testing.

## Sources / references
- [GitHub Repository](https://github.com/tatsu-lab/alpaca_eval)
- [AlpacaEval 2.0 Paper (Dubois et al., 2024)](https://arxiv.org/abs/2404.04475)
- [Official Leaderboard](https://tatsu-lab.github.io/alpaca_eval/)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
