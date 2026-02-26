# OpenHands

## What it is
OpenHands (formerly OpenDevin) is an open-source platform for building autonomous AI agents for software engineering.

## What problem it solves
It provides a full agentic environment with a terminal, browser, and file editor, allowing models to solve complex engineering tasks that require more than just file edits.

## Where it fits in the stack
**Agent / Orchestration**. It is a heavy-duty agent platform that can perform multi-step, autonomous tasks.

## Architecture overview
Client-server architecture. Usually runs in a Docker container to provide a sandboxed environment where the agent can safely execute shell commands and browse the web.

## Typical workflows
- **End-to-end Feature Development**: "Implement a new dashboard page, test it in the browser, and fix any CSS issues."
- **Automated Bug Hunting**: "Find and fix the memory leak in the background worker."
- **Tool Building**: "Write a script to migrate the database and run it against the dev instance."

## Strengths
- **High Autonomy**: Can iterate through multiple steps (Plan -> Act -> Observe) without constant human input.
- **Multimodal**: Can use a browser to verify changes or gather information.
- **Sandboxed**: Runs in Docker, protecting the host system from potentially harmful commands.

## Limitations
- **Complexity**: Heavier to set up and run than simpler tools like Aider.
- **Resource Intensive**: Requires significant local resources or a remote server to run the Docker environment.
- **Experimental**: Some features are still in active development and may be less stable.

## When to use it
- For complex, multi-step tasks that require high autonomy.
- When the agent needs to verify its work via a browser or a running application.
- When you want a fully sandboxed execution environment.

## When not to use it
- For simple file edits where Aider would be faster.
- On machines with limited RAM/CPU for Docker.

## Security considerations
- **Sandbox Escape**: While Docker provides isolation, be cautious when giving agents high-level permissions.
- **API Costs**: Highly autonomous agents can consume many tokens quickly.

## Links to related pages
- [Aider](aider.md)
- [Custom Agents](custom_agents.md)
- [OpenAI](../ai_knowledge/openai.md)

## Sources / References

- [Reference](https://github.com/All-Hands-AI/OpenHands)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
