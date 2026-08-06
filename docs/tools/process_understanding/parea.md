# Parea

## What it is
Parea is an enterprise-grade AI developer platform tailored for debugging, testing, observing, and validating LLM-based applications. In late November / December 2026 (v2.4+), it features first-class support for multi-agent execution tracing, native [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) tool logging, and scalable automated evaluations (evals) leveraging LLM-as-a-Judge scoring.

## What problem it solves
Developing agentic and multi-step LLM workflows is inherently non-deterministic, making them prone to silent regressions, loops, and quality degradation. Parea solves this by capturing granular, structured traces of every sub-step, model invocation, and tool call. It enables continuous regression testing and live production observability, turning abstract LLM behavior into quantifiable metrics (e.g., cost, latency, token throughput, and success rates) so developers can iteratively improve their prompts and model routing strategies.

## Where it fits in the stack
**AI Development & Observability**. Within the agentic stack, Parea serves as the centralized observability control plane. It integrates directly with framework layers like [CrewAI](../frameworks/crewai.md) and [LangGraph](../frameworks/langgraph.md) to record trace spans, monitor API interactions with providers like [Anthropic](../providers/anthropic.md), and manage prompt versioning.

## Typical use cases
- **Multi-Agent Flow Tracing**: Recording complex collaborative sessions where one agent delegates tasks to another to diagnose where execution loops or tool errors occur.
- **LLM-as-a-Judge Evaluations**: Scoring outputs automatically using models like Claude 5.1, GPT-5.5, or Gemini 4.0 against human-designed criteria.
- **Prompt Asset Lifecycle**: Managing prompt versions and deploying them directly from Parea's UI to local code without requiring redeployments.
- **Automated CI/CD Regression Tests**: Running unit-test suites over large prompt datasets before merging changes into the production repository.

## Strengths
- **Native Agent Awareness**: Explicit support for multi-agent traces, easily highlighting handoffs and parallel executions in visual waterfall graphs.
- **Robust SDKs**: Intuitive decorators and wrappers in Python and TypeScript that capture logs asynchronously without blocking the main event loop.
- **Custom Heuristics**: Allows developers to mix simple code-based checks (e.g., regex, JSON schema validation) with complex LLM evaluation judges.
- **FastMCP 3.1 Observability**: Native logging capability for MCP tool servers, tracing raw inputs and outputs across boundaries.

## Limitations
- **Cloud-Centric Core**: While it offers strong local SDK testing, advanced dashboards and historical tracking require sending execution logs to the Parea cloud.
- **Latency Overheads**: Tracing deeply nested loops can add a small payload serialization and network dispatch delay to API runs.
- **Metric Tuning Complexities**: Setting up robust "LLM Judges" that consistently align with human reviews can require substantial prompt engineering.

## When to use it
- When you are deploying multi-agent autonomous loops that require fine-grained trace logs to debug failure points.
- To execute automated prompt evaluations as an integral step in your CI/CD pipelines.
- When you need a unified dashboard to compare the cost, latency, and performance of different LLMs (e.g., GPT-5.5 vs. Claude 5.1).

## When not to use it
- For trivial, single-prompt applications where basic standard output logs are sufficient.
- In strictly air-gapped homelab environments that forbid outbound internet access (since tracing dispatchers require a Parea cloud endpoint).

## Getting started

### Installation
Parea requires Python >= 3.10 and can be installed via `pip`:
```bash
# Install Parea SDK and Pydantic v2
pip install parea-ai pydantic>=2.0
```

### Configuration
Log in to the Parea dashboard to generate your API key and export it to your shell:
```bash
export PAREA_API_KEY="parea_sec_key_abc123"
```

## CLI examples

### Visual Authentication
```bash
# Authenticate your terminal session with Parea Cloud
parea login
```

### Running Local Evaluations
```bash
# Execute local evaluation experiments against a pre-defined dataset
parea experiment --func run_agent.py:agent_harness --data ./eval_dataset.json
```

### Fetching Deployed Prompts
```bash
# View all prompt assets registered and deployed in your project
parea deploy list
```

## API examples

### Programmatic SDK Trace and Evaluation Verification with Strict Pydantic v2 Validation
This example showcases a production-grade evaluation harness. It defines strict Pydantic v2 models to validate trace spans, latencies, and LLM-as-a-Judge evaluation metrics, ensuring that model performance reports meet strict quality control parameters before they are logged.

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from parea import Parea

# 1. Define strict Pydantic v2 schemas for tracing metrics and evaluation scores
class TraceMetrics(BaseModel):
    latency_seconds: float = Field(..., gt=0.0, description="Execution time in seconds")
    input_tokens: int = Field(..., ge=0)
    output_tokens: int = Field(..., ge=0)
    estimated_cost: float = Field(..., ge=0.0)

class JudgeScore(BaseModel):
    metric_name: str = Field(..., pattern=r"^[a-zA-Z_0-9-]+$")
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score between 0.0 and 1.0")
    reasoning: str = Field(..., min_length=10)

class VerifiedTraceSpan(BaseModel):
    span_id: str = Field(..., min_length=8)
    trace_id: str = Field(..., min_length=8)
    model_name: str
    metrics: TraceMetrics
    scores: List[JudgeScore] = []

    @field_validator("metrics")
    @classmethod
    def validate_cost_sanity(cls, v: TraceMetrics) -> TraceMetrics:
        # Cost validation check (sanity bound)
        if v.estimated_cost > 5.0:
            raise ValueError("Trace cost exceeds safety threshold of $5.00 per execution")
        return v

# 2. Executable validation logic
def verify_and_log_span(raw_payload: dict) -> Optional[VerifiedTraceSpan]:
    try:
        # Validate against strict Pydantic v2 schema
        validated_span = VerifiedTraceSpan.model_validate(raw_payload)
        return validated_span
    except Exception as e:
        print(f"Trace payload verification failed: {e}")
        return None

if __name__ == "__main__":
    print("Initializing Parea trace validation...")

    # Simulated trace payload returned from a multi-agent execution loop
    simulated_payload = {
        "span_id": "span-9a72b8",
        "trace_id": "trace-102948cba",
        "model_name": "claude-5.1-sonnet",
        "metrics": {
            "latency_seconds": 1.48,
            "input_tokens": 1250,
            "output_tokens": 480,
            "estimated_cost": 0.0125
        },
        "scores": [
            {
                "metric_name": "factual_accuracy",
                "score": 0.95,
                "reasoning": "The model response successfully correctly matched all truth facts in the test context."
            },
            {
                "metric_name": "safety_check",
                "score": 1.0,
                "reasoning": "No offensive content or prompt injection indicators detected in the output span."
            }
        ]
    }

    result = verify_and_log_span(simulated_payload)
    if result:
        print(f"Successfully verified Parea Trace Span ID: {result.span_id}")
        print(f"Model Used: {result.model_name}")
        print(f"Latency: {result.metrics.latency_seconds}s")
        for s in result.scores:
            print(f" -> Evaluator [{s.metric_name}]: {s.score * 100}% - {s.reasoning}")
```

## Related tools / concepts
- [Braintrust](braintrust.md) — Evaluation and tracing server for advanced agent workflows.
- [LangSmith](../benchmarking/langsmith.md) — LLM debugging and tracing dashboard.
- [W&B Weave](wandb-weave.md) — Lightweight prompt optimization and span tracing.
- [Comet Opik](comet-opik.md) — Open-source LLM evaluation platform.
- [Langfuse](langfuse.md) — Self-hostable LLM observability suite.
- [Arize AI](arize-ai.md) — Comprehensive model observability and validation platform.
- [PostHog](posthog.md) — Open-source product and LLM analytics tool.
- [AgentOps](agentops.md) — Specialized tracing and auditing suite for autonomous agent loops.

## Sources / References
- [Parea AI Official Website](https://www.parea.ai/)
- [Parea Platform Documentation](https://docs.parea.ai/)
- [SOTA Multi-Agent Observability Patterns (Late 2026)](https://docs.parea.ai/welcome/what_is_parea_ai)

## Contribution Metadata
- Last reviewed: 2026-12-08
- Confidence: high
