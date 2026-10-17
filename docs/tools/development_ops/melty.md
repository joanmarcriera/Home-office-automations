# Melty

## What it is
Melty is an open-source, AI-native Integrated Development Environment (IDE) designed to act as a stateful, "human-in-the-loop" collaborator that understands the intent behind every code change. Built on a fully transparent VS Code-fork foundation, Melty implements a continuous "Intent-State" synchronization loop. As of early 2027, Melty fully supports frontier SOTA late 2026/2027 models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6 VL). Rather than acting as a simple passive autocomplete helper, Melty operates as an active pair programmer, tracking real-time development context, terminal outputs, build failures, and git diffs to co-author software iteratively alongside the developer.

## What problem it solves
Solves the cognitive friction and "black box" generation issues associated with traditional AI coding assistants. Standard tools often generate massive code dumps that are disconnected from the developer’s high-level architecture or current design patterns.

Melty addresses this by tracking the developer's "Intent" incrementally across terminal sessions, compiler messages, and version control states. It reduces code-review overhead, mitigates model hallucinations by grounding context in current git diffs, and eliminates the risk of silent, untracked modifications by managing changes through explicit state verification loops.

## System Architecture & Intent-State Synchronization Loop

Melty operates an active event-driven loop that captures developer actions, terminal output streams, and git index mutations to update the LLM's active working context:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     Developer / IDE Interface                          │
│        (Melty Visual Editor / Terminal Window / File Editor)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Active Intent / Keyboard Inputs
┌───────────────────────────────────▼────────────────────────────────────┐
│                    MELTY INTENT-STATE ENGINE                           │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────┐ │
│ │ Git Diff Tracker     │ │ Terminal Stream      │ │ FastMCP 3.1      │ │
│ │ & Staged File Index  │ │ Listener & Linter    │ │ Tool Client      │ │
│ └──────────────────────┘ └──────────────────────┘ └──────────────────┘ │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Context Stream & Prompt Construction
┌───────────────────────────────────▼────────────────────────────────────┐
│               LLM Provider Layer (Local & Cloud SOTA)                   │
│        (Claude 5.6 / GPT-5.6 / DeepSeek-V4 / Local Gemma 4)            │
└────────────────────────────────────────────────────────────────────────┘
```

### Event Hook & State Verification Pipeline

1. **Intent Registration**: Developer enters a high-level intent (e.g., "Refactor SQL queries to use Asyncpg and handle pool timeouts").
2. **Context Snapshotting**: Melty queries the local git status, reads active file diffs, and fetches current compiler/linter warnings from the integrated terminal buffer.
3. **Targeted Code Mutator Execution**: Melty dispatches a multi-file diff proposal to the configured LLM (e.g. Claude 5.6).
4. **Verification & Self-Correction**: The proposed diff is applied to a working buffer. Melty executes the local test suite via terminal. If a test fails, the output stack trace is fed back into the model for immediate self-healing.

```
Developer              Melty IDE Engine           LLM Provider            Terminal / Test Suite
    │                         │                        │                            │
    │── Enter Intent ────────>│                        │                            │
    │  ("Fix Async Memory")   │── Snapshot Git Diff ──>│                            │
    │                         │   & Active Workspace   │                            │
    │                         │<── Proposed Code Diff ─│                            │
    │                         │                        │                            │
    │                         │── Run Test Suite ──────────────────────────────────>│
    │                         │<── Test Failure Log (Stack Trace) ──────────────────│
    │                         │                        │                            │
    │                         │── Self-Correction Prompt ──────────────────────────>│
    │                         │<── Corrected Diff ─────│                            │
    │<── Present Diff Preview ─│                        │                            │
```

## Where it fits in the stack
**Development & Ops**. It serves as the primary developer workspace and AI-assisted code editor. Positioned as a fully open-source, customizable alternative to proprietary tools like [Cursor](cursor.md) or [Windsurf](windsurf.md), Melty sits at the intersection of local coding runtimes and remote or local LLM providers. It coordinates directly with terminal pipelines and git workflows, offering native hooks for external agentic orchestrators and repository managers via FastMCP 3.1.

## Feature Comparison Matrix

| Feature / Metric | Melty | Cursor | Windsurf | Aider | Zed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Open Source Status** | 100% Open Source | Proprietary | Proprietary | Open Source | Open Source |
| **Foundation Base** | VS Code Fork | VS Code Fork | VS Code Fork | Terminal CLI | Custom Rust GUI |
| **Intent-State Sync Loop**| Native | Partial | Cascade Agent | Git-based | Basic |
| **Terminal Log Inspection**| Native Real-time | Manual / Extension| Agent Guided | Auto-Injected | Manual |
| **FastMCP 3.1 Ready** | Native Client/Server | Proprietary MCP | Native MCP | Community | Native MCP |
| **Self-Hosted LLM Support**| Native (Ollama/vLLM) | Limited | Limited | Native | Native |
| **Headless CLI Mode** | Native (`melty apply`) | No | No | Native | No |

## Typical use cases
- **Intent-Driven Greenfield Prototyping**: Generating and scaffolding clean, module-based structures from high-level developer intents while keeping the developer's feedback loop tightly integrated.
- **Continuous Real-Time Refactoring**: Aligning existing codebases with modern design conventions, where the AI suggests structural improvements as you write, responding dynamically to compiler outputs and linter warnings.
- **SSH and Remote Environment Synchronization**: Developing directly on remote VMs or container environments using a local Melty instance connected over secure SSH/terminal channels.
- **Multi-File Context-Aware Coding**: Working on features where modifications span across several frontend files, backend controllers, and database schemas concurrently, with the AI tracking files in a consolidated, active workspace context.
- **Headless CI/CD Refactoring Loops**: Executing batch code migrations in headless mode (`melty apply`) within automated GitHub Actions pipelines.

## Strengths
- **Open-Source Transparency**: Fully open-source codebase, allowing deep, enterprise-level modifications, custom branding, and absolute privacy compliance.
- **Stateful Git & Terminal Tracking**: Natively listens to local git diff changes and terminal output streams, allowing models to immediately self-correct errors if a build or test command fails.
- **Native MCP 3.1 / FastMCP 3.1 Integration**: Operates as a robust Model Context Protocol client and server, enabling developers to connect third-party MCP servers for dynamic database query execution, file system management, and real-time cloud resource access.
- **Multi-Model Orchestration**: Supports swappable local and remote models, allowing developers to execute heavy-weight tasks with Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, or DeepSeek-V4, and light-weight local autocompletion tasks using local Gemma 4 or Qwen 3.6 instances via Ollama.
- **Headless Automation Ready**: Provides CLI commands to execute intent-driven code transformations without launching the visual UI.

## Limitations
- **Ecosystem Footprint**: Although built as a VS Code fork, some specialized proprietary extensions (such as closed marketplace debuggers) require manual configuration.
- **Resource Footprint**: Active terminal scanning, real-time git state diffing, and maintaining high-dimensional local semantic vector indexes can be resource-intensive on older hardware (<16GB RAM).
- **Dependency on High-Tier Reasoning**: Simpler, quantized offline models (<7B parameters) can sometimes lose track of multi-file intents, necessitating frontier model access for complex, multi-layered refactoring.

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Resolution / Operational Action |
| :--- | :--- | :--- |
| **Terminal Hook Disconnect** | Terminal buffer buffer size exceeded | Increase `melty.terminal.bufferSize` in settings and restart daemon. |
| **Semantic Vector Index Out-of-Sync** | Unindexed file additions or heavy branch switching | Run `melty index --rebuild --exclude "**/node_modules/**"` to refresh. |
| **FastMCP Server Connection Timeout** | FastMCP 3.1 port conflict or missing secret | Verify MCP server status via `melty mcp status` and check environment variables. |
| **Model Self-Correction Loop Stall** | Test suite producing non-deterministic outputs | Isolate unit test suite execution using `melty apply --test-command "pytest tests/unit"`. |
| **High CPU Usage During Indexing** | Large binary artifacts being scanned | Ensure `.gitignore` and `.meltyignore` contain `dist/`, `.git/`, and data directories. |

## Operational Best Practices & Guardrails

1. **Explicit Test Suite Hooking**: Configure explicit test execution commands (`melty config set test_cmd "npm test"`) so the Intent-State engine can verify code diffs automatically before presenting them.
2. **Context Scope Granularity**: Keep individual developer intents focused on single modules or related files rather than repository-wide transformations to maximize model precision.
3. **Secret Masking**: Verify that `.env` files and API tokens are listed in `.meltyignore` to prevent accidental inclusion in LLM prompt contexts.
4. **Local Fallback Setup**: Configure Ollama with local Qwen 3.6 or Gemma 4 models as a fallback provider when working in offline or air-gapped environments.
5. **Incremental Git Commits**: Commit or stage clean code checkpoints before launching large AI-driven refactoring passes.

## When to use it
- When you are looking for an open-source AI-native IDE that prioritizes developer intent, privacy, and continuous collaboration over passive black-box autocomplete.
- When you require a development environment that natively integrates with the [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) to dynamically extend your LLM's capabilities.
- For team-wide development where open-source transparency is necessary to ensure strict intellectual property and data sovereignty boundaries.
- When automating headless repository transformations inside CI/CD pipelines.

## When not to use it
- If your daily development workflows require heavy visual, multi-editor GUI configurations or proprietary extension suites that are tightly locked to official closed marketplaces.
- If you are seeking a terminal-native, keyboard-only environment (in which case, [Aider](aider.md), [Junie CLI](junie-cli.md), or [Terminus 2](terminus-2.md) are more appropriate choices).
- In highly resource-constrained environments where running an active, background-indexing visual IDE causes visible latency.

## Getting started

### Installation
Melty can be installed as a precompiled standalone binary or compiled directly from source for local modification.

```bash
# Clone the repository and install dependencies
git clone https://github.com/meltylabs/melty.git
cd melty
npm install

# Run Melty in development mode
npm run dev
```

### Configuration and Model Setup
Upon launching, Melty prompts for a preferred model provider. Configure your credentials or local endpoint:

```bash
# Configure Melty to use a local Ollama instance for Qwen 3.6 / Gemma 4
melty config set provider ollama --url http://localhost:11434 --model gemma-4

# Or configure remote API credentials
melty config set provider anthropic --api-key $ANTHROPIC_API_KEY --model claude-5.6
```

## CLI examples
Melty features a command-line interface for starting the editor, indexing repositories, and executing headless refactoring.

### Opening a Repository
```bash
# Open the current directory in Melty
melty .
```

### Running Headless Refactoring Loops
```bash
# Run Melty in headless mode to apply changes based on an intent
melty apply --intent "Refactor controllers to use async/await syntax and log output" --path ./src/controllers
```

### Workspace Indexing
```bash
# Force-refresh the local vector index of the codebase
melty index --rebuild --exclude "**/node_modules/**"
```

### Checking MCP Server Status
```bash
# List active FastMCP 3.1 connections
melty mcp status
```

## API examples

### Custom Intent Provider (TypeScript)
Developers can register custom intent providers to intercept and modify Melty's AI recommendations.

```typescript
import { MeltyExtension, IntentContext, ProposedDiff } from '@melty/sdk';

export class DatabaseOptimizerExtension implements MeltyExtension {
  id = 'db-optimizer';

  async onIntentDetected(intent: string, context: IntentContext): Promise<ProposedDiff | null> {
    if (intent.toLowerCase().includes('optimize query') || intent.toLowerCase().includes('index sql')) {
      const activeSQLFiles = await context.getFilesByPattern('**/*.sql');

      // Inject database context or analyze schemas
      const systemPrompt = `Analyze the SQL files: ${activeSQLFiles.map(f => f.name).join(', ')} and suggest optimized indexes.`;
      const completion = await context.llm.generate(systemPrompt);

      return context.createDiffFromCompletion(completion);
    }
    return null;
  }
}
```

### Subprocess Workspace State Check (Python & Pydantic v2)
Integrate external validation engines with Melty's active "Intent-State" loop via standard output. This example uses robust **Pydantic v2** validation to enforce schema correctness of the returned session state.

```python
import subprocess
import json
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class MeltySessionState(BaseModel):
    current_intent: str = Field(..., description="The high-level objective/intent currently tracked by Melty")
    staged_diff_files: List[str] = Field(default_factory=list, description="List of files with uncommitted changes")
    active_mcp_servers: List[str] = Field(default_factory=list, description="Currently connected FastMCP 3.1 server URIs")
    model_provider: str = Field(..., description="LLM provider name, e.g., 'anthropic' or 'ollama'")
    model_name: str = Field(..., description="The model currently in use, e.g., 'claude-5.6'")
    is_headless_active: bool = Field(default=False, description="Whether headless mode is currently running")

    @field_validator("model_provider")
    @classmethod
    def validate_provider(cls, value: str) -> str:
        valid_providers = ["anthropic", "openai", "google", "ollama", "vllm", "deepseek"]
        if value.lower() not in valid_providers:
            raise ValueError(f"Provider must be one of {valid_providers}")
        return value.lower()

def get_melty_session_state() -> Optional[MeltySessionState]:
    """Queries Melty's headless daemon and parses state with strict Pydantic v2 validation."""
    try:
        response = subprocess.run(
            ["melty", "state", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        parsed_json = json.loads(response.stdout)
        # Enforce strict validation via Pydantic v2
        state = MeltySessionState.model_validate(parsed_json)
        return state
    except subprocess.CalledProcessError as e:
        print(f"Error fetching Melty state: {e.stderr}")
        return None
    except ValidationError as e:
        print(f"Melty session state schema mismatch: {e}")
        return None

if __name__ == "__main__":
    state = get_melty_session_state()
    if state:
        print(f"Active Intent: {state.current_intent}")
        print(f"Pending changes in {len(state.staged_diff_files)} files.")
        print(f"Model In Use: {state.model_name} via {state.model_provider}")
```

### Complete FastMCP 3.1 Server Bridge Example
Bridge Melty's Intent-State engine to external multi-agent networks (**Claude 5.6**, **GPT-5.6**) using a Python **FastMCP 3.1** server wrapper:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, List

mcp = FastMCP("Melty-IDE-Bridge")

class ApplyIntentInput(BaseModel):
    intent_text: str = Field(..., description="High-level refactoring intent")
    target_path: str = Field(default=".", description="Target directory or file path")
    run_tests: bool = Field(default=True, description="Execute test suite after diff generation")

class WorkspaceStatusInput(BaseModel):
    include_git_diff: bool = Field(default=True)

@mcp.tool()
async def apply_code_intent(payload: ApplyIntentInput) -> Dict[str, Any]:
    """Executes a headless refactoring pass in Melty using current Intent-State loop."""
    # Simulates dispatching intent to Melty daemon
    return {
        "status": "success",
        "intent_applied": payload.intent_text,
        "files_modified": [f"{payload.target_path}/main.py"],
        "tests_passed": payload.run_tests,
        "fastmcp_version": "3.1"
    }

@mcp.tool()
async def query_workspace_context(payload: WorkspaceStatusInput) -> Dict[str, Any]:
    """Retrieves active Melty workspace state, uncommitted git diffs, and terminal logs."""
    return {
        "active_branch": "main",
        "uncommitted_files_count": 2,
        "recent_terminal_status": "COMPILER_OK",
        "connected_mcp_servers": ["db-inspector", "git-mcp"]
    }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Cursor](cursor.md) — A popular proprietary AI-native IDE built on VS Code.
- [Zed](zed.md) — A high-performance, collaborative visual code editor written in Rust.
- [Codeium](codeium.md) — Multi-IDE AI developer productivity and autocomplete platform.
- [Windsurf](windsurf.md) — SOTA visual IDE implementing the Cascade interaction model.
- [Aider](aider.md) — High-performance terminal-native pair programmer and git integration assistant.
- [Junie CLI](junie-cli.md) — Terminal companion and indexer.
- [Terminus 2](terminus-2.md) — Open-source terminal-native AI agent baseline with a tmux bridge.
- [GPT Engineer](gpt_engineer.md) — Rapid prototyping and scaffolding orchestrator for greenfield codebases.
- [Sourcegraph Cody](sourcegraph_cody.md) — Multi-repository code intelligence and semantic context indexing client.
- [Anti-Gravity](anti_gravity.md) — Enterprise-grade agentic development and execution framework.
- [Droid](droid.md) — Enterprise-grade AI coding orchestrator configuring dedicated sub-agents.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Automated development architectures and code production systems.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration patterns for multi-step AI planning.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — FastMCP 3.1 standard for integrating AI tools and data sources.

## Sources / references
- [Melty Labs Official Website](https://melty.sh/)
- [Melty GitHub Repository](https://github.com/meltylabs/melty)
- [Melty Technical Architecture Wiki](https://github.com/meltylabs/melty/wiki)
- [Model Context Protocol v3.1 Specification](https://modelcontextprotocol.org)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
