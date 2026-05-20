# AlpacaEval

## What it is
AlpacaEval is an automatic evaluator for instruction-following language models. It is designed to be fast, cheap, and highly correlated with human preferences. It measures the win rate of a model's outputs against a reference model (typically GPT-4 or GPT-4 Turbo) using an LLM-based automatic annotator.

## What problem it solves
Evaluation of instruction-following models typically requires human interaction, which is time-consuming, expensive, and difficult to replicate. AlpacaEval provides a replicable, automated proxy that allows developers to iterate quickly on model development by simulating human preference judgments.

## Where it fits in the stack
**Benchmarking**. It serves as a middle-ground evaluation tool between static, objective benchmarks (like MMLU) and slow, expensive human evaluations (like Chatbot Arena).

## Typical use cases
- **Model Development**: Running frequent evaluations during the training or fine-tuning process.
- **Comparative Analysis**: Measuring how a new model performs against established baselines like GPT-4.
- **Prompt Engineering**: Testing the impact of different system prompts on model performance.

## Getting started

### 1. Installation
```bash
pip install alpaca_eval
```

### 2. Configuration
Set your API key for the evaluator model (e.g., OpenAI API for GPT-4).

```bash
export OPENAI_API_KEY="your_api_key"
```

### 3. Running an Evaluation
AlpacaEval requires a JSON or JSONL file containing the model's outputs for the evaluation set.

```bash
# Evaluate your model outputs
alpaca_eval --model_outputs 'path/to/your_model_outputs.json'
```

## Technical Methodology
AlpacaEval 2.0 uses a length-controlled win rate to address the "verbosity bias" where LLMs (and humans) tend to prefer longer, more detailed responses regardless of quality.
- **Reference Outputs**: Uses a gold standard set of responses from a strong model (GPT-4 Turbo).
- **Annotator**: A powerful LLM (the "judge") is given the prompt and two anonymized responses, then asked to pick the better one.
- **LC Win Rate**: Applies a statistical correction to ensure models aren't rewarded just for being wordy.

## Leaderboard Integration
Results are typically compared against the [official AlpacaEval leaderboard](https://tatsu-lab.github.io/alpaca_eval/), which ranks both open-source and proprietary models.
- **Verified vs. Unverified**: Official rankings are verified by the Tatsu Lab team, but users can run local "unverified" evals for internal benchmarking.

## CLI Reference
Commonly used arguments for the `alpaca_eval` command:
- `--model_outputs`: Path to the JSON file with model responses.
- `--reference_outputs`: (Optional) Path to custom reference responses.
- `--annotator_config`: Configuration for the judge model (defaults to `weighted_alpaca_eval_gpt4_turbo`).
- `--output_path`: Where to save the evaluation summary and individual judgments.

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

## Strengths
- **Speed and Cost**: Can run in less than 5 minutes for under $10.
- **Human Correlation**: AlpacaEval 2.0 has a 0.98 Spearman correlation with Chatbot Arena.
- **Length Normalization**: Effectively mitigates the bias toward longer outputs.
- **Reproducibility**: Uses fixed evaluation sets and cached annotations.

## Limitations
- **Style over Substance**: Like many LLM-based evaluators, it may favor the style and tone of a response over its factual accuracy.
- **Instruction Breadth**: The evaluation set might not be representative of extremely complex or niche professional tasks.
- **Safety**: It does not measure model safety, toxicity, or potential for harm.

## When to use it
- When you need quick, automated feedback on model quality during development.
- When you want to see how a model's conversational performance aligns with human-perceived quality.

## When not to use it
- For high-stakes decisions regarding model safety or final production release.
- When you need to evaluate specific technical domains (e.g., medical, legal) that require expert verification.

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md) - The "ground truth" human preference leaderboard.
- [MT-Bench](mt-bench.md) - Multi-turn conversation benchmark.
- [MMLU](mmlu.md) - Knowledge-based benchmark.
- [GPQA](gpqa.md) - Expert-level reasoning benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Framework for running many benchmarks, including objective ones.
- [OpenCompass](opencompass.md) - Comprehensive evaluation platform that integrates AlpacaEval.
- [HELM](helm.md) - Holistic evaluation framework.

## Sources / references
- [GitHub Repository](https://github.com/tatsu-lab/alpaca_eval)
- [AlpacaEval 2.0 Paper (Dubois et al., 2024)](https://arxiv.org/abs/2404.04475)
- [AlpacaFarm Project](https://github.com/tatsu-lab/alpaca_farm)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
