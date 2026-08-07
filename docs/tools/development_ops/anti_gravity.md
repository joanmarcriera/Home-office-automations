# Anti-Gravity

## What it is
Anti-Gravity (v2026.12.x+) is Google's premier agentic development and execution framework, engineered to build, orchestrate, and deploy autonomous AI agents capable of navigating, reasoning about, and modifying complex software ecosystems. It provides high-level, production-grade abstractions for "Missions" (long-horizon tasks) and "Surfaces" (the agent's operational and environmental context). Natively leveraging the **Gemini 4.0** series (Ultra, Flash, and Pro), Gemini Spark (for autonomous multi-agent orchestration), and Gemini Omni (for multimodal and generative media reasoning), Anti-Gravity offers native code execution, massive context windows (2M+ tokens), and native integration with the Model Context Protocol (**MCP 3.1 / FastMCP 3.1**) to expose agent environments and tool calls seamlessly.

## What problem it solves
Anti-Gravity addresses the "Complexity Wall" in autonomous software engineering. Typical agent setups suffer from brittle tool-calling loops, high error-propagation rates on large-scale refactoring tasks, and sandbox isolation limits. It simplifies the creation of agents that can safely refactor multi-million line codebases, resolve complex cross-repository dependencies, and maintain execution state over long-running asynchronous tasks. Furthermore, it implements an ultra-secure, SHARP-compliant, and VPC-isolated execution sandbox, ensuring that autonomous agent actions are contained without exposing the host operating system to damage or unauthorized network exfiltration.

## Where it fits in the stack
**Development & Ops / Agent Execution Layer**. Anti-Gravity resides as a central development and runtime orchestration layer within the Vertex AI Agent Builder and Google Cloud environments. It acts as the bridge between raw foundational model reasoning and stateful, real-world development environments (git repositories, CI/CD runtimes, and local filesystems). It exposes standardized **MCP 3.1 / FastMCP 3.1** server endpoints, allowing any external compatible agent (such as Claude Code, Terminus 2, or Droid) to utilize Anti-Gravity's secure sandboxes as execution surfaces.

## Typical use cases
- **Autonomous Repository Refactoring**: Large-scale migrations (e.g., Python 3.10 to 3.13, or legacy Java architectures to Go/Python) across hundreds of distributed microservices.
- **Claude 5.1 & Partner Model Missions**: Running multi-model developer agents inside a specialized Anti-Gravity Surface connector, allowing models like Claude 5.1 or Llama 4 to run complex systems-engineering tasks securely.
- **Agentic CI/CD Self-Healing**: Integrating directly into GitHub Actions or Google Cloud Build to automatically spin up a mission, analyze test failures or security alerts, apply the correct patch, and verify the outcome.
- **Generative World and Simulation Testing**: Underpinning agent training by leveraging DeepMind's Project Genie to dynamically synthesize non-deterministic physical and mechanical sandboxes.
- **Legacy Code Modernization**: Systematically parsing, documenting, and rewriting deprecated COBOL or Java systems into cloud-native architectures.

## Strengths
- **Native Gemini 4.0 & Multi-Model Integration**: Deeply optimized for Gemini 4.0's 2M+ token context window, Gemini Spark's autonomous planning, and partner-model connectors (Claude 5.1, Llama 4).
- **Model Context Protocol (MCP 3.1 / FastMCP 3.1) Native Support**: Exposes development surfaces, toolboxes, and agent runtimes as standardized, streaming telemetry-enabled MCP servers.
- **Stateful Mission Abstraction**: Out-of-the-box support for multi-step, long-running processes with built-in checkpointing, rollback triggers, and human-in-the-loop steering feedback.
- **SHARP-Compliant Security Sandboxing**: Built-in isolation with Google Cloud IAM, VPC Service Controls, and automated code-integrity scanning to guarantee strict execution boundaries.
- **Advanced Observability and Tracing**: Complete observability of agent thought loops, tool executions, and system resource metrics via Google Cloud Operations Suite integration.

## Limitations
- **Google Cloud Ecosystem Lock-in**: Deeply integrated with and optimized for GCP services (Vertex AI, Cloud Run, Artifact Registry, VPCs), making full local deployments complex.
- **High Token Consumption**: Leveraging massive 2M+ token contexts for continuous repository-wide reasoning can incur high operational API costs.
- **Closed Orchestration Core**: Although the client SDK and MCP integrations are open-source, the core mission-orchestration engine is a managed Google Cloud service.

## When to use it
- When building production-grade autonomous software engineering agents designed to interact with enterprise-scale codebases.
- For missions requiring extremely large context windows or real-world system interactions that demand deep tracing and strict security isolation.
- When your engineering organization is standardized on Google Cloud Platform and Vertex AI.
- When you need to build collaborative multi-agent teams where agents must safely share sandboxed terminal workspaces and telemetry.

## When not to use it
- For simple, local-only command-line scripts or personal side-projects where lightweight tools like [Aider](./aider.md) or [Cline](../agents/cline.md) are sufficient.
- In multi-cloud or AWS/Azure-centric environments where GCP is not an option (consider [OpenHands](./openhands.md) instead).
- If your architecture requires a completely open-source, local-first orchestrator (consider [LangGraph](../frameworks/langgraph.md)).

## Getting started

### 1. Installation
The Anti-Gravity SDK is available as part of the Google Cloud AI library:
```bash
pip install google-cloud-antigravity==2026.12.0
```

### 2. Authentication and Setup
Configure your Google Cloud credentials and ensure you are operating in a SHARP-compliant GCP project:
```bash
# Authenticate with Google Cloud SDK
gcloud auth application-default login

# Configure project and location context
gcloud config set project my-agentic-sandbox-project
```

### 3. Basic Mission Definition
Define a declarative `mission.yaml` to specify the agent's goal, surface isolation, and runtime rules:
```yaml
mission:
  name: "legacy-to-pytest-migration"
  goal: "Migrate all legacy unittest files to pytest under /tests directory, ensuring all new tests pass successfully."
  surface:
    type: "git"
    repository: "git@github.com:my-org/auth-service.git"
    branch: "agent/pytest-refactor"
    sandbox_profile: "restricted-developer"
  rules:
    - "Do not alter CI/CD pipeline definitions in .github/"
    - "Ensure 100% parity across all test suites"
    - "All newly generated code must comply with PEP 8 standards"
```

## CLI examples

- **Launch an Autonomous Mission**:
  ```bash
  antigravity missions launch --config mission.yaml --mode autonomous
  ```

- **Expose an Anti-Gravity Surface as an MCP 3.1 Server**:
  ```bash
  antigravity surfaces serve --id "auth-service-workspace" --protocol mcp --port 8080
  ```

- **Trace Agent Reasoning and Telemetry Live**:
  ```bash
  antigravity missions trace <mission_id> --format=live --telemetry
  ```

- **Inject Human-in-the-Loop Steering Feedback**:
  ```bash
  antigravity missions feedback <mission_id> "Focus on migrating tests inside /tests/auth/ first before moving to other modules."
  ```

- **List Active Sandboxed Surfaces**:
  ```bash
  antigravity surfaces list --project my-agentic-sandbox-project
  ```

## API examples

### Programmatic Gemini 4.0 Pro Mission
This example shows how to launch and orchestrate a long-horizon software engineering mission using the Python SDK:

```python
from google.cloud import antigravity

# Initialize the Anti-Gravity Client
client = antigravity.AgentServiceClient()

# Construct the operational and sandboxed surface
surface = antigravity.Surface(
    repository="https://source.developers.google.com/p/my-proj/r/my-repo",
    sandbox_profile="secure-isolation",
    context_depth="high"
)

# Launch an autonomous mission with Gemini 4.0 Pro
mission = client.create_mission(
    parent="projects/my-proj/locations/us-central1",
    mission={
        "name": "dependency-audit-mission",
        "goal": "Identify and resolve all deprecated library imports and security vulnerabilities in package.json",
        "surface": surface,
        "model": "gemini-4.0-pro",
        "mode": antigravity.MissionMode.AUTONOMOUS
    }
)

print(f"Mission {mission.name} launched. Status: {mission.status}")
```

### Robust Mission Config Validation with Pydantic v2
The following example shows how to programmatically model, validate, and verify an Anti-Gravity mission and sandbox profile using Pydantic v2 to ensure proper formatting prior to execution.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class SandboxProfile(BaseModel):
    profile_name: str = Field(..., min_length=3, max_length=50)
    vpc_isolated: bool = True
    allowed_ports: List[int] = Field(default_factory=list)
    resource_limits: Dict[str, str] = Field(default_factory=lambda: {"cpu": "2", "memory": "4Gi"})

    @field_validator("allowed_ports")
    @classmethod
    def validate_ports(cls, ports: List[int]) -> List[int]:
        for port in ports:
            if not (1 <= port <= 65535):
                raise ValueError(f"Port {port} must be between 1 and 65535.")
        return ports

class MissionConfig(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]{3,64}$")
    goal: str = Field(..., min_length=10)
    sandbox_profile: SandboxProfile
    model_name: str = Field("gemini-4.0-pro")
    mcp_version: str = Field("3.1", pattern=r"^3\.1$")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "legacy-to-pytest-migration",
                "goal": "Migrate all legacy unittest files to pytest under /tests directory.",
                "sandbox_profile": {
                    "profile_name": "secure-isolation",
                    "vpc_isolated": True,
                    "allowed_ports": [443, 8080],
                    "resource_limits": {"cpu": "4", "memory": "8Gi"}
                },
                "model_name": "gemini-4.0-pro",
                "mcp_version": "3.1"
            }
        }
    }

def validate_and_parse_mission(payload: dict) -> str:
    """Validates Anti-Gravity mission configuration using Pydantic v2."""
    try:
        mission = MissionConfig.model_validate(payload)
        return json.dumps({
            "status": "success",
            "validated_payload": mission.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    payload = {
        "name": "legacy-to-pytest-migration",
        "goal": "Migrate all legacy unittest files to pytest under /tests directory.",
        "sandbox_profile": {
            "profile_name": "secure-isolation",
            "vpc_isolated": True,
            "allowed_ports": [443, 8080],
            "resource_limits": {"cpu": "4", "memory": "8Gi"}
        },
        "model_name": "gemini-4.0-pro",
        "mcp_version": "3.1"
    }
    print(validate_and_parse_mission(payload))
```

## Related tools / concepts
- [Gemini](../ai_knowledge/google-gemini.md) — Multi-modal foundational models underpinning Google agent systems.
- [Project Genie](../ai_knowledge/project-genie.md) — Google DeepMind's generative simulation and world-building engine.
- [Terminus 2](./terminus-2.md) — Raw tmux-based shell-execution baseline and terminal-benchmarking engine.
- [OpenHands](./openhands.md) — Flexible open-source software engineering agent workspace.
- [Cline](../agents/cline.md) — Highly popular VS Code autonomous agentic coding assistant.
- [Aider](./aider.md) — Command-line and terminal-based Git-native pair programming tool.
- [Windsurf](./windsurf.md) — Next-generation developer IDE powered by flow-based agentic architectures.
- [Claude Code](./claude-code.md) — Anthropic's interactive CLI developer agent.
- [Droid](./droid.md) — Autonomous task automation and execution agent.
- [LangGraph](../frameworks/langgraph.md) — Stateful, multi-agent graph orchestration framework.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural patterns for multi-agent chains, routing, and task decomposition.
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — System designs comparing native model-tool calling against MCP tool integration.
- [SHARP Security Benchmark](../../knowledge_base/llm_security_privacy.md) — Evaluation suite measuring security safety limits of LLMs.

## Sources / references
- [Build with Google Anti-Gravity (Google Developers Blog)](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
- [Vertex AI Antigravity Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder/antigravity-overview)
- [Google Cloud Agentic Architecture Guide (December 2026)](https://cloud.google.com/architecture/ai-agents)

## Contribution Metadata
- Last reviewed: 2026-12-14
- Confidence: high
