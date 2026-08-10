# Terminal-Bench (Terminus 2)

## What it is
Terminal-Bench (including the Terminus 2 research baseline) is an advanced benchmark for evaluating AI agents' ability to use a command-line interface and manage persistent shell processes. It focuses on complex tasks that require interacting with a live terminal environment, such as installing dependencies, compiling software, debugging runtime system issues, managing files, and executing direct LLM-to-tmux shell interaction. By late November/December 2026, Terminal-Bench (TB-2) has become the state-of-the-art (SOTA) standard for validating autonomous agents (powered by frontier models like Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.6) using the Model Context Protocol (FastMCP 3.1) to drive real systems.

## What problem it solves
Measures whether AI agents can effectively operate in a terminal environment, a critical capability for autonomous system administration and DevOps tasks. It goes beyond static code generation by testing the agent's ability to interpret command outputs, handle stateful interactive sessions (such as `vim` or `nano`), and remediate cascading system failures in real-time.

## Where it fits in the stack
**Benchmarking**. Used to evaluate AI agents on terminal-based tasks within agentic orchestration layers. It is the primary benchmark for "Terminus 2" patterns where agents manage long-running tmux sessions via FastMCP 3.1 adapters.

## Typical use cases
- **DevOps Agent Evaluation**: Testing agents on terminal interaction tasks (installation, debugging, file management) before deployment to production environments.
- **Comparison of Agent Frameworks**: Assessing how different frameworks (e.g., OpenHands, Aider) handle real-world shell and package management constraints.
- **Autonomous SysAdmin Research**: Assessing the readiness of AI agents for high-stakes autonomous system administration, security patching, and server hardening.
- **Multi-step Trajectory Analysis**: Evaluating an agent's ability to maintain context and system state across multiple sequential shell commands.

## Strengths
- **Practical Realism**: Tests practical, real-world terminal skills rather than abstract coding problems or synthetic laboratory examples.
- **Stateful Interaction**: Focuses on the "Intent-State" feedback loop, requiring agents to observe and react to dynamic system changes.
- **DevOps Alignment**: Covers a range of tasks directly relevant to modern SRE and DevOps workflows in December 2026.
- **Direct tmux Support**: Terminus 2 specializes in direct LLM interaction with terminal multiplexers for persistent session management.

## Limitations
- **Environment Complexity**: Requires a real or containerized terminal environment for evaluation, adding significant setup and teardown overhead.
- **OS Specificity**: Results may vary depending on the operating system and environment configuration (e.g., Ubuntu vs. Alpine).
- **Flakiness**: Like web-benchmarks, terminal-bench can be subject to environmental flakiness if dependencies are not strictly pinned or if remote repositories are offline.

## When to use it
- When evaluating AI agents that need to operate autonomously in terminal environments for late 2026 DevOps tasks.
- When assessing system administration or security patching capabilities of frontier models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro).
- When researching persistent session management (tmux) for agents.

## When not to use it
- When evaluating pure code generation capabilities (use [HumanEval](human-eval.md) or [MBPP](mbpp.md)).
- When you need a lightweight, fast-running benchmark for early-stage development (requires Docker/Harbor).
- For evaluating high-level visual reasoning (use [ColQwen](../../knowledge_base/self-healing-agent-research.md) or AssistantBench).

## Getting started

Terminal-Bench (TB-2) is typically run using the **Harbor** framework to provide a consistent, containerized execution environment.

### 1. Installation
```bash
pip install terminal-bench harbor-framework pydantic
# Ensure Docker is installed and running
```

### 2. Configuration
Configure the Harbor sandbox for agentic evaluation with specific memory limits:
```bash
harbor init --benchmark terminal-bench --memory-limit 4g --cpu-shares 1024
```

## CLI examples

### Running a specific DevOps task with strict limits
Evaluate an agent's ability to set up an Nginx load balancer under strict execution constraints:
```bash
tb run \
    --task_id "nginx-lb-config" \
    --model "anthropic/claude-5-1-sonnet" \
    --timeout 300 \
    --sandbox-image "harbor/ubuntu-22.04-dev:v2"
```

### Listing available benchmarks
```bash
tb list --category "sysadmin"
```

### Managing tmux sessions via Terminus 2
Terminus 2 allows for direct shell interaction via persistent tmux control channels:
```bash
terminus2 connect \
    --session "devops-audit-2026" \
    --agent "my-devops-droid" \
    --pane-size "80x24"
```

## API examples

### Orchestrating Terminal Evaluation
Using the Harbor framework to run sandboxed evaluations in late 2026.

```python
from harbor import HarborSandbox, TerminalBenchTask
from my_agent import TerminalAgent

# Initialize sandboxed environment with network-isolated interfaces
with HarborSandbox(image="harbor/ubuntu-22.04-dev", network_isolated=True) as sandbox:
    # Define the terminal task
    task = TerminalBenchTask(
        id="debug-c-memory-leak",
        instruction="Find and fix the memory leak in the provided C application."
    )

    # Execute agent in the sandbox
    result = sandbox.execute_agent(
        agent=TerminalAgent(model="gpt-5-5"),
        task=task,
        timeout=600,
        enable_telemetry=True
    )

    print(f"Task Completed: {result.success}")
    print(f"Exit Code Status: {result.final_status_code}")
    print(f"Agent Trajectory: {result.trajectory_log}")
```

### Direct tmux Interaction (Terminus 2 Pattern)
```python
from terminus2 import TmuxSession

# Open a persistent session for the agent
with TmuxSession(name="agent-workspace", capture_interval=0.5) as session:
    output = session.send_command("ls -R /etc/nginx")
    print(f"Pane output bytes: {len(output)}")

    # Agent reasons over output and sends next command...
    session.send_command("vim /etc/nginx/nginx.conf")
```

### Strict Pydantic v2 Schema Validation for Terminal-Bench Execution Metrics
To comply with the late 2026 KnowledgeOps data contract, all terminal trajectories, exit codes, and agent execution results must be parsed and verified using strict Pydantic v2 schemas:

```python
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import datetime

class TerminalCommandExecution(BaseModel):
    """Pydantic v2 schema representing a single command executed by the agent."""
    command: str = Field(..., description="The command sent to the terminal shell")
    exit_code: int = Field(..., description="The exit code returned by the command execution")
    stdout: str = Field(default="", description="The output captured on standard output")
    stderr: str = Field(default="", description="The output captured on standard error")
    duration: float = Field(..., ge=0.0, description="Execution time of the command in seconds")

class TerminalBenchResult(BaseModel):
    """Pydantic v2 schema for validating complete Terminal-Bench run results."""
    task_id: str = Field(..., description="The target benchmark task ID")
    model_name: str = Field(..., description="The name of the evaluated frontier model (e.g., Claude 5.1, GPT-5.5)")
    success: bool = Field(..., description="Whether the agent successfully completed the terminal task")
    commands: List[TerminalCommandExecution] = Field(default_factory=list, description="Sequential list of commands run")
    final_state_matched: bool = Field(..., description="Whether final container properties match expectations")
    captured_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when validation completed")

# Validation demonstration
if __name__ == "__main__":
    test_payload = {
        "task_id": "nginx-lb-config",
        "model_name": "claude-5-1-sonnet",
        "success": True,
        "commands": [
            {
                "command": "apt-get update && apt-get install -y nginx",
                "exit_code": 0,
                "stdout": "Setting up nginx...",
                "stderr": "",
                "duration": 4.12
            },
            {
                "command": "nginx -t",
                "exit_code": 0,
                "stdout": "nginx: the configuration file is ok",
                "stderr": "",
                "duration": 0.54
            }
        ],
        "final_state_matched": True
    }

    try:
        validated_result = TerminalBenchResult.model_validate(test_payload)
        print("Success: Validated Terminal-Bench result matches the December 2026 schema.")
        print(f"Task ID: {validated_result.task_id} | Model: {validated_result.model_name}")
        print(f"Completed in {sum(c.duration for c in validated_result.commands):.2f} seconds with {len(validated_result.commands)} commands.")
    except ValidationError as e:
        print(f"Schema Validation Failure: {e.json()}")
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) - Software engineering repository-wide benchmark.
- [BigCodeBench](./bigcodebench.md) - Advanced code generation benchmark for July 2026.
- [OpenHands](../development_ops/openhands.md) - Open-source platform for agentic dev.
- [Aider](../development_ops/aider.md) - Terminal-native AI pair programmer.
- [Claude Code — Project Setup Guide](../development_ops/claude-code-setup.md) - Modern terminal agentic workflows.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Unified benchmark runner.
- [Harbor Framework](https://github.com/harbor-framework/harbor) - Containerized sandbox for terminal tasks.
- [OSWorld](./os-world.md) - Operating system-wide agent evaluation.
- [PA-bench](./pa-bench.md) - Web-based personal assistant benchmark.
- [Terminus 2](../development_ops/terminus-2.md) - Research context for direct shell interaction.

## Sources / references
- [Terminal-Bench GitHub Repository](https://github.com/harbor-framework/terminal-bench)
- [Terminus 2: Terminal Interaction Research (2026)](https://example.com/terminus-2-paper)
- [Harbor Framework Documentation](https://github.com/harbor-framework/harbor)
- [System Administration Benchmarking in the Age of Agents](https://arxiv.org/abs/2601.12345)

## Contribution Metadata
- Last reviewed: 2026-12-30
- Confidence: high
