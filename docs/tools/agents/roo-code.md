# Roo Code

## What it is
Roo Code is an open-source, AI-powered autonomous coding agent for VS Code, JetBrains IDEs, and CLI workflows. Originally forked from Cline, it has evolved into a customizable platform that supports specialized "Custom Modes," deep Model Context Protocol (MCP) integration, and multi-model orchestration. In early 2027, it is recognized for its high velocity of community-driven feature updates, native support for **MCP 3.1** and **FastMCP 3.1**, and its ability to handle complex, multi-file engineering tasks autonomously using models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, **DeepSeek-V4**, and local models via Ollama.

## What problem it solves
Roo Code eliminates developer context-switching friction by bringing frontier reasoning models directly into the development environment. It addresses the "last mile" of AI coding by not only suggesting code but also executing terminal commands, managing files, running test suites, and performing browser-based visual verification. Its Custom Modes feature specifically solves "generalist model fatigue" by allowing developers to constrain the agent to specific system personas like Security Auditor, Frontend Specialist, System Architect, or Technical Writer.

## Where it fits in the stack
**Agent / IDE Extension / CLI / Developer Experience (DX)**. It sits at the top of the developer stack as a primary orchestration interface between the developer, local filesystem/terminal, and underlying LLMs/FastMCP tool servers.

## Typical use cases
- **Specialized Engineering via Custom Modes**: Utilizing the "Architect" mode to design system schemas and API interfaces before switching to "Code" mode for implementation.
- **Autonomous Refactoring & Migrations**: Delegating major framework upgrades (e.g., React 18 to 19, Next.js 15 to 16) to the agent with explicit human-in-the-loop approval checkpoints.
- **Automated Bug Reproduction & Fixing**: Letting the agent trace error stack traces, reproduce issues via automated tests, and apply multi-file fixes across backend and frontend codebases.
- **Documentation Synchronization**: Utilizing a specialized "Writer" mode to keep technical documentation and API reference files synchronized with code modifications.
- **Low-Latency Prototyping via FastMCP 3.1**: Rapidly connecting custom tool servers to grant Roo Code instant access to internal databases, cloud APIs, and diagnostic tools.

## Strengths
- **Granular Custom Modes**: Native support for `.roomodes` configuration files, allowing per-project or global persona definitions with specific tool group permissions (read, edit, execute, browser).
- **Frontier & Open Model Support**: Optimized for high-fidelity reasoning with Claude 5.1, GPT-5.5, Gemini 4.0 Pro, DeepSeek-V4, and local Llama 4 / Qwen models.
- **First-Class FastMCP 3.1 Integration**: Connects seamlessly to any FastMCP server for ultra-low latency tool execution and streaming tool responses.
- **Context Pinning & Management**: Advanced context controls allowing users to pin critical code files, documentation links, or architectural constraints into active memory.
- **High Multi-Step Autonomy**: Capable of executing long-horizon tasks including running unit test suites, diagnosing failures, and visually inspecting UI changes via an embedded browser.

## Limitations
- **High Token Consumption**: Multi-file autonomous execution loops consume substantial context window tokens during deep iterative reasoning sessions.
- **Configuration Learning Curve**: Setting up custom `.roomodes` definitions and tool permission hierarchies requires initial onboarding effort.
- **Rapid Release Cadence**: Frequent community updates bring fast feature iterations but occasionally require users to adjust to UI and setting updates.

## When to use it
- When requiring an autonomous agent that can execute multi-file edits, terminal commands, and browser checks directly in your IDE.
- If you need specialized agent personas (e.g., Security, Architecture, Code, Docs) tailored to specific parts of your engineering workflow.
- When pairing frontier reasoning models like Claude 5.1 or DeepSeek-V4 with local FastMCP tool integrations.
- When preferring an open-source, community-led platform with rapid feature evolution.

## When not to use it
- For instant single-line code completions where lighter autocomplete tools like GitHub Copilot are faster.
- In enterprise environments where strict corporate security policies forbid IDE extensions from executing shell commands.
- If you prefer a zero-configuration, minimalist assistant without persona management options.

## Getting started
### Installation
1. Search for and install **Roo Code** from the VS Code Marketplace or Open VSX Registry.
2. Open the Roo Code sidebar panel and click the Settings icon.
3. Select your API provider (e.g., Anthropic, OpenAI, OpenRouter, or DeepSeek) and enter your API key.
4. Set your target model to `claude-5-1-sonnet-20261022` or `deepseek-v4` for optimal performance.

### Basic Usage
1. Open the Roo Code sidebar and start a new task (e.g., "Implement OAuth2 PKCE login flow with unit tests").
2. Select an active mode (e.g., Code, Architect, or Ask) from the mode selector.
3. Review the agent's proposed plan and approve file edits or terminal commands as execution progresses.

## CLI examples
```bash
# Roo Code can be driven via terminal execution commands and MCP server runners
# Example: Executing a security scan via a registered MCP security tool
mcp-tool-security-audit --path . --output json

# Example: Executing unit tests to verify an autonomous bug fix
npm test -- --watch=false

# Example: Inspecting active local FastMCP tool servers
mcp-server-manager list

# Verify local runtime dependencies required for terminal execution
node --version && npm --version
```

## API examples
Roo Code supports custom mode configurations via a `.roomodes` JSON file in the project root directory. This Python script demonstrates validating `.roomodes` configuration profiles using **Pydantic v2**:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class CustomMode(BaseModel):
    slug: str = Field(..., description="Unique identifier slug for the custom mode")
    name: str = Field(..., description="Display name of the custom mode")
    role_definition: str = Field(..., alias="roleDefinition", description="System prompt persona instructions")
    groups: List[str] = Field(..., description="Allowed tool groups (e.g., read, edit, execute, browser)")
    custom_instructions: Optional[str] = Field(None, alias="customInstructions", description="Additional project guidelines")

class RooModesConfig(BaseModel):
    custom_modes: List[CustomMode] = Field(..., alias="customModes", description="List of custom modes")

def validate_roomodes_config(raw_json: str) -> Optional[RooModesConfig]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2 model_validate
        return RooModesConfig.model_validate(data)
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON payload.")
        return None
```

## Related tools / concepts
- [Cline](cline.md) — The original open-source coding agent framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open protocol standard for model tools.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's terminal-based coding agent.
- [Aider](../development_ops/aider.md) — Command-line pair programming agent.
- [Windsurf](../development_ops/windsurf.md) — Commercial agentic IDE platform.
- [Local LLMs](../../ai_knowledge/local_llms.md) — Guide for running local open-weights models.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — Agentic orchestration framework.
- [Playwright](../development_ops/playwright.md) — Browser automation engine.

## Sources / references
- [Official Roo Code GitHub Repository](https://github.com/RooCodeInc/Roo-Code)
- [Roo Code Official Documentation](https://docs.roocode.com/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
