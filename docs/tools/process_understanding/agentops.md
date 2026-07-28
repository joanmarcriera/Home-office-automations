# AgentOps

## What it is
AgentOps is a specialized, enterprise-ready observability, tracking, and evaluation platform built specifically for autonomous agents. It provides developers with an end-to-end suite of tools for tracing agentic execution paths, debugging multi-step logic chains, monitoring API spends, and benchmarking agent behaviors across diverse environments.

## What problem it solves
Developing autonomous agents is uniquely challenging due to their non-deterministic nature, complex multi-turn decision frameworks, and vulnerability to logical failures. AgentOps resolves the "black box" complexity of agentic systems by providing:
- **Comprehensive Trace Visualization**: Interactive event graphs detailing exactly when and why an agent chose a specific tool or route.
- **Loop and Recursive Guardrails**: Real-time detection and alerting for infinite execution loops, recursive thoughts, and reasoning traps.
- **Granular Cost Tracking**: Instant reporting on API usage and expenditures across 400+ LLM backends via native gateways like [LiteLLM](../../services/litellm.md).
- **Automated Agent Evaluations**: Vetted benchmarking tools to evaluate agent performance over time and prevent system regressions.

## Where it fits in the stack
**AI Observability and Developer Tooling**. Sitting at the monitoring and evaluation layer, it connects directly into agentic codebases. It is deeply integrated with the **Model Context Protocol (MCP 3.1)** and standard multi-agent orchestration frameworks.

## Typical use cases
- **Multi-Agent Flow Monitoring**: Tracking handoffs, communication packets, and dependency relationships between cooperating agents in frameworks like [CrewAI](../frameworks/crewai.md) or AG2 ([AutoGen](../frameworks/autogen.md)).
- **MCP Tool Interception**: Analyzing latency, input payloads, and failure thresholds for queries directed to [MCP](../automation_orchestration/mcp.md) servers.
- **Session Replay Diagnostics**: Replaying entire user-agent sessions in production to analyze failure modes and optimize prompts.
- **Enterprise Spend Auditing**: Continuous auditing and control of commercial API budgets for large-scale, long-running agent squads.
- **Dataset Extraction for Fine-Tuning**: Exporting successful agent execution traces to create clean training datasets for specialized local models.

## Strengths
- **Native Framework Integrations**: Minimal-boilerplate setup for industry-standard packages, including [CrewAI](../frameworks/crewai.md), [AutoGen](../frameworks/autogen.md), LangChain, and LlamaIndex.
- **Dynamic Session Dashboard**: Intuitive, agent-first visual platform featuring detailed execution logs and tool call traceboards.
- **PII and Guardrail Defenses**: Integrated prompt injection defenses, PII detection, and honeypot alerts (powered by PromptArmor).
- **Local Sandbox Execution Tracking**: Correlates filesystem edits and shell commands executed by code-generation assistants back to specific agent sessions.

## Limitations
- **Highly Specialized**: Tailored entirely for agentic workflows; standard RAG or basic completion APIs may find the platform over-engineered.
- **Cloud Dependency**: While core tracking metrics are available locally, advanced dashboard visualization and analytics require connecting to the AgentOps cloud.
- **Instrumentation Overhead**: To extract maximum value, developers must properly instrument custom tools and custom agent classes.

## When to use it
- When developing complex, multi-agent orchestrations that require systematic auditing of tool handoffs.
- When deploying production-grade agents that execute commands autonomously and require a "flight recorder" to debug failures.
- When integrating with standard agent frameworks like [CrewAI](../frameworks/crewai.md) or [AutoGen](../frameworks/autogen.md) where AgentOps can be enabled with single-line configuration changes.

## When not to use it
- For trivial, synchronous LLM integrations where simple request/response proxies (like [Helicone](helicone.md)) are faster and simpler.
- If you have strict regulations completely banning external cloud telemetry, and you do not have an enterprise contract to run the private AgentOps stack.

## Getting started

### Installation
Install the official AgentOps Python library via pip:

```bash
pip install agentops pydantic
```

### Basic Framework Integration (Python)
To initialize session recording, instantiate the client. AgentOps automatically detects and hooks into supported active frameworks (e.g., CrewAI) when initialized:

```python
import os
import agentops

# Initialize AgentOps tracing session
# Looks for AGENTOPS_API_KEY inside environment variables automatically
agentops.init(
    api_key=os.environ.get("AGENTOPS_API_KEY"),
    tags=["production", "auth-migration"]
)

# Your agentic and multi-agent execution logic goes here...

# Ensure session is safely terminated and flushed
agentops.end_session(end_state="Success")
```

## CLI examples

### Initializing a Project
Configure your local environment with your unique developer key:
```bash
export AGENTOPS_API_KEY="your_secure_agentops_api_key_here"
```

### Direct Session Verification
```bash
# Query active session states via inline Python command
python3 -c "import agentops; print(agentops.get_api_key())"
```

### Exporting Local Logs
```bash
# Export successful session trace data for local model evaluations
agentops export --session_id "sess_987654321" --format json --output-dir ./traces
```

## API examples

### Recording Programmatic MCP 3.1 Tool Runs
Below is a structured Python example showing how to programmatically track and log custom MCP 3.1 tool operations using safe exception checks and AgentOps decorators.

```python
import os
import sys
import agentops
from agentops.sdk.decorators import agent, operation

@agent
class DeveloperAgent:
    """An autonomous agent persona instrumented for tracing by AgentOps."""
    def __init__(self, name: str):
        self.name = name

    @operation
    def run_mcp_validation_tool(self, tool_name: str, parameters: dict) -> str:
        """Invokes an MCP tool and logs the interaction detail directly to AgentOps."""
        print(f"[{self.name}] Calling MCP 3.1 tool '{tool_name}'...")

        try:
            # Record explicit tool call action manually for fine-grained telemetry
            agentops.record_action(
                f"Invoke MCP Tool: {tool_name}",
                params={
                    "parameters": parameters,
                    "mcp_version": "3.1"
                }
            )
            # Simulated tool execution logic
            result = f"Successfully validated configuration for: {parameters.get('target', 'unknown')}"
            return result
        except Exception as e:
            print(f"Error during tool recording: {e}", file=sys.stderr)
            return "Execution Failed"

if __name__ == "__main__":
    # Ensure client is initialized
    api_key = os.environ.get("AGENTOPS_API_KEY")
    if not api_key:
        print("Warning: Missing AGENTOPS_API_KEY. Session will not be uploaded.", file=sys.stderr)

    agentops.init(api_key=api_key, tags=["mcp-tool-verification"])

    # Spawn and invoke the instrumented agent
    dev_agent = DeveloperAgent("SystemArchitect")
    dev_agent.run_mcp_validation_tool(
        tool_name="validate_tsconfig",
        parameters={"target": "src/tsconfig.json", "strict": True}
    )

    agentops.end_session(end_state="Success")
    print("==> Telemetry session uploaded to AgentOps dashboard!")
```

### Multi-Model Trajectory Log
```python
import agentops

# Initialize session tagging
agentops.init(tags=["frontier-eval-test"])

# Track trajectory spanning Claude 5.1 and GPT-5.5
# ... model inference runs ...

agentops.end_session(end_state="Success")
```

## Related tools / concepts
- [Langfuse](langfuse.md) - Open-source alternative with strong prompt management.
- [Helicone](helicone.md) - Proxy-based LLM observability.
- [Arize AI](arize-ai.md) - Enterprise-grade observability and evaluation.
- [W&B Weave](wandb-weave.md) - Lightweight tracing for ML workflows.
- [MCP](../automation_orchestration/mcp.md) - Protocol for connecting agents to data/tools.
- [Claude](../ai_knowledge/claude.md) - Primary frontier model for agentic workflows.
- [CrewAI](../frameworks/crewai.md) - Multi-agent framework with native AgentOps support.
- [AutoGen](../frameworks/autogen.md) - Microsoft's agent orchestration framework.
- [LiteLLM](../../services/litellm.md) - Gateway that integrates with AgentOps for cost tracking.

## Sources / references
- [AgentOps Official Website](https://www.agentops.ai/)
- [AgentOps Documentation](https://docs.agentops.ai/introduction)
- [AgentOps GitHub Repository](https://github.com/AgentOps-AI/agentops)

## Contribution Metadata
- Last reviewed: 2026-10-24
- Confidence: high
