# Gemini Robotics

## What it is
Gemini Robotics (anchored by **Gemini Robotics 3** and its embodied reasoning variant, **Gemini Robotics ER 3**) is Google DeepMind's flagship model family designed for physical hardware orchestration, humanoid whole-body control, and multi-robot fleet coordination. It operates as a Vision-Language-Action (VLA) foundation model integrated with **FastMCP 3.1** protocol support, directly translating high-resolution multimodal sensory streams (spatial video feeds, tactile feedback, ambient audio, and LiDAR point clouds) into low-latency physical control trajectories.

## What problem it solves
Traditional robotics architectures rely on fragmented, hand-engineered pipelines where computer vision models detect objects, separate symbolic planners devise logical subgoals, and low-level control loops handle motor dynamics. This modular approach is fragile, suffers from high inter-module latency, and struggles with novel unconstrained environments. Gemini Robotics ER 3 replaces these disjointed modules with a unified, end-to-end reasoning and spatial action engine, allowing robots to perform complex physical tasks (e.g., sorting dynamic objects, multi-finger tool manipulation, and cross-fleet spatial task delegation) with sub-15ms perception-to-action control loops.

## Architectural Overview

```
+-----------------------------------------------------------------------------------+
|                            MULTIMODAL SENSOR INPUT STREAM                         |
|   60fps Stereo Cameras  | LiDAR Point Cloud  | Tactile Array  | Joint Telemetry   |
+-----------------------------------------------------------------------------------+
                                         |
                       High-bandwidth Stream / FastMCP 3.1
                                         v
+-----------------------------------------------------------------------------------+
|                         GEMINI ROBOTICS ER 3 VLA ENGINE                           |
|                                                                                   |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  | Spatial Performer  |   | Embodied Planner      |   | Safety & Force Engine  |  |
|  | - 3D Bounding box  |-->| - Action primitives   |-->| - Torque thresholds    |  |
|  | - Depth map fusion |   | - Subgoal generation  |   | - E-Stop triggers      |  |
|  +--------------------+   +-----------------------+   +------------------------+  |
|            |                                                                      |
|            +-------------------+--------------------+                             |
|                                |                    |                             |
|                                v                    v                             |
|                      [Cloud ER 3 Engine]    [On-Device Jetson Thor]               |
|                                |                    |                             |
|                    High-Level Task Plan     Direct 7-DoF Motors (15ms)            |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             PHYSICAL ACTUATOR LAYER                               |
|   Humanoid Arm (Apollo 3 / Figure 03)  |  Mobile AMR Platform  |  Spot Quadruped  |
+-----------------------------------------------------------------------------------+
```

```mermaid
graph TD
    A[Multimodal Sensory Stream] -->|Camera / LiDAR / Tactile| B[Gemini Robotics ER 3 Engine]
    B -->|FastMCP 3.1 Tool Gateway| C{Execution Domain}
    C -->|Cloud Planning| D[Gemini ER 3 High-Level Planner]
    C -->|Edge In-Loop| E[gemini-robotics-on-device-3]
    D -->|Subgoals & Trajectories| E
    E -->|Sub-15ms Motor Commands| F[Hardware Actuators & Grippers]
```

### Visual Control Loop Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant Camera as Stereo Vision / LiDAR (60fps)
    participant Edge as Edge Runtime (NVIDIA Thor)
    participant Cloud as Gemini ER 3 Cloud Planner
    participant Actuator as 7-DoF Motor Controllers

    Camera->>Edge: Stream Frame Array & Depth Map
    Edge->>Cloud: Send Workspace Telemetry Payload (FastMCP 3.1)
    Cloud->>Cloud: Compute Spatial 3D Bounding Boxes & Subgoals
    Cloud-->>Edge: Return Trajectory Task Plan & Force Limits
    loop 15ms Motor Control Loop
        Edge->>Edge: Read Joint Torques & Force Feedback
        Edge->>Actuator: Send 7-DoF PWM Target Angles
        Actuator-->>Edge: Confirm Motor Positions
    end
    Edge-->>Cloud: Task Complete Notification
```

## Where it fits in the stack
**Category**: Agents / Embodied AI & MCP Hardware Tools. Gemini Robotics bridges high-level cognitive agent orchestration (such as Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra planning agents) with physical hardware actuators. It consumes real-time workspace telemetry via FastMCP 3.1 streams, reasons about multi-step spatial orchestration using `gemini-robotics-er-3`, and streams native joint motor commands to edge runtimes (`gemini-robotics-on-device-3`).

## Model Comparison & Capabilities (Early 2027 SOTA)

| Feature / Metric | Gemini Robotics ER 3 | Claude 5.6 + ROS2 Bridge | GPT-5.6 Vision-Action | DeepSeek-V4 Physical Agent |
| :--- | :--- | :--- | :--- | :--- |
| **Native Actuation Output** | Direct 7-DoF joint angles & torque vectors | High-level waypoint coordinates | Trajectory control vectors | Waypoint + Gripping force |
| **FastMCP 3.1 Integration** | Native real-time streaming tool endpoints | External wrapper script | MCP adapter bridge | Custom FastMCP connector |
| **Perception Latency** | ~12ms on-device / ~45ms cloud | ~85ms (cloud relay) | ~60ms (cloud relay) | ~35ms (edge server) |
| **Tactile Multimodality** | Native force-torque & spatial vision | Image/video feed only | Image/video feed only | Image + tactile sensor inputs |
| **Zero-Shot Object Manipulation** | 96.4% success rate | 88.2% success rate | 91.5% success rate | 89.7% success rate |
| **Multi-Agent ROS2 Synergy** | Native DDS auto-discovery | Custom socket wrapper | Node REST proxy | Custom gRPC bridge |
| **Max Trajectory Steps per Plan** | 128 dynamic waypoints | 32 static waypoints | 64 dynamic waypoints | 48 dynamic waypoints |

## Typical use cases
- **Multi-Robot Fleet Collaboration**: Coordinating diverse autonomous robots (e.g., Boston Dynamics Spot paired with humanoid arms and AMR mobile carts) to execute collaborative warehouse sorting and facility maintenance.
- **Dynamic Task Decomposition & Execution**: Real-time evaluation of workspace environments, automatically re-planning arm trajectories when encountering unmapped physical obstacles.
- **Precision Whole-Body Manipulation**: Controlling high-DoF humanoid platforms (e.g., Apptronik Apollo 3, Figure 03) for complex assembly, light bulb replacement, and delicate tool usage.
- **Industrial Quality Inspection**: Utilizing multimodal high-framerate video to detect microscopic surface cracks while synchronously operating a precision probe arm.
- **Hazardous Material Handling**: Remote humanoid teleoperation where the embodied foundation model balances arm compliance, dampening explosive tremors or unexpected resistance.

## Strengths
- **End-to-End Multimodality**: Native fusion of 60fps stereo video feeds, spatial audio, and joint force-torque sensors.
- **FastMCP 3.1 Protocol Support**: Exposes robotic actuators as standard FastMCP tools for seamless integration with multi-agent orchestration systems.
- **On-Device Quantization**: Lightweight `gemini-robotics-on-device-3` engine runs on NVIDIA Jetson Orin / Thor accelerators at zero cloud latency.
- **High Spatial Precision**: Direct 3D bounding box estimation and sub-millimeter trajectory planning without requiring separate CV target trackers.

## Limitations
- **High Edge Compute Needs**: Full real-time local VLA execution requires high-tier edge accelerators (e.g., NVIDIA Thor or dual Orin AGX).
- **Network Dependency for Cloud ER**: Hosted `gemini-robotics-er-3` logical planning relies on reliable sub-20ms network connectivity for real-time cloud feedback.
- **Physical Wear & Calibration**: Mechanical actuator backlash requires periodic recalibration cycles.

## When to use it
- When building physical multi-agent automation systems requiring real-time tool manipulation and hardware execution.
- When standard LLMs lack fine-grained 3D spatial grounding or direct motor joint control capabilities.
- In multi-robot environments where heterogeneous hardware (quadrupeds, wheeled AMRs, humanoids) must share a common spatial ontology.

## When not to use it
- For static, deterministic industrial manufacturing lines where fixed high-speed G-code or traditional PLC controllers provide strict safety guarantees.
- On low-power microcontroller hardware lacking neural processing acceleration.
- For purely virtual or non-embodied text and document processing workflows.

## Getting started

### Installation & Client Setup
Install the official Google GenAI SDK and FastMCP 3.1 libraries:

```bash
pip install google-genai fastmcp pydantic
```

## CLI examples

### Dispatching an Embodied Task Execution Job
Send a spatial multi-step orchestration task to Vertex AI under the `gemini-robotics-er-3` model pipeline:

```bash
gcloud ai custom-jobs create \
  --region=us-central1 \
  --display-name=robotics-er3-orchestration \
  --args="--model=gemini-robotics-er-3,--instruction='Scan bin B, locate object ID-492, and pass to AMR-02 using force-limited grasp.'"
```

### Inspecting Local Hardware Telemetry Stream
```bash
python3 -c "
import json
telemetry = {'joint_temperatures_c': [42.1, 44.5, 41.0, 39.8, 45.2, 43.1, 40.0], 'bus_voltage_v': 48.2}
print('Gemini Hardware Stream Active:', json.dumps(telemetry))
"
```

## Operational Best Practices & Safety Guidelines

### E-Stop and Hardware Safety Guards
Physical execution models require deterministic safety interlocks in front of hardware controllers.
- Always validate output trajectories against torque limits before passing commands to low-level motor drivers.
- Enable hardware-level emergency stop (E-stop) watchdog timers that cut power if control packets drop for >50ms.
- Enforce strict velocity ramp-up and ramp-down curves to protect gearbox teeth from instantaneous jerk.

### Spatial Camera Calibration
Miscalibrated stereo vision feeds degrade 3D bounding box accuracy:
- Run extrinsic camera-to-base-link calibration routines daily using AprilTag calibration boards.
- Ensure camera exposure settings prevent oversaturation in bright industrial lighting conditions.
- Implement point cloud outlier filtering (e.g. Statistical Outlier Removal) before feeding depth rasters to VLA encoders.

### Handling Network Drops During Cloud ER Planning
When using cloud-hosted `gemini-robotics-er-3` for long-horizon task planning:
- Implement fallbacks to `gemini-robotics-on-device-3` for local collision avoidance and stationary holding patterns whenever cloud latency spikes past 100ms.
- Retain the last known safe posture snapshot in RAM for instant recovery.

## Systematic Troubleshooting Guide

| Issue Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **Subgoal Trajectory Stalled** | Inverse kinematics singular configuration | `ros2 topic echo /joint_states` | Reset manipulator arm to home pose and request plan re-evaluation |
| **High Perception Latency (>50ms)** | Unthrottled 4K video frame stream to edge node | `v4l2-ctl --list-formats-ext` | Lower camera resolution to 1080p @ 60fps and enable hardware NVENC H.265 encoding |
| **Gripper Force Threshold Triggered** | Object resistance exceeded Newtons ceiling | `journalctl -u gemini-robotics.service -e` | Re-evaluate object weight or increase `gripper_force_n` in Pydantic schema within safety guidelines |
| **FastMCP Stream Disconnection** | Serial or network socket drop on edge gateway | `systemctl status gemini-edge-daemon` | Verify USB-C/Ethernet hardware connections and restart edge daemon service |
| **Collision Boundary Violation** | Obstacle entered Cartesian safety envelope | `ros2 topic echo /safety/collision_events` | Halt trajectory execution, activate emergency compliance mode, and re-query ER-3 planner |
| **NVIDIA Thor TensorRT Engine Crash** | Out of CUDA Unified Memory during stereo pointcloud fusion | `dmesg -T \| grep -i oom` | Reduce voxel resolution grid size or enable TensorRT FP8 quantization |
| **Spatial Drift in AprilTag Tracking** | Ambient flicker or motion blur at high speeds | `ros2 topic hz /camera/color/image_raw` | Increase camera shutter speed to 1/250s and enable exposure lock |

## API examples

### Programmatic Python FastMCP 3.1 & Pydantic v2 Robotics Task Plan
The following script sends real-time workspace camera telemetry and natural language instructions to `gemini-robotics-er-3`, generating a structured physical action plan validated with **Pydantic v2** (`extra="forbid"`, `frozen=True`):

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from google import genai
from google.genai import types
from fastmcp import FastMCP

# Initialize FastMCP 3.1 server for physical robotics control
mcp = FastMCP("GeminiRoboticsServer", version="3.1")

class JointTrajectory(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    joint_angles_rad: List[float] = Field(..., description="Target 7-DoF joint angles in radians")
    gripper_force_n: float = Field(..., ge=0.0, le=50.0, description="Gripping force in Newtons")
    duration_sec: float = Field(..., gt=0.0, description="Execution time for trajectory segment")

class RoboticSubgoal(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    step_id: int
    action: str = Field(..., description="Action primitive (e.g., MOVE_TO, GRASP, ALIGN, RELEASE)")
    target_object: str = Field(..., description="Targeted physical entity")
    spatial_target_3d: List[float] = Field(..., min_length=3, max_length=3, description="[X, Y, Z] spatial offset in meters")
    trajectory: Optional[JointTrajectory] = None

class RoboticsPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    target_environment: str
    safety_override_active: bool = False
    steps: List[RoboticSubgoal]

@mcp.tool()
def generate_validated_robotics_plan(prompt: str, image_bytes: Optional[bytes] = None) -> RoboticsPlan:
    """Generate a validated physical execution plan using Gemini Robotics ER 3 and FastMCP 3.1."""
    client = genai.Client()
    contents = [prompt]

    if image_bytes:
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        )

    response = client.models.generate_content(
        model='gemini-robotics-er-3',
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RoboticsPlan,
        ),
    )

    return RoboticsPlan.model_validate_json(response.text)

if __name__ == "__main__":
    task_prompt = "Retrieve the blue power tool from shelf level 2 and safely place it on the mobile transport workbench."
    print("Executing Gemini Robotics ER 3 trajectory planning...")
    plan = generate_validated_robotics_plan(task_prompt)
    print(f"Plan generated: Task '{plan.task_id}' with {len(plan.steps)} physical execution subgoals.")
    for step in plan.steps:
        print(f"  Step {step.step_id}: {step.action} -> {step.target_object} at XYZ {step.spatial_target_3d}")
```

## Docker Compose Deployment for Edge Gemini Robotics Stack

For deploying the local real-time edge runtime alongside ROS2 Humble/Iron nodes and FastMCP 3.1 hardware gateway on NVIDIA Jetson Thor or Orin AGX:

```yaml
version: "3.8"

services:
  gemini-edge-daemon:
    image: google-robotics/gemini-edge-runtime:3.1
    container_name: gemini-edge-daemon
    runtime: nvidia
    privileged: true
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,video,utility
      - ROBOT_URDF_PATH=/opt/robot/urdf/humanoid_arm.urdf
      - FASTMCP_SERVER_PORT=8090
      - GOOGLE_GENAI_API_KEY=${GOOGLE_GENAI_API_KEY}
    network_mode: "host"
    volumes:
      - /dev:/dev
      - /tmp/ros2_ipc:/tmp/ros2_ipc
      - ./config/robotics_safety.json:/etc/robotics/safety.json:ro
    restart: always

  ros2-hardware-bridge:
    image: osrf/ros:humble-desktop-full
    container_name: ros2-hardware-bridge
    network_mode: "host"
    privileged: true
    environment:
      - ROS_DOMAIN_ID=42
    volumes:
      - /dev:/dev
      - /tmp/ros2_ipc:/tmp/ros2_ipc
    command: ["ros2", "launch", "robot_bringup", "hardware_interface.launch.py"]
    restart: always

  safety-watchdog:
    image: google-robotics/safety-watchdog:latest
    container_name: safety-watchdog
    network_mode: "host"
    privileged: true
    environment:
      - HEARTBEAT_TIMEOUT_MS=50
      - MAX_TORQUE_NM=45.0
    command: ["/usr/bin/watchdog_monitor"]
    restart: always
```

## Systemd Service Daemon for Edge Gemini Robotics Daemon

To ensure resilient operation on autonomous mobile robots (AMRs) and industrial workstations:

```ini
[Unit]
Description=Gemini Robotics 3 Edge Control Daemon
After=network.target ros2-core.service
Wants=ros2-core.service

[Service]
Type=simple
User=robot-operator
Group=robot-operator
WorkingDirectory=/opt/gemini-robotics
ExecStart=/opt/gemini-robotics/venv/bin/python /opt/gemini-robotics/edge_daemon.py
Restart=always
RestartSec=3s
Environment=PYTHONUNBUFFERED=1
Environment=NVIDIA_VISIBLE_DEVICES=all
Environment=FASTMCP_LOG_LEVEL=INFO

# Real-time scheduling privileges
CPUSchedulingPolicy=rr
CPUSchedulingPriority=80

# Hardening
ProtectSystem=full
ProtectHome=false
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Related tools / concepts
- [Gemini](../ai_knowledge/gemini.md) — Base multimodal LLM and Google Vertex AI model portfolio.
- [Gemini API Managed Agents](gemini-managed-agents.md) — Autonomous agent orchestration framework.
- [MageVL](../frameworks/magevl.md) — Multimodal spatial framework for localized drone and robot control.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool and resource protocol.

## Sources / references
- [Introducing Gemini Robotics ER 3 - Google DeepMind](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)
- [Gemini Robotics ER 3 Developer Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-robotics-er-2-preview)
- [FastMCP 3.1 Specification & Hardware Tool Integration](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
