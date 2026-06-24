# Factory AI Droid CLI

## What it is
Factory AI Droid (v2026.5.x+) is an enterprise-grade AI coding agent designed to automate complex, multi-step development workflows. It operates as a "knowledge-aware" orchestrator that utilizes specialized sub-agents ("Droids") to perform domain-specific tasks such as code reviews, security hardening, and feature implementation. Droid leverages the latest frontier models (Claude 4.8, GPT-5.5) and is configured via a `droid.yml` manifest to maintain deep project-specific context.

## What problem it solves
Droid solves the "Execution Gap" in AI-assisted development by moving beyond simple completions to autonomous task completion. It automates repetitive engineering toil—like updating API schemas across multiple layers, performing semantic security scans, and maintaining architectural consistency—allowing human engineers to focus on high-level system design.

## Where it fits in the stack
**Development & Ops**. Droid functions as a CLI-based agentic layer that sits between the developer's intent and the file system/Git. It is frequently integrated into CI/CD pipelines as an autonomous "Junior Engineer" or "Security Auditor."

## Typical use cases
- **Autonomous Feature Development**: Implementing full-stack features from a natural language specification.
- **Continuous Security Hardening**: Identifying and automatically patching vulnerabilities found in static or dynamic analysis.
- **Architectural Enforcement**: Ensuring that new code follows project-defined patterns (e.g., proper dependency injection).
- **Automated Dependency Updates**: Updating library versions and refactoring breaking changes across the codebase.

## Strengths
- **Specialized Multi-Agent System**: Domain-specific Droids (Infra, Security, Frontend) provide higher precision than general-purpose agents.
- **Deep Context Awareness**: The `droid.yml` configuration allows for fine-grained control over the agent's "sight" and "rules."
- **CI/CD Native**: Seamlessly integrates with GitHub Actions, GitLab CI, and Jenkins for automated PR reviews and fixes.
- **Human-in-the-Loop**: Supports interactive "chat" modes for collaborative task refinement and approval gates.

## Limitations
- **Configuration Overhead**: Complex repositories require a well-maintained `droid.yml` to maximize performance.
- **Resource Intensive**: Large-scale autonomous tasks can consume significant LLM tokens and execution time.
- **Proprietary Core**: While the CLI is open, the core reasoning engine is a managed service from Factory AI.

## When to use it
- When you need to automate large-scale refactoring or maintenance tasks across a private codebase.
- In enterprise environments where strict architectural rules must be enforced autonomously.
- To augment a small engineering team with specialized AI agents for security or infrastructure.

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
version: 2.0
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
- [Claude Code](./claude-code.md)
- [Aider](./aider.md)
- [OpenHands](./openhands.md)
- [Cline](../agents/cline.md)
- [Software Factories](../../knowledge_base/patterns/software-factories.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Sourcegraph Cody](./sourcegraph_cody.md)
- [Codeium](./codeium.md)
- [Factory AI Documentation](https://docs.factory.ai/)

## Sources / references
- [Factory AI Website](https://www.factory.ai/)
- [GitHub - Factory-AI/droid-action](https://github.com/Factory-AI/droid-action)
- [Autonomous Development Patterns (2026 Whitepaper)](https://factory.ai/resources/autonomous-patterns-2026)

## Contribution Metadata

- Last reviewed: 2026-06-22
- Confidence: high
