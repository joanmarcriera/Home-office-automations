# Prompt Requests: Post-PR Development Workflows

This document outlines the transition from traditional Git-based "Pull Requests" to agent-centric "Prompt Requests" and reputation-based systems for post-human development.

## Overview

The "RIP Pull Requests (2005-2026)" analysis highlights a fundamental shift in software engineering. As AI agents handle an increasing percentage of code generation and modification, traditional human-centric collaboration tools like Pull Requests (PRs) and Code Reviews are being superseded by workflows optimized for speed, safety, and agentic autonomy.

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

## Sources / References
- [[AINews] RIP Pull Requests (2005-2026) (Latent Space)](https://www.latent.space/p/ainews-rip-pull-requests-2005-2026)
- [Building for Trillions of Agents (Aaron Levie)](https://x.com/levie/status/2030714592238956960)

## Contribution Metadata
- Last reviewed: 2026-04-24
- Confidence: high
