# Playbook: AI-Assisted Dev Workflow

## Objective
Accelerate homelab infrastructure development using a hierarchy of AI coding agents.

## Pre-requisites
- [VS Code](../tools/development_ops/vscode.md) or [Cursor](../tools/development_ops/cursor.md)
- [Aider](../tools/development_ops/aider.md)
- [Ollama](../services/ollama.md)
- [Jules (Google)](../tools/ai_knowledge/jules.md)

## Step-by-Step Flow
1.  **Drafting**: Use Cursor to outline a new automation script in Python.
2.  **Implementation**: Use Aider to perform targeted code generation for complex functions.
3.  **Refactoring**: Assign [Jules](../tools/ai_knowledge/jules.md) to refactor the repository asynchronously, focusing on best practices and unit test coverage.
4.  **Verification**: [Anti-Gravity](../tools/development_ops/anti_gravity.md) runs a plan-code-test loop to ensure the new script doesn't break existing Home Assistant configurations.
5.  **Audit**: Review AI-generated commits before merging into the `main` branch.

## Data Contract
- **Input**: Natural language prompt + Codebase context.
- **Output**: Git diff + Commit message.

## Failure Modes & Recovery
- **Hallucination**: AI generates non-existent API calls.
    - *Detection*: Linter or compiler errors.
    - *Recovery*: Feed error logs back to Aider for automated fixing.
- **Context Limit**: Large repositories exceed LLM context window.
    - *Recovery*: Use Aider's repository map feature.

## Local-First Setup
A fully local-first development workflow ensures complete privacy and zero per-token costs.

- **Reasoning**: Use `Qwen3-Coder-Next` via [Ollama](../services/ollama.md). This model is highly optimized for coding tasks and can be run on consumer hardware with 16GB+ VRAM.
- **Agent**: [Aider](../tools/development_ops/aider.md) configured to use the local Ollama endpoint.
- **Context Management**: Leverage Aider's **repository map** to provide the LLM with a concise overview of your codebase, ensuring high relevance while staying within local context limits.
- **Verification**: Run local unit tests and linting autonomously after each AI-generated change.

## Token-Efficiency & Value
- **Differential Context**: Only send files that are directly related to the task. Use Aider's `/add` and `/drop` commands to manage context manually if the auto-selection is too broad.
- **Commit Summaries**: Use the LLM to generate concise git commit messages, but review them to ensure they provide technical value without fluff.
- **Local Routing**: Use [LiteLLM](../services/litellm.md) to route simple tasks (like docstring generation) to smaller, faster local models while reserving larger models for complex logic.

## Variants
- **Cloud-Based**: Use GPT-4o via [LiteLLM](../services/litellm.md) for better reasoning.
- **Privacy-First**: Use local Llama-3-Coder models in Ollama.

## Case Studies & References
- [How we rebuilt Next.js with AI in one week](https://blog.cloudflare.com/vinext) (Cloudflare's experience with AI-assisted rebuilding of components).


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://blog.cloudflare.com/vinext
