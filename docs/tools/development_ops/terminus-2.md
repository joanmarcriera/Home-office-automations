# Terminus 2 (Terminal-Bench)

## What it is
Terminus 2 is a minimal, terminal-native AI agent designed by the Terminal-Bench team. Unlike complex agents with multi-step reasoning engines or GUI-bound tools, Terminus 2 takes a "raw" approach by giving the LLM direct access to a tmux session. The model sends commands as text and parses the terminal output itself, acting as a direct interface between the model's reasoning and the shell.

## What problem it solves
It demonstrates that a simple, direct approach to terminal-based AI agents (LLM + tmux) can achieve strong performance on complex tasks without the overhead of heavy orchestration layers. It serves as a baseline and a research tool for evaluating how well models can manage terminal state, handle long-running processes, and recover from shell errors.

## Where it fits in the stack
**Development & Ops**. It is a specialized, terminal-centric agent that sits at the intersection of developer productivity and autonomous systems research.

## Typical use cases
- **Terminal Task Automation**: Automating repetitive shell tasks, migrations, or server configuration via natural language.
- **Agentic Benchmarking**: Used as a baseline in the "Terminal-Bench" suite to evaluate LLM capability in a CLI environment.
- **Minimalist Agent Research**: Exploring the limits of simple agent architectures that use tmux for session management.

## Strengths
- **Minimalist Architecture**: Low overhead; easier to understand and debug than multi-layered agents.
- **High Portability**: Works anywhere tmux and Python can run.
- **Direct Feedback Loop**: The model "sees" the raw terminal output exactly as a human would in a tmux window.
- **Benchmark Leader**: Performs remarkably well on terminal tasks compared to more complex competitors.

## Limitations
- **Minimal Tooling**: Lacks advanced features like built-in file editors or complex GUI interaction.
- **State Management**: Relies heavily on the LLM's ability to keep track of the terminal state within its context window.
- **tmux Dependency**: Requires a functional tmux environment, which may be a barrier for some users.

## When to use it
- When you need a lightweight agent to perform shell-based tasks without a full IDE integration.
- When conducting research on agent performance in CLI environments.
- For users who prefer a "raw" terminal experience but want AI assistance.

## When not to use it
- When you need a full-featured AI coding agent with LSP integration and IDE features (e.g., Cursor or VS Code).
- For users unfamiliar with tmux or shell-based workflows.

## Getting started

### Installation
Terminus 2 typically requires a Python environment and tmux.
```bash
# Clone the Terminal-Bench repository
git clone https://github.com/pro-puffin/terminal-bench.git
cd terminal-bench

# Install dependencies
pip install -r requirements.txt

# Ensure tmux is installed on your system
sudo apt install tmux
```

### Basic usage
You can run Terminus 2 by pointing it to a specific task or prompt:
```bash
python -m terminal_bench.agents.terminus2 --task "Find all large log files in /var/log and compress them."
```

## Technical Examples

### tmux Session Inspection
Because Terminus 2 uses tmux, you can attach to the session and watch the agent work in real-time:
```bash
# List tmux sessions
tmux ls

# Attach to the session used by Terminus (usually named or indexed)
tmux attach -t <session_id>
```

### Custom Prompting Pattern
Terminus 2 uses a specific system prompt to guide the LLM's terminal interactions. You can modify this in `agents/terminus2/prompts.py` to add project-specific constraints or tools.

## Related tools / concepts
- [OpenHands](openhands.md)
- [Devin](devin.md)
- [Codeium](codeium.md)
- [Claude Code — Project Setup Guide](claude-code-setup.md)
- [OpenCode (Oh My OpenCode Ecosystem)](opencode.md)
- [Aider](../development_ops/aider.md)
- [Goose](../automation_orchestration/goose.md)
- [Stagehand](../automation_orchestration/stagehand.md)

## Sources / references
- [Terminal-Bench GitHub](https://github.com/pro-puffin/terminal-bench)
- [Reference Blog Post](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)
- [Terminal-Bench: A Benchmark for AI Agents in the Terminal](https://arxiv.org/abs/2501.00000)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
