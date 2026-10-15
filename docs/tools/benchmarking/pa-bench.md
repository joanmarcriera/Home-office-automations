# PA-bench

## What it is
PA-bench is a comprehensive benchmark suite designed to evaluate the performance of Personal Assistant (PA) web agents on real-world workflows. It utilizes simulated environments (e.g., mock Gmail, mock Google Calendar) to provide a safe, reproducible, and cost-effective testbed for early January 2027 agentic orchestration.

## Architecture & Agentic Simulation Flow

```
+-----------------------------------------------------------------------------------+
|                              PA-bench Execution Flow                              |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +--------------------+         +-----------------------+                         |
|  | Task Definition    | ------> | Experiment            |                         |
|  | Calendar/Email/Travel        | Orchestrator          |                         |
|  +--------------------+         +-----------+-----------+                         |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | Docker Simulation     |                         |
|                                 | Mock Gmail & GCal     |                         |
|                                 +-----------+-----------+                         |
|                                             |                                     |
|                        +--------------------+--------------------+                |
|                        |                                         |                |
|                        v                                         v                |
|           +-------------------------+               +-------------------------+   |
|           | Web Agent Execution     |               | FastMCP 3.1 Task Server |   |
|           | Headless Browser / MCP  |               | Trajectory Telemetry    |   |
|           +------------+------------+               +------------+------------+   |
|                        |                                         |                |
|                        +--------------------+--------------------+                |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | Deterministic State   |                         |
|                                 | Verifier              |                         |
|                                 +-----------+-----------+                         |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | Pydantic v2 Scorecard |                         |
|                                 | Metric Report         |                         |
|                                 +-----------------------+                         |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It addresses the lack of realistic evaluation frameworks for web-based agents by providing a set of complex, multi-step tasks that mirror actual user needs, such as booking travel, managing calendars, or conducting research across multiple websites. It is a critical tool for measuring "Agentic Session Orchestration" and risk mitigation in early 2027.

## Where it fits in the stack
**Eval**. It provides the metrics and environment necessary to measure the effectiveness and reliability of autonomous web agents. It is the gold standard for evaluating "Agentic Hooks" and side-panel integration in Chrome v145+/146+.

## Typical use cases
- **Agent Comparison**: Evaluating different agent architectures (e.g., Claude 5.6 vs. GPT-5.6 vs. Gemini 4.0 Ultra) on their ability to complete complex web tasks.
- **Regression Testing**: Ensuring that updates to an agent's reasoning or navigation logic don't break existing capabilities in the Ralph-loop.
- **Research**: Providing a standardized baseline for academic and industrial research into autonomous web navigation and "Computer Use" capabilities.
- **Security Auditing**: Testing agentic resilience against adversarial UI patterns using the SHARP (SharpAI Security Benchmark) methodology.

## Benchmark Comparison Matrix

| Benchmark Suite | Focus Domain | Execution Environment | Evaluation Metric | Interaction Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **PA-bench** | Personal Assistant / Web Apps | Mock Web Services (Docker) | State Verification & Trajectory Success | Browser Side-Panel / FastMCP 3.1 |
| **promptfoo** | LLM Prompt / Security / Red-Teaming | API / Simulated Prompts | Assertions / LLM-as-a-Judge | HTTP / REST API |
| **DeepEval** | LLM Quality & RAG Pipelines | Python In-Memory | Hallucination, Faithfulness, Toxicity | Python SDK / Pytest |
| **SWE-bench** | Software Engineering / GitHub | Docker Containers | Unit Test Pass Rate | Terminal / Git Commands |
| **OSWorld** | OS-Level GUI Control | QEMU VMs / Linux / Win / Mac | OS State / Pixels | VNC / OS API |
| **Terminal-bench** | Bash Command Line Tasks | Docker / Container Shell | Exit Code / File System State | PTY Shell Commands |

## Strengths
- **Real-world Focus**: Tasks are based on actual personal assistant workflows rather than synthetic laboratory examples.
- **End-to-End Evaluation**: Measures the agent's ability to see a task through from start to finish, including handling unexpected UI states.
- **Complexity**: Includes tasks that require multi-site navigation, state management, and interaction with JMAP/Graph APIs via FastMCP 3.1 Task Protocol.
- **Deterministic**: Simulated backends ensure that benchmark runs are reproducible and not subject to real-world data drift.

## Limitations
- **Environment Stability**: While simulations are more stable than the live web, maintaining them requires ongoing effort as real-world APIs evolve.
- **Resource Intensive**: Running full-scale web agent evaluations can be time and credit consuming, requiring significant inference budget in early 2027.
- **Not for Code-Gen**: Less effective for evaluating pure code generation or algorithmic reasoning (use [MBPP](mbpp.md) or [SWE-bench](swe-bench.md) for those).

## When to use it
- When developing or refining autonomous agents intended for web-based personal assistant tasks in 2027.
- When you need a high-signal metric for how well an agent handles real-world web complexity and "Computer Use".
- When validating "Agentic Calendar Orchestration" workflows.

## When not to use it
- For evaluating models on pure reasoning or coding tasks without a web navigation component.
- If you lack the infrastructure to run autonomous browser-based agents or the LiteLLM inference plane.
- For evaluating low-level text completion or translation tasks.

## Getting started

PA-bench is typically executed via its Python SDK, which manages simulated environments for email and calendar applications. It requires a local Docker environment for the simulation manager.

### 1. Installation
```bash
pip install pa-bench pydantic mcp
# Ensure Docker is running
docker pull vibrantlabs/pa-simulations:latest
```

### 2. Basic Configuration
Configure your agent's API access via environment variables or a `.env` file:
```bash
export ANTHROPIC_API_KEY="sk-..."
export OPENAI_API_KEY="sk-proj-..."
export PA_BENCH_MODE="simulation"
```

## FastMCP 3.1 Server Evaluation & Trajectory Logging

The following Python snippet implements a FastMCP 3.1 server designed to evaluate PA-bench task runs, record agent step trajectories, and return validated scorecard reports using Pydantic v2 schemas:

```python
import json
from typing import List, Optional
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, field_validator

# Initialize FastMCP 3.1 Server
mcp = FastMCP("pa-bench-evaluator", version="3.1.0")


class TrajectoryStepSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    step_num: int = Field(..., ge=1, description="Sequential step counter")
    action_type: str = Field(..., description="Action type: navigate, click, type, wait, verify")
    target_selector: Optional[str] = Field(None, description="CSS or XPath target element")
    input_text: Optional[str] = Field(None, description="Typed text payload")
    url: Optional[str] = Field(None, description="URL location during action execution")
    screenshot_b64: Optional[str] = Field(None, description="Base64 encoded screenshot image")


class EvaluationTaskRunSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    run_id: str = Field(..., min_length=5, description="Unique evaluation session ID")
    task_id: str = Field(..., description="PA-bench task identifier (e.g. 'calendar_sync_2027')")
    suite_category: str = Field(..., description="Suite category: travel, email, calendar, research")
    steps: List[TrajectoryStepSchema] = Field(default_factory=list)
    max_allowed_steps: int = Field(default=50, ge=5, le=200)
    is_completed: bool = Field(False)
    verification_passed: bool = Field(False)


@mcp.tool()
async def evaluate_task_trajectory(payload: EvaluationTaskRunSchema) -> dict:
    """Validate and evaluate a completed PA-bench task trajectory execution."""
    total_steps = len(payload.steps)
    step_efficiency = 1.0 - (total_steps / payload.max_allowed_steps)

    scorecard = {
        "run_id": payload.run_id,
        "task_id": payload.task_id,
        "suite_category": payload.suite_category,
        "total_steps": total_steps,
        "verification_status": "PASSED" if payload.verification_passed else "FAILED",
        "efficiency_score": max(0.0, round(step_efficiency, 2)),
        "timestamp": datetime.utcnow().isoformat()
    }
    return scorecard


if __name__ == "__main__":
    mcp.run()
```

## CLI examples

### Running a standard evaluation suite
Run the "Travel" category of tasks against an agent:
```bash
pa-bench run --suite travel --agent my_custom_agent --max_steps 50
```

### Running with visual diagnostics
Execute the benchmark while preserving visual trajectories, specifying a target output directory:
```bash
pa-bench run \
    --suite calendar_sync \
    --agent agent_claude_5_6 \
    --max_steps 75 \
    --visualize \
    --screenshot_dir ./diagnostics/screenshots/
```

### Listing available tasks
```bash
pa-bench list-tasks --category research
```

### Visualizing Agent Trajectories
Generate a video report of the agent's interaction:
```bash
pa-bench report --run_id RUN_123 --format webm
```

## API examples

### Trajectory Schema Validation & FastMCP 3.1 Integration
Using **Pydantic v2** and **FastMCP 3.1 Task Protocol**, we validate web agent trajectories generated during PA-bench runs before persisting them to the database or passing them to evaluation engines.

```python
import json
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server for PA-bench Trajectory Telemetry
mcp = FastMCP("PA-Bench-Evaluator", version="3.1")

class TrajectoryStep(BaseModel):
    step_num: int = Field(..., description="Chronological step number", ge=1)
    action: str = Field(..., description="Web action performed (click, type, navigate, wait)")
    url: Optional[str] = Field(None, description="URL where the action occurred")
    screenshot_path: Optional[str] = Field(None, description="Local path to screenshot artifact")

class PAEvaluationRun(BaseModel):
    run_id: str = Field(..., description="Unique run identifier")
    task_name: str = Field(..., description="Name of the task from PA-bench suite")
    started_at: datetime = Field(default_factory=datetime.utcnow, description="Evaluation run start time")
    steps: List[TrajectoryStep] = Field(default_factory=list, description="Sequence of actions taken by agent")
    is_success: bool = Field(False, description="Whether final verification check succeeded")

@mcp.tool(name="validate_pa_trajectory", description="Validates PA-bench trajectory execution data using strict Pydantic v2 schema.")
def validate_pa_bench_run(run_data: dict) -> str:
    try:
        validated = PAEvaluationRun.model_validate(run_data)
        return validated.model_dump_json(indent=2)
    except ValidationError as e:
        return json.dumps({"error": "Trajectory verification failed", "details": e.errors()})

if __name__ == "__main__":
    sample_run = {
        "run_id": "run-pa-9912",
        "task_name": "calendar_sync_2027",
        "is_success": True,
        "steps": [
            {
                "step_num": 1,
                "action": "navigate",
                "url": "http://gcal.mock-env.local",
                "screenshot_path": "./diagnostics/screenshots/step_01.png"
            }
        ]
    }

    print(validate_pa_bench_run(sample_run))
```

### Orchestrating an Evaluation
Integrate PA-bench into a CI/CD pipeline for agentic software factories.

```python
from pa_bench import SimulationManager, ExperimentOrchestrator
from my_agent import CustomWebAgent

# Initialize simulations (Gmail, GCal, etc.)
sim_manager = SimulationManager()
sim_manager.spawn_instances(apps=["gmail", "google_calendar"])

# Configure orchestrator with early January 2027 settings
orchestrator = ExperimentOrchestrator(
    agent=CustomWebAgent(model="claude-5-6-sonnet"),
    max_steps=75,
    resolution=(1280, 960),
    mcp_enabled=True,
    chrome_args=[
        "--enable-extension-hooks",
        "--side-panel-integration"
    ]
)

# Run benchmark suite
results = orchestrator.run_suite(tasks="calendar_sync_2027")
print(f"Success Rate: {results.success_rate}")
print(f"Mean Steps: {results.mean_steps_to_completion}")

# Cleanup
sim_manager.shutdown()
```

## Troubleshooting & Common Errors

| Error / Failure Mode | Cause | Resolution Strategy |
| :--- | :--- | :--- |
| `DOCKER_CONTAINER_TIMEOUT` | Simulation environment container failed to spawn within 30s. | Increase Docker memory limit to 8GB; restart `vibrantlabs/pa-simulations` daemon. |
| `SIDE_PANEL_HOOK_FAILED` | Chrome headless extension unable to attach to side-panel DOM context. | Ensure Chrome args include `--enable-extension-hooks` and update to Chrome v145+. |
| `STATE_VERIFICATION_MISMATCH` | Agent completed actions but backend DB verification script returned non-zero. | Check target mock API endpoint state; inspect `diagnostics/screenshots/` for UI navigation errors. |
| `MAX_STEPS_EXCEEDED` | Agent stuck in infinite UI interaction loop without reaching completion state. | Adjust prompt system instructions with clear stopping criteria or decrease element selector timeout. |
| `INFERENCE_RATE_LIMIT` | LLM provider API rate limit hit during multi-step browser interaction. | Configure LiteLLM proxy with fallback keys or apply retry backoff on API calls. |

## Production Validation Guardrails

1. **Simulated Isolation**: Always run PA-bench evaluations against isolated mock container enclaves to prevent unintended side effects on real user accounts.
2. **Determinism Verification**: Run 3 trials per task to calculate trajectory consistency and rule out stochastic prompt variance.
3. **Artifact Retention**: Store DOM snapshots, network HAR files, and step screenshots for every failed trajectory step to accelerate agent debugging.
4. **Token Cost Budgeting**: Set strict per-run token limits in LiteLLM or agent orchestrators to prevent budget exhaustion during agent loop bugs.
5. **Security Isolation**: Execute un-trusted agent code within unprivileged sandboxes to mitigate prompt injection risks targeting browser agents.

## Related tools / concepts
- [Web Agents](../../knowledge_base/agent_protocols.md) - Core architectural patterns.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) - Orchestration strategies.
- [OpenHands](../development_ops/openhands.md) - Open-source agentic development platform.
- [SWE-bench](./swe-bench.md) - Software engineering benchmark.
- [Terminal-bench](./terminal-bench.md) - Shell interaction benchmark.
- [GAIA (General AI Assistants)](gaia.md) - Real-world assistant tasks.
- [AssistantBench](assistant-bench.md) - Web-search and navigation benchmark.
- [OSWorld](./os-world.md) - Operating system-wide agent evaluation.
- [Skills in Chrome](../ai_knowledge/skills-in-chrome.md) - Browser-native agentic hooks in early 2027.
- [FastMCP 3.1 Task Protocol](../../knowledge_base/self-healing-agent-research.md) - The protocol for agentic tool use and tasks.

## Sources / references
- [PA-bench: Evaluating web agents on real world personal assistant workflows](https://vibrantlabs.com/blog/pa-bench)
- [Vibrant Labs GitHub Repository](https://github.com/vibrantlabsai/)
- [Agentic Session Orchestration 2027 Whitepaper](https://example.com/aso-2027)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
