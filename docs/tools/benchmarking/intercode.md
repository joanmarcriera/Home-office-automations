# InterCode

## What it is
InterCode is an interactive benchmarking framework designed for evaluating Large Language Models (LLMs) in real-world programming and shell environments. It focuses on multi-turn interactions where the model can execute code or commands and receive feedback from the environment. In July 2026, it serves as a foundational environment for testing **MCP 3.0 Task Protocol** compliance in autonomous coding agents.

## What problem it solves
Standard static benchmarks often fail to capture the interactive nature of software development. InterCode addresses this by providing an environment where models must reason over multiple steps, handle errors, and adapt based on actual execution results. It tests the "plan-execute-verify" loop essential for self-healing agents and advanced coding assistants like **GPT-5.5** and **Claude 4.8 Opus**.

## Where it fits in the stack
**Benchmarking / Agentic Evaluation**. It sits in the "agentic" evaluation space, testing the model's ability to act as a coding assistant or terminal agent. It is a critical validation layer for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) ecosystem and autonomous platforms like [Devin](../development_ops/devin.md) and [OpenHands](../development_ops/openhands.md).

## Typical use cases
- **Evaluating Terminal Agents**: Measuring how well models handle multi-step Bash/Shell tasks in a sandboxed environment.
- **SQL Generation Benchmarking**: Testing SQL generation and execution capabilities against live databases.
- **MCP 3.0 Protocol Validation**: Ensuring agents correctly use standardized tool-calling patterns to complete interactive tasks.
- **Iterative Debugging**: Benchmarking models on tasks that require multiple rounds of execution and log analysis to solve.

## Strengths
- **Interactivity**: Models can "try and fail," mirroring human developer workflows and allowing for self-correction.
- **Environment Fidelity**: Uses actual [Docker](../infrastructure/docker.md) containers for safe, reproducible, and realistic execution environments.
- **Multi-domain Support**: Benchmarks across Bash, SQL, Python, and web-based interaction layers.
- **Standardized API**: Provides a Gym-like interface for easy integration with reinforcement learning and automated evaluation pipelines like [JudgeGPT](judgegpt.md).

## Limitations
- **Complexity**: Harder to set up and maintain than static, text-only benchmarks.
- **Resource Intensive**: Requires significant compute to run multiple containers for evaluation.
- **State Leakage**: Ensuring a completely clean environment between turns can be challenging in complex multi-step tasks.

## When to use it
- When developing coding agents or terminal-based AI assistants that need to interact with a system.
- When you need to measure how well a model handles and recovers from real-world execution errors.
- For evaluating [MCP](../automation_orchestration/mcp.md) tool-calling performance in a realistic feedback loop.

## When not to use it
- For quick, "shallow" evaluations of general model intelligence (use [MMLU](mmlu.md) or [ARC](arc.md) instead).
- When you don't have the infrastructure or permissions to run Docker-based evaluations safely.

## Getting started

### Installation
InterCode requires [Docker](../infrastructure/docker.md) and Python 3.10+.

```bash
git clone https://github.com/princeton-nlp/intercode
cd intercode
pip install -r requirements.txt
```

### Running an Evaluation with MCP 3.0
1. Ensure the Docker daemon is running.
2. Initialize an InterCode environment with an MCP-compliant agent.
3. Execute a task using the standardized Task Protocol.

## CLI examples

### Bash Environment Evaluation
```bash
python -m intercode.run --env bash --data data/bash/sample.json
```

### SQL Environment Evaluation
```bash
python -m intercode.run --env sql --data data/sql/sample.json
```

## API examples

### Environment Interaction Loop (Python)
A typical interaction involves the agent receiving an observation and issuing a command.

```python
import gym
import intercode

# Initialize the Bash environment
env = gym.make('intercode-bash-v0')
observation = env.reset()

# Agent issues a command (e.g., from GPT-5.5)
action = "ls -la"
observation, reward, done, info = env.step(action)

print(f"Shell Output: {observation}")
```

### MCP 3.0 Task Integration
```python
from intercode.mcp import InterCodeMCPServer

# Expose InterCode environment as an MCP 3.0 tool server
server = InterCodeMCPServer(env_type="bash")
server.run()
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) — for evaluating models on real-world GitHub issues.
- [BigCodeBench](bigcodebench.md) — benchmark for instruction-following coding tasks.
- [JudgeGPT](judgegpt.md) — for automated qualitative evaluation of agent traces.
- [Promptfoo](promptfoo.md) — for test-driven prompt engineering.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — standard for agent-tool communication.
- [Devin](../development_ops/devin.md) — autonomous software engineering agent.
- [OpenHands](../development_ops/openhands.md) — open-source autonomous agent platform.
- [Docker](../infrastructure/docker.md) — the standard for isolated execution environments.

## Sources / references
- [GitHub Repository](https://github.com/princeton-nlp/intercode)
- [Research Paper: InterCode (arXiv:2306.14898)](https://arxiv.org/abs/2306.14898)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/docs/concepts/tasks)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
