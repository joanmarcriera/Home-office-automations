# OSWorld

## What it is
OSWorld is a scalable, real computer environment designed for benchmarking multimodal agents. It supports unified task setup, execution-based evaluation, and interactive reinforcement learning across desktop operating systems such as Ubuntu, Windows, and macOS. It is the premier environment for testing 'Computer Use' and OS-level control capabilities of frontier models.

## What problem it solves
Most agent benchmarks are constrained to isolated web sandboxes or mock APIs. OSWorld provides an interactive "OS-in-a-box" environment for assessing open-ended computer tasks that involve arbitrary desktop applications, native file I/O, terminal commands, and workflows spanning multiple programs. It evaluates an agent's ability to act as a 'Digital Twin' or fully autonomous desktop assistant, handling real-world OS noise.

## Where it fits in the stack
**Eval / Environment**. It provides the benchmarking tasks and virtualized runtime infrastructure (Docker, VMware, VirtualBox) required for executing and validating agentic computer control actions. It is a cornerstone of the evaluation layer for testing visual grounding and GUI navigation in VLMs like Claude 5.1, GPT-5.5, Gemini 4.0 Pro/Flash, Llama 4, Gemma 3, and Qwen 3.6.

## Typical use cases
- **Desktop Agent Evaluation**: Benchmarking autonomous agents interacting with native OS elements (e.g., system menus, file managers, desktop configurations).
- **Multi-App GUI Workflows**: Testing an agent's ability to orchestrate tasks across applications, such as copying data from a spreadsheet, querying a web browser, and generating a local markdown report.
- **Multimodal Visual Grounding**: Evaluating the ability of Vision-Language Models (VLMs) to translate pixel-level GUI screenshots into accurate click, drag, type, and scroll coordinates.
- **Computer Use Research**: Training and assessing agents (e.g., Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6) on raw keyboard and mouse control without custom tool-specific APIs.

## Strengths
- **Real OS Deployments**: Integrates with actual operating systems (Ubuntu, Windows, macOS) hosted inside secure virtual machines or containers.
- **Rich Task Suite**: Over 369 diverse tasks modeled after real-world professional workflows.
- **Execution-based State Verification**: Verifies success by running background scripts that inspect the final state of the file system or application registries rather than simple string-matching on logs.
- **Comprehensive GUI Event Tracking**: Captures drag-and-drop, right-clicks, keyboard shortcuts, and complex mouse maneuvers.

## Limitations
- **Heavy Infrastructure Demands**: Running full virtualization software (VMware/VirtualBox) requires significant local CPU, RAM, and disk resources.
- **High Setup Friction**: Initial VM image installation, snapshot configuration, and display server configuration can be complex.
- **Inference Latency**: Incorporating multimodal screenshots into the agent loop can create execution and billing overhead due to massive visual token usage.

## When to use it
- When developing or testing "Computer Use" agents or visual operating system controllers.
- When evaluating VLM grounding and coordinate-mapping capabilities on raw desktop interfaces.
- For academic or enterprise research in multimodal agentic planning, navigation, and self-correction.

## When not to use it
- For lightweight, non-visual agent benchmarking (use [GAIA](./gaia.md) or [AssistantBench](./assistant-bench.md) instead).
- If your development environment lacks the hardware resources to support multiple parallel VM instances.
- For testing pure text-based reasoning models that do not have visual processing (VLM) inputs.

## Getting started
OSWorld is run by cloning its repository, configuring the hypervisor backend (Docker, VMware, or VirtualBox), and loading the target OS virtual machine images.

### 1. Installation
Clone the repository and install the standard dependencies:
```bash
git clone https://github.com/xlang-ai/OSWorld
cd OSWorld
pip install -r requirements.txt
```

### 2. Configure VM/Container Backend
Ensure that Docker is running (for Ubuntu-only tasks) or that VMware/VirtualBox is configured on your host. Download the required virtual machine snapshots as instructed in the OSWorld documentation.

## CLI examples

### Executing a Single Task
Evaluate an agent on a specific Docker-based Ubuntu task using a frontier model:
```bash
python run_task.py \
    --task_id "ubuntu-123" \
    --model "anthropic/claude-5.1" \
    --env_type "docker"
```

### Running Benchmark Set
Execute a full evaluation suite against a defined configuration file using a GPT model:
```bash
python run_benchmark.py \
    --config configs/ubuntu_all.json \
    --model "openai/gpt-5.5"
```

### Recording Agent Trajectories
Instruct OSWorld to record video of the desktop interaction for auditability and step-by-step diagnostic review:
```bash
python run_task.py \
    --task_id "windows-456" \
    --record_video \
    --output_dir ./recordings/ \
    --model "meta-llama/llama-4-70b-instruct"
```

## API examples

### Programmatic Environment Setup
The following python snippet shows how to instantiate the OSWorld environment and step through agent actions programmatically:
```python
from osworld.env import OSWorldEnv

# Initialize the environment for a Docker-backed Ubuntu task
env = OSWorldEnv(os_type="ubuntu", backend="docker")

# Reset to load the initial task state and retrieve the screenshot observation
obs = env.reset(task_id="ubuntu-tasks-1")

# obs contains: {"screenshot": VLM_compatible_image, "instruction": str_task}
# action format is a serialized computer command, e.g., mouse_click(x, y)
action = "mouse_click(450, 300)"
obs, reward, done, info = env.step(action)
```

### State-Verification Script Structure
OSWorld executes target verification scripts inside the guest OS to determine task completion:
```python
def verify_task_completion():
    import os
    # Success condition: User must have downloaded the correct file and moved it
    target_path = "/home/user/Desktop/invoice_july_2026.csv"
    if os.path.exists(target_path):
        with open(target_path, "r") as f:
            if "total_due,4500.0" in f.read():
                return True
    return False
```

### Programmatic Agent Commands Validation
Validate OSWorld-compatible computer use keyboard and mouse actions using **Pydantic v2**:
```python
from pydantic import BaseModel, Field
from typing import Literal, Union

class MouseClickAction(BaseModel):
    action_type: Literal["click"] = "click"
    x: int = Field(..., ge=0, le=1920, description="X coordinate (pixel)")
    y: int = Field(..., ge=0, le=1080, description="Y coordinate (pixel)")

class KeyboardAction(BaseModel):
    action_type: Literal["type"] = "type"
    text: str = Field(..., min_length=1, description="String payload to input")

# Validate action payloads programmatically
click_event = MouseClickAction.model_validate({"action_type": "click", "x": 450, "y": 300})
print(f"Validated Click action: {click_event.action_type} at coordinates ({click_event.x}, {click_event.y})")
```

## Related tools / concepts
- [PA-bench](./pa-bench.md) — Web navigation benchmark.
- [GAIA](./gaia.md) — General AI assistant benchmark.
- [AssistantBench](./assistant-bench.md) — Multi-step web mission benchmark.
- [Claude Code](../development_ops/claude-code.md) — Agentic CLI for development.
- [OpenHands](../development_ops/openhands.md) — Agentic software engineering platform.
- [Terminal-Bench](./terminal-bench.md) — Evaluating direct shell interactions.
- [Inspect AI](./inspect-ai.md) — Framework for running agentic evaluations.
- [Open WebUI Computer](../automation_orchestration/open-webui-computer.md) — Open workstation interface.
- [Browser Use](../automation_orchestration/browser-use.md) — Library for web interaction.
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Foundational protocol for agent tool use.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: The benchmark code is completely free. Executing visual GUI agents over multiple tasks requires significant local computing hardware and substantial multimodal LLM API token costs.

## Sources / references
- [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks (ArXiv)](https://arxiv.org/abs/2404.07972)
- [OSWorld Project Website](https://os-world.github.io/)
- [OSWorld GitHub Repository](https://github.com/xlang-ai/OSWorld)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
