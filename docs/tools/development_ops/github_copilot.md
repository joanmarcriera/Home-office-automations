# GitHub Copilot

## What it is
An AI pair programmer that provides autocomplete-style suggestions as you code. Powered by OpenAI, Anthropic, and Google models, it integrates into various IDEs, CLI environments, and GitHub's web interface. As of early 2027, GitHub Copilot incorporates native **FastMCP 3.1 Task Protocol** support, enabling agentic workspace reasoning, context-aware tool calling, and automated cross-repository multi-step task execution.

## What problem it solves
Speeds up coding by generating inline code suggestions, reducing time spent writing boilerplate and looking up API usage. It provides a chat interface and background task runner for complex reasoning, refactoring, agentic task execution, and debugging directly within the IDE or CLI.

## Where it fits in the stack
**Development & Ops**. Provides AI-powered code completion, FastMCP 3.1 agent execution, and chat assistance as an IDE extension, CLI tool, and GitHub platform integration.

## Typical use cases
- Inline code completion while writing code.
- Generating boilerplate and repetitive patterns.
- CLI-based command explanation, script generation, and shell automation.
- Full-project reasoning via the `@workspace` agent using FastMCP 3.1 Task Protocol loops.
- **Enterprise Inference**: Integration with [NVIDIA NIM](../providers/nvidia.md) (NVIDIA Inference Microservices) for self-hosted, high-performance model serving in hybrid enterprise environments.

## Strengths
- Deep integration with GitHub ecosystem (Issues, PRs, Actions, FastMCP 3.1 tool catalog).
- Supported in many popular IDEs (VS Code, JetBrains, Visual Studio, Neovim, Zed).
- Support for multiple frontier models, including [GPT-5.6](../ai_knowledge/openai.md), [Claude 5.6](../providers/anthropic.md), and Gemini 4.0 Ultra.
- Enterprise-grade security, privacy compliance, and repository access boundary filters.

## Limitations
- Requires a paid subscription or enterprise plan.
- Cloud-based by default; code snippets are sent to external or hybrid servers for inference unless configured with self-hosted NIM endpoints.
- Native integration in non-VS Code IDEs can occasionally lag behind VS Code feature releases.

## When to use it
- When you want a well-supported, mainstream AI code completion and task automation tool.
- When working within the GitHub ecosystem.
- When you need to toggle between different SOTA frontier models (GPT-5.6 vs Claude 5.6 vs Gemini 4.0 Ultra) for different reasoning tasks.

## When not to use it
- When strict local-only code processing is required without enterprise cloud options (consider [Ollama](../../services/ollama.md) + [Continue](continue_dev.md)).
- When you prefer an open-source or free alternative (consider [Codeium](codeium.md)).

## Getting started

### Installation
GitHub Copilot is available as an extension for VS Code, Visual Studio, JetBrains, Neovim, and Zed, or via the GitHub CLI:

```bash
gh extension install github/gh-copilot
```

### Hello-world example
Verify installation and invoke Copilot in the terminal to explain a command:

```bash
gh copilot explain "git status"
```

1. **IDE Setup**: Install the "GitHub Copilot" and "GitHub Copilot Chat" extensions from your IDE marketplace.
2. **Auth**: Sign in to your GitHub account with an active Copilot subscription.
3. **Use**: Start typing to see inline suggestions, or press `Cmd+I` (Mac) / `Ctrl+I` (Windows) to open the inline chat or launch a FastMCP 3.1 agent loop.

### Model Selection (January 2027)
You can select your preferred model in the Copilot Chat settings or agent session panel:
- **Default / Speed**: GPT-5.6 (Optimized for low-latency speed and general coding).
- **Advanced Reasoning & Architecture**: Claude 5.6 (Optimized for complex architectural tasks, refactoring, and FastMCP 3.1 agent loops).
- **Multimodal & Long-Context**: Gemini 4.0 Ultra (Optimized for massive codebase analysis and multimodal input processing).

## CLI examples

### GitHub Copilot CLI
The Copilot CLI brings AI assistance directly to your terminal for explaining commands or generating scripts.

```bash
# Ask for a command explanation
gh copilot explain "git log --oneline --graph --all"

# Suggest a command for a task (interactive)
gh copilot suggest "find all large files over 100MB and delete them"

# Update the CLI extension
gh extension upgrade gh-copilot
```

## API examples

### Copilot Extensions & FastMCP 3.1 Task Protocol API
Developers can build custom extensions for Copilot Chat using FastMCP 3.1 Task Protocol schemas:

```javascript
// FastMCP 3.1 Task Protocol Copilot Extension snippet
export async function handleRequest(request) {
  const { prompt, model, task_context } = request;
  // Dynamic tool calling and context fetching via FastMCP 3.1
  const context = await fetchInternalDocs(prompt, task_context);
  return {
    message: `Based on verified internal docs: ${context}`,
    model: 'claude-5.6',
    task_status: 'in_progress'
  };
}
```

### Programmatic Python Setup (Pydantic v2)
Validate enterprise configuration properties, model routing policies, and FastMCP 3.1 Task Protocol options:

```python
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class FastMCPTaskConfig(BaseModel):
    protocol_version: str = Field(default="3.1", alias="protocolVersion")
    max_steps: int = Field(default=20, alias="maxSteps")
    enable_auto_execution: bool = Field(default=False, alias="enableAutoExecution")

class EnterprisePolicy(BaseModel):
    allowed_models: List[str] = Field(default_factory=list, alias="allowedModels")
    allow_telemetry: bool = Field(default=False, alias="allowTelemetry")
    blocked_patterns: List[str] = Field(default_factory=list, alias="blockedPatterns")

class CopilotConfig(BaseModel):
    user_model: Literal["gpt-5.6", "claude-5.6", "gemini-4.0-ultra"] = Field(default="claude-5.6")
    enable_autocomplete: bool = Field(default=True)
    task_config: Optional[FastMCPTaskConfig] = None
    policy: Optional[EnterprisePolicy] = None

    class Config:
        populate_by_name = True

# Validate active policy configuration
config_data = {
    "user_model": "claude-5.6",
    "enable_autocomplete": True,
    "task_config": {
        "protocolVersion": "3.1",
        "maxSteps": 25,
        "enableAutoExecution": True
    },
    "policy": {
        "allowedModels": ["gpt-5.6", "claude-5.6", "gemini-4.0-ultra"],
        "allowTelemetry": False,
        "blockedPatterns": ["**/*.key", "**/*.pem"]
    }
}

config = CopilotConfig.model_validate(config_data)
print(f"Validated Model selection: {config.user_model}")
if config.task_config:
    print(f"FastMCP Task Protocol Version: {config.task_config.protocol_version}")
if config.policy:
    print(f"Telemetry allowed: {config.policy.allow_telemetry}")
    print(f"Blocked path patterns count: {len(config.policy.blocked_patterns)}")
```

## Related tools / concepts
- [Codeium](codeium.md) — Fast, AI coding assistant.
- [Tabnine](tabnine.md) — Privacy-focused AI pair programmer.
- [Claude Code](claude-code.md) — Anthropic's agentic coding CLI.
- [Aider](aider.md) — Terminal-native pair programming with Git integration.
- [VS Code](vscode.md) — The primary IDE host for Copilot.
- [Zed](zed.md) — High-performance editor with native Copilot support.
- [Cursor](cursor.md) — AI-native IDE with deep code intelligence.
- [Sourcegraph Cody](sourcegraph_cody.md) — Context-aware AI coding assistant.

## Sources / references
- [Official Website](https://github.com/features/copilot)
- [Copilot CLI Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)
- [GitHub Copilot Trust Center](https://resources.github.com/copilot-trust-center/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
