# OpenSwarm

## What it is
OpenSwarm is an open-source multi-agent orchestrator designed to run on top of the Claude CLI (Claude Code). It enables the creation of an autonomous "AI dev team" that integrates directly into real-world engineering workflows, specifically targeting platforms like GitHub and Linear.

## What problem it solves
Managing multiple AI agents for complex, interdependent tasks often involves significant manual overhead. OpenSwarm automates the coordination of these agents, allowing them to triage issues, write code, run tests, and generate documentation in a structured pipeline, reducing the "human-in-the-loop" requirement for routine development tasks.

## Where it fits in the stack
**Agent / Orchestrator**. It acts as the management layer that dispatches tasks to multiple instances of the Claude CLI, coordinating their outputs and maintaining long-term project context.

## Typical use cases
- **Autonomous Issue Resolution**: Automatically pulling issues from Linear, implementing a fix, and submitting a PR.
- **AI-Powered Code Review**: Running a specialized "Reviewer" agent on every new Pull Request.
- **Continuous Documentation**: Using a "Documenter" agent to update markdown files whenever code changes are merged.
- **Impact Analysis**: Building a code knowledge graph to understand how a change in one module affects the rest of the system.

## Getting started

### Installation
OpenSwarm typically requires Python and the Anthropic Claude CLI.

```bash
# Clone the repository
git clone https://github.com/Intrect-io/OpenSwarm
cd OpenSwarm

# Install dependencies
pip install -r requirements.txt
```

### Configuration
You will need API keys for Anthropic, Linear, and GitHub. These are usually configured via environment variables or a `.env` file:

```bash
export ANTHROPIC_API_KEY='your-key'
export LINEAR_API_KEY='your-key'
export GITHUB_TOKEN='your-token'
```

### Basic Workflow
OpenSwarm can be triggered to work on a specific Linear issue:

```bash
python main.py --issue LINEAR-123
```

This initiates the pipeline: **Worker** (implements fix) -> **Tester** (verifies) -> **Reviewer** (checks quality) -> **Documenter** (updates docs).

## Strengths
- **Native Claude Integration**: Built specifically to leverage the advanced reasoning and coding capabilities of Claude 3.5.
- **Real-world Integration**: Direct support for Linear and GitHub makes it more than just a "toy" agent.
- **Long-term Memory**: Uses LanceDB for vector-based memory, allowing agents to reuse context across different tasks.
- **Observability**: Often includes a Discord bot interface for real-time status updates and job dispatching.

## Limitations
- **Early Stage**: As a frontier project, it may have "rough edges" regarding safety and complex task decomposition.
- **Platform Specificity**: Heavily optimized for GitHub and Linear; other platforms may require custom integration.
- **Token Usage**: Running multiple agentic loops can consume significant API credits.

## When to use it
- When you want to automate the end-to-end lifecycle of a software issue (from triage to PR).
- If you are already using Claude CLI and want to scale it to multiple specialized agents.
- For solo developers or small teams looking to augment their capacity with autonomous agents.

## When not to use it
- For high-stakes, mission-critical code changes where human oversight is non-negotiable.
- If your project does not use Linear or GitHub for task and source management.
- When budget constraints limit the use of high-volume LLM API calls.

## Related tools / concepts
- [Claude Code](claude-code.md): The underlying CLI tool used by OpenSwarm.
- [Anthropic](../providers/anthropic.md): The provider of the Claude models.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): The architectural pattern OpenSwarm implements.
- [OpenHands](openhands.md): An open-source platform for autonomous AI software agents.
- [Devin](devin.md): A fully autonomous AI software engineer.
- [Aider](aider.md): A high-performance terminal coding assistant.
- [Linear Integration](../../knowledge_base/patterns/linear-integration.md): Patterns for connecting AI to project management.

## Sources / References
- [OpenSwarm GitHub Repository](https://github.com/Intrect-io/OpenSwarm)
- [Hacker News Launch Thread](https://news.ycombinator.com/item?id=47160980)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
