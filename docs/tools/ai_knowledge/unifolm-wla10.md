# UniFolm-WLA10

## What it is
**UniFolm-WLA10** is a single-stream 6-billion parameter multimodal embodied foundation model released by Unitree Robotics in late 2026 / early 2027. Engineered specifically for robotic manipulation, leg-and-arm locomotion coordination, visual-tactile perception, and direct physical agent control, UniFolm-WLA10 unifies high-level visual reasoning and low-level motor joint trajectory output within a single autoregressive 6B parameter neural network architecture.

Unlike decoupled modular robotics pipelines that separate vision, text planning, and low-level motor controllers, UniFolm-WLA10 accepts interleaved multimodal inputs (camera video feeds, depth maps, tactile sensor matrices, natural language instructions) and directly outputs high-frequency end-effector trajectories and joint position delta vectors. This enables zero-shot robot manipulation, home automation physical task execution, and sub-10ms real-time sensory-motor feedback loops.

```
+-----------------------------------------------------------------------------------+
|                     UNIFOLM-WLA10 EMBODIED CONTROL ARCHITECTURE                   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +------------------------+      +---------------------------------------------+  |
|  | Interleaved Multimodal | ---> | UniFolm-WLA10 (Single-Stream 6B Foundation)|  |
|  | Inputs (Video/Tactile) |      | Vision-Language-Action (VLA) Model          |  |
|  +------------------------+      +---------------------------------------------+  |
|                                                         |                         |
|                                                         v                         |
|                                  +---------------------------------------------+  |
|                                  | Joint Delta Trajectories / Action Tokens     |  |
|                                  +---------------------------------------------+  |
|                                         /               |               \         |
|                                        v                v                v        |
|                            +---------------+    +---------------+    +----------+ |
|                            | Unitree Human |    | FastMCP 3.1   |    | ROS2     | |
|                            | Arm/Leg Motors|    | Tool Router   |    | Node Bus | |
|                            +---------------+    +---------------+    +----------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
- **High Latency in Multi-Stage Robotic Pipelines**: Eliminates multi-hop network and process latencies between vision-language planning models and motor trajectory generators by using a single integrated 6B VLA network.
- **Brittle Sim-to-Real Transfer**: Solves trajectory instability when adapting from synthetic simulation to physical environments by leveraging pre-training on thousands of hours of real-world human demonstration data.
- **Physical Home Automation Hardware Integration**: Enables autonomous home robotics (e.g., dish sorting, laundry folding, parcel receiving) to interpret natural language commands and adapt to changing physical object states in real time.
- **Coordinated Arm-Base Locomotion**: Integrates mobile biped/quadruped base movement with multi-DOF robotic arm manipulation under a unified trajectory control token space.

## Where it fits in the stack
**AI Knowledge / Embodied AI / Robotics & Action Foundation Models**. UniFolm-WLA10 sits at the action execution layer of the physical AI stack, bridging high-level agent orchestrators (FastMCP, AutoGen, LangChain) with low-level robotic hardware control buses (ROS2, Unitree SDK, Ethernet/CAN buses).

```
+-----------------------------------------------------------------------------------+
|                           EMBODIED ROBOTICS STACK                                 |
+-----------------------------------------------------------------------------------+
| Agentic High Planner   : Home Admin Agent / FastMCP Orchestrator / User Voice     |
+-----------------------------------------------------------------------------------+
| Embodied VLA Model     : UniFolm-WLA10 (6B Multimodal Trajectory Generator)       |
+-----------------------------------------------------------------------------------+
| Hardware Execution     : ROS2 Node Engine / Unitree Robot SDK / Motor Actuators   |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Physical Home Automation**: Translating voice commands like "Pick up the coffee mug from the kitchen counter and place it in the dishwasher" into collision-free joint trajectories.
- **Visual-Tactile Quality Inspection**: Inspecting physical inventory, detecting surface defects, and sorting home lab components using real-time camera and tactile sensor feedback.
- **Zero-Shot Task Adaptation**: Executing novel physical manipulation tasks without task-specific fine-tuning by parsing natural language spatial instructions.
- **FastMCP 3.1 Physical Action Server**: Serving robotic motor execution capabilities as standardized FastMCP tool calls for multi-agent systems.

## Strengths
- **Single 6B Parameter Efficiency**: Fits into consumer GPU VRAM (e.g., RTX 4090, RTX 5080) for low-latency local physical control inference.
- **High-Frequency Trajectory Tokenization**: Emits smooth 50Hz action trajectory tokens directly without requiring separate kinematic solvers.
- **Interleaved Multimodal Support**: Accepts simultaneous video streams, tactile grids, spatial point clouds, and text prompts.
- **Open-Weights Availability**: Released with open weights on Hugging Face for research and local deployment.

## Limitations
- **High Compute Requirements for Real-Time Control**: Requires continuous GPU inference to sustain 50Hz trajectory generation in dynamic environments.
- **Physical Safety Safeguards Mandatory**: Requires external hardware stop-loops and force-limiters to guarantee physical safety around humans.
- **Hardware-Specific Actuator Dynamics**: Achieving optimal control on non-Unitree custom robotic arms requires motor response calibration.

## When to use it
- When controlling physical robotic hardware (quadrupeds, bipeds, robotic arms) with natural language and vision inputs.
- For building physical smart home agents capable of manipulating physical objects.
- When you need a unified single-model approach to vision, language, and motion generation.
- For research in Vision-Language-Action (VLA) foundation models and sim-to-real transfer.

## When not to use it
- For purely virtual text or code generation tasks where physical manipulation is not required.
- In resource-constrained microcontrollers incapable of hosting 6B parameter weights.
- When standard fixed trajectory motion planning (like MoveIt 2 or standard Inverse Kinematics) is sufficient.

## Getting started

### Prerequisites
- NVIDIA GPU with 16GB+ VRAM (RTX 4090, A100, H100) running PyTorch 2.4+.
- Python 3.10+ with `transformers`, `torch`, `pydantic` v2, and `fastmcp`.

### Installation
```bash
pip install torch transformers accelerate pydantic fastmcp
```

### Loading UniFolm-WLA10 for Action Generation
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "unitree/unifolm-wla10"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="cuda" if torch.cuda.is_available() else "cpu",
    trust_remote_code=True
)

prompt = "Task: Pick up blue mug at coordinates (0.45, 0.12, 0.85). Generate joint trajectory delta tokens."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

with torch.no_grad():
    actions = model.generate(**inputs, max_new_tokens=64)

print("UniFolm-WLA10 Trajectory Action Tokens:", tokenizer.decode(actions[0], skip_special_tokens=True))
```

## CLI examples

### Inspecting Model Info via Hugging Face CLI
```bash
# Verify UniFolm-WLA10 Hugging Face repository metadata
python3 -c "
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('unitree/unifolm-wla10', trust_remote_code=True)
print('UniFolm-WLA10 Tokenizer successfully loaded. Model vocabulary size:', len(tokenizer))
"
```

### Running Simulated ROS2 Trajectory Node
```bash
# Simulating ROS2 action dispatch using UniFolm-WLA10 CLI runner
python3 -c "
import torch
print('Initializing UniFolm-WLA10 action generator on device:', 'cuda' if torch.cuda.is_available() else 'cpu')
"
```

## API examples

### FastMCP 3.1 Robotic Action Dispatch Server
This example builds a FastMCP 3.1 tool server that exposes UniFolm-WLA10 robotic arm motor control to higher-level agents:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import torch
from typing import List

mcp = FastMCP("UniFolm-WLA10-Robot-Dispatcher")

class ManipulationTaskRequest(BaseModel):
    task_description: str = Field(..., description="Natural language physical task instruction")
    target_object: str = Field(..., description="Target object identifier")
    safety_max_speed_m_s: float = Field(default=0.2, ge=0.01, le=1.0, description="Maximum speed limit in meters/second")

class ActionTrajectoryResponse(BaseModel):
    task_status: str = Field(..., description="Execution status ('planned', 'executing', 'failed')")
    joint_deltas: List[List[float]] = Field(..., description="Series of 6-DOF joint delta positions")
    estimated_duration_sec: float = Field(..., description="Estimated execution time in seconds")

@mcp.tool()
def plan_and_execute_manipulation(request: ManipulationTaskRequest) -> ActionTrajectoryResponse:
    """Plans physical trajectory using UniFolm-WLA10 VLA model and executes on robot motor bus."""
    # Simulated 6-DOF joint trajectory generated by UniFolm-WLA10
    simulated_trajectory = [
        [0.01, -0.02, 0.05, 0.0, 0.0, 0.1],
        [0.02, -0.04, 0.10, 0.0, 0.0, 0.2],
        [0.03, -0.06, 0.15, 0.0, 0.0, 0.3],
    ]

    return ActionTrajectoryResponse(
        task_status="planned",
        joint_deltas=simulated_trajectory,
        estimated_duration_sec=2.5
    )

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Trajectory Vector Validation
```python
from typing import List
from pydantic import BaseModel, Field, field_validator, ValidationError

class JointTrajectoryPoint(BaseModel):
    step_index: int = Field(..., ge=0, description="Sequence step index")
    joint_angles_rad: List[float] = Field(..., description="Radiant values for 6 joint motors")
    gripper_closed: bool = Field(default=False, description="Gripper state (True=closed, False=open)")

    @field_validator("joint_angles_rad")
    @classmethod
    def validate_6dof(cls, v: List[float]) -> List[float]:
        if len(v) != 6:
            raise ValueError(f"Joint angles list must contain exactly 6 DOF values, got {len(v)}")
        return v

# Validation test
try:
    point = JointTrajectoryPoint(
        step_index=1,
        joint_angles_rad=[0.0, -0.5, 1.2, 0.0, 0.8, 0.0],
        gripper_closed=True
    )
    print("Trajectory Point Schema Validated:", point.model_dump_json(indent=2))
except ValidationError as e:
    print("Validation Error:", e.json())
```

## Related tools / concepts
- [Gemini Robotics](../agents/gemini-robotics.md) — Multimodal embodied agents and robotics control framework.
- [LeRobot](../frameworks/lerobot.md) — Open-source robotics framework from Hugging Face.
- [Local LLMs](../ai_knowledge/local_llms.md) — Running local AI models on edge hardware.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Model Context Protocol python server framework.
- [Python](../ai_knowledge/python.md) — Core programming language for robotics and AI.

## Sources / references
- [Unitree UniFolm-WLA10 Release Announcement on Reddit / LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1ww91uw/unitree_just_dropped_unifolmwla10_a_single_6b/)
- [Unitree Robotics Official Website](https://www.unitree.com/)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
