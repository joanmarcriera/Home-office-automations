# Anti-Gravity

## What it is
Anti-Gravity (v2026.4.x+) is Google's premier agentic development and execution framework. It is specifically engineered to build, orchestrate, and deploy autonomous AI agents capable of navigating, reasoning about, and modifying complex software systems. Operating at the cutting edge of July 2026 state-of-the-art (SOTA), Anti-Gravity leverages the multimodal and ultra-long context capabilities of the **Gemini 3.5 series (Ultra/Flash/Pro)**, **Gemini Spark** (for autonomous agent reasoning), and **Gemini Omni** (for spatial and interface comprehension). The framework provides standard high-level abstractions for "Missions" (long-horizon, stateful software tasks) and "Surfaces" (the target operational environments, such as git repositories, containers, or remote servers), enabling native, sandboxed code execution and formal, multi-step verification.

## What problem it solves
Autonomous software development agents operating in real-world workspaces face the "Complexity Wall" and "Abruption Risk." When agents perform large-scale refactoring or cross-repository migrations, raw LLM APIs fail due to context fragmentation, state drift, and lack of real-time environment validation. Anti-Gravity solves these issues by providing:
1. **Stateful Mission Continuity**: Robust, resumable state machines that survive underlying VM failures, execution timeouts, or model disconnects.
2. **Context-Aware Compression**: Section-aware codebase chunking that respects the 2M+ token context window while prioritizing relevant control flow maps.
3. **Formal Verification Loops**: Built-in AST validation, static analysis, and unit-test execution routines to ensure agent modifications never break main-branch compilation.
4. **Sandboxed Isolation**: Safe, isolated sandbox environments preventing arbitrary execution hazards on host systems.

## Where it fits in the stack
**Development & Ops Layer**. Anti-Gravity sits as the primary orchestration runtime for software agents in the Google Cloud and Vertex AI ecosystems. It integrates directly with Vertex AI Agent Builder, Google Cloud IAM, VPC Service Controls, and standard source-control hosts (GitHub, GitLab, Google Cloud Source Repositories), serving as a bridge between frontier reasoning models and production code environments.

## Typical use cases
- **Enterprise-Scale Refactoring**: Automatically updating massive codebases to new language versions (e.g., migrating python microservices from 3.10 to 3.13, or upgrading Java Spring Boot apps).
- **Agentic CI/CD Reconciliation**: Automatically listening to CI failures (e.g., failed tests or lint checks), spawning a sandboxed mission to diagnose the root cause, applying the fix, and resubmitting a validated pull request.
- **Architectural Discovery and Documentation**: Systematically scanning undocumented, legacy systems to construct interactive UML dependency graphs and functional technical specifications.
- **Vulnerability Remediation**: Integrating with security scanners (like Google Cloud Security Command Center) to autonomously patch CVEs, run regression tests, and apply security hardening policies.

## Strengths
- **Sub-100ms Native Tool Execution**: Leverages Vertex AI's native runtime sandbox for rapid tool-calling loops without container startup overhead.
- **Massive Context Support**: Native optimization for Gemini 3.5 Ultra's 2M+ context window, allowing entire repositories to be loaded, searched, and reasoning-mapped in a single agent step.
- **Secure by Default (SHARP Compliant)**: Full integration with enterprise security benchmarks, VPC Service Controls, and granular role-based access control (RBAC).
- **Model Context Protocol (MCP 3.0/3.1) Support**: Natively exposes all mission tracking, sandbox environments, and execution telemetry as standard MCP tools.
- **Project Genie Integration**: Able to leverage Google DeepMind's **Project Genie** platform to simulate and physically verify mechanical, terminal, or network interaction layers in a simulated world-model sandbox before running on real environments.

## Limitations
- **Platform Lock-in**: Deeply optimized for the Google Cloud Platform (GCP) and Vertex AI API structures, making on-premises or AWS/Azure-centric setups highly complex.
- **API Token Costs**: Sustained multi-step missions utilizing Gemini 3.5 Ultra for complex reasoning can accumulate substantial API consumption costs.
- **Closed-Source Orchestrator**: The core state machine and vertex sandbox scheduler are closed-source Google products, limiting customization of lower-level execution primitives.

## When to use it
- When building or deploying enterprise-grade autonomous software engineering agents with long-horizon goals.
- When your engineering organization is already standardized on GCP, Google Cloud Source Repositories, or Vertex AI.
- For complex, repository-wide auditing tasks requiring reasoning over millions of lines of code simultaneously.

## When not to use it
- For lightweight, local-only coding tasks where [Aider](./aider.md) or [Cline](../agents/cline.md) is a more cost-effective and portable option.
- If your development environment relies heavily on local execution without cloud dependencies (consider [Terminus 2](./terminus-2.md)).
- When building vendor-agnostic agent networks that require open-weights frameworks (consider [AG2](../frameworks/ag2.md) or [LangGraph](../frameworks/langgraph.md)).

## Getting started

### 1. Installation
Ensure Python 3.11+ is active. Install the stable July 2026 release of the Anti-Gravity SDK:

```bash
pip install google-cloud-antigravity==2026.7.15
```

### 2. Configure GCP Credentials & Project
Ensure your local terminal has appropriate authentication scopes to interact with Vertex AI Agent Builder:

```bash
# Login to GCP Application Default Credentials
gcloud auth application-default login

# Set active project
gcloud config set project my-enterprise-sandbox
```

### 3. Surface Configuration
Define your project's target surface configuration file (`surface.yaml`) to instruct the agent on execution boundaries:

```yaml
surface:
  id: "core-billing-service"
  repository: "https://github.com/my-enterprise/billing-api.git"
  branch: "main"
  workspace_root: "/workspace"
  sandbox:
    image: "us-central1-docker.pkg.dev/my-project/agents/sandbox-python311:latest"
    network_egress: "restricted"
```

## CLI examples

### Initialize a Surface Workspace
Register a target surface to build the operational environment for the agent:

```bash
antigravity surfaces register --config surface.yaml
```

### Launch an Autonomous Mission
Spawn a background mission using Gemini 3.5 Ultra to perform a dependency upgrade:

```bash
antigravity missions launch \
    --surface core-billing-service \
    --goal "Migrate our database pooling layer from SQLAlchemy 1.4 to 2.0. Ensure no deprecation warnings remain." \
    --mode autonomous \
    --model "gemini-3.5-ultra"
```

### Live Reasoning Telemetry
Stream the real-time reasoning steps, tool calls, and state transitions of an active mission:

```bash
antigravity missions trace projects/my-project/locations/us-central1/missions/ms-873941 \
    --format=live \
    --include-logs
```

### Inject Human Feedback
Provide real-time corrections or adjustments to an active mission loop without restarting the state machine:

```bash
antigravity missions feedback ms-873941 --message "Focus on the auth-handler module first before modifying database models."
```

## API examples

### Programmatic Mission Execution
Use the Python SDK to define surfaces, configure execution constraints, launch autonomous missions, and poll for resolution:

```python
import time
from google.cloud import antigravity

# Initialize the Vertex AI Agent Service Client
client = antigravity.AgentServiceClient()

# Define the target operational surface
surface = antigravity.Surface(
    repository="https://github.com/my-enterprise/billing-api.git",
    branch="main",
    context_depth=antigravity.ContextDepth.HIGH,
    isolation_mode=antigravity.IsolationMode.VPC_SANDBOX
)

# Define the formal verification steps
verification = antigravity.VerificationSuite(
    test_command="pytest tests/unit",
    lint_command="flake8 src/",
    auto_rollback=True
)

# Construct and launch the mission payload
mission_payload = {
    "display_name": "SQLAlchemy v2 Migration",
    "goal": "Rewrite legacy engine setup in src/db.py to use SQLAlchemy 2.0 Context Managers.",
    "surface": surface,
    "verification": verification,
    "mode": antigravity.MissionMode.AUTONOMOUS,
    "model_name": "gemini-3.5-ultra"
}

print("Launching autonomous Anti-Gravity mission...")
mission = client.create_mission(
    parent="projects/my-gcp-project/locations/us-central1",
    mission=mission_payload
)
print(f"Mission initiated. ID: {mission.name}")

# Poll mission status until completion
while True:
    status = client.get_mission(name=mission.name)
    print(f"Current State: {status.state} | Progress: {status.progress_percentage}%")

    if status.state in [antigravity.MissionState.SUCCEEDED, antigravity.MissionState.FAILED]:
        break
    time.sleep(15)

if status.state == antigravity.MissionState.SUCCEEDED:
    print(f"Mission succeeded! Changes applied to branch: {status.output_branch}")
else:
    print(f"Mission failed. Error log: {status.error_details}")
```

### Exposing Anti-Gravity as an MCP 3.0 Server
Launch an MCP server to expose Anti-Gravity tool execution structures to external local clients like Claude Desktop:

```python
from google.cloud.antigravity.mcp import AntiGravityMCPServer

# Instantiate and run the MCP 3.0/3.1 server on stdio
server = AntiGravityMCPServer(
    project_id="my-enterprise-sandbox",
    location="us-central1",
    allowed_surfaces=["core-billing-service"]
)

if __name__ == "__main__":
    # Start the standard input/output transport loop
    server.start()
```

## Related tools / concepts
- [Gemini](../ai_knowledge/google-gemini.md) — Google's foundational frontier model suite.
- [OpenHands](./openhands.md) — Highly extensible, open-source agentic workspace framework.
- [Cline](../agents/cline.md) — Local terminal-native and editor-integrated agent.
- [LangGraph](../frameworks/langgraph.md) — State-machine-based multi-agent coordination library.
- [Aider](./aider.md) — Powerful, CLI-driven, Git-native pair programming tool.
- [Windsurf](./windsurf.md) — Advanced IDE built for collaborative flow-state software development.
- [Claude Code](./claude-code.md) — Terminal-native autonomous software developer.
- [Terminus 2](./terminus-2.md) — Standard raw-terminal model execution baseline.
- [AG2](../frameworks/ag2.md) — Multi-agent workflow automation and orchestration framework.
- [Project Genie](../ai_knowledge/project-genie.md) — Google DeepMind's generative physical and digital interactive simulator.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Standard architecture patterns for agent reasoning loops.
- [SHARP Security Benchmark](../../knowledge_base/llm_security_privacy.md) — Privacy, compliance, and sandbox security standard.

## Sources / references
- [Build with Google Anti-Gravity (Google Developers Blog)](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
- [Vertex AI Antigravity Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder/antigravity-overview)
- [Google Cloud Agentic Architecture Guide (June 2026)](https://cloud.google.com/architecture/ai-agents)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
