# Prompt Requests: Post-PR Development Workflows

This document outlines the transition from traditional Git-based "Pull Requests" to agent-centric "Prompt Requests" and reputation-based systems for post-human development.

## What it is

The "RIP Pull Requests (2005-2026)" analysis highlights a fundamental shift in software engineering. As AI agents handle an increasing percentage of code generation and modification, traditional human-centric collaboration tools like Pull Requests (PRs) and Code Reviews are being superseded by workflows optimized for speed, safety, and agentic autonomy.

## What problem it solves

- **The Human Bottleneck**: Traditional PRs require human review, which is slow compared to the speed at which agents can generate code.
- **Merge Conflicts**: Agent-generated code often drifts from the main branch; Prompt Requests focus on the *intent* (the prompt), allowing the agent to regenerate against the latest main branch.
- **Spec-Code Divergence**: Ensures the source of truth is the high-level specification or prompt, not just the resulting lines of code.

## Where it fits in the stack

**Workflow Pattern**. Operates at the **Development / CI layer**. It replaces or augments the standard GitHub Flow (branch -> commit -> PR -> merge) with a Spec Flow (spec/prompt -> agent execution -> validation -> reputation-based auto-merge).

## Typical use cases

- **Automated Bug Fixing**: Providing a stack trace and asking an agent to "fix this and update the test suite."
- **Feature Expansion**: Adding a new API endpoint based on an existing schema and pattern.
- **Large-scale Refactoring**: Migrating a codebase from one library version to another by updating the global "coding standards" prompt.

## Strengths

- **High Architectural Alignment**: Agents follow the provided prompt strictly, ensuring consistency across a large codebase.
- **Reduced Human Labor**: Removes the need for line-by-line review for boilerplate or standard tasks.
- **Durable Intent**: The "Prompt Request" serves as documentation for *why* a change was made, often more clearly than a commit message.

## Limitations

- **Spec Fidelity**: Requires extremely clear and high-quality prompts/specifications to avoid "hallucinated" features.
- **Sandboxing Requirements**: Demands robust, isolated execution environments (like E2B or Modal) to safely run and test agentic code.
- **Reputation Complexity**: Building a reliable system to "trust" agent output without human eyes is technically challenging.

## When to use it

- For **boilerplate-heavy tasks** or repetitive pattern application.
- When working in **sandboxed environments** where automated tests provide 100% coverage confidence.
- In **high-velocity teams** where humans focus on architecture and agents focus on implementation.

## When not to use it

- **Critical Security Kernels**: Any code where a single logic error could lead to a major breach still requires human "Deep Review".
- **Ambiguous UI/UX Polish**: Tasks requiring subjective human aesthetic judgment.
- **Low Test Coverage**: If you cannot prove the code is correct via automation, do not use autonomous Prompt Requests.

## From Pull Requests to Prompt Requests

The "human bottleneck" in Git-based workflows is becoming evident. The emerging "Prompt Request" pattern suggests:
- **Direct Prompting**: Maintainers modify the *prompt* or *specification* rather than the resulting code.
- **Auto-Regeneration**: The agent regenerates the code based on the updated prompt, eliminating manual merge conflicts.
- **Maintainer Focus**: Shifts from reviewing code lines to refining architectural intent and constraints.

## Reputation-Based Systems
To handle untrusted or high-volume agentic contributions, "reputation" systems are replacing manual reviews:
- **Mitchell Hashimoto's / Amp Code Patterns**: Moving toward systems where code contributions are evaluated based on the submitter's (or agent's) historical reliability and automated safety checks.
- **Reputation Scores**: Agents earn trust through successful deployments, passing test suites, and adhering to security protocols.

## Agent-to-Agent Collaboration
Agents are increasingly designed for a "software that agents want" paradigm:
- **Stateless Orchestration + Stateful Workspaces**: Converging on patterns where stateless agents operate in durable, isolated sandbox environments (e.g., OpenAI Agents SDK, Cloudflare Project Think).
- **File-as-Bus**: Using durable workspace artifacts (files) as the communication medium between specialized agents rather than complex API handshakes.

## Security Implications
The shift to "Prompt Requests" addresses key security risks:
- **Malicious PRs**: It is harder to slip malicious code into a prompt modification than into an innocent-looking 1,000-line PR.
- **Isolated Execution**: Mandatory use of sandboxed environments (E2B, Modal, Cloudflare) for all agentic code execution.

## Related tools / concepts

- [Agentic Workflows](agentic-workflows.md) — the broader framework for agent-led development.
- [Agent Skills Best Practices](skills-best-practices.md) — authoring the modules that Prompt Requests trigger.
- [Self-healing Agent Research](../self-healing-agent-research.md) — automated remediation triggered by Prompt Requests.
- [Claude Code](../../tools/development_ops/claude-code.md) — terminal-based agent that uses these patterns.
- [Context7](../../tools/development_ops/context7.md) — providing fresh context to Prompt Requests.
- [OpenClaw](../../tools/development_ops/openclaw.md) — runtime for executing agentic prompts.
- [LLMFit](../../tools/development_ops/llmfit.md) — benchmarking the models used in Prompt Request loops.

## Sources / References
- [[AINews] RIP Pull Requests (2005-2026) (Latent Space)](https://www.latent.space/p/ainews-rip-pull-requests-2005-2026)
- [Building for Trillions of Agents (Aaron Levie)](https://x.com/levie/status/2030714592238956960)

## Contribution Metadata
- Last reviewed: 2026-04-24
- Confidence: high
