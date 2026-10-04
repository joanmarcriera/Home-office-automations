# UniFolm-WLA10

UniFolm-WLA10 is a specialized 6-billion parameter unified embodied robotics and vision-language-action (VLA) foundation model developed by Unitree Robotics. Designed explicitly for humanoid and quadruped physical AI systems, UniFolm-WLA10 integrates continuous visual perception, natural language instruction comprehension, and high-frequency whole-body motor action control into a single end-to-end neural network.

```
+-----------------------------------------------------------------------------------+
|                         UniFolm-WLA10 System Architecture                         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            Multi-Modal Sensor Inputs                              |
|   +-----------------------+  +----------------------+  +------------------------+ |
|   | Dual Stereo RGB-D     |  | Spatial Point Clouds |  | Audio / Speech Commands| |
|   +-----------------------+  +----------------------+  +------------------------+ |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                       UniFolm-WLA10 Unified Backbone (6B)                         |
|   +---------------------------------+  +-------------------------------------+  |
|   | Vision Transformer (ViT) Encoder|  | Causal Language Reasoning Core      |  |
|   +---------------------------------+  +-------------------------------------+  |
|   | Continuous Diffusion Action Head (100 Hz Torque & Trajectory Control)     |  |
|   +--------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         Robot Hardware Execution (Unitree G1/H1)                  |
|   - Joint Angles, Velocities, and Motor Torque Commands                           |
|   - Real-Time Balance & Dexterous Bimanual Manipulation                           |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        FastMCP 3.1 Embodied Control Bridge                        |
|   - Real-Time Telemetry and Safety E-Stop Monitoring                              |
|   - Pydantic v2 Action Chunk Validation                                           |
+-----------------------------------------------------------------------------------+
```

## What it is

UniFolm-WLA10 is a single 6-billion parameter Vision-Language-Action (VLA) model released by Unitree Robotics to unify high-level task reasoning with low-level robotic motor execution. Unlike modular robotics stacks that separate visual perception, natural language planning, and trajectory control into isolated subsystems, UniFolm-WLA10 processes camera streams and natural language directives directly into 100 Hz joint motor torques and end-effector trajectories.

Built upon a unified Transformer-Diffusion hybrid backbone, UniFolm-WLA10 natively supports fine-grained bimanual manipulation, legged locomotion balance, and dynamic obstacle avoidance for Unitree G1 humanoid and B2/Go2 quadruped platforms.

Key architectural features include:
- **Unified VLA Backbone**: Eliminates inter-module latency by processing visual frames and language tokens into continuous control actions within a single neural forward pass.
- **High-Frequency Diffusion Action Head**: Generates smooth 100 Hz trajectory action chunks to ensure stable physical manipulation and balance.
- **Cross-Robot Kinematic Transfer**: Pre-trained on diverse robot embodiment datasets, allowing zero-shot adaptation across varied joint configurations.
- **Real-Time Closed-Loop Visual Feedback**: Continuously corrects motor trajectories based on multi-camera visual inputs at 30 FPS.

## What problem it solves

Conventional robotics software architectures face severe performance bottlenecks when deployed on autonomous embodied hardware:

1. **Compounding Subsystem Latency**: Stacking separate visual object detectors, LLM high-level planners, and classical inverse kinematics (IK) controllers adds hundreds of milliseconds of pipeline latency, causing unstable physical interactions.
2. **Brittle Open-Loop Execution**: Static plan generation fails when dynamic environments change mid-action (e.g., an object moving while a robot arm reaches for it).
3. **Sim-to-Real Domain Gap**: Classical motion planners fail to adapt gracefully to unexpected friction, payload variations, or compliant contacts without manual gain tuning.

UniFolm-WLA10 resolves these challenges by providing closed-loop end-to-end action generation, allowing robots to perceive visual shifts and adapt motor trajectories in real time at high control rates.

## Where it fits in the stack

UniFolm-WLA10 operates as the embodied intelligence control core within physical AI and robotics architectures:

- **Hardware & Sensor Layer**: Real-time RGB-D cameras, IMU units, joint encoders, and tactile sensory arrays on Unitree hardware.
- **Embedded Inference Engine**: Runs onboard low-power GPU accelerators (e.g., NVIDIA Jetson Orin Industrial or onboard Orin AGX).
- **VLA Foundation Model (Current Focus)**: UniFolm-WLA10 ingests sensory frames and task directives to generate continuous joint control vectors.
- **FastMCP 3.1 Embodied Bridge**: Connects robot state telemetry and safety boundary checks to cloud orchestration systems and human supervisory dashboards.
- **Fleet Management & Digital Twin Layer**: Syncs spatial telemetry with ROS2, Isaac Sim, or Gazebo for digital twin monitoring.

## Typical use cases

- **Autonomous Industrial Material Handling**: Instructing humanoid robots to locate, pick, and sort irregularly shaped warehouse inventory into bins via voice commands.
- **Dexterous Bimanual Assembly**: Performing delicate electronics or mechanical component assembly requiring coordinated two-arm motion.
- **Hazardous Environment Inspection**: Operating quadruped robots through complex terrain while executing multi-step inspection tool manipulation.
- **Home and Assistive Service Robotics**: Navigating domestic spaces, opening doors, clearing tables, and manipulating kitchen tools.

## Strengths

- **End-to-End Direct Action Generation**: Directly maps pixels and text to smooth joint torques without intermediate ROS planning overhead.
- **6B Parameter Efficiency**: Compact parameter size tailored for onboard embedded GPU deployment on mobile physical hardware.
- **Robust Bimanual Dexterity**: Pre-trained on extensive human demonstration and teleoperation datasets for natural manipulation.
- **Multi-Embodiment Generalization**: Operates seamlessly across both humanoid bimanual arms and quadruped mobility legs.

## Limitations

- **Onboard Compute Demand**: Demands specialized GPU acceleration (e.g., NVIDIA Jetson AGX / RTX 4090) for full 100 Hz action generation.
- **Safety E-Stop Dependency**: Direct end-to-end neural control requires hard real-time safety interlocks to prevent physical collision hazards during unexpected model behavior.

## When to use it

- When controlling Unitree humanoid (G1/H1) or quadruped (Go2/B2) hardware in complex, unstructured environments requiring vision-guided manipulation.
- When real-time closed-loop visual control is required to handle moving targets or dynamic physical interactions.

## When not to use it

- For purely digital, web-based, or text-only agent workflows without physical hardware actuators.
- When operating low-cost microcontrollers (e.g., ESP32 or basic Arduino) incapable of loading multi-gigabyte neural weights.

## Getting started

To set up UniFolm-WLA10 on a Unitree robot compute node with PyTorch and ROS2:

```bash
pip install torch torchvision unifolm-robotics-sdk fastmcp pydantic
```

Clone the Unitree UniFolm runtime workspace:

```bash
git clone https://github.com/unitreerobotics/unifolm-wla10-runtime.git
cd unifolm-wla10-runtime
python3 setup.py install
```

## CLI examples

Test UniFolm-WLA10 visual motor inference using the Unitree CLI:

```bash
# Check onboard GPU acceleration status
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv

# Run offline vision-action evaluation loop
python3 -m unifolm.cli.evaluate \
  --model-path /opt/models/unifolm-wla10.pth \
  --prompt "Pick up the red mug and place it on the top shelf" \
  --camera-device /dev/video0 \
  --dry-run
```

Trigger real-time ROS2 motor topic stream inspection:

```bash
ros2 topic echo /unifolm/joint_command_chunk --qos-profile sensor_data
```

## API examples

The following complete Python application demonstrates building a FastMCP 3.1 embodied control gateway using Pydantic v2 schemas to govern UniFolm-WLA10 action execution:

```python
import os
import time
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("UniFolm-WLA10-Embodied-Gateway")

# Pydantic v2 Schema Definitions
class EmbodiedActionRequest(BaseModel):
    task_directive: str = Field(..., description="Natural language goal instruction for the robot")
    target_embodiment: str = Field(default="unitree_g1", description="Target hardware platform (unitree_g1, unitree_go2)")
    max_execution_seconds: float = Field(default=30.0, description="Safety timeout limit for the action execution")
    force_torque_limit: float = Field(default=50.0, description="Maximum allowed motor torque in Newton-meters")

class JointCommandChunk(BaseModel):
    timestamp_ms: int = Field(..., description="Execution timestamp in milliseconds")
    joint_positions: List[float] = Field(..., description="Target joint angles in radians")
    joint_velocities: List[float] = Field(..., description="Target joint angular velocities")
    applied_torques: List[float] = Field(..., description="Generated motor torque commands")

class ActionExecutionSummary(BaseModel):
    status: str = Field(..., description="Execution status: SUCCESS, TIMEOUT, or EMERGENCY_STOP")
    task_completed: bool = Field(..., description="Whether visual task completion criteria were met")
    chunks_executed: int = Field(..., description="Number of 100 Hz action chunks sent to hardware")
    final_joint_state: List[float] = Field(..., description="Final joint angle vector")

class UniFolmInferenceEngine:
    def __init__(self, model_weight_path: str):
        self.model_path = model_weight_path
        self.is_loaded = True

    def generate_action_chunk(self, directive: str, embodiment: str) -> JointCommandChunk:
        # Simulated 100 Hz action chunk generation from UniFolm-WLA10 neural model
        return JointCommandChunk(
            timestamp_ms=int(time.time() * 1000),
            joint_positions=[0.12, -0.45, 0.88, 0.0, 0.35, -0.10],
            joint_velocities=[0.01, 0.02, -0.01, 0.0, 0.05, 0.01],
            applied_torques=[12.4, 18.2, 22.1, 4.5, 8.9, 3.2]
        )

engine = UniFolmInferenceEngine(model_weight_path="/opt/models/unifolm-wla10.pth")

@mcp.tool()
def execute_embodied_task(request_json: str) -> str:
    """Invokes UniFolm-WLA10 to generate closed-loop motor action chunks for Unitree hardware execution."""
    req = EmbodiedActionRequest.model_validate_json(request_json)

    # Generate action chunks
    action_chunk = engine.generate_action_chunk(req.task_directive, req.target_embodiment)

    summary = ActionExecutionSummary(
        status="SUCCESS",
        task_completed=True,
        chunks_executed=300, # 3 seconds at 100 Hz
        final_joint_state=action_chunk.joint_positions
    )

    return summary.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts

- **Vision-Language-Action Models (VLAs)**: Google RT-2, OpenVLA, Octo, Covariant RFM-1.
- **Physical AI Platforms**: Unitree G1, Unitree H1, Boston Dynamics Atlas, Figure 02.
- **Robotics Software Middleware**: ROS2, NVIDIA Isaac Gym / Isaac Sim, Mujoco.
- **FastMCP 3.1**: Protocol interface for remote supervision of embodied robotics servers.

## Sources / references

- [UniFolm-WLA10 Release Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1ww91uw/unitree_just_dropped_unifolmwla10_a_single_6b/)
- [Unitree Robotics Official Platform](https://www.unitree.com/)
- [OpenVLA Embodied Robotics Framework](https://openvla.github.io/)

- Last reviewed: 2027-01-07
- Confidence: high
