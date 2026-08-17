# AutoGen

## What it is
AutoGen (and AG2) is an open-source framework originally created by Microsoft Research for developing multi-agent LLM applications. It enables developers to construct autonomous systems where multiple AI agents converse with each other, execute code, and leverage tools to solve complex multi-step tasks. In early January 2027, AutoGen v0.4+ serves as an enterprise multi-agent framework orchestrating frontier models like **Claude 5.1 Opus**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and sovereign open-weight models.

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
- **State Management Complexity**: Tracking complex conversational context across dozens of agents in long-running tasks requires explicit persistence configuration.
- **Migration Surface**: Transitioning between legacy AutoGen versions and the updated AG2 / AutoGen v0.4+ event-driven architecture requires code updates.

## When to use it
- When your application requires multiple conversational agents collaborating to solve non-linear problems.
- When automated code generation, sandboxed execution, and interactive feedback loops are core requirements.
- When building complex agent networks with human-in-the-loop validation checkpoints.

## When not to use it
- For deterministic, linear workflows that do not require conversational back-and-forth between specialized agents.
- If you require a strict, graph-based DAG orchestration paradigm without conversational agent autonomy (use [LangGraph](langgraph.md)).

## Getting started

### 1. Installation
Install AutoGen / AG2 via pip:
```bash
pip install pyautogen pydantic
```

### 2. Configuration
Configure API access for models like `claude-5-1-opus-20261031` or `gpt-5.5-preview`.

### 3. Basic Example
```python
import os
from autogen import AssistantAgent, UserProxyAgent

llm_config = {
    "config_list": [
        {
            "model": "gpt-5.5-preview",
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
    message="Write a Python function to compute the Fibonacci sequence up to n terms."
)
```

## CLI examples

### AutoGen Studio UI
Launch the interactive web UI for visual agent configuration:
```bash
autogenstudio ui --port 8081
```

### Docker Execution Environment Setup
Install AutoGen with optional Docker sandboxing support:
```bash
pip install "pyautogen[docker]"
```

### Interactive Execution Mode
Run an agent script forcing interactive human approval for every tool step:
```bash
python main_agent.py --human_input_mode ALWAYS
```

## API examples

### Multi-Agent Group Chat with Pydantic v2 Configuration
Orchestrate a multi-agent coding and critique group chat using Pydantic v2 schemas:

```python
from typing import List
from pydantic import BaseModel, Field
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

class ModelConfig(BaseModel):
    model: str = Field(default="claude-5-1-opus-20261031")
    api_key: str = Field(..., description="API Key for model provider")
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)

class AgentTeamConfig(BaseModel):
    max_rounds: int = Field(default=10, ge=1, le=50)
    work_directory: str = Field(default="workspace")

def run_multi_agent_team(model_cfg: ModelConfig, team_cfg: AgentTeamConfig) -> None:
    llm_config = {
        "config_list": [{
            "model": model_cfg.model,
            "api_key": model_cfg.api_key
        }],
        "temperature": model_cfg.temperature
    }

    coder = AssistantAgent("Coder", llm_config=llm_config)
    critic = AssistantAgent(
        "Critic",
        system_message="Critique proposed code for safety and efficiency.",
        llm_config=llm_config
    )
    user_proxy = UserProxyAgent(
        "User",
        code_execution_config={"work_dir": team_cfg.work_directory, "use_docker": False}
    )

    groupchat = GroupChat(
        agents=[coder, critic, user_proxy],
        messages=[],
        max_round=team_cfg.max_rounds
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy.initiate_chat(
        manager,
        message="Build a FastMCP 3.1 tool server template in Python using Pydantic v2."
    )

if __name__ == "__main__":
    m_cfg = ModelConfig(api_key="your-anthropic-key")
    t_cfg = AgentTeamConfig(max_rounds=12, work_directory="mcp_workspace")
    run_multi_agent_team(m_cfg, t_cfg)
```

## Related tools / concepts
- [CrewAI](crewai.md) - Role-based multi-agent framework.
- [LangGraph](langgraph.md) - Stateful cyclic graph orchestration library.
- [Semantic Kernel](semantic-kernel.md) - Enterprise AI orchestration SDK.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) - Architectural patterns for multi-agent knowledge systems.
- [Plandex](../development_ops/plandex.md) - Terminal-based AI software engineering engine.
- [Smolagents](smolagents.md) - Lightweight agent framework from Hugging Face.
- [Model Context Protocol](../automation_orchestration/mcp.md) - Standard protocol for tool and resource exposure.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) - Design patterns for multi-step agents.

## Sources / references
- [AutoGen GitHub Repository](https://github.com/microsoft/autogen)
- [Official AutoGen Documentation](https://microsoft.github.io/autogen/)
- [AG2 Project Portal](https://ag2.ai/)
- [FastMCP 3.1 Tool Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
