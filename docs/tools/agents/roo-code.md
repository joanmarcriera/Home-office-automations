# Roo Code

## What it is
Roo Code is an open-source, AI-powered autonomous coding agent for VS Code. Originally forked from Cline, it has evolved into a highly customizable platform that supports specialized "Custom Modes," deep Model Context Protocol (MCP) integration, and multi-model orchestration. As of July 2026, it is recognized for its high velocity of community-driven feature updates, native support for **FastMCP 3.0**, and its ability to handle complex, multi-file engineering tasks autonomously using models like **Gemma 3**, Claude 4.8, and GPT-5.5.

## What problem it solves
Roo Code eliminates the friction of manual context-switching by bringing frontier reasoning models directly into the development environment. It addresses the "last mile" of AI coding by not only suggesting code but also executing terminal commands, managing files, and performing browser-based verification. Its Custom Modes feature specifically solves the "generalist fatigue" by allowing users to constrain the agent to specific roles like Security Auditor, Frontend Specialist, or Documentation Expert.

## Where it fits in the stack
**Agent / IDE Extension / Developer Experience (DX)**. It sits at the top of the stack as the primary interface between the developer and the underlying LLMs/tools.

## Typical use cases
- **Specialized Engineering**: Using the "Architect" mode to design system schemas before implementation.
- **Autonomous Refactoring**: Delegating large-scale migrations (e.g., from React 18 to 19) to the agent with human-in-the-loop oversight.
- **Automated Bug Resolution**: Letting the agent trace error logs, identify root causes, and apply fixes across the backend and frontend.
- **Documentation as Code**: Using a specialized "Writer" mode to keep technical docs in sync with code changes.
- **Fast Tool Creation**: Leveraging FastMCP 3.0 to rapidly create and deploy new tools that Roo Code can use instantly.

## Strengths
- **Custom Modes**: Native support for `.roomodes`, allowing per-project or global persona definitions with specific tool access.
- **Frontier Model Support**: Optimized for high-fidelity reasoning with Claude 4.8 Opus, GPT-5.5, and the latest **Gemma 3** models.
- **First-Class MCP Support**: Seamlessly connects to any MCP server, with enhanced support for FastMCP 3.0 for low-latency tool interactions.
- **Context Pinning**: Advanced context management allowing users to pin critical files, URLs, or documentation segments.
- **High Autonomy**: Capable of long-horizon tasks including running tests, fixing failures, and verifying UI changes via an internal browser.

## Limitations
- **Token Intensity**: Autonomous "Act Mode" can consume significant tokens, especially when processing large context windows in July 2026 models.
- **Complexity**: The high degree of customizability requires a learning curve to master mode definitions and instruction hierarchies.
- **Stability**: Fast-paced community updates can occasionally introduce regressions compared to more conservative IDE extensions.

## When to use it
- When you require an agent that can act autonomously within your IDE (file edits + terminal execution).
- If you need specialized personas for different parts of your workflow.
- When working with high-reasoning models like Claude 4.8 Opus or **Gemma 3** for complex architectural changes.
- If you prefer an open-source, community-led project with rapid feature iteration.

## When not to use it
- For simple code completions where a lighter tool like GitHub Copilot (extension) is sufficient.
- In highly restricted enterprise environments that forbid extensions from executing terminal commands.
- If you prefer a minimalist, "no-config" experience without persona management.

## Getting started
### Installation
1. Install the **Roo Code** extension from the VS Code Marketplace or Open VSX Registry.
2. Open the Roo Code sidebar and click the "Settings" (gear) icon.
3. Select your API provider (e.g., Anthropic, OpenAI, or OpenRouter) and enter your API key.
4. Set your model to `claude-4-8-opus-20260528`, `gpt-5.5-preview`, or `gemma-3-27b` for optimal performance.

### Basic Usage
1. Start a new task in the sidebar (e.g., "Implement a new API endpoint for user profiles").
2. Choose a mode (Code, Architect, or Ask) from the dropdown.
3. Review and "Approve" the plan and tool executions proposed by Roo Code.

## CLI examples
```bash
# Roo Code is primarily used as a VS Code extension; however, it can execute terminal commands
# Example: Running a security scan through an MCP-provided tool
mcp-tool-security-audit --path .

# Example: Running tests to verify an autonomous fix
npm test

# Example: Managing local MCP servers used by Roo Code
mcp-server-manager list

# Verify the current environment for Roo Code
node --version && npm --version
```

## API examples
Roo Code supports custom mode definitions via a `.roomodes` file in the repository root. This allows for defining specialized agent behaviors:

```json
{
  "customModes": [
    {
      "slug": "security-specialist",
      "name": "Security Specialist",
      "roleDefinition": "You are a senior security engineer. Your goal is to identify vulnerabilities and suggest mitigations following OWASP 2026 standards.",
      "groups": ["read", "browser", "edit"],
      "customInstructions": "Always check for dependency vulnerabilities and SQL injection patterns."
    }
  ]
}
```

## Related tools / concepts
- [Cline](cline.md) — The original project Roo Code was forked from.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard tool protocol.
- [Claude Code](../development_ops/claude-code.md) — Agentic CLI from Anthropic.
- [Aider](../development_ops/aider.md) — Terminal-based coding agent.
- [Windsurf](../development_ops/windsurf.md) — Agentic IDE from Codeium.
- [Gemma 3](../ai_knowledge/local_llms.md) — Standard high-performance local model.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — Orchestration framework.
- [Playwright](../development_ops/playwright.md) — Browser automation standard.

## Sources / references
- [Official Roo Code GitHub](https://github.com/RooCodeInc/Roo-Code)
- [Roo Code Documentation](https://docs.roocode.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2026-07-03
- Confidence: high
