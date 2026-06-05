# OSWorld

## What it is
OSWorld is a scalable, real computer environment for benchmarking multimodal agents. It supports task setup, execution-based evaluation, and interactive learning across operating systems like Ubuntu, Windows, and macOS.

## What problem it solves
Most agent benchmarks are limited to the web or specific applications. OSWorld provides a unified environment for assessing open-ended computer tasks that involve arbitrary desktop applications, file I/O, and workflows spanning multiple apps.

## Where it fits in the stack
**Eval / Environment**. It provides both the benchmarking tasks and the interactive "OS-in-a-box" infrastructure for agent testing.

## Typical use cases
- **Desktop Agent Evaluation**: Testing agents that interact with native OS elements (menus, file explorers, desktop apps).
- **Multi-app Workflows**: Evaluating tasks that require moving data between a spreadsheet, a browser, and a local text editor.
- **VLM Grounding**: Benchmarking the visual grounding capabilities of Vision-Language Models (VLMs) on complex GUIs.

## Strengths
- **Real OS Environments**: Uses VMware, VirtualBox, or Docker to host actual operating systems.
- **Diverse Tasks**: 369 tasks derived from real-world computer use cases.
- **Execution-based Evaluation**: Uses custom scripts to verify the final state of the OS (e.g., "is the file saved in the correct directory?").
- **Multi-OS**: Not limited to just Linux; includes Windows and macOS support.

## Limitations
- **Heavy Infrastructure**: Requires virtualization software and significant local/cloud resources to run VM instances.
- **Setup Complexity**: Initial environment configuration can be challenging.

## When to use it
- When developing "Computer Use" agents (like Claude Computer Use or Open Operator).
- When you need to test an agent's ability to handle OS-level interactions and native apps.

## When not to use it
- For lightweight testing of pure web agents (use WebArena or AssistantBench).
- If you lack the hardware resources to run virtual machines.

## Getting started
OSWorld is typically run by cloning the repository and setting up a virtual machine environment.

### 1. Installation
```bash
git clone https://github.com/xlang-ai/OSWorld
cd OSWorld
pip install -r requirements.txt
```

### 2. Environment Setup
OSWorld supports VMware, VirtualBox, and Docker. Refer to the [official documentation](https://os-world.github.io/) for OS image setup.

## Related tools / concepts
- [PA-bench](./pa-bench.md)
- [GAIA](./gaia.md)
- [AssistantBench](./assistant-bench.md)
- [Claude Code](../development_ops/claude-code.md)
- [OpenHands](../development_ops/openhands.md)

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free, but requires significant compute/storage for VMs.

## Sources / References
- [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks (ArXiv)](https://arxiv.org/abs/2404.07972)
- [OSWorld Project Website](https://os-world.github.io/)
- [OSWorld GitHub Repository](https://github.com/xlang-ai/OSWorld)

## Contribution Metadata

- Last reviewed: 2026-06-05
- Confidence: high
