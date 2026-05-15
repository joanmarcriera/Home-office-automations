# Plandex

## What it is
Plandex is an open-source AI coding agent designed to handle large projects and complex, real-world tasks. It operates through a terminal-based REPL and is capable of full autonomy, including loading relevant files, planning and implementing changes, executing commands, and automatically debugging.

## What problem it solves
It addresses the limitations of simpler AI tools that struggle with large codebases or multi-step tasks. Plandex reduces the manual effort of managing context and applying coordinated edits across many files, providing a structured workflow for complex refactoring and feature development.

## Where it fits in the stack
**Development & Ops / AI Coding Agent**. It sits between simple completion tools (like Copilot) and fully managed AI platforms, providing a developer-centric, terminal-native environment for agentic coding.

## Typical use cases
- **Complex Refactoring**: Implementing changes that require understanding logic across multiple directories.
- **Automated Debugging**: Running tests, identifying failures, and iterating on fixes autonomously.
- **Codebase Exploration**: Loading entire directories into context to understand how a specific module interacts with the system.
- **Scaffolding New Projects**: Generating initial code structures based on high-level architecture plans.

## Getting started

### Installation
Plandex can be installed with a single command:

```bash
curl -sL https://plandex.ai/install.sh | bash
```

### Configuration
Set your provider API keys (e.g., OpenRouter, OpenAI, or Anthropic):

```bash
export OPENROUTER_API_KEY='your-api-key'
# Or for direct providers
export ANTHROPIC_API_KEY='your-key'
```

### Basic Workflow
1. **Initialize**: Navigate to your project directory and start the REPL.
   ```bash
   plandex
   ```
2. **Load Context**: Tell Plandex which files or directories to focus on.
   ```bash
   pdx load src/ lib/
   ```
3. **Create a Plan**: Describe your task in chat mode, then switch to "tell" mode to generate a formal plan.
4. **Review & Execute**: Plandex will implement the changes. You can review the diffs and apply them to your files.

## Strengths
- **Resilient to Scale**: Designed specifically to handle large projects where other tools might fail.
- **Fine-grained Control**: Offers developers the ability to step through plans and review changes before application.
- **Self-Hostable**: Can be run entirely locally using Docker, providing privacy and control over the serving stack.
- **Autonomous Debugging**: Capable of running terminal commands and iterating on its own output based on error messages.

## Limitations
- **Learning Curve**: The REPL-based workflow and specific commands (`load`, `plan`, `apply`) require some initial familiarization.
- **API Costs**: High-autonomy tasks can lead to significant token consumption, especially with large file contexts.
- **Windows Support**: Requires WSL; it does not natively support the Windows CMD or PowerShell environments.

## When to use it
- When working on large, complex codebases that require multi-file awareness.
- When you want an autonomous agent that can run and verify its own code changes.
- If you prefer a CLI-first workflow and want to self-host your AI coding infrastructure.

## When not to use it
- For quick, single-line code completions where an IDE extension is more convenient.
- If you are not comfortable working in a terminal environment or WSL.
- When working on very small scripts where the overhead of planning/loading context is unnecessary.

## Related tools / concepts
- [Aider](aider.md): A popular terminal-based AI pair programmer.
- [Mentat](mentat.md): An AI tool for coordinating edits across multiple files.
- [OpenHands](openhands.md): An open-source autonomous agent platform.
- [Claude Code](claude-code.md): Anthropic's terminal coding assistant.
- [OpenRouter](../ai_knowledge/openrouter.md): Often used as the primary provider for Plandex.
- [LocalAI](../infrastructure/localai.md): A provider for self-hosting models that Plandex can utilize.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md): Patterns for selecting the best model for Plandex tasks.

## Sources / References
- [Official Website](https://plandex.ai/)
- [Plandex Documentation](https://docs.plandex.ai/)
- [Plandex GitHub Repository](https://github.com/plandex-ai/plandex)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
