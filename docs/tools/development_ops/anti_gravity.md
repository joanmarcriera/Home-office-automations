# Anti-Gravity

## What it is
Anti-Gravity (v2026.4.x+) is Google's premier agentic development and execution framework, engineered to build, orchestrate, and deploy autonomous AI agents. It utilizes the Gemini 3.5 series (Ultra/Flash/Pro), Gemini Spark, and Gemini Omni models, and natively supports the Model Context Protocol (MCP 3.0/3.1) to expose surfaces and execute stateful, long-horizon tasks ("Missions") across complex software ecosystems.

## What problem it solves
Anti-Gravity addresses the "Complexity Wall" in autonomous software engineering. It simplifies the creation of agents that can safely refactor multi-million line codebases, handle cross-repository dependencies, and maintain state over long-running asynchronous tasks, reducing the boilerplate associated with manual LLM orchestration and tool-calling loops. It mitigates token ingestion bottlenecks and execution loop failures by natively integrating state checkpointing, execution-aware compression, and multi-modal sandbox isolation.

## Where it fits in the stack
**Development & Ops**. It serves as the primary framework for building "Antigravity Agents" within the Google Cloud and Vertex AI ecosystems. It bridges the gap between raw LLM capabilities and production-grade autonomous agent deployments.

## Typical use cases
- **Autonomous Refactoring**: Large-scale migrations (e.g., Python 3.10 to 3.13) across multiple microservices.
- **Agentic CI/CD**: Integrating agents into the deployment pipeline to automatically fix test failures or security vulnerabilities.
- **Legacy Modernization**: Systematically analyzing and rewriting legacy COBOL or Java services into modern Go/Python architectures.
- **Architectural Discovery**: Autonomous mapping of undocumented system dependencies and data flows.
- **SOTA Mission Execution**: Deploying long-range, self-correcting agent missions that interface with external networks via MCP 3.0/3.1 client/server standard transports.

## Strengths
- **Native Gemini Integration**: Optimized for Gemini's 2M+ token context window and native code execution capabilities.
- **Mission Abstraction**: Sophisticated handling of multi-step, stateful operations with built-in checkpointing, rollback, and recovery.
- **Enterprise Security**: Native integration with Google Cloud IAM, VPC Service Controls, and SHARP-compliant security guardrails.
- **Advanced Observability**: Detailed tracing of agent reasoning steps and state telemetry via integration with Google Cloud Operations (formerly Stackdriver) and MCP 3.1 streaming telemetry.
- **Multi-Agent Capabilities**: Direct support for orchestrating dual-agent pipelines (such as Vertex AI Agents cooperating with external Claude 5.1 missions).

## Limitations
- **Ecosystem Lock-in**: Deeply tied to Google Cloud and Vertex AI infrastructure.
- **Experimental Features**: Some high-level "Autonomous Surface" capabilities remain in developer preview.
- **Cost**: High-frequency use of Gemini Ultra for complex reasoning can be expensive compared to local models.

## When to use it
- When building production-grade autonomous agents for enterprise-scale software engineering.
- When your organization is already standardized on Google Cloud Platform (GCP).
- For tasks requiring massive context (e.g., auditing an entire repository in a single prompt).
- When utilizing Gemini Spark or Gemini Omni features for multimodal agent workflows.

## When not to use it
- For small, local-only coding tasks where [Aider](./aider.md) or [Cline](../agents/cline.md) is sufficient.
- When working in a multi-cloud or AWS/Azure-centric environment (consider [OpenHands](./openhands.md)).
- If you require full transparency and local execution of the agent framework's logic (consider [LangGraph](../frameworks/langgraph.md)).

## Getting started
Anti-Gravity is accessed via the Vertex AI Agent Builder or the `antigravity` Python SDK.

### 1. Installation
```bash
pip install google-cloud-antigravity==2026.4.2
```

### 2. Authentication
```bash
gcloud auth application-default login
```

### 3. Basic Mission Definition
Define a `mission.yaml` to specify the agent's goal and constraints:
```yaml
mission:
  goal: "Migrate all legacy unittest cases to pytest"
  surface:
    repo: "git@github.com:my-org/core-service.git"
    branch: "agent/pytest-migration"
  rules:
    - "Do not modify the CI configuration"
    - "Ensure 100% test parity"
```

## CLI examples
- **Spawn a new mission**:
  ```bash
  antigravity missions launch --config mission.yaml --mode autonomous
  ```
- **Inspect agent reasoning**:
  ```bash
  antigravity missions trace <mission_id> --format=live
  ```
- **Intervene in an active mission**:
  ```bash
  antigravity missions feedback <mission_id> "Focus on the auth module first"
  ```
- **List active surfaces**:
  ```bash
  antigravity surfaces list --project my-gcp-project
  ```

## API examples
The Anti-Gravity SDK allows for programmatic mission orchestration and MCP tool integration:

```python
from google.cloud import antigravity

client = antigravity.AgentServiceClient()

# Define the operational surface with MCP 3.0/3.1 server tools
surface = antigravity.Surface(
    repository="https://source.developers.google.com/p/my-proj/r/my-repo",
    context_depth="high",
    mcp_servers=[
        "mcp://localhost:8080/filesystem",
        "mcp://localhost:8081/database"
    ]
)

# Launch an autonomous mission utilizing Gemini 3.5 Pro/Spark capabilities
mission = client.create_mission(
    parent="projects/my-proj/locations/us-central1",
    mission={
        "goal": "Identify and fix all potential memory leaks in the ingestion service",
        "surface": surface,
        "mode": antigravity.MissionMode.AUTONOMOUS
    }
)

print(f"Mission launched: {mission.name}")
```

## Related tools / concepts
- [Gemini](../ai_knowledge/google-gemini.md)
- [OpenHands](./openhands.md)
- [Cline](../agents/cline.md)
- [LangGraph](../frameworks/langgraph.md)
- [Aider](./aider.md)
- [Windsurf](./windsurf.md)
- [Claude Code](./claude-code.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [SHARP Security Benchmark](../../knowledge_base/llm_security_privacy.md)
- [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder)

## Sources / references
- [Build with Google Anti-Gravity (Google Developers Blog)](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
- [Vertex AI Antigravity Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder/antigravity-overview)
- [Google Cloud Agentic Architecture Guide (June 2026)](https://cloud.google.com/architecture/ai-agents)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
