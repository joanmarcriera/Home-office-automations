# Factory AI Droid CLI

## What it is
Factory AI Droid CLI (v2026.7.x+) is an enterprise-grade AI coding orchestrator designed to automate complex, multi-step development workflows. It operates as a "knowledge-aware" orchestrator that utilizes specialized sub-agents ("Droids") configured via a `droid.yml` manifest to maintain deep project-specific context. Built for the modern developer workspace, Droid CLI natively supports frontier reasoning and foundational models (Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6) and features Model Context Protocol (MCP 3.0/3.1) integration to dynamically discover tools, run secure sandboxed workflows, and execute stateful long-horizon coding tasks.

## What problem it solves
Droid solves the "Execution Gap" in AI-assisted development by moving beyond simple completions to autonomous task completion. It automates repetitive engineering toil—such as updating API schemas across multiple layers, performing semantic security scans, managing containerized dependencies, and maintaining architectural consistency—allowing human engineers to focus on high-level system design. By enforcing declarative constraints specified in the repo, it prevents context drift and ensures all changes pass repository build rules autonomously.

## Where it fits in the stack
**Development & Ops**. Droid functions as a CLI-based agentic layer that sits between the developer's intent and the file system/Git. It is frequently integrated into local development terminals, specialized agent IDEs, and CI/CD pipelines as an autonomous "Junior Engineer" or "Security Auditor."

## Typical use cases
- **Autonomous Feature Development**: Implementing full-stack features from a natural language specification or a tracking ticket.
- **Continuous Security Hardening**: Identifying and automatically patching vulnerabilities found in static or dynamic analysis, securely running local test runners to verify patches.
- **Architectural Enforcement**: Ensuring that new code strictly follows project-defined patterns (e.g., proper dependency injection, specific design patterns, type safety).
- **Automated Dependency Updates**: Safely upgrading library versions, refactoring breaking changes across the codebase, and verifying build and test suite status.
- **MCP Tool Interoperability**: Exposing local development tools to frontier models or executing tasks by querying external MCP databases.

## Strengths
- **Specialized Multi-Agent System**: Domain-specific Droids (Infra, Security, Frontend, Backend) provide higher precision than general-purpose agents.
- **Deep Context Awareness**: The `droid.yml` configuration allows for fine-grained control over the agent's "sight", workspace boundaries, and architectural rules.
- **CI/CD Native**: Seamlessly integrates with GitHub Actions, GitLab CI, and Jenkins for automated pull request reviews, test-driven debugging, and autonomous hotfixes.
- **Human-in-the-Loop Steering**: Supports interactive "chat" and approval modes for collaborative task refinement and approval gates before committing changes.
- **Native MCP 3.0/3.1 Integration**: Integrates both as an MCP client (consuming remote or local servers) and as an MCP server to expose its internal file-editing and agent execution tools.

## Limitations
- **Configuration Overhead**: Complex repositories require a well-maintained `droid.yml` to maximize performance and prevent the agent from getting lost in massive codebases.
- **Resource Intensive**: Large-scale autonomous tasks can consume significant LLM tokens and execution time due to iterative reasoning loops and self-correction cycles.
- **Proprietary Core**: While the CLI is open, the core advanced reasoning and task decomposition engine is a managed service from Factory AI.

## When to use it
- When you need to automate large-scale refactoring, compliance, or maintenance tasks across a private codebase.
- In enterprise environments where strict architectural rules, coding standards, and security controls must be enforced autonomously.
- To augment engineering teams with specialized AI agents for security, documentation, or infrastructure automation.
- In environments utilizing Model Context Protocol (MCP) to seamlessly link tools and servers under a unified agentic loop.

## When not to use it
- For simple, single-file edits or quick autocomplete where [Aider](./aider.md) or [Cline](../agents/cline.md) is faster and more lightweight.
- In air-gapped environments that cannot reach the Factory AI inference plane or external model gateways.
- If you prefer a fully open-source, locally-hosted agent framework (see [OpenHands](./openhands.md)).

## Getting started
Droid is installed via `npm` or `brew` and requires a Factory AI account and API credentials.

### 1. Installation
```bash
npm install -g @factory-ai/droid
```

### 2. Configuration (`droid.yml`)
Create a manifest in your repository root to configure your project scope and the specialized droids:
```yaml
version: 3.0
project:
  name: "Service-Mesh-Core"
  stack: ["typescript", "rust", "kubernetes"]
  standards: "docs/standards-and-conventions.md"
droids:
  - name: "security-droid"
    type: "auditor"
    scope: ["src/auth/**", "src/crypto/**"]
    mcp_servers: ["http://localhost:8080/mcp"]
  - name: "refactor-droid"
    type: "coder"
    rules: ["Use functional components only", "Prefer async/await over promises"]
```

### 3. Login and Initialization
Authenticate the CLI client:
```bash
droid login
```

Initialize Droid configuration:
```bash
droid init
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
- **Interactive session with custom context**:
  ```bash
  droid chat --context "current-sprint"
  ```
- **Analyze and review PR changes**:
  ```bash
  droid review --pr 452 --detailed
  ```

## API examples
Droid can be triggered programmatically via its Node.js SDK for custom automation:

```javascript
const { DroidClient } = require('@factory-ai/sdk');

const client = new DroidClient({ apiKey: process.env.FACTORY_API_KEY });

async function runAudit() {
  const task = await client.tasks.create({
    droid: 'security-droid',
    input: 'Perform a deep scan for SQL injection in the data-layer module.',
    autoFix: true
  });

  console.log(`Task started: ${task.id}`);

  const result = await task.waitForCompletion();
  console.log(`Audit complete. Found ${result.issues.length} issues.`);
}

runAudit();
```

## Related tools / concepts
- [Claude Code](./claude-code.md) — Interactive terminal-native developer agent.
- [Aider](./aider.md) — Terminal-based Git-native pair programming tool.
- [OpenHands](./openhands.md) — Full-featured autonomous agent platform and workspace environment.
- [Cline](../agents/cline.md) — Autonomous coding agent built for IDE integration.
- [Sourcegraph Cody](./sourcegraph_cody.md) — Code intelligence platform and contextual agent.
- [Codeium](./codeium.md) — AI-native developer productivity and completion platform.
- [Anti-Gravity](./anti_gravity.md) — Google's enterprise agentic execution and sandboxing platform.
- [Terminus 2](./terminus-2.md) — Tmux-based execution loop and terminal automation environment.
- [Windsurf](./windsurf.md) — Agentic developer IDE powered by flow-based architectures.
- [Cloud Code](./cloud_code.md) — Kubernetes, GKE, and cloud-native service IDE development tools.
- [Custom Agents](./custom_agents.md) — Lightweight, SSH-capable task execution loops.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — System designs and architectural patterns of AI software engineering pools.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Task decomposition, routing, and multi-agent coordination.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — The universal standard for connecting LLMs to external systems.

## Sources / references
- [Factory AI Website](https://www.factory.ai/)
- [GitHub - Factory-AI/droid-action](https://github.com/Factory-AI/droid-action)
- [Autonomous Development Patterns (2026 Whitepaper)](https://factory.ai/resources/autonomous-patterns-2026)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
