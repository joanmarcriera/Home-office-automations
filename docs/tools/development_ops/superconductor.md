# Superconductor

## What it is
Superconductor is a multiplayer, cloud-native AI workspace designed for parallel agent orchestration. It allows developers to deploy, monitor, and collaborate with multiple AI agents (e.g., **Claude 4.8**, **GPT-5.5**, and **Llama 4 Maverick**) in a synchronized, sandboxed environment.

## What problem it solves
Managing multiple autonomous agents in a single project often leads to "state drift" and conflicting changes. Superconductor solves this by providing a unified "ground truth" workspace where agents can work in parallel on different branches, with live previews and integrated network sandboxing to prevent unauthorized data exfiltration.

## Where it fits in the stack
**Development & Ops / Multi-Agent Orchestration**. It serves as the "Operating System" for agentic teams, providing the infrastructure for collaboration, resource management, and security.

## Typical use cases
- **Multi-Agent Development**: Assigning a "frontend agent" and a "backend agent" to work on the same feature simultaneously.
- **Automated QA Loops**: Deploying specialized "tester agents" that interact with live previews to identify regressions.
- **Red Teaming**: Running "attacker" agents against a sandboxed version of your infrastructure to find vulnerabilities.
- **Multiplayer Coding**: Humans and AI agents collaborating in the same live workspace with shared state.

## Strengths
- **Parallelism**: Native support for running dozens of agents in parallel without state collisions.
- **Security**: Robust network sandboxing and per-agent resource quotas.
- **Observability**: Real-time "execution graphs" that show how agents are interacting with each other and the code.
- **Live Previews**: Automatically generates ephemeral URLs for web applications, allowing agents to "see" their changes.

## Limitations
- **Cloud-Native Reliance**: Requires a modern Kubernetes or Docker Swarm environment for the sandboxed workspaces.
- **Complexity**: Setting up multi-agent workflows requires understanding of agentic routing and state management.
- **Cost**: Running multiple frontier models in parallel can be expensive.

## When to use it
- When building complex systems that require the coordination of multiple specialized AI agents.
- When security and isolation are top priorities for agentic execution.
- For large-scale refactors or migrations that benefit from parallel processing.

## When not to use it
- For small, single-file projects where a single agent (like **Aider** or **Claude Code**) is sufficient.
- In environments where you cannot deploy cloud-native infrastructure (e.g., restricted local machines).
- If you prefer a simpler, single-agent pair-programming experience.

## Getting started

### Installation
Superconductor is typically deployed via Helm or Docker Compose:

```bash
# Deploy to local Kubernetes cluster
helm install superconductor oci://ghcr.io/superconductor/charts/superconductor
```

### Authentication
Set up your workspace tokens and model API keys in the `superconductor.yaml` config:

```yaml
auth:
  method: oidc
  provider: google
models:
  - id: claude-4.8-opus
    api_key: env:ANTHROPIC_API_KEY
```

### Initializing a Project
Create a new collaborative workspace:

```bash
superconductor init my-parallel-project
cd my-parallel-project
```

## CLI examples

### Launching an Agent Session
Start a new agent session with a specific persona and task:

```bash
superconductor agent run --persona "Backend Architect" --task "Optimize the database schema"
```

### Managing Sandboxes
List and inspect active agent sandboxes:

```bash
superconductor sandbox list
superconductor sandbox logs <sandbox-id>
```

### Synchronizing Files
Force a sync between the local workspace and the Superconductor cloud:

```bash
superconductor sync push
```

## API examples

### Triggering Work from External Signals
Superconductor provides a REST API to trigger agentic work from CI/CD or other events:

```bash
curl -X POST https://api.superconductor.ai/v1/workspaces/ws_123/trigger \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "trigger": "webhook",
    "persona": "QA-Specialist",
    "context": "Failing test in PR #456"
  }'
```

### Workspace Status (Node.js)
```javascript
const sc = require('@superconductor/sdk');
const client = new sc.Client(process.env.SC_TOKEN);

async function checkStatus() {
  const status = await client.workspaces.get('ws_123');
  console.log(`Active Agents: ${status.active_agents}`);
}
```

## Related tools / concepts
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The core design pattern.
- [Model Context Protocol](../automation_orchestration/mcp.md) — For agent tool integration.
- [Claude Code](claude-code.md) — Can be used as a client for Superconductor sandboxes.
- [Aider](aider.md) — For local pair programming.
- [Cursor](cursor.md) — For local IDE-based AI.
- [Plandex](plandex.md) — For plan-first engineering.
- [EKS Auto Mode](../../architecture/infrastructure.md) — Recommended hosting platform.
- [Langfuse](../process_understanding/langfuse.md) — For tracing agent interactions.
- [AgentOps](../process_understanding/agentops.md) — For session monitoring.

## Sources / references
- [Superconductor Official Site](https://superconductor.ai/)
- [GitHub: Superconductor Orchestrator](https://github.com/superconductor/superconductor)
- [Documentation: Multi-Agent Parallelism](https://docs.superconductor.ai/concepts/parallelism)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
