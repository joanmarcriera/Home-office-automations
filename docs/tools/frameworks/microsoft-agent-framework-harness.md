# Microsoft Agent Framework Harness

## What it is
The **Microsoft Agent Framework Harness** (or simply **Agent Harness**) is the production-grade, supported execution runtime for the Microsoft Agent Framework. Reaching General Availability (GA) alongside **Foundry Hosted Agents** at Build 2026, it transitions the agentic stack from an SDK library to a managed, self-contained binary environment. The Harness wraps models (including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **Llama 4**, and **Gemma 3**) to provide turnkey handling of planning, run-loop management, persistence, compaction, and security policy enforcement.

## What problem it solves
Before the Harness, developers had to manually write orchestration infrastructure—including state persistence, context compaction (to prevent token overflow), runaway safety brakes, manual tool approval prompts, and OpenTelemetry hooks. Research shows that up to 98.4% of high-autonomy agent code (like Claude Code or Codex CLI) is comprised of this harness infrastructure, with only 1.6% devoted to actual decision logic. The Microsoft Agent Framework Harness eliminates this development overhead by acting as a standard, secure, and production-supported runtime that wraps the agent logic, preventing common issues such as infinite agent loops and unmanaged context growth.

## Where it fits in the stack
**Category**: Frameworks & Orchestration.
It represents the runtime execution layer that hosts, governs, and runs agent workflows. It sits directly on top of the Microsoft Agent Framework and Semantic Kernel SDKs, connecting agents with underlying inference layers (such as Azure OpenAI, Anthropic, or custom local model endpoints) and tool integrations (such as the **Model Context Protocol (MCP)**).

## Typical use cases
- **Fleet Governance**: Wrapping diverse model-based agents (e.g. specialized Azure OpenAI or Claude 5.1 agents) in a single unified execution harness to guarantee standard auditing, policy enforcement, and telemetry across the entire enterprise.
- **Runaway Prevention**: Setting rigid execution limits on highly autonomous agents to prevent token draining, infinite tool-calling loops, or rogue operations.
- **Long-Running Task Delegation**: Allowing continuous live-voice conversation agents to delegate complex, background-running reasoning or search queries to decoupled frontier models without interrupting active conversations.
- **Context Preservation**: Automatically maintaining a per-call persistent history and compacting long conversation threads on the fly for heavy agents.

## Strengths
- **Production Runtime vs SDK**: Serves as a single, compiled binary running consistently across local development, Docker containers, and Azure Foundry Hosted Agents.
- **Robust Built-In Features**: Features out-of-the-box support for per-call history persistence, automatic context compaction, structured task planning, local file memory, and OpenTelemetry instrumentation.
- **Ecosystem Integration**: Built-in support for Claude Agent SDK and GitHub Copilot SDK connectors, permitting different agent loops to compose in a single cohesive workflow.
- **Rigid Runaway Brakes**: Incorporates host-side stopping controls (stopping loops after a configurable number of turns) to enforce budget and loop safety.

## Limitations
- **Overhead for Simpler Tasks**: Introduces substantial coordination overhead and state tracking, which may be excessive for single-turn, low-complexity completions.
- **Azure Coupling for Managed Scaling**: Though it can run locally, the consumption-billed target and fleet-level governing dashboards require the Azure Foundry Hosted Agents infrastructure.
- **Opt-In Security Risk warnings**: Powerful capabilities like shell access, local filesystem write access, and background sub-agent spawning require explicit opt-in and emit prominent warnings.

## When to use it
- When deploying autonomous, multi-agent systems in enterprise environments where governance, auditing, and resource tracking are mandatory.
- When working with models of varying capabilities that need a unified runtime to coordinate tool invocation, history tracking, and manual authorization steps.
- When wrapping voice-interaction layers (such as **GPT-Live**) that require background reasoning delegation without losing stream continuity.

## When not to use it
- For simple, light-weight client scripts or chat completions that do not leverage multi-step tool calls or stateful memory.
- When building highly custom, non-standard orchestration frameworks where full-duplex background-delegation patterns are unnecessary.

## Getting started
The Harness can be installed via standard package managers and executed locally as a binary or via Python bindings.

### Installation
```bash
pip install azure-ai-projects azure-identity pydantic>=2.0.0
```

### Running the Harness Agent locally (Python)
Ensure you have the Azure CLI logged in with access to an Azure AI Foundry project.

```python
import asyncio
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize connection
project_client = AIProjectClient.from_connection_string(
    conn_str="YOUR_AZURE_FOUNDRY_CONNECTION_STRING",
    credential=DefaultAzureCredential()
)
```

## CLI examples

### Starting the Harness local binary with custom policy
```bash
# Start the local agent harness runtime, specifying an allowed tools policy JSON
agent-harness-runtime --port 8080 --policy-config ./policies/restrictive-policy.json
```

### Controlling and auditing active Harness Agents via Azure CLI
```bash
# List all active hosted harness instances
az ai agent-harness list --project-name "EnterpriseResearch"

# View live telemetry traces for a running harness instance
az ai agent-harness trace --run-id "run_8f7b2a9d" --follow
```

## API examples
To build highly secure applications, configuration parameters are checked with strict validation via Pydantic v2 schemas before being sent to the Harness agent.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

# Define strict Pydantic v2 schemas to validate Harness settings before execution
class ToolPolicy(BaseModel):
    allowed_tools: List[str] = Field(default_factory=list, description="Names of tools allowed for invocation")
    require_approval: bool = Field(True, description="Enforce human-in-the-loop approval before tool calling")

class HarnessAgentConfig(BaseModel):
    agent_instructions: str = Field(..., min_length=10, description="The core instruction set for the agent")
    max_execution_loops: int = Field(40, ge=1, le=100, description="Runaway loop prevention ceiling")
    enable_telemetry: bool = Field(True, description="Expose OpenTelemetry traces")
    tool_policy: ToolPolicy = Field(default_factory=ToolPolicy, description="Harness safety tool policies")

def validate_and_create_config(raw_data: dict) -> Optional[HarnessAgentConfig]:
    try:
        # Pydantic v2 validation
        config = HarnessAgentConfig.model_validate(raw_data)
        print("Harness configuration successfully validated!")
        return config
    except ValidationError as e:
        print(f"Harness configuration validation failed: {e.errors()}")
        return None

# Example configuration data
harness_data = {
    "agent_instructions": "You are a research assistant. Plan your work, then execute it.",
    "max_execution_loops": 45,
    "enable_telemetry": True,
    "tool_policy": {
        "allowed_tools": ["web_search", "document_reader"],
        "require_approval": True
    }
}

validated_harness_config = validate_and_create_config(harness_data)
```

## Related tools / concepts
- [Microsoft Agent Framework](microsoft-agent-framework.md) - The SDK and conceptual library underlying the Harness.
- [Semantic Kernel](semantic-kernel.md) - The developer SDK integrated within Azure Foundry Agents.
- [AutoGen](autogen.md) - Microsoft's experimental framework for multi-agent conversation patterns.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - The open standard for connecting agents to toolsets.
- [Azure OpenAI](../providers/azure-openai.md) - Prime deployment model provider for the Harness.
- [Aider](../development_ops/aider.md) - Autonomous coding tool using similar architectural harness traits.
- [Claude Code](../development_ops/claude-code.md) - SOTA high-autonomy agent whose harness/runtime infrastructure is analyzed in similar architecture studies.

## Sources / references
- [Microsoft Agent Framework Harness GA News](https://www.infoq.com/news/2026/08/agent-framework-harness-ga/)
- [Microsoft Agent Framework Release Details](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [MBZUAI VILA-Lab Research Paper: Dive into Claude Code](https://arxiv.org/abs/2604.14228)
- [Microsoft Agent Framework at Build 2026 Announcements](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/)
- [Microsoft Agent Lightning Harness Overview](https://thenewstack.io/microsoft-agent-lightning-harness/)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
