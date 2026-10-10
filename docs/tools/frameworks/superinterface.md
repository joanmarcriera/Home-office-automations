# Superinterface

## What it is
Superinterface is an open-source framework and platform for building and deploying AI assistants with production-ready user interfaces. It provides a set of React components and a backend infrastructure to handle streaming, tool calls, and conversation state. As of early 2027, it supports advanced agentic features including **Computer Use**, native **FastMCP 3.1 Task Protocol** integration, and **Interactive Components** optimized for **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **Gemma 4**.

## System Architecture

```
                                +-------------------------------------------------------+
                                |               React / Next.js Web App                 |
                                |     (@superinterface/react Threads & Forms UI)        |
                                +---------------------------+---------------------------+
                                                            |
                                                            v  WebSocket / SSE Stream
                                +-------------------------------------------------------+
                                |              Superinterface Server Core               |
                                |    (Session Manager / Thread Storage / Prompt Engine) |
                                +---------------------------+---------------------------+
                                                            |
                                        +-------------------+-------------------+
                                        |                                       |
                                        v                                       v
                     +-------------------------------------+   +-------------------------------------+
                     |     FastMCP 3.1 Gateway Client      |   |       Model Provider Gateway        |
                     |  (Sub-10ms FastMCP Tool Integration)|   | (Claude 5.6 / GPT-5.6 / Gemini 4.0) |
                     +------------------+------------------+   +-------------------------------------+
                                        |
                                        v
                     +-------------------------------------+
                     |     Computer Use Sandbox Target     |
                     |  (Virtual Machine / Headless Browser)
                     +-------------------------------------+
```

```mermaid
graph TD
    subgraph Frontend Client Layer
        A[React / Next.js Web App] -->|@superinterface/react Components| B[Interactive Thread / Chat UI]
        B -->|WebSocket / SSE Stream| C[Superinterface Server Backend]
    end

    subgraph Superinterface Server Core
        C -->|Session State & Thread Persistence| D[PostgreSQL / Redis]
        C -->|Computer Use & Action Dispatch| E[FastMCP 3.1 Gateway]
        C -->|Context & Message Truncation| F[Prompt Management Engine]
    end

    subgraph LLM & FastMCP Execution Layer
        E <-->|Sub-10ms Tool Execution| G[FastMCP Tool Server]
        F <-->|Streaming Completions| H[Model Providers / Claude 5.6 / GPT-5.6]
        G -->|Computer Use Actions| I[Virtual Machine / Browser Container]
    end
```

## What problem it solves
It bridges the gap between AI agents and the end-user by providing a structured way to build conversational and interactive interfaces. It eliminates the need to build custom UI components for complex agentic behaviors like file handling, multi-modal streaming, and **Computer Use** (controlling virtual environments). The integration with **FastMCP 3.1** ensures sub-10ms tool interaction latency while keeping backend session state and frontend UI states synchronized across real-time streaming connections.

## Where it fits in the stack
**Category**: Frameworks / UI Library & Assistant Backend. It sits at the **Application & Presentation Layer**, bridging frontend user interaction with model orchestrators and FastMCP tool servers.

## Key Feature Comparison Matrix

| Capability / Feature | Superinterface | Dify Platform | Vercel AI SDK | Open WebUI |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Embeddable React assistant UI & backend | Complete No-Code/Low-Code agent platform | React/Next.js streaming primitives | Full chat UI web application |
| **Interactive Components**| Native rich form & action UI embedding | Limited standard form widgets | Custom React Server Components | Standard Markdown/Code rendering |
| **FastMCP 3.1 Support** | Built-in gateway client & SSE | Webhook / REST tools | Community integrations | Custom Python pipelines |
| **Computer Use Support** | Native VM / Browser control support | None | Third-party function calls | Web browsing tool calling |
| **Backend Architecture** | Docker / Node.js / PostgreSQL | Docker Compose / Python / Celery | Serverless / Edge functions | Python FastAPI / SQLite |

## Typical use cases
- **AI-Powered Customer Portals**: Building chat interfaces that support **Interactive Components** like forms, surveys, and interactive cards for structured data entry.
- **Agentic Desktop Controls**: Utilizing **Computer Use** (via Anthropic, OpenRouter, or local VM endpoints) to allow assistants to control virtual machines or web browsers directly from the chat interface.
- **Enterprise Assistant Backend**: Deploying a self-hosted backend (using `@superinterface/server`) that integrates with internal **FastMCP 3.1** tool servers and enterprise single sign-on (SSO).
- **Real-Time Voice Assistants**: Implementing low-latency voice interactions using specialized **Gemma 4** and **Claude 5.6** audio streaming pipelines with visual feedback waves.
- **Multi-Modal Document Workflows**: Uploading images, PDFs, and audio clips with automatic client-side client rendering and server-side vector embedding indexing.

## Strengths
- **Native FastMCP 3.1 Support**: Seamlessly connects assistants to any FastMCP tool server for expanded agentic capabilities without custom webhooks.
- **Rich UI Library**: Customizable React components for threads, messages, multi-modal file attachments, and complex video/audio playback.
- **Interactive Components**: Allows agents to present structured UI elements (forms, carousels, action buttons) directly within the chat stream.
- **Developer-Centric Tools**: Comprehensive **Tools REST API** and TypeScript SDKs for managing assistant capabilities programmatically.
- **Multi-Tenant Session Management**: Built-in tenant isolation, user session threads, and conversation history persistence.

## Limitations
- **React Dependency**: The frontend library is strictly built for React/Next.js and Radix-UI ecosystems.
- **Infrastructure Requirements**: Self-hosting the full server stack requires managing PostgreSQL database and streaming WebSocket/SSE infrastructure.
- **Latency Overhead on Heavy UI State**: Rendering large interactive form trees dynamically can cause minor client-side re-render overhead if state updates are unthrottled.

## When to use it
- When you want to build a feature-rich, multi-modal AI chat interface with minimal frontend development effort.
- When you require advanced agentic capabilities like **Computer Use** or native **FastMCP 3.1** tool integration.
- When you need to self-host your assistant infrastructure for data privacy and security compliance.

## When not to use it
- For backend-only AI tasks that do not require a user interface (use [LangGraph](langgraph.md) or [Agno](../agents/agno.md)).
- If you are building a non-React application (e.g., Vue, Svelte, Flutter, or native mobile without WebView).

## Getting started

### Installation
```bash
npm install @superinterface/react @tanstack/react-query @radix-ui/themes
```

### Self-Hosted Server (Docker)
```bash
docker run -d \
  --name superinterface-server \
  -p 3000:3000 \
  -e DATABASE_URL="postgresql://user:pass@localhost:5432/superinterface" \
  -e SUPERINTERFACE_SECRET_KEY="your-secret-key" \
  supercorp/superinterface-server:latest
```

## Operational Best Practices & Troubleshooting

### Operational Guidance
1. **WebSocket Connection Handling**: Configure reverse proxies to handle WebSocket upgrades (`Upgrade $http_upgrade`, `Connection "upgrade"`) with generous read/write timeouts (e.g., 3600s).
2. **Database Pooling**: Ensure PgBouncer or server-side connection pooling is enabled on PostgreSQL instances supporting high-concurrency Superinterface thread streams.
3. **State Sync Enforcements**: Keep component client-side state synchronized by avoiding direct mutation of message objects outside the `@superinterface/react` hook lifecycle.

### Common Troubleshooting Scenarios
- **Streaming Interruptions**: Verify reverse proxy buffer settings (`proxy_buffering off;`) to prevent SSE response chunking delay.
- **FastMCP Tool Connection Errors**: Inspect network reachability between the Superinterface backend container and FastMCP tool servers.
- **Hydration Mismatches**: Ensure server-rendered Next.js pages wrapping Superinterface components specify client component directives (`"use client"`).

## CLI examples

### Deployment via CLI
```bash
superinterface deploy --assistant-id <ASSISTANT_ID> --environment production
```

### Managing Tools
```bash
superinterface tools add web_search --type fastmcp --url http://localhost:8080/mcp
```

### FastMCP 3.1 Server Registration
```bash
superinterface mcp register --url http://localhost:8080/mcp --auth-token "mcp_token_xyz"
```

## API examples

### Python FastMCP 3.1 Server Integration & Pydantic v2 Tool Validation
This example demonstrates configuring a **FastMCP 3.1** tool server that interfaces with Superinterface to process interactive component events and validate payloads using **Pydantic v2**:

```python
import os
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

# Initialize FastMCP 3.1 Server for Superinterface
mcp = FastMCP("Superinterface-Interactive-Gateway")

class InteractiveFormSubmission(BaseModel):
    form_id: str = Field(..., description="Unique ID of the interactive component form")
    user_id: str = Field(..., description="ID of the submitting user")
    field_values: Dict[str, Any] = Field(..., description="Key-value dictionary of form input data")
    client_timestamp: float = Field(..., description="Client-side submit timestamp")

class ComponentOption(BaseModel):
    label: str = Field(..., description="Human readable selection label")
    value: str = Field(..., description="Internal key value string")

class InteractiveComponentSpec(BaseModel):
    component_type: str = Field(..., pattern="^(form|carousel|action_card|survey)$", description="Type of UI element")
    title: str = Field(..., min_length=3, description="Component header title")
    options: List[ComponentOption] = Field(default_factory=list, description="Selection options")

class SuperinterfaceToolConfig(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$", description="Alpha-numeric name of the tool")
    description: str = Field(..., min_length=10, description="Detailed tool description for LLM prompting")
    type: str = Field("custom", description="The tool execution type")
    parameters_schema: dict = Field(..., description="The tool's parameters formatted as JSON schema (Pydantic v2 compliant)")

@mcp.tool()
def handle_form_submit(payload: dict) -> dict:
    """Validate and process interactive form submissions received from Superinterface UI components."""
    try:
        submission = InteractiveFormSubmission.model_validate(payload)

        # Process interactive form logic (e.g. database updates, downstream agent trigger)
        return {
            "status": "success",
            "form_id": submission.form_id,
            "processed_fields": len(submission.field_values),
            "message": f"Successfully processed interactive component submission for user {submission.user_id}."
        }
    except ValidationError as err:
        return {"status": "validation_error", "details": err.errors()}

if __name__ == "__main__":
    # Test local validation logic
    sample_payload = {
        "form_id": "retreat_booking_form_01",
        "user_id": "usr_9876",
        "field_values": {"location": "Lake Tahoe", "guests": 25, "dates": "2027-06-12"},
        "client_timestamp": 1772188800.0
    }

    result = handle_form_submit(sample_payload)
    print("FastMCP Superinterface Form Submission Result:", result)
```

### Configuring Message Truncation & Context Limits
```json
{
  "truncationType": "LAST_MESSAGES",
  "truncationLastMessagesCount": 15,
  "maxTokens": 4096
}
```

## Related tools / concepts
- [Vercel AI SDK](../providers/vercel-ai-gateway.md) — Frontend framework for AI applications.
- [Dify](../ai_knowledge/dify.md) — LLM application development platform.
- [Open WebUI](../../services/open-webui.md) — Popular self-hosted LLM interface.
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standardized tool-calling and resource specification.
- [OpenRouter](../ai_knowledge/openrouter.md) — Provider for Computer Use and diverse foundation models.
- [Langflow](langflow.md) — Visual workflow builder for agents.
- [Mastra](mastra.md) — TypeScript-native agent framework.
- [Rivet](rivet.md) — Visual AI programming environment.

## Sources / references
- [Official Website](https://superinterface.ai/)
- [Superinterface Documentation](https://superinterface.ai/docs)
- [GitHub Repository](https://github.com/superinterface/superinterface)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
