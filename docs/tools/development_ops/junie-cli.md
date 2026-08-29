# Junie CLI

## What it is
Junie CLI is an AI-driven, high-speed, terminal-native codebase navigation and autonomous software engineering assistant developed under the JetBrains AI Lab initiative. As of early January 2027, the stable **v2.5+** release functions as an enterprise background daemon and CLI companion. Built with native support for the **FastMCP 3.1 Task Protocol**, it leverages state-of-the-art JetBrains models and frontier reasoning engines (including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL) to deliver sub-second codebase search, tmux-native test orchestration, and semantic repository auditing.

## What problem it solves
It eliminates the high-latency context switching and system resource consumption associated with heavy GUI IDEs. Remote developers working over SSH connections or inside multi-pane tmux workspaces gain real-time, repository-wide intelligence without leaving the command line. Furthermore, Junie CLI executes autonomous, multi-step agentic loops—running test suites, evaluating terminal buffer outputs, reading build failures, and applying self-correcting patches in isolated background panes.

## Where it fits in the stack
**Development & Ops**. It serves as an **AI-Native Shell Companion and Orchestrator**, interfacing directly with local shells, Git repositories, search engines (like `rg` and `fd`), and FastMCP 3.1 model servers.

## Typical use cases
- **SSH-Based Remote Refactoring**: Running autonomous, multi-file code modifications on distant cloud servers over lightweight terminal sessions.
- **Tmux-Bridge Test Automation**: Spawning isolated background tmux splits to execute test-run and code-fix loops, continuously monitoring build status until completion.
- **Sub-Second Code Navigation**: Leveraging a high-performance local vector and keyword cache to map relational code dependencies instantly.
- **Security & Compliance Auditing**: Programmatically verifying code changes against enterprise architecture rulesets before commits.

## Strengths
- **Tmux-Bridge Automation Matrix**: Native understanding of tmux window and pane hierarchies, enabling non-blocking background command execution and terminal buffer analysis.
- **Native MCP 3.1 & FastMCP 3.1 Client/Server**: Programmatically streams execution contexts, tool schemas, and task resolution state across distributed agent networks.
- **High-Performance Rust Indexer**: Sub-second indexing capability across million-line codebases with minimal memory overhead.
- **Keyboard-First Interface**: Integrates cleanly into terminal workflows utilizing Vim, Neovim, Helix, or standard zsh/bash environments.

## Limitations
- **Terminal Only**: Lacks visual side-by-side GUI diff editors or mouse-driven interactive panels.
- **UNIX & Tmux Curve**: Requires familiarity with command-line environment variables, shell pipelines, and tmux session management.
- **API Token Bounded**: Long-horizon multi-file refactoring runs depend on access to frontier model endpoints (Claude 5.6 or GPT-5.6).

## When to use it
- When working in keyboard-centric terminal environments (Neovim, Helix, tmux) over local or SSH connections.
- When performing rapid code exploration, semantic indexing, or autonomous bug fixing in large codebases.
- For integrating automated software refactoring tasks into continuous development workflows.

## When not to use it
- When daily development depends heavily on visual GUI layout managers, drag-and-drop debugging UI, or graphical timelines.
- On offline or strictly air-gapped workstations without local LLM capabilities or external API access.

## Getting started

### Installation
Junie CLI v2.5+ is distributed as a global binary npm package or cargo crate:

```bash
# Globally install via npm
npm install -g @jetbrains/junie-cli

# Or compile from source via cargo
cargo install junie-cli
```

### Basic Setup
Initialize the workspace index and configure active model endpoints:
```bash
# Initialize local index db
junie init

# Set model endpoints and provider credentials
junie configure --model claude-5.6 --provider anthropic
```

## CLI examples
The command-line interface provides fast, direct access to its agentic features.

### Semantic Codebase Exploration
```bash
junie ask "Where are the FastMCP 3.1 session authentication contexts created and validated?"
```

### Tmux-Native Refactoring Run
```bash
junie run "Refactor all authentication decorators in src/middleware/ to comply with FastMCP 3.1. Compile and execute npm test." --tmux-bridge
```

### Workspace Architecture Audit
```bash
junie audit --ruleset "./rules/mcp-3.1-compliance.json" --output "./reports/audit_summary.md"
```

## API examples

### JavaScript Custom Schema Integration
Extend Junie CLI's daemon capabilities with custom plugin schemas loaded at runtime:

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
- Last reviewed: 2027-01-07
- Confidence: high
