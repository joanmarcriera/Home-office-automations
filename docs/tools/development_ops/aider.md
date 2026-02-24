# Aider

## What it is
Aider is an AI pair programming tool that runs in your terminal and allows you to chat with your code directly from your git repository.

## What problem it solves
It streamlines the AI coding process by providing a low-friction, terminal-based interface that automatically applies changes to your local files and commits them to git.

## Where it fits in the pipeline
**Reason / Act (Development)**

## Typical use cases (in this homelab / family automation context)
- **Rapid Prototyping**: Quickly building out a new automation script by describing it in the terminal.
- **Documentation Updates**: Asking the AI to document existing home automation code based on its functionality.
- **Refactoring**: Performing targeted code changes across several files with automatic git commits for easy rollbacks.

## Integration points
- **Git**: Deeply integrated for tracking changes and managing history.
- **LLM APIs**: Supports OpenAI, Anthropic, and local models via Ollama or LiteLLM.
- **Editors**: Works alongside any editor (VS Code, Vim, Cursor) since it modifies local files.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free (but requires LLM API keys)
- **Free tier**: N/A (Self-hosted tool)
- **Self-hostable**: Yes

## Strengths
- Extremely fast and efficient workflow.
- High success rate for complex, multi-file edits.
- Excellent management of git context and history.

## Limitations
- Command-line interface may be intimidating for some users.
- Relies on external LLM APIs for the best performance.

## Alternatives / Related tools
- **OpenHands**
- **Cursor**
- **Continue**

## Links
- [Official Website](https://aider.chat/)
- [GitHub](https://github.com/paul-gauthier/aider)
