# Zed

## What it is
Zed is a high-performance, multiplayer code editor authored in Rust by the creators of Atom and Tree-sitter. Operating directly on the GPU hardware via the custom GPUI UI framework and leveraging multi-core CPU threading, Zed delivers sub-millisecond input rendering and ultra-low latency text buffer manipulation. As of early 2027, **Zed 0.180+** has evolved into a premier AI-native editor featuring native multi-model Assistant workspaces, streaming inline transformations, CRDT-based multiplayer pair programming, and native **FastMCP 3.1** Model Context Protocol integrations.

By eliminating Electron abstractions and JavaScript runtime overhead, Zed provides a lightweight, battery-efficient editing platform capable of handling multi-gigabyte source repositories without frame drops or input lag.

## System Architecture

```mermaid
graph TD
    SubGraph_GPUI[Native GPUI Rendering Engine - Rust]
        GPUI[GPUI Hardware Canvas - Vulkan / Metal / Direct3D]
        TreeSitter[Tree-sitter Incremental AST Parser]
        Buffer[Rope Buffer & CRDT Sync Engine]
    end

    SubGraph_Core[Zed Core & AI Controller]
        Assistant[Assistant Panel v2]
        Inline[Inline Transformations - Streaming Engine]
        FastMCP[FastMCP 3.1 Context Server Manager]
        WASM[Wasm Extension Runtime - Wasip1]
    end

    SubGraph_External[External AI Services & Tools]
        LLM[Frontier Models - Claude 5.1 / GPT-5.5 / Gemini 4 Pro]
        LocalLLM[Local Models - Ollama / vLLM Llama 4]
        MCPServers[Remote & Local FastMCP Tools]
    end

    GPUI --> TreeSitter
    GPUI --> Buffer
    Buffer --> Assistant
    Buffer --> Inline
    Assistant --> FastMCP
    FastMCP --> MCPServers
    Assistant --> LLM
    Inline --> LLM
    Inline --> LocalLLM
    WASM --> FastMCP
```

## What problem it solves
Zed addresses the fundamental performance and resource constraints of modern developer tooling:
1. **Input & UI Latency**: Replaces heavy WebKit/Electron rendering loops with native Metal/Vulkan GPU shaders, eliminating keystroke latency even under high LSF/AST indexing loads.
2. **Memory Bloat**: Consumes a fraction of the memory required by Electron IDEs (typically <300MB RAM versus 2GB+ for VS Code with extensions).
3. **Multiplayer Friction**: Replaces screen-sharing or third-party extension overlays with native CRDT (Conflict-free Replicated Data Type) shared buffers for zero-latency collaborative pair programming.
4. **AI Context Friction**: Integrates **FastMCP 3.1** servers directly into the assistant runtime, allowing LLMs to access database schemas, logs, and terminal state natively during chat or inline refactoring.

## Where it fits in the stack
**Development & Ops / High-Performance IDE & AI Workbench**. Zed serves as a resource-efficient, high-speed alternative to VS Code and Cursor, particularly favored by systems engineers, Rust/Go/C++ developers, and AI engineers requiring instant editor startup, native Wasm extensions, and FastMCP 3.1 connectivity.

## Typical use cases
- **Sub-Millisecond Code Editing**: Editing massive monorepos with zero lag and instant tree-sitter syntax highlighting.
- **Multi-Model AI Pairing**: Alternating between **Claude 5.1** for complex refactoring, **GPT-5.5** for logic synthesis, and local **Llama 4** models for zero-cost inline auto-completions.
- **CRDT Multiplayer Pair Programming**: Collaborating live on codebases across distributed teams with real-time cursor tracking, selection highlighting, and voice channels.
- **FastMCP 3.1 Tooling**: Discovering and invoking local or remote Model Context Protocol servers for live DB schema inspection, unit test execution, and log streaming.
- **Custom Wasm Plugin Execution**: Extending editor features safely using WebAssembly plugins compiled from Rust.

## Strengths
- **Unrivaled Input Responsiveness**: Native GPU rendering engine delivering 120+ FPS canvas refresh rates and sub-5ms keystroke latencies.
- **Embedded Multi-Model Assistant**: Native AI UI panel supporting side-by-side prompt buffers, inline transformation diffs, and customizable system prompts.
- **Native FastMCP 3.1 Protocol Support**: Out-of-the-box discovery and connection management for Model Context Protocol servers.
- **Minimal Resource Footprint**: Starts in under 200 milliseconds and maintains a minimal RAM/CPU footprint.
- **Multiplayer CRDT Architecture**: Built-in real-time collaboration engine supporting seamless multi-cursor pair programming.

## Limitations
- **Growing Extension Ecosystem**: While expanding rapidly via the Wasm plugin API, the plugin marketplace is smaller than VS Code's extension library.
- **Rust/Wasm Plugin Curve**: Writing custom plugins requires Rust knowledge and WebAssembly compilation targets (`wasm32-wasip1`).
- **Niche Legacy Enterprise Tooling**: Specialized visual drag-and-drop design tools for legacy enterprise platforms are less prevalent compared to VS Code.

## When to use it
- When requiring maximum editor speed, minimal RAM usage, and long battery life on mobile development rigs.
- For pair programming sessions where zero latency multi-user editing is required.
- When working extensively with **FastMCP 3.1** context servers alongside frontier models.
- When developing systems-level code in Rust, Go, C++, Zig, TypeScript, or Python.

## When not to use it
- If your daily workflow requires specific proprietary VS Code extensions without Wasm equivalents in Zed.
- In enterprise environments that forbid WebAssembly runtime execution or local compiled binaries.
- If visual drag-and-drop UI builders for legacy frameworks are mandatory.

## Getting started

### Installation
Install Zed on macOS, Linux, or Windows using official installation scripts or package managers:

```bash
# Official installation script (macOS / Linux)
curl https://zed.dev/install.sh | sh

# macOS via Homebrew
brew install --cask zed

# Linux via Flatpak
flatpak install flathub dev.zed.Zed
```

### Configuration
Zed is configured via a central JSON file (`~/.config/zed/settings.json`).

#### Native AI & FastMCP 3.1 Configuration
```json
{
  "theme": "One Dark",
  "buffer_font_family": "JetBrains Mono",
  "buffer_font_size": 14,
  "assistant": {
    "default_model": {
      "provider": "anthropic",
      "model": "claude-5-1"
    },
    "version": "2"
  },
  "language_models": {
    "anthropic": {
      "api_key": "YOUR_ANTHROPIC_API_KEY"
    },
    "openai": {
      "api_key": "YOUR_OPENAI_API_KEY"
    }
  },
  "context_servers": {
    "zed-mcp-tools": {
      "source": "custom",
      "command": {
        "path": "python3",
        "args": ["-m", "servers.zed_tools"],
        "env": {
          "PYTHONUNBUFFERED": "1"
        }
      }
    }
  }
}
```

### Essential Shortcuts
- `Cmd+Shift+>` / `Ctrl+Shift+>`: Toggle Assistant Panel.
- `Cmd+R` / `Ctrl+R`: Inline AI Prompt / Refactor.
- `Cmd+Alt+C` / `Ctrl+Alt+C`: Connect FastMCP Context Tools.
- `Cmd+Shift+P` / `Ctrl+Shift+P`: Command Palette.

## CLI examples

### Workspace & Buffer Manipulation
Invoke Zed from your shell for interactive editing or diffing:

```bash
# Open current workspace
zed .

# Open file at line 84
zed src/main.rs:84

# Wait for buffer completion before returning (useful for Git commit editor)
zed --wait COMMIT_EDITMSG
```

### Managing Extensions & MCP Servers via CLI
Zed provides command-line flags for extension discovery and context management:

```bash
# List installed Wasm extensions
zed --list-extensions

# Verify status of registered FastMCP 3.1 servers
zed --mcp-status
```

## API examples

### FastMCP 3.1 Python Context Server Integration
Zed communicates with tools using standard FastMCP 3.1. Below is a complete Python FastMCP server implementation that exposes repository analysis and linting tools to Zed Assistant sessions:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import os
import subprocess

# Initialize FastMCP 3.1 Server for Zed Assistant
mcp = FastMCP("ZedContextTools")

class SyntaxCheckResult(BaseModel):
    filepath: str = Field(description="Target file checked")
    is_valid: bool = Field(description="True if syntax check passed")
    errors: str = Field(default="", description="Compiler or linter error output")

class ProjectSearchRequest(BaseModel):
    query: str = Field(description="Search string or regex")
    extension: str = Field(default="rs", description="File extension filter")

@mcp.tool()
def run_cargo_check(project_dir: str) -> str:
    """Runs 'cargo check' on a Rust workspace and returns errors directly to Zed Assistant."""
    if not os.path.exists(os.path.join(project_dir, "Cargo.toml")):
        return f"Error: '{project_dir}' is not a valid Cargo workspace root."

    try:
        result = subprocess.run(
            ["cargo", "check", "--message-format=short"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return "Cargo Check Passed: No errors found."
        return f"Cargo Check Failures:\n{result.stderr or result.stdout}"
    except Exception as e:
        return f"Execution error: {str(e)}"

@mcp.tool()
def search_codebase(project_dir: str, search_req: ProjectSearchRequest) -> str:
    """Searches files in project directory for specific text queries for Zed context context injection."""
    matches = []
    for root, _, files in os.walk(project_dir):
        if "target" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(f".{search_req.extension}"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for idx, line in enumerate(f, 1):
                            if search_req.query in line:
                                matches.append(f"{filepath}:{idx}: {line.strip()}")
                except Exception:
                    pass

    if not matches:
        return f"No matches found for '{search_req.query}' in .{search_req.extension} files."
    return f"Found {len(matches)} matches:\n" + "\n".join(matches[:25])

if __name__ == "__main__":
    mcp.run()
```

### Validating Zed Config Schemas with Pydantic v2
Ensure local Zed configuration files and MCP server definitions comply with strict Pydantic v2 schemas before syncing:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional

class MCPCommand(BaseModel):
    path: str = Field(description="Path to executable binary")
    args: List[str] = Field(default_factory=list, description="Command line arguments")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment flags")

class ContextServerConfig(BaseModel):
    source: str = Field(default="custom")
    command: MCPCommand

class ZedSettingsSchema(BaseModel):
    theme: str = Field(default="One Dark")
    buffer_font_size: int = Field(default=14, alias="buffer_font_size")
    context_servers: Dict[str, ContextServerConfig] = Field(default_factory=dict, alias="context_servers")

    @field_validator("buffer_font_size")
    @classmethod
    def check_font_size(cls, v: int) -> int:
        if v < 8 or v > 48:
            raise ValueError("Font size must be between 8 and 48 pt")
        return v

    class Config:
        populate_by_name = True

# Validate active Zed settings payload
sample_zed_settings = {
    "theme": "One Dark",
    "buffer_font_size": 15,
    "context_servers": {
        "zed-mcp-tools": {
            "source": "custom",
            "command": {
                "path": "python3",
                "args": ["-m", "servers.zed_tools"],
                "env": {"PYTHONUNBUFFERED": "1"}
            }
        }
    }
}

config = ZedSettingsSchema.model_validate(sample_zed_settings)
print(f"Validated Zed Theme: {config.theme}")
print(f"Registered MCP Tool: {list(config.context_servers.keys())[0]}")
```

### Authoring Wasm Extensions for Zed in Rust
Zed plugins compile to `wasm32-wasip1`. Below is an example plugin skeleton that registers language grammar support and FastMCP tools:

```rust
use zed_extension_api::{self as zed, Result};

struct FastMcpZedExtension;

impl zed::Extension for FastMcpZedExtension {
    fn new() -> Self {
        Self
    }

    fn language_server_command(
        &mut self,
        _config: &zed::LanguageServerId,
        _worktree: &zed::Worktree,
    ) -> Result<zed::Command> {
        Ok(zed::Command {
            command: "fastmcp-lsp".string(),
            args: vec!["--stdio".to_string()],
            env: Default::default(),
        })
    }
}

zed::register_extension!(FastMcpZedExtension);
```

## Related tools / concepts
- [VS Code](vscode.md) — The dominant industry-standard editor framework.
- [Cursor](cursor.md) — VS Code-derived AI-native editor.
- [Aider](aider.md) — Terminal pair programming agent.
- [Claude Code](claude-code.md) — Agentic command-line interface by Anthropic.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standardized protocol for external tool connectivity (FastMCP 3.1).
- [Ollama](../../services/ollama.md) — Local model runner supported directly by Zed for zero-cost completions.
- [Codeium](codeium.md) — High-speed code completion service with native Zed integration.

## Sources / references
- [Zed Official Website](https://zed.dev/)
- [Zed Documentation & Assistant Guide](https://zed.dev/docs)
- [Zed Open-Source Repository on GitHub](https://github.com/zed-industries/zed)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
