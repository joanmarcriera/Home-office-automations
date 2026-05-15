# PA-bench

## What it is
PA-bench is a comprehensive benchmark suite designed to evaluate the performance of Personal Assistant (PA) web agents on real-world workflows.

## What problem it solves
It addresses the lack of realistic evaluation frameworks for web-based agents by providing a set of complex, multi-step tasks that mirror actual user needs, such as booking travel, managing calendars, or conducting research across multiple websites.

## Where it fits in the stack
**Eval**. It provides the metrics and environment necessary to measure the effectiveness and reliability of autonomous web agents.

## Typical use cases
- **Agent Comparison**: Evaluating different agent architectures on their ability to complete complex web tasks.
- **Regression Testing**: Ensuring that updates to an agent's reasoning or navigation logic don't break existing capabilities.
- **Research**: Providing a standardized baseline for academic and industrial research into autonomous web navigation.

## Strengths
- **Real-world Focus**: Tasks are based on actual personal assistant workflows rather than synthetic laboratory examples.
- **End-to-End Evaluation**: Measures the agent's ability to see a task through from start to finish.
- **Complexity**: Includes tasks that require multi-site navigation and state management.

## Limitations
- **Environment Stability**: Web-based benchmarks are subject to "flakiness" if the underlying websites change their structure.
- **Resource Intensive**: Running full-scale web agent evaluations can be time and credit consuming.

## When to use it
- When developing or refining autonomous agents intended for web-based personal assistant tasks.
- When you need a high-signal metric for how well an agent handles real-world web complexity.

## When not to use it
- For evaluating models on pure reasoning or coding tasks without a web navigation component.
- If you lack the infrastructure to run autonomous browser-based agents.

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free (benchmark), but requires LLM/Browser resources to execute.
- **Self-hostable**: Yes

## Getting started

PA-bench is typically executed via its Python SDK, which manages simulated environments for email and calendar applications.

### 1. Installation
```bash
pip install pa-bench
```

### 2. Running an Evaluation
```python
from pa_bench import SimulationManager, ExperimentOrchestrator
from my_agent import CustomWebAgent

# Initialize simulations
sim_manager = SimulationManager()
sim_manager.spawn_instances(apps=["gmail", "google_calendar"])

# Configure orchestrator
orchestrator = ExperimentOrchestrator(
    agent=CustomWebAgent(),
    max_steps=75,
    resolution=(1280, 960)
)

# Run benchmark
results = orchestrator.run_suite(tasks="travel_planning")
print(f"Success Rate: {results.success_rate}")

# Cleanup
sim_manager.shutdown()
```

## Related tools / concepts
- [Web Agents](../../knowledge_base/agent_protocols.md)
- [SWE-bench](./swe-bench.md)
- [Terminal-bench](./terminal-bench.md)
- [WebArena](https://webarena.dev/)
- [Mind2Web](https://github.com/osu-nlp-group/Mind2Web)
- [GAIA (General AI Assistants)](./gaia.md)
- [AssistantBench](./assistant-bench.md)
- [OSWorld](./os-world.md)

## Sources / References
- [PA-bench: Evaluating web agents on real world personal assistant workflows](https://vibrantlabs.com/blog/pa-bench)
- [Vibrant Labs GitHub](https://github.com/vibrantlabsai/)

## Contribution Metadata

- Last reviewed: 2026-05-15
- Confidence: high
