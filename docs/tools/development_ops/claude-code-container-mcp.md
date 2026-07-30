# Claude Code Container MCP Server

## What it is
An Model Context Protocol (MCP 3.1) server that manages containerized Claude Code sessions, transforming the CLI tool into an orchestratable, isolated service. It allows reasoning models like **Claude 5.1** and **GPT-5.5** to manage their own execution environments securely via Docker.

## What problem it solves
It enables AI assistants to create and control isolated Claude Code instances programmatically. It provides Docker-based isolation, multi-session management, and support for **AWS Bedrock**, making it suitable for enterprise AI-to-AI workflows. It solves the risk of an agent performing destructive actions on a host machine by confining the agent to a disposable container.

## Where it fits in the stack
**Tool / Orchestration**. It provides a managed environment for running other coding agents, following the [Agent Protocols](../../knowledge_base/agent_protocols.md) for structured tool interaction and MCP 3.1 communication.

## Typical use cases
- Parallel development workflows (managing different microservices in separate, isolated containers).
- Automated code reviews in CI/CD pipelines using GitHub Actions.
- Enterprise batch operations across multiple legacy repositories.
- Running Claude Code with **AWS Bedrock** for enterprise compliance and data residency.

## Strengths
- **Isolation**: Docker containers protect the host system and isolate projects from each other.
- **Scalability**: Can run dozens of Claude Code sessions simultaneously on a single host.
- **AWS Bedrock Integration**: Native support for AWS enterprise LLM endpoints for secure, compliant inference.
- **Programmable API**: Full MCP tools for creating, executing, and destroying sessions programmatically.

## Limitations
- **Docker Dependency**: Requires access to the Docker daemon, which has significant security implications if not managed correctly.
- **TOS Compliance**: This is an unofficial containerization; users must comply with Anthropic's Terms of Service.
- **Configuration Complexity**: Manual processing required for some complex MCP configurations within containers.

## When to use it
- When you need "an agent in your agent" to perform complex coding tasks in isolated environments.
- When you want to automate Claude Code actions via a central orchestrator or CI/CD pipeline.
- For enterprise deployments requiring **AWS Bedrock** instead of direct Anthropic API access.

## When not to use it
- On systems where you cannot or should not provide Docker daemon access to an AI agent.
- For simple CLI interactions where the standard Claude Code installation is sufficient.
- If you lack sufficient system resources (RAM/CPU) to run multiple concurrent Docker containers.

## Getting started

Claude Code Container MCP provides a bridge between high-level orchestration and low-level agent execution.

### 1. Prerequisites
- Docker installed and running on the host.
- MCP client (like Claude Desktop or [Desktop Commander MCP](desktop-commander-mcp.md)).

### 2. Installation
```bash
npm install -g @democratize-technology/claude-code-container-mcp
```

### 3. Configuration (Claude Desktop)
```json
{
  "mcpServers": {
    "claude-container": {
      "command": "claude-code-container-mcp",
      "args": ["--docker-socket", "/var/run/docker.sock"]
    }
  }
}
```

## CLI examples

### 1. Listing active sessions
Check currently running Claude Code containers and their status:
```bash
claude-code-container-mcp list
```

### 2. Manual session cleanup
Force-stop and remove all managed containers to free up resources:
```bash
claude-code-container-mcp prune --force
```

### 3. Debugging a session
View logs for a specific containerized agent session to diagnose failures:
```bash
claude-code-container-mcp logs --session <session-id>
```

## API examples

### 1. Creating a Session (Anthropic API)
Automate the creation of an isolated Claude Code session for a specific project directory.

```json
{
  "tool": "create_session",
  "arguments": {
    "projectPath": "/home/user/workspace/web-app",
    "sessionName": "frontend-refactor",
    "apiKey": "sk-ant-..."
  }
}
```

### 2. Creating a Session (AWS Bedrock)
Use enterprise-grade models via AWS Bedrock for the session for enhanced security.

```json
{
  "tool": "create_session",
  "arguments": {
    "projectPath": "/home/user/workspace/data-pipeline",
    "useBedrock": true,
    "awsRegion": "us-east-1",
    "bedrockModel": "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
  }
}
```

### 3. Programmatic Session Validation using Pydantic v2
This Python script validates isolated containerized Claude Code session payloads against provider requirements (either Anthropic API or AWS Bedrock) using **Pydantic v2**:

```python
import json
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict, model_validator

class ClaudeSessionConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    project_path: str = Field(..., validation_alias="projectPath", description="Absolute local path to clone or mount")
    session_name: str = Field(..., validation_alias="sessionName", description="A unique identifier for the Claude session")
    api_key: Optional[str] = Field(None, validation_alias="apiKey", description="Anthropic API key for direct access")

    # AWS Bedrock specific parameters
    use_bedrock: bool = Field(False, validation_alias="useBedrock")
    aws_region: Optional[str] = Field(None, validation_alias="awsRegion")
    bedrock_model: Optional[str] = Field(None, validation_alias="bedrockModel")

    @model_validator(mode="after")
    def validate_provider_config(self) -> 'ClaudeSessionConfig':
        if self.use_bedrock:
            if not self.aws_region or not self.bedrock_model:
                raise ValueError("awsRegion and bedrockModel are required when useBedrock is set to True.")
        else:
            if not self.api_key:
                raise ValueError("apiKey is required when using direct Anthropic API access.")
        return self

def validate_session_payload(raw_json: str) -> Optional[ClaudeSessionConfig]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2
        config = ClaudeSessionConfig.model_validate(data)
        return config
    except json.JSONDecodeError:
        print("Error: Input is not valid JSON.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None

# Example usage:
# if __name__ == "__main__":
#     # Valid Bedrock config
#     bedrock_payload = """
#     {
#         "projectPath": "/workspace/pipeline",
#         "sessionName": "bedrock-sync",
#         "useBedrock": true,
#         "awsRegion": "us-east-1",
#         "bedrockModel": "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
#     }
#     """
#     validated = validate_session_payload(bedrock_payload)
#     if validated:
#         print("Claude Container Session Config successfully validated!")
#         print(validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Claude Code](claude-code-setup.md)
- [Docker](../infrastructure/docker.md)
- [AWS Bedrock](../providers/aws-bedrock.md)
- [Desktop Commander MCP](desktop-commander-mcp.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [CI/CD Workflows](../../playbooks/dev-workflow-ai-assisted.md)
- [Fuzzing MCP Server](fuzzing-mcp-server.md)
- [Jupyter Kernel MCP](jupyter-kernel-mcp.md)
- [Symbolic MCP](symbolic-mcp.md)
- [Aider](aider.md)

## Sources / References
- [Claude Code Container MCP GitHub](https://github.com/democratize-technology/claude-code-container-mcp)
- [Claude Code Official Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [AWS Bedrock Model IDs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html)

## Contribution Metadata
- Last reviewed: 2026-11-02
- Confidence: high
