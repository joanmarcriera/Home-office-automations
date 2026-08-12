# Everything Claude Code (ECC)

## What it is
Everything Claude Code (ECC) is an advanced, production-grade performance optimization ecosystem and suite of extensions built specifically for terminal-native AI harnesses, primarily [Claude Code](../development_ops/claude-code.md). It is not just a collection of static files but an active, integrated runtime of specialized subagents, lifecycle hooks, and contextual rules designed to maximize reasoning fidelity.

## What problem it solves
It bridges the critical gap between a raw AI terminal CLI and a fully functional, autonomous software engineering environment. ECC addresses agent context-window saturation, security vulnerability exposures, memory state persistence across development sessions, and domain-specific coding standard compliance. It is tuned to optimize token efficiency for frontier reasoning models like Claude 5.1 using FastMCP 3.1.

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
- **SOTA Alignment**: Native support for Claude 5.1 planning models, optimizing `MAX_THINKING_TOKENS` configuration metrics.
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

## API examples
ECC configurations and custom post-edit hooks are structured programmatically using Python and strict **Pydantic v2** validation to model ECC configuration environments.

### 1. Validating ECC Agent Configuration (Python)
ECC configurations are verified and mapped to local development environments using strict schemas.

```python
from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional

class SecurityPolicy(BaseModel):
    block_env_secrets: bool = True
    scan_exclude: List[str] = Field(default_factory=lambda: ["*.log", "node_modules/"])

class RoutingConfig(BaseModel):
    security_audit: str = "ecc:agentshield"
    lint_fix: str = "ecc:typescript-reviewer"
    architecture_review: str = "ecc:architect"

class ECCConfig(BaseModel):
    """
    Validates ECC runtime configuration under strict Pydantic v2.
    """
    routing: RoutingConfig
    security: SecurityPolicy
    max_thinking_tokens: int = Field(default=4000, gt=0, le=16000)
    mcp_version: str = Field(default="3.1")

    @field_validator("mcp_version")
    @classmethod
    def validate_mcp_version(cls, val: str) -> str:
        if val not in ["3.1", "3.0"]:
            raise ValueError("Only MCP versions 3.0 and 3.1 are supported.")
        return val

# Verify active configurations
sample_config = {
    "routing": {
        "security_audit": "ecc:agentshield",
        "lint_fix": "ecc:typescript-reviewer",
        "architecture_review": "ecc:architect"
    },
    "security": {
        "block_env_secrets": True,
        "scan_exclude": ["*.log", "node_modules/", "*.key"]
    },
    "max_thinking_tokens": 8000,
    "mcp_version": "3.1"
}

validated_ecc = ECCConfig.model_validate(sample_config)
print(f"ECC Configuration validated. Active MCP Standard: {validated_ecc.mcp_version}")
print(validated_ecc.model_dump_json(indent=2))
```

### 2. Custom Post-Edit Automation Hook (Node.js)
```javascript
// .claude/hooks/post-edit.js
const { execSync } = require('child_process');

module.exports = async ({ file, content }) => {
  if (file.endsWith('.py')) {
    try {
      console.log(`ECC Hook: Formatting ${file} with Ruff...`);
      execSync(`ruff format ${file}`);
    } catch (error) {
      console.error(`ECC Hook Error: ${error.message}`);
    }
  }
};
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — The primary terminal execution agent.
- [Cursor](../development_ops/cursor.md) — Supported desktop IDE wrapper.
- [OpenCode](../development_ops/opencode.md) — Multi-agent developer CLI harness.
- [Aider](../development_ops/aider.md) — Command-line git-integrated assistant.
- [last30days-skill](last30days-skill.md) — Social research extension.
- [Claude Hooks](../development_ops/claude-hooks.md) — Terminal-native lifecycle hook architecture.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Tool interaction protocol standard.
- [Claude How-To](claude-howto.md) — Curriculum for Anthropic terminal tools.

## Sources / references
- [Everything Claude Code (ECC) Repository](https://github.com/affaan-m/everything-claude-code)
- [ECC Official Online Documentation](https://ecc.tools/)
- [Anthropic Developer Site - Designing Agentic Systems](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [AgentShield Project Release Notes](https://ecc.tools/blog/agentshield-v2)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
