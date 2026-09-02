# GitHub Copilot

## What it is
An AI pair programmer that provides autocomplete-style suggestions as you code. It is powered by OpenAI, Anthropic, and Google models (including GPT-5.6, Claude 5.6, and Gemini 4.0 Ultra) and integrated into various IDEs. It can also be used via CLI, GitHub's web interface, and FastMCP 3.1 Task Protocol agent extensions.

## What problem it solves
Speeds up coding by generating inline code suggestions, reducing the time spent writing boilerplate and looking up API usage. It also provides a chat interface for complex reasoning, refactoring, and debugging directly within the IDE, as well as multi-file workspace indexing and autonomous background PR generation.

## Where it fits in the stack
**Development & Ops**. Provides AI-powered code completion, chat assistance, and FastMCP 3.1 task protocol dispatch as an IDE extension, CLI tool, and GitHub platform agent.

## Typical use cases
- Inline code completion and real-time syntax generation while writing code.
- Generating boilerplate, test suites, and repetitive architectural patterns.
- CLI-based command explanation, script generation, and shell automation.
- Full-project multi-file reasoning via the `@workspace` agent and FastMCP 3.1 context tools.
- **Enterprise Inference**: Integration with [NVIDIA NIM](../providers/nvidia.md) (NVIDIA Inference Microservices) for self-hosted, high-performance model serving in hybrid enterprise environments.

## Strengths
- Deep integration with GitHub ecosystem (Issues, PRs, Actions, and Copilot Workspace).
- Supported in many popular IDEs (VS Code, JetBrains, Visual Studio, Neovim, and Xcode).
- Support for multiple frontier models, including [GPT-5.6](../ai_knowledge/openai.md), [Claude 5.6](../providers/anthropic.md), and [Gemini 4.0 Ultra](../ai_knowledge/gemini.md).
- Enterprise-grade security, IP indemnity, and compliance features.

## Limitations
- Requires a paid subscription (Copilot Individual, Business, or Enterprise).
- Cloud-based by default; code snippets are sent to external servers for inference unless using self-hosted NIM endpoints.
- Native integration in non-VS Code IDEs can sometimes lag behind in specialized agentic features.

## When to use it
- When you want a well-supported, mainstream AI code completion and workspace agent tool.
- When working within the GitHub ecosystem and leveraging automated PR reviews and workspace tasks.
- When you need to toggle between different frontier models (GPT-5.6 vs Claude 5.6 vs Gemini 4.0 Ultra) for different software tasks.

## When not to use it
- When strict local-only offline code processing is required (consider [Ollama](../../services/ollama.md) + [Continue](continue_dev.md)).
- When you prefer a fully open-source alternative (consider [Codeium](codeium.md)).

## Getting started

### Installation
GitHub Copilot is available as an extension for VS Code, Visual Studio, JetBrains, and Neovim, or via the GitHub CLI:

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
3. **Use**: Start typing to see inline suggestions, or press `Cmd+I` (Mac) / `Ctrl+I` (Windows) to open the inline chat.

### Model Selection
You can select your preferred model in the Copilot Chat settings:
- **Default (Fast Code Completion)**: GPT-5.6 (Optimized for low-latency inline completions).
- **Advanced Reasoning & Architecture**: Claude 5.6 (Optimized for complex refactoring and multi-file logic).
- **Multimodal & Code Search**: Gemini 4.0 Ultra (Optimized for deep visual documentation and cross-repo context).

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

### Copilot Extensions API with FastMCP 3.1 Task Protocol
Developers can build custom FastMCP 3.1 extensions for Copilot Chat to integrate internal tools and databases:

```javascript
// FastMCP 3.1 Copilot Extension snippet
export async function handleFastMCPTaskRequest(request) {
  const { prompt, model, taskContext } = request;
  // Custom logic to fetch internal context via FastMCP protocol
  const context = await fetchInternalDocs(prompt, taskContext.taskId);
  return {
    message: `Based on FastMCP task state and internal docs: ${context}`,
    model: 'claude-5.6',
    taskStatus: 'completed'
  };
}
```

### Programmatic Python Setup (Pydantic v2)
Validate enterprise configuration properties, model routing policies, and FastMCP task protocol settings using strict **Pydantic v2**:

```python
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class FastMCPTaskConfig(BaseModel):
    task_protocol_version: str = Field(default="3.1", alias="taskProtocolVersion")
    allow_background_execution: bool = Field(default=True, alias="allowBackgroundExecution")
    max_tokens_per_task: int = Field(default=128000, alias="maxTokensPerTask")

class EnterprisePolicy(BaseModel):
    allowed_models: List[str] = Field(default_factory=list, alias="allowedModels")
    allow_telemetry: bool = Field(default=False, alias="allowTelemetry")
    blocked_patterns: List[str] = Field(default_factory=list, alias="blockedPatterns")

class CopilotConfig(BaseModel):
    user_model: Literal["gpt-5.6", "claude-5.6", "gemini-4.0-ultra"] = Field(default="gpt-5.6")
    enable_autocomplete: bool = Field(default=True)
    policy: Optional[EnterprisePolicy] = None
    mcp_config: Optional[FastMCPTaskConfig] = Field(default=None, alias="mcpConfig")

    class Config:
        populate_by_name = True

# Validate active policy configuration
config_data = {
    "user_model": "claude-5.6",
    "enable_autocomplete": True,
    "policy": {
        "allowedModels": ["gpt-5.6", "claude-5.6", "gemini-4.0-ultra"],
        "allowTelemetry": False,
        "blockedPatterns": ["**/*.key", "**/*.pem"]
    },
    "mcpConfig": {
        "taskProtocolVersion": "3.1",
        "allowBackgroundExecution": True,
        "maxTokensPerTask": 128000
    }
}

config = CopilotConfig.model_validate(config_data)
print(f"Validated Model selection: {config.user_model}")
if config.policy:
    print(f"Telemetry allowed: {config.policy.allow_telemetry}")
    print(f"Blocked path patterns count: {len(config.policy.blocked_patterns)}")
if config.mcp_config:
    print(f"FastMCP Version: {config.mcp_config.task_protocol_version}")
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
- Last reviewed: 2027-01-07
- Confidence: high
