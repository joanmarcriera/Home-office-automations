# Mentat

## What it is
Mentat is an AI coding assistant that runs in your terminal and coordinates with your IDE. It allows you to select files and ask for changes across them.

## What problem it solves
Provides a high-speed, terminal-centric interface for cross-file refactoring, allowing developers to precisely control which files are in the AI's context.

## Where it fits in the pipeline
**Act (Development)**

## Typical use cases (in this homelab / family automation context)
- Applying a consistent change to all Docker Compose files in the homelab repository.
- Quickly adding a new utility function and updating its usages throughout the project.

## Integration points
- **Git**: For tracking changes.
- **LLM APIs**: Supports GPT-4 and other powerful models.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free (Software) + LLM costs.
- **Free tier**: N/A
- **Self-hostable**: Yes

## Strengths
- Extremely fast for developers who prefer the terminal.
- Explicit control over context.
- Minimalistic and efficient.

## Limitations
- Less "conversational" than tools like Cursor.
- Requires some familiarity with terminal workflows.

## Alternatives / Related tools
- **Aider**
- **Cursor**

## Links
- [Official Website](https://mentat.ai)
- [GitHub](https://github.com/Mentat-AI/mentat)
