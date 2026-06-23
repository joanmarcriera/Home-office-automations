# OSWorld

## What it is
OSWorld is a scalable, real computer environment for benchmarking multimodal agents. It supports task setup, execution-based evaluation, and interactive learning across operating systems like Ubuntu, Windows, and macOS. In June 2026, it is the primary environment for testing 'Computer Use' capabilities of frontier models like Claude 4.8 and GPT-5.5.

## What problem it solves
Most agent benchmarks are limited to the web or specific applications. OSWorld provides a unified environment for assessing open-ended computer tasks that involve arbitrary desktop applications, file I/O, and workflows spanning multiple apps. It evaluates an agent's ability to act as a 'Digital Twin' or 'Desktop Assistant'.

## Where it fits in the stack
**Eval / Environment**. It provides both the benchmarking tasks and the interactive "OS-in-a-box" infrastructure for agent testing. It is a key component of the 'Agentic Workbench' testing pipeline.

## Typical use cases
- **Desktop Agent Evaluation**: Testing agents that interact with native OS elements (menus, file explorers, desktop apps).
- **Multi-app Workflows**: Evaluating tasks that require moving data between a spreadsheet, a browser, and a local text editor.
- **VLM Grounding**: Benchmarking the visual grounding capabilities of Vision-Language Models (VLMs) on complex GUIs.
- **Computer Use Research**: Developing new architectures for direct OS interaction without specialized APIs.

## Strengths
- **Real OS Environments**: Uses VMware, VirtualBox, or Docker to host actual operating systems.
- **Diverse Tasks**: 369+ tasks derived from real-world computer use cases.
- **Execution-based Evaluation**: Uses custom scripts to verify the final state of the OS (e.g., "is the file saved in the correct directory?").
- **Multi-OS**: Includes support for Ubuntu, Windows, and macOS.
- **High Fidelity**: Captures the complexity of real desktop interactions (drag-and-drop, right-clicks, window management).

## Limitations
- **Heavy Infrastructure**: Requires virtualization software and significant local/cloud resources to run VM instances.
- **Setup Complexity**: Initial environment configuration and VM image management can be challenging.
- **Latency**: Virtualization overhead can introduce latency in agent feedback loops.

## When to use it
- When developing "Computer Use" agents (like Claude Computer Use or Open Operator).
- When you need to test an agent's ability to handle OS-level interactions and native apps.
- For research into multimodal agentic planning in complex, stateful environments.

## When not to use it
- For lightweight testing of pure web agents (use WebArena or AssistantBench).
- If you lack the hardware resources to run virtual machines.
- For testing pure text-based reasoning without visual/GUI components.

## Getting started
OSWorld is typically run by cloning the repository and setting up a virtual machine environment.

### 1. Installation
```bash
git clone https://github.com/xlang-ai/OSWorld
cd OSWorld
pip install -r requirements.txt
```

### 2. Environment Setup
OSWorld supports VMware, VirtualBox, and Docker. Refer to the [official documentation](https://os-world.github.io/) for OS image setup. Ensure you have the required VMX or OVA files for the target OS.

## CLI examples

### Run a Specific Task
Evaluate an agent on a single OSWorld task:
```bash
python run_task.py --task_id "ubuntu-123" --model "anthropic/claude-4.8" --env_type "docker"
```

### Batch Evaluation
Run evaluation across a set of tasks:
```bash
python run_benchmark.py --config configs/ubuntu_all.json --model "openai/gpt-5.5"
```

### Recording Trajectories
Enable video recording of the agent's interaction for later review:
```bash
python run_task.py --task_id "windows-456" --record_video --output_dir ./recordings
```

## API examples

### Programmatic Environment Interaction
```python
from osworld.env import OSWorldEnv

# Initialize the environment
env = OSWorldEnv(os_type="ubuntu", backend="docker")

# Reset to a specific task state
obs = env.reset(task_id="ubuntu-tasks-1")

# Agent interaction loop (conceptual)
action = agent.get_action(obs)
obs, reward, done, info = env.step(action)
```

### Verification Script Example
OSWorld uses Python scripts to verify task completion:
```python
def verify_task_completion():
    import os
    # Check if the expected file exists and has correct content
    if os.path.exists("/home/user/report.pdf"):
        return True
    return False
```

## Related tools / concepts
- [PA-bench](./pa-bench.md) — Web navigation benchmark.
- [GAIA](./gaia.md) — General AI assistant benchmark.
- [AssistantBench](./assistant-bench.md) — Multi-step web mission benchmark.
- [Claude Code](../development_ops/claude-code.md) — Agentic CLI for development.
- [OpenHands](../development_ops/openhands.md) — Agentic software engineering platform.
- [Terminal-Bench](./terminal-bench.md) — Benchmarking direct shell interactions.
- [Claude Computer Use](../../knowledge_base/capabilities/claude-computer-use.md) — The foundational capability OSWorld measures.
- [Inspect AI](./inspect-ai.md) — Framework for running agentic evaluations.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free, but requires significant compute/storage for VMs. LLM API costs for multimodal vision can be high.

## Sources / References
- [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks (ArXiv)](https://arxiv.org/abs/2404.07972)
- [OSWorld Project Website](https://os-world.github.io/)
- [OSWorld GitHub Repository](https://github.com/xlang-ai/OSWorld)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
