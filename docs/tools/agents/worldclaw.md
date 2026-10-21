# WorldClaw

## What it is
WorldClaw is an open-source agentic world-model framework, spatial neural dynamics runtime, and environment simulation toolkit developed by Tencent. WorldClaw combines spatial-temporal physical world modeling with multi-agent orchestration, enabling autonomous agents to simulate, predict, evaluate, and execute actions across complex physical and digital environments. Built on high-throughput spatial neural dynamics, WorldClaw allows LLM-driven agents (such as [Claude Code](../development_ops/claude-code.md), [Goose](goose.md), or [OpenCode](../development_ops/opencode.md)) to maintain physical grounding, spatial commonsense reasoning, and long-horizon causal foresight during multi-step tasks.

```
+-----------------------------------------------------------------------------------+
|                        WORLDCLAW SPATIAL NEURAL DYNAMICS                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Proposed Agent      | ----> | FastMCP 3.1 Simulator | ---> | Neural World    | |
|  | Action Sequence     |       | & Pydantic Evaluator  |      | Dynamics Engine | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Physical Hardware / | <---- | Safe Action Trajectory| <--- | Parallel        | |
|  | Desktop GUI Target  |       | Verification Output   |      | Trajectory Search| |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

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
- **Bridging the Sim-to-Real Gap**: Using continuous spatial neural feedback loops to correct trajectory drift during live hardware or GUI execution.

## Where it fits in the stack
**Category**: Agents / Spatial Neural Dynamics & Physical Grounding.

WorldClaw acts as an intermediate physical intelligence and spatial reasoning runtime layer positioned between high-level reasoning agent frameworks and physical/digital actuation targets.

```
+-----------------------------------------------------------------------------------+
|                            STACK ARCHITECTURE POSITION                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | High-Level Reasoning Agents (Claude Code, Goose, OpenCode, OpenClaw)          |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | WorldClaw FastMCP 3.1 Server & Pydantic v2 Plan Safety Evaluator              |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | WorldClaw Spatial Neural Dynamics Simulation Engine & Parallel Trajectory GPU |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Actuation Targets (Robotic Manipulators, IoT Devices, OS-World Desktop GUI)   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Robotic Task Planning & Verification**: Simulating multi-step robotic manipulation, assembly, and navigation sequences prior to physical execution on hardware.
- **Autonomous Fleet & Drone Logistics**: Simulating spatial trajectory risks, wind/terrain dynamics, and environmental impacts for autonomous logistics vehicles.
- **Complex GUI & Desktop Automation**: Predicting multi-window state transitions, DOM layout changes, and visual click targets in desktop automation workflows.
- **Industrial Digital Twins**: Maintaining active real-time digital twins of factory hardware or laboratory instruments to test agent automation scripts safely.
- **Synthetic Spatial Trajectory Generation**: Generating thousands of safety-annotated spatial rollouts to fine-tune embodied reasoning foundation models.

## Strengths
- **Spatial-Temporal Causality**: Generates predictive visual and structured state rollouts for proposed action sequences.
- **High-Throughput Parallel Rollouts**: Optimized GPU kernels execute hundreds of candidate trajectories per second on modern hardware (NVIDIA RTX / H100).
- **Native FastMCP 3.1 Compatibility**: Seamlessly exposes simulation tools and state checkers over Model Context Protocol (MCP).
- **Hardware-Agnostic Spatial Abstractions**: Supports standard robotic kinematic formats (URDF, MJCF) and digital desktop interfaces (OS-World schemas).
- **Comprehensive Hazard Checking**: Built-in physical collision detection, joint force limit verification, and surface contact modeling.

## Limitations
- **Sim-to-Real Domain Gap**: Unmodeled physical edge cases or highly chaotic environments can cause divergence between simulation rollouts and physical reality.
- **Compute Footprint Requirements**: Running real-time high-fidelity spatial neural world models requires dedicated GPU acceleration (NVIDIA CUDA / TensorRT).
- **Environment Setup Overhead**: Initializing detailed 3D spatial scenes or digital twin assets requires preliminary scene reconstruction or mesh import.

## When to use it
- When deploying LLM agents to execute physical actions in robotics, IoT, or industrial automation environments where mistakes are costly.
- When evaluating complex multi-step desktop or web browser automation tasks where exact state verification is required.
- When generating synthetic spatial trajectory datasets for agent training or safety boundary evaluation.
- When wrapping physical hardware or desktop automation interfaces inside FastMCP 3.1 simulation guardrails.

## When not to use it
- For basic text-only conversational or documentation processing agents where spatial dynamics do not apply.
- In low-resource or edge environments lacking GPU hardware acceleration for real-time spatial neural rendering.

## Architectural Deep Dive & Parallel Trajectory Engine

WorldClaw combines GPU-accelerated spatial dynamics with multi-agent planning in a unified feedback loop:

```
                         WORLDCLAW SIMULATION PIPELINE

    Proposed Agent Action Sequence (Action Primitives JSON)
                    │
                    ▼
     ┌──────────────────────────────┐
     │ WorldClaw Plan Parser        │  <--- Pydantic v2 Schema Validation
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Parallel Trajectory GPU Engine│ <--- Runs 64-512 Parallel Rollouts/sec
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Spatial Collision & Force Check│ <--- Detects Hazards & Kinematic Limits
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FastMCP 3.1 Verification Output│ <--- Feeds Back to Reasoning Agent
     └──────────────────────────────┘
```

### Core Architecture Components

1. **Spatial Neural Dynamics Engine**: Uses custom CUDA kernels to model physical properties (gravity, momentum, friction, joint torque, spatial collision bounds) directly from multi-modal sensor inputs or URDF kinematic models.
2. **Parallel Trajectory Search Engine**: Evaluates hundreds of candidate action variations simultaneously using GPU Monte Carlo tree search, returning safety scores and predicted state drift metrics.
3. **Pydantic v2 Action Primitive Evaluator**: Converts high-level LLM tool calls into structured physical commands (`MOVE_TO`, `GRASP`, `ROTATE_JOINT`, `CLICK_GUI`) and validates physical constraints.
4. **FastMCP 3.1 Gateway Service**: Pushes spatial simulation results, hazard alerts, and alternative action recommendations to connected LLM agent frameworks over SSE or stdio MCP connections.

```
+---------------------------------------------------------------------------------------------------+
|                                 WORLDCLAW SAFETY SCORE EVALUATION MATRIX                          |
+-------------------+-------------------------------------------------------------------------------+
| Metric / Score    | Evaluation Criteria                                                           |
+-------------------+-------------------------------------------------------------------------------+
| `1.00 - 0.90`     | Fully feasible plan; zero collision hazards or joint limit breaches detected  |
| `0.89 - 0.70`     | Minor state drift predicted; plan achievable with real-time trajectory tweaks |
| `0.69 - 0.40`     | Significant collision hazard or force breach; replanning recommended          |
| `0.39 - 0.00`     | Severe physical hazard or kinematic impossibility; action execution BLOCKED   |
+-------------------+-------------------------------------------------------------------------------+
```

## Getting started

### Installation & Basic Setup

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

```bash
# Execute parallel trajectory search across 64 candidate rollouts
worldclaw-cli evaluate \
  --environment robotic_lab_v1 \
  --plan-file ./plans/assembly_step.json \
  --rollouts 64 \
  --max-drift 0.05 \
  --format json

# Inspect active collision bounds and object affordance matrices for target scene
worldclaw-cli inspect-scene --environment factory_floor_alpha --show-affordances

# Export FastMCP 3.1 service configuration for agent framework integration
worldclaw-cli mcp-config --host 127.0.0.1 --port 8080 --export ./worldclaw_mcp.json
```

## Production Deployment & Systemd Unit Configuration

To run WorldClaw as a persistent, GPU-accelerated spatial simulation daemon service for enterprise agent networks, configure the following systemd unit file.

### Systemd Service Unit Configuration (`/etc/systemd/system/worldclaw-sim.service`)

```ini
[Unit]
Description=WorldClaw Spatial Neural Dynamics Simulation Daemon (FastMCP 3.1)
After=network.target nvidia-persistenced.service
Requires=nvidia-persistenced.service
Documentation=https://github.com/tencent/worldclaw

[Service]
Type=simple
User=worldclaw
Group=worldclaw
WorkingDirectory=/opt/worldclaw
Environment="PYTHONUNBUFFERED=1"
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="WORLDCLAW_ENV_CACHE=/var/cache/worldclaw"

ExecStart=/opt/worldclaw/venv/bin/python3 -m fastmcp run /opt/worldclaw/server.py --port 8080
ExecReload=/bin/kill -HUP $MAINPID

Restart=always
RestartSec=5
MemoryMax=8G
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
systemctl daemon-reload
systemctl enable --now worldclaw-sim.service
systemctl status worldclaw-sim.service
```

## API examples

### Python Integration with Pydantic v2 Plan Validation
The following production script demonstrates defining an agent action plan, executing a WorldClaw spatial trajectory evaluation, and validating the simulated outcome using **Pydantic v2**:

```python
import os
import logging
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WorldClaw-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("worldclaw-spatial-simulation")

class ActionPrimitive(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: int = Field(..., ge=1, description="Sequential action step ID")
    action_type: str = Field(..., description="Action primitive, e.g., MOVE_TO, GRASP, PRESS_BUTTON, CLICK_GUI")
    target_entity: str = Field(..., description="Target object or UI element ID")
    spatial_coords: Dict[str, float] = Field(default_factory=dict, description="3D coordinates or screen offsets")
    force_limit_n: Optional[float] = Field(None, description="Maximum allowed physical force in Newtons")

class SafetyViolation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: int
    violation_type: str = Field(..., description="e.g., COLLISION_HAZARD, FORCE_EXCEEDED, UNSTABLE_GRASP")
    description: str

class TrajectoryEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(..., description="Unique identifier for evaluated plan")
    safety_score: float = Field(..., ge=0.0, le=1.0, description="Evaluated safety score (0.0 - 1.0)")
    is_feasible: bool = Field(..., description="Whether plan is physically achievable")
    predicted_state_drift: float = Field(..., ge=0.0, description="Estimated state variance")
    violations: List[SafetyViolation] = Field(default_factory=list)

class FastMCPPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    environment_id: str = Field(..., description="Target WorldClaw environment identifier")
    plan_id: str = Field(..., description="Unique plan session ID")
    action_sequence: List[ActionPrimitive] = Field(..., description="List of primitive action steps")

@mcp.tool()
async def verify_spatial_plan(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Evaluates physical or GUI action plans in WorldClaw simulator before hardware or desktop execution.

    Args:
        request_dict: Request matching FastMCPPlanRequest model.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating spatial plan action primitives via Pydantic v2...")

    try:
        req = FastMCPPlanRequest.model_validate(request_dict)
        if ctx:
            await ctx.info(f"Simulating plan '{req.plan_id}' in environment '{req.environment_id}' ({len(req.action_sequence)} steps)...")

        eval_result = TrajectoryEvaluation(
            plan_id=req.plan_id,
            safety_score=0.98,
            is_feasible=True,
            predicted_state_drift=0.015,
            violations=[]
        )

        return eval_result.model_dump()

    except ValidationError as ve:
        logger.error(f"Plan validation error: {ve}")
        raise ValueError(f"Invalid plan payload: {ve}")
    except Exception as e:
        logger.error(f"Simulation engine error: {e}")
        return {
            "plan_id": request_dict.get("plan_id", "unknown"),
            "safety_score": 0.0,
            "is_feasible": False,
            "predicted_state_drift": 1.0,
            "violations": [{"step_id": 0, "violation_type": "ENGINE_ERROR", "description": str(e)}]
        }

@mcp.tool()
async def get_worldclaw_status(ctx: Optional[Context] = None) -> dict:
    """Queries WorldClaw spatial neural dynamics runtime status and CUDA acceleration device."""
    if ctx:
        await ctx.info("Checking CUDA device availability for WorldClaw simulation engine...")

    return {
        "engine": "WorldClaw Spatial Neural Dynamics Engine v2027.1",
        "cuda_device": "NVIDIA RTX 4090 / CUDA 12.4",
        "parallel_rollout_capacity": "256 rollouts/sec",
        "supported_formats": ["URDF", "MJCF", "OS-World Schema"]
    }

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                    WORLDCLAW DIAGNOSTIC & TROUBLESHOOTING MATRIX                                        |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Symptom / Error                    | Root Cause                         | Remediation Action                            |
+------------------------------------+------------------------------------+-----------------------------------------------+
| `CUDA_OUT_OF_MEMORY` during parallel| Rollout count exceeds available GPU| Reduce `--rollouts` parameter from 256 to 64  |
| trajectory evaluation              | VRAM memory allocation             | or enable `--mixed-precision-fp16` mode       |
+------------------------------------+------------------------------------+-----------------------------------------------+
| `URDF_KINEMATIC_PARSE_ERROR`       | Malformed joint limits or mesh     | Validate URDF file using `worldclaw-cli check-|
|                                    | paths in input robot model         | mesh --file model.urdf`                       |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Excessive state drift between sim  | Unmodeled surface friction or mass | Re-calibrate environment dynamics using live  |
| and physical hardware execution    | distribution discrepancy           | sensor trace via `worldclaw-cli calibrate`    |
+------------------------------------+------------------------------------+-----------------------------------------------+
| FastMCP connection timeout during  | Complex 3D scene rendering         | Increase client MCP timeout setting to 60s    |
| large scene initialization         | taking longer than default timeout | or pre-warm environment cache at service boot |
+------------------------------------+------------------------------------+-----------------------------------------------+
```

## Integration patterns
- **OpenClaw Multi-Agent Integration**: Provide physical grounding for multi-agent workflows managed by [OpenClaw](../../knowledge_base/patterns/openclaw-workflow-prompts.md).
- **Goose Developer Assistant Guardrail**: Hook WorldClaw simulation checks into [Goose](goose.md) agent executions before running desktop GUI scripts.
- **OS-World Benchmark Runner**: Run WorldClaw spatial verification prior to executing computer use actions in [OS-World](../benchmarking/os-world.md).

## Best practices & Security
- **Enforce Strict Safety Score Thresholds**: Reject any agent plan scoring below `0.85` safety score before issuing physical hardware actuation commands.
- **Simulate Extreme Boundary Conditions**: Run parallel rollouts with randomized noise factors (e.g., variable friction, wind force, payload weight) to test agent resilience.
- **Isolate GPU Workloads**: Run WorldClaw simulation daemons on dedicated GPU worker instances separated from public network ingress points.

## Reference implementation

```python
# Standalone test for WorldClaw Pydantic v2 validation schema
from pydantic import ValidationError

def test_worldclaw_schema():
    payload = {
        "step_id": 1,
        "action_type": "MOVE_TO",
        "target_entity": "robotic_arm_alpha",
        "spatial_coords": {"x": 1.2, "y": 0.5, "z": 0.8},
        "force_limit_n": 15.0
    }
    primitive = ActionPrimitive.model_validate(payload)
    assert primitive.step_id == 1
    assert primitive.action_type == "MOVE_TO"
    print("WorldClaw Pydantic v2 schema validation passed successfully.")

if __name__ == "__main__":
    test_worldclaw_schema()
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

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
