# AssistantBench

## What it is
AssistantBench is a benchmark designed to evaluate whether web agents can solve realistic, time-consuming, and multi-step tasks on the open web.

## What problem it solves
It addresses the limitation of benchmarks that focus on atomic actions or single-site interactions. AssistantBench provides 214 tasks that require agents to navigate multiple websites, retrieve information, and reason over it to find answers that a human would typically find "time-consuming."

## Where it fits in the stack
**Eval**. It serves as a rigorous testing ground for web-connected agents and browser-based automation systems.

## Typical use cases
- **Web Agent Evaluation**: Testing the reliability of agents like OpenHands, Multi-On, or custom Playwright-based agents.
- **Information Retrieval**: Measuring the ability to synthesize data from diverse web sources (e.g., real estate, business listings).
- **Long-Horizon Planning**: Evaluating how agents handle tasks that take 10+ minutes for a human.

## Strengths
- **Realistic Tasks**: Based on actual queries humans perform on the web.
- **Multi-domain**: Covers real estate, travel, business, and more.
- **Execution-based**: Evaluation is grounded in the final answer found on the live web.

## Limitations
- **Web Volatility**: Since it uses the live web, changes in site structure can affect reproducibility.
- **Latency**: Running full trajectories on the open web is slower than synthetic environments.

## When to use it
- When building agents intended for public web navigation.
- When you need to measure success on complex, multi-site "information seeking" missions.

## When not to use it
- For testing basic UI interaction (use a UI-specific benchmark like OSWorld).
- For evaluating models in a sandbox without internet access.

## Getting started

### Installation
AssistantBench is primarily used through the `inspect-ai` framework for evaluation.

```bash
pip install inspect-ai inspect-evals
```

### Hello-world example
To run a single sample of AssistantBench to verify your environment setup:

```bash
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-4o --limit 1
```

## CLI examples

### Run full evaluation
Execute the entire benchmark against a specific model:
```bash
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-4o
```

### Run with Anthropic Claude
Evaluate using a different provider:
```bash
inspect eval inspect_evals/assistant_bench_web_browser --model anthropic/claude-3-5-sonnet-20240620
```

### View evaluation results
Open the Inspect view to see detailed logs of the trajectories:
```bash
inspect view
```

## API examples

### Loading the dataset via Hugging Face
You can interact with the benchmark data directly using the `datasets` library.

```python
from datasets import load_dataset

# Load the development set
dataset = load_dataset("AssistantBench/AssistantBench", split="dev")

# Access a specific task
example = dataset[0]
print(f"Task: {example['task']}")
print(f"Answer: {example['answer']}")
```

## Related tools / concepts
- [PA-bench](./pa-bench.md)
- [GAIA](./gaia.md)
- [OSWorld](./os-world.md)
- [WebArena](https://webarena.dev/)
- [OpenHands](../development_ops/openhands.md)
- [Stagehand](../automation_orchestration/stagehand.md)

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free (benchmark), but requires internet access and LLM API credits.

## Sources / References
- [AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks? (ArXiv)](https://arxiv.org/abs/2407.15711)
- [AssistantBench Project Website](https://assistantbench.github.io/)
- [AssistantBench GitHub](https://github.com/assistantbench/assistantbench)

## Contribution Metadata

- Last reviewed: 2026-06-05
- Confidence: high
