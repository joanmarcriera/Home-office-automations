# NVIDIA NeMo Claw

## What it is
NVIDIA NeMo Claw is an enterprise-grade agent orchestration framework designed for building, deploying, and managing high-performance AI agents. As of late November/December 2026, it serves as the primary agentic layer within the [NVIDIA NIM](../providers/nvidia.md) ecosystem, optimized for the NVIDIA Rubin and Blackwell architectures. NeMo Claw provides a standardized runtime for agentic reasoning, native Model Context Protocol (MCP 3.1) support, and deep integration with TensorRT-LLM for low-latency tool execution.

## What problem it solves
NeMo Claw addresses the "inference-to-action" latency gap in production agent deployments. It simplifies the orchestration of complex, multi-agent systems by providing standardized patterns for model serving via NVIDIA NIM, secure tool-calling validation, and sandboxed execution. It solves the scalability challenges of deploying agents across [K3s clusters](../infrastructure/k3s.md) and provides built-in mechanisms for MCP 3.1 / FastMCP 3.1 Task Protocol coordination, ensuring reliable tool use in industrial environments.

## Where it fits in the stack
NeMo Claw sits in the **Agent Framework / Orchestration Layer**. It functions as the management plane that connects NVIDIA-optimized models (like [Nemotron](../ai_knowledge/nemotron.md), Qwen 3.6, and Llama 4) to external tools and enterprise data sources, leveraging the [NVIDIA AI Enterprise](../providers/nvidia.md) stack for hardware-accelerated performance.

## Typical use cases
- **Autonomous Data Center Management**: Coordinating agents on Rubin-class clusters to monitor power distribution and optimize cooling in real-time.
- **Industrial Multi-Agent Orchestration**: Managing fleets of specialized agents in smart factories using FastMCP 3.1 for tool discovery and execution.
- **Enterprise-Grade Customer Support**: Deploying high-throughput agents with persistent memory and secure tool access via NVIDIA NIM.
- **GPU-Accelerated Scientific Research**: Automating high-fidelity simulations and data analysis on NVIDIA DGX systems.

## Strengths
- **Rubin & Blackwell Architecture Optimization**: Native support for the NVIDIA Rubin and Blackwell architectures, providing unprecedented efficiency for agentic reasoning loops.
- **NVIDIA NIM Integration**: Seamlessly pulls and manages models via NVIDIA Inference Microservices (NIM), now in General Availability (GA).
- **Native FastMCP 3.1 Support**: Full implementation of the MCP 3.1 Task Protocol for standardized tool-calling and agent coordination.
- **Production-Ready Scalability**: Optimized for deployment in [Docker](../infrastructure/docker.md) and Kubernetes environments using the NVIDIA GPU Operator.
- **Security & Guardrails**: Integrated with NeMo Guardrails to ensure agent outputs and tool calls remain safe and compliant.

## Limitations
- **Hardware Affinity**: Maximum performance gains are strictly tied to NVIDIA GPU infrastructure, particularly Rubin and Blackwell.
- **Infrastructure Complexity**: Requires familiarity with the NVIDIA software stack and container orchestration.
- **Proprietary Lock-in**: While supporting open models, the most advanced features are optimized for the NVIDIA ecosystem.

## When to use it
- When building production-scale multi-agent systems that require sub-millisecond reasoning latency.
- If your infrastructure is centered on [NVIDIA GPU](../providers/nvidia.md) clusters, especially the Rubin architecture.
- When enterprise-grade security, monitoring, and MCP-based tool orchestration are mandatory.
- If you are already leveraging [TensorRT-LLM](../infrastructure/tensorrt-llm.md) for model inference.

## When not to use it
- For simple, non-production personal automations that do not require GPU acceleration.
- In environments where you lack access to NVIDIA hardware or the NVIDIA NIM ecosystem.
- If your primary requirement is a lightweight, zero-dependency framework for [Local LLMs](../ai_knowledge/local_llms.md) on consumer CPUs.

## Getting started
### Prerequisite: NVIDIA NIM
NeMo Claw requires a running NVIDIA NIM instance. Ensure your environment is configured for [Docker](../infrastructure/docker.md) with the NVIDIA Container Toolkit.

```bash
# Pull and start a Nemotron NIM
docker run --gpus all -p 8000:8000 nvcr.io/nim/nvidia/nemotron-4-340b-instruct:latest
```

### Installation
Install the NeMo Claw SDK and the MCP 3.1 client:

```bash
pip install nemoclaw-sdk mcp-python-sdk pydantic
```

### Hello World Agent
```python
from nemoclaw import Agent
from mcp.client import MCPClient

# Initialize the MCP client for tool discovery
mcp_client = MCPClient(server_url="http://localhost:8080")

# Initialize the NeMo Claw agent
agent = Agent(
    model="nemotron-4-340b-instruct",
    endpoint="http://localhost:8000/v1",
    mcp_context=mcp_client.get_context()
)

# Execute a simple task
response = agent.run("Check the cluster health using the monitoring tool.")
print(response.output)
```

## CLI examples
```bash
# Initialize a new agent sandbox
nemoclaw init my-agent

# Register an MCP server with the agent
nemoclaw mcp add-server http://localhost:8080/mcp

# Deploy the agent to a K3s cluster
nemoclaw deploy --target k3s --namespace production

# Monitor agentic reasoning loops in real-time
nemoclaw trace my-agent --live

# Update security guardrails for all active agents
nemoclaw guardrails update ./configs/security-policy.yaml
```

## API examples

### NeMo Claw Telemetry & Response Schema Verification (Pydantic v2)
For mission-critical operations, NeMo Claw execution payloads and tool dispatch telemetry can be strictly validated using Pydantic v2. This ensures no malformed tool calls enter physical data center execution layers:

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class NIMInferenceMetrics(BaseModel):
    gpu_utilization: float = Field(..., ge=0.0, le=100.0, description="NVIDIA Rubin/Blackwell GPU utilization percentage.")
    time_to_first_token_ms: float = Field(..., ge=0.0)
    tokens_per_second: float = Field(..., ge=0.0)

class NeMoClawPayload(BaseModel):
    agent_id: str
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    n_tokens: int = Field(..., ge=1)
    mcp_server_invoked: Optional[str] = None
    telemetry_metrics: NIMInferenceMetrics
    security_verdict: str = Field("approved")

    @field_validator("security_verdict")
    @classmethod
    def check_verdict(cls, val: str) -> str:
        allowed = {"approved", "blocked", "flagged_by_guardrails"}
        if val not in allowed:
            raise ValueError(f"Verdict must be one of {allowed}")
        return val

# Verify incoming execution response from a NeMo Claw REST interface
sample_payload = {
    "agent_id": "production-monitor-rubin01",
    "run_id": "claw-run-44810-2026",
    "n_tokens": 1056,
    "mcp_server_invoked": "http://localhost:8080/mcp/fastmcp-3.1",
    "telemetry_metrics": {
        "gpu_utilization": 82.5,
        "time_to_first_token_ms": 11.4,
        "tokens_per_second": 120.5
    },
    "security_verdict": "approved"
}

validated_run = NeMoClawPayload(**sample_payload)
print(f"Validated Run ID: {validated_run.run_id}")
print(f"Inference Speed: {validated_run.telemetry_metrics.tokens_per_second} tok/sec")
```

## Related tools / concepts
- [NVIDIA NIM](../providers/nvidia.md): The backbone for model serving in NeMo Claw.
- [TensorRT-LLM](../infrastructure/tensorrt-llm.md): High-performance inference engine.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Standard for tool and data integration.
- [K3s](../infrastructure/k3s.md): Lightweight Kubernetes for edge agent deployment.
- [Docker](../infrastructure/docker.md): Standard containerization for NeMo environments.
- [Nemotron](../ai_knowledge/nemotron.md): NVIDIA's frontier models optimized for NeMo Claw.
- [Local LLMs](../ai_knowledge/local_llms.md): Guide for running models on-premises.

## Sources / references
- [NVIDIA Developer Blog: NeMo Claw GA and Rubin Support (July 2026)](https://developer.nvidia.com/blog/nemoclaw-ga-rubin-architecture)
- [Official NVIDIA NeMo Documentation](https://docs.nvidia.com/nemoclaw/)
- [MCP 3.1 Task Protocol Specification](https://modelcontextprotocol.org/docs/task-protocol)
- [NVIDIA NIM User Guide](https://docs.nvidia.com/nim/)

## Contribution Metadata
- Last reviewed: 2026-11-28
- Confidence: high
