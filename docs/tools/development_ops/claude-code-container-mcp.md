# Claude Code Container MCP Server

## What it is
An MCP server that manages containerized Claude Code sessions, transforming the CLI tool into an orchestratable service.

## What problem it solves
It enables AI assistants to create and control isolated Claude Code instances programmatically. It provides Docker-based isolation, multi-session management, and support for AWS Bedrock, making it suitable for enterprise AI-to-AI workflows.

## Where it fits in the stack
**Tool / Orchestration**. It provides a managed environment for running other coding agents, following the [Agent Protocols](../../knowledge_base/agent_protocols.md) for structured tool interaction.

## Typical use cases
- Parallel development workflows (managing different microservices in separate containers).
- Automated code reviews in CI/CD pipelines.
- Enterprise batch operations across multiple projects.
- Running Claude Code with AWS Bedrock for enterprise compliance.

## Strengths
- **Isolation**: Docker containers protect the host system and isolate projects.
- **Scalability**: Can run multiple Claude Code sessions simultaneously.
- **AWS Bedrock Integration**: Native support for AWS enterprise LLM endpoints.
- **Programmable API**: Full MCP tools for creating, executing, and destroying sessions.

## Limitations
- Requires access to the Docker daemon (significant security implications).
- ⚠️ This is an unofficial containerization; users must comply with Anthropic's TOS.
- Manual processing required for some MCP configurations within containers.

## When to use it
- When you need "an agent in your agent" to perform complex coding tasks in isolated environments.
- When you want to automate Claude Code actions via a central orchestrator or CI/CD.

## When not to use it
- On systems where you cannot or should not provide Docker daemon access to an AI agent.
- For simple CLI interactions where the standard Claude Code installation is sufficient.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (software); Anthropic API or AWS usage costs apply.
- **Self-hostable**: Yes (Requires Docker)

## Technical examples

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
Use enterprise-grade models via AWS Bedrock for the session.

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

### 3. Executing Commands in Session
Send a prompt to an active Claude Code container to perform work.

```json
{
  "tool": "execute_in_session",
  "arguments": {
    "sessionId": "abc-123-xyz",
    "prompt": "Refactor the authentication middleware to use JWT instead of sessions."
  }
}
```

### 4. Transferring Files
Move files between the host and the container for initial setup or result extraction.

```json
{
  "tool": "transfer_files",
  "arguments": {
    "sessionId": "abc-123-xyz",
    "direction": "to_container",
    "sourcePath": "./local-config.json",
    "destPath": "/workspace/config.json"
  }
}
```

## Related tools / concepts
- [Claude Code](claude-code-setup.md)
- [Docker](../infrastructure/docker.md)
- [AWS Bedrock](../providers/aws-bedrock.md)
- [Desktop Commander MCP](desktop-commander-mcp.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [CI/CD Workflows](../../playbooks/dev-workflow.md)
- [Fuzzing MCP Server](fuzzing-mcp-server.md)
- [Jupyter Kernel MCP](jupyter-kernel-mcp.md)
- [Symbolic MCP](symbolic-mcp.md)

## Sources / References
- [Claude Code Container MCP GitHub](https://github.com/democratize-technology/claude-code-container-mcp)
- [Claude Code Official Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
