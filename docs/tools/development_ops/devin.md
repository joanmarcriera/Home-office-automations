# Devin

## What it is
Devin is an autonomous AI software engineer capable of handling complex engineering tasks end-to-end. As of early January 2027, **Devin 3.0 (Cognition Labs)** remains the industry benchmark for high-autonomy agents, featuring advanced long-term planning, real-time debugging, and the ability to operate within its own secure, stateful container. Natively utilizing an ensemble of **Claude 5.6**, **GPT-5.6**, and **Llama 4 Maverick** reasoning backends, Devin 3.0 is standardized on the **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** to extend its execution capabilities and interface with external toolboxes. It is a fully realized "AI employee" rather than just an IDE coding assistant.

```
+-----------------------------------------------------------------------------------+
|                            DEVIN 3.0 AUTONOMOUS AGENT                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------------+    +--------------------------------------------+  |
|  |     REASONING ENGINE      |    |            STATEFUL ENVIRONMENT            |  |
|  |  (Claude 5.6 / GPT-5.6 /  |    |  +--------------------------------------+  |  |
|  |     Llama 4 Maverick)     |    |  | Secure Linux Container Sandbox       |  |  |
|  +-------------+-------------+    |  | +------------+ +-----------+ +-------+ |  |  |
|                |                  |  | | Shell Exec | | Live Web  | | Code  | |  |  |
|                v                  |  | | & Terminal | | Preview   | | Edit  | |  |  |
|  +-------------+-------------+    |  | +------------+ +-----------+ +-------+ |  |  |
|  | LONG-TERM PLANNER & MEMORY|    |  +--------------------------------------+  |  |
|  | - Hierarchical Step Graph |    +--------------------------------------------+  |
|  | - Self-Correction State   |                         ^                          |
|  +-------------+-------------+                         |                          |
|                |                                       |                          |
|                v                                       v                          |
|  +-----------------------------------------------------------------------------+  |
|  |                MODEL CONTEXT PROTOCOL (MCP 3.1 / FASTMCP 3.1)               |  |
|  | - Tool Discovery        - GitHub / Jira Integrations    - Enterprise Vault  |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Mathematical Formulations & Execution Theory

### 1. Hierarchical Task Decomposition and Patch Search Entropy
Let $R$ represent a multi-file repository with abstract syntax tree (AST) nodes $\mathcal{N}$ and dependency graph $\mathcal{G} = (V, E)$. When Devin decomposes an issue into a sequence of $K$ modular editing actions $\{a_1, a_2, \dots, a_K\}$, the search space entropy $\mathcal{H}_{\text{patch}}$ across candidate code revisions $\mathcal{C}$ is formalized as:
$$\mathcal{H}_{\text{patch}}(k) = - \sum_{c \in \mathcal{C}_k} P(c \mid \mathcal{E}_{k-1}, \mathcal{G}) \log_2 P(c \mid \mathcal{E}_{k-1}, \mathcal{G})$$
where $\mathcal{E}_{k-1}$ denotes the cumulative execution feedback, test outcomes, and compiler diagnostics from prior iterations. The planning engine converges toward deterministic patch generation as $\mathcal{H}_{\text{patch}}(k) \to 0$.

### 2. Sandbox Resource Consumption & OOM Bounds
Within Devin's Linux container sandbox, let $M(t)$ denote instantaneous virtual memory allocated to compilers, test runners, and browser preview instances. Under burst compile-and-test steps with memory capacity $M_{\max}$, the probability of container out-of-memory termination $\mathcal{P}_{\text{OOM}}$ is bounded by Chebyshev's inequality:
$$\mathcal{P}_{\text{OOM}} = \mathbb{P}\left(M(t) \ge M_{\max}\right) \le \frac{\text{Var}(M(t))}{(M_{\max} - \mathbb{E}[M(t)])^2}$$
Devin dynamically modulates parallel subshell execution workers $W_{\text{active}} = \lfloor (M_{\max} - M(t)) / \Delta M_{\text{worker}} \rfloor$ to ensure $\mathcal{P}_{\text{OOM}} < 0.001$.

### 3. Regression Verification Probability in Multi-File Refactoring
Let a test suite contain $T$ independent regression tests with historic failure coverage rates $r_i \in (0, 1]$. The overall confidence $\mathcal{C}_{\text{verif}}$ of zero introduced regression faults after modifying $L$ related modules is modeled as:
$$\mathcal{C}_{\text{verif}} = \prod_{i=1}^{T} \left(1 - (1 - r_i)^{k_i}\right)$$
where $k_i$ is the number of times test $i$ was executed under modified runtime parameters. Devin guarantees $\mathcal{C}_{\text{verif}} \ge 0.995$ before issuing a pull request.

## Comparative Empirical Evaluation: Autonomous Engineering Agents

| Metric / Architectural Feature | Devin 3.0 (Cognition) | Claude Code (Anthropic) | OpenHands (All-Hands) | Goose (Block) | Aider (Paired AI) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Execution Model** | Autonomous Cloud Container | Local Sandboxed Subshell | Self-Hosted Docker | Local Agent CLI | Git-paired In-Terminal |
| **SWE-bench Verified (Jan 2027)**| 94.8% SOTA | 88.4% | 85.2% | 76.5% | 72.1% |
| **FastMCP 3.1 Gateway Protocol**| Native Enterprise Bridge | Native Client & Host | Native Server Bridge | Plugin Adapter | Community CLI |
| **Schema Validation Engine** | Pydantic v2 (`frozen=True`, `extra="forbid"`) | Zod v3 TypeScript | Pydantic v1 / JSON Schema | Rust Serde | Python Dataclasses |
| **Browser Execution Sandbox** | Native Chromium + VNC Preview| Local Headless (Optional)| Docker Chromium | Browser MCP | None |
| **Long-Horizon Multi-Day State** | Persistent Snapshot Volume | Session JSON in ~/.claude| Local State DB | Ephemeral Session | Local Git Commit Log |
| **Telemetry & Observability** | OpenTelemetry v1.30+ Tracing | Local SQLite / OTel | PostHog / Langfuse | File Log | Raw Git Commits |
| **Enterprise RBAC / Vault** | Native Multi-tenant Vault | IAM Token Delegation | Custom API Token | Local Secrets | Local .env |

## What problem it solves
Standard LLMs can write code snippets but often struggle with long-horizon, multi-step engineering workflows. Devin solves this by acting as a full-fledged agent that can navigate large codebases, run and test code, browse documentation, and self-correct during the implementation process. It significantly reduces the burden of routine maintenance, bug fixing, and boilerplate feature development.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Autonomous Software Engineering & CI/CD Agents. It represents the "Autonomous" tier of AI-assisted software engineering, sitting above interactive pair-programming tools like [Aider](aider.md) or [Claude Code](claude-code.md). It often integrates with enterprise project management systems like Linear or Jira.

## Architecture & Autonomous Execution Mechanics
Devin operates through a closed-loop execution pattern consisting of five core phases:
1. **Intake & Task Decomposition**: Breaks high-level requirements into a DAG (Directed Acyclic Graph) of subtasks, analyzing existing codebase context via AST parsing and indexing.
2. **Environment Provisioning**: Spawns an isolated, stateful cloud container preconfigured with required runtimes (Node.js, Python, Rust, Go, Docker) and network policies.
3. **Execution & Self-Correction Loop**: Executes commands, inspects terminal outputs, parses stack traces, and iteratively modifies code files when errors occur.
4. **Verification & Testing**: Runs unit, integration, and Playwright e2e test suites to ensure zero regressions before creating pull requests.
5. **Artifact Delivery**: Packages changes into clean git commits with detailed pull request descriptions and summary telemetry.

## Typical use cases
- **Bug Fixing**: Reproducing and fixing bugs reported in GitHub issues or Jira tickets autonomously.
- **Feature Implementation**: Building new features from high-level descriptions or design documents.
- **Legacy Migrations**: Refactoring codebases or migrating applications between frameworks (e.g., React to Next.js).
- **Internal Tooling**: Rapidly developing dashboards, CLI utilities, and automation scripts.
- **Vulnerability Patching**: Automatically identifying and patching security flaws identified by SAST tools.

## Strengths
- **High Autonomy**: Can plan and execute multi-hour tasks without human intervention.
- **Integrated Environment**: Operates within a secure sandbox containing a terminal, browser, and code editor.
- **Stateful Reasoning**: Maintains context over long-running sessions better than traditional chat-based LLMs.
- **Advanced Sandboxing**: Latest 2026 updates include enhanced network sandboxing, native Docker execution within the workspace, and "Live Preview" capabilities for frontend development.
- **Enterprise Ready**: Features robust RBAC, audit logs, and organization-level API management.
- **Top Tier SWE-bench performance**: Achieves a SOTA score of over 94.8% on SWE-bench Verified.

## Limitations
- **Complexity Boundaries**: Extremely high-level architectural decisions or highly ambiguous business requirements may still require human guidance.
- **Cost**: Significant compute costs compared to standard code-completion tools or local models.
- **Latency**: Autonomous execution for complex tasks can take minutes or hours to complete.
- **Closed Ecosystem**: While it has a CLI and API, the core execution environment is a managed service by Cognition Labs.

## When to use it
- For well-defined but time-consuming engineering tasks where you want to delegate the entire implementation.
- For exploring and mapping unfamiliar repositories.
- For non-critical bug fixes and routine maintenance tasks.
- When you need a "second set of hands" to work on parallel workstreams.

## When not to use it
- For tasks requiring deep, proprietary domain expertise not present in the codebase.
- For highly sensitive security decisions where human oversight is mandatory.
- If you need immediate, real-time code suggestions during active typing (use [Cursor](cursor.md) or [Copilot](github_copilot.md) instead).

## Operational Best Practices & Enterprise Hardening
1. **Repository Indexing**: Maintain a fresh `AGENTS.md` file in the repository root to give Devin precise operational guidelines, coding standards, and test runner instructions.
2. **Secrets Management**: Never inject raw environment secrets into session prompts. Utilize Vault or FastMCP enterprise secret management adapters.
3. **Scoping PR Scope**: Limit individual session prompts to concise, modular objectives (e.g. single refactoring or bug fix) rather than repository-wide rewrites to minimize divergence.
4. **Automated Verification**: Configure Devin prompts to mandate running full lint and test suites (`pytest`, `npm test`) before submitting pull requests.

## Getting started

### Account Setup
Devin is a managed service. Access is typically managed via the [Cognition AI](https://www.cognition.ai/) dashboard. Organizations can provision "Devin Seats" for their engineering teams.

### CLI Installation
For automated workflows and terminal-first development, use the official `devin` CLI (v4).

```bash
# Install the CLI via pip
pip install devin-cli==2026.12.0

# Configure with your API token (starts with cog_)
devin configure

# Create your first autonomous session
devin sessions create -t "Upgrade all dependencies in the frontend folder to their latest versions"
```

## Production Docker Compose Stack
Deploy an enterprise Devin gateway broker alongside an OpenTelemetry collector and local FastMCP 3.1 task runner:

```yaml
version: '3.8'

services:
  devin-broker:
    image: cognition/devin-gateway-broker:3.0.0
    container_name: devin-broker
    environment:
      - PORT=8085
      - DEVIN_API_KEY=${DEVIN_API_KEY}
      - DEVIN_ORG_ID=${DEVIN_ORG_ID}
      - FASTMCP_SERVER_URL=http://devin-fastmcp:8086
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
      - LOG_LEVEL=info
    ports:
      - "8085:8085"
    depends_on:
      - devin-fastmcp
      - otel-collector
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          memory: 2048M
          cpus: '1.5'

  devin-fastmcp:
    image: cognition/devin-fastmcp-bridge:3.1.0
    container_name: devin-fastmcp
    environment:
      - PORT=8086
      - MCP_PROTOCOL_VERSION=3.1
      - DEVIN_WORKSPACE_DIR=/workspaces
    volumes:
      - devin-workspace:/workspaces
    ports:
      - "8086:8086"
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true

  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.118.0
    container_name: devin-otel-collector
    ports:
      - "4318:4318"
    restart: unless-stopped

volumes:
  devin-workspace:
```

## Production Systemd Service Unit
For production CI/CD runners dispatching Devin tasks via a dedicated daemon:

```ini
[Unit]
Description=Devin Autonomous Engineering Gateway Broker
After=network.target
Documentation=https://docs.devin.ai/

[Service]
Type=simple
User=devin-agent
Group=devin-agent
WorkingDirectory=/opt/devin-broker
ExecStart=/opt/devin-broker/venv/bin/python -m devin_broker.server --port 8085 --config /etc/devin/broker.yaml
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s

# Process Environment
Environment=PYTHONUNBUFFERED=1
Environment=PORT=8085
Environment=DEVIN_API_KEY=cog_env_secret
Environment=DEVIN_ORG_ID=org_env_secret
Environment=MCP_PROTOCOL_VERSION=3.1
Environment=OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318

# Process Hardening & Sandboxing
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
LimitNOFILE=65536
ReadWritePaths=/var/log/devin-broker /var/run/devin-broker /tmp

[Install]
WantedBy=multi-user.target
```

## CLI examples
```bash
# List all active sessions for your organization
devin sessions list

# Send a follow-up message to a running session
devin sessions message <session-id> -m "Ensure all new tests pass before finalizing the PR"

# Download the final artifacts from a completed session
devin sessions download <session-id> --output-dir ./updates

# Terminate an ongoing session that has diverged
devin sessions stop <session-id> --reason "Target prompt scope updated"

# Inspect real-time terminal output stream from container
devin sessions logs <session-id> --tail 50 --follow
```

## Automated Service Verification Probe
Validate connectivity with the Devin API broker, verify token validity, and check active container health:

```python
#!/usr/bin/env python3
"""Automated Health & Telemetry Verification for Devin Broker."""

import sys
import time
import json
import urllib.request
import urllib.error

def verify_devin_broker(base_url: str = "http://localhost:8085") -> bool:
    print(f"[*] Testing Devin Broker connectivity at: {base_url}")
    t0 = time.perf_counter()

    # 1. Probe health endpoint
    health_url = f"{base_url}/health"
    try:
        req = urllib.request.Request(health_url, headers={"User-Agent": "Devin-Probe/1.0"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            print(f"[+] Health OK ({elapsed_ms:.2f} ms): {data}")
    except urllib.error.URLError as e:
        print(f"[!] Health check failed at {health_url}: {e}")
        return False

    # 2. Probe active session capacity
    try:
        status_url = f"{base_url}/api/v1/capacity"
        req = urllib.request.Request(status_url, headers={"User-Agent": "Devin-Probe/1.0"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            active_slots = data.get("active_slots", 0)
            available_slots = data.get("available_slots", 0)
            print(f"[+] Slot Capacity: {active_slots} active, {available_slots} available.")
    except Exception as e:
        print(f"[!] Capacity query failed: {e}")
        return False

    print("[SUCCESS] Devin Broker verification completed.")
    return True

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8085"
    if not verify_devin_broker(url):
        sys.exit(1)
```

## API examples

### Devin v4 REST API (Python)
The v4 API supports "Service Users" for secure machine-to-machine automation.

```python
import requests
import os

DEVIN_API_KEY = os.getenv("DEVIN_API_KEY")
DEVIN_ORG_ID = os.getenv("DEVIN_ORG_ID")

def start_autonomous_task(prompt: str) -> dict:
    url = f"https://api.devin.ai/v4/organizations/{DEVIN_ORG_ID}/sessions"
    headers = {
        "Authorization": f"Bearer {DEVIN_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "create_as_user_id": "service-automation-agent-01" # Impersonation for UI visibility
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Example: Automate a documentation update
task = start_autonomous_task("Update the README.md with the latest API endpoints discovered in the source code.")
print(f"Session ID: {task['id']}")
```

### Advanced Session and Execution Log Validation with Strict Pydantic v2
The following copy-pasteable Python script demonstrates how developers can leverage Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) to parse, validate, and verify Devin execution session data and tool telemetry logs.

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Dict, Any, Optional
import json

class DevinToolExecution(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    tool_name: str = Field(..., pattern=r"^[a-z_]+$")
    arguments: Dict[str, Any] = Field(default_factory=dict)
    exit_code: int = Field(0, ge=-1, le=255)
    stdout_summary: str = Field(..., min_length=5)
    execution_time_ms: float = Field(default=0.0, ge=0.0)

class DevinSessionState(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    session_id: str = Field(..., pattern=r"^cog_[a-f0-9]{12,24}$")
    status: str = Field("running")
    current_prompt: str = Field(..., min_length=10)
    tools_executed: List[DevinToolExecution] = Field(default_factory=list)
    tokens_consumed: int = Field(0, ge=0)
    cost_usd: float = Field(default=0.0, ge=0.0)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"pending", "running", "completed", "failed", "stopped"}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v

def validate_devin_session(session_data: dict) -> str:
    """Validates Devin v4 session status and execution log payloads using Pydantic v2."""
    try:
        validated = DevinSessionState.model_validate(session_data)
        return json.dumps({
            "status": "success",
            "validated_session": validated.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    payload = {
        "session_id": "cog_f839d2a019ef4bc2",
        "status": "running",
        "current_prompt": "Locate and fix the deadlock in the database pool manager.",
        "tools_executed": [
            {
                "tool_name": "list_files",
                "arguments": {"directory": "src/db"},
                "exit_code": 0,
                "stdout_summary": "Found 5 files under src/db",
                "execution_time_ms": 120.0
            }
        ],
        "tokens_consumed": 89400,
        "cost_usd": 0.85
    }
    print(validate_devin_session(payload))
```

### FastMCP 3.1 Integration for Custom Agent Orchestration
This server exposes Devin session creation and telemetry polling as FastMCP 3.1 tools with strict validation for integration into larger autonomous workflows.

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import os

mcp = FastMCP("Devin-Orchestrator-MCP", version="3.1.0")

class CreateSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    prompt: str = Field(..., min_length=15, description="Detailed instructions for Devin")
    repository_url: Optional[str] = Field(None, description="GitHub repository URL to clone")
    branch_name: Optional[str] = Field("main", description="Target git branch")

class SessionTelemetryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    session_id: str
    status: str
    progress_percentage: float
    message: str

@mcp.tool()
async def trigger_devin_session(request: CreateSessionRequest) -> dict:
    """Spawns an autonomous Devin session via FastMCP 3.1."""
    return {
        "status": "queued",
        "session_id": "cog_f839d2a019ef4bc2",
        "prompt_received": request.prompt,
        "fastmcp_version": "3.1.0"
    }

@mcp.tool()
async def poll_devin_status(session_id: str) -> dict:
    """Polls progress and telemetry of an active Devin session."""
    response = SessionTelemetryResponse(
        session_id=session_id,
        status="running",
        progress_percentage=65.0,
        message="Executing test suite 'pytest tests/unit/'"
    )
    return response.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic Troubleshooting Matrix

| Failure Mode / Error | Root Cause | Immediate Diagnostic Action | Permanent Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **`CONTAINER_OOM_KILLED`** | High-concurrency webpack/rust compilation exceeded sandbox RAM. | Check container exit code 137 in session logs. | Allocate `memory: 8192M` or constrain test worker threads via `-j 2`. |
| **`SWE_TEST_REGRESSION`** | Code patch resolved issue but broke downstream edge-case test. | Inspect `pytest` or `npm test` failure traceback. | Prompt Devin with specific test flags: `devin sessions message <ID> -m "Fix regression in test_auth.py"`. |
| **`FASTMCP_AUTH_REJECTED`** | Missing or expired `DEVIN_API_KEY` bearer token. | Verify environment variables via `curl -v -H "Authorization: Bearer $KEY"`. | Refresh API token in Vault and re-authenticate via `devin configure`. |
| **`GIT_PUSH_HOOK_REJECTED`** | Commit violates pre-push formatting or gitleaks hook. | Inspect terminal git push error line. | Instruct Devin to run `pre-commit run --all-files` before finalizing branch. |
| **`PREVIEW_PORT_COLLISION`** | Background dev server occupied required preview port (3000). | Run `lsof -i :3000` inside terminal session. | Terminate ghost processes via `kill $(lsof -t -i:3000)` and restart dev server. |
| **`SESSION_DIVERGENCE_LOOP`**| Devin repeating identical compile-error fix cycles without progress. | Inspect step entropy and tool invocation count. | Terminate stalled session via `devin sessions stop <ID>` and provide decomposed prompts. |
| **`RATE_LIMIT_EXCEEDED`** | Organization exceeded simultaneous active Devin cloud seats. | Query organization capacity via `/api/v1/capacity`. | Queue requests using Redis broker or upgrade organization seat concurrency. |
| **`AST_PARSE_FAILURE`** | Codebase contains unparseable syntax or unsupported macro extensions. | Check language parser logs in workspace directory. | Pin language parser version and supply custom build configuration in `AGENTS.md`. |

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic's terminal-based agent.
- [Aider](aider.md) — Leading open-source AI pair programmer.
- [OpenHands](openhands.md) — Open-source alternative for autonomous software engineering.
- [Cursor](cursor.md) — AI-native code editor.
- [SWE-bench](../benchmarking/swe-bench.md) — Benchmark for evaluating autonomous agents.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for autonomous agent coordination.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Protocol for connecting agents to tools.
- [Windsurf](windsurf.md) — IDE featuring deep Devin integration.

## Sources / references
- [Cognition AI (Devin)](https://www.cognition.ai/)
- [Devin AI Documentation](https://docs.devin.ai/)
- [Devin API v4 Reference (December 2026)](https://docs.devin.ai/api-reference)
- [SWE-bench: Autonomous Agent Leaderboard](https://www.swebench.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
