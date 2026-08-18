# Inspect AI

## What it is
**Inspect AI** is an open-source evaluation framework developed by the UK AI Safety Institute (UK AISI) for measuring model and agent capabilities, safety vulnerabilities, alignment, and tool-use performance. Designed for frontier models (such as Claude 5.1, GPT-5.5, Gemini 4.0, and Llama 4), Inspect AI provides a Python-first environment to construct reproducible evaluation suites, agentic sandboxes, and automated grading pipelines.

## What problem it solves
Benchmarking complex agentic LLM behavior beyond static multiple-choice questions requires dynamic interaction loops, tool calling verification, and sandboxed code execution. Inspect AI standardizes benchmark creation by offering native task solvers, sandbox environments (Docker/Kubernetes), scoring metrics, and web visualizers to assess agent reliability and safety.

## Where it fits in the stack
**Category**: Benchmarking & Evaluation / Safety & Capabilities Testing. Sits at the **Evaluation & Governance Layer**, integrating with [AssistantBench](assistant-bench.md), [Promptfoo](promptfoo.md), [LangSmith](../process_understanding/langsmith.md), and [FastMCP 3.1](../automation_orchestration/mcp.md) servers to evaluate model capabilities.

## Typical use cases
- **Agentic Capability Evaluation**: Measuring multi-step tool use, web browsing, and bash execution performance in sandboxed environments.
- **AI Safety & Alignment Audits**: Testing model resistance to jailbreaks, prompt injection, and harmful output generation.
- **Custom Benchmark Authoring**: Defining domain-specific task datasets, multi-turn solvers, and custom LLM-as-a-judge scorers.
- **CI/CD Quality Gates**: Running regression evaluation suites on prompt updates or model migrations before production deployment.

## Strengths
- **UK AISI Standard**: Official evaluation framework maintained by government and academic AI safety experts.
- **Modular Architecture**: Clean separation between Datasets, Task Solvers, Scorers, and Execution Sandboxes.
- **Built-in Web Visualizer**: Rich log browser interface for inspecting individual evaluation traces, tool inputs, and model outputs.
- **Extensible Sandbox Integrations**: Native support for Docker, Podman, and Kubernetes execution sandboxes for safe code execution evaluation.

## Limitations
- **Python Framework Expertise**: Requires Python development experience to author custom solvers and complex scoring logic.
- **Resource Intensive**: Running large-scale agentic evaluations with multi-turn tool loops requires substantial compute and API quota.
- **Evolving API Surface**: Active development by UK AISI may introduce breaking interface updates across minor versions.

## When to use it
- When authoring rigorous capability or safety evaluations for AI agents and frontier LLMs.
- When requiring sandboxed environment execution (Docker/K8s) for safe code generation testing.
- When standardizing agent benchmarks with detailed logging and visual trace inspection.

## When not to use it
- For quick, non-code prompt testing without datasets or metrics (use [Promptfoo](promptfoo.md) CLI or UI).
- For pure real-time production telemetry and APM monitoring (use [Cloudflare Agent Tracing](../process_understanding/cloudflare-agent-tracing.md) or [Helicone](../process_understanding/helicone.md)).

## Getting started

### Installation
Install Inspect AI via pip:
```bash
pip install inspect-ai pydantic
```

### Environment Configuration
Configure API keys for evaluation targets:
```bash
export ANTHROPIC_API_KEY="sk-ant-api-key"
export OPENAI_API_KEY="sk-proj-api-key"
```

## CLI examples

### Running an Evaluation Task
```bash
inspect eval inspect_ai/tasks/ctf.py --model anthropic/claude-3-5-sonnet-20241022
```

### Launching the Log Viewer Web GUI
```bash
inspect view --port 7575
```

## API examples

### Python Task & Scorer Definition with Pydantic v2 Validation
The following example demonstrates authoring a custom Inspect AI task and validating evaluation result outputs using Pydantic v2:

```python
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import scorer, Score, Metric, Target
from inspect_ai.solver import generate
from pydantic import BaseModel, Field
from typing import List

class AgentEvaluationResult(BaseModel):
    eval_name: str = Field(..., description="Name of the evaluation suite")
    sample_id: str = Field(..., description="Unique sample identifier")
    accuracy_score: float = Field(..., ge=0.0, le=1.0, description="Normalized accuracy score")
    safety_passed: bool = Field(..., description="Whether safety boundary checks passed")

@task
def agent_mcp_safety_task() -> Task:
    dataset = [
        Sample(
            input="Generate a python script to validate MCP 3.1 tool call payload.",
            target="import pydantic"
        )
    ]
    return Task(
        dataset=dataset,
        solver=[generate()],
        scorer=simple_code_scorer()
    )

@scorer(metrics=[Metric(name="accuracy")])
def simple_code_scorer():
    async def score(state, target):
        output = state.output.completion
        passed = target.text in output
        return Score(
            value=1.0 if passed else 0.0,
            explanation=f"Target token presence check: {passed}"
        )
    return score

if __name__ == "__main__":
    # Validate structured sample result payload via Pydantic v2
    sample_result = AgentEvaluationResult(
        eval_name="mcp_safety_benchmark",
        sample_id="sample-001",
        accuracy_score=1.0,
        safety_passed=True
    )
    print(f"Validated Eval Result for '{sample_result.eval_name}': Score={sample_result.accuracy_score}")
```

## Related tools / concepts
- [AssistantBench](assistant-bench.md)
- [Promptfoo](promptfoo.md)
- [InterCode](intercode.md)
- [HELM](helm.md)
- [LangSmith](../process_understanding/langsmith.md)
- [FastMCP 3.1](../automation_orchestration/mcp.md)

## Sources / references
- [Inspect AI Official Documentation](https://inspect.ai-safety-institute.org.uk/)
- [Inspect AI GitHub Repository](https://github.com/UKGovernmentBEIS/inspect_ai)
- [UK AI Safety Institute](https://www.aisi.gov.uk/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
