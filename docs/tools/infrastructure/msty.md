# Msty

## What it is
Msty is a highly professional, local-first AI desktop application designed to provide a secure and integrated workspace for executing both local models (via Ollama/Llama.cpp/Aphrodite Engine) and major cloud-based API providers. Following major upgrades throughout 2026 (including the stable Msty Claw series), it has evolved from a simple graphical chat wrapper into a modular "AI Desktop Operating System." It features a robust, isolated extension marketplace, dynamic local RAG indexers, and native client integration with the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.1 specifications.

## What problem it solves
Managing local model dependencies, model files, VRAM calculations, and multi-model routing can be highly complex and intimidating. Msty solves this by providing a unified, user-friendly desktop dashboard. It handles VRAM estimation dynamically to prevent allocation crashes, organizes disjointed PDFs/documents into searchable "Knowledge Stacks" for context-injection (RAG), and allows running collaborative, multi-agent "Crews" locally. Furthermore, it addresses "context pollution" and model amnesia during long agent cycles by implementing structured, reusable "Memory Packs."

## Where it fits in the stack
**Category**: Infrastructure / AI Desktop Clients. It sits at the top of the local infrastructure layer, acting as the user interface and orchestration client. It connects down to local model execution backends (like Ollama, llama.cpp, or [Aphrodite Engine](aphrodite-engine.md)) or cloud provider endpoints, and leverages FastMCP 3.1 tools to interact with local system resources safely.

```
┌────────────────────────────────────────┐
│               USER UI                  │
│       Msty Desktop Workspace           │
└───────────────────┬────────────────────┘
                    │ Manages Workflows / Extensions
┌───────────────────▼────────────────────┐
│      LOCAL ORCHESTRATION CLIENT        │
│    Crews, Memory Packs, RAG Index      │
└───────────────────┬────────────────────┘
                    │ REST / API Calls
┌───────────────────▼────────────────────┐
│      Inference Server / Provider       │
│     (Ollama, Aphrodite, Claude 5.1)    │
└────────────────────────────────────────┘
```

## Typical use cases
- **Secure, Offline Chat**: Running highly capable local models (such as Gemma 3 27B or Qwen 3.6 14B) fully offline for secure document analysis.
- **Local Multi-Agent Simulations**: Designing and orchestrating local teams of specialized AI workers ("Crews") using local LLMs.
- **Dynamic Context Injection (RAG)**: Indexing gigabytes of research papers, code repositories, or financial records into custom "Knowledge Stacks" for zero-configuration Q&A.
- **Tool-Enabled Desktop Automation**: Installing third-party "Skills" and custom tools via MCP 3.1 to enable local models to read webpages, parse system files, or execute Python code safely.

## Strengths
- **Isolated Extension Architecture**: Extension-based system allows installing Skills, Custom Personas, and Workflows safely.
- **Dynamic Memory Control**: Supports modular "Memory Packs" to keep context relevant, highly focused, and memory-efficient.
- **VRAM Matchmaker**: Built-in visual hardware profiler and VRAM calculator that recommends the perfect quantization sizes of GGUF/EXL2 files for the user's specific GPU setup.
- **Universal Connection Hub**: Connects natively to local Ollama endpoints, local OpenAI-compatible APIs, and enterprise providers (Anthropic, OpenAI, Azure, Bedrock).
- **Advanced UI Workspace**: Multi-tab interface supporting side-by-side chats, branchable chat histories, and multi-model comparative evaluation.

## Limitations
- **Closed-Source Core**: Although the application is free to use and fully supports open-source extensions and models, the core desktop container is proprietary.
- **No Native Multi-User Sharing**: Built primarily as a single-user desktop client application rather than a shared, collaborative multi-user web portal.
- **Hardware Bound**: Executing highly capable local models remains strictly limited by local system resources (RAM/VRAM), although the app mitigates this via split-offloading estimators.

## When to use it
- When you require a polished, desktop AI workspace that integrates local and cloud models.
- When your workflows rely heavily on local document retrieval (RAG) and multi-agent crews.
- When you want to utilize modular MCP 3.1 tools and extension "Skills" without configuring command-line environments.

## When not to use it
- If your environment demands a 100% open-source core stack (use [Jan.ai](jan-ai.md) or [LobeHub](../ai_knowledge/lobehub.md) instead).
- If you need to serve model API endpoints to thousands of concurrent network clients (use [vLLM](vllm.md) or [Aphrodite Engine](aphrodite-engine.md)).

## Getting started
1. **Download**: Install the latest desktop release matching your operating system from the [Official Msty Portal](https://msty.ai/).
2. **Model Download**: Open the model manager ("One Local Model Hub") to fetch an optimized model; the "Matchmaker" will recommend appropriate weights (such as `gemma-3-27b-it`) based on your hardware profile.
3. **Configure RAG**: Create a "Knowledge Stack", drag and drop local directories or files, and allow the background vectorizer to complete indexing.
4. **Extend**: Visit the extension gallery to enable advanced Skills and register local or remote MCP 3.1 servers.

## CLI examples

### 1. Launch with Specific Persona
Start Msty on your desktop with a pre-configured persona immediately active:
```bash
msty --persona "Security Auditor"
```

### 2. Headless Local Server Launch
Run Msty in headless mode to serve as a local proxy or API backend for third-party scripts:
```bash
msty --headless --port 5050
```

### 3. VRAM Requirement Estimation
Estimate hardware headroom for a prospective local model configuration:
```bash
msty calculate-vram --model ~/models/gemma-3-27b-Q4_K_M.gguf --gpu-vram 16
```

## API examples

### 1. Python: Importing and Validating an Extension Manifest (Pydantic v2)
In the modern Msty Claw ecosystem, extension packages and skills are structured via JSON manifests. This Python script validates an extension manifest using strict Pydantic v2 models before loading.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class ExtensionManifest(BaseModel):
    extension_id: str = Field(description="Unique namespace identifier for the Msty extension")
    version: str = Field(description="Semantic version string")
    required_mcp_version: str = Field(default="3.1", description="Required minimum MCP version")
    supported_models: List[str] = Field(description="List of compatible model names/wildcards")
    sandbox_permissions: List[str] = Field(description="System permission scopes required")

    @field_validator("version")
    @classmethod
    def validate_semver(cls, value: str) -> str:
        import re
        if not re.match(r"^\d+\.\d+\.\d+$", value):
            raise ValueError("Version must follow strict semantic versioning format (e.g., 1.2.0)")
        return value

# Example configuration representation
raw_manifest = {
    "extension_id": "msty.skills.websearch",
    "version": "1.4.2",
    "required_mcp_version": "3.1",
    "supported_models": ["gemma-3-*", "llama-4-*"],
    "sandbox_permissions": ["network", "local-filesystem-read"]
}

# Perform parsing and strict validation
validated_manifest = ExtensionManifest(**raw_manifest)
print(f"Validated Msty Extension Manifest: {validated_manifest.model_dump_json(indent=2)}")
```

### 2. Dynamic Connection via FastMCP (MCP 3.1)
Exposing local tools to Msty via FastMCP 3.1. When registered, Msty allows models to query this tool automatically:

```python
from mcp.server.fastmcp import FastMCP
import shutil

mcp = FastMCP("Msty System Companion")

@mcp.tool()
def check_disk_space() -> str:
    """Returns the available and total storage space of the local homelab disk."""
    total, used, free = shutil.disk_usage("/")
    return f"Total: {total // (2**30)} GB | Free: {free // (2**30)} GB"
```

## Related tools / concepts
- [Jan.ai](jan-ai.md) — Open-source local-first alternative AI desktop client.
- [LM Studio](lm-studio.md) — Desktop local model explorer and server.
- [Ollama](../../services/ollama.md) — High-performance, easy-to-use local model runner.
- [GPT Researcher](../agents/gpt-researcher.md) — Autonomous agent often integrated as a researcher skill.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Desktop client specialized for document-heavy RAG.
- [LobeHub](../ai_knowledge/lobehub.md) — Modern visual agent frontend and server.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open standard for connecting model UI clients to local tool servers.

## Sources / references
- [Msty Official Website](https://msty.ai/)
- [Msty Claw Extensions & Changelog](https://msty.ai/claw/changelog/)
- [Msty Blog: Memory Packs & Crews](https://msty.ai/blog/)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
