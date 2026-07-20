# Factory AI Droid CLI

## What it is
Factory AI Droid (v2026.7.x+) is an enterprise-grade AI coding agent designed to automate complex, multi-step development workflows. It operates as a "knowledge-aware" orchestrator that utilizes specialized sub-agents ("Droids") to perform domain-specific tasks such as code reviews, security hardening, and feature implementation. Droid leverages the latest July 2026 frontier models (Claude 5.1, GPT-5.5, Llama 4, Gemma 3, and Qwen 3.6) and is configured via a `droid.yml` manifest to maintain deep project-specific context, while natively integrating with the Model Context Protocol (MCP 3.0/3.1) standard to extend its execution capabilities.

## What problem it solves
Droid solves the "Execution Gap" in AI-assisted development by moving beyond simple completions to autonomous task completion. It automates repetitive engineering toil—like updating API schemas across multiple layers, performing semantic security scans, and maintaining architectural consistency—allowing human engineers to focus on high-level system design. It eliminates brittle tool-calling setups by standardizing agentic actions via stream-aware MCP protocols and secure sandbox execution environments.

## Where it fits in the stack
**Development & Ops**. Droid functions as a CLI-based agentic layer that sits between the developer's intent and the file system/Git. It is frequently integrated into CI/CD pipelines as an autonomous "Junior Engineer" or "Security Auditor." It can also act as an MCP 3.0 client, interacting with external databases, sandboxed runtimes, or custom tools exposed by other parts of the infrastructure.

## Typical use cases
- **Autonomous Feature Development**: Implementing full-stack features from a natural language specification.
- **Continuous Security Hardening**: Identifying and automatically patching vulnerabilities found in static or dynamic analysis.
- **Architectural Enforcement**: Ensuring that new code follows project-defined patterns (e.g., proper dependency injection).
- **Automated Dependency Updates**: Updating library versions and refactoring breaking changes across the codebase.
- **MCP-Enabled Workspace Navigation**: Querying external documentation, API definitions, or local Docker environments via standard MCP 3.0 server interfaces.

## Strengths
- **Specialized Multi-Agent System**: Domain-specific Droids (Infra, Security, Frontend) provide higher precision than general-purpose agents.
- **Deep Context Awareness**: The `droid.yml` configuration allows for fine-grained control over the agent's "sight" and "rules."
- **CI/CD Native**: Seamlessly integrates with GitHub Actions, GitLab CI, and Jenkins for automated PR reviews and fixes.
- **Human-in-the-Loop**: Supports interactive "chat" modes for collaborative task refinement and approval gates.
- **MCP 3.0/3.1 Compliance**: Fully compatible with Model Context Protocol servers, allowing standard-based extension of the agent's toolbox.

## Limitations
- **Configuration Overhead**: Complex repositories require a well-maintained `droid.yml` to maximize performance.
- **Resource Intensive**: Large-scale autonomous tasks can consume significant LLM tokens and execution time.
- **Proprietary Core**: While the CLI is open-source, the core reasoning engine and agent orchestration loop are managed services from Factory AI.

## When to use it
- When you need to automate large-scale refactoring or maintenance tasks across a private codebase.
- In enterprise environments where strict architectural rules must be enforced autonomously.
- To augment a small engineering team with specialized AI agents for security or infrastructure.
- When you want an agent that natively integrates with MCP 3.0 servers to control external sandboxes.

## When not to use it
- For simple, single-file edits where [Aider](./aider.md) or [Cline](../agents/cline.md) is faster.
- In air-gapped environments that cannot reach the Factory AI inference plane.
- If you prefer a fully open-source, locally-hosted agent framework (see [OpenHands](./openhands.md)).

## Getting started
Droid is installed via `npm` or `brew` and requires a Factory AI account.

### 1. Installation
```bash
npm install -g @factory-ai/droid
```

### 2. Configuration (`droid.yml`)
Create a manifest in your repository root:
```yaml
version: 3.0
project:
  name: "Service-Mesh-Core"
  stack: ["typescript", "rust", "kubernetes"]
droids:
  - name: "security-droid"
    type: "auditor"
    scope: ["src/auth/**", "src/crypto/**"]
  - name: "refactor-droid"
    type: "coder"
    rules: ["Use functional components only", "Prefer async/await over promises"]
mcp_servers:
  - name: "filesystem-mcp"
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
```

### 3. Login
```bash
droid login
```

## CLI examples
- **Run a specific Droid**:
  ```bash
  droid run security-droid --target "./src" --fix
  ```
- **Initiate a build task**:
  ```bash
  droid build "Implement the new OAuth2 flow described in docs/auth-spec.md"
  ```
- **Interactive session**:
  ```bash
  droid chat --context "current-sprint"
  ```
- **Analyze PR changes**:
  ```bash
  droid review --pr 452 --detailed
  ```
- **Manage MCP Servers**:
  ```bash
  droid mcp list
  ```

## API examples
Droid can be triggered programmatically via its Node.js SDK for custom automation:

```javascript
// Modern Node.js ES Modules usage of @factory-ai/sdk
import { DroidClient } from '@factory-ai/sdk';

const client = new DroidClient({ apiKey: process.env.FACTORY_API_KEY });

async function runAudit() {
  const task = await client.tasks.create({
    droid: 'security-droid',
    input: 'Perform a deep scan for SQL injection in the data-layer module.',
    autoFix: true,
    mcp_context: {
      enabled: true,
      servers: ['filesystem-mcp']
    }
  });

  console.log(`Task started: ${task.id}`);

  const result = await task.waitForCompletion();
  console.log(`Audit complete. Found ${result.issues.length} issues.`);
}

runAudit();
```

## Related tools / concepts
- [Aider](./aider.md) — Terminal-based collaborative coding partner.
- [Anti-Gravity](./anti_gravity.md) — Google's enterprise agent orchestration and sandbox framework.
- [Claude Code](./claude-code.md) — Anthropic's interactive developer agent CLI.
- [Codeium](./codeium.md) — AI-powered IDE developer productivity platform.
- [Cline](../agents/cline.md) — VS Code autonomous agentic coding assistant.
- [OpenHands](./openhands.md) — Flexible open-source software engineering agent workspace.
- [Sourcegraph Cody](./sourcegraph_cody.md) — Multi-repository reasoning and context retrieval platform.
- [Terminus 2](./terminus-2.md) — Terminal-native tmux bridging AI agent and baseline.
- [Windsurf](./windsurf.md) — Flow-based agentic development environment and IDE.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Recurring design patterns for multi-agent systems.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — System designs and standards for connecting models to tools.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Industrialized development paradigms powered by LLM loops.

## Sources / references
- [Factory AI Website](https://www.factory.ai/)
- [GitHub - Factory-AI/droid-action](https://github.com/Factory-AI/droid-action)
- [Autonomous Development Patterns (2026 Whitepaper)](https://factory.ai/resources/autonomous-patterns-2026)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
