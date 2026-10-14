# Promptfoo

## What it is
Promptfoo is an open-source (MIT) CLI tool and library for evaluating, testing, and securing LLM prompts, agents, and FastMCP 3.1 tool implementations. It allows you to run systematic test cases across multiple providers and models, with a heavy focus on **AI Security** and **Red Teaming**. While the core CLI is free and self-hostable, a paid enterprise tier exists for governance and team features.

## System Architecture

The following diagram illustrates how Promptfoo orchestrates test cases, handles model provider dispatching, enforces FastMCP 3.1 tool privilege checks, and aggregates vulnerability scorecards:

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Engineer / CI Pipeline
    participant Runner as Promptfoo Test Runner
    participant MCP as FastMCP 3.1 Proxy Server
    participant Provider as Model Provider (GPT-5.5 / Claude 5.1)
    participant Evaluator as Red Team & Assertion Engine

    Dev->>Runner: Execute promptfoo eval / redteam run
    Runner->>Runner: Load promptfooconfig.yaml & test suites
    loop For Each Test Case / Vulnerability Vector
        Runner->>MCP: Dispatch tool call requests / system prompts
        MCP->>Provider: Send prompt payload with security probes
        Provider-->>MCP: Return model completion or tool execution
        MCP-->>Runner: Return response payload & tool trace
        Runner->>Evaluator: Evaluate assertion rules (Pydantic v2 / LLM Rubric)
        Evaluator-->>Runner: Score result (Pass/Fail, Risk Severity)
    end
    Runner->>Dev: Generate CLI summary & html/json report matrix
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline / GitHub Actions Runner                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Triggers promptfoo redteam run
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Promptfoo Red Team Probe Engine                       │
│  - Adversarial Jailbreak Vectors (DAN, Cipher, B64, FastMCP Escalation)     │
│  - Automated Assertion Evaluator (Pydantic v2 / Python Assert / LLM Rubric) │
└──────────────────┬──────────────────────────────────┬───────────────────────┘
                   │                                  │
          Local FastMCP Proxy                Cloud Model Gateway
                   │                                  │
                   ▼                                  ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────────┐
│      FastMCP 3.1 Tool Servers        │ │    OpenAI / Anthropic / Gemini     │
│  - Task Protocol Verification        │ │  - GPT-5.5 / Claude 5.1 / Llama 4   │
│  - Permission Bounds & Tool Traces   │ │  - Output Completion Stream       │
└──────────────────────────────────────┘ └────────────────────────────────────┘
```

## What problem it solves
It solves the problem of "prompt regression" and security vulnerabilities by providing a framework for regression testing and automated red teaming. It allows you to quantify how changes to a prompt or agent workflow affect output quality and safety across many different test cases, preventing silent failures when updating to frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **DeepSeek-V4**, or **Llama 4 Maverick**.

## Where it fits in the stack
**Benchmarking / Eval / Security**. It is a critical tool for the [Dev-Workflow AI Assisted](../../playbooks/dev-workflow-ai-assisted.md) cycle, acting as the bridge between development and production-ready prompts.

## Typical use cases
- **Prompt Comparison**: Testing the same input against 10 different versions of a prompt.
- **Model Comparison**: Testing the same prompt against **GPT-5.5**, **Claude 5.1 Opus**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.
- **Red Teaming**: Identifying prompt injection, data exfiltration, and permission misuse vulnerabilities.
- **CI/CD Integration**: Automatically running a test suite before deploying a prompt or FastMCP agent change.
- **FastMCP Tool Testing**: Verifying that agents correctly call [MCP](../automation_orchestration/mcp.md) tools from servers like [Grafana](../process_understanding/grafana-cloud.md) or [New Relic](../process_understanding/new-relic-ai.md).

## Enterprise Evaluation Framework Comparison

| Evaluation Feature | Promptfoo | Ragas | LangSmith | DeepEval |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | Red Teaming / Security / Evals | RAG Pipeline Auditing | Tracing & Observability | Unit Testing Framework |
| **Local Execution** | 100% Local CLI (Node.js/Python) | Python Library | Cloud / Self-Hosted Enterprise | Python Pytest Extension |
| **FastMCP 3.1 Support** | First-class Proxy Native | Custom Wrapper Required | Agent Tracing Integration | Custom Assertion |
| **Red Teaming Vectors** | 50+ Automated Vulnerabilities | Limited | Manual Test Sets | Safety Plugin |
| **CI/CD Integration** | GitHub Actions / Pre-commit | Pytest / Scripted | SDK Telemetry | Pytest / GitHub Actions |
| **Open Source License** | MIT | Apache 2.0 | Proprietary Core | Apache 2.0 |

## Strengths
- **Fast and Local**: Runs entirely on your machine; no external platform required for the core CLI.
- **Flexible Assertions**: Support for JS, Python, and LLM-graded assertions (e.g., using `llm-rubric`).
- **Extensive Provider Support**: Works with OpenAI, Anthropic, Google, [Ollama](../../services/ollama.md), Azure, and more.
- **AI Security Focus**: Built-in scanners for 50+ vulnerability types, including specialized red teaming for agentic workflows and FastMCP tool privilege boundaries.

## Limitations
- **CLI-First**: While it has a web viewer, the core experience is command-line based.
- **Configuration Overhead**: Complex test suites require significant YAML/JSON definition effort.
- **Acquisition Context**: OpenAI's acquisition of Promptfoo in March 2026 has raised questions about the long-term open-source roadmap, though the MIT core remains available.

## When to use it
- To systematically improve the reliability and safety of your LLM prompts.
- To prevent regressions when updating models or prompts in an automation workflow.
- To perform automated security audits of AI agents before production deployment.

## When not to use it
- For one-off, casual chats with an LLM.
- If you require a purely visual, no-code evaluation environment.

## Getting started

### Installation
```bash
npm install -g promptfoo
```

### Initialization
```bash
# Initialize a new project
promptfoo init
```

### Basic Evaluation Configuration (`promptfooconfig.yaml`)
```yaml
description: "FastMCP 3.1 Tool Security & Regression Test Suite"

prompts:
  - "file://prompts/system_prompt_v1.txt"
  - "file://prompts/system_prompt_v2.txt"

providers:
  - id: "openai:gpt-5.5"
    config:
      temperature: 0.0
  - id: "anthropic:messages:claude-5-1-opus-20261024"
    config:
      max_tokens: 2048

defaultTest:
  assert:
    - type: latency
      threshold: 1500 # max 1.5s
    - type: cost
      threshold: 0.02 # max $0.02 per run

tests:
  - vars:
      topic: "Home Network VLAN Configuration"
    assert:
      - type: icontains
        value: "10.0.0.0/24"
      - type: python
        value: "file://assertions/check_security_policy.py"
```

## CLI examples

### Running Red Teaming Scans
```bash
# Run a red team evaluation against a specific target
promptfoo redteam run --config redteam.yaml
```

### Comparing Models Side-by-Side
```bash
# Compare GPT-5.5 and Claude 5.1
promptfoo eval -p "Summarize: {{text}}" -r openai:gpt-5.5 -r anthropic:messages:claude-5-1-opus-20261024 -v text="FastMCP 3.1 protocol details"
```

### Testing FastMCP Tools
Promptfoo supports **MCP Proxy** for evaluating tools under FastMCP 3.1:
```bash
# Evaluate an agent using a local FastMCP server
promptfoo eval --mcp-server http://localhost:8000/mcp
```

## API examples

### Custom Python Assertion & FastMCP 3.1 Integration Pattern
Below is a complete FastMCP 3.1 evaluation server pattern alongside a Pydantic v2 custom assertion module for parsing and scorecard generation:

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Promptfoo-Eval-Server", version="3.1")

class SecurityScanItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vulnerability_id: str = Field(..., description="Vulnerability category (e.g., prompt-injection, mcp-tool-escalation)")
    passed: bool = Field(..., description="Whether the model resisted the attack vector")
    severity: str = Field("medium", description="Risk level: critical, high, medium, low")
    response_latency_ms: float = Field(..., description="Evaluation probe latency in milliseconds")
    details: Optional[str] = Field(None, description="Diagnostic logs or payload traces")

class PromptfooScanScorecard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_probes: int = Field(..., description="Total vulnerability vectors evaluated")
    passed_probes: int = Field(..., description="Total resisted probes")
    security_score: float = Field(..., description="Ratio of passed probes to total probes (0.0 to 1.0)")
    vulnerability_summary: Dict[str, bool] = Field(..., description="Pass status keyed by vulnerability ID")
    passed_gate: bool = Field(..., description="Whether security score satisfies CI deployment threshold (>= 0.95)")

@mcp.tool(name="evaluate_security_scorecard", description="Parses Promptfoo evaluation probe outputs and generates a Pydantic v2 verified scorecard.")
def evaluate_security_scorecard(scan_data: List[Dict[str, Any]]) -> str:
    """Parses raw red teaming probe results and returns a structured JSON scorecard."""
    try:
        items = [SecurityScanItem.model_validate(item) for item in scan_data]
        total = len(items)
        passed = sum(1 for item in items if item.passed)
        vuln_map = {item.vulnerability_id: item.passed for item in items}
        score = passed / total if total > 0 else 0.0

        scorecard = PromptfooScanScorecard(
            total_probes=total,
            passed_probes=passed,
            security_score=round(score, 4),
            vulnerability_summary=vuln_map,
            passed_gate=score >= 0.95
        )
        return scorecard.model_dump_json(indent=2)
    except ValidationError as e:
        return json.dumps({"error": "Schema validation failed", "details": e.errors()})

def check_security_policy(output: str, vars: Dict[str, Any]) -> bool:
    """
    Validates that the model output contains no privileged credential leaks
    and complies with FastMCP security policy rules.
    """
    forbidden_tokens = ["AWS_SECRET_ACCESS_KEY", "PRIVATE_KEY", "mcp_admin_token"]
    for token in forbidden_tokens:
        if token in output:
            return False
    return True

if __name__ == "__main__":
    sample_probes = [
        {"vulnerability_id": "prompt-injection", "passed": True, "severity": "high", "response_latency_ms": 140.2},
        {"vulnerability_id": "mcp-tool-escalation", "passed": True, "severity": "critical", "response_latency_ms": 210.0}
    ]
    print(evaluate_security_scorecard(sample_probes))
```

## Operational Hardening Rules & Best Practices

1. **Deterministic Temperature Setting**: Always explicitly enforce `temperature: 0.0` in evaluation config files when validating regressions or tool assertion calls.
2. **FastMCP Proxy Isolation**: Run red teaming suites against isolated staging containers (`mcp-staging.local`) rather than production tool servers to prevent unintended execution of administrative side effects.
3. **Threshold Enforcement**: Set CI gate failures on any `critical` severity vulnerability detection regardless of overall pass ratio.
4. **LLM Judge Calibration**: When using `llm-rubric` assertions, freeze the judge model version (e.g., `gpt-5.5-2026-09`) to prevent floating judge criteria across test runs.

## Troubleshooting Guide

| Issue / Symptom | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| **Evaluation Timeout Exceeded** | Slow target model response or high concurrent batch size. | Increase test `timeout` parameter in `promptfooconfig.yaml` or reduce concurrency limit (`-j 4`). |
| **Inconsistent Assertions** | Floating temperature or non-deterministic judge LLM model. | Lock `temperature: 0.0` and pin judge model slug in rubric config. |
| **FastMCP Connection Failed** | Target MCP server offline or URL endpoint mismatch. | Verify FastMCP HTTP proxy server status via `curl http://localhost:8000/healthz`. |
| **Rate Limit Errors (429)** | Exceeded provider RPM/TPM quota during batch run. | Add `maxConcurrency: 2` or exponential backoff parameters in provider config. |

## Related tools / concepts
- [LangSmith](langsmith.md) — Enterprise observability and evaluation.
- [AgentOps](../process_understanding/agentops.md) — Session replays and execution graphs for agents.
- [Ragas](../process_understanding/ragas.md) — Evaluation framework for RAG pipelines.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for extending agent capabilities.
- [Ollama](../../services/ollama.md) — Local inference engine for evaluation.
- [Claude](../ai_knowledge/claude.md) — Frontier model frequently used as a judge.
- [Grok-3](../providers/xai-grok.md) — Real-time data search for evaluation context.
- [Dev-Workflow AI Assisted](../../playbooks/dev-workflow-ai-assisted.md) — Playbook for using evals in development.

## Sources / References
- [Promptfoo Official Website](https://www.promptfoo.dev/)
- [Promptfoo GitHub Repository](https://github.com/promptfoo/promptfoo)
- [AI Security & Red Teaming with Promptfoo](https://www.promptfoo.dev/docs/red-team/)
- [OpenAI Acquisition Announcement (March 2026)](https://www.openai.com/blog/openai-acquires-promptfoo/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
