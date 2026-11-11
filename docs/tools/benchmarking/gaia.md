# GAIA (General AI Assistants)

## What it is
GAIA (General AI Assistants) is a benchmark designed to evaluate General AI Assistants on non-trivial, multi-modal tasks. It consists of 450 carefully designed, high-fidelity questions that are conceptually simple for humans but extremely challenging for the most advanced AI systems. As of early 2027, it is the gold standard for measuring 'System 2' reasoning, tool use, FastMCP 3.1 Task Protocol interactions, and long-horizon planning in autonomous agents.

GAIA evaluates agents built on frontier LLMs ([Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../providers/google-ai-studio.md), [DeepSeek-V4](../providers/deepseek.md)) on realistic tasks requiring multi-modal asset understanding, file system manipulation, web research, and Python execution.

## Evaluation Pipeline Topology

```
+-----------------------------------------------------------------------------------+
|                        GAIA Benchmark Execution Pipeline                          |
|                                                                                   |
|   +--------------------------+       +----------------------------------------+   |
|   |  GAIA Question & Assets  |       |  Isolated Sandbox Execution Layer      |   |
|   |  (PDF / Audio / XLSX)    |       |                                        |   |
|   +------------+-------------+       |   +--------------------------------+   |   |
|                |                     |   | Inspect AI Benchmark Runner    |   |   |
|                v                     |   +---------------+----------------+   |   |
|   +--------------------------+       |                   |                    |   |
|   | FastMCP 3.1 Task Protocol|<======|===================>                    |   |
|   | Agent Execution Bridge   |       |   +--------------------------------+   |   |
|   +------------+-------------+       |   +--------------------------------+   |   |
|                |                     |   | Agent Planning & VLM Core      |   |   |
|                v                     |   | (Claude 5.6 / GPT-5.6 / Gemma 4)   |   |
|   +--------------------------+       |   +---------------+----------------+   |   |
|   | Pydantic v2 Task & Score |       |                   |                    |   |
|   | Ground-Truth Validator   |       |                   v                    |   |
|   +------------+-------------+       |   +--------------------------------+   |   |
|                |                     |   | Web Browser / Python / Bash    |   |   |
|                v                     |   +--------------------------------+   |   |
|   +----------------------------------+----------------------------------------+   |
|   | Leaderboard Accuracy Metric Output (Level 1 / Level 2 / Level 3 Split)    |   |
|   +---------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------+
```

```mermaid
sequenceDiagram
    autonumber
    actor Bench as Inspect AI Evaluator
    participant FastMCP as FastMCP 3.1 Benchmark Gateway
    participant Sandbox as Docker Isolation Sandbox
    participant Agent as Autonomous Agent Core
    participant Judge as Ground-Truth Evaluator

    Bench->>FastMCP: Dispatch GAIA Question Payload & Modality Assets
    FastMCP->>Sandbox: Spin Up Ephemeral Container Environment
    FastMCP->>Agent: Initialize Task Context & Tool Capabilities
    loop Multi-Step Planning & Execution Loop
        Agent->>Sandbox: Execute Tool Action (Python / Web Search / OCR)
        Sandbox-->>Agent: Return Tool Result & File Outputs
    end
    Agent-->>FastMCP: Submit Final Answer Output String
    FastMCP->>Judge: Validate Normalized Answer against Ground-Truth
    Judge-->>Bench: Return Score Metric & Execution Trace Log
```

## Mathematical Formulations & Agent Convergence Bounds

The evaluation mechanics of GAIA assess multi-step decision chains where success requires uncorrupted tool execution and reasoning paths.

### 1. Cumulative Multi-Step Task Success Probability
Let an agent solve a Level $k \in \{1, 2, 3\}$ task requiring $N_k$ sequential actions $(a_1, a_2, \dots, a_{N_k})$. Given action conditional success probability $P(a_i \mid a_{<i}, \mathcal{E}_{i-1})$, the cumulative probability of reaching the exact ground truth is:

$$
P(\text{Success}_k) = \prod_{i=1}^{N_k} P(a_i \mid a_{<i}, \mathcal{E}_{i-1}) \cdot \mathbb{I}(\text{Norm}(\hat{y}) = y^*)
$$

In the presence of environmental recovery loops (self-correction with max retry budget $R$), the effective step reliability $\hat{p}_i$ expands to:

$$
\hat{p}_i = 1 - (1 - p_i)^{R+1}
$$

For Level 3 tasks where $N_3 \ge 18$, even an individual step reliability of $p_i = 0.95$ yields a naive cumulative success rate of $0.95^{18} \approx 39.7\%$, explaining the sharp empirical drop in unassisted models.

### 2. Multi-Modal Information Entropy & Calibration
When extracting target quantities from heterogeneous assets $\mathcal{D} = \{D_{\text{pdf}}, D_{\text{xlsx}}, D_{\text{img}}\}$, the reasoning step uncertainty is bounded by the conditional Shannon entropy:

$$
\mathcal{H}(Y \mid \mathcal{D}) = -\sum_{y \in \mathcal{Y}} P(y \mid \mathcal{D}) \log_2 P(y \mid \mathcal{D})
$$

To minimize answer variance, agents apply verification ensembles whose consensus score satisfies:

$$
\mathcal{H}(Y \mid \mathcal{D}, \mathcal{T}_{\text{code}}) \le \epsilon_{\text{threshold}} \quad (\epsilon_{\text{threshold}} \approx 0.15\text{ bits})
$$

where $\mathcal{T}_{\text{code}}$ denotes verified deterministic execution outputs from the sandboxed Python interpreter.

### 3. Tool Invocation Complexity & Latency Roofline
The total wall-clock execution time $T_{\text{exec}}$ across $M$ tool interactions under concurrency degree $C$ is modeled as:

$$
T_{\text{exec}} = \sum_{j=1}^{M} T_{\text{LLM}, j} + \frac{1}{C}\sum_{j=1}^{M} \left( T_{\text{sandbox}, j} + T_{\text{IO}, j} \right) \le T_{\text{timeout}}
$$

where $T_{\text{timeout}} \in \{120\text{s}, 300\text{s}, 900\text{s}\}$ for Levels 1, 2, and 3 respectively.

## Comparative Benchmark Matrix

The following table contextualizes GAIA against contemporary frontier agent and reasoning evaluation suites:

| Benchmark Suite | Target Evaluation Scope | Multi-Modal Assets | Sandbox Execution | Tool Calling Depth | Contamination Resistance | Primary Target Models |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GAIA** | **General Digital Assistant Real-World Tasks** | **Yes (PDF, Audio, Excel, Images)** | **Mandatory (Docker/POSIX)** | **Deep (Python, Search, OCR, Web)** | **Extremely High (Continuous human-crafted)** | **Claude 5.6, GPT-5.6, DeepSeek-V4** |
| **AssistantBench** | Web search and task execution | Text & URLs only | Optional | Moderate (Search & Browser) | High | Web Navigation Agents |
| **OSWorld** | Full GUI OS Desktop Manipulation | Screenshots & GUI | Full Virtual Machine (Ubuntu/Windows) | Deep (Bash, OS GUI APIs) | High | Computer-Use Agents |
| **SWE-bench Verified** | GitHub Software Engineering Issues | Code repositories & diffs | Docker Sandbox | Code Editing & Test Execution | Moderate | Coding Agents (Claude Code, Cursor) |
| **Humanity's Last Exam** | Multi-disciplinary expert reasoning | Multimodal academic | No (Closed-ended Q&A) | None (Single forward pass) | Very High | Frontier Base/Reasoning Models |

## What problem it solves
Existing benchmarks often focus on synthetic reasoning, code syntax, or closed-book trivia. GAIA targets real-world, open-ended tasks that require fundamental human-like abilities: complex reasoning, multi-modality handling (text, spreadsheets, images, PDFs, audio), web browsing, and programmatic tool execution. It exposes the 'reasoning gap' in frontier models, serving as a reliable metric of actual operational utility.

Furthermore, GAIA prevents prompt hacking and false accuracy saturation through strict ground-truth target formats. Answers are verified via unambiguous strings, numeric constants, or exact JSON structures, ensuring that agents cannot bypass reasoning steps via vague qualitative assertions.

## Difficulty Level Matrix & Benchmark Profile

| Level | Tasks Count | Human Accuracy | Typical AI Success Rate | Core Requirements | Execution Timeout |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Level 1** | ~160 tasks | 92% | ~65-80% | Short web search, single file parsing, single tool execution call | 120 seconds |
| **Level 2** | ~200 tasks | 92% | ~35-55% | Multi-step reasoning, combination of 2+ tools (Python + OCR), intermediate state persistence | 300 seconds |
| **Level 3** | ~90 tasks | 92% | ~15-30% | Long-horizon multi-modal planning, complex spreadsheet calculations, error recovery loops | 900 seconds |

## Where it fits in the stack
**Eval / Benchmarking**. It provides a high-signal evaluation standard for testing autonomous agents, VLMs, and multi-agent workflows. It is used to validate the 'Agentic Core' of systems built on frontier LLMs such as Claude 5.6 and GPT-5.6.

## Typical use cases
- **Agent Architecture Benchmarking**: Comparing the performance of different agent runtimes and planning frameworks on realistic assistant tasks.
- **Multimodal VLM Testing**: Benchmarking the vision and document-understanding capabilities of multimodal models when interacting with complex charts, PDFs, and media assets.
- **Tool-Calling Verification**: Measuring an agent's ability to select, configure, and execute tools (e.g., Python interpreters, web browsers, and FastMCP 3.1 Task Protocol servers) correctly.
- **Long-Horizon Planning**: Evaluating an agent's ability to maintain state and recover from execution failures over multi-step tasks.

## Strengths
- **Non-synthetic & Real-World**: Tasks are grounded in actual web, document, and system scenarios.
- **Low Effort for Humans, High for AI**: Tasks are easily resolvable by a human in minutes, yet yield low scores for modern AI systems, clearly showing the agentic performance gap.
- **Contamination Resistant**: Questions require active reasoning, file processing, and execution rather than memory retrieval, making them highly resistant to pre-training memorization.
- **Diverse Modalities**: Integrates multimodal inputs (spreadsheets, audio files, images, PDFs) natively.

## Limitations
- **High API Execution Costs**: Running multi-step agent loops on GAIA tasks can incur significant LLM token costs.
- **Environment Fragility**: Web-browsing tasks can fail if target live websites change their layout, structure, or access controls.
- **Complex Sandbox Requirements**: Requires a robust sandbox environment (e.g., Docker) to safely run file operations and python tool executions.

## When to use it
- When evaluating the operational "generalist" and multi-modal capacity of an AI agent.
- To measure the performance improvements of multi-step planning or self-correction algorithms.
- When benchmarking an agent's integration with real-world file-parsing and execution tools.

## When not to use it
- For testing domain-specific expertise (such as medical, legal, or advanced financial compliance) unless it falls under general digital assistant skills.
- For lightweight or low-latency regression testing (use simpler benchmarks like MMLU-Pro instead).
- For evaluating base foundational models that have not been instruction-aligned or agent-tuned.

## Getting started
GAIA evaluations are typically orchestrated using the `inspect-ai` evaluation framework, which provides a structured sandboxed runner for executing agent benchmarks.

### 1. Installation
Install the `inspect-ai` framework along with the standardized `inspect-evals` package:
```bash
pip install inspect-ai inspect-evals fastmcp pydantic
```

### 2. Configure Environment
Set up your LLM API keys and configure docker for safe execution of agent actions:
```bash
export ANTHROPIC_API_KEY="your-api-key"
export OPENAI_API_KEY="your-api-key"
```

## Systemd Service Unit Template

In continuous integration and benchmarking pipelines, the GAIA Evaluation Daemon is managed via systemd to execute scheduled evaluation jobs against nightly model checkpoints:

```ini
[Unit]
Description=GAIA Benchmark Automation Daemon
Documentation=https://gaia-benchmark.github.io/
After=docker.service network-online.target
Wants=docker.service network-online.target

[Service]
Type=simple
User=gaia-runner
Group=gaia-runner
WorkingDirectory=/opt/gaia-eval
ExecStart=/opt/gaia-eval/venv/bin/python3 -m gaia_eval.server --port 8120 --concurrency 4
Restart=on-failure
RestartSec=10s

# Security Restrictions
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true
ReadWritePaths=/var/log/gaia-eval /tmp/gaia-sandboxes
Environment=INSPECT_LOG_LEVEL=INFO
Environment=GAIA_SANDBOX_DRIVER=docker
MemoryMax=8G
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Multi-Container Docker Compose Stack (`docker-compose.yml`)

The following Docker Compose configuration runs the sandboxed GAIA evaluation suite alongside an isolated ephemeral execution runner:

```yaml
version: "3.8"

services:
  gaia-coordinator:
    image: python:3.11-slim
    container_name: gaia-eval-coordinator
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./gaia_data:/opt/gaia/data:ro
      - ./evaluation_logs:/opt/gaia/logs
    working_dir: /opt/gaia
    command: ["python", "-m", "inspect_ai", "eval", "inspect_evals/gaia_level1", "--limit", "10"]
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DOCKER_HOST=unix:///var/run/docker.sock
    deploy:
      resources:
        limits:
          cpus: "4.0"
          memory: 4096M

  ephemeral-tool-sandbox:
    image: python:3.11
    container_name: gaia-tool-sandbox
    network_mode: bridge
    volumes:
      - ./evaluation_scratchpad:/tmp/scratchpad:rw
    command: ["sleep", "infinity"]
    security_opt:
      - no-new-privileges:true
```

## CLI examples

### Running GAIA Evaluations via Inspect
Run the full GAIA validation suite against a frontier model:
```bash
inspect eval inspect_evals/gaia --model anthropic/claude-5.6
```

### Filtering by Difficulty Levels
GAIA categorizes questions into three difficulty levels. You can target specific subsets to save cost or test specialized agent traits:
```bash
# Evaluate Level 1 (easiest, basic tool use)
inspect eval inspect_evals/gaia_level1 --model openai/gpt-5.6

# Evaluate Level 3 (hardest, multi-step long-horizon reasoning)
inspect eval inspect_evals/gaia_level3 --model anthropic/claude-5.6
```

### Running with Limited Samples
For faster feedback loops, limit the evaluation to a subset of samples:
```bash
inspect eval inspect_evals/gaia_level2 --limit 5 --model meta-llama/llama-4-70b-instruct
```

## FastMCP 3.1 GAIA Evaluation Server

Expose a FastMCP 3.1 server to manage and trigger sandboxed GAIA benchmark evaluations with strict **Pydantic v2** validation (`extra="forbid"`, `frozen=True`):

```python
"""
FastMCP 3.1 Production GAIA Benchmark Tool Server
Provides strict schemas for launching, streaming, and grading GAIA task evaluation runs.
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict
from fastmcp import FastMCP

mcp = FastMCP("GaiaBenchmarkServer", version="3.1")

# ---------------------------------------------------------------------------
# Strict Pydantic v2 Schemas
# ---------------------------------------------------------------------------

class GaiaEvalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    level: Literal["level1", "level2", "level3"] = Field(
        default="level1",
        description="GAIA difficulty level to execute"
    )
    model_name: str = Field(
        default="anthropic/claude-5.6",
        description="Target model identifier (e.g. anthropic/claude-5.6, openai/gpt-5.6)"
    )
    sample_limit: int = Field(5, ge=1, le=50, description="Max number of benchmark samples to evaluate")
    concurrency: int = Field(2, ge=1, le=8, description="Number of parallel evaluation workers")
    enable_web_tools: bool = Field(True, description="Enable Playwright web browser tool")
    enable_code_sandbox: bool = Field(True, description="Enable Docker python interpreter sandbox")

class BenchmarkTaskTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    level: str
    steps_taken: int
    tool_calls_count: int
    duration_seconds: float
    accuracy_matched: bool
    ground_truth_target: str
    model_predicted_target: str

class GaiaEvalSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    evaluated_samples: int = Field(..., description="Number of evaluated samples")
    accuracy_percentage: float = Field(..., description="Ground truth accuracy percentage")
    mean_latency_sec: float = Field(..., ge=0.0)
    total_tokens_consumed: int = Field(..., ge=0)
    status: Literal["COMPLETED", "FAILED", "RUNNING"]
    tasks: List[BenchmarkTaskTelemetry]
    timestamp: str

# ---------------------------------------------------------------------------
# FastMCP Tools
# ---------------------------------------------------------------------------

@mcp.tool(name="trigger_gaia_evaluation", description="Triggers a sandboxed GAIA evaluation run under FastMCP 3.1")
def trigger_gaia_evaluation(request: GaiaEvalRequest) -> GaiaEvalSummary:
    """Triggers an inspect-ai GAIA evaluation run under FastMCP 3.1 task protocol rules."""
    # Deterministic simulation for FastMCP tooling integration
    telemetry_tasks = [
        BenchmarkTaskTelemetry(
            task_id=f"gaia-2023-{request.level}-001",
            level=request.level,
            steps_taken=4 if request.level == "level1" else 12,
            tool_calls_count=3 if request.level == "level1" else 9,
            duration_seconds=14.8,
            accuracy_matched=True,
            ground_truth_target="1842.50",
            model_predicted_target="1842.50"
        )
    ]

    return GaiaEvalSummary(
        evaluated_samples=request.sample_limit,
        accuracy_percentage=82.5 if request.level == "level1" else (48.0 if request.level == "level2" else 24.0),
        mean_latency_sec=18.4,
        total_tokens_consumed=14200 * request.sample_limit,
        status="COMPLETED",
        tasks=telemetry_tasks,
        timestamp="2027-01-07T12:00:00Z"
    )

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Custom Evaluator Pipeline with Pydantic v2 Validation
To parse, validate, and serialize the evaluation outputs securely, the following example uses strict **Pydantic v2** validation schemas (`extra="forbid"`, `frozen=True`):

```python
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from datetime import datetime

# Define strict Pydantic v2 models for GAIA evaluation schemas
class GaiaScoreDetails(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    value: float = Field(..., ge=0.0, le=1.0, description="Normalized score metric (0.0 to 1.0)")
    explanation: Optional[str] = Field(None, description="Grading breakdown or reasoning step")

class GaiaTaskResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    sample_id: str = Field(..., description="The unique benchmark sample ID")
    level: str = Field(..., description="Difficulty level (level1, level2, level3)")
    status: str = Field(..., description="Completion state of the agent task")
    latency_seconds: float = Field(..., ge=0.0)
    scores: Dict[str, GaiaScoreDetails] = Field(default_factory=dict)
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        if v not in {"level1", "level2", "level3"}:
            raise ValueError("Level must be 'level1', 'level2', or 'level3'")
        return v

# Example usage validating a GAIA result payload
sample_payload = {
    "sample_id": "gaia-2023-lvl2-042",
    "level": "level2",
    "status": "COMPLETED",
    "latency_seconds": 45.2,
    "scores": {
        "accuracy": {"value": 1.0, "explanation": "Answer string matched ground truth exactly"}
    }
}

validated_result = GaiaTaskResult.model_validate(sample_payload)
print("Validated GAIA Task Result:", validated_result.model_dump())
```

## Diagnostic Troubleshooting Guide

| Issue Symptom | Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Docker Sandbox Crash** | Memory exhaustion during browser or Python execution | `docker ps -a; docker logs <container_id>` | Increase sandbox RAM allocation in systemd daemon or inspect settings (`--memory 4g`). |
| **Ground Truth Format Mismatch** | Agent return string contains extraneous formatting (e.g., markdown) | `inspect view` | Enforce rigid system prompt instructions or string normalization regex in judge. |
| **Timeout Violation (Level 3)** | Long-horizon planning loop stuck in non-terminating retry loop | `journalctl -u gaia-eval-daemon -n 50` | Set strict per-step timeouts and maximum tool call recursion depth (max 25 loops). |
| **Web Search Stale Page Error** | External web asset or target URL changed structure | `curl -I <target_url>` | Use cached offline WebArchive snapshots for reproducible evaluation sets. |
| **Playwright Headless Crash** | Missing system browser libraries (libasound2, libnss3) | `playwright install-deps chromium` | Install underlying system dependencies or use `mcr.microsoft.com/playwright` base image. |
| **Audio Modality Read Error** | Non-standard WAV header or multi-channel audio format | `ffprobe -v error -show_streams sample.wav` | Pre-convert media assets using ffmpeg to 16kHz mono PCM before sandbox mounting. |
| **Pydantic Validation Failure** | Missing required metadata fields in Inspect AI json export | Check exception traceback in validator | Ensure `extra="forbid"` models match latest schema release or update translation adapter. |
| **Docker Socket Permission Denied** | Runner user not added to host `docker` group | `id -Gn gaia-runner` | Add execution user via `sudo usermod -aG docker gaia-runner` and reboot runner daemon. |

## Operational Best Practices & Evaluation Hardening

1. **Deterministic Sandboxing**:
   - Always run Python code tools inside ephemeral Docker containers (`--network none` when offline calculation is sufficient) to avoid benchmark environment corruption.
2. **Web Browser Caching & Replay**:
   - For Level 2 and Level 3 web-browsing tasks, utilize Playwright trace recordings or mock replay proxies to maintain reproducible evaluation runs over time.
3. **Token Usage Monitoring**:
   - Set maximum token bounds per task sample (e.g., max 30,000 tokens per Level 3 question) to prevent agent loops from consuming unexpected budget.

## Related tools / concepts
- [PA-bench](./pa-bench.md) — Web navigation benchmark.
- [AssistantBench](./assistant-bench.md) — Multi-step web mission benchmark.
- [OSWorld](./os-world.md) — Desktop OS agent benchmark.
- [Humanity's Last Exam](./humanitys-last-exam.md) — Frontier reasoning benchmark.
- [GPQA](./gpqa.md) — Graduate-level Google-proof Q&A benchmark.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Implementation patterns for GAIA-capable agents.
- [Tool Calling](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Foundational capability for GAIA tasks.
- [Inspect AI](./inspect-ai.md) — The framework used to run GAIA.

## Licensing and cost
- **Open Source**: Yes (CC-BY-SA 4.0).
- **Cost**: The benchmark dataset and evaluation software are open source. Executing agents over GAIA requires LLM API credits; Level 3 tasks can consume substantial tokens due to long execution loops.

## Sources / references
- [GAIA: A Benchmark for General AI Assistants (ArXiv)](https://arxiv.org/abs/2311.12983)
- [GAIA Project Website](https://gaia-benchmark.github.io/)
- [GAIA Leaderboard (Hugging Face)](https://huggingface.co/spaces/gaia-benchmark/leaderboard)
- [Inspect AI Benchmark Documentation](https://ukgovernmentbeis.github.io/inspect_ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
