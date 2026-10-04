# Cline

## What it is
**Cline** (formerly Claude Dev) is an open-source, autonomous AI coding agent operating natively within Visual Studio Code, JetBrains IDEs, and headless terminal execution environments. Designed as an industry-standard platform for enterprise software development, Cline possesses comprehensive, safe access to the local filesystem, terminal sub-processes, an embedded Chromium browser instance for visual UI testing, and **FastMCP 3.1** (Model Context Protocol) tool servers. Built for human-in-the-loop security and deterministic task execution, Cline orchestrates frontier reasoning models ([Claude 5.6](../tools/providers/anthropic.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md), [DeepSeek-V4](../tools/providers/deepseek.md)) alongside local inference engines ([Ollama](../../services/ollama.md), [ExLlamaV2](../infrastructure/exllamav2.md)) to complete multi-file engineering tasks autonomously.

## What problem it solves
Conventional chat assistants and inline code completion plugins fail on complex, multi-file software engineering tasks due to key structural limitations:
- **Context Copy-Paste Friction**: Developers must manually copy code snippets, error traces, and documentation between the IDE and external chat windows.
- **Single-File Isolation**: Traditional AI completions lack awareness of project-wide file dependencies, build pipelines, and environment variables.
- **Execution-Blind Generation**: Code generated without terminal feedback or test verification frequently contains invisible build errors or runtime regressions.
- **Protocol Isolation**: Integrating custom internal APIs, secret vaults, and databases into the agent loop traditionally required bespoke plugin engineering.

Cline solves these challenges by operating as an **Autonomous Software Engineer inside the IDE**. It proactively explores codebase hierarchies, executes terminal commands, inspects browser rendering output, diagnoses test failures, and iteratively applies multi-file fixes until tasks pass all verifications.

## Where it fits in the stack
```
+-----------------------------------------------------------------------------------+
|                            DEVELOPER / IDE INTERFACE LAYER                        |
|                     (VS Code / JetBrains / Headless Cline CLI)                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           CLINE AGENT ORCHESTRATOR & ENGINE                       |
|      - Human-in-the-Loop (HITL) Safety & Approval Boundary                        |
|      - Autonomous Reasoning Loop & Plan Decomposition Engine                       |
|      - Context Window Optimizing & File Indexing Manager                           |
+-----------------------------------------------------------------------------------+
          |                                  |                                  |
          v                                  v                                  v
+------------------------+        +------------------------+        +------------------------+
|   LOCAL SYSTEM TOOLS   |        |   FASTMCP 3.1 SERVERS  |        |    LLM PROVIDERS       |
|   - File System Read/Edit|      |   - Playwright-MCP     |        |   - Claude 5.6 / GPT-5.6   |
|   - Terminal Subprocess|        |   - DB Query / Vault   |        |   - DeepSeek-V4            |
|   - Browser Automation |        |   - Custom Tool APIs   |        |   - Local Ollama / vLLM    |
+------------------------+        +------------------------+        +------------------------+
```

Cline operates at the **Developer Experience & IDE Agent Layer**, bridging high-level developer prompts with automated codebase mutations, shell execution, visual inspection, and Model Context Protocol tool execution.

## Human-in-the-Loop (HITL) Safety & Execution Architecture

Cline enforces a strict **Human-in-the-Loop Safety Framework** to prevent unauthorized command execution or destructive file modifications:

```
+----------------------------------------------------------------------------------------------------+
|                                    CLINE PERMISSION ENGINE MATRIX                                  |
+-------------------+-----------------------------------+--------------------------------------------+
| Tool Action       | Execution Risk Level              | Safety Approval Mechanism                  |
+-------------------+-----------------------------------+--------------------------------------------+
| `read_file`       | Low (Read-only)                   | Auto-approved or single prompt             |
| `write_to_file`   | Medium (Filesystem mutation)      | Visual Diff Preview + User Confirmation    |
| `execute_command` | High (Shell execution)            | Explicit Terminal Command Approval Prompt  |
| `browser_action` | Medium (Headless navigation)      | Embedded Browser Screenshot Preview        |
| `use_mcp_tool`    | Variable (External tool call)     | FastMCP 3.1 Schema & Parameter Inspection  |
+-------------------+-----------------------------------+--------------------------------------------+
```

### Execution Loop Lifecycle
1. **Task Planning**: Cline decomposes a user prompt into a sequential, multi-step execution plan.
2. **Tool Request Proposal**: Before invoking a tool (e.g., editing `src/auth.ts` or running `npm test`), Cline displays the target file diff or terminal payload to the user.
3. **User Approval / Auto-Approval Gate**: The developer approves, rejects, or provides feedback on the proposed action.
4. **Tool Execution & Feedback Capture**: Cline receives stdin/stdout streams, error logs, or browser screenshots and uses them to refine subsequent steps in the reasoning loop.

## Typical use cases
- **Test-Driven Development (TDD) Loops**: Writing unit/integration test specifications, running test suites in the local terminal, capturing failure logs, and modifying implementation code autonomously until all tests pass.
- **Framework & Dependency Migrations**: Executing large-scale codebase refactoring (e.g., upgrading React 18 to 19 or Pydantic v1 to v2) across dozens of dependent files.
- **Visual Web UI Verification**: Using the embedded Chromium browser instance to navigate local web servers, take screenshots, test UI responsiveness, and verify frontend changes.
- **Database Schema & Migration Authoring**: Interfacing via FastMCP 3.1 tool servers to inspect database tables, execute migrations, and generate ORM model definitions.

## Strengths
- **Rigorous Human-in-the-Loop Safety**: Complete user visibility and granular approval controls over shell commands, file edits, and network actions.
- **First-Class FastMCP 3.1 Integration**: Connects to any standard FastMCP server to grant agents access to local databases, secrets vaults, and enterprise tools.
- **Local & Offline Execution Support**: Seamless operation with self-hosted models running on [Ollama](../../services/ollama.md) or [ExLlamaV2](../infrastructure/exllamav2.md) for strict data privacy compliance.
- **Transparent Execution Logging**: Complete audit history of reasoning steps, terminal commands, and raw tool inputs/outputs.

## Limitations
- **Context Window Usage**: Multi-file autonomous loops generate high token consumption, requiring active context pruning on large projects.
- **Resource Allocation**: Running background build tools, test runners, and embedded browser instances requires adequate host system memory.

## When to use it
- When implementing features requiring multi-file edits, build tool execution, and local test suite verification.
- For interactive refactoring where real-time browser visual inspection or terminal output feedback is essential.
- When enterprise privacy policies mandate local-first or air-gapped development using self-hosted models.

## When not to use it
- For instant single-line code inline completions where lighter autocomplete plugins are faster.
- In security-restricted corporate environments where IDE extensions are barred from spawning shell subprocesses.
- When requiring specialized custom persona prompt definitions (refer to [Roo Code](roo-code.md)).

## Getting started

### Installation & Configuration
1. Install **Cline** from the Visual Studio Code Marketplace or JetBrains Plugin Repository.
2. Click the Cline icon in the activity bar to open the workspace panel.
3. Open Settings and select your API Provider (Anthropic, OpenAI, OpenRouter, DeepSeek, or Ollama).
4. Enter your API key and set your target model (e.g., `claude-3-7-sonnet-20250219`, `gpt-4o`, or `deepseek-v3`).

## CLI examples

Execute headless tasks or verify system integration using the Cline CLI and shell tools:

```bash
# Install the Cline CLI globally
npm install -g cline

# Authenticate with your preferred provider key
cline auth

# Run an autonomous task in headless mode with auto-approval
cline -y "Refactor authentication middleware to use AsyncLocalStorage"

# Run a codebase dependency audit task
cline task "Audit project dependencies and source files for hardcoded secrets"

# Verify installed CLI version
cline --version
```

## API examples

### FastMCP 3.1 Codebase Security Scanner Tool Server for Cline

This FastMCP 3.1 server provides security auditing capabilities directly to Cline agents:

```python
"""
FastMCP 3.1 Codebase Security Auditor for Cline Agent Integration.
Enforces security rules and detects hardcoded credentials across source files.
"""

import re
from typing import List
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cline-security-auditor", version="3.1.0")

class AuditRequest(BaseModel):
    file_path: str = Field(..., description="Target relative file path to scan")
    file_content: str = Field(..., description="Raw text content of the file")

class VulnerabilityIssue(BaseModel):
    line_number: int
    rule_id: str
    severity: str
    description: str

@mcp.tool(
    name="scan_file_security",
    description="Scan file content for secret leaks, API keys, and insecure patterns."
)
def scan_file_security(request: AuditRequest) -> List[VulnerabilityIssue]:
    """
    Scans code content for common credentials and security flaws.
    """
    findings = []
    lines = request.file_content.split("\n")

    secret_patterns = [
        (r"(?i)(api_key|secret_key|password)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "SEC-001", "CRITICAL", "Hardcoded credential detected"),
        (r"eval\s*\(", "SEC-002", "HIGH", "Insecure eval() execution detected"),
    ]

    for idx, line in enumerate(lines, start=1):
        for pattern, rule_id, severity, desc in secret_patterns:
            if re.search(pattern, line):
                findings.append(VulnerabilityIssue(
                    line_number=idx,
                    rule_id=rule_id,
                    severity=severity,
                    description=desc
                ))
    return findings

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Cline MCP Configuration Validation Schema

```python
"""
Pydantic v2 Validation Model for Cline MCP Server Configuration File.
Validates environment parameters, command executables, and server arguments.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class MCPServerConfig(BaseModel):
    command: str = Field(..., description="Executable tool binary (e.g., node, python, npx)")
    args: List[str] = Field(default_factory=list, description="Command arguments passed to server binary")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment variables for the subprocess")

    @field_validator("command")
    @classmethod
    def validate_command(cls, cmd: str) -> str:
        allowed_executables = {"node", "npx", "python", "python3", "uvx", "docker"}
        if cmd not in allowed_executables:
            raise ValueError(f"Executable '{cmd}' is not in allowed binary set: {allowed_executables}")
        return cmd

class ClineSettings(BaseModel):
    mcp_servers: Dict[str, MCPServerConfig] = Field(..., alias="mcpServers")

# Execution Example
if __name__ == "__main__":
    raw_config = {
        "mcpServers": {
            "security-auditor": {
                "command": "python3",
                "args": ["-m", "mcp_security_auditor"],
                "env": {"AUDIT_LEVEL": "STRICT"}
            }
        }
    }
    validated = ClineSettings.model_validate(raw_config)
    print("Successfully validated Cline settings:")
    print(validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Roo Code](roo-code.md) — Multi-persona fork of Cline with custom `.roomodes`.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's CLI-native agent harness.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — FastMCP 3.1 standard specification.
- [Playwright-MCP](../automation_orchestration/playwright-mcp.md) — Browser automation tools for agents.
- [Ollama](../../services/ollama.md) — Self-hosted local inference engine.

## Sources / references
- [Cline Official GitHub Repository](https://github.com/cline/cline)
- [Cline Official Documentation](https://docs.cline.bot/)
- [Model Context Protocol Standard](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
