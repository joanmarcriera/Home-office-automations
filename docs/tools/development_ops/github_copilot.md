# GitHub Copilot

## What it is
An AI pair programmer that provides autocomplete-style suggestions as you code. It is powered by OpenAI and Anthropic models and integrated into various IDEs. It can also be used via CLI and GitHub's web interface.

## What problem it solves
Speeds up coding by generating inline code suggestions, reducing the time spent writing boilerplate and looking up API usage. It also provides a chat interface for complex reasoning, refactoring, and debugging directly within the IDE.

## Where it fits in the stack
**Development & Ops**. Provides AI-powered code completion and chat assistance as an IDE extension and CLI tool.

## Typical use cases
- Inline code completion while writing code.
- Generating boilerplate and repetitive patterns.
- CLI-based command explanation and script generation.
- Full-project reasoning via the `@workspace` agent.
- **Enterprise Inference**: Integration with [NVIDIA NIM](../providers/nvidia.md) (NVIDIA Inference Microservices) for self-hosted, high-performance model serving in hybrid environments.

## Strengths
- Deep integration with GitHub ecosystem (Issues, PRs, Actions).
- Supported in many popular IDEs (VS Code, JetBrains, Visual Studio, Neovim).
- Support for multiple frontier models, including [GPT-5.5](../ai_knowledge/openai.md) and [Claude 5.1](../providers/anthropic.md).
- Enterprise-grade security and compliance features.

## Limitations
- Requires a paid subscription.
- Cloud-based; code snippets are sent to external servers for inference.
- Native integration in non-VS Code IDEs can sometimes lag behind in features.

## When to use it
- When you want a well-supported, mainstream AI code completion tool.
- When working within the GitHub ecosystem.
- When you need to toggle between different frontier models (GPT-5.5 vs Claude 5.1) for different tasks.

## When not to use it
- When strict local-only code processing is required (consider [Ollama](../../services/ollama.md) + [Continue](continue_dev.md)).
- When you prefer a free alternative (consider [Codeium](codeium.md)).

## Getting started

### Installation
GitHub Copilot is available as an extension for VS Code, Visual Studio, JetBrains, and Neovim.

1. **Install Extension**: Install the "GitHub Copilot" and "GitHub Copilot Chat" extensions from your IDE's marketplace.
2. **Auth**: Sign in to your GitHub account with an active Copilot subscription.
3. **Use**: Start typing to see inline suggestions, or press `Cmd+I` (Mac) / `Ctrl+I` (Windows) to open the inline chat.

### Model Selection (December 2026)
You can now select your preferred model in the Copilot Chat settings:
- **Default**: GPT-5.5 (Optimized for speed and general coding).
- **Advanced Reasoning**: Claude 5.1 (Optimized for complex architectural tasks).

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

### Copilot Extensions API
Developers can build custom extensions for Copilot Chat to integrate internal tools:

```javascript
// Minimal Copilot Extension snippet
export async function handleRequest(request) {
  const { prompt, model } = request;
  // Custom logic to fetch internal context
  const context = await fetchInternalDocs(prompt);
  return {
    message: `Based on internal docs: ${context}`,
    model: 'gpt-5.5'
  };
}
```

### Programmatic Python Setup (Pydantic v2)
Validate enterprise configuration properties and model routing policies:

```python
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class EnterprisePolicy(BaseModel):
    allowed_models: List[str] = Field(default_factory=list, alias="allowedModels")
    allow_telemetry: bool = Field(default=False, alias="allowTelemetry")
    blocked_patterns: List[str] = Field(default_factory=list, alias="blockedPatterns")

class CopilotConfig(BaseModel):
    user_model: Literal["gpt-5.5", "claude-5.1"] = Field(default="gpt-5.5")
    enable_autocomplete: bool = Field(default=True)
    policy: Optional[EnterprisePolicy] = None

    class Config:
        populate_by_name = True

# Validate active policy configuration
config_data = {
    "user_model": "claude-5.1",
    "enable_autocomplete": True,
    "policy": {
        "allowedModels": ["gpt-5.5", "claude-5.1"],
        "allowTelemetry": False,
        "blockedPatterns": ["**/*.key", "**/*.pem"]
    }
}

config = CopilotConfig.model_validate(config_data)
print(f"Validated Model selection: {config.user_model}")
if config.policy:
    print(f"Telemetry allowed: {config.policy.allow_telemetry}")
    print(f"Blocked path patterns count: {len(config.policy.blocked_patterns)}")
```

## Related tools / concepts
- [Codeium](codeium.md) — Fast, free AI coding assistant.
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
- Last reviewed: 2026-12-31
- Confidence: high
