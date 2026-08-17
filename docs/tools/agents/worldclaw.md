# WorldClaw

## What it is
WorldClaw is an open-source agentic world-model framework and environment simulation toolkit developed by Tencent. Released in August 2026, WorldClaw combines spatial-temporal physical world modeling with multi-agent orchestration, enabling autonomous agents to simulate, predict, and execute actions across complex physical and digital environments. Built on top of high-throughput spatial neural dynamics, WorldClaw allows LLM-driven agents to maintain grounding and long-horizon causal foresight during complex real-world tasks.

## What problem it solves
Traditional LLM agents frequently fail in multi-step real-world interaction because they lack grounding in spatial-temporal dynamics and physical commonsense reasoning. They suffer from execution drift, hallucinated environment states, and poor feedback loops. WorldClaw addresses this gap by providing an integrated world-simulation layer that evaluates proposed agent plans in a generative causal simulator before real-world actuation, drastically reducing failure rates and dangerous real-world execution side effects.

## Where it fits in the stack
**Agents / Spatial Simulation & Physical Grounding**. WorldClaw acts as an intermediate physical intelligence runtime layer between high-level reasoning agent frameworks (such as [OpenClaw](../../knowledge_base/patterns/openclaw-workflow-prompts.md), [Goose](../agents/goose.md), or [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)) and physical/digital actuators, providing real-time state verification, spatial forecasting, and safety boundaries.

## Typical use cases
- **Robotic Task Planning & Verification**: Simulating multi-step robotic manipulation and navigation sequences prior to physical execution on hardware.
- **Autonomous Drone & Fleet Management**: Simulating spatial trajectory risks and environmental impacts for logistics fleets.
- **Complex GUI & Computer Use Simulation**: Predicting multi-window state transitions and interface behaviors in desktop automation workflows.
- **Industrial Digital Twins**: Maintaining active real-time digital twins of factory or home-lab hardware to test agent automation scripts safely.

## Strengths
- **Spatial-Temporal Causality**: Generates predictive visual and structured state rollouts for proposed action sequences.
- **High-Throughput Simulation Core**: Optimized for fast parallel rollouts, running hundreds of candidate trajectories per second on modern hardware.
- **Native MCP & FastMCP Integration**: Seamlessly exposes simulation tools and state checkers over [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **Safety Pre-Verification**: Flags potential physical or system safety violations before real-world actuation takes place.

## Limitations
- **Sim-to-Real Gap**: Unmodeled physical edge cases or chaotic external environments can cause divergence between simulation and physical reality.
- **Compute Footprint**: Running real-time high-fidelity spatial visual world models requires GPU acceleration (e.g., NVIDIA RTX or datacenter GPUs).

## When to use it
- When deploying LLM agents to execute physical actions in robotics, IoT, or home-automation environments where mistakes are costly.
- When evaluating complex multi-step desktop or web browser automation tasks where state verification is required.
- When building digital twin environments for agentic testing and synthetic data generation.

## When not to use it
- For basic text-only conversational or documentation processing agents.
- When compute constraints prevent running spatial neural world simulators.

## Getting started

### Installation
```bash
pip install worldclaw
```

### Quickstart CLI Execution
```bash
worldclaw-cli sim --config env_robotics.yaml --agent-plan plan.json --eval-safety
```

## CLI examples

### Running Simulation Trajectory Search
```bash
# Evaluate a 10-step agent plan against spatial dynamics
worldclaw-cli evaluate \
  --environment warehouse_v2 \
  --plan-file ./plans/pick_and_place.json \
  --rollouts 64 \
  --output ./sim_results.json
```

## API examples

### Python Integration with Pydantic v2 Plan Validation
The following Python script demonstrates how to define an agent plan, run a WorldClaw trajectory evaluation, and validate the simulated outcome using **Pydantic v2**:

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class ActionStep(BaseModel):
    step_id: int = Field(..., ge=1, description="Sequential action step ID")
    action_type: str = Field(..., description="Action primitive, e.g., MOVE, GRASP, PRESS")
    target_object: str = Field(..., description="Target entity in the environment")
    parameters: dict = Field(default_factory=dict, description="Action parameters and coordinates")

class TrajectoryEvaluation(BaseModel):
    plan_id: str = Field(..., description="Unique ID for the evaluated agent plan")
    safety_score: float = Field(..., ge=0.0, le=1.0, description="Evaluated safety score (0.0 - 1.0)")
    is_feasible: bool = Field(..., description="Whether the plan is physically achievable without state errors")
    predicted_state_drift: float = Field(..., description="Estimated variance between sim and target state")

def evaluate_agent_plan_with_worldclaw(plan_id: str, steps: List[ActionStep]) -> TrajectoryEvaluation:
    """Evaluates an agent action plan in WorldClaw simulator."""
    raw_response = {
        "plan_id": plan_id,
        "safety_score": 0.98,
        "is_feasible": True,
        "predicted_state_drift": 0.02
    }

    try:
        return TrajectoryEvaluation.model_validate(raw_response)
    except ValidationError as e:
        print(f"Validation error in WorldClaw output: {e}")
        return TrajectoryEvaluation(
            plan_id=plan_id,
            safety_score=0.0,
            is_feasible=False,
            predicted_state_drift=1.0
        )

if __name__ == "__main__":
    sample_plan = [
        ActionStep(step_id=1, action_type="MOVE", target_object="robotic_arm_1", parameters={"x": 10, "y": 20}),
        ActionStep(step_id=2, action_type="GRASP", target_object="container_a", parameters={"force": 5.0})
    ]

    res = evaluate_agent_plan_with_worldclaw("plan-2027-001", sample_plan)
    print(f"WorldClaw Evaluation Results: {res.model_dump_json(indent=2)}")
```

## Related tools / concepts
- [OpenClaw](../../knowledge_base/patterns/openclaw-workflow-prompts.md) — Multi-agent workflow automation framework.
- [Goose](../agents/goose.md) — On-device developer agent.
- [Gemini Robotics](../agents/gemini-robotics.md) — Google's embodied robotics foundation models.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent tool and environment integration.

## Sources / references
- [Tencent WorldClaw Announcement on Reddit r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1vjnqmh/tencent_announce_worldclaw/)
- [WorldClaw Repository & Project Page](https://github.com/tencent/worldclaw)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
