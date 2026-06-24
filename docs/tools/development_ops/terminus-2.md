# Terminus 2 (Terminal-Bench)

## What it is
Terminus 2 is a lightweight, terminal-native AI agent and research baseline developed by the Terminal-Bench team. As of June 2026, it represents the standard for 'raw' agentic interaction with the shell, eschewing heavy orchestration layers in favor of a direct LLM-to-tmux bridge. It is widely used for evaluating the CLI capabilities of frontier models like Claude 4.8 and GPT-5.5.

## What problem it solves
It addresses the 'abstraction tax' in agentic software. While many agents use complex tool-calling protocols or virtualized file systems, Terminus 2 gives the model direct control over a standard tmux session. This allows for native handling of long-running processes, real-time terminal feedback, and authentic shell error recovery, making it an ideal tool for benchmarking 'pure' CLI reasoning.

## Where it fits in the stack
**Benchmark / Interface Layer**. Terminus 2 sits between the model's reasoning engine and the operating system's shell. It is frequently used in the 'Agentic Workbench' pattern as a minimal interface for performing system-level tasks without the overhead of a full IDE.

## Typical use cases
- **CLI-Agent Benchmarking**: Serving as the reference implementation for the 'Terminal-Bench' suite to measure model performance in raw shell environments.
- **System Administration Automation**: Executing complex multi-step shell tasks (e.g., database migrations, server hardening) via natural language.
- **Observability and Debugging**: Attaching to a tmux session to watch an agent's reasoning and execution in real-time.
- **Minimalist Toolchain Research**: Exploring the limits of agentic capability when restricted to standard Unix tools and basic session management.

## Strengths
- **Low Overhead**: Extremely lightweight compared to comprehensive agents like OpenHands or Devin.
- **Transparency**: Uses standard tmux sessions, allowing humans to 'attach' and interact with the agent's workspace seamlessly.
- **Resilience**: The model sees exactly what a human sees, including stderr, interactive prompts, and terminal color codes.
- **State-of-the-Art (SOTA) Baseline**: Consistently ranks at the top of terminal-centric benchmarks for reasoning accuracy and command efficiency.

## Limitations
- **Terminal Only**: Lacks built-in support for GUI interactions, web browsing, or native IDE features like LSP.
- **Context Management**: Relies heavily on the LLM's ability to maintain the terminal state within its context window, which can degrade during extremely long sessions.
- **Environment Sensitivity**: Requires a stable tmux and Unix-like environment; performance can vary based on the specific shell configuration.

## When to use it
- When you need a 'pure' terminal agent for system automation or research.
- For benchmarking the CLI capabilities of a new LLM version or fine-tuned model.
- When transparency and the ability to manually intervene in a terminal session are critical.

## When not to use it
- For high-level software engineering tasks that require deep IDE integration (use [Windsurf](./codeium.md) or [Cursor](./cursor.md)).
- If you require an agent with native web browsing or multi-modal tool-use capabilities.
- For users who are uncomfortable with tmux or command-line-first workflows.

## Getting started

### Installation
Terminus 2 requires Python 3.10+ and a functional tmux installation.
```bash
# Clone the Terminal-Bench repository
git clone https://github.com/pro-puffin/terminal-bench.git
cd terminal-bench

# Install core dependencies
pip install -r requirements.txt

# Ensure tmux is available
sudo apt install tmux
```

### Basic Usage
Start an agentic session by defining a task:
```bash
python -m terminal_bench.agents.terminus2 --task "Locate all .log files in /var/log/nginx, find errors from the last 24h, and summarize the top 3 IPs."
```

## CLI examples

### Attaching to the Agent Session
One of Terminus 2's key features is the ability to 'peek' into the agent's mind via tmux:
```bash
# List active agent sessions
tmux ls

# Attach to see the agent's work-in-progress
tmux attach -t terminus_agent_01
```

### Headless Evaluation
Run a suite of benchmarks from the Terminal-Bench library:
```bash
python -m terminal_bench.evaluator --agent terminus2 --suite "system_admin_v2"
```

## API examples

### Custom Prompting Interface
Terminus 2 allows for easy modification of its 'Inner Monologue' and system instructions:
```python
# agents/terminus2/config.py
# Customize the system prompt to favor specific tools (e.g., ripgrep over grep)
SYSTEM_PROMPT = """
You are a terminal-native AI agent.
You have direct access to a tmux session.
Prioritize 'rg' and 'fd' for search tasks.
"""
```

### Integration with AG2 (AgentOS)
Terminus 2 can be wrapped as a 'Terminal Tool' within a larger AG2 orchestration:
```python
from ag2 import Agent
from terminal_bench.agents import TerminusTool

# Define an agent that uses Terminus 2 for shell execution
sysadmin_agent = Agent(
    name="SysAdmin",
    tools=[TerminusTool(session_name="maintenance_v1")]
)
```

## Related tools / concepts
- [OpenHands](openhands.md)
- [Devin](devin.md)
- [Codeium](./codeium.md)
- [Aider](./aider.md)
- [Goose](../agents/goose.md)
- [AG2](../frameworks/ag2.md)
- [Model Context Protocol (MCP 3.0)](../automation_orchestration/mcp.md)
- [tmux (Terminal Multiplexer)](https://github.com/tmux/tmux)
- [Agentic Benchmarking](../../knowledge_base/patterns/agent-benchmarking.md)

## Sources / references
- [Terminal-Bench GitHub Repository](https://github.com/pro-puffin/terminal-bench)
- [Research Paper: Terminal-Bench - Evaluative Frontiers for CLI Agents](https://arxiv.org/abs/2501.00000)
- [Blog: The Rise of Terminal-Native Agents (June 2026)](https://mariozechner.at/posts/2026-06-15-terminus2-update/)

## Contribution Metadata

- Last reviewed: 2026-06-22
- Confidence: high
