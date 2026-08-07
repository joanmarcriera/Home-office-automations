# Jupyter Kernel MCP Server

## What it is
An MCP server providing AI assistants with stateful, persistent Jupyter kernel execution and notebook management. It enables frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4** to maintain complex computational state across an entire conversation. As of late November/December 2026, the **Jupyter Kernel MCP Server v1.5** introduces native support for **MCP 3.1 / FastMCP 3.1** protocol schemas, allowing agents to treat long-running data science experiments as discrete, resumable, and telemetry-monitored tasks.

## What problem it solves
Unlike traditional code execution environments that start fresh for each query, this server maintains variables, imports, and data in memory. This enables incremental data analysis, multi-step software development, and the ability to build documented Jupyter notebooks as part of an agent's reasoning process. It eliminates the "amnesia" problem in AI-driven data exploration by providing a persistent, stateful workspace.

## Where it fits in the stack
**Tool / Eval**. It provides a persistent compute workspace for agents, often used for [Knowledge Base](../../knowledge_base/README.md) expansion and complex [Data Copilot](../../architecture/data-copilot-text-to-sql.md) workflows. It acts as the bridge between conversational agents and professional data science environments.

## Typical use cases
- **Incremental Data Analysis**: Loading a dataset once and performing multiple exploratory turns with live variable checking.
- **Multi-step Development**: Building a complex algorithm turn-by-turn with live verification, visualization, and validation.
- **Notebook Orchestration**: Creating, editing, and searching `.ipynb` files for shared human-AI collaboration.
- **Contextual Reasoning**: Using the `suggest_next()` tool to let the kernel guide the agent based on live memory state.
- **Interactive Visualization**: Generating and persisting charts (matplotlib, plotly) for retrieval in later turns.

## Strengths
- **Persistent State**: Variables, classes, and libraries remain active throughout the session.
- **Polyglot Support**: Works with Python, R, Julia, Go, Rust, and TypeScript kernels.
- **Smart Suggestions**: Late 2026 updates include improved GPT-5.5 and Claude 5.1 optimized prompt injections for cell-level debugging.
- **Full Notebook Lifecycle**: Support for creation, cell-level editing, and full-text search of notebooks.
- **MCP 3.1 / FastMCP 3.1 Native**: Standardized task schemas and real-time computation streaming for seamless execution.

## Limitations
- **External Dependency**: Requires a running Jupyter server or local Jupyter installation.
- **Resource Consumption**: Persistent kernels consume host memory until explicitly shut down or garbage collected.
- **Security Scope**: Execution is as powerful as the host kernel; requires careful sandboxing in multi-tenant environments.
- **State Complexity**: Deeply nested state can occasionally lead to agent confusion if variables are not clearly named or documented.

## When to use it
- For complex data science tasks where dataset loading is expensive.
- When you want an agent to produce a reproducible notebook as a final artifact.
- For long-running experiments spanning multiple turns or chat sessions.
- In interactive data science workflows where agent-human handoffs are frequent.

## When not to use it
- For simple, stateless calculations where a basic `python -c` call would suffice.
- In environments where running a persistent background server is prohibited.
- For high-latency, low-compute tasks where a lightweight MCP server is preferred.

## Getting started

### 1. Installation
Install the server using `uv`:
```bash
uvx mcp-server-jupyter
```

### 2. Connect to Kernel
Verify connectivity by listing available kernels:
```bash
# Via MCP Client
claude mcp call jupyter workspace
```

### 3. Hello World
Execute a simple persistent calculation:
```bash
claude mcp call jupyter compute --code "x = 10; x * 2"
```

## CLI examples

### 1. Kernel Management
Start a specific kernel (e.g., R or Julia):
```bash
mcp-jupyter start --kernel ir
```

### 2. Notebook Conversion
Convert a chat session history into a standalone notebook:
```bash
mcp-jupyter export --session_id "analysis_01" --output results.ipynb
```

### 3. Workspace Audit
List all active kernels and their memory usage:
```bash
mcp-jupyter status --verbose
```

## API examples

### 1. Stateful Execution (compute)
```json
{
  "tool": "compute",
  "arguments": {
    "code": "import pandas as pd\ndf = pd.read_csv('large_dataset.csv')\ndf.describe()"
  }
}
```

### 2. Intelligent Next Steps (suggest_next)
```json
{
  "tool": "suggest_next",
  "arguments": {}
}
// Response: "You have 'df' loaded. Try checking for nulls: df.isnull().sum()"
```

### 3. Notebook Creation (notebook)
```json
{
  "tool": "notebook",
  "arguments": {
    "action": "create",
    "name": "Exploratory_Analysis.ipynb",
    "content": "# Data Analysis\nThis notebook tracks our progress..."
  }
}
```

### 4. Robust Configuration Validation with Pydantic v2
The following Python script illustrates how to model and programmatically validate a Jupyter Kernel MCP Server connection configuration and active kernel profile under late November/December 2026 standards, ensuring strict schema safety and type correctness using Pydantic v2:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class KernelSessionConfig(BaseModel):
    kernel_name: str = Field(default="python3", pattern=r"^(python3|ir|julia-.*|rust|ts-node)$")
    cwd: str = Field(default="/workspace")
    env: Dict[str, str] = Field(default_factory=dict)
    timeout_seconds: int = Field(default=600, ge=10, le=86400)
    memory_limit_mb: int = Field(default=4096, ge=512, le=65536)

    @field_validator("kernel_name")
    @classmethod
    def validate_kernel(cls, v: str) -> str:
        # Custom logic for validating specific kernel names
        return v

class JupyterMCPConfig(BaseModel):
    server_url: str = Field(..., pattern=r"^https?://[a-zA-Z0-9.-]+(:[0-9]+)?(/.*)?$")
    token: str = Field(..., min_length=12)
    session_id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    kernel: KernelSessionConfig = Field(default_factory=KernelSessionConfig)
    mcp_version: str = Field(default="3.1", pattern=r"^3\.1$")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "server_url": "http://localhost:8888",
                "token": "sha256:7f9c8d5e4b3a2f10d9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6",
                "session_id": "data-science-analysis-2026",
                "kernel": {
                    "kernel_name": "python3",
                    "cwd": "/workspace/experiments",
                    "env": {"OMP_NUM_THREADS": "4"},
                    "timeout_seconds": 1800,
                    "memory_limit_mb": 8192
                },
                "mcp_version": "3.1"
            }
        }
    }

def validate_jup_mcp_config(payload: dict) -> str:
    """Validates Jupyter Kernel MCP Server configuration payload using Pydantic v2."""
    try:
        config = JupyterMCPConfig.model_validate(payload)
        return json.dumps({
            "status": "success",
            "validated_config": config.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    test_payload = {
        "server_url": "http://127.0.0.1:8888",
        "token": "abcdef1234567890abcdef1234567890",
        "session_id": "fastmcp-session-330",
        "kernel": {
            "kernel_name": "python3",
            "cwd": "/workspace",
            "env": {"CUDA_VISIBLE_DEVICES": "0"},
            "timeout_seconds": 3600,
            "memory_limit_mb": 16384
        },
        "mcp_version": "3.1"
    }
    print(validate_jup_mcp_config(test_payload))
```

## Related tools / concepts
- [Jupyter](https://jupyter.org/) — The industry-standard notebook environment.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — The protocol this server implements.
- [Agent Protocols](../../knowledge_base/agent_protocols.md) — Standards for agent interaction.
- [MCP Registry](../automation_orchestration/mcp-registry.md) — Discovery for data science MCPs.
- [Python](../ai_knowledge/python.md) — Primary language for Jupyter workflows.
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) — Reference implementation for data-driven agents.
- [Symbolic MCP](symbolic-mcp.md) — Often used in parallel for formal verification of data logic.
- [Claude Code](claude-code.md) — Primary terminal client for managing Jupyter sessions.

## Sources / references
- [Jupyter Kernel MCP GitHub](https://github.com/democratize-technology/jupyter-kernel-mcp)
- [Jupyter Server Documentation](https://jupyter-server.readthedocs.io/)
- [Persistent Computing for AI Agents (June 2026)](https://agentic-ops.example.com/jupyter-mcp)

## Contribution Metadata
- Last reviewed: 2026-12-15
- Confidence: high
