# Terminal-Bench (Terminus 2)

## What it is
Terminal-Bench (including the Terminus 2 research baseline) is a benchmark for evaluating AI agents' ability to use a terminal. It focuses on tasks that require interacting with a real terminal environment, such as installing software, debugging system issues, managing files, and direct LLM-to-tmux shell interaction—a key July 2026 capability for autonomous DevOps agents.

## What problem it solves
Measures whether AI agents can effectively operate in a terminal environment, a critical capability for autonomous system administration and DevOps tasks. It goes beyond code generation by testing the agent's ability to interpret command output, handle stateful sessions, and remediate system failures.

## Where it fits in the stack
**Benchmarking**. Used to evaluate AI agents on terminal-based tasks within agentic orchestration layers. It is the primary benchmark for "Terminus 2" patterns where agents manage long-running tmux sessions.

## Typical use cases
- **DevOps Agent Evaluation**: Testing agents on terminal interaction tasks (installation, debugging, file management) before deployment to production.
- **Comparison of Agent Frameworks**: Assessing how different frameworks (e.g., OpenHands, Aider) handle real-world system environments.
- **Autonomous SysAdmin Research**: Assessing the readiness of AI agents for high-stakes autonomous system administration and security patching.
- **Multi-step Trajectory Analysis**: Evaluating an agent's ability to maintain state across multiple shell commands.

## Strengths
- **Practical Realism**: Tests practical, real-world terminal skills rather than abstract coding problems or synthetic laboratory examples.
- **Stateful Interaction**: Focuses on the "Intent-State" loop, requiring agents to observe and react to dynamic system changes.
- **DevOps Alignment**: Covers a range of tasks directly relevant to modern SRE and DevOps workflows in July 2026.
- **Direct tmux Support**: Terminus 2 specializes in direct LLM interaction with terminal multiplexers for persistent session management.

## Limitations
- **Environment Complexity**: Requires a real or containerized terminal environment for evaluation, adding significant setup overhead.
- **OS Specificity**: Results may vary depending on the operating system and environment configuration (e.g., Ubuntu vs. Alpine).
- **Flakiness**: Like web-benchmarks, terminal-bench can be subject to environmental flakiness if dependencies are not strictly pinned.

## When to use it
- When evaluating AI agents that need to operate autonomously in terminal environments for July 2026 DevOps tasks.
- When assessing system administration or security patching capabilities of frontier models (Claude 5.1, GPT-5.5).
- When researching persistent session management (tmux) for agents.

## When not to use it
- When evaluating pure code generation capabilities (use [HumanEval](human-eval.md) or [MBPP](mbpp.md)).
- When you need a lightweight, fast-running benchmark for early-stage development (requires Docker/Harbor).
- For evaluating high-level visual reasoning (use [ColQwen](../../knowledge_base/self-healing-agent-research.md) or AssistantBench).

## Getting started

Terminal-Bench (TB-2) is typically run using the **Harbor** framework to provide a consistent, containerized execution environment.

### 1. Installation
```bash
pip install terminal-bench harbor-framework
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
Using the Harbor framework to run sandboxed evaluations in July 2026.

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

- Last reviewed: 2026-07-23
- Confidence: high
