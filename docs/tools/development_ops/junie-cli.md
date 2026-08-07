# Junie CLI

## What it is
Junie CLI is an AI-driven, high-speed, terminal-native codebase navigation and autonomous software engineering assistant developed under the JetBrains AI Lab initiative. As of late December 2026, the stable **v2.0+** release acts as an enterprise-grade background daemon and command-line companion. Optimized for sub-second terminal interactions, it leverages state-of-the-art JetBrains models and frontier reasoning systems (including Claude 5.1, GPT-5.5, Llama 4, Gemma 3, and Qwen 3.6) to enable lightning-fast terminal-centric editing, tmux-native testing, and semantic codebase auditing.

## What problem it solves
It eliminates the high-latency context-switching overhead and massive system memory footprint associated with graphic-heavy AI IDEs. Remote developers working over SSH connections or nested tmux panes gain real-time, repository-wide intelligence without relying on heavy graphical interfaces. Furthermore, it overcomes the static boundaries of traditional command-line utilities by executing autonomous, multi-step agentic loops—safely running tests, checking compilation outputs, reading terminal buffers, and self-correcting errors.

## Where it fits in the stack
**Development & Ops**. It serves as an **AI-Native Shell Companion and Orchestrator**, interfacing directly with local shells, Git filesystems, search utilities (like `rg` and `fd`), and background model servers.

## Typical use cases
- **SSH-Based Remote Refactoring**: Running autonomous, multi-file code modifications on distant cloud-hosted environments without GUI overhead.
- **Tmux-Bridge Automation**: Executing parallel test-run and code-fix loops in isolated tmux splits, continuously monitoring execution status until all tasks succeed.
- **Sub-Second Code Navigation**: Generating a highly compressed local vector cache to locate complex relational code pathways instantly.
- **Security & Compliance Auditing**: Programmatically reviewing code changes against custom architecture rulesets before commits.

## Strengths
- **Stable v2.0 tmux-Bridge**: Deeply understands tmux pane matrices, enabling background pane spawning, live buffer analysis, and non-blocking command execution.
- **Native MCP 3.1 / FastMCP 3.1 Protocol**: Functions natively as both an MCP client and server to stream execution parameters, tool metrics, and schema trees.
- **High-Performance Rust Indexer**: Features an optimized local semantic database that builds indexes across millions of code lines in sub-second timeframes.
- **Keyboard-First Interface**: Fits seamlessly into advanced development environments using Vim, Neovim, Helix, or standard command line interfaces.

## Limitations
- **No GUI Layout**: Relies entirely on command-line terminal structures, lacking visual side-by-side diff comparisons or interactive file trees.
- **Advanced UNIX Curve**: Demands proficiency in standard shell commands, tmux multiplexing, and pipeline redirection to exploit its complete power.
- **Compute Bound**: Demands access to frontier-tier reasoning APIs (like Claude 5.1 or GPT-5.5) for complex, long-horizon bug-fixing tasks.

## When to use it
- When you are a terminal-centric developer utilizing keyboard-focused environments (such as Neovim or Helix) within nested tmux workspaces.
- When performing fast exploration, semantic indexing, or autonomous code changes on remote environments over SSH.
- For building fully automated code production pipelines within modern software factories.

## When not to use it
- If your daily development workflows are highly dependent on rich mouse-driven GUIs, visual debugging panels, or graphical interactive timelines.
- When working entirely offline on highly restricted developer workstations with insufficient local CPU/GPU capacities to support high-tier models.

## Getting started

### Installation
Junie CLI v2.0+ is distributed as a global binary and cargo crate. Install it using the default system toolchains:

```bash
# Globally install via npm
npm install -g @jetbrains/junie-cli

# Or compile from source via cargo
cargo install junie-cli
```

### Basic Setup
Initialize the local database and build the semantic repository workspace index:
```bash
# Initialize local index db
junie init

# Set model endpoints and configure active API credentials
junie configure --model claude-5.1 --provider anthropic
```

## CLI examples
The command-line interface provides high-performance access to its underlying agentic capabilities.

### Semantic codebase exploration
```bash
junie ask "Where are the FastMCP 3.1 session authentication contexts created and validated?"
```

### Tmux-Native Refactoring Run
```bash
junie run "Refactor all authentication decorators in src/middleware/ to comply with FastMCP 3.1. Compile and execute npm test." --tmux-bridge
```

### Run Workspace Architecture Audit
```bash
junie audit --ruleset "./rules/mcp-3.1-compliance.json" --output "./reports/audit_summary.md"
```

## API examples

### JavaScript Custom Schema Integration
Extend Junie CLI v2.0+'s daemon capabilities with custom JavaScript/TypeScript plugin schemas loaded at runtime:

```javascript
// schema-audit-plugin.js
export const skill = {
  name: "schema-integrity-checker",
  description: "Validates database schema configurations against FastMCP 3.1 rules",
  async run(context) {
    const schemas = await context.workspace.findFiles("**/db/schemas/*.json");
    const violations = [];

    for (const file of schemas) {
      const parsed = JSON.parse(await file.read());
      if (!parsed.hasOwnProperty("version") || parsed.version !== "3.1") {
        violations.push({ file: file.path, message: "Outdated schema version. FastMCP 3.1 required." });
      }
    }

    return {
      status: violations.length === 0 ? "passed" : "failed",
      violations
    };
  }
};
```

### Python Programmatic Daemon Controller
Wrap and orchestrate Junie's workspace-indexing features inside external Python workflows utilizing Pydantic v2 schemas:

```python
import subprocess
import json
from pydantic import BaseModel, Field
from typing import List, Optional

class JunieSearchResult(BaseModel):
    file_path: str = Field(..., alias="file")
    similarity_score: float = Field(..., alias="score")
    matched_lines: List[int] = Field(..., alias="lines")
    snippet: str

class JunieResponse(BaseModel):
    query: str
    matches: List[JunieSearchResult]
    execution_time_ms: int

def execute_semantic_lookup(query: str) -> Optional[JunieResponse]:
    """Spawns the Junie CLI to execute a fast semantic lookup across the codebase."""
    try:
        res = subprocess.run(
            ["junie", "search", query, "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(res.stdout)
        return JunieResponse.model_validate(data)
    except Exception as e:
        print(f"Failed to query semantic daemon: {e}")
        return None

# Execute lookup
response = execute_semantic_lookup("JWT token validation payload")
if response:
    print(f"Found {len(response.matches)} files in {response.execution_time_ms}ms")
```

## Related tools / concepts
- [Claude Code](claude-code.md)
- [ripgrep (rg)](ripgrep.md)
- [Aider](aider.md)
- [Melty](melty.md)
- [Sourcegraph Cody](sourcegraph_cody.md)
- [Terminus 2](terminus-2.md)
- [GPT Engineer](gpt_engineer.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [JetBrains Junie CLI Homepage](https://junie.jetbrains.com/)
- [JetBrains AI Lab Research and Documentation Portal](https://blog.jetbrains.com/ai/)
- [GitHub - JetBrains Junie CLI Repository](https://github.com/jetbrains/junie)

---
## Contribution Metadata
- Last reviewed: 2026-12-19
- Confidence: high
