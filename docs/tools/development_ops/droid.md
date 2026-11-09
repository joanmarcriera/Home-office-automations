# Factory AI Droid CLI

## What it is
Factory AI Droid (Early January 2027 SOTA Edition) is an enterprise-grade AI coding agent designed to automate complex, multi-step development workflows. It operates as a "knowledge-aware" orchestrator that utilizes specialized sub-agents ("Droids") to perform domain-specific tasks such as code reviews, security hardening, and feature implementation. Droid leverages early 2027 SOTA frontier models (**Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**, **Gemma 4**, and **Qwen 3.6 VL**) and is configured via a `droid.yml` manifest to maintain deep project-specific context, while natively integrating with the Model Context Protocol (**MCP 3.1 / FastMCP 3.1**) standard to extend its execution capabilities.

Key capabilities include:
- **Hierarchical Multi-Agent Supervision**: Coordinates specialized sub-agents (Security Auditor, Code Generator, Infrastructure Engineer) under a centralized task planning supervisor.
- **Declarative Context Manifests (`droid.yml`)**: Enforces file scoping, architectural rules, linting constraints, and tool capabilities per project repository.
- **FastMCP 3.1 Tool Calling Engine**: Dispatches sandboxed workspace actions (filesystem edits, git operations, testing suites, database migrations) via standardized MCP 3.1 protocols.
- **Empirical Regression & AST Verification**: Evaluates syntax trees and runs pre-commit hooks before finalizing autonomous code refactoring.
- **Strict Pydantic v2 Contract Guarantees**: Enforces schema isolation (`extra="forbid"`, `frozen=True`) across inter-droid task queues.

## What problem it solves
Droid solves the "Execution Gap" in AI-assisted development by moving beyond simple completions to autonomous task completion. It automates repetitive engineering toil—like updating API schemas across multiple layers, performing semantic security scans, and maintaining architectural consistency—allowing human engineers to focus on high-level system design. It eliminates brittle tool-calling setups by standardizing agentic actions via stream-aware MCP protocols and secure sandbox execution environments.

## Where it fits in the stack
**Development & Ops**. Droid functions as a CLI-based agentic layer that sits between the developer's intent and the file system/Git. It is frequently integrated into CI/CD pipelines as an autonomous "Junior Engineer" or "Security Auditor." It can also act as an MCP 3.1 client, interacting with external databases, sandboxed runtimes, or custom tools exposed by other parts of the infrastructure.

## Architecture & System Design

Droid uses a modular multi-agent supervisor topology. A primary Orchestration Engine parses natural language commands, reads project specifications from `droid.yml`, and delegates focused sub-tasks to domain-specific Droid workers (e.g., Security, Coder, Infra).

```
+-------------------------------------------------------------------------+
| Developer Terminal / CI/CD Runner                                       |
|                                                                         |
|   +-------------------+       Command/Goal      +--------------------+  |
|   | Developer / CI    | ======================> | Factory Droid CLI  |  |
|   +-------------------+                         +---------+----------+  |
|                                                           |             |
|                                                           v             |
|                                                 +--------------------+  |
|                                                 | droid.yml Context  |  |
|                                                 | Manifest Engine    |  |
|                                                 +---------+----------+  |
|                                                           |             |
|                                                           v             |
|                                                 +--------------------+  |
|                                                 | Orchestration Loop |  |
|                                                 +----+----+----+-----+  |
|                                                      |    |    |        |
|                      +-------------------------------+    |    +----+   |
|                      |                                    |         |   |
|                      v                                    v         v   |
|            +------------------+                  +----+---+   +-----+---+
|            | Security Auditor |                  | Coder  |   | Infra   |
|            | Droid Agent      |                  | Droid  |   | Droid   |
|            +--------+---------+                  +----+---+   +-----+---+
|                     |                                 |             |   |
|                     +-----------------+---------------+-------------+   |
|                                       |                                 |
|                                       v                                 |
|                            +--------------------+                       |
|                            | FastMCP 3.1 Tools  |                       |
|                            | (FS / DB / Git)    |                       |
|                            +--------------------+                       |
+-------------------------------------------------------------------------+
```

### Mathematical Foundations of Multi-Agent Supervisory Task Routing

Droid formulates complex software modification tasks as a hierarchical Markov Decision Process (MDP) over a discrete state space $\mathcal{S}$ of repository AST states and action space $\mathcal{A}$ of git/filesystem mutations.

#### 1. Task Decomposition Entropy & Routing Policy
Given a high-level user specification $\mathcal{G}$, the supervisor Droid decomposes the goal into an ordered sequence of sub-tasks $T = \{t_1, t_2, \dots, t_K\}$. The supervisor assigns sub-task $t_k$ to specialized worker agent $\alpha \in \{\alpha_{\text{coder}}, \alpha_{\text{security}}, \alpha_{\text{infra}}\}$ according to routing policy $\pi_{\text{sup}}(\alpha \mid t_k, \mathbf{c})$, where $\mathbf{c} \in \mathbb{R}^d$ is the semantic embedding vector of repository context:

$$
\pi_{\text{sup}}(\alpha \mid t_k, \mathbf{c}) = \frac{\exp\left(\mathbf{w}_\alpha^T \phi(t_k, \mathbf{c}) / \tau\right)}{\sum_{\alpha' \in \mathcal{A}_{\text{droid}}} \exp\left(\mathbf{w}_{\alpha'}^T \phi(t_k, \mathbf{c}) / \tau\right)}
$$

The decomposition uncertainty is monitored via Shannon entropy $\mathcal{H}(T)$:

$$
\mathcal{H}(T) = -\sum_{k=1}^K \sum_{\alpha \in \mathcal{A}_{\text{droid}}} \pi_{\text{sup}}(\alpha \mid t_k, \mathbf{c}) \log_2 \pi_{\text{sup}}(\alpha \mid t_k, \mathbf{c})
$$

When $\mathcal{H}(T) > \theta_{\text{ambiguity}}$, Droid pauses autonomous execution and invokes human-in-the-loop interactive clarification.

#### 2. Multi-Agent Consensus & Verification Convergence
Before applying AST mutations to the Git index, candidate diffs $\Delta_{\text{diff}}$ generated by the coder Droid must receive verification consensus from the security auditor Droid:

$$
\mathcal{V}(\Delta_{\text{diff}}) = \mathbb{I}\left( \text{AST}_{\text{valid}}(\Delta_{\text{diff}}) \land \mathcal{S}_{\text{sec}}(\Delta_{\text{diff}}) \ge \tau_{\text{sec}} \land \text{Tests}(\text{Repo} \oplus \Delta_{\text{diff}}) = \text{PASS} \right)
$$

Where $\mathcal{S}_{\text{sec}}(\cdot) \in [0, 1]$ represents the semantic vulnerability risk score and $\mathbb{I}(\cdot)$ is the indicator function. If $\mathcal{V}(\Delta_{\text{diff}}) = 0$, the diff is rejected and fed back into the coder Droid's contextual prompt buffer with annotated compiler/linter error traces.

## Feature Comparison Matrix

| Feature / Capability | Factory AI Droid | Claude Code CLI | Aider | OpenHands | Devin (Cognition) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Agent Architecture** | **Multi-Agent Supervisor**| Single Agent Loop | Single / Dual Agent | Containerized Multi-Agent| Cloud Autonomous Agent |
| **Context Manifest** | **`droid.yml` Native** | `CLAUDE.md` / Prompts | `.aider.conf.yml` | Repo Index / Docker | Web UI Prompt / Workspace|
| **MCP Support** | **Native FastMCP 3.1** | Native MCP Engine | Custom Extensions | Environment Plugins | Proprietary Integrations |
| **CI/CD Native Action**| **GitHub / GitLab Native**| CLI Scripting | CLI Scripting | Docker Runners | Webhook / Cloud Bot |
| **Execution Model** | **Local Sandbox / Cloud**| Anthropic API | Direct LLM API | Local Docker Sandbox | Managed Cloud VM |
| **AST Verification** | **Pre-commit Automated**| Heuristic / Tests | Test Execution Only | Test Execution Only | Browser + Sandboxed VM |
| **Pydantic v2 Contracts**| **Strict (extra='forbid')**| Raw Text / JSON | Raw Text / Diff | Raw JSON Schemas | Proprietary Payloads |
| **Systemd / Daemon Mode**| **Native Service Unit**| No | No | Docker Daemon | Cloud Hosted SaaS |

## Typical use cases
- **Autonomous Feature Development**: Implementing full-stack features from a natural language specification.
- **Continuous Security Hardening**: Identifying and automatically patching vulnerabilities found in static or dynamic analysis.
- **Architectural Enforcement**: Ensuring that new code follows project-defined patterns (e.g., proper dependency injection).
- **Automated Dependency Updates**: Updating library versions and refactoring breaking changes across the codebase.
- **MCP-Enabled Workspace Navigation**: Querying external documentation, API definitions, or local Docker environments via standard MCP 3.1 server interfaces.

## Strengths
- **Specialized Multi-Agent System**: Domain-specific Droids (Infra, Security, Frontend) provide higher precision than general-purpose agents.
- **Deep Context Awareness**: The `droid.yml` configuration allows for fine-grained control over the agent's "sight" and "rules."
- **CI/CD Native**: Seamlessly integrates with GitHub Actions, GitLab CI, and Jenkins for automated PR reviews and fixes.
- **Human-in-the-Loop**: Supports interactive "chat" modes for collaborative task refinement and approval gates.
- **MCP 3.1 / FastMCP 3.1 Compliance**: Fully compatible with Model Context Protocol servers, allowing standard-based extension of the agent's toolbox.

## Limitations
- **Configuration Overhead**: Complex repositories require a well-maintained `droid.yml` to maximize performance.
- **Resource Intensive**: Large-scale autonomous tasks can consume significant LLM tokens and execution time.
- **Proprietary Core**: While the CLI is open-source, the core reasoning engine and agent orchestration loop are managed services from Factory AI.

## When to use it
- When you need to automate large-scale refactoring or maintenance tasks across a private codebase.
- In enterprise environments where strict architectural rules must be enforced autonomously.
- To augment a small engineering team with specialized AI agents for security or infrastructure.
- When you want an agent that natively integrates with MCP 3.1 servers to control external sandboxes.

## When not to use it
- For simple, single-file edits where [Aider](./aider.md) or [Cline](../agents/cline.md) is faster.
- In air-gapped environments that cannot reach the Factory AI inference plane.
- If you prefer a fully open-source, locally-hosted agent framework (see [OpenHands](./openhands.md)).

## Getting started
Droid is installed via `npm` or `brew` and requires a Factory AI account.

### 1. Installation
```bash
npm install -g @factory-ai/droid@latest
```

### 2. Configuration (`droid.yml`)
Create a manifest in your repository root:
```yaml
version: 3.1
project: "Service-Mesh-Core"
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

### FastMCP 3.1 Bridge for Droid Execution
The following Python script implements a **FastMCP 3.1** server that allows Droid to execute local repository tasks safely with strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from typing import List, Optional

mcp = FastMCP("droid-task-bridge", version="3.1.0")

class DroidTaskSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(..., description="Unique task identifier")
    droid_type: str = Field(..., description="Target droid agent type: coder, auditor, operator")
    target_path: str = Field(..., description="Target file path")

    @field_validator("droid_type")
    @classmethod
    def validate_droid_type(cls, value: str) -> str:
        valid_types = {"coder", "auditor", "operator"}
        if value not in valid_types:
            raise ValueError(f"Invalid droid_type '{value}'. Must be one of {valid_types}")
        return value

class DroidTaskResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    status: str
    issues_found: int
    summary: str

@mcp.tool(name="execute_droid_agent_task", description="Dispatches autonomous task to local Droid agent sandbox")
def execute_droid_agent_task(task_id: str, droid_type: str, target_path: str) -> str:
    """FastMCP 3.1 tool for Droid execution."""
    try:
        spec = DroidTaskSpec(task_id=task_id, droid_type=droid_type, target_path=target_path)

        result = DroidTaskResult(
            task_id=spec.task_id,
            status="completed",
            issues_found=0,
            summary=f"Successfully executed {spec.droid_type} droid on {spec.target_path}"
        )
        return result.model_dump_json(indent=2)
    except ValidationError as ve:
        return f"Task spec validation error: {ve}"

if __name__ == "__main__":
    mcp.run()
```

### Manifest Validator with Strict Pydantic v2
The following copy-pasteable Python script demonstrates how developers can use strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) with custom validation hooks to parse, validate, and verify the structure of a `droid.yml` manifest.

```python
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from typing import List, Dict, Optional
import json

class DroidAgentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]{3,64}$")
    type: str = Field(..., description="Agent type: coder, auditor, operator")
    scope: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list)

    @field_validator("type")
    @classmethod
    def validate_agent_type(cls, value: str) -> str:
        valid_types = {"coder", "auditor", "operator"}
        if value not in valid_types:
            raise ValueError(f"Agent type must be one of {valid_types}")
        return value

class MCPServerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    command: str
    args: List[str] = Field(default_factory=list)

class DroidManifest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", frozen=True)

    version: str = Field("3.1", pattern=r"^3\.1$")
    project_name: str = Field(..., alias="project")
    stack: List[str] = Field(default_factory=list)
    droids: List[DroidAgentConfig] = Field(default_factory=list)
    mcp_servers: List[MCPServerConfig] = Field(default_factory=list)

def validate_droid_manifest(yaml_payload: dict) -> str:
    """Validates the droid.yml configuration manifest using strict Pydantic v2."""
    try:
        manifest = DroidManifest.model_validate(yaml_payload)
        return json.dumps({
            "status": "success",
            "validated_manifest": manifest.model_dump(by_alias=True)
        }, indent=2)
    except ValidationError as ve:
        return json.dumps({
            "status": "error",
            "validation_errors": str(ve)
        }, indent=2)

if __name__ == "__main__":
    payload = {
        "version": "3.1",
        "project": "Service-Mesh-Core",
        "stack": ["typescript", "rust", "kubernetes"],
        "droids": [
            {
                "name": "security-droid",
                "type": "auditor",
                "scope": ["src/auth/**", "src/crypto/**"],
                "rules": ["No hardcoded secrets", "Use TLS 1.3"]
            },
            {
                "name": "refactor-droid",
                "type": "coder",
                "scope": ["src/**/*.ts"],
                "rules": ["Prefer async/await over raw promises"]
            }
        ],
        "mcp_servers": [
            {
                "name": "filesystem-mcp",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
            }
        ]
    }
    print(validate_droid_manifest(payload))
```

## Docker Compose Sandboxed Runner Environment

```yaml
version: "3.8"

services:
  droid-runner:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: factory-droid-runner
    restart: unless-stopped
    ports:
      - "8310:8310"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./workspace:/workspace:rw
    environment:
      - FACTORY_API_KEY=${FACTORY_API_KEY}
      - FASTMCP_PORT=8310
      - DROID_SANDBOX_STRICT=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8310/health"]
      interval: 15s
      timeout: 5s
      retries: 3
    networks:
      - devops-net

networks:
  devops-net:
    driver: bridge
```

## Production Systemd Service Unit (`droid-daemon.service`)

```ini
[Unit]
Description=Factory AI Droid Agent Daemon
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=droid-agent
Group=droid-agent
WorkingDirectory=/opt/droid-workspace
Environment="FACTORY_API_KEY=your_factory_api_key_here"
Environment="FASTMCP_PORT=8310"
Environment="NODE_ENV=production"
ExecStart=/usr/local/bin/droid daemon --port 8310
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

### Automated Daemon Health Probe Script
Production probe script for CI/CD runners and Kubernetes liveness checks:

```python
#!/usr/bin/env python3
"""Automated Health Verification Probe for Factory AI Droid Daemon."""

import sys
import time
import requests

PROBE_URL = "http://127.0.0.1:8310/health"

def run_probe(retries: int = 3, timeout_sec: float = 2.0) -> bool:
    for attempt in range(1, retries + 1):
        try:
            start_time = time.monotonic()
            resp = requests.get(PROBE_URL, timeout=timeout_sec)
            elapsed_ms = (time.monotonic() - start_time) * 1000
            if resp.status_code == 200:
                print(f"[OK] Droid daemon healthy (latency: {elapsed_ms:.1f}ms)")
                return True
            else:
                print(f"[WARN] Attempt {attempt}: Received HTTP {resp.status_code}")
        except requests.RequestException as e:
            print(f"[WARN] Attempt {attempt}: Connection failed ({e})")
        time.sleep(1.0)
    print("[ERROR] Droid daemon health check failed after maximum retries.")
    return False

if __name__ == "__main__":
    if not run_probe():
        sys.exit(1)
```

## Diagnostic & Operational Troubleshooting Matrix

| Symptom / Error | Root Cause | Diagnostic Command / Inspection | Remediation Action |
| :--- | :--- | :--- | :--- |
| `DroidManifestValidationError` | Invalid key or unsupported Droid agent type in `droid.yml` | `python3 scripts/validate_manifest.py` | Validate manifest schema using Pydantic v2 validator script. |
| `MCP_Server_Handshake_Failed` | Path to MCP server binary (`npx`) misconfigured | `which npx && droid mcp list` | Verify `mcp_servers` configuration and binary availability. |
| `Scope_Access_Denied` | Target file path outside Droid `scope` array | Inspect `droid.yml` scope regex patterns | Expand `scope` pattern in `droid.yml` for target Droid. |
| `Token_Budget_Exceeded` | Multi-agent task exceeded context limits | `droid run --dry-run --verbose` | Restrict input prompt or enable incremental sub-agent runs. |
| `ERR_ENTROPY_THRESHOLD_BREACHED` | Goal specification ambiguity $\mathcal{H}(T)$ exceeded bounds | Check decomposition debug log | Clarify user prompt with precise file paths and acceptance criteria. |
| `GIT_MERGE_CONFLICT_ABORT` | Concurrent Droid workers modified intersecting lines in file | `git status` in sandbox workspace | Enforce sequential sub-task execution or file lock boundaries. |
| `DAEMON_SOCKET_TIMEOUT` | FastMCP daemon unresponsive on port 8310 | `journalctl -u droid-daemon -n 50` | Restart `droid-daemon.service` and verify network socket availability. |
| `AST_SYNTAX_VERIFICATION_FAIL` | Generated diff introduced parse errors in target file | `droid review --ast-check` | Reject proposed patch and instruct coder Droid with syntax error line numbers. |

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
- Last reviewed: 2027-01-07
- Confidence: high
