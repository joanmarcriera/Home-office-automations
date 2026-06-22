# Flowise

## What it is
Flowise is an open-source visual builder for LLM applications and agentic systems. Built on top of LangChain and enhanced with the "AgentFlow" framework, it provides a drag-and-drop interface to create complex multi-agent orchestrations, RAG pipelines, and automated AI workflows.

## What problem it solves
It lowers the barrier to entry for building sophisticated AI applications by providing a no-code/low-code interface. It enables rapid prototyping of agentic systems where autonomous agents can reason, collaborate, and act, while providing built-in Human-in-the-Loop (HITL) controls to ensure safety and reliability in production.

## Where it fits in the stack
**Orchestration / Builder Layer**. It sits as the "control plane" above your LLM providers, vector databases, and external tools, serving as the visual orchestration engine for both simple chatbots and complex multi-agent systems.

## Typical use cases
- **Multi-Agent Orchestration**: Coordinating multiple specialized agents (e.g., a "Researcher" and a "Writer") to complete complex tasks using distributed workflows.
- **Enterprise RAG Pipelines**: Building high-fidelity retrieval systems that connect to 10+ vector databases and utilize advanced retrievers.
- **Agentic Automation**: Creating workflows where agents use the Model Context Protocol (MCP) to interact with local files, databases, and APIs.
- **Secure Internal Tools**: Deploying AI assistants for team use with built-in SSRF protection and security isolation for sensitive data.

## Strengths
- **Visual Programming for Agents**: The "AgentFlow" interface makes complex multi-agent logic and task delegation intuitive.
- **MCP Integration**: Native support for Model Context Protocol allows for seamless connection to a vast ecosystem of standardized tools and data sources.
- **Safety & Oversight**: Includes default SSRF protection and Human-in-the-Loop nodes to prevent unauthorized access and ensure output quality.
- **Rapid Deployment**: Features a wide array of pre-built templates for common integrations (e.g., WhatsApp, Telegram, Slack).
- **Self-Hostable**: Easily deployable via Docker for full data sovereignty in homelab or corporate environments.

## Limitations
- **Visual Complexity**: Extremely large and complex flows can become difficult to manage visually compared to modular code.
- **LangChain Dependency**: While highly flexible, it is still primarily optimized for workflows supported by the underlying LangChain/LangGraph libraries.
- **Resource Overhead**: Running the full visual server and agentic runtime is more resource-intensive than executing lightweight Python scripts.

## When to use it
- When you want to build and iterate on multi-agent systems and RAG pipelines visually.
- For rapid prototyping of complex AI workflows that require human oversight (HITL).
- When you need a self-hosted platform with standardized tool integration via MCP.

## When not to use it
- For performance-critical, low-latency applications where the overhead of a visual builder is unacceptable.
- When you need absolute programmatic control over every byte of the LLM interaction (consider [DSPy](../frameworks/dspy.md) or [Rivet](../frameworks/rivet.md)).

## Getting started

### 1. Installation via Docker
The recommended way to run Flowise is using Docker to ensure all dependencies and security protections are active:

```bash
docker run -d --name flowise -p 3000:3000 flowiseai/flowise
```

### 2. Building an AgentFlow
1. Navigate to `http://localhost:3000` and click "Add New" -> "AgentFlow".
2. Drag an "Agent" node and a "Supervisor" node into the workspace.
3. Connect specialized agent nodes (e.g., "Web Search Agent", "Code Interpreter Agent") to the Supervisor.
4. Add an "MCP Tool" node to give your agents access to local resources.
5. Save and use the built-in "Chat" interface to test the orchestration.

## CLI examples
Flowise provides CLI tools for management and starting the server in different configurations.

```bash
# Start Flowise with a custom persistent directory for database and uploads
npx flowise start --databasePath ~/.flowise/db --uploadsPath ~/.flowise/uploads

# Update Flowise to the latest version
npm install -g flowise && flowise start

# Export a specific chatflow to a JSON file for version control
flowise export --id <CHATFLOW_ID> --output ./my-flow.json
```

## API examples
Flowise automatically generates REST endpoints for every flow, supporting both streaming and variable overrides.

```bash
# Trigger a multi-agent prediction with a session ID for persistence
curl -X POST "http://localhost:3000/api/v1/prediction/<CHATFLOW_ID>" \
     -H "Content-Type: application/json" \
     -d '{
            "question": "Research the latest trends in quantum computing and write a summary.",
            "overrideConfig": {
                "sessionId": "user-123",
                "mcpServerUrl": "http://localhost:8080"
            }
         }'
```

## Related tools / concepts
- [LangFlow](../frameworks/langflow.md) — Primary competitor in the visual builder space.
- [Dify](dify.md) — Advanced LLMOps and multi-agent platform.
- [n8n](../../services/n8n.md) — General automation with strong AI agent support.
- [Rivet](../frameworks/rivet.md) — Visual builder focused on complex, low-level logic.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for tool and agent interoperability.
- [AnythingLLM](anythingllm.md) — Desktop RAG and agentic alternative.
- [CrewAI](../agents/crewai.md) — Code-native framework for multi-agent orchestration.
- [LangGraph](../frameworks/langgraph.md) — Underlying library for complex agent state management.

## Sources / references
- [Flowise Official Documentation](https://docs.flowiseai.com/)
- [Flowise Review 2026: AI Infrastructure](https://aiagentslist.com/agents/flowise)
- [Top 7 Open-Source AI Low-Code Tools in 2026](https://htdocs.dev/posts/top-7-open-source-ai-lowno-code-tools-in-2026/)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
