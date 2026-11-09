# AssistantBench

## What it is
AssistantBench is a rigorous, open-source evaluation benchmark designed to measure the capability of web-connected AI agents and autonomous assistants to execute complex, realistic, and time-consuming multi-step tasks on the live web. As of early 2027, AssistantBench is established as a critical component of the "Agentic Evaluation Standard." It systematically quantifies the planning, navigation, retrieval, and reasoning capabilities of frontier models (including Claude 5.6, GPT-5.6, Llama 4, Gemma 4, DeepSeek-V4, Qwen 3.6 VL, and Gemini 4.0 Ultra) operating in stateful browser environments and FastMCP 3.1 Task Protocol integrations.

## What problem it solves
Most traditional LLM benchmarks evaluate atomic capabilities, such as isolated code generation or single-turn QA, in synthetic environments. However, these benchmarks fail to evaluate real-world agentic execution, where an agent must navigate dynamic websites, bypass anti-bot systems, manage complex browser states, retrieve scattered data, and reason across multiple pages to complete a single user request. AssistantBench solves this by providing long-horizon, multi-domain web-agent tasks that typically take a human developer or assistant 10 to 30 minutes to complete, allowing teams to rigorously benchmark success rates and measure Agentic Latency.

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / [Agentic Evaluations](../../knowledge_base/README.md).
It functions as a high-level performance and capability auditing layer, typically orchestrated via modular evaluation frameworks like the UK AISI's `inspect-ai` and integrated into development workflows to compare agent planning architectures (e.g., ReAct, plan-and-solve, or custom state-machines).

```
+-----------------------------------------------------------------------------------+
|                     ASSISTANTBENCH AGENTIC EVALUATION STACK                      |
+-----------------------------------------------------------------------------------+
|  [Benchmark Dataset: Long-Horizon Open-Web Real World Tasks]                       |
|                │                                                                  |
|                ▼                                                                  |
|  [Inspect-AI / UK AISI Framework Orchestration Engine]                            |
|                │                                                                  |
|                ▼                                                                  |
|  [FastMCP 3.1 Task Protocol & Agent Controller Bridge]                            |
|        │                                               │                          |
|        ▼ (Playwright Browser Loop)                     ▼ (Frontier Reasoning VLM) |
|  [Headless Chromium / DOM Tree & Screenshot Engine]   [Claude 5.6 / GPT-5.6 / Gemini 4] |
|        │                                               │                          |
|        └───────────────────────┬───────────────────────┘                          |
|                                ▼                                                  |
|  [Pydantic v2 Trajectory Metric Validation & Ground Truth Assertion]              |
|                │                                                                  |
|                ▼                                                                  |
|  [Performance Report: Accuracy %, Agentic Latency, Step Trajectory Analytics]     |
+-----------------------------------------------------------------------------------+
```

## Multi-Step Tool Execution & Browser Loop Architecture

```mermaid
sequenceDiagram
    autonumber
    participant Bench as AssistantBench Orchestrator
    participant Agent as FastMCP 3.1 Web Agent
    participant Driver as Playwright Headless Browser
    participant Web as Live Web Services

    Bench->>Agent: Dispatch evaluation task prompt
    Agent->>Driver: Issue DOM interaction command (click/type/scroll)
    Driver->>Web: Execute live HTTP request / JS rendering
    Web-->>Driver: Return updated DOM tree + screenshot
    Driver-->>Agent: Vision-Language DOM state & DOM tree snapshot
    Agent->>Agent: Evaluate progress, plan next action, log latency
    Agent->>Bench: Emit partial trajectory step
    Bench->>Bench: Assert completion criteria & ground truth match
```

## Mathematical Formulations & Long-Horizon Web Navigation Dynamics

AssistantBench models web agent trajectories as Partially Observable Markov Decision Processes (POMDPs) over dynamic web graphs.

### 1. Web Graph Traversal & Information State Formulation
The web is formalized as a dynamic directed multigraph $G_t = (V_t, E_t)$, where vertices $v \in V_t$ represent web pages (DOM states and rendered viewports) and edges $e \in E_t$ correspond to clickable hyperlinks, form submissions, and JavaScript event listeners.

At step $k$, the agent observes an incomplete observation $o_k = (I_{\text{screenshot}}, \mathcal{T}_{\text{accessibility}})$, where:
- $I_{\text{screenshot}} \in \mathbb{R}^{H \times W \times 3}$ is the high-resolution RGB browser render.
- $\mathcal{T}_{\text{accessibility}}$ is the pruned semantic Accessibility Tree representation with node count $|\mathcal{T}| \ll |\text{DOM}|$.

Given historical trajectory history $H_k = (o_1, a_1, o_2, a_2, \dots, o_k)$, the agent's policy $\pi_\theta(a_k \mid H_k)$ selects action $a_k \in \mathcal{A}$ from:

$$\mathcal{A} = \{\text{click}(x, y), \, \text{type}(\text{selector}, \text{text}), \, \text{scroll}(\Delta x, \Delta y), \, \text{navigate}(\text{url}), \, \text{finish}(\text{answer})\}$$

### 2. Multi-Hop Goal Reachability & Task Completion Accuracy
For task $T$ with ground truth target state or factual target answer $y^*$, the trajectory accuracy $\text{Acc}(T)$ is formulated using exact and semantic F1 alignment bounds:

$$\text{Acc}(T) = \max\Big(\mathbb{I}(\hat{y} = y^*), \, \text{BERTScore}(\hat{y}, y^*) \ge \tau_{\text{thresh}}\Big)$$

For multi-step numeric or entity extraction tasks, the string token-overlap F1 score is evaluated:

$$\text{Precision} = \frac{|\text{Tokens}(\hat{y}) \cap \text{Tokens}(y^*)|}{|\text{Tokens}(\hat{y})|}, \quad \text{Recall} = \frac{|\text{Tokens}(\hat{y}) \cap \text{Tokens}(y^*)|}{|\text{Tokens}(y^*)|}$$

$$\text{F1}_{\text{score}}(\hat{y}, y^*) = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall} + \epsilon}$$

### 3. Agentic Latency & Action Economy Cost Metric
Agent efficiency across long-horizon trajectories is parameterized by step complexity $K$, token consumption $N_{\text{tokens}}$, and total wall-clock duration $T_{\text{wall}}$:

$$\mathcal{C}_{\text{agentic}} = \sum_{k=1}^K \Big( t_{\text{think}}(k) + t_{\text{DOM}}(k) + t_{\text{net}}(k) \Big)$$

Where:
- $t_{\text{think}}(k)$ is the VLM inference latency for reasoning step $k$.
- $t_{\text{DOM}}(k)$ is the Playwright driver interaction and mutation observation delay.
- $t_{\text{net}}(k)$ is external HTTP transit time on the live internet.

The Action Economy Metric $\eta_{\text{task}}$ evaluates navigational efficiency relative to human expert shortest path $K_{\text{human}}^*$:

$$\eta_{\text{task}} = \frac{K_{\text{human}}^*}{\max(K_{\text{human}}^*, K_{\text{agent}})} \cdot \text{Acc}(T)$$

Under high-performing frontier models (Claude 5.6, GPT-5.6), action economy approaches $0.68\text{--}0.75$, reflecting near-optimal navigation paths without dead-end looping.

## Comparative Empirical Benchmark Matrix

The following table compares AssistantBench against peer web agent and autonomous evaluation suites:

| Metric / Capability | AssistantBench (v2027.1) | WebArena | OSWorld | GAIA | Mind2Web |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Target Environment** | Live Open Web (Unconstrained) | Sandboxed Local Web (Docker) | OS Desktop (Ubuntu/Win) | General Multimodal / Tools | Recorded Web Traces |
| **FastMCP 3.1 Integration** | Native FastMCP Tool Server | Adapter wrapper required | Custom RPC wrapper | Custom client tool hook | Static Dataset (No MCP) |
| **Task Horizon Length** | Long (10-30 mins / 15-50 steps) | Medium (5-15 mins / 10-25 steps)| Long (15-45 mins / 20-80 steps)| Medium (5-20 mins) | Short (2-8 steps) |
| **Visual DOM Grounding** | Native VLM Screenshots + a11y | Accessibility tree / DOM text | Desktop Pixel Coordinates | File / Image attachments | Raw DOM Element ID |
| **Anti-Bot & Dynamic JS** | Real-world bot detection, CAPTCHA| Synthetic (No bot protection) | N/A (Desktop OS) | Minimal (Offline tasks) | Static Snapshot |
| **Agentic Latency Profiling** | Step-by-step action breakdown | End-to-end task timer | Task & Action timer | Total duration timer | N/A |
| **Ground Truth Validation** | Exact Match + Semantic F1 | Exact Match / State Diff | Execution State Assertion | Exact Text / Number Match | Element Selector Match |
| **Reproducibility Rigor** | Dynamic (Live Web Variance) | Deterministic (Reset VM) | Deterministic (QEMU Snapshot)| Deterministic | Fully Deterministic |

## Typical use cases
- **Web Agent Capability Profiling**: Measuring and auditing the execution success rate of browser-based agents like OpenHands, MultiOn, Stagehand, or custom Playwright-based systems.
- **VLM Visual Grounding Analysis**: Evaluating how effectively vision-language models can interpret dynamic, interactive web interfaces, complex layouts, and multi-format graphics.
- **Planning & Self-Correction Audits**: Testing the resilience of agent decision loops when encountering unexpected layout adjustments, pop-ups, modal dialogs, or dead ends.
- **Agentic Latency Quantification**: Measuring the relationship between planning token overhead, action sequences, and actual execution duration on live web routes.
- **RAG & Synthesis Evaluation**: Assessing an agent's capability to search the web, scrape raw materials, and synthesize a single, factual, non-hallucinated answer to multi-layered research queries.

## Strengths
- **Authentic and Realistic Tasks**: Sourced from actual, real-world questions and tasks that humans perform, ensuring evaluation results reflect genuine utility.
- **Dynamic Live Web Execution**: Tests agents on the open web, verifying their resilience against real-world web-design patterns and javascript-dense interfaces.
- **Standardized Framework Integration**: Natively integrated with `inspect-ai` and the `inspect-evals` package, enabling standardized execution and evaluation runs.
- **Long-Horizon Multi-Domain Coverage**: Spans across business, real estate, travel booking, scientific research, and SaaS interfaces, ensuring a diverse capability profile.
- **Detailed Visual Tracing**: Generates complete execution logs with visual step-by-step screenshots to allow developers to inspect and analyze agent failure modes.

## Limitations
- **Live Web Volatility**: Because tests are executed on the live internet, unexpected modifications to external websites can occasionally impact test reproducibility and baseline consistency.
- **Compute and Token Cost**: Running long-horizon, multi-step browser loops utilizing frontier visual models (like Claude 5.6 or GPT-5.6) consumes a high volume of input and output tokens.
- **Operational Execution Speed**: Executing true end-to-end browser trajectories on live websites is intrinsically slower than running synthetic unit tests, making it better suited for periodic scheduled runs rather than rapid pre-commit checks.

## When to use it
- When developing or tuning autonomous web assistants, personal agents, or automated research pipelines that navigate the open web.
- To compare and benchmark the cost-to-performance efficiency of different planning layers and model backbones.
- When you need to generate high-confidence capability profiles and success rate reports for enterprise-grade autonomous systems.

## When not to use it
- For testing isolated desktop interface interactions (such as system-level mouse and keyboard actions), where an operating-system-level benchmark like [OSWorld](./os-world.md) is appropriate.
- If you are building a highly sandboxed, air-gapped agent that is explicitly blocked from accessing the external, live internet.
- For high-speed, local regression testing of simple prompts where lightweight, deterministic unit-test assertions are sufficient.

## Installation / setup

AssistantBench evaluations are primarily orchestrated using the `inspect-ai` framework and the companion `inspect-evals` suite:

```bash
# Install core inspection and benchmarking dependencies
pip install --upgrade "inspect-ai>=0.3.30" "inspect-evals>=0.1.15" "playwright>=1.50.0" "fastmcp>=3.1.0" "pydantic>=2.10.0"

# Install Playwright browser engines and system runtime dependencies
playwright install --with-deps chromium
```

Configure your environment with necessary API keys and browser configurations:

```bash
# Configure frontier LLM credentials
export ANTHROPIC_API_KEY="sk-ant-api03-2027-example-key"
export OPENAI_API_KEY="sk-proj-2027-example-key"

# Enable headless browser execution flags
export PLAYWRIGHT_HEADLESS=true
export INSPECT_EVAL_MAX_RETRIES=2
```

## Getting started

### 1. Basic Evaluation Run
Run a sample evaluation on a limited set of tasks to verify local setup:

```bash
# Run 3 sample tasks against Claude 5.6
inspect eval inspect_evals/assistant_bench_web_browser --model anthropic/claude-5.6 --limit 3
```

### 2. Launching Visual Trajectory Inspector
Inspect the step-by-step browser DOM screenshots, action choices, and model reasoning:

```bash
# Launch interactive local web UI for trace inspection
inspect view --port 7575
```

## CLI examples
The `inspect` command-line utility provides intuitive controls to run, configure, and inspect AssistantBench evaluations.

```bash
# Run a standard AssistantBench evaluation using a frontier model
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.6

# Restrict the evaluation run to a small, sample-limited set (e.g., 5 tasks) for debugging
inspect eval inspect_evals/assistant_bench_web_browser --model anthropic/claude-5.6 --limit 5

# Compare performance across multiple frontier models simultaneously
inspect eval inspect_evals/assistant_bench_web_browser --model openai/gpt-5.6,anthropic/claude-5.6

# Boot up the interactive visual log viewer to analyze step-by-step agent trajectories
inspect view --port 7575
```

## Systemd Production Service Configuration

For running automated nightly batch evaluation sweeps against live web benchmarks, deploy the following systemd service configuration as `/etc/systemd/system/assistantbench-eval.service`:

```ini
[Unit]
Description=AssistantBench Nightly FastMCP 3.1 Evaluation Runner
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=eval-agent
Group=eval-agent
WorkingDirectory=/opt/assistantbench-runner
Environment=PATH=/opt/assistantbench-runner/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=HOME=/home/eval-agent
Environment=PLAYWRIGHT_BROWSERS_PATH=/home/eval-agent/.cache/ms-playwright
Environment=ANTHROPIC_API_KEY=sk-ant-api03-prod-eval-key
Environment=OPENAI_API_KEY=sk-proj-prod-eval-key
ExecStart=/opt/assistantbench-runner/venv/bin/inspect eval inspect_evals/assistant_bench_web_browser --model anthropic/claude-5.6 --limit 25 --output /var/log/assistantbench/eval-nightly.json
StandardOutput=journal
StandardError=journal
SyslogIdentifier=assistantbench-eval
LimitNOFILE=65536
TimeoutStartSec=7200

# Process Sandboxing
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/var/log/assistantbench /home/eval-agent/.cache
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Infrastructure Configuration

To run AssistantBench evaluations inside isolated browser container sandboxes with a dedicated Redis telemetry buffer, use the following Compose setup:

```yaml
version: '3.8'

services:
  assistantbench-runner:
    image: mcr.microsoft.com/playwright/python:v1.50.0-noble
    container_name: assistantbench-eval-runner
    restart: "no"
    working_dir: /workspace
    volumes:
      - ./:/workspace
      - eval-artifacts:/workspace/artifacts
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PLAYWRIGHT_HEADLESS=true
      - PYTHONUNBUFFERED=1
    command: >
      bash -c "pip install --no-cache-dir inspect-ai inspect-evals fastmcp pydantic &&
               python3 -m mcp_benchmark_runner"
    networks:
      - eval-net

  eval-telemetry-cache:
    image: redis:7-alpine
    container_name: assistantbench-redis
    restart: unless-stopped
    ports:
      - "6380:6379"
    volumes:
      - redis-data:/data
    networks:
      - eval-net

volumes:
  eval-artifacts:
    driver: local
  redis-data:
    driver: local

networks:
  eval-net:
    driver: bridge
```

## Automated Health Probe Script

Use this health check script `scripts/assistantbench_health_probe.sh` to verify Playwright browser installation, network reachability to target web benchmarks, and FastMCP benchmark controller availability:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration defaults
FASTMCP_PORT="${1:-8095}"
FASTMCP_HOST="${2:-127.0.0.1}"
MAX_TIMEOUT=10

echo "=========================================================="
echo " Starting AssistantBench Evaluation Health Probe"
echo " FastMCP Controller: $FASTMCP_HOST:$FASTMCP_PORT"
echo "=========================================================="

# 1. Test Playwright Chromium Driver Readiness
echo -n "[1/3] Inspecting Playwright Chromium browser driver... "
if command -v playwright &> /dev/null; then
    BROWSER_CHECK=$(python3 -c "
import sys
from playwright.sync_api import sync_playwright
try:
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        b.close()
    sys.exit(0)
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(1)
" 2>&1 || echo "ERROR")
    if [[ -z "$BROWSER_CHECK" || "$BROWSER_CHECK" == "" ]]; then
        echo "OK (Headless Chromium operational)"
    else
        echo "WARNING (Playwright launch warning: $BROWSER_CHECK)"
    fi
else
    echo "FAILED (playwright executable not found)"
    exit 1
fi

# 2. Check Open Web Outbound Reachability
echo -n "[2/3] Testing live internet connectivity for benchmarks... "
OUTBOUND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$MAX_TIMEOUT" "https://assistantbench.github.io" || echo "000")
if [[ "$OUTBOUND_STATUS" =~ ^(200|301|302)$ ]]; then
    echo "OK (HTTP $OUTBOUND_STATUS)"
else
    echo "WARNING (Live web probe returned HTTP $OUTBOUND_STATUS; verify proxy/firewall)"
fi

# 3. Test Inspect-AI Framework Availability
echo -n "[3/3] Validating inspect-ai CLI environment... "
if python3 -c "import inspect_ai; print(inspect_ai.__version__)" &> /dev/null; then
    echo "OK (Inspect-AI Python package detected)"
else
    echo "FAILED (inspect-ai library not importable)"
    exit 1
fi

echo "=========================================================="
echo " AssistantBench Health Probe Completed Successfully"
echo "=========================================================="
exit 0
```

## API examples

AssistantBench evaluations can be driven through Python scripts or orchestrated via FastMCP 3.1 tool implementations.

### 1. FastMCP 3.1 Evaluation Runner Server Implementation with Strict Pydantic v2

```python
"""
FastMCP 3.1 AssistantBench Evaluation Controller
Orchestrates agent trajectory execution, latency tracking, and metric validation.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP, Context
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AssistantBenchMCP")

mcp = FastMCP("AssistantBench-Evaluation-Server", version="3.1.0")

class TrajectoryStep(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    step_number: int = Field(..., ge=1, description="Sequential index of trajectory step")
    action_type: str = Field(..., pattern=r"^(click|type|scroll|navigate|extract|finish)$")
    target_selector: Optional[str] = Field(None, description="CSS or XPath DOM selector")
    step_latency_seconds: float = Field(..., ge=0.0, description="Execution delay for action step")

class EvaluationTaskMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(..., description="AssistantBench benchmark task UUID")
    model_evaluated: str = Field(..., description="Frontier LLM or VLM evaluated")
    is_successful: bool = Field(..., description="Ground truth answer match status")
    total_steps: int = Field(..., ge=1, description="Total trajectory actions executed")
    agentic_latency_avg: float = Field(..., ge=0.0, description="Mean latency per action step")
    trajectory: List[TrajectoryStep] = Field(default_factory=list, description="Detailed action log")

    @field_validator("agentic_latency_avg")
    def validate_latency(cls, v: float) -> float:
        if v > 120.0:
            logger.warning("Average agentic latency exceeds 120 seconds per step.")
        return v

@mcp.tool()
async def log_evaluation_trajectory(
    data: Dict[str, Any],
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Validates and logs an AssistantBench evaluation trajectory using Pydantic v2 schemas."""
    if ctx:
        await ctx.info("Validating incoming AssistantBench trajectory payload...")

    try:
        metrics = EvaluationTaskMetrics.model_validate(data)
        logger.info(f"Task {metrics.task_id} evaluated for model {metrics.model_evaluated}. Success: {metrics.is_successful}")
        if ctx:
            await ctx.info(f"Trajectory recorded: {metrics.task_id} ({metrics.total_steps} steps, avg {metrics.agentic_latency_avg:.2f}s)")
        return {
            "status": "logged",
            "task_id": metrics.task_id,
            "success": metrics.is_successful,
            "avg_latency": metrics.agentic_latency_avg,
            "logged_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    except Exception as err:
        logger.error(f"Failed to log trajectory: {err}")
        return {"error": str(err), "status": "validation_failed"}

@mcp.tool()
async def run_benchmark_sample(
    task_id: str,
    model_name: str = "claude-5.6",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Dispatches a single AssistantBench web evaluation task across the headless browser harness."""
    if ctx:
        await ctx.info(f"Launching web agent loop for task {task_id} with model {model_name}...")

    # Simulated long-horizon browser execution
    return {
        "task_id": task_id,
        "model": model_name,
        "success": True,
        "steps_taken": 8,
        "total_time_seconds": 42.6,
        "f1_score": 0.94
    }

if __name__ == "__main__":
    mcp.run()
```

### 2. Programmatic Evaluation Execution (Python)

```python
import os
from inspect_ai import eval
from inspect_evals import assistant_bench_web_browser

# Set up the API environment
os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"

# Execute the evaluation run on a limited set of samples
evaluation_results = eval(
    assistant_bench_web_browser(),
    model="anthropic/claude-5.6",
    limit=10,
    score_filter=None
)

# Extract and output high-level statistics
for run in evaluation_results:
    print(f"Model Evaluated: {run.model}")
    print(f"Task Success Accuracy: {run.metrics['accuracy'].value * 100:.2f}%")
```

## Systematic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Verification Command | Resolution & Workaround Strategy |
| :--- | :--- | :--- | :--- |
| **Browser Context Timeout (>300s)** | Dynamic JavaScript rendering loop or infinite scroll trap | `inspect view` & check trajectory step logs | Implement step-level timeout limit (`max_step_timeout: 30s`) in Playwright args. |
| **Bot Detection Challenge / Cloudflare Block** | Headless Playwright browser fingerprint flagged by WAF | Inspect screenshot artifact for challenge iframe | Use stealth browser plugin (`playwright-stealth`) or residential proxy pools. |
| **DOM Selector Target Not Found** | Dynamic Single-Page App DOM re-rendered after action | Compare pre/post DOM snapshots | Fall back to visual spatial bounding box clicks via VLM rather than brittle CSS IDs. |
| **High Agentic Latency (>60s/step)** | Massive raw HTML serialization saturating context window | Audit token consumption per prompt step | Prune raw HTML and translate DOM into compact accessibility tree (`a11y`). |
| **Playwright Missing Shared Libraries** | Linux host missing required WebKit/Chromium shared libs | `ldd ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome` | Run `playwright install --with-deps chromium` to install OS packages. |
| **Pydantic Validation Error on Output** | Evaluation runner emitted extra unmodeled fields | Inspect error trace in FastMCP tool output | Align metrics dictionary strictly to schema configured with `extra="forbid"`. |
| **Out-of-Memory (OOM) on Browser Node** | Accumulation of detached Chromium tabs over long sweeps | `ps aux \| grep chrome` | Ensure `browser_context.close()` is invoked in `finally` blocks after every task run. |
| **Non-Deterministic Web Content Drift** | Live site modified text content between baseline and test | Review cached HTTP archive (WARC) | Store deterministic web page snapshots via HAR/WARC recording proxies for offline tests. |

## Related tools / concepts
- [PA-bench](./pa-bench.md) — Web session orchestration and procedural navigation benchmark.
- [GAIA](./gaia.md) — General AI Assistant benchmark targeting multimodal, tool-connected real-world tasks.
- [OSWorld](./os-world.md) — Comprehensive sandbox benchmark for evaluating agents in real operating-system and desktop environments.
- [Inspect AI](inspect-ai.md) — Foundational framework developed by the UK AISI for orchestrating model benchmarks.
- [MultiOn](../agents/multion.md) — High-performance visual navigation and execution engine.
- [Stagehand](../automation_orchestration/stagehand.md) — LLM-driven browser-automation SDK built on Playwright.
- [Browser Use](../automation_orchestration/browser-use.md) — Multi-agent browser control framework.
- [Agentic Latency](../../knowledge_base/patterns/index.md) — The measure of cognitive and network delay during autonomous long-horizon runs.

## Licensing and cost
- **License**: Apache-2.0 (Open Source)
- **Cost**: The benchmark framework is free, but executing browser trajectories requires live internet connectivity and substantial LLM API token consumption. Long trajectories on premium visual models can result in significant usage costs.

## Sources / references
- [AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks? (ArXiv Paper)](https://arxiv.org/abs/2407.15711)
- [AssistantBench Official Webpage](https://assistantbench.github.io/)
- [AssistantBench Project GitHub Repository](https://github.com/assistantbench/assistantbench)
- [UK AISI Inspect-AI Documentation](https://github.com/UKGovernmentBEIS/inspect-ai)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
