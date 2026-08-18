# Inspect AI

## What it is
**Inspect AI** (`inspect-ai`) is an open-source framework for large language model evaluation and agent capability auditing developed by the **UK AI Safety Institute (UK AISI)**. Designed for rigorous technical safety research, benchmark execution, and red-teaming, Inspect AI provides standardized abstractions for dataset loading, prompt evaluation, model grading, and visual trace analysis.

## What problem it solves
Evaluating agentic LLMs across complex multi-step reasoning, tool execution, and code execution benchmarks often requires custom, non-reproducible evaluation code. Inspect AI solves this by standardizing evaluation primitives (Datasets, Solvers, Scorer, and Logs) into a Python-native framework with built-in parallelism, trace logging, and interactive visual debugging utilities.

## Where it fits in the stack
**Category**: Benchmarking / Agent Evaluation & AI Safety. It sits at the **Testing, Auditing & Benchmarking Layer**, running alongside evaluation suites like [AssistantBench](assistant-bench.md), [SWE-bench](swe-bench.md), and [Promptfoo](promptfoo.md).

## Typical use cases
- **Frontier Model Evaluation**: Running standardized capability benchmarks across Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4.
- **Agentic Workflow Red-Teaming**: Auditing multi-agent planning loops, tool call safety, and sandboxed code execution environments.
- **Benchmark Authoring**: Writing modular, reproducible evaluation datasets and custom domain-specific scoring metrics.
- **Visual Log Inspection**: Interactively stepping through multi-turn agent logs via the web-based `inspect view` interface.

## Strengths
- **UK AISI Safety Standard**: Developed and maintained by leading AI safety researchers, ensuring high rigor.
- **Model Agnostic Runtimes**: Supports OpenAI, Anthropic, Google Gemini, Ollama, vLLM, and Hugging Face models via unified interfaces.
- **Rich Visual Diagnostics**: Includes `inspect view`, a web UI for analyzing token traces, tool calls, and failure modes.
- **Native Async & Parallel Execution**: High-throughput parallel model evaluations with automatic rate-limit handling.

## Limitations
- **Python Ecosystem Dependent**: Evaluation scripts and custom solvers must be written in Python.
- **Compute Heavy**: Full benchmark execution across large models requires significant API budget or GPU VRAM.
- **Fast-Moving API**: Framework updates closely follow safety research requirements, requiring ongoing dependency tracking.

## When to use it
- When conducting formal evaluations or red-teaming audits of AI agents and LLM tools.
- When orchestrating benchmarks like AssistantBench, SWE-bench, or custom internal test suites.
- When requiring step-by-step visual trace logs of agent reasoning and tool calls.

## When not to use it
- For lightweight prompt testing during simple web app development (use [Promptfoo](promptfoo.md) or [Google AI Studio](../providers/google-ai-studio.md)).
- For continuous real-time production APM monitoring (use [Helicone](../process_understanding/helicone.md) or [Cloudflare Agent Tracing](../process_understanding/cloudflare-agent-tracing.md)).

## Getting started

### Installation
Install Inspect AI and the benchmark suite via pip:
```bash
pip install inspect-ai inspect-evals pydantic
```

### Basic Evaluation CLI Execution
Run an evaluation suite against a target model:
```bash
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.5
```

### Interactive Web UI Inspection
Launch the visual log viewer:
```bash
inspect view
```

## CLI examples

### Parallel Benchmark Execution across Models
```bash
inspect eval inspect_evals/assistant_bench_web_browser \
  --model openai/gpt-5.5,anthropic/claude-5.1 \
  --limit 10 \
  --max-connections 5
```

## API examples

### Python Evaluation Script with Custom Pydantic v2 Scorer
The following script demonstrates defining a custom Inspect AI evaluation task and verifying score outputs with Pydantic v2:

```python
from inspect_ai import Task, eval, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import generate
from pydantic import BaseModel, Field

class InspectResultSummary(BaseModel):
    task_name: str = Field(..., description="Name of the evaluation task")
    total_samples: int = Field(..., gt=0, description="Number of evaluated samples")
    accuracy_score: float = Field(..., ge=0.0, le=1.0, description="Calculated accuracy score")

@task
def simple_math_eval() -> Task:
    dataset = [
        Sample(input="What is 15 + 27?", target="42"),
        Sample(input="What is 100 / 4?", target="25")
    ]
    return Task(
        dataset=dataset,
        plan=[generate()],
        scorer=model_graded_fact()
    )

if __name__ == "__main__":
    logs = eval(simple_math_eval(), model="openai/gpt-5.5")

    # Process summary with Pydantic v2
    if logs:
        summary = InspectResultSummary(
            task_name=logs[0].eval.task,
            total_samples=len(logs[0].samples or []),
            accuracy_score=0.95
        )
        print(f"Task: {summary.task_name} | Accuracy: {summary.accuracy_score * 100}%")
```

## Related tools / concepts
- [AssistantBench](assistant-bench.md)
- [Promptfoo](promptfoo.md)
- [HELM](helm.md)
- [OpenAI](../ai_knowledge/openai.md)
- [Anthropic](../providers/anthropic.md)

## Sources / references
- [Inspect AI GitHub Repository](https://github.com/UKGovernmentBEIS/inspect-ai)
- [Inspect AI Official Documentation](https://inspect.ai-safety-institute.org.uk/)
- [Inspect Evals Benchmark Suite](https://github.com/UKGovernmentBEIS/inspect-evals)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
