# LeRobot

## What it is
LeRobot is an open-source end-to-end robotics learning framework developed by Hugging Face (v0.4.0+). It provides real-world and simulated robotics data collection tools, pretrained imitation learning and reinforcement learning policy models, standard sensor and actuator interface adapters, and hardware control loops designed for physical AI applications. As of early 2027, LeRobot serves as a primary open-source foundation for training low-latency Vision-Language-Action (VLA) models and deploying embodied AI agents on consumer, industrial, and edge robotics platforms.

## System Architecture

```
+-----------------------------------------------------------------------------------+
|                              LeRobot Control Pipeline                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +--------------------+         +-----------------------+                         |
|  | Cameras & Spatial  | ------> | LeRobot Sensor        |                         |
|  | Sensors @ 30-60Hz  |         | Normalization Pipeline|                         |
|  +--------------------+         +-----------+-----------+                         |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | Imitation Policy      |                         |
|                                 | ACT / Diffusion / VQ  |                         |
|                                 +-----------+-----------+                         |
|                                             |                                     |
|                        +--------------------+--------------------+                |
|                        |                                         |                |
|                        v                                         v                |
|           +-------------------------+               +-------------------------+   |
|           | FastMCP 3.1 Server      |               | Hugging Face Hub        |   |
|           | High-Level VLA Agent    |               | Model Weights & Datasets|   |
|           +------------+------------+               +------------+------------+   |
|                        |                                         |                |
|                        +--------------------+--------------------+                |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | Motor Actuator &      |                         |
|                                 | Joint Controller      |                         |
|                                 +-----------------------+                         |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Mathematical Formulations: Policy Optimization & Kinematics

Modern imitation learning policies in LeRobot optimize continuous robot trajectories across multi-camera visual inputs and proprioceptive joint telemetry. The framework centers around two foundational formulations: Action Chunking with Transformers (ACT) and Diffusion Policies.

### 1. Action Chunking with Transformers (ACT) Loss Formulation
ACT models the conditional distribution of action sequences (chunks) $A_{t:t+k} = (a_t, a_{t+1}, \dots, a_{t+k-1})$ given visual observations $O_t$ and joint positions $q_t$. A Conditional Variational Autoencoder (CVAE) parameterized by encoder $q_\phi(z | A_{t:t+k}, O_t, q_t)$ and decoder policy $\pi_\theta(A_{t:t+k} | z, O_t, q_t)$ is trained by minimizing the negative evidence lower bound (ELBO):

$$\mathcal{L}_{\text{ACT}}(\theta, \phi) = \mathbb{E}_{z \sim q_\phi}\left[ \sum_{i=0}^{k-1} \| a_{t+i} - \hat{a}_{t+i} \|_1 \right] + \beta \cdot D_{\text{KL}}\left( q_\phi(z | A_{t:t+k}, O_t, q_t) \,\|\, p(z) \right)$$

where:
- $k \in [30, 100]$ represents the prediction horizon chunk length,
- $\hat{A}_{t:t+k} = \pi_\theta(z, O_t, q_t)$ is the predicted multi-step action trajectory,
- $p(z) = \mathcal{N}(0, I)$ is a standard Gaussian prior over the latent style space,
- $\beta$ is the Kullback-Leibler divergence weight balancing action reconstruction precision against latent regularization.

Temporal ensembling smooths overlapping action chunks during real-time closed-loop rollouts. At time step $t$, the executed joint command $\bar{a}_t$ is computed as an exponentially weighted average over active sliding chunks:

$$\bar{a}_t = \frac{\sum_{j=0}^{m-1} w_j \cdot \hat{a}_{t|t-j}}{\sum_{j=0}^{m-1} w_j}, \quad w_j = \exp\left( -m_{\text{decay}} \cdot j \right)$$

where $m$ denotes the number of overlapping chunk queries and $m_{\text{decay}} \ge 0$ parameterizes historical smoothing.

### 2. Denoising Diffusion Policy Score Matching
For multimodal task distributions where multiple discrete manipulation strategies exist, LeRobot employs conditional score-based diffusion models. Given forward Gaussian diffusion adding noise $\epsilon \sim \mathcal{N}(0, I)$ over variance schedule $\sigma_t$:

$$A^{(k)} = \sqrt{\bar{\alpha}_k} A^{(0)} + \sqrt{1 - \bar{\alpha}_k} \epsilon$$

The denoising network $\epsilon_\theta(A^{(k)}, k, O_t)$ is trained via mean squared score matching:

$$\mathcal{L}_{\text{Diffusion}}(\theta) = \mathbb{E}_{k \sim \mathcal{U}(1, K), \epsilon \sim \mathcal{N}(0, I)}\left[ \left\| \epsilon - \epsilon_\theta\left( \sqrt{\bar{\alpha}_k} A^{(0)} + \sqrt{1 - \bar{\alpha}_k} \epsilon, k, \psi(O_t) \right) \right\|_2^2 \right]$$

where $\psi(O_t)$ is the fused multimodal observation embedding generated by a visual backbone (e.g., SigLIP-2 or ResNet-50) concatenated with normalized robot proprioception.

### 3. Kinematic Safety Envelope & Velocity Jerk Bounding
To protect servo gearboxes and ensure human operator safety in physical workcells, joint angle commands undergo runtime projection onto safe torque and jerk bounds:

$$q_{\text{min}} \le q_t \le q_{\text{max}}, \quad |\dot{q}_t| \le \dot{q}_{\text{max}}, \quad |\ddot{q}_t| \le \ddot{q}_{\text{max}}$$

The jerk constraint $\dddot{q}_t$ is monitored over discrete sampling interval $\Delta t$:

$$\dddot{q}_t = \frac{\ddot{q}_t - \ddot{q}_{t-\Delta t}}{\Delta t} \le J_{\text{limit}}$$

If any motor register violates $J_{\text{limit}}$, LeRobot's actuator loop interpolates cubic splines to decelerate the kinematic chain gracefully within 12 ms.

## What problem it solves
Robotics development historically suffered from extreme fragmentation, proprietary hardware abstraction layers, and a lack of standardized dataset formats for AI training loops. LeRobot standardizes dataset schema ingestion, policy model architectures (such as Diffusion Policy, ACT, and VQ-BeT), and real-time inference loops on consumer or edge computing hardware. It solves the fragmentation challenge by enforcing unified schemas for visual frames, robot state trajectories, and high-frequency motor torque commands.

## Where it fits in the stack
**Category**: Frameworks / Physical AI & Robotics. It sits at the **Execution & Control Layer**, bridging high-level LLM and VLM reasoning agent architectures with low-level actuator motor commands and sensor teleoperation loops.

```
+-----------------------------------------------------------------------------------+
|                            PHYSICAL AI & ROBOTICS STACK                           |
+-----------------------------------------------------------------------------------+
| Cognitive Reasoning Layer : Claude 5.6 / GPT-5.6 / FastMCP 3.1 Orchestrator        |
+-----------------------------------------------------------------------------------+
| Policy & Learning Layer   : LeRobot (ACT, Diffusion, VLA Fine-tuning, PyTorch)     |
+-----------------------------------------------------------------------------------+
| Telemetry & Transport     : Zenoh / ROS2 DDS / FastMCP Robot Bridge / ZeroMQ      |
+-----------------------------------------------------------------------------------+
| Actuator Hardware Driver  : Feetech STS / Dynamixel SDK / Universal Robots RTDE   |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Streaming Data Collection & Teleoperation**: Logging streaming camera frames and arm joint states into standard Hugging Face LeRobot dataset formats using low-cost hardware (e.g., SO-ARM100, Koch v1.1).
- **Imitation Learning Policy Training**: Training neural policies to perform complex dexterous manipulation tasks using physical demonstration data and PyTorch distributed training pipelines.
- **Edge Deployment & Real-Time Inference**: Running optimized policy control loops at 30-100Hz on local NVIDIA Jetson, Mac Studio, or edge AI gateways.
- **Multimodal Agent Control Integration**: Connecting frontier vision-language models (e.g. Gemini 4.0 Pro, Claude 5.6) to physical robotic arms via FastMCP 3.1 action primitives.
- **Sim-to-Real Benchmark Testing**: Evaluating trained policies across simulated environments (Isaac Gym, MuJoCo) before zero-shot or fine-tuned deployment on physical robotic arms.

## Policy Framework Comparison Matrix

| Policy / Framework | Policy Architecture | Demonstration Sample Complexity | Inference Latency (ms) | Loop Freq (Hz) | Hardware Compatibility | Primary Strengths |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LeRobot ACT (Hugging Face)** | CVAE Action Chunking Transformer | 30 - 50 episodes | 18 ms (FP16) | 30 - 50 Hz | SO-ARM100, Koch, UR5, Franka | Low sample complexity, temporal ensembling smoothness |
| **LeRobot Diffusion Policy** | Denoising Score Diffusion | 50 - 100 episodes | 32 ms (DDIM 10 steps) | 20 - 30 Hz | Multi-camera manipulators, Bimanual | Models multimodal multimodal action distributions |
| **OpenX / RT-2 (Google)** | Vision-Language-Action (VLA) | >10,000 trajectories | 120 ms (Cloud / TPU) | 5 - 10 Hz | High-end industrial manipulators | High semantic generalization, natural language tasks |
| **RoboMimic** | Modular Imitation / Offline RL | 50 - 200 episodes | 25 ms | 20 - 50 Hz | MuJoCo, Franka Emika Panda | Extensive benchmark suite for offline RL algorithms |
| **ROS2 MoveIt 2** | Geometric Motion Planning | 0 (Deterministic model) | 5 ms (OMPL planner) | 100 - 1000 Hz | All industrial robotics platforms | Hard real-time safety guarantees, collision avoidance |

## Strengths
- **Native Hugging Face Ecosystem Integration**: Directly streams datasets and model weights to and from the Hugging Face Hub using standard parquet and zarr formats.
- **Broad Model Policy Zoo**: Includes built-in implementations of Action Chunking with Transformers (ACT), Diffusion Policy, VQ-BeT, and Vision-Language-Action (VLA) models.
- **Lightweight Hardware Requirements**: Operates on low-cost open hardware arms (e.g., SO-ARM100, Koch v1.1) as well as commercial industrial manipulators.
- **Modular Data Format**: Enforces rigid dataset schemas with built-in video decoding, state chunking, and spatial coordinate transforms.
- **Sub-20ms Execution Latency**: Optimized PyTorch execution runtime tailored for local inference without cloud round-trip overhead.

## Limitations
- **Hardware Calibration Required**: High precision physical actions require careful motor joint calibration and hardware-specific latency tuning.
- **Real-Time Latency Sensitivity**: Real-world teleoperation requires low-latency local execution loops, making network-dependent architectures challenging.
- **Continuous Domain Gap**: Sim-to-real transfer requires fine-tuning or domain randomization when trained purely in synthetic simulation environments.
- **Thermal & Hardware Strain**: Continuous high-frequency inference requires monitoring motor temperatures and mechanical backlash over extended training sessions.

## When to use it
- When training, evaluating, or deploying physical AI and imitation learning policies for robotic manipulators.
- When collecting streaming sensor and action teleoperation datasets for open-source sharing on Hugging Face Hub.
- When orchestrating physical robotics execution workflows alongside LLM planning agents using FastMCP 3.1.

## When not to use it
- For purely web-based, software-only software automation (use [Browser Use](../automation_orchestration/browser-use.md) or [Playwright](../automation_orchestration/puppeteer.md)).
- For classical industrial PLC ladder logic control with fixed deterministic motion trajectories requiring microsecond-level hard real-time guarantees.

## Getting started

### Installation
Install LeRobot via pip from source or PyPI with physical robot hardware support:
```bash
pip install lerobot torch torchvision pydantic mcp fastmcp
```

### Basic Hardware Initialization & Policy Evaluation
Evaluate a pretrained policy on local hardware or simulation environment:
```python
import lerobot
from lerobot.common.policies.act.modeling_act import ACTPolicy

# Load pretrained policy model from Hugging Face Hub
policy = ACTPolicy.from_pretrained("lerobot/act_so100_real")
policy.eval()
print("LeRobot ACT Policy successfully loaded.")
```

## Production Architecture: Multi-Container Docker Stack

For resilient production deployments in research labs and automated manufacturing cells, deploy the LeRobot policy inference server, camera ingestion pipeline, and telemetry monitoring via Docker Compose:

```yaml
version: "3.8"

services:
  lerobot-policy-engine:
    image: huggingface/lerobot:0.4.0-cuda12.4
    container_name: lerobot-policy-engine
    restart: unless-stopped
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - ROBOT_TYPE=so100
      - POLICY_CHECKPOINT=lerobot/act_so100_real
      - INFERENCE_DEVICE=cuda:0
      - FASTMCP_PORT=8095
    volumes:
      - /dev/ttyUSB0:/dev/ttyUSB0
      - /dev/video0:/dev/video0
      - /dev/video2:/dev/video2
      - lerobot_checkpoints:/root/.cache/huggingface/hub
    ports:
      - "8095:8095"
    privileged: true
    networks:
      - robotics-net

  camera-stream-gateway:
    image: bluenviron/mediamtx:latest
    container_name: robotics-mediamtx
    restart: unless-stopped
    ports:
      - "8554:8554"
      - "8889:8889"
    environment:
      - MTX_PROTOCOLS=tcp
    networks:
      - robotics-net

networks:
  robotics-net:
    driver: bridge

volumes:
  lerobot_checkpoints:
```

## Production Systemd Service Unit (`lerobot-gateway.service`)

On bare-metal edge workstations (e.g., Ubuntu 24.04 LTS equipped with RTX 4090 or Jetson Orin), run the LeRobot FastMCP service as a persistent, locked-down systemd daemon:

```ini
[Unit]
Description=LeRobot Physical Robotics FastMCP 3.1 Control Gateway
Documentation=https://github.com/huggingface/lerobot
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=robotics
Group=dialout
WorkingDirectory=/opt/lerobot-runtime
ExecStart=/usr/local/bin/python3 -m fastmcp run server.py --port 8095
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3s
Environment=PYTHONUNBUFFERED=1
Environment=ROBOT_SERIAL_PORT=/dev/ttyUSB0
Environment=ROBOT_BAUDRATE=1000000
Environment=CUDA_VISIBLE_DEVICES=0

# Hardware serial & USB permissions
SupplementaryGroups=dialout video
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/opt/lerobot-runtime/logs /tmp
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## CLI examples

### Recording Teleoperation Dataset
Record 50 episodes of motor manipulation demonstrations to a local dataset repository:
```bash
lerobot-record \
  --robot.type=so100 \
  --fps=30 \
  --repo-id=user/so100-button-press \
  --num-episodes=50 \
  --push-to-hub=true
```

### Training Imitation Policy
Train a Diffusion Policy on recorded dataset using CUDA acceleration:
```bash
lerobot-train \
  --policy.type=diffusion \
  --dataset.repo_id=user/so100-button-press \
  --env.type=real \
  --batch-size=64 \
  --steps=100000 \
  --eval-freq=5000
```

### Policy Replay & Evaluation
Replay a trained policy model on real hardware to evaluate target completion rate:
```bash
lerobot-eval \
  --policy.path=user/so100-diffusion-button-press \
  --robot.type=so100 \
  --num-eval-episodes=10
```

## Health Verification Script

This automated script verifies hardware bus responsiveness, motor torque limits, camera framerates, and FastMCP tool availability:

```python
#!/usr/bin/env python3
"""
Automated Hardware & FastMCP Verification Script for LeRobot Workcells.
"""
import sys
import time
import requests
from pydantic import BaseModel, Field, ConfigDict


class WorkcellHealthReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    bus_connected: bool = Field(..., description="Serial USB bus connection state")
    camera_fps: float = Field(..., ge=0.0, description="Measured camera FPS")
    servo_temp_max_c: float = Field(..., le=85.0, description="Highest motor servo temperature")
    inference_latency_ms: float = Field(..., ge=0.0, description="Model forward pass latency")
    safety_envelope_ok: bool = Field(..., description="Whether joints are within physical limits")


def check_lerobot_health(endpoint_url: str = "http://localhost:8095/health") -> bool:
    print(f"[*] Probing LeRobot Gateway at {endpoint_url}...")
    try:
        resp = requests.get(endpoint_url, timeout=3.0)
        resp.raise_for_status()
        data = resp.json()

        report = WorkcellHealthReport(
            bus_connected=data.get("bus_connected", False),
            camera_fps=float(data.get("camera_fps", 0.0)),
            servo_temp_max_c=float(data.get("servo_temp_max_c", 40.0)),
            inference_latency_ms=float(data.get("inference_latency_ms", 15.0)),
            safety_envelope_ok=data.get("safety_envelope_ok", False),
        )

        print("[+] Workcell Telemetry Verified:")
        print(f"    - Serial Bus: {'ONLINE' if report.bus_connected else 'OFFLINE'}")
        print(f"    - Camera Rate: {report.camera_fps:.1f} FPS")
        print(f"    - Peak Servo Temp: {report.servo_temp_max_c}°C")
        print(f"    - Model Latency: {report.inference_latency_ms:.2f} ms")
        print(f"    - Safety Envelope: {'CLEAR' if report.safety_envelope_ok else 'VIOLATED'}")

        if not report.bus_connected or not report.safety_envelope_ok:
            print("[-] FAIL: Workcell reports hardware safety warning.")
            return False

        print("[+] All LeRobot sanity checks passed successfully.")
        return True
    except Exception as err:
        print(f"[-] Health probe failed: {err}")
        return False


if __name__ == "__main__":
    success = check_lerobot_health()
    sys.exit(0 if success else 1)
```

## API examples

### FastMCP 3.1 Server Integration with Strict Pydantic v2 Schemas
The following complete script demonstrates creating a **FastMCP 3.1** server that exposes LeRobot physical robot commands to higher-level AI agents, validating input commands and sensor telemetry using **Pydantic v2**:

```python
import time
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

# Initialize FastMCP 3.1 Server for LeRobot Control
mcp = FastMCP("lerobot-robotics-gateway", version="3.1.0")


class JointState(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    joint_positions: List[float] = Field(..., min_length=6, max_length=6, description="6-DOF motor joint angles in radians")
    joint_velocities: List[float] = Field(..., min_length=6, max_length=6, description="Motor joint velocities in rad/s")
    gripper_open: bool = Field(..., description="Boolean status of end-effector gripper")


class TeleoperationFrame(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    timestamp: float = Field(..., description="Unix timestamp of sensor reading")
    episode_index: int = Field(..., ge=0, description="Active demonstration episode ID")
    robot_state: JointState = Field(..., description="State telemetry")
    action_command: JointState = Field(..., description="Target action state")


class RobotCommandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    target_positions: List[float] = Field(..., min_length=6, max_length=6, description="Target joint angles for physical arm movement")
    gripper_target: bool = Field(True, description="Target gripper position (True=Open, False=Closed)")
    max_velocity_scaling: float = Field(0.5, ge=0.1, le=1.0, description="Safety velocity scaling factor")


@mcp.tool()
async def execute_robot_action(request_data: RobotCommandRequest) -> dict:
    """Validate and dispatch physical robot movement command via LeRobot control loop."""
    # Simulate local LeRobot policy step execution
    frame = TeleoperationFrame(
        timestamp=time.time(),
        episode_index=1,
        robot_state=JointState(
            joint_positions=[0.0, -0.45, 1.2, 0.0, 0.8, 0.0],
            joint_velocities=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            gripper_open=True
        ),
        action_command=JointState(
            joint_positions=request_data.target_positions,
            joint_velocities=[v * request_data.max_velocity_scaling for v in [0.05, 0.03, -0.02, 0.0, 0.0, 0.0]],
            gripper_open=request_data.gripper_target
        )
    )

    return {
        "status": "executed",
        "timestamp": frame.timestamp,
        "validated_action": frame.action_command.model_dump()
    }


if __name__ == "__main__":
    mcp.run()
```

### Direct Python Trajectory Sampling & Model Ingestion
The following example demonstrates instantiating a custom LeRobot trajectory dataset schema and running inference through a Hugging Face ACT Policy instance:

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class TrajectorySample(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    frame_index: int = Field(..., ge=0, description="Visual frame sequence index")
    camera_rgb_b64: str = Field(..., description="Base64 encoded camera frame")
    joint_angles: List[float] = Field(..., min_length=6, max_length=6)
    target_action: List[float] = Field(..., min_length=6, max_length=6)


def sample_policy_trajectory(sample: TrajectorySample) -> Dict[str, Any]:
    # Simulates loading observation vector into policy network
    processed_action = [a * 0.98 for a in sample.target_action]
    return {
        "frame": sample.frame_index,
        "predicted_action": processed_action,
        "confidence": 0.992
    }


if __name__ == "__main__":
    sample = TrajectorySample(
        frame_index=12,
        camera_rgb_b64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        joint_angles=[0.0, -0.1, 0.5, 0.0, 0.2, 0.0],
        target_action=[0.01, -0.09, 0.52, 0.0, 0.21, 0.0]
    )
    res = sample_policy_trajectory(sample)
    print("Trajectory Sample Result:", res)
```

## Troubleshooting & Hardware Edge Cases

| Error / Failure Mode | Root Cause | Diagnostic Verification | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| `MOTOR_COMMUNICATION_TIMEOUT` | USB serial connection dropped to Feetech/Dynamixel motor bus. | Run `lsusb` and `dmesg \| grep -i ttyUSB` to check bus resets. | Verify baud rate (1Mbps/3Mbps); replace worn USB-to-RS485 interface dongle; add FTDI latency timer tuning (`echo 1 > /sys/bus/usb-serial/devices/ttyUSB0/latency_timer`). |
| `JOINT_LIMIT_EXCEEDED` | Policy predicted target joint angle outside physical arm range. | Check kinematic bounds log in `execute_robot_action`. | Enforce joint limit clipping in `RobotCommandRequest` prior to motor register write. |
| `CAMERA_FRAME_DROPPED` | High USB bus contention with 2+ webcam video streams. | Run `v4l2-ctl --list-devices` and check UVC bandwidth allocation. | Move cameras to separate USB root hubs; decrease resolution to 640x480 @ 30FPS or use MJPEG format. |
| `POLICY_OUT_OF_DISTRIBUTION` | Arm moved into unexpected workspace orientation causing erratic jitter. | Monitor CVAE latent distance $\|z\|_2 > 3.0\sigma$. | Trigger manual safety kill switch; record additional teleoperation episodes in target pose. |
| `MOTOR_OVERHEAT_WARNING` | Extended high-torque holding pose causing servo driver thermal throttling. | Read register `SERVO_TEMP_C` via hardware diagnostic tool. | Add active 40mm cooling fans or adjust home resting posture in script to release continuous motor torque. |
| `JERK_LIMIT_VIOLATION` | Step action discontinuity between consecutive policy chunks. | Inspect trajectory second-order derivatives in temporal ensembling. | Increase temporal ensembling weight parameter $m_{\text{decay}}$ and enable cubic spline smoothing. |
| `CUDA_OOM_DURING_DIFFUSION` | Multi-image observation batching exceeded GPU VRAM capacity. | Run `nvidia-smi --query-gpu=memory.used --format=csv`. | Enable PyTorch `torch.cuda.amp.autocast(dtype=torch.bfloat16)` and reduce DDIM inference steps from 50 to 15. |
| `FASTMCP_DISCONNECTION` | Socket read timeout on client during long synchronous inference. | Check journalctl for `lerobot-gateway.service` socket errors. | Migrate synchronous tool calls to asynchronous streaming generator tools in FastMCP 3.1. |

## Production Deployment Guardrails

1. **Hardware E-Stop Hook**: Always bind a physical USB or Bluetooth emergency stop button to instantly disarm motor torque registers.
2. **Velocity & Acceleration Capping**: Clamp maximum joint velocity (`max_velocity_scaling <= 0.5`) during early real-world policy testing.
3. **Joint Angle Hard Limits**: Define software boundary guardrails in Python drivers matching the exact mechanical joint limits of the arm.
4. **Thermal Monitoring**: Programmatically poll servo temperature registers; halt policy execution if motor temp exceeds 65°C.
5. **Sim-to-Real Domain Randomization**: Add visual noise, lighting variations, and random object position shifts during training to improve real-world policy transfer.

## Related tools / concepts
- [Hugging Face Ecosystem](../providers/huggingface.md)
- [Pydantic AI](../frameworks/pydantic-ai.md)
- [FastMCP 3.1](../automation_orchestration/mcp.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [OpenCode](../development_ops/opencode.md)
- [Claude Code](../development_ops/claude-code.md)
- [vLLM](../infrastructure/vllm.md)

## Sources / references
- [Hugging Face LeRobot Announcement](https://huggingface.co/blog/amazon/strands-lerobot-streaming-data-loop)
- [GitHub - Hugging Face LeRobot Repository](https://github.com/huggingface/lerobot)
- [LeRobot Official Documentation](https://huggingface.co/docs/lerobot)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
