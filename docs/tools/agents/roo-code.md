# Roo Code

## What it is
Roo Code is an open-source, AI-powered coding agent for VS Code. It is a highly popular and feature-rich fork of Cline (formerly Claude Dev), designed to provide a more dynamic and community-driven alternative for autonomous development.

## What problem it solves
Like its predecessor, Roo Code solves the context-switching problem by integrating AI directly into the IDE. It differentiates itself by offering specialized "Custom Modes" (personalities), rapid integration of community features, and a focus on power-user customizations.

## Where it fits in the stack
**Agent / IDE Extension / Developer Experience (DX)**.

## Typical use cases
- **Task-Specific Assistance**: Using Custom Modes for security auditing, documentation writing, or performance optimization.
- **Autonomous Refactoring**: Delegating complex codebase changes to the agent while monitoring progress.
- **Rapid Prototyping**: Quickly spinning up boilerplate and initial logic across multiple files.
- **Exploratory Debugging**: Letting the agent trace through logs and source code to find root causes.

## Patterns
- **Custom Modes**: Users can define specific personas in a `.roomodes` file, allowing for specialized agents like "Reviewer", "DevOps", or "Copywriter".
- **MCP Tool Hub**: Roo Code treats the [Model Context Protocol](../automation_orchestration/mcp.md) as a first-class citizen, enabling seamless connection to local and remote tools.
- **Context Pinning**: Allows users to pin specific files or documentation URLs to the current task to ensure the agent has the necessary background.

## Strengths
- **Custom Modes**: Allows users to define specific personas and instruction sets for different tasks.
- **Community-Driven**: Fast-paced development cycle with frequent updates and community contributions.
- **Extensible Tooling**: Strong support for the Model Context Protocol (MCP) to add new capabilities.
- **Model Flexibility**: Supports all major LLM providers (Anthropic, OpenAI, DeepSeek, Google, etc.) and local models.
- **Power User Features**: Includes advanced options for context management, instruction hierarchy, and terminal interaction.

## Limitations
- **Stability**: Due to its fast-paced nature, it can occasionally be less polished than the more conservative upstream Cline.
- **Complexity**: The sheer number of features and customization options can be overwhelming for new users.
- **Token Usage**: Agentic "Act Mode" can be expensive if not monitored.

## When to use it
- If you want the most cutting-edge features and customization options available for a VS Code agent.
- When you need task-specific "modes" to constrain the AI's behavior to certain domains (e.g., unit testing).
- If you prefer a community-led project with a high velocity of updates.

## When not to use it
- If you prioritize absolute stability and a minimalist interface over advanced features.
- In environments where extension updates need to be strictly vetted.

## CLI examples
```bash
# Roo Code is primarily used as a VS Code extension; however, it can execute terminal commands
# Example: Running a security scan through an MCP-provided tool
mcp-tool-security-audit --path .

# Example: Running tests to verify an autonomous fix
npm test

# Example: Managing local MCP servers used by Roo Code
mcp-server-manager list
```

## Getting started
### Installation
1. Install the **Roo Code** extension from the VS Code Marketplace or Open VSX Registry.
2. Open the Roo Code sidebar and configure your Preferred AI provider.
3. (Optional) Explore "Custom Modes" by clicking the mode selector at the top of the sidebar.

### Basic Usage
1. Open a workspace and start a new Roo Code task.
2. Choose a mode (e.g., Code, Architect, or Ask).
3. Review and approve the proposed file changes and terminal commands.

## API examples
Roo Code allows for custom mode definitions via JSON. A sample `.roomodes` entry:

```json
{
  "customModes": [
    {
      "slug": "security-audit",
      "name": "Security Auditor",
      "roleDefinition": "You are an expert security researcher focusing on OWASP Top 10 vulnerabilities.",
      "groups": ["read", "browser"]
    }
  ]
}
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free (Extension) + LLM API costs.
- **Self-hostable**: Yes (local models supported).

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Cline](cline.md) (The project it was forked from)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Aider](../development_ops/aider.md) (Terminal-based agent)
- [Claude Code](../development_ops/claude-code.md)
- [Windsurf](../development_ops/windsurf.md)

## Sources / References
- [Official GitHub](https://github.com/RooCodeInc/Roo-Code)
- [Roo Code Documentation](https://docs.roocode.com/)
- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
