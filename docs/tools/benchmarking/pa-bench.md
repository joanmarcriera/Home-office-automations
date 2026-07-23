# PA-bench

## What it is
PA-bench is a comprehensive benchmark suite designed to evaluate the performance of Personal Assistant (PA) web agents on real-world workflows. It utilizes simulated environments (e.g., mock Gmail, mock Google Calendar) to provide a safe, reproducible, and cost-effective testbed for July 2026 agentic orchestration.

## What problem it solves
It addresses the lack of realistic evaluation frameworks for web-based agents by providing a set of complex, multi-step tasks that mirror actual user needs, such as booking travel, managing calendars, or conducting research across multiple websites. It is a critical tool for measuring "Agentic Session Orchestration" and risk mitigation in July 2026.

## Where it fits in the stack
**Eval**. It provides the metrics and environment necessary to measure the effectiveness and reliability of autonomous web agents. It is the gold standard for evaluating "Agentic Hooks" and side-panel integration in Chrome v145+/146+.

## Typical use cases
- **Agent Comparison**: Evaluating different agent architectures (e.g., Claude 5.1 vs. GPT-5.5) on their ability to complete complex web tasks.
- **Regression Testing**: Ensuring that updates to an agent's reasoning or navigation logic don't break existing capabilities in the Ralph-loop.
- **Research**: Providing a standardized baseline for academic and industrial research into autonomous web navigation and "Computer Use" capabilities.
- **Security Auditing**: Testing agentic resilience against adversarial UI patterns using the SHARP (SharpAI Security Benchmark) methodology.

## Strengths
- **Real-world Focus**: Tasks are based on actual personal assistant workflows rather than synthetic laboratory examples.
- **End-to-End Evaluation**: Measures the agent's ability to see a task through from start to finish, including handling unexpected UI states.
- **Complexity**: Includes tasks that require multi-site navigation, state management, and interaction with JMAP/Graph APIs via MCP 3.0/3.1.
- **Deterministic**: Simulated backends ensure that benchmark runs are reproducible and not subject to real-world data drift.

## Limitations
- **Environment Stability**: While simulations are more stable than the live web, maintaining them requires ongoing effort as real-world APIs evolve.
- **Resource Intensive**: Running full-scale web agent evaluations can be time and credit consuming, requiring significant inference budget in July 2026.
- **Not for Code-Gen**: Less effective for evaluating pure code generation or algorithmic reasoning (use [MBPP](mbpp.md) or [SWE-bench](swe-bench.md) for those).

## When to use it
- When developing or refining autonomous agents intended for web-based personal assistant tasks in July 2026.
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
pip install pa-bench
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
    --agent agent_claude_5_1 \
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

### Orchestrating an Evaluation
Integrate PA-bench into a CI/CD pipeline for agentic software factories.

```python
from pa_bench import SimulationManager, ExperimentOrchestrator
from my_agent import CustomWebAgent

# Initialize simulations (Gmail, GCal, etc.)
sim_manager = SimulationManager()
sim_manager.spawn_instances(apps=["gmail", "google_calendar"])

# Configure orchestrator with July 2026 settings
orchestrator = ExperimentOrchestrator(
    agent=CustomWebAgent(model="claude-5-1-sonnet"),
    max_steps=75,
    resolution=(1280, 960),
    mcp_enabled=True,
    chrome_args=[
        "--enable-extension-hooks",
        "--side-panel-integration"
    ]
)

# Run benchmark suite
results = orchestrator.run_suite(tasks="calendar_sync_2026")
print(f"Success Rate: {results.success_rate}")
print(f"Mean Steps: {results.mean_steps_to_completion}")

# Cleanup
sim_manager.shutdown()
```

### Defining a Custom Web Task
```python
from pa_bench import TaskDefinition

task = TaskDefinition(
    id="multi_calendar_sync_01",
    goal="Sync my Fastmail and GCal events for next Tuesday.",
    apps=["gmail", "google_calendar"],
    eval_script="verify_sync.py"
)
```

## Related tools / concepts
- [Web Agents](../../knowledge_base/agent_protocols.md) - Core architectural patterns.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) - Orchestration strategies.
- [OpenHands](../development_ops/openhands.md) - Open-source agentic development platform.
- [SWE-bench](./swe-bench.md) - Software engineering benchmark.
- [Terminal-bench](./terminal-bench.md) - Shell interaction benchmark.
- [GAIA (General AI Assistants)](gaia.md) - Real-world assistant tasks.
- [AssistantBench](assistant-bench.md) - Web-search and navigation benchmark.
- [OSWorld](./os-world.md) - Operating system-wide agent evaluation.
- [Skills in Chrome](../ai_knowledge/skills-in-chrome.md) - Browser-native agentic hooks in July 2026.
- [MCP 3.0](../../knowledge_base/self-healing-agent-research.md) - The protocol for agentic tool use.

## Sources / references
- [PA-bench: Evaluating web agents on real world personal assistant workflows](https://vibrantlabs.com/blog/pa-bench)
- [Vibrant Labs GitHub Repository](https://github.com/vibrantlabsai/)
- [Agentic Session Orchestration July 2026 Whitepaper](https://example.com/aso-2026)

- Last reviewed: 2026-07-23
- Confidence: high
