# AssistantBench

## What it is
AssistantBench is a benchmark designed to evaluate whether web agents can solve realistic, time-consuming, and multi-step tasks on the open web. It is a core component of the June 2026 'Agentic Evaluation Standard' for general-purpose assistants.

## What problem it solves
It addresses the limitation of benchmarks that focus on atomic actions or single-site interactions. AssistantBench provides tasks that require agents to navigate multiple websites, retrieve information, and reason over it to find answers that a human would typically find "time-consuming." It helps quantify 'Agentic Latency' and success rates for long-horizon missions.

## Where it fits in the stack
**Eval**. It serves as a rigorous testing ground for web-connected agents and browser-based automation systems, frequently used to benchmark Claude 4.8 and GPT-5.5 performance in real-world environments.

## Typical use cases
- **Web Agent Evaluation**: Testing the reliability of agents like OpenHands, MultiOn, or custom Playwright-based agents.
- **Information Retrieval**: Measuring the ability to synthesize data from diverse web sources (e.g., real estate, business listings).
- **Long-Horizon Planning**: Evaluating how agents handle tasks that take 10+ minutes for a human.
- **VLM Grounding**: Testing how well vision-language models can interpret complex, dynamic web interfaces.

## Strengths
- **Realistic Tasks**: Based on actual queries humans perform on the web.
- **Multi-domain**: Covers real estate, travel, business, and more.
- **Execution-based**: Evaluation is grounded in the final answer found on the live web.
- **Standardized Integration**: Native support for the `inspect-ai` framework.

## Limitations
- **Web Volatility**: Since it uses the live web, changes in site structure can affect reproducibility.
- **Latency**: Running full trajectories on the open web is slower than synthetic environments.
- **Cost**: High token usage for long-horizon agents navigating multiple sites.

## When to use it
- When building agents intended for public web navigation.
- When you need to measure success on complex, multi-site "information seeking" missions.
- To compare the efficiency of different planning architectures (e.g., ReAct vs. Agentic RAG).

## When not to use it
- For testing basic UI interaction (use a UI-specific benchmark like OSWorld).
- For evaluating models in a sandbox without internet access.
- For high-speed regression testing where deterministic results are required.

## Getting started
AssistantBench is integrated into the `inspect-ai` framework via the `inspect-evals` package.

### 1. Installation
```bash
pip install inspect-ai inspect-evals
```

### 2. Basic Usage
Run the evaluation using the `inspect` CLI:
```bash
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.5
```

## CLI examples

### Run with Sample Limit
Test the agent on a small subset (e.g., 5 tasks) to verify the environment setup:
```bash
inspect eval inspect_evals/assistant_bench_web_browser --model anthropic/claude-4.8 --limit 5
```

### Compare Multiple Models
Run AssistantBench across different models to compare performance:
```bash
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.5,anthropic/claude-4.8
```

### Visualize Results
Launch the Inspect log viewer to inspect the agent's step-by-step trajectories:
```bash
inspect view
```

## API examples
You can also trigger AssistantBench evaluations programmatically using the Inspect Python API.

### Minimal Evaluation Script
```python
from inspect_ai import eval
from inspect_evals import assistant_bench_web_browser

# Run AssistantBench on a specific model
results = eval(
    assistant_bench_web_browser(),
    model="openai/gpt-5.5",
    limit=10  # Optional: limit to 10 samples for testing
)

# Output the accuracy and scores
for result in results:
    print(f"Model: {result.model}, Accuracy: {result.metrics['accuracy'].value}")
```

## Related tools / concepts
- [PA-bench](./pa-bench.md) — Web navigation and session orchestration benchmark.
- [GAIA](./gaia.md) — General AI Assistant benchmark for real-world tasks.
- [OSWorld](./os-world.md) — Benchmarking agents in real desktop environments.
- [WebArena](https://webarena.dev/) — Reproducible web environment for agents.
- [OpenHands](../development_ops/openhands.md) — Open-source platform for agentic software engineering.
- [Stagehand](../automation_orchestration/stagehand.md) — Playwright-based agentic browser automation.
- [MultiOn](../agents/multion.md) — Autonomous web navigation agent.
- [Inspect AI](./inspect-ai.md) — The foundational framework for running these evaluations.

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free (benchmark), but requires internet access and LLM API credits. Long trajectories on GPT-5.5 or Claude 4.8 can be expensive.

## Sources / references
- [AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks? (ArXiv)](https://arxiv.org/abs/2407.15711)
- [AssistantBench Project Website](https://assistantbench.github.io/)
- [AssistantBench GitHub](https://github.com/assistantbench/assistantbench)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
