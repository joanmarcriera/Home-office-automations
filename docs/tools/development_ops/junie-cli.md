# Junie CLI

## What it is
Junie CLI is an AI-driven, high-speed, terminal-native codebase navigation and autonomous software engineering assistant developed under the JetBrains AI Lab initiative. As of July 2026, **v1.8+** (nearing stable **v2.0**) acts as a lightweight daemon and a stateful command-line companion. Optimized for low-latency terminal interactions, it is powered by JetBrains AI Lab SOTA models and frontier reasoning engines (such as Claude 5.1, GPT-5.5, Llama 4, Gemma 3, and Qwen 3.6), enabling rapid, keyboard-first codebase navigation, semantic auditing, and tmux-native editing.

## What problem it solves
Eliminates high-latency context switching and the substantial memory footprint associated with modern graphical AI IDEs. It provides developers on remote SSH connections or nested tmux sessions with instant repository-wide semantic intelligence. Additionally, it overcomes the static boundaries of traditional command-line utilities by implementing stateful multi-step loops—permitting the AI to safely execute commands, run tests, sniff terminal buffers, and self-correct compilation errors autonomously.

## Where it fits in the stack
**Development & Ops**. Functions as an intelligent, terminal-native developer companion and orchestrator. It sits directly on top of the local shell, bridging UNIX pipelines (such as `rg`, `fd`, and `git`) with remote or locally hosted LLMs. It functions alongside collaborative coding editors and lightweight autonomous agents in modern software factories.

## Typical use cases
- **Autonomous Tmux-Bound Multi-File Edits**: Spinning up an attached or detached tmux session to systematically execute a refactoring pattern, compile the results, read the standard error streams, and refine code files in real-time.
- **Sub-Second Semantic Code Navigation**: Locating specific logical flows and functional entry points inside multimillion-line repositories using local high-performance vector caching.
- **SSH-Native Repository Auditing**: Conducting comprehensive, lightweight security or design audits of codebases hosted on remote developer virtual machines without the overhead of X11 or VNC port forwarding.
- **Onboarding and Architecture Explanations**: Interrogating a new, unfamiliar repository via natural language queries to instantly map dependency relationships and configuration matrices.

## Strengths
- **Tmux-Bridge Protocol**: Deeply understands tmux pane states, enabling non-blocking terminal buffer reading, split-screen live terminals, and parallel multi-pane command execution.
- **High-Performance Rust Core**: Employs a blazing-fast local indexer written in Rust, generating and updating semantic repository indices in sub-second timeframes.
- **Zero-GUI, SSH-Optimized Footprint**: Consumes minimal RAM and network bandwidth, making it highly effective for editing codebases on remote cloud instances over flaky connections.
- **Native MCP 3.0/3.1 Integration**: Operates natively as both an MCP client and server, granting LLM reasoning engines standard access to git history, filesystem blocks, and pipeline telemetry.

## Limitations
- **No Rich Visual Interface**: Lacks graphical file-tree navigation, interactive side-by-side diff sliders, and visual timeline representations (reliant entirely on unified diffs and terminal terminal UI controls).
- **Steep CLI Mastery Curve**: Requires comfort with terminal workflows, tmux multiplexing, and advanced command line options to unlock its full utility.
- **Frontier Reasoning Dependence**: Simpler offline models often struggle with complex, long-horizon multi-step debugging tasks, requiring access to high-tier reasoning APIs for stable results.

## When to use it
- When you are a dedicated terminal developer using keyboard-centric editors like Vim, Neovim, or Helix within a tmux and shell workspace.
- When performing rapid, multi-file code exploration, structural searches, or lightweight automated audits.
- For managing, troubleshooting, and editing microservices directly on remote staging or production environments over SSH.

## When not to use it
- When your workflow depends heavily on a rich, mouse-driven graphical interface with integrated debugger panels and drag-and-drop file trees.
- For heavy frontend UI design and alignment tasks that require real-time, browser-native visual previews embedded alongside the editor window.
- In offline environments where secure local inference is mandatory but local hardware is insufficient to run SOTA 70B+ reasoning models.

## Getting started
### Installation
Junie CLI is distributed via common package registries and cargo crates. It can be installed globally using Node or Rust toolchains.

```bash
# Install the CLI globally via npm
npm install -g @jetbrains/junie-cli

# Or compile from source via cargo
cargo install junie-cli
```

### Initial Setup
To construct the local vector index and configure model provider endpoints, execute the initialize routine within the repository root:

```bash
# Initialize local database and index workspace
junie init

# Configure model endpoints and API keys
junie configure --model claude-5.1
```

## CLI examples
### Codebase Exploration
```bash
# Perform a semantic search on webhook execution
junie ask "Where and how are the checkout stripe webhooks validated and processed?"
```

### Stateful Tmux Refactoring
```bash
# Initiate an autonomous tmux-bound multi-file migration
junie run "Refactor all endpoints in src/api/ to use the new token schema, compile, and run cargo test to verify." --tmux-bridge
```

### Workspace Auditing
```bash
# Run a specific architecture audit and output the results as markdown
junie audit --ruleset "mcp-v3" --output "./reports/mcp_compliance.md"
```

## API examples
### JavaScript Custom Skill Definition
Junie CLI enables developers to extend its capabilities with custom JavaScript or TypeScript skill definitions loaded at runtime.

```javascript
// custom-validator.js
export const skill = {
  name: "db-schema-validator",
  description: "Validates local schema structures against model definitions",
  async run(context) {
    // Access local files using the workspace utility
    const schemaFiles = await context.workspace.findFiles("**/schemas/*.sql");
    const results = [];

    for (const file of schemaFiles) {
      const content = await file.read();
      if (!content.includes("FOREIGN KEY")) {
        results.push({ file: file.path, issue: "Missing relational integrity check." });
      }
    }

    return {
      status: results.length === 0 ? "success" : "warning",
      issues: results
    };
  }
};
```

### Python Programmatic Subprocess Integration
Execute Junie's semantic indexer programmatically to integrate repository intelligence into automation tools.

```python
import subprocess
import json

def get_codebase_context(query_string: str) -> dict:
    """Invokes Junie CLI semantic indexer to fetch structured context."""
    try:
        result = subprocess.run(
            ["junie", "search", query_string, "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to query Junie: {e.stderr}")
        return {"error": "Execution failed"}

if __name__ == "__main__":
    context = get_codebase_context("JWT authentication expiration parameters")
    print(f"Retrieved {len(context.get('matches', []))} relevant file slices.")
```

## Related tools / concepts
- [Aider](aider.md) — For terminal-based, interactive collaborative pair programming and incremental editing.
- [ripgrep (rg)](ripgrep.md) — Fast command-line pattern search utility integrated directly with Junie's backend.
- [Claude Code](claude-code.md) — Interactive terminal coding agent from Anthropic.
- [Codeium](codeium.md) — Multi-IDE AI developer productivity platform and completion daemon.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Conceptual architectures for fully automated code production lines.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Recurring patterns for multi-step AI planning and execution.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standardized tool integration protocol natively supported by Junie.
- [Zed](zed.md) — High-performance, collaborative AI-native visual text editor.
- [Anti-Gravity](anti_gravity.md) — Google's enterprise agentic execution and orchestration framework.
- [Droid](droid.md) — Specialized enterprise-grade coding orchestrator configuring dedicated sub-agents.
- [Terminus 2](terminus-2.md) — Terminal-native AI agent baseline leveraging a tmux-to-LLM bridge.
- [GPT Engineer](gpt_engineer.md) — AI-driven greenfield codebase prototyping and scaffolding orchestrator.
- [Melty](melty.md) — Open-source AI-native IDE offering deep shell and git execution loops.
- [Sourcegraph Cody](sourcegraph_cody.md) — Multi-repository code intelligence and autonomous context indexing client.

## Sources / references
- [Junie CLI Home Page](https://junie.jetbrains.com/)
- [JetBrains AI Lab Research and Blog](https://blog.jetbrains.com/ai/)
- [GitHub - Junie CLI Discussions and Community](https://github.com/jetbrains/junie)
- [Model Context Protocol v3.0 Specification](https://modelcontextprotocol.org)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
