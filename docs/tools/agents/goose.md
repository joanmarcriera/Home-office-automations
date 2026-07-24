# Goose

## What it is
Goose is an open-source, extensible AI agent designed to go beyond simple code suggestions. It is built to install, execute, edit, and test code autonomously or with human supervision, using any LLM that supports tool-calling. Hosted by the Agentic AI Foundation (AAIF), it serves as a robust platform for building and deploying specialized developer agents. As of late August 2026, it fully integrates the **Model Context Protocol (MCP 3.1)** Task Protocol and is optimized for frontier models such as **Claude 5.1** and **GPT-5.5**.

## What problem it solves
It bridges the gap between static code completion and full-loop agentic software engineering. Goose can manage its own environment, install dependencies, and run scripts to verify its work, reducing the manual "context switching" developers often face when integrating AI-generated code. It solves the "execution gap" by running the code it writes to ensure correctness (and automatically fixing errors via traceback loops) before presenting it to the user.

## Where it fits in the stack
**Automation & Orchestration / Agents**. It is an agentic layer that sits on top of LLMs (like Claude, GPT-4/GPT-5.5, or local models) and interacts with the filesystem and shell. It is a direct open-source alternative to tools like [Aider](../development_ops/aider.md) or [OpenHands](../development_ops/openhands.md).

## Typical use cases
- **Automated Bug Fixing**: Providing an issue description and letting Goose find, fix, and verify the solution with unit tests.
- **Environment Setup**: Asking Goose to "set up a new React project with Tailwind and Vitest" and letting it handle all shell commands, config, and tests.
- **Large-Scale Refactoring**: Executing systematic code changes across hundreds of files with automated verification loops.
- **Agentic CI/CD Remediation**: Integrating Goose into pipeline scripts to automatically attempt remediation for common build or dependency failures.

## Strengths
- **Extensible Toolkit**: Users can easily add new "Toolkits" (e.g., specific DB connectors, proprietary API clients, or MCP 3.1 servers) to Goose.
- **AAIF Governance**: Community-driven development ensures neutrality, vendor independence, and long-term stability.
- **Model Agnostic**: Seamlessly switches between Anthropic, OpenAI, Google, and local models via [Ollama](../../services/ollama.md) or [LiteLLM](../../services/litellm.md).
- **Session Management**: Supports durable, stateful sessions, allowing users to pause, resume, and audit complex multi-step agentic missions.
- **MCP 3.1 Task Protocol**: Allows external agents to delegate background execution tasks directly to Goose over the network.

## Limitations
- **Security Responsibility**: Giving an agent shell and filesystem access requires the user to manage trust boundaries and sandboxing (e.g., running in Docker/VMs).
- **Token Efficiency**: Complex tasks can involve many iterations, leading to high token consumption if the model loops on difficult problems.
- **Rapid Evolution**: Frequent core updates can lead to breaking changes in experimental toolkits.

## When to use it
- When you need a full-loop agentic software engineer that can fix bugs and run tests autonomously.
- When you want a neutral, open-source platform for building your own specialized coding agents.
- When you need to automate repetitive system administration or development tasks that require both shell execution and code editing.

## When not to use it
- For simple, single-file code completion where a lightweight tool like standard Copilot is faster.
- In highly restricted environments where giving an AI agent shell/filesystem access is strictly prohibited.
- If you prefer a purely GUI-based tool (Goose is optimized for CLI and agentic API usage).

## Getting started

### Installation
Goose can be installed via its official installer or as a Python package.

```bash
# Recommended installer
curl -fsSL https://goose.run/install.sh | sh
```

### Basic Usage
```bash
# Start an interactive Goose session
goose session

# Execute a one-off mission
goose run "Audit the current directory for security vulnerabilities in package.json and fix them."
```

## CLI examples

### Mission Execution
```bash
# Run a specific mission with a defined model
goose run "Refactor all exported functions in src/utils to use arrow syntax" --model claude-5-1-sonnet

# Run an autonomous verification loop
goose run "Run pytest and fix any failures found in the test suite" --max-turns 15

# List active sessions
goose session list
```

### Toolkit and MCP 3.1 Management
```bash
# List available toolkits
goose tools list

# Enable a specific toolkit for a session
goose session --toolkit developer

# Connect Goose directly to an external MCP 3.1 server
goose session --mcp-server http://localhost:8080/mcp
```

## API examples

### Python Agentic API
Goose can be used as a library to build custom agent applications under late August 2026 specs:
```python
from goose.agent import GooseAgent
from goose.config import AgentConfig

# Initialize with advanced token limits and prompt templates
config = AgentConfig(
    model="gpt-5.5-preview",
    temperature=0.2,
    max_tokens_per_turn=4096
)

agent = GooseAgent(config=config)
response = agent.execute("Create a summary report of the current git status and stage modified files.")
print(response.content)
```

### Custom MCP 3.1-Compatible Toolkit Definition
```python
from goose.toolkit import Toolkit, tool
from pydantic import BaseModel, Field

class NetworkQuery(BaseModel):
    hostname: str = Field(..., description="The host to run diagnostics on")

class DiagnosticsToolkit(Toolkit):
    @tool
    def ping_host(self, query: NetworkQuery) -> str:
        """Runs a ping check against the provided hostname and returns diagnostic summary."""
        import subprocess
        try:
            res = subprocess.run(["ping", "-c", "3", query.hostname], capture_output=True, text=True, timeout=5)
            return res.stdout
        except Exception as e:
            return f"Ping failed: {str(e)}"
```

## Related tools / concepts
- [Aider](../development_ops/aider.md) — CLI tool for pair programming.
- [OpenHands](../development_ops/openhands.md) — platform for autonomous software development.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's terminal-based agent.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — protocol used by many agentic tools.
- [ServiceNow MCP Server](../automation_orchestration/servicenow-mcp.md) — example of a specialized toolset.
- [LiteLLM](../../services/litellm.md) — used for universal model access.
- [Ollama](../../services/ollama.md) — for running local models with Goose.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — framework for managing agentic knowledge.

## Sources / references
- [Goose GitHub Repository](https://github.com/aaif-goose/goose)
- [Goose Official Website](https://goose.run)
- [AAIF Announcement on Developer Tooling](https://agentic-ai-foundation.org/news/goose-joins-aaif)
- [Goose Documentation](https://goose.run/docs)

## Contribution Metadata
- Last reviewed: 2026-08-03
- Confidence: high
