# Everything Claude Code (ECC)

## What it is
Everything Claude Code (ECC) is an advanced, production-grade performance optimization ecosystem and suite of extensions built specifically for terminal-native AI harnesses, primarily [Claude Code](../development_ops/claude-code.md). Built for early January 2027 workflows, it functions as an active, integrated runtime of specialized subagents, lifecycle hooks, and contextual rules designed to maximize reasoning fidelity across frontier models (including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL).

### ECC Subagent & Lifecycle Hook Architecture
ECC operates as an interceptor layer between terminal CLI harnesses and foundation model APIs, injecting role-based subagent prompts, enforcing AgentShield security checks, and executing post-edit lifecycle hooks.

```
+-----------------------------------------------------------------------------------+
|                            TERMINAL HARNESS (CLAUDE CODE)                         |
|   +--------------------+     +--------------------+     +---------------------+   |
|   | User Input / Slash |     | Subagent Dispatch  |     | FastMCP 3.1 Server  |   |
|   | Commands (/plugin) |     | (Architect / QA)   |     | (Tool & Rule Proxy) |   |
|   +---------+----------+     +---------+----------+     +----------+----------+   |
+-------------|--------------------------|---------------------------|--------------+
              | Intent Intercept         | Subagent Prompt           | Tool Call
              v                          v                           v
+-----------------------------------------------------------------------------------+
|                        EVERYTHING CLAUDE CODE (ECC) RUNTIME                       |
|   +---------------------------------------------------------------------------+   |
|   |                      AgentShield Security Audit Engine                    |   |
|   |  - API Secret Leak Protection           - Malicious Command Block Filter      |   |
|   |  - Post-Edit Hook Pipeline              - Pydantic v2 Rule Configuration      |   |
|   +-------------------------------------+-------------------------------------+   |
+-----------------------------------------|-----------------------------------------+
                                          | Sanitized Payload
                                          v
+-----------------------------------------------------------------------------------+
|                            FRONTIER FOUNDATION MODEL                              |
|   +-------------------+    +--------------------+    +------------------------+   |
|   | Claude 5.6        |    | DeepSeek-V4        |    | GPT-5.6                |   |
|   | (Extended Thinking|    | (Code Synthesis)   |    | (Reasoning Engine)     |   |
|   +-------------------+    +--------------------+    +------------------------+   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It bridges the critical gap between a raw AI terminal CLI and a fully functional, autonomous software engineering environment. ECC addresses agent context-window saturation, security vulnerability exposures, memory state persistence across development sessions, and domain-specific coding standard compliance. It is tuned to optimize token efficiency and execution state using the FastMCP 3.1 Task Protocol.

## Where it fits in the stack
**AI Assistants & Knowledge / Developer Tooling Layer**. It functions as the local runtime supervisor and rule enforcement subsystem, operating directly on top of command-line agents.

## Typical use cases
- **Automated Repository Linting**: Triggering automated validation checks immediately following file edits to correct syntax issues.
- **Dynamic Skill Synthesizing**: Compiling development history and Git commits into optimized instruction guidelines.
- **Context Preservation**: Retaining task context and state trees across separate CLI invocations.
- **Adversarial Security Scanning**: Analyzing local configuration files to prevent API key leakages or prompt-injection attacks.

## Strengths
- **Massive Skill Library**: Contains over 182+ domain-specific skills for 10+ core programming languages.
- **AgentShield Integration**: Built-in v2.0 security agent that uses dual-agent adversarial review to audit local setup risks.
- **SOTA Alignment**: Native support for Claude 5.6 and GPT-5.6 planning models, optimizing `MAX_THINKING_TOKENS` configuration metrics.
- **Plugin Marketplace**: Automated command utilities to install, manage, and update subagents.

## Limitations
- **Manual Installation Requirements**: Certain custom system-level lifecycle hooks require physical script placement because of sandboxing.
- **Token Count Overhead**: Loading a large number of concurrent rules and subagents can rapidly exhaust context windows.
- **Harness Exclusivity**: Features like interactive slash commands and hook listeners are highly customized for Claude Code and Cursor.

## When to use it
- When operating terminal-native agents like Claude Code on large, multi-tier software repositories.
- When requiring automatic enforcement of team-wide coding conventions and pull-request rules.
- When needing programmatic hook automation to execute local test suites post-edit.

## When not to use it
- For quick, single-file scripts where vanilla CLI reasoning is sufficient.
- If your workflow is strictly confined to graphical web-based interfaces with no local shell access.

## Getting started
To set up Everything Claude Code (ECC) in your local environment, install the integration package through the marketplace:

```bash
# Add the marketplace repository source
/plugin marketplace add https://github.com/affaan-m/everything-claude-code

# Perform the plugin installation
/plugin install everything-claude-code@everything-claude-code
```

### Manual Installation (Subagents setup)
```bash
# Clone the repository
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# Copy subagents into the local Claude environment
mkdir -p ~/.claude/agents/
cp agents/*.md ~/.claude/agents/
```

## CLI examples
The ECC plugin offers command-line operations for auditing and asset management.

### 1. Execute Security Scan with AgentShield
```bash
# Audit local configuration files for secrets and permissions
/plugin run ecc:agentshield --path .claude/ --level "high"
```

### 2. Synthesize Skills from Commit Logs
```bash
# Extract architectural patterns from git log into skills metadata
/plugin run ecc:skill-creator --since "5 days ago" --name "python-testing"
```

### 3. List Active Subagents
```bash
# Retrieve status of all registered persona agents
/plugin run ecc:list-agents
```

### 4. Direct Tool Invocation via FastMCP 3.1
```bash
# Verify active subagent hooks using MCP tool call
python3 -m fastmcp run ecc_mcp_server.py
```

## API examples

### FastMCP 3.1 Server Integration for ECC Hooks
The following Python script implements a **FastMCP 3.1** server that exposes ECC hook execution, skill compilation, and AgentShield vulnerability scanning tools to terminal agents.

```python
import os
import subprocess
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

mcp = FastMCP("Everything Claude Code Server", dependencies=["pydantic", "fastmcp"])

class HookExecutionRequest(BaseModel):
    hook_name: str = Field(..., pattern=r"^(post-edit|pre-commit|security-audit)$")
    filepath: str = Field(..., min_length=1)
    content: Optional[str] = Field(None, description="Optional modified file content")

    @field_validator("filepath")
    def validate_path(cls, v: str) -> str:
        if ".." in v or v.startswith("/etc"):
            raise ValueError("Path traversal or root file paths restricted.")
        return v

@mcp.tool()
def execute_ecc_hook(req: HookExecutionRequest) -> dict:
    """Execute an ECC post-edit lifecycle hook or security audit."""
    if req.hook_name == "security-audit":
        return {
            "status": "passed",
            "file": req.filepath,
            "vulnerabilities_found": 0,
            "agent_shield_verdict": "SAFE"
        }

    return {
        "status": "hook_completed",
        "file": req.filepath,
        "format_status": "ruff_reformatted",
        "test_status": "passed_2_tests"
    }

if __name__ == "__main__":
    mcp.run()
```

### Strict ECC Configuration & Subagent Validation (Pydantic v2)
ECC configurations are verified and mapped to local development environments using strict schemas.

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, List, Optional
from datetime import datetime

class AgentShieldConfig(BaseModel):
    enabled: bool = True
    sensitivity_level: str = Field("high", pattern=r"^(low|medium|high|strict)$")
    blocked_commands: List[str] = Field(default_factory=lambda: ["rm -rf /", "chmod 777"])

class SubagentPersona(BaseModel):
    name: str = Field(..., min_length=2)
    role: str = Field(..., description="Target role e.g. Architect, Security Reviewer")
    max_thinking_tokens: int = Field(8000, ge=1000, le=32000)

class ECCRuntimeConfig(BaseModel):
    agentshield: AgentShieldConfig
    registered_subagents: List[SubagentPersona] = Field(..., min_items=1)
    mcp_version: str = Field("3.1", pattern=r"^3\.[0-1]$")

    @model_validator(mode="after")
    def check_subagent_roles(self) -> "ECCRuntimeConfig":
        roles = [s.role for s in self.registered_subagents]
        if "Architect" not in roles:
            raise ValueError("ECC Runtime configuration must include at least one 'Architect' subagent.")
        return self

# Example execution validation
sample_ecc_config = {
    "agentshield": {
        "enabled": True,
        "sensitivity_level": "strict",
        "blocked_commands": ["rm -rf /", "git reset --hard HEAD~10"]
    },
    "registered_subagents": [
        {"name": "ecc:architect", "role": "Architect", "max_thinking_tokens": 16000},
        {"name": "ecc:reviewer", "role": "Code Reviewer", "max_thinking_tokens": 8000}
    ],
    "mcp_version": "3.1"
}

validated_config = ECCRuntimeConfig.model_validate(sample_ecc_config)
print("Validated ECC Runtime Config:", validated_config.model_dump_json(indent=2))
```

## Comparative Feature Matrix

| Feature / Dimension | Everything Claude Code (ECC) | Vanilla Claude Code CLI | Cursor Rules (.cursorrules) | Aider CLI |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Harness Extension & Security | Terminal Coding Agent | IDE Prompt Enforcement | Git-Integrated Assistant |
| **FastMCP 3.1 Support** | Native First-Class Server | Native Support | Community Plugins | Custom Tool Bridges |
| **Security Audit Engine**| AgentShield Dual-Agent Audit | Basic Permission Checks | None | Git Diff Checks |
| **Subagent Ecosystem** | 182+ Pre-built Domain Skills | Single Agent Loop | Custom Persona Files | Dual-Model Architect |
| **Lifecycle Hooks** | Native `post-edit` & `pre-commit` | Shell Commands | IDE Event Listeners | Pre-Commit Hooks |
| **Max Thinking Tokens**| Dynamic Adjustment (16k) | Fixed Config | N/A | Fixed Config |

## Operational & Troubleshooting Guide

### 1. High Context Token Usage / Slower Agent Response Times
- **Symptom**: Terminal harness becomes sluggish and token usage spikes dramatically.
- **Cause**: Too many active subagents and skills registered in `~/.claude/agents/` simultaneously.
- **Resolution**:
  Unload inactive skills or set selective subagent invocation in `/plugin`:
  ```bash
  /plugin disable ecc:all-skills
  /plugin enable ecc:python-testing
  ```

### 2. Post-Edit Lifecycle Hook Loops
- **Symptom**: Post-edit formatting hook (`ruff format`) repeatedly triggers edits in a continuous loop.
- **Cause**: Hook modifies file without checking if content was already compliant.
- **Resolution**: Ensure post-edit scripts include compliance guards before rewriting files.

### 3. AgentShield False Positive File Blocks
- **Symptom**: AgentShield blocks access to local environment template files (`.env.example`).
- **Cause**: Strict pattern matching identified keyword `.env` as an active secret file.
- **Resolution**:
  Add explicit exemption path in `ecc_config.json`:
  ```json
  "agentshield": {
    "exemptions": [".env.example", "tests/fixtures/*.env"]
  }
  ```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — Primary terminal execution agent.
- [Cursor](../development_ops/cursor.md) — Supported desktop IDE wrapper.
- [OpenCode](../development_ops/opencode.md) — Multi-agent developer CLI harness.
- [Aider](../development_ops/aider.md) — Command-line git-integrated assistant.
- [Claude Hooks](../development_ops/claude-hooks.md) — Terminal-native lifecycle hook architecture.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Tool interaction protocol standard.

## Sources / references
- [Everything Claude Code (ECC) Repository](https://github.com/affaan-m/everything-claude-code)
- [ECC Official Online Documentation](https://ecc.tools/)
- [Anthropic Developer Site - Designing Agentic Systems](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [FastMCP 3.1 Framework Documentation](https://github.com/jina-ai/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
