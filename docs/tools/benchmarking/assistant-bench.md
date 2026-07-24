# AssistantBench

## What it is
AssistantBench is a benchmark designed to evaluate whether web agents can solve realistic, complex, and multi-step tasks on the open web. As of late July 2026, it is a core component of the industry-wide 'Agentic Evaluation Standard' for general-purpose digital assistants, testing multi-agent capabilities, long-horizon tool manipulation, and execution tracking under the **Model Context Protocol (MCP 3.1)**.

## What problem it solves
It addresses the core limitation of benchmarks that only focus on atomic actions or single-site synthetic interactions. AssistantBench provides tasks that require agents to navigate multiple real-world websites, bypass visual layout shifts, retrieve disjointed information, and reason over it to find answers that a human would typically find "time-consuming." It helps systematically quantify 'Agentic Latency' and overall mission success rates.

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / Evaluation Framework. It serves as a rigorous testing ground for web-connected agents, multi-agent orchestrators, and browser-based automation systems, frequently used to benchmark **Claude 5.1**, **GPT-5.5**, **Llama 4**, **Gemma 3**, and **Qwen 3.6** performance in live, sandboxed environments.

## Typical use cases
- **Web Agent Evaluation**: Testing the reliability of autonomous web agents like OpenHands, MultiOn, or custom Playwright-based pipelines.
- **Complex Information Synthesis**: Measuring the ability to synthesize structured data from highly diverse web sources (e.g., real estate, financial tables, corporate directories).
- **Long-Horizon Planning**: Evaluating how agents handle complex missions that take 10 to 30 minutes for a skilled human.
- **Multimodal Grounding**: Testing how well vision-language models (VLMs) can interpret dynamic, interactive, or JS-heavy web interfaces.
- **MCP 3.1 Task Compliance**: Monitoring how cleanly agents report progress or manage sub-tasks during web execution.

## Strengths
- **Realistic Task Design**: Grounded entirely in actual, high-effort queries that humans perform on the web daily.
- **Multi-Domain Breadth**: Covers real estate, travel routing, business research, e-commerce, and public databases.
- **Execution-Grounded**: Evaluation metrics are strictly based on the final, verified answer found on the live web rather than synthetic steps.
- **Standardized Framework**: Built-in, native support for running within the `inspect-ai` and `inspect-evals` environments.

## Limitations
- **Web Volatility**: Since tasks are executed on the live open web, real-time changes in third-party site structures can occasionally affect task reproducibility.
- **High Latency**: Running full trajectories with dozens of reasoning and visual feedback loops is inherently slower than local code evals.
- **Operational Cost**: High token consumption for long-horizon agents navigating several sites with dense visual or DOM structures.

## When to use it
- When developing or tuning AI agents intended for autonomous, public web browsing.
- When you need to measure success on complex, multi-site "information seeking" and transaction-facilitating missions.
- To objectively compare the efficiency and accuracy of different planning architectures (e.g., ReAct vs. state-machines vs. Agentic RAG).
- When validating an agent's compliance with standard **MCP 3.1** task events.

## When not to use it
- For testing basic OS-level desktop interaction (use OSWorld instead).
- For evaluating models in restricted, air-gapped sandbox environments without live internet routing.
- For high-speed regression testing where instant, deterministic unit results are required.

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
inspect eval inspect_evals/assistant_bench_web_browser --model anthropic/claude-5.1 --limit 5
```

### Compare Multiple Models
Run AssistantBench across different models to compare performance:
```bash
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.5,anthropic/claude-5.1
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
- [WebArena](https://webarena.dev/) — Reproducible, synthetic web environment for agents.
- [OpenHands](../development_ops/openhands.md) — Open-source platform for agentic software engineering.
- [Stagehand](../automation_orchestration/stagehand.md) — Playwright-based agentic browser automation.
- [MultiOn](../agents/multion.md) — Autonomous web navigation agent.
- [Inspect AI](./inspect-ai.md) — The foundational framework for running these evaluations.

## Licensing and cost
- **Open Source**: Yes (MIT Licensed)
- **Cost**: Free (the benchmark code itself), but requires internet access and LLM API credits. Long trajectories on GPT-5.5 or Claude 5.1 can incur significant API costs.

## Sources / references
- [AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks? (ArXiv)](https://arxiv.org/abs/2407.15711)
- [AssistantBench Project Website](https://assistantbench.github.io/)
- [AssistantBench GitHub](https://github.com/assistantbench/assistantbench)

## Contribution Metadata
- Last reviewed: 2026-07-29
- Confidence: high
