# Anti-Gravity

## What it is
An experimental AI engineering framework from Google that provides high-level abstractions for building autonomous agents capable of navigating and modifying complex software systems.

## What problem it solves
Simplifies the development of autonomous coding agents by offering pre-built abstractions, reducing the effort needed to build agents that can understand and refactor large codebases.

## Where it fits in the stack
**Development & Ops**. Serves as a framework for building autonomous software engineering agents.

## Typical use cases
- Building autonomous agents that navigate complex software systems
- Automated codebase refactoring via agent orchestration
- Prototyping AI-driven development workflows

## Strengths
- High-level abstractions reduce boilerplate for agent development
- Focused on autonomous navigation and modification of software systems
- Native integration with Google's development ecosystem

## Limitations
- Experimental status; not production-ready
- Limited community and documentation compared to established frameworks
- Primarily accessible through waitlists and developer previews

## When to use it
- When building custom autonomous agents for software engineering tasks
- When exploring agent-based approaches to codebase management
- When participating in Google's developer preview programs

## When not to use it
- When you need a stable, production-grade agent framework (use [OpenHands](../agents/openhands.md) or [CrewAI](../frameworks/crewai.md))
- When general-purpose LLM orchestration (e.g., [LangChain](../ai_knowledge/langchain.md)) is sufficient

## Agent Mission Architecture
In Anti-Gravity, work is organized into "Missions". A Mission consists of:
1. **Goal**: The high-level objective in natural language.
2. **Surface Context**: The relevant parts of the codebase the agent has "sight" of.
3. **Execution Steps**: A series of autonomous actions taken by the agent to reach the goal.

## Conceptual Workflow
- **Manager Surface**: Used for spawning and observing autonomous agents.
- **Editor View**: A familiar IDE experience for synchronous AI-assisted coding.
- **Mission Control**: The central interface for defining "Missions" (long-horizon tasks).

## Defining a Mission
Missions are typically defined in natural language via the Manager Surface:
```text
Mission: Implement a new REST endpoint for user profile updates.
1. Create the Pydantic schema in models/user.py.
2. Implement the route in api/routes/users.py.
3. Launch the server in the terminal to verify.
4. Use the browser to test the API docs (Swagger).
```

## Rule and Workflow Customization
Anti-Gravity allows defining project-level constraints and standards via "Rules" that agents must follow during execution, similar to [Cline's .clinerules](cline.md).

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [CrewAI](../frameworks/crewai.md)
- [OpenHands](../agents/openhands.md)
- [Claude Code — Project Setup Guide](claude-code-setup.md)
- [Cline](cline.md)
- [Windsurf](./windsurf.md)
- [Cursor](./cursor.md)
- [Aider](./aider.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / references
- [Build with Google Anti-Gravity (Google Developers Blog)](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
- [Getting Started with Google Anti-Gravity (Codelabs)](https://codelabs.developers.google.com/getting-started-google-antigravity)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
