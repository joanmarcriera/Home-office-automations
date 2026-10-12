# Msty

## What it is
Msty is a highly professional, local-first AI desktop application designed to provide a secure and integrated workspace for executing both local models (via Ollama/Llama.cpp/Aphrodite Engine) and major cloud-based API providers. Following major upgrades (including the stable Msty Claw series and early 2027 v2.5 releases), it has evolved from a simple graphical chat wrapper into a modular "AI Desktop Operating System." It features a robust, isolated extension marketplace, dynamic local RAG indexers, multi-agent Crews, and native client integration with the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.1 specifications.

## What problem it solves
Managing local model dependencies, model files, VRAM calculations, and multi-model routing can be highly complex and intimidating. Msty solves this by providing a unified, user-friendly desktop dashboard. It handles VRAM estimation dynamically to prevent allocation crashes, organizes disjointed PDFs/documents into searchable "Knowledge Stacks" for context-injection (RAG), and allows running collaborative, multi-agent "Crews" locally. Furthermore, it addresses "context pollution" and model amnesia during long agent cycles by implementing structured, reusable "Memory Packs."

## Architecture & System Flow

Msty operates as a multi-tier local application, separating the user-facing desktop shell from background worker runtimes, vector storage engines, and FastMCP 3.1 tool integration buses.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Msty Desktop Shell (Electron/Tauri)                │
│  ┌───────────────────────────────┐        ┌──────────────────────────────┐  │
│  │     Workspace & Tab Manager   │        │     Persona & Skill Gallery  │  │
│  └───────────────┬───────────────┘        └──────────────┬───────────────┘  │
└──────────────────┼───────────────────────────────────────┼──────────────────┘
                   │ IPC / Internal Channel                │
┌──────────────────▼───────────────────────────────────────▼──────────────────┐
│                      Msty Core Orchestration Engine                         │
│  ┌─────────────────────────┐   ┌───────────────────┐   ┌─────────────────┐ │
│  │ VRAM Matchmaker & Profiler│   │ Memory Pack Store │   │ Crew Sequencer  │ │
│  └──────────────┬──────────┘   └─────────┬─────────┘   └────────┬────────┘ │
└─────────────────┼────────────────────────┼──────────────────────┼───────────┘
                  │ API Calls / Rest       │ Local Retrieval      │ MCP Bus
┌─────────────────▼────────┐    ┌──────────▼────────────┐  ┌─────▼─────────────┐
│ Local Inference Server   │    │ Knowledge Stack RAG   │  │ FastMCP 3.1       │
│ (Ollama / Aphrodite Engine│    │ (Chroma / SQLite-Vec) │  │ Tool Servers      │
│  / llama.cpp / Cloud APIs)│    └───────────────────────┘  └───────────────────┘
└──────────────────────────┘
```

The system flow follows strict sequence isolation:
1. **Model Discovery & Profiling**: The VRAM Matchmaker scans host GPU hardware, calculating exact layer offloading potential before model instantiation.
2. **Context Assembly**: Queries trigger parallel retrieval across registered Knowledge Stacks (local vector stores) and attached Memory Packs.
3. **Multi-Agent Orchestration**: Crews route sub-tasks to designated specialized models or system skills using standardized FastMCP 3.1 protocol bridges.
4. **Output Synthesis**: Synthesized responses are rendered in real-time with citation tracking and branchable conversation trees.

## Where it fits in the stack
**Category**: Infrastructure / AI Desktop Clients. It sits at the top of the local infrastructure layer, acting as the user interface and orchestration client. It connects down to local model execution backends (like Ollama, llama.cpp, or [Aphrodite Engine](aphrodite-engine.md)) or cloud provider endpoints (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra), and leverages FastMCP 3.1 tools to interact with local system resources safely.

## Typical use cases
- **Secure, Offline Chat**: Running highly capable local models (such as Gemma 3 27B, Llama 4 70B, or Qwen 3.6 14B) fully offline for secure document analysis.
- **Local Multi-Agent Simulations**: Designing and orchestrating local teams of specialized AI workers ("Crews") using local LLMs.
- **Dynamic Context Injection (RAG)**: Indexing gigabytes of research papers, code repositories, or financial records into custom "Knowledge Stacks" for zero-configuration Q&A.
- **Tool-Enabled Desktop Automation**: Installing third-party "Skills" and custom tools via MCP 3.1 / FastMCP 3.1 to enable local models to read webpages, parse system files, or execute Python code safely.

## Strengths
- **Isolated Extension Architecture**: Extension-based system allows installing Skills, Custom Personas, and Workflows safely.
- **Dynamic Memory Control**: Supports modular "Memory Packs" to keep context relevant, highly focused, and memory-efficient.
- **VRAM Matchmaker**: Built-in visual hardware profiler and VRAM calculator that recommends the perfect quantization sizes of GGUF/EXL2 files for the user's specific GPU setup.
- **Universal Connection Hub**: Connects natively to local Ollama endpoints, local OpenAI-compatible APIs, and enterprise providers (Anthropic, OpenAI, Azure, Bedrock, DeepSeek).
- **Advanced UI Workspace**: Multi-tab interface supporting side-by-side chats, branchable chat histories, and multi-model comparative evaluation.

## Limitations
- **Closed-Source Core**: Although the application is free to use and fully supports open-source extensions and models, the core desktop container is proprietary.
- **No Native Multi-User Sharing**: Built primarily as a single-user desktop client application rather than a shared, collaborative multi-user web portal.
- **Hardware Bound**: Executing highly capable local models remains strictly limited by local system resources (RAM/VRAM), although the app mitigates this via split-offloading estimators.

## Comparison Matrix

| Feature / Dimension | Msty (v2.5 / Claw) | Jan.ai | LM Studio | LobeHub |
| :--- | :--- | :--- | :--- | :--- |
| **License Core** | Proprietary Desktop Shell | Open Source (AGPL-3.0) | Proprietary Commercial | Open Source (MIT) |
| **Native MCP 3.1 Support** | Full / Native Client | Experimental | Limited / Plugin-based | Full / Web-native |
| **Multi-Agent Crews** | Built-in Sequencer | Third-party / Extensions | Single-agent focal | Full Agent Workflows |
| **Memory Packs** | Native Modular Store | Manual System Prompts | System Prompt Presets | Session Context Maps |
| **VRAM Matchmaker** | Automated GPU Profiling | Basic RAM Warning | Static Model Specs | N/A (Server Dependent) |
| **Local RAG (Knowledge Stacks)**| Integrated Zero-Config | Extension Required | Not Built-in | Full Vector RAG |
| **Cloud Provider Fallback** | Universal Connection Hub| OpenAI / Anthropic API | OpenAI Compatible | Multi-provider API |

## When to use it
- When you require a polished, desktop AI workspace that integrates local and cloud models.
- When your workflows rely heavily on local document retrieval (RAG) and multi-agent crews.
- When you want to utilize modular MCP 3.1 tools and extension "Skills" without configuring command-line environments.

## When not to use it
- If your environment demands a 100% open-source core stack (use [Jan.ai](jan-ai.md) or [LobeHub](../ai_knowledge/lobehub.md) instead).
- If you need to serve model API endpoints to thousands of concurrent network clients (use [vLLM](vllm.md) or [Aphrodite Engine](aphrodite-engine.md)).

## Getting started
1. **Download**: Install the latest desktop release matching your operating system from the [Official Msty Portal](https://msty.ai/).
2. **Model Download**: Open the model manager ("One Local Model Hub") to fetch an optimized model; the "Matchmaker" will recommend appropriate weights (such as `gemma-3-27b-it` or `llama-4-scion`) based on your hardware profile.
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

### 4. Direct Extension Skill Verification
Test extension integrity and registered MCP tool endpoints directly from the command line:
```bash
msty extension verify --id "msty.skills.websearch" --verbose
```

### 5. Exporting Memory Packs
Export a compressed Memory Pack snapshot for backup or deployment to another Msty node:
```bash
msty memory export --pack-id "sec-ops-2027" --output ./sec-ops-backup.mpk
```

## API examples

### 1. Python: Validating Extension Manifests & Memory Packs (Pydantic v2)
In the Msty ecosystem, extension packages, tool declarations, and Memory Packs follow strict schemas. The following script validates manifest configurations prior to registering with Msty's local extension manager.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any

class ModelAllocationRule(BaseModel):
    model_pattern: str = Field(..., description="Glob pattern or exact name of model")
    min_vram_gb: float = Field(..., ge=1.0, description="Minimum VRAM in GB required")
    context_window: int = Field(default=8192, description="Target context window length")

class MemoryPackMetadata(BaseModel):
    pack_id: str = Field(..., description="Unique alphanumeric identifier for memory pack")
    title: str = Field(..., description="Human-readable title")
    persistent_facts: List[str] = Field(default_factory=list, description="Core immutable facts")
    embedding_dimension: int = Field(default=1536, description="Vector dimension size")

class MstyExtensionConfig(BaseModel):
    extension_id: str = Field(..., description="Unique namespace identifier for extension")
    version: str = Field(..., description="Semantic version string")
    required_mcp_version: str = Field(default="3.1", description="Required minimum MCP version")
    sandbox_permissions: List[str] = Field(description="Granted permission scopes")
    allocations: List[ModelAllocationRule] = Field(description="Hardware allocation rules")
    memory_pack: Optional[MemoryPackMetadata] = Field(default=None, description="Optional attached memory pack")

    @field_validator("version")
    @classmethod
    def validate_semver(cls, value: str) -> str:
        import re
        if not re.match(r"^\d+\.\d+\.\d+$", value):
            raise ValueError("Version must follow semantic versioning (e.g., 1.2.0)")
        return value

# Example runtime manifest input
manifest_data = {
    "extension_id": "msty.skills.homelab_monitor",
    "version": "2.5.0",
    "required_mcp_version": "3.1",
    "sandbox_permissions": ["network-local", "filesystem-read", "system-metrics"],
    "allocations": [
        {"model_pattern": "gemma-3-27b-*", "min_vram_gb": 16.0, "context_window": 16384},
        {"model_pattern": "llama-4-scion-*", "min_vram_gb": 24.0, "context_window": 32768}
    ],
    "memory_pack": {
        "pack_id": "homelab-arch-2027",
        "title": "Homelab Infrastructure Rules",
        "persistent_facts": [
            "Primary storage array uses ZFS pool zpool0",
            "Local DNS resolver resides at 10.0.0.53",
            "Headscale mesh network domain is internal.net"
        ],
        "embedding_dimension": 1536
    }
}

config = MstyExtensionConfig(**manifest_data)
print(f"Validated Msty Configuration: {config.model_dump_json(indent=2)}")
```

### 2. FastMCP 3.1 Tool Integration for Msty Companion
To expose homelab status and system controls directly to Msty's local agent crews, build a FastMCP 3.1 server:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import shutil
import os

mcp = FastMCP("Msty Homelab Companion")

class StorageReport(BaseModel):
    path: str = Field(description="Target mount point path")
    total_gb: float = Field(description="Total disk capacity in GB")
    free_gb: float = Field(description="Free disk space in GB")
    used_percent: float = Field(description="Used space percentage")

@mcp.tool()
def inspect_system_storage(mount_point: str = "/") -> StorageReport:
    """Provides detailed storage utilization metrics for Msty automation workflows."""
    total, used, free = shutil.disk_usage(mount_point)
    total_gb = total / (1024 ** 3)
    free_gb = free / (1024 ** 3)
    used_percent = ((total - free) / total) * 100.0
    return StorageReport(
        path=mount_point,
        total_gb=round(total_gb, 2),
        free_gb=round(free_gb, 2),
        used_percent=round(used_percent, 1)
    )

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices

1. **VRAM Offloading Management**:
   - Always run `msty calculate-vram` before initializing heavy 70B+ models to ensure offload layers do not cause system swapping or CUDA OOM exceptions.
   - For hybrid GPU setups (e.g., NVIDIA discrete GPU + integrated iGPU), lock Msty execution to the discrete GPU via `CUDA_VISIBLE_DEVICES=0`.

2. **Knowledge Stack RAG Optimization**:
   - Chunk large PDF and Markdown libraries at 512-1024 token boundaries with 10% overlap to preserve semantic context across chunk boundaries.
   - Re-index Knowledge Stacks whenever underlying local repository documentation receives major structural edits.

3. **Memory Pack Hygiene**:
   - Periodically prune stale or contradictory entries from active Memory Packs to prevent hallucination cycles during multi-agent Crew executions.
   - Isolate domain-specific Memory Packs (e.g., "Kubernetes Ops" vs "Python Refactoring") rather than maintaining a monolithic memory file.

4. **MCP 3.1 Tool Security**:
   - Explicitly define allowed permissions in Msty Extension manifests. Restrict arbitrary shell execution tools to sandbox containers.

## Troubleshooting & Common Pitfalls

- **Model Stalls on Generation**: Ensure context lengths in Knowledge Stacks do not exceed physical VRAM allocation limits. Reduce context window setting in model properties from 32k to 16k if inference slows dramatically.
- **MCP Tool Server Connection Timeout**: Confirm FastMCP 3.1 servers execute in Python environments with `mcp` library version >= 1.2.0 and that standard I/O streams (`stdio`) are not polluted with debug `print()` statements.
- **Vector Index Corrupted**: Delete the `.index` folder inside the specific Knowledge Stack directory and initiate a re-index from the Msty Knowledge Stack UI menu.

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
- Last reviewed: 2027-01-07
- Confidence: high
