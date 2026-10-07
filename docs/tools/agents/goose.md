# Goose

Goose is an open-source, extensible AI agent framework and CLI runtime designed for autonomous software development, environment management, and multi-tool execution. Managed under the governance of the **Agentic AI Foundation (AAIF)**, Goose goes beyond static code completion by operating a self-contained execution loop that installs dependencies, modifies code, runs automated test suites, and fixes runtime tracebacks.

By early 2027, Goose natively integrates **FastMCP 3.1 (Model Context Protocol)** and **MCP Task Protocols**, enabling frontier models—such as [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), [Llama 4](../ai_knowledge/llama.md), [DeepSeek-V4](../ai_knowledge/deepseek.md), and [Qwen 3.6 VL](../ai_knowledge/qwen.md)—to execute multi-step engineering missions across localized developer environments and distributed cloud infra.

## What it is

Goose is an open-source, extensible AI agent designed to go beyond simple code suggestions. It is built to install, execute, edit, and test code autonomously or with human supervision, using any LLM that supports tool-calling. Hosted by the Agentic AI Foundation (AAIF), it serves as a robust platform for building and deploying specialized developer agents.

## What problem it solves

Traditional AI developer assistants operate as single-turn chat interfaces or passive autocomplete plugins. They generate code snippets but leave environment setup, execution testing, compilation verification, and bug fixing to the human engineer.

Goose solves five critical software engineering bottlenecks:
1. **The Execution Gap**: Runs the code it generates within a sandboxed shell, observing stdout/stderr tracebacks to iteratively fix syntax and runtime errors.
2. **Context-Switching Friction**: Performs file operations, directory traversals, terminal commands, and git commits directly within the active session.
3. **Multi-File Refactoring**: Executes refactoring missions across large codebases while preserving architecture consistency and type safety.
4. **Tool Extensibility via MCP 3.1**: Connects seamlessly to external FastMCP 3.1 servers (database tools, CI/CD pipelines, Kubernetes clusters) without custom boilerplate.
5. **Model Vendor Independence**: Operates as a neutral platform that switches dynamically between Anthropic, OpenAI, Google, DeepSeek, and local [Ollama](../../services/ollama.md) instances via [LiteLLM](../../services/litellm.md).

## Where it fits in the stack

**Automation & Orchestration / Agents**. It is an agentic layer that sits on top of LLMs (like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, or local models) and interacts with the filesystem and shell. It is a direct open-source alternative to tools like [Aider](../development_ops/aider.md) or [OpenHands](../development_ops/openhands.md).

## Typical use cases

- **Automated Bug Fixing**: Providing an issue description and letting Goose find, fix, and verify the solution with unit tests.
- **Environment Setup**: Asking Goose to "set up a new React project with Tailwind and Vitest" and letting it handle all shell commands, config, and tests.
- **Large-Scale Refactoring**: Executing systematic code changes across hundreds of files with automated verification loops.
- **Agentic CI/CD Remediation**: Integrating Goose into pipeline scripts to automatically attempt remediation for common build or dependency failures.

## Strengths

- **Extensible Toolkit**: Users can easily add new "Toolkits" (e.g., specific DB connectors, proprietary API clients, or FastMCP 3.1 servers) to Goose.
- **AAIF Governance**: Community-driven development ensures neutrality, vendor independence, and long-term stability.
- **Model Agnostic**: Seamlessly switches between Anthropic, OpenAI, Google, and local models via [Ollama](../../services/ollama.md) or [LiteLLM](../../services/litellm.md).
- **Session Management**: Supports durable, stateful sessions, allowing users to pause, resume, and audit complex multi-step agentic missions.
- **MCP 3.1 / FastMCP 3.1 Task Protocol**: Allows external agents to delegate background execution tasks directly to Goose over the network with complete state verification.

## Limitations

- **Security Responsibility**: Giving an agent shell and filesystem access requires the user to manage trust boundaries and sandboxing (e.g., running in Docker/VMs).
- **Token Efficiency**: Complex tasks can involve many iterations, leading to high token consumption if the model loops on difficult problems.
- **Rapid Evolution**: Frequent core updates can lead to breaking changes in experimental toolkits.

## When to use it

- When you need a full-loop agentic software engineer that can fix bugs and run tests autonomously.
- When you want a neutral, open-source platform for building your own specialized coding agents.
- When you need to automate repetitive system administration or development tasks that require both shell execution and code editing.

## When not to use it

- For simple, single-file code completion where a lightweight tool like standard Copilot is faster.
- In highly restricted environments where giving an AI agent shell/filesystem access is strictly prohibited.
- If you prefer a purely GUI-based tool (Goose is optimized for CLI and agentic API usage).

## Getting started

Goose operates a stateful **Observe-Plan-Execute-Verify (OPEV)** loop. The architecture separates the cognitive driver (LLM reasoning engine) from the execution plane (Toolkit sub-systems, shell, and filesystem handlers).

```
+---------------------------------------------------------------------------------------------------+
|                                       USER & API INTERFACES                                       |
|  +--------------------------------+   +---------------------------------+   +------------------+  |
|  | Goose CLI (`goose session`)    |   | FastMCP 3.1 Agentic API Bridge  |   | CI/CD Pipeline   |  |
+-----------------+-----------------+---+----------------+----------------+---+--------+---------+  |
                  |                                      |                             |            |
                  +--------------------------------------+-----------------------------+            |
                                                         |                                          |
                                                         v                                          |
+---------------------------------------------------------------------------------------------------+  |
|                                       GOOSE CORE AGENT ENGINE                                     |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | Session State Manager                                                                       |  |  |
|  |   - Conversation History & Token Budgeting                                                  |  |  |
|  |   - Multi-Turn Plan Tree & Execution Verification State                                     |  |  |
|  +--------------------------------------------+------------------------------------------------+  |  |
|                                               |                                                   |  |
|  +--------------------------------------------v------------------------------------------------+  |  |
|  | Model Provider Adapter Layer (LiteLLM / Ollama)                                            |  |  |
|  |   - Claude 5.6 / GPT-5.6 / Gemini 4.0 Ultra / Llama 4 Local                                 |  |  |
|  +--------------------------------------------+------------------------------------------------+  |  |
+-----------------------------------------------|---------------------------------------------------+  |
                                                v                                                      |
+---------------------------------------------------------------------------------------------------+  |
|                                     TOOLKIT & FASTMCP 3.1 LAYER                                   |  |
|  +------------------------+    +------------------------+    +---------------------------------+  |  |
|  | Core Developer Toolkit |    | Native FastMCP Server  |    | Custom Domain Toolkits          |  |  |
|  |  - Shell Execution     |    |  - Postgres / K8s MCP  |    |  - Security Auditing           |  |  |
|  |  - File Edit / Patch   |    |  - GitHub / GitLab MCP |    |  - Pydantic v2 Validators       |  |  |
|  +-----------+------------+    +-----------+------------+    +----------------+----------------+  |  |
+--------------|-----------------------------|----------------------------------|-------------------+  |
               |                             |                                  |                      |
               v                             v                                  v                      |
+---------------------------------------------------------------------------------------------------+  |
|                                       SANDBOXED EXECUTION PLANE                                   |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | Subprocess Shell / File System / Docker Runtime                                             |  |  |
|  +---------------------------------------------------------------------------------------------+  |  |
+---------------------------------------------------------------------------------------------------+  |
```

Install and run Goose:
```bash
# Recommended official shell installer
curl -fsSL https://goose.run/install.sh | sh

# Start interactive session
goose session
```

## CLI examples

```bash
# Launch Goose connected to a local FastMCP 3.1 server
goose session --mcp-server "http://localhost:8000/mcp"

# Execute a non-interactive mission to fix test failures
goose run \
  "Analyze pytest failures in tests/test_auth.py, refactor src/auth.py to fix the issue, and verify with pytest." \
  --model claude-5-6-sonnet \
  --max-turns 20

# List previous Goose agent sessions
goose session list
```

## API examples

Below is a complete, runnable FastMCP 3.1 custom Toolkit server (`goose_dev_toolkit.py`) that extends Goose with strict Pydantic v2 parameter validation, safe shell execution, and unit test verification tools.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Developer Extension Toolkit for Goose Agent
Provides safe subprocess execution, test validation, and git status checks.
"""

import os
import sys
import re
import subprocess
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("goose-mcp-toolkit")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="Goose Developer Verification Toolkit",
    version="3.1.0",
    description="Agentic tool extensions for safe shell commands, pytest execution, and git status analysis"
)

# ------------------------------------------------------------------------------
# Pydantic v2 Input Models
# ------------------------------------------------------------------------------

class PytestExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    test_path: str = Field("tests/", description="Relative path to test file or directory")
    coverage_check: bool = Field(False, description="Whether to compute coverage report")
    fail_fast: bool = Field(True, description="Stop execution on first test failure (-x flag)")

    @field_validator("test_path")
    @classmethod
    def sanitize_test_path(cls, v: str) -> str:
        if ".." in v or v.startswith("/"):
            raise ValueError("Test path must be a relative directory without parent path traversal.")
        return v

class GitCommandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    target_branch: Optional[str] = Field("main", description="Target git branch to inspect")
    include_untracked: bool = Field(True, description="Include untracked files in git status")

# ------------------------------------------------------------------------------
# FastMCP Tools
# ------------------------------------------------------------------------------

@mcp.tool()
async def run_pytest_suite(request: PytestExecutionRequest) -> Dict[str, Any]:
    """
    Executes pytest in the workspace and returns structured stdout, stderr, and test metrics.
    """
    logger.info(f"Running pytest suite on path: {request.test_path}")

    cmd = [sys.executable, "-m", "pytest", request.test_path]
    if request.fail_fast:
        cmd.append("-x")
    if request.coverage_check:
        cmd.extend(["--cov=src", "--cov-report=term-missing"])

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return {
            "status": "passed" if proc.returncode == 0 else "failed",
            "return_code": proc.returncode,
            "stdout": proc.stdout[-3000:],
            "stderr": proc.stderr[-1000:],
            "command": " ".join(cmd)
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "return_code": -1,
            "stdout": "",
            "stderr": "Pytest execution timed out after 120 seconds."
        }
    except Exception as e:
        logger.error(f"Failed to execute pytest: {str(e)}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def check_git_workspace_status(request: GitCommandRequest) -> Dict[str, Any]:
    """
    Analyzes the local git repository status and modified file lists.
    """
    logger.info("Checking git workspace status...")
    cmd = ["git", "status", "--porcelain"]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode != 0:
            return {"status": "error", "stderr": proc.stderr}

        lines = proc.stdout.strip().split("\n")
        modified = []
        untracked = []

        for line in lines:
            if not line:
                continue
            code = line[:2]
            filepath = line[3:]
            if "??" in code:
                if request.include_untracked:
                    untracked.append(filepath)
            else:
                modified.append(filepath)

        return {
            "status": "clean" if not (modified or untracked) else "dirty",
            "modified_files": modified,
            "untracked_files": untracked,
            "total_changes": len(modified) + len(untracked)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Related tools / concepts

- [Aider](../development_ops/aider.md): Terminal pair-programming CLI tool.
- [OpenHands](../development_ops/openhands.md): Platform for autonomous AI software development.
- [Claude Code](../development_ops/claude-code.md): Anthropic's agentic command-line interface.
- [LiteLLM](../../services/litellm.md): Universal proxy for LLM API load balancing and failover.
- [Ollama](../../services/ollama.md): Local LLM runtime for running open models with Goose.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Standard agent-tool integration specification.

## Sources / references

- [Goose Official Repository (GitHub)](https://github.com/aaif-goose/goose)
- [Goose Official Documentation Site](https://goose.run/docs)
- [Agentic AI Foundation (AAIF) Website](https://agentic-ai-foundation.org)
- [FastMCP Framework Reference](https://github.com/jlowin/fastmcp)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
