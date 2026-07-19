# Terminus 2 (Terminal-Bench)

## What it is
Terminus 2 is an open-source, terminal-native AI agent and research baseline developed by the Terminal-Bench consortium. As of July 2026, it serves as the industry-standard "raw" shell execution model, bypassing heavy orchestration layers to provide a direct LLM-to-tmux bridging protocol. Specifically optimized for the CLI capabilities of SOTA frontier models like **Claude 5.1**, **GPT-5.5**, **Llama 4**, and **Gemma 3**, Terminus 2 allows models to interact with standard Unix-like shell environments natively without intermediate abstraction taxes.

## What problem it solves
Traditional agent frameworks rely on heavy runtime abstractions, isolated container sandboxes, or virtualized/mocked filesystem drivers. This introduces "abstraction tax" and context mismatch—models often struggle to translate raw terminal signals, interactive prompts, and stderr outputs when they are parsed through middleware. Terminus 2 gives the LLM direct, raw control over standard **tmux** terminal sessions. This enables authentic handling of long-running daemonized processes, real-time streaming feedback, multi-pane multiplexing, and authentic terminal error recovery, establishing a reliable baseline for "pure" terminal reasoning and evaluation.

## Where it fits in the stack
**Benchmark / Shell Interface Layer**. Terminus 2 resides directly between the model's primary reasoning/tool-calling engine and the host operating system's kernel shell. It acts as a lightweight interactive loop, translating natural language objectives into raw bash sequences executed within persistent tmux sessions, exposing these sessions natively via [Model Context Protocol (MCP 3.0)](../automation_orchestration/mcp.md) transport interfaces.

## Typical use cases
- **CLI-Agent Benchmarking**: Serving as the canonical baseline for the "Terminal-Bench v3" suite, measuring model performance on complex, multi-step command-line tasks.
- **Interactive System Administration**: Executing sophisticated sysadmin flows (e.g., live database migrations, service hardening, network port debugging) using raw terminal tooling.
- **Real-Time Human-in-the-Loop Monitoring**: Allowing human operators to `tmux attach` directly to the active agent session, observing command output and intervening manually if needed.
- **Agentic Sandboxing Research**: Researching the physical constraints, error-handling strategies, and recovery limits of models when restricted strictly to standard Unix tools and basic shell capabilities.

## Strengths
- **Zero-Abstraction Overhead**: Eschews custom virtual filesystems or heavy language-specific runtimes, providing a standard, direct shell environment.
- **Full Transparency and Observability**: High human-in-the-loop auditability. Since commands run in a real, attachable tmux session, debugging is as simple as launching a terminal.
- **Robust Session Continuity**: Native tmux architecture ensures that if the agent's Python wrapper crashes or disconnects, the underlying shell processes continue running unimpeded.
- **Extensive Multimodal Support**: Captures actual ANSI color codes and terminal layout dimensions, allowing multimodal CLI models to reason over terminal-based visuals and layouts.
- **SOTA Alignment**: Updated for **MCP 3.0/3.1**, allowing the agent's shell environment to be exposed as a standardized tool server to external orchestration clients.

## Limitations
- **Lacks GUI/Web Native Support**: Exclusively restricted to terminal applications; cannot run web-scraping browser loops or graphical tools out of the box.
- **High Token Consumption**: Raw terminal scrollbacks, interactive logs, and long-running process buffers can rapidly consume context window tokens.
- **Host Security Risk**: Unless executed inside an isolated, containerized VM (such as an [Anti-Gravity](./anti_gravity.md) sandbox), giving a model direct shell write-access poses significant host safety hazards.

## When to use it
- When evaluating or benchmarking raw shell performance and CLI tool navigation capabilities of fine-tuned frontier LLMs.
- For lightweight system administration tasks where human observability and live shell intervention are critical requirements.
- In containerized research settings where you want to minimize overhead and avoid heavy frameworks.

## When not to use it
- For enterprise software-engineering workflows that require heavy, workspace-wide IDE support (use [Windsurf](./windsurf.md), [Cursor](./cursor.md), or [Codeium](./codeium.md) instead).
- If your agent requires native web-browsing capabilities or GUI interaction.
- In production environments without robust container-level sandboxing.

## Getting started

### Installation
Terminus 2 requires Python 3.10+ and a functional host installation of `tmux` (v3.2+ recommended).

```bash
# Clone the Terminal-Bench official repository
git clone https://github.com/pro-puffin/terminal-bench.git
cd terminal-bench

# Install python dependencies
pip install -r requirements.txt

# Ensure tmux is installed in your local package manager
sudo apt-get update && sudo apt-get install -y tmux
```

### Basic Initialization
Spawn a raw Terminus 2 interactive shell session with a natural language goal:

```bash
python -m terminal_bench.agents.terminus2 \
    --task "Analyze active ports, check for listening services, and ensure nginx is running on port 80." \
    --model "claude-5-1-sonnet"
```

## CLI examples

### Active Session Management
Check and inspect active agent sessions executing within the tmux multiplexer:

```bash
# List all active background Terminus 2 agent sessions
tmux ls

# Attach directly to the active agent's run workspace to monitor command execution in real-time
tmux attach -t terminus_agent_01
```

### Headless Benchmarking Suite
Execute automated evaluations against standard terminal task benchmarks using Terminus 2:

```bash
# Run the terminal-bench v3 evaluator using Llama 4 as the backbone model
python -m terminal_bench.evaluator \
    --agent terminus2 \
    --model "llama-4-70b-instruct" \
    --suite "sysadmin_v3" \
    --output "./results/llama4_results.json"
```

### MCP 3.0 Server Integration
Expose the local Terminus 2 terminal context to external LLM clients over Model Context Protocol:

```bash
# Launch the Terminus 2 sandboxed terminal server
terminus2-mcp --port 8080 --sandbox-dir /var/tmp/agent_sandbox
```

## API examples

### Python Agent Instantiation
Use the Terminus 2 programmatic API to construct, configure, and monitor shell-native reasoning loops:

```python
from terminal_bench.agents.terminus import TerminusAgent
from terminal_bench.session import TmuxSession

# Initialize a standard tmux session wrapper
session = TmuxSession(session_name="maintenance_task_2026")

# Configure the Terminus 2 Agent with July 2026 SOTA SFT system parameters
agent = TerminusAgent(
    session=session,
    model="claude-5-1-sonnet",
    temperature=0.0,
    system_prompt="""
    You are an expert systems engineer operating in a direct tmux terminal.
    Favor modern Unix CLI tools (rg, fd, bat) and verify the outcome of all actions.
    If a command blocks, detach or background it.
    """
)

# Execute a complex terminal workflow programmatically
objective = "Find and compress all .log files in /var/log/app/ older than 7 days, excluding sys.log"
success = agent.run(task=objective)

if success:
    print("Agent completed the objective successfully.")
else:
    print("Agent encountered errors or failed to resolve the goal.")
```

### Wrapping Terminus 2 within AG2 Framework
Incorporate Terminus 2 as a low-level tmux execution tool inside a multi-agent assembly under [AG2](../frameworks/ag2.md):

```python
from ag2 import Agent, GroupChat
from terminal_bench.integrations.ag2 import TerminusTmuxTool

# Instantiate the specialized tmux execution tool
terminal_tool = TerminusTmuxTool(session_name="ag2_shell_sandbox")

# Define a system administrator agent equipped with direct tmux access
sysadmin_agent = Agent(
    name="SystemAdmin",
    instructions="You execute shell maintenance tasks. Use the tmux tool to run and observe commands.",
    tools=[terminal_tool]
)

# Now, SystemAdmin can interact dynamically with the same terminal session
# while maintaining session persistence across group chat turns.
```

## Related tools / concepts
- [OpenHands](./openhands.md) — Comprehensive agentic workspace framework.
- [Devin](./devin.md) — Autonomous software engineer.
- [Codeium](./codeium.md) — Enterprise-grade AI-assisted developer ecosystem.
- [Aider](./aider.md) — Terminal-based Git-native pair programmer.
- [Goose](../agents/goose.md) — Extensible agentic coding and automation tool.
- [AG2](../frameworks/ag2.md) — Orchestration framework for multi-agent applications.
- [Model Context Protocol (MCP 3.0)](../automation_orchestration/mcp.md) — Telemetry-driven universal LLM tool connection protocol.
- [Claude Code](./claude-code.md) — Anthropic's terminal developer agent.
- [Windsurf](./windsurf.md) — Next-gen flow-based developer IDE.
- [Cursor](./cursor.md) — AI-first code editor.
- [Droid](./droid.md) — CLI task automation agent.
- [Anti-Gravity](./anti_gravity.md) — Sandboxed mission executor.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Structured design patterns for multi-agent coordination.
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Pattern comparison for native vs. protocol-hosted tools.
- [tmux (Terminal Multiplexer)](https://github.com/tmux/tmux) — Standard terminal session multiplexer.

## Sources / references
- [Terminal-Bench GitHub Repository](https://github.com/pro-puffin/terminal-bench)
- [Research Paper: Terminal-Bench - Evaluative Frontiers for CLI Agents](https://arxiv.org/abs/2501.00000)
- [Blog: The Rise of Terminal-Native Agents (June 2026)](https://mariozechner.at/posts/2026-06-15-terminus2-update/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
