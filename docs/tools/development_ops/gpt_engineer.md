# GPT Engineer

## What it is
**GPT Engineer** is an AI-driven software engineering orchestrator and prototyping platform designed to generate complete, functional application codebases from high-level natural language prompts. It focuses specifically on the "bootstrapping" phase of software development, utilizing interactive prompting loops to clarify requirements prior to generation. Under late November/December 2026 SOTA standards, **v2.4.x+** introduces advanced integration with **WebContainer** environments to provide instant, browser-based full-stack previews, alongside full support for the **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** to ingest external schema definitions and API contracts for frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **Llama 4**, **Gemma 3**, and **Qwen 3.6**.

## What problem it solves
Reduces the cognitive and procedural overhead of starting new projects by automating boilerplate creation, environment configuration, and directory scaffolding. It bridges the gap between conceptual requirements and runnable applications, eliminating "configuration hell" and allowing developers to quickly test ideas in an isolated, previewable client-side sandbox.

## Where it fits in the stack
**Development & Ops**. Functions as a high-fidelity codebase scaffolding and automated development system. It sits at the top of the "Software Factory" pipeline, turning product requirements into structured repositories that can be further developed using interactive coding assistants or manually by engineers.

## Typical use cases
- **Greenfield Prototyping**: Instantly bootstrapping a React dashboard, Python microservice, or database-backed web application from a descriptive text prompt.
- **Client-Side Interactive Previews**: Deploying generated code directly inside a WebContainer-based browser tab to visually inspect UI elements and interactive flows in real-time.
- **API and Schema Bootstrapping**: Combining GPT Engineer with MCP servers to import database structures (e.g., PostgreSQL or Supabase schemas) and generate matching typed endpoints.
- **Architectural Exploration**: Comparing different frontend frameworks (such as Svelte, Next.js, or Vue) by generating the same functional MVP across each stack.

## Strengths
- **Interactive Clarification Loop**: Rather than generating code in a "one-shot" manner, it queries the developer on ambiguous specifications before writing a single line of code, significantly reducing logical errors.
- **WebContainer Integration**: Compiles and runs generated full-stack Node.js environments client-side, removing the need for local package installations during exploration.
- **Frontier Model Optimization**: Fully optimized for July 2026 reasoning models (including Claude 5.1, GPT-5.5, Gemma 3, Qwen 3.6, and Llama 4), ensuring superior code modularity and adherence to modern syntax rules.
- **Extensible File System Manipulation**: Operates cleanly over local workspaces, producing editable files without lock-in.

## Limitations
- **Incremental Refactoring**: While outstanding at initial project creation, editing highly complex, multi-module legacy codebases remains a challenge; incremental tools like [Aider](aider.md) are better suited for these tasks.
- **WebContainer Sandbox Constraints**: Client-side execution is limited to Node.js/browser environments; heavy server technologies (like Docker-based backend clusters or C++ runtimes) cannot run inside browser-native WebContainers.
- **Security Auditing**: Generates code based on public packages; developers must manually audit dependencies and code blocks before promoting to production.

## When to use it
- When you need to build a new application, feature prototype, or MVP from scratch.
- When you want to immediately see and interact with your application without performing local `npm install` or setting up virtual environments.
- When generating scaffolded microservices with strict schema boundaries.
- For rapid training and experimentation with novel frontend frameworks.

## When not to use it
- For modifying or refactoring large-scale, pre-existing enterprise applications (use [Aider](aider.md) or [Plandex](plandex.md)).
- When building backend systems requiring non-Node, heavy server architectures (such as complex Kubernetes deployments or low-level systems programming).
- In environments where absolute, manual control over every architectural pattern and package choice is required from day one.

## Getting started
### Installation
GPT Engineer v2.4.x+ can be run directly from the shell via `npx` (which leverages WebContainers for browser-based work) or installed as a Python package via `pip` for local-only file generation.

```bash
# To run the WebContainer-integrated interactive generator:
npx gpt-engineer

# To install the command-line workspace generator locally:
pip install gpt-engineer
```

### Basic Workflow
1. **Prepare Workspace**: Create and navigate to a new empty directory:
   ```bash
   mkdir home-dashboard && cd home-dashboard
   ```
2. **Initialize Scaffolder**:
   ```bash
   gpt-engineer .
   ```
3. **Specify Requirements**: Provide a descriptive text description when prompted.
4. **Clarify**: Respond to the interactive questions generated by the assistant.
5. **Inspect & Run**: Review files created in the workspace.

## CLI examples
### Greenfield App Generation
```bash
# Generate a React application in the current directory using Claude 5.1
gpt-engineer . --model claude-5.1 --prompt "A sleek home automation panel tracking temperature and lighting"
```

### Spec-First Generation (Clarify Mode)
```bash
# Force the agent to run through an extended question-and-answer loop to build exact specifications
gpt-engineer . --steps clarify --model gpt-5.5
```

### Non-Interactive CI/CD Scaffolding
```bash
# Run headless code generation for a fastapi backend service using a predefined prompt file
gpt-engineer . --prompt-file ./requirements.txt --no-interactive --model gemini-4.0-pro
```

## API examples
### Python Core Programmatic Generation
Developers can embed GPT Engineer within automated "Software Factories" to programmatically assemble codebases.

```python
from gpt_engineer.core.ai import AI
from gpt_engineer.core.steps import gen_code
from gpt_engineer.core.db import DBs, Archive, DB

def generate_automated_microservice(requirements_path: str, output_path: str):
    # Initialize connection to SOTA reasoning models
    ai = AI(model_name="gpt-5.5")

    # Setup working database structures
    workspace = DB(output_path)
    dbs = DBs(
        workspace=workspace,
        archive=Archive(output_path + "/archive"),
        preprompts=DB("./preprompts")
    )

    # Ingest prompt file
    with open(requirements_path, "r") as f:
        prompt = f.read()

    print(f"Generating codebase in: {output_path}")
    # Execute generation steps
    gen_code(ai, dbs, prompt)
    print("Generation complete!")

if __name__ == "__main__":
    generate_automated_microservice("specs.txt", "./src/generated_service")
```

### JS/TS WebContainer SDK Integration
 In-browser platforms can programmatically trigger GPT Engineer and mount the resulting workspace into a local iframe using WebContainers.

```typescript
import { GPTEngineerSDK } from '@gpt-engineer/sdk';

const client = new GPTEngineerSDK({
  apiKey: process.env.GPT_ENGINEER_API_KEY,
  mcpServers: ['http://localhost:3011/mcp'] // Connect to local MCP context
});

async function runBrowserEngine() {
  const prompt = "A responsive dashboard for tracking local solar panel outputs";

  // Scaffolds code and automatically returns a WebContainer-compatible volume object
  const project = await client.createProject({
    prompt,
    framework: 'vite-react-ts',
    llm: 'claude-5.1'
  });

  // Mounts the virtual file system client-side and returns the server URL
  const previewUrl = await project.mountAndServe();

  // Embed in iframe
  const iframe = document.getElementById('preview-frame') as HTMLIFrameElement;
  iframe.src = previewUrl;
}
```

### Robust Workspace and Scaffold Configuration Validation with Pydantic v2
The following Python script illustrates how to model and programmatically validate GPT Engineer workspace parameters, targeted LLM connections, and WebContainer environments under late November/December 2026 standards, ensuring strict schema safety and type correctness using Pydantic v2:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class WebContainerEnvConfig(BaseModel):
    port: int = Field(default=3000, ge=1024, le=65535)
    hot_reload: bool = Field(default=True)
    framework: str = Field(default="vite-react-ts", pattern=r"^(vite-react-ts|nextjs|svelte-kit|vue)$")

class GPTEngineerWorkspaceConfig(BaseModel):
    project_name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    model_name: str = Field(..., pattern=r"^(claude-5\.1-sonnet|gpt-5\.5-preview|gemini-4\.0-pro)$")
    webcontainer: WebContainerEnvConfig = Field(default_factory=WebContainerEnvConfig)
    mcp_servers: List[str] = Field(default_factory=list)
    auto_install_dependencies: bool = Field(default=True)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "project_name": "homelab-solar-dashboard",
                "model_name": "claude-5.1-sonnet",
                "webcontainer": {
                    "port": 3000,
                    "hot_reload": True,
                    "framework": "vite-react-ts"
                },
                "mcp_servers": ["http://localhost:3011/mcp"],
                "auto_install_dependencies": True
            }
        }
    }

def validate_gpt_engineer_config(payload: dict) -> str:
    """Validates GPT Engineer Workspace and Scaffolding configurations using Pydantic v2."""
    try:
        config = GPTEngineerWorkspaceConfig.model_validate(payload)
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
        "project_name": "homelab-solar-dashboard",
        "model_name": "claude-5.1-sonnet",
        "webcontainer": {
            "port": 5173,
            "hot_reload": True,
            "framework": "vite-react-ts"
        },
        "mcp_servers": ["http://localhost:3011/mcp"],
        "auto_install_dependencies": True
    }
    print(validate_gpt_engineer_config(test_payload))
```

## Related tools / concepts
- [Aider](aider.md) — Terminal-based collaborative coding tool optimized for incremental edits.
- [Anti-Gravity](anti_gravity.md) — Google's premier agentic development and task orchestration framework.
- [Claude Code](claude-code.md) — Anthropic's interactive high-fidelity terminal agent.
- [Codeium](codeium.md) — Multi-IDE AI autocomplete and agentic refactoring.
- [Cursor](cursor.md) — AI-first IDE optimized for codebase navigation and chat-driven edits.
- [Devin](devin.md) — Full-featured autonomous software engineering agent.
- [Droid](droid.md) — Specialized enterprise-grade coding orchestrator.
- [Junie CLI](junie-cli.md) — JetBrains AI Lab terminal codebase navigation assistant.
- [Melty](melty.md) — Open-source AI-native IDE with deep git and terminal loop integration.
- [OpenHands](openhands.md) — General-purpose autonomous software agent platform.
- [Plandex](plandex.md) — CLI-based multi-step code-generation orchestrator.
- [../../knowledge_base/patterns/software-factories.md](../../knowledge_base/patterns/software-factories.md) — Pattern for automated code generation.

## Sources / references
- [GPT Engineer GitHub Repository](https://github.com/AntonOsika/gpt-engineer)
- [Official Documentation and Guides](https://gpt-engineer.readthedocs.io/)
- [WebContainer API Integration](https://webcontainers.io/)
- [GPT Engineer v2.4.0 Release Notes](https://github.com/AntonOsika/gpt-engineer/releases)

## Contribution Metadata
- Last reviewed: 2026-12-17
- Confidence: high
