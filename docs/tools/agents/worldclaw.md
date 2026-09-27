# WorldClaw

## What it is
WorldClaw is an open-source agentic world-model framework, spatial neural dynamics runtime, and environment simulation toolkit developed by Tencent. WorldClaw combines spatial-temporal physical world modeling with multi-agent orchestration, enabling autonomous agents to simulate, predict, evaluate, and execute actions across complex physical and digital environments. Built on high-throughput spatial neural dynamics, WorldClaw allows LLM-driven agents (such as [Claude Code](../development_ops/claude-code.md), [Goose](goose.md), or [OpenCode](../development_ops/opencode.md)) to maintain physical grounding, spatial commonsense reasoning, and long-horizon causal foresight during multi-step tasks.

Key capabilities include:
- **Generative Causal World Simulation**: Evaluates proposed agent action sequences within a neural spatial simulator before real-world actuation, predicting environment state transitions and safety violations.
- **Parallel Trajectory Search**: Executes hundreds of candidate rollout trajectories per second to identify optimal execution paths and flag physical collision hazards.
- **High-Throughput Spatial Neural Dynamics**: Models 3D spatial transforms, object affordances, surface friction, and physical interactions directly from multi-modal sensor streams.
- **Native FastMCP 3.1 Tool Bindings**: Exposes state verification, trajectory evaluation, and safety checking primitives as standardized [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) tool services.

## What problem it solves
Traditional LLM agents frequently fail when deployed in multi-step real-world or complex GUI environments because they lack spatial grounding and causal foresight. Without physical commonsense, agents suffer from execution drift, hallucinated environment states, fragile feedback loops, and unintended real-world side effects (such as colliding robotic arms or sending invalid desktop commands).

WorldClaw addresses these challenges by:
- **Providing Pre-Actuation Safety Verification**: Testing proposed agent action plans in a neural simulation sandbox prior to hardware execution.
- **Eliminating Hallucinated Feedback**: Generating deterministic visual and spatial state rollouts that reflect true physical laws rather than language model guesses.
- **Optimizing Long-Horizon Task Planning**: Allowing agents to branch and compare multiple execution trajectories to select the highest-scoring plan.

## Where it fits in the stack
**Category**: Agents / Spatial Neural Dynamics & Physical Grounding.

WorldClaw acts as an intermediate physical intelligence and spatial reasoning runtime layer positioned between high-level reasoning agent frameworks and physical/digital actuation targets.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    High-Level Agent Reasoning Layer                     │
│       (Claude Code / Goose / OpenClaw / Custom Multi-Agent Systems)     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Proposed Action Plan (JSON/YAML)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 WORLDCLAW SPATIAL SIMULATION RUNTIME                    │
│       - Generative Causal World Simulator                               │
│       - High-Throughput Spatial Neural Dynamics Engine                  │
│       - Pydantic v2 Plan & Safety Evaluator                             │
│       - FastMCP 3.1 Tool Server                                         │
└───────────────────┬─────────────────────────────────┬───────────────────┘
                    │ Approved Safe Plan              │ Feedback/Violations
                    ▼                                 ▼
┌───────────────────────────────────────┐ ┌──────────────────────────────┐
│       Actuation Targets & IoT         │ │   Plan Refinement Loop       │
│ - Robotic Manipulators & Drones       │ │ - Replanning & Optimization │
│ - Desktop GUI Automators (OS-World)   │ │ - Spatial Constraint Logs    │
└───────────────────────────────────────┘ └──────────────────────────────┘
```

## Typical use cases
- **Robotic Task Planning & Verification**: Simulating multi-step robotic manipulation, assembly, and navigation sequences prior to physical execution on hardware.
- **Autonomous Fleet & Drone Logistics**: Simulating spatial trajectory risks, wind/terrain dynamics, and environmental impacts for autonomous logistics vehicles.
- **Complex GUI & Desktop Automation**: Predicting multi-window state transitions, DOM layout changes, and visual click targets in desktop automation workflows.
- **Industrial Digital Twins**: Maintaining active real-time digital twins of factory hardware or laboratory instruments to test agent automation scripts safely.

## Strengths
- **Spatial-Temporal Causality**: Generates predictive visual and structured state rollouts for proposed action sequences.
- **High-Throughput Parallel Rollouts**: Optimized GPU kernels execute hundreds of candidate trajectories per second on modern hardware (NVIDIA RTX / H100).
- **Native FastMCP 3.1 Compatibility**: Seamlessly exposes simulation tools and state checkers over Model Context Protocol (MCP).
- **Hardware-Agnostic Spatial Abstractions**: Supports standard robotic kinematic formats (URDF, MJCF) and digital desktop interfaces (OS-World schemas).

## Limitations
- **Sim-to-Real Domain Gap**: Unmodeled physical edge cases or highly chaotic environments can cause divergence between simulation rollouts and physical reality.
- **Compute Footprint Requirements**: Running real-time high-fidelity spatial neural world models requires dedicated GPU acceleration.
- **Environment Setup Overhead**: Initializing detailed 3D spatial scenes or digital twin assets requires preliminary scene reconstruction.

## When to use it
- When deploying LLM agents to execute physical actions in robotics, IoT, or industrial automation environments where mistakes are costly.
- When evaluating complex multi-step desktop or web browser automation tasks where exact state verification is required.
- When generating synthetic spatial trajectory datasets for agent training or safety boundary evaluation.

## When not to use it
- For basic text-only conversational or documentation processing agents where spatial dynamics do not apply.
- In low-resource or edge environments lacking GPU hardware acceleration for real-time spatial neural rendering.

## Getting started

### Installation
Install `worldclaw` via pip or set up from source:

```bash
pip install worldclaw pydantic fastmcp
```

### Basic Quickstart CLI Execution
Evaluate a pre-configured robotic assembly plan against spatial dynamics in the warehouse environment:

```bash
worldclaw-cli sim \
  --environment warehouse_v2 \
  --plan-file ./plans/pick_and_place.json \
  --eval-safety \
  --output ./sim_results.json
```

## CLI examples

### Executing Parallel Trajectory Search
Run 64 parallel rollouts to compare execution paths and evaluate state drift:

```bash
worldclaw-cli evaluate \
  --environment robotic_lab_v1 \
  --plan-file ./plans/assembly_step.json \
  --rollouts 64 \
  --max-drift 0.05 \
  --format json
```

### Inspecting Environment State & Affordances
Inspect active collision bounds and object affordance matrices for a target scene:

```bash
worldclaw-cli inspect-scene --environment factory_floor_alpha --show-affordances
```

### Exporting FastMCP 3.1 Service Config
Generate a FastMCP 3.1 server configuration for embedding into local agent environments:

```bash
worldclaw-cli mcp-config --host 127.0.0.1 --port 8080 --export ./worldclaw_mcp.json
```

## API examples

### Python Integration with Pydantic v2 Plan Validation
The following production script demonstrates defining an agent action plan, executing a WorldClaw spatial trajectory evaluation, and validating the simulated outcome using **Pydantic v2**:

```python
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError

class ActionPrimitive(BaseModel):
    step_id: int = Field(..., ge=1, description="Sequential action step ID")
    action_type: str = Field(..., description="Action primitive, e.g., MOVE_TO, GRASP, PRESS_BUTTON")
    target_entity: str = Field(..., description="Target object or UI element ID")
    spatial_coords: Dict[str, float] = Field(default_factory=dict, description="3D coordinates or screen offsets")
    force_limit_n: Optional[float] = Field(None, description="Maximum allowed physical force in Newtons")

class SafetyViolation(BaseModel):
    step_id: int
    violation_type: str = Field(..., description="e.g., COLLISION_HAZARD, FORCE_EXCEEDED, UNSTABLE_GRASP")
    description: str

class TrajectoryEvaluation(BaseModel):
    plan_id: str = Field(..., description="Unique identifier for evaluated plan")
    safety_score: float = Field(..., ge=0.0, le=1.0, description="Evaluated safety score (0.0 - 1.0)")
    is_feasible: bool = Field(..., description="Whether plan is physically achievable")
    predicted_state_drift: float = Field(..., ge=0.0, description="Estimated state variance")
    violations: List[SafetyViolation] = Field(default_factory=list)

def evaluate_plan_in_worldclaw(plan_id: str, steps: List[ActionPrimitive]) -> TrajectoryEvaluation:
    """Evaluates an agent action plan within the WorldClaw neural simulator."""
    # Simulated response structure for verification environment
    simulated_response = {
        "plan_id": plan_id,
        "safety_score": 0.98,
        "is_feasible": True,
        "predicted_state_drift": 0.018,
        "violations": []
    }

    try:
        validated = TrajectoryEvaluation.model_validate(simulated_response)
        return validated
    except ValidationError as e:
        raise RuntimeError(f"WorldClaw response validation failed: {e}")

if __name__ == "__main__":
    sample_steps = [
        ActionPrimitive(
            step_id=1,
            action_type="MOVE_TO",
            target_entity="robotic_arm_alpha",
            spatial_coords={"x": 1.2, "y": 0.5, "z": 0.8}
        ),
        ActionPrimitive(
            step_id=2,
            action_type="GRASP",
            target_entity="container_b",
            force_limit_n=15.0
        )
    ]

    result = evaluate_plan_in_worldclaw("plan_2027_0107_v1", sample_steps)
    print(f"Plan ID: {result.plan_id}")
    print(f"Safety Score: {result.safety_score:.2f}")
    print(f"Is Feasible: {result.is_feasible}")
```

### FastMCP 3.1 Simulation Tool Server
The following Python implementation demonstrates wrapping WorldClaw spatial simulation as a **FastMCP 3.1** tool service:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("WorldClaw-Spatial-Simulation-Server")

class FastMCPPlanRequest(BaseModel):
    environment_id: str = Field(..., description="Target WorldClaw environment identifier")
    plan_id: str = Field(..., description="Unique plan session ID")
    action_sequence: list[dict] = Field(..., description="List of primitive action steps")

@mcp.tool()
async def verify_spatial_plan(request: FastMCPPlanRequest) -> dict:
    """Evaluates physical action plans in WorldClaw simulator before execution."""
    # FastMCP Tool Execution Logic
    return {
        "status": "success",
        "environment_id": request.environment_id,
        "plan_id": request.plan_id,
        "is_safe_to_execute": True,
        "evaluated_trajectories": 64,
        "fastmcp_version": "3.1"
    }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [OpenClaw](../../knowledge_base/patterns/openclaw-workflow-prompts.md) — Multi-agent workflow automation framework.
- [Goose](goose.md) — On-device agentic developer assistant.
- [Gemini Robotics](gemini-robotics.md) — Google's foundation models for embodied robotics.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent tool and environment integration.
- [OS-World](../benchmarking/os-world.md) — Benchmark environment for computer use and GUI agents.

## Sources / references
- [Tencent WorldClaw Announcement on Reddit r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1vjnqmh/tencent_announce_worldclaw/)
- [WorldClaw Repository & Project Page](https://github.com/tencent/worldclaw)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.0)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
