# AssistantBench

## What it is
AssistantBench is a rigorous, open-source evaluation benchmark designed to measure the capability of web-connected AI agents and autonomous assistants to execute complex, realistic, and time-consuming multi-step tasks on the live web. As of late July 2026, AssistantBench is established as a critical component of the "Agentic Evaluation Standard." It systematically quantifies the planning, navigation, retrieval, and reasoning capabilities of frontier models (including Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6, and Gemini 3.5) operating in stateful browser environments.

## What problem it solves
Most traditional LLM benchmarks evaluate atomic capabilities, such as isolated code generation or single-turn QA, in synthetic environments. However, these benchmarks fail to evaluate real-world agentic execution, where an agent must navigate dynamic websites, bypass anti-bot systems, manage complex browser states, retrieve scattered data, and reason across multiple pages to complete a single user request. AssistantBench solves this by providing long-horizon, multi-domain web-agent tasks that typically take a human developer or assistant 10 to 30 minutes to complete, allowing teams to rigorously benchmark success rates and measure Agentic Latency.

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / [Agentic Evaluations](../../knowledge_base/index.md).
It functions as a high-level performance and capability auditing layer, typically orchestrated via modular evaluation frameworks like the UK AISI's `inspect-ai` and integrated into development workflows to compare agent planning architectures (e.g., ReAct, plan-and-solve, or custom state-machines).

## Typical use cases
- **Web Agent Capability Profiling**: Measuring and auditing the execution success rate of browser-based agents like OpenHands, MultiOn, Stagehand, or custom Playwright-based systems.
- **VLM Visual Grounding Analysis**: Evaluating how effectively vision-language models can interpret dynamic, interactive web interfaces, complex layouts, and multi-format graphics.
- **Planning & Self-Correction Audits**: Testing the resilience of agent decision loops when encountering unexpected layout adjustments, pop-ups, modal dialogs, or dead ends.
- **Agentic Latency Quantification**: Measuring the relationship between planning token overhead, action sequences, and actual execution duration on live web routes.
- **RAG & Synthesis Evaluation**: Assessing an agent's capability to search the web, scrape raw materials, and synthesize a single, factual, non-hallucinated answer to multi-layered research queries.

## Strengths
- **Authentic and Realistic Tasks**: Sourced from actual, real-world questions and tasks that humans perform, ensuring evaluation results reflect genuine utility.
- **Dynamic Live Web Execution**: Tests agents on the actual open web, verifying their resilience against real-world web-design patterns and javascript-dense interfaces.
- **Standardized Framework Integration**: Natively integrated with `inspect-ai` and the `inspect-evals` package, enabling standardized execution and evaluation runs.
- **Long-Horizon Multi-Domain Coverage**: Spans across business, real estate, travel booking, scientific research, and SaaS interfaces, ensuring a diverse capability profile.
- **Detailed Visual Tracing**: Generates complete execution logs with visual step-by-step screenshots to allow developers to inspect and analyze agent failure modes.

## Limitations
- **Live Web Volatility**: Because tests are executed on the live internet, unexpected modifications to external websites can occasionally impact test reproducibility and baseline consistency.
- **Compute and Token Cost**: Running long-horizon, multi-step browser loops utilizing frontier visual models (like Claude 5.1 or GPT-5.5) consumes a high volume of input and output tokens.
- **Operational Execution Speed**: Executing true end-to-end browser trajectories on live websites is intrinsically slower than running synthetic unit tests, making it better suited for periodic scheduled runs rather than rapid pre-commit checks.

## When to use it
- When developing or tuning autonomous web assistants, personal agents, or automated research pipelines that navigate the open web.
- To compare and benchmark the cost-to-performance efficiency of different planning layers and model backbones.
- When you need to generate high-confidence capability profiles and success rate reports for enterprise-grade autonomous systems.

## When not to use it
- For testing isolated desktop interface interactions (such as system-level mouse and keyboard actions), where an operating-system-level benchmark like [OSWorld](./os-world.md) is appropriate.
- If you are building a highly sandboxed, air-gapped agent that is explicitly blocked from accessing the external, live internet.
- For high-speed, local regression testing of simple prompts where lightweight, deterministic unit-test assertions are sufficient.

## Getting started
AssistantBench evaluations are primarily orchestrated using the `inspect-ai` framework and the companion `inspect-evals` suite.

### 1. Installation
Install the required packages utilizing pip:
```bash
pip install inspect-ai inspect-evals
```

### 2. Live Web Driver Dependencies
Ensure Playwright or your targeted browser driver is installed and authenticated:
```bash
playwright install
```

## CLI examples
The `inspect` command-line utility provides intuitive controls to run, configure, and inspect AssistantBench evaluations.

```bash
# Run a standard AssistantBench evaluation using a frontier model
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.5

# Restrict the evaluation run to a small, sample-limited set (e.g., 5 tasks) for debugging
inspect eval inspect_evals/assistant_bench_web_browser --model anthropic/claude-5.1 --limit 5

# Compare performance across multiple frontier models simultaneously
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.5,anthropic/claude-5.1

# Boot up the interactive visual log viewer to analyze step-by-step agent trajectories
inspect view
```

## API examples

### 1. Programmatic Evaluation Execution (Python)
Trigger AssistantBench runs programmatically and extract detailed metrics utilizing the Python API.

```python
import os
from inspect_ai import eval
from inspect_evals import assistant_bench_web_browser

# Set up the API environment
os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"

# Execute the evaluation run on a limited set of samples
evaluation_results = eval(
    assistant_bench_web_browser(),
    model="anthropic/claude-5.1",
    limit=10,
    score_filter=None
)

# Extract and output high-level statistics
for run in evaluation_results:
    print(f"Model Evaluated: {run.model}")
    print(f"Task Success Accuracy: {run.metrics['accuracy'].value * 100:.2f}%")
    print(f"Total Trajectory Steps: {run.stats.total_tokens if run.stats else 'N/A'}")
```

### 2. Custom Evaluation Configuration with Target Limits
Configure the benchmark parameters programmatically to isolate specific capabilities or control API costs.

```python
from inspect_ai import eval
from inspect_evals import assistant_bench_web_browser

# Initialize custom evaluation with specific model parameters
results = eval(
    assistant_bench_web_browser(),
    model="openai/gpt-5.5",
    limit=5,
    max_connections=2, # limit concurrent browser execution threads
    model_args={
        "temperature": 0.1,
        "max_tokens": 4096
    }
)

# Parse output metrics programmatically
summary = results[0]
print("Evaluation complete.")
print(f"Mean Accuracy: {summary.metrics.get('accuracy').value}")
```

## Related tools / concepts
- [PA-bench](./pa-bench.md) — Web session orchestration and procedural navigation benchmark.
- [GAIA](./gaia.md) — General AI Assistant benchmark targeting multimodal, tool-connected real-world tasks.
- [OSWorld](./os-world.md) — Comprehensive sandbox benchmark for evaluating agents in real operating-system and desktop environments.
- [Inspect AI](./inspect-ai.md) — Foundational framework developed by the UK AISI for orchestrating model benchmarks.
- [MultiOn](../agents/multion.md) — High-performance visual navigation and execution engine.
- [Stagehand](../automation_orchestration/stagehand.md) — LLM-driven browser-automation SDK built on Playwright.
- [Browser Use](../automation_orchestration/browser-use.md) — Multi-agent browser control framework.
- [Agentic Latency](../../knowledge_base/index.md) — The measure of cognitive and network delay during autonomous long-horizon runs.

## Licensing and cost
- **License**: Apache-2.0 (Open Source)
- **Cost**: The benchmark framework is free, but executing browser trajectories requires live internet connectivity and substantial LLM API token consumption. Long trajectories on premium visual models can result in significant usage costs.

## Sources / references
- [AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks? (ArXiv Paper)](https://arxiv.org/abs/2407.15711)
- [AssistantBench Official Webpage](https://assistantbench.github.io/)
- [AssistantBench Project GitHub Repository](https://github.com/assistantbench/assistantbench)
- [UK AISI Inspect-AI Documentation](https://github.com/UKGovernmentBEIS/inspect-ai)

## Contribution Metadata
- Last reviewed: 2026-07-28
- Confidence: high
