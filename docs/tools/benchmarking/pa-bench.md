# PA-bench

## What it is
PA-bench is a comprehensive benchmark suite designed to evaluate the performance of Personal Assistant (PA) web agents on real-world workflows. It uses a simulation-based approach to measure how effectively agents can navigate the web to complete complex, multi-application tasks.

## What problem it solves
It addresses the lack of realistic evaluation frameworks for web-based agents by providing a set of complex, multi-step tasks that mirror actual user needs, such as booking travel, managing calendars, or conducting research across multiple websites. It moves beyond static question-answering to evaluate long-horizon agency.

## Where it fits in the stack
**Benchmarking / Eval**. It provides the metrics and environment necessary to measure the effectiveness and reliability of autonomous web agents before deployment in production "KnowledgeOps" pipelines.

## Typical use cases
- **Agent Comparison**: Evaluating different agent architectures on their ability to complete complex web tasks.
- **Regression Testing**: Ensuring that updates to an agent's reasoning or navigation logic don't break existing capabilities.
- **Research**: Providing a standardized baseline for academic and industrial research into autonomous web navigation and tool-use.

## Strengths
- **Real-world Focus**: Tasks are based on actual personal assistant workflows rather than synthetic laboratory examples.
- **End-to-End Evaluation**: Measures the agent's ability to see a task through from start to finish.
- **Complexity**: Includes tasks that require multi-site navigation and state management.
- **Simulation Environment**: Provides a `SimulationManager` to handle environment resets and state tracking.

## Limitations
- **Environment Stability**: Web-based benchmarks are subject to "flakiness" if the underlying websites change their structure.
- **Resource Intensive**: Running full-scale web agent evaluations can be time and credit consuming.
- **Setup Complexity**: Requires a headless browser environment and often specific API keys for the websites being simulated.

## When to use it
- When developing or refining autonomous agents intended for web-based personal assistant tasks.
- When you need a high-signal metric for how well an agent handles real-world web complexity.

## When not to use it
- For evaluating models on pure reasoning or coding tasks without a web navigation component (use [HumanEval](human-eval.md)).
- If you lack the infrastructure to run autonomous browser-based agents or require sub-second evaluation feedback.

## Getting Started: Python Example

PA-bench utilizes a `SimulationManager` to orchestrate evaluations.

```python
from pa_bench import SimulationManager, WebAgent

# Initialize the simulation environment
manager = SimulationManager(config="configs/travel_booking.yaml")

# Define your agent's decision loop
class MyAgent(WebAgent):
    def act(self, observation):
        # Your LLM logic here to return an action (click, type, etc.)
        return {"action": "click", "selector": "#book-now"}

agent = MyAgent()

# Run the evaluation
results = manager.run(agent)

print(f"Success Rate: {results.success_rate}")
print(f"Average Steps: {results.avg_steps}")
```

## Technical Details

| Metric | Description |
| :--- | :--- |
| **SR (Success Rate)** | Percentage of tasks completed according to the ground truth. |
| **Sub-goal SR** | Success rate for intermediate steps within a long-horizon task. |
| **Efficiency Score** | A weighted measure of successful completion vs. number of actions taken. |
| **Trajectory Length** | Total steps taken by the agent to reach a terminal state. |

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free (benchmark), but requires LLM/Browser resources to execute.
- **Self-hostable**: Yes

## Related tools / concepts
- [Web Agents](../../knowledge_base/agent_protocols.md)
- [SWE-bench](swe-bench.md)
- [Terminal-Bench](terminal-bench.md)
- [InterCode](intercode.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [OpenClaw (Autonomous Assistant)](../development_ops/openclaw.md)
- [Multi-Agent KnowledgeOps](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / References
- [PA-bench: Evaluating web agents on real world personal assistant workflows](https://vibrantlabs.com/blog/pa-bench)
- [GitHub Repository - PA-bench](https://github.com/vibrant-labs/pa-bench)

## Contribution Metadata

- Last reviewed: 2026-05-15
- Confidence: high
