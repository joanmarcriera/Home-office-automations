# AutoGen

## What it is
AutoGen (and AG2) is an open-source framework originally created by Microsoft Research for developing multi-agent LLM applications. It enables developers to construct autonomous systems where multiple AI agents converse with each other, execute code, and leverage tools to solve complex multi-step tasks. In early January 2027, AutoGen v0.4+ serves as an enterprise multi-agent framework orchestrating frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Qwen 3.6 VL** across distributed environments.

### Core Multi-Agent Topology & Communication Loop
AutoGen's execution model is built on event-driven agent message routing where `ConversableAgent` entities exchange structured messages containing text, tool invocation payloads, sandboxed code execution directives, and system signals.

```
+-----------------------------------------------------------------------------------+
|                            AUTOGEN GROUPCHAT MANAGER                              |
|   +-------------------+    +--------------------+    +------------------------+   |
|   | GroupChatManager  |    | FSM State Router   |    | FastMCP 3.1 Connector  |   |
|   | (Speaker Selection|    | (Transition Graph) |    | (Tool Registry Proxy)  |   |
|   +---------+---------+    +---------+----------+    +-----------+------------+   |
+-------------|------------------------|---------------------------|----------------+
              | Broadcast Message      | Next Speaker Token        | Tool Results
              v                        v                           v
+-----------------------------------------------------------------------------------+
|                              CONVERSABLE AGENT POOL                               |
|   +------------------+     +-------------------+     +------------------------+   |
|   | Software Coder   |     | Security Critic   |     | Sandboxed Executor     |   |
|   | (DeepSeek-V4)    |     | (Claude 5.6)      |     | (Docker / WASM Core)   |   |
|   +--------+---------+     +---------+---------+     +-----------+------------+   |
+------------|-------------------------|---------------------------|----------------+
             | Code Patch              | Safety Audit              | Execution Log
             +-------------------------+---------------------------+
                                       |
                                       v
                       +-------------------------------+
                       | Consolidated Output Artifact  |
                       +-------------------------------+
```

## What problem it solves
Complex real-world tasks require specialized domain roles, multi-turn reasoning loops, code execution, and human-in-the-loop approvals that single-prompt pipelines cannot handle. AutoGen automates multi-agent conversation management, state routing, and tool integration through **Model Context Protocol (FastMCP 3.1)** standards.

## Where it fits in the stack
**Framework / Multi-Agent Orchestration**. It operates between foundation models and downstream business applications, coordinating agent interactions, sandbox execution environments, and state management. It directly implements [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) design architectures.

## Typical use cases
- **Automated Software Engineering**: A team of Coder, Reviewer, and Test Runner agents collaboratively writing, debugging, and executing code in sandboxes.
- **Hierarchical Group Chat**: Specialized agents (e.g., Domain Expert, Analyst, Project Manager) engaging in multi-turn discussions to reach structured consensus.
- **Human-in-the-Loop Operations**: Critical workflows where agents propose plans or executed code but pause for human review before execution.
- **Dynamic FSM Workflows**: Utilizing Finite State Machine (FSM) transition rules to route execution between specialized agents based on task status.

## Strengths
- **Customizable Agent Behaviors**: Agents can be granularly configured with distinct system prompts, model endpoints, and tool sets.
- **Isolated Code Execution**: Built-in support for executing agent-generated Python and Bash code within secure Docker or WASM containers.
- **Diverse Interaction Topologies**: Native primitives for two-agent chats, group chats, nested chats, and sequential agent pipelines.
- **FastMCP 3.1 Tooling Support**: Native integration with the Model Context Protocol, enabling agents to tap into enterprise tools and data sources.

## Limitations
- **Token Overhead**: Unconstrained multi-agent conversation loops can lead to elevated token consumption and higher API costs if max round limits are not enforced.
- **State Management Complexity**: Tracking complex conversational context across dozens of agents in long-running tasks requires explicit persistence configuration (e.g. Redis or SQLite checkpointers).
- **Migration Surface**: Transitioning between legacy AutoGen versions and the updated AG2 / AutoGen v0.4+ event-driven architecture requires code updates.

## When to use it
- When your application requires multiple conversational agents collaborating to solve non-linear problems.
- When automated code generation, sandboxed execution, and interactive feedback loops are core requirements.
- When building complex agent networks with human-in-the-loop validation checkpoints.

## When not to use it
- For deterministic, linear workflows that do not require conversational back-and-forth between specialized agents.
- If you require a strict, graph-based DAG orchestration paradigm without conversational agent autonomy (use [LangGraph](langgraph.md)).

## Getting started

### Installation
Install AutoGen / AG2 via pip:
```bash
pip install pyautogen fastmcp pydantic
```

### Configuration
Configure API access for models like `claude-5.6` or `gpt-5.6`.

### Basic Multi-Agent Chat
```python
import os
from autogen import AssistantAgent, UserProxyAgent

llm_config = {
    "config_list": [
        {
            "model": "gpt-5.6",
            "api_key": os.environ.get("OPENAI_API_KEY", "mock-key")
        }
    ],
    "temperature": 0.2
}

assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to compute prime numbers using Eratosthenes Sieve."
)
```

## CLI examples

```bash
# Launch AutoGen Studio interactive orchestration UI
autogenstudio ui --port 8081

# Run agent suite inside secure Docker execution sandbox
python -m autogen.agentchat.realtime --config agent_config.json --use-docker

# Inspect execution state and active conversational turns
autogen-cli status --session-id sess-9941
```

## API examples

### FastMCP 3.1 Server Integration with AutoGen
AutoGen agents can seamlessly bind to **FastMCP 3.1** servers to invoke external API tools safely.

```python
import os
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

# Initialize FastMCP Server for AutoGen agents
mcp = FastMCP("AutoGen Tool Registry", dependencies=["pydantic", "fastmcp"])

class CodeExecutionRequest(BaseModel):
    language: str = Field(..., pattern=r"^(python|bash|javascript)$")
    script: str = Field(..., min_length=5, description="Source code to execute inside sandbox")
    timeout_seconds: int = Field(30, ge=5, le=300)

    @field_validator("script")
    def check_non_empty(cls, v: str) -> str:
        if "rm -rf /" in v or "import os; os.system" in v:
            raise ValueError("Dangerous execution command blocked by safety policy.")
        return v

@mcp.tool()
def execute_sandboxed_code(req: CodeExecutionRequest) -> dict:
    """FastMCP 3.1 tool endpoint for sandboxed agent code execution."""
    # Simulated sandbox execution response
    return {
        "status": "completed",
        "exit_code": 0,
        "stdout": "Execution completed successfully.\nResult: [2, 3, 5, 7, 11]",
        "execution_time_sec": 0.42
    }

if __name__ == "__main__":
    mcp.run()
```

### Strict Multi-Agent GroupChat & Pydantic v2 Schema Validation
This example configures an AutoGen `GroupChat` with strict Pydantic v2 configuration checks and output parsers:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

class LLMModelConfig(BaseModel):
    model: str = Field("claude-5.6", description="Target foundation model identifier")
    api_key: str = Field(..., min_length=10, description="API credential key")
    temperature: float = Field(0.0, ge=0.0, le=1.0)

class AutoGenTeamConfig(BaseModel):
    max_rounds: int = Field(15, ge=1, le=50, description="Max conversational rounds")
    work_directory: str = Field("autogen_workspace", min_length=3)
    enable_docker: bool = Field(True, description="Enforce Docker container sandboxing")

class AgentConsensusResult(BaseModel):
    session_id: str = Field(...)
    status: str = Field(..., pattern=r"^(consensus_reached|max_rounds_exceeded|failed)$")
    final_artifact: Optional[str] = Field(None)
    rounds_executed: int = Field(..., ge=1)

    @model_validator(mode="after")
    def validate_artifact(self) -> "AgentConsensusResult":
        if self.status == "consensus_reached" and not self.final_artifact:
            raise ValueError("Consensus status requires a non-empty final artifact payload.")
        return self

def orchestrate_autogen_team(m_cfg: LLMModelConfig, t_cfg: AutoGenTeamConfig) -> AgentConsensusResult:
    llm_dict = {
        "config_list": [{"model": m_cfg.model, "api_key": m_cfg.api_key}],
        "temperature": m_cfg.temperature
    }

    coder = AssistantAgent("Coder_Agent", llm_config=llm_dict)
    critic = AssistantAgent("Security_Critic", system_message="Audit code for security.", llm_config=llm_dict)
    user_proxy = UserProxyAgent("User_Proxy", code_execution_config={"work_dir": t_cfg.work_directory, "use_docker": False})

    groupchat = GroupChat(agents=[coder, critic, user_proxy], messages=[], max_round=t_cfg.max_rounds)
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_dict)

    # Simulated completion payload
    raw_output = {
        "session_id": "sess-8821-ag",
        "status": "consensus_reached",
        "final_artifact": "def sieve(n):\n    # Optimized Eratosthenes Sieve\n    ...",
        "rounds_executed": 6
    }
    return AgentConsensusResult.model_validate(raw_output)

if __name__ == "__main__":
    model_conf = LLMModelConfig(api_key="mock_anthropic_api_key_12345")
    team_conf = AutoGenTeamConfig(max_rounds=20, work_directory="mcp_workspace")
    res = orchestrate_autogen_team(model_conf, team_conf)
    print("Validated Consensus Output:", res.model_dump_json(indent=2))
```

## Multi-Agent Framework Benchmark Comparison

| Feature / Dimension | AutoGen (AG2) | LangGraph | CrewAI | Smolagents |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Paradigm** | Conversational Agents | Stateful Graph (DAG/Cyclic) | Role-Based Crew Teams | Code-Agent ReAct Loops |
| **FastMCP 3.1 Support** | Native Protocol Binding | Node Integration | Extension Adapter | Native Python Tools |
| **Code Execution Sandbox**| Native Docker / WASM | Code Interpreter Nodes | Docker Sandbox | E2B / Local Python Exec |
| **Human-in-the-loop** | Native Interruption Hooks | State Checkpoint Interrupt | Step Review Callback | Step Callback |
| **State Persistence** | SQLite / Redis Checkpoint | Postgres / Redis Saver | Memory Storage (Chroma) | Minimal In-Memory |
| **Consensus Mechanism** | Conversational GroupChat | Graph Conditional Routing | Sequential Handoff | ReAct Action Loop |

## Operational & Troubleshooting Guide

### 1. Infinite Conversational Loops Between Agents
- **Symptom**: Coder and Critic agents continuously send repetitive correction messages without reaching completion.
- **Cause**: Missing explicit termination condition phrase or unconstrained `max_rounds`.
- **Resolution**:
  1. Always define `is_termination_msg` callback in agent config checking for `TERMINATE`.
  2. Cap `max_rounds` in `GroupChat` definition (e.g., `max_round=15`).

### 2. Context Window Overflow in GroupChats
- **Symptom**: Agents throw `InvalidRequestError: context length exceeded` after 8-10 turns.
- **Cause**: Multi-agent message history accumulates all turns across all agents.
- **Resolution**: Enable message transform filters or summary compression:
  ```python
  from autogen.agentchat.contrib.capabilities import transforms

  context_handling = transforms.LimitChatMessageCount(max_messages=10)
  coder.register_capability(context_handling)
  ```

### 3. Docker Socket Permission Error
- **Symptom**: UserProxyAgent fails with `docker.errors.DockerException: Error while fetching server API version`.
- **Cause**: Current user lacks read/write access to `/var/run/docker.sock`.
- **Resolution**:
  Add user to docker group or pass `use_docker=False` during local development testing:
  ```bash
  sudo usermod -aG docker $USER
  ```

## Related tools / concepts
- [CrewAI](crewai.md) — Role-based multi-agent framework.
- [LangGraph](langgraph.md) — Stateful cyclic graph orchestration library.
- [Semantic Kernel](semantic-kernel.md) — Enterprise AI orchestration SDK.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — Architectural patterns for multi-agent systems.
- [Smolagents](smolagents.md) — Lightweight code-agent framework.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard protocol for tool and resource exposure.

## Sources / references
- [AutoGen GitHub Repository](https://github.com/microsoft/autogen)
- [Official AutoGen Documentation](https://microsoft.github.io/autogen/)
- [AG2 Project Portal](https://ag2.ai/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
