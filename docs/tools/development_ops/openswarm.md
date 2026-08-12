# OpenSwarm

## What it is
OpenSwarm is a multi-agent orchestrator for the Claude CLI, designed specifically for managing workflows on platforms like Linear and GitHub. It leverages the agentic capabilities of Claude to automate repetitive development and project management tasks. As of late December 2026, OpenSwarm features native support for the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** Task Protocols, enabling seamless coordination of complex, long-running agentic tasks.

## What problem it solves
It simplifies the coordination of multiple AI agents performing complex, interdependent tasks across project management and version control systems, reducing the manual overhead of managing individual agent runs. It bridges the gap between raw LLM APIs and the specific workflows used by engineering teams.

## Where it fits in the stack
**Agent / Orchestrator**. It acts as the management layer that dispatches tasks to multiple instances of the Claude CLI, coordinating their outputs and maintaining long-term project context.

## Typical use cases
- **Automated Issue Management**: Using agents to triage, label, and respond to Linear issues.
- **Pull Request Orchestration**: Coordinating multiple agents to review code, run tests, and suggest improvements on GitHub.
- **CLI-based Agent Loops**: Running complex multi-step agentic tasks directly from the terminal.
- **Context Synthesis**: Summarizing long discussion threads across multiple platforms to provide actionable next steps.

## Strengths
- **Native Claude CLI Integration**: Leverages the power of Anthropic's official CLI tools.
- **Workflow Focused**: Specifically tuned for the tools developers use most (Linear, GitHub).
- **Open Source**: Allows for community customization and extension.
- **Scalable**: Can manage a "swarm" of agents working in parallel on different parts of a project.
- **Frontier Model Ready**: Optimized for [Claude 5.1](../providers/anthropic.md) and [GPT-5.5](../ai_knowledge/openai.md).

## Limitations
- **Narrow Ecosystem**: Primarily focused on Linear and GitHub; may require custom work for other integrations.
- **Dependency**: Highly dependent on the stability and features of the Claude CLI and Anthropic's API.

## When to use it
- When you need to coordinate multiple agentic tasks across Linear and GitHub using Claude.
- For developers looking for a CLI-first approach to multi-agent orchestration.
- When automating the "human-in-the-loop" triage process for high-volume repositories.

## When not to use it
- For general-purpose automation that doesn't involve the Claude CLI or specific engineering tools.
- When working with platforms not yet supported by the OpenSwarm ecosystem (e.g., Jira, GitLab) without custom drivers.

## Getting started

### Installation
OpenSwarm can be installed via npm or cloned from GitHub:

```bash
npm install -g @intrect/openswarm
```

### Configuration
Configure your environment variables for platform access:

```bash
export ANTHROPIC_API_KEY="your-key"
export LINEAR_API_KEY="your-linear-key"
export GITHUB_TOKEN="your-github-token"
```

## CLI examples

### Triaging Linear Issues
Run an agent to triage new issues in a specific Linear team, applying labels based on AI analysis:

```bash
openswarm linear triage --team "ENG" --auto-label
```

### GitHub PR Review Swarm
Initiate a swarm of agents to review a specific Pull Request with specialized strategies:

```bash
openswarm github review --pr 42 --strategy "security,performance,style"
```

### Context and Knowledge Management
OpenSwarm utilizes LanceDB for high-performance vector storage of project context. You can sync documentation or code to the vector store:

```bash
# Sync local documentation for RAG-based reasoning
openswarm context sync --path ./docs --db-path ~/.openswarm/lancedb
```

## API examples

### Minimal Node.js Integration
OpenSwarm can be used programmatically to trigger swarms from your own scripts:

```javascript
import { OpenSwarm } from '@intrect/openswarm';

const swarm = new OpenSwarm({
  provider: 'anthropic',
  model: 'claude-5.1-opus-20261215'
});

await swarm.dispatch('linear', 'triage', { team: 'ENG' });
```

### Programmatic Python Session Handler (Pydantic v2)
Manage the state of multi-agent execution safely using Pydantic validation:

```python
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class AgentTask(BaseModel):
    agent_id: str = Field(..., alias="agentId")
    strategy: Literal["security", "performance", "style", "triage"]
    max_duration_seconds: int = Field(default=300, alias="maxDurationSeconds")

class SwarmDispatchConfig(BaseModel):
    session_id: str = Field(..., alias="sessionId")
    provider: str = Field(default="anthropic")
    model: str = Field(default="claude-5.1")
    tasks: List[AgentTask] = Field(default_factory=list)

    class Config:
        populate_by_name = True

# Validate active dispatcher session
dispatch_payload = {
    "sessionId": "swarm-session-abc-123",
    "provider": "anthropic",
    "model": "claude-5.1",
    "tasks": [
        {"agentId": "agent-1", "strategy": "security", "maxDurationSeconds": 600},
        {"agentId": "agent-2", "strategy": "triage"}
    ]
}

config = SwarmDispatchConfig.model_validate(dispatch_payload)
print(f"Validated swarm session: {config.session_id}")
print(f"Dispatched {len(config.tasks)} agents using model {config.model}")
```

## Related tools / concepts
- [Claude Code](./claude-code.md) — Anthropic's CLI tool that OpenSwarm orchestrates.
- [Anthropic](../providers/anthropic.md) — The underlying LLM provider.
- [Multi-Agent Systems](../../knowledge_base/agent_protocols.md) — Architectural patterns for agent coordination.
- [Plandex](./plandex.md) — For complex, multi-file engineering tasks.
- [Aider](./aider.md) — Terminal-native pair programming.
- [Mentat](./mentat.md) — Multi-file AI editing.
- [Sweep](./sweep_dev.md) — For automating GitHub issues into PRs.
- [Superconductor](./superconductor.md) — Parallel agent sessions for rapid development.
- [Model Context Protocol](../automation_orchestration/mcp.md) — For extending agent capabilities.

## Sources / References
- [OpenSwarm GitHub](https://github.com/Intrect-io/OpenSwarm)
- [Anthropic Claude CLI Documentation](https://docs.anthropic.com/claude/docs/claude-cli)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
