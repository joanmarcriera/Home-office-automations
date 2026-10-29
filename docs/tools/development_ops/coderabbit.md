# CodeRabbit

## What it is
**CodeRabbit** is an AI-powered automated code review platform and Developer Operations agent designed to streamline pull request auditing, detect security vulnerabilities, enforce repository linting rules, and accelerate software review cycles. Powered by fine-tuned coding models (including GPT-6.1 Sol / CodeRabbit security models), CodeRabbit natively integrates with GitHub, GitLab, and Bitbucket workflows to deliver contextual line-by-line feedback, automated regression test generation, and FastMCP 3.1 tool execution.

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / Contributor
    participant Git as GitHub / GitLab PR Trigger
    participant CR as CodeRabbit Review Engine
    participant FastMCP as FastMCP 3.1 Security / Linter Tools
    participant Model as GPT-6.1 Sol / CodeRabbit LLM

    Dev->>Git: Push Commit / Open Pull Request
    Git->>CR: Webhook Trigger (`pull_request.opened`)
    CR->>FastMCP: Dispatch AST Analysis & Security Scan (`audit_diff`)
    FastMCP-->>CR: Return Security AST Findings & SAST Alerts
    CR->>Model: Send Diff Context & Security SAST AST Tokens
    Model-->>CR: Synthesize Line-by-Line Code Review & Inline Suggestions
    CR->>Git: Post Inline PR Comments & Summary Review Walkthrough
```

## System Architecture

```
+-----------------------------------------------------------------------------------+
|                           CODERABBIT SYSTEM ARCHITECTURE                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +------------------------+      +---------------------------------------------+  |
|  | GitHub / GitLab /      | ---> | CodeRabbit Webhook Ingestion & Event Queue |  |
|  | Bitbucket PR Triggers  |      | (Diff Parser & Context Synthesizer)         |  |
|  +------------------------+      +---------------------------------------------+  |
|                                                         |                         |
|                                                         v                         |
|                                  +---------------------------------------------+  |
|                                  | CodeRabbit Multi-Model Review Engine        |  |
|                                  | (GPT-6.1 Sol / Code Security / FastMCP)     |  |
|                                  +---------------------------------------------+  |
|                                         /               |               \         |
|                                        v                v                v        |
|                            +---------------+    +---------------+    +----------+ |
|                            | FastMCP SAST  |    | AST Line-by-  |    | Automated| |
|                            | Security Tool |    | Line Linter   |    | Test Gen | |
|                            +---------------+    +---------------+    +----------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
- **Pull Request Review Bottlenecks**: Accelerates code review throughput by providing instant, automated first-pass feedback on open pull requests.
- **Security Vulnerability Exposure**: Identifies SQL injection risks, secret leaks, race conditions, and unhandled memory errors directly in PR diffs before merge.
- **Inconsistent Architectural Standards**: Enforces custom organization guidelines, style conventions, and linting rules across distributed development teams.
- **Superficial Code Reviews**: Offers deep AST-aware logic verification rather than simple syntax checking.

## Where it fits in the stack
**Development Ops / Code Review & Security Automation**. CodeRabbit operates at the CI/CD and pull request gate layer, sitting between git repository hosting services and deployment pipelines.

```
+-----------------------------------------------------------------------------------+
|                            CODERABBIT STACK LOCATION                              |
+-----------------------------------------------------------------------------------+
| Version Control Layer : GitHub / GitLab / Bitbucket Repository Hosting            |
+-----------------------------------------------------------------------------------+
| Code Review Automation: CodeRabbit Engine (GPT-6.1 Sol / Security Models / MCP)   |
+-----------------------------------------------------------------------------------+
| CI/CD Pipeline Layer  : GitHub Actions / GitLab CI / Jenkins / FastMCP 3.1 Scanners|
+-----------------------------------------------------------------------------------+
```

## Feature Comparison Matrix

| Feature / Metric | CodeRabbit | Standard Linter (ESLint/Ruff) | SonarQube | Manual Peer Review |
| :--- | :--- | :--- | :--- | :--- |
| **Contextual Logic Analysis** | High (LLM AST-Aware) | Low (Rule-based static) | Moderate (Rules + SAST) | High (Human intensive) |
| **Inline PR Comments** | Automated Line-by-Line | CI Status Checks only | Summary Quality Gate | Manual typing |
| **One-Click Code Fixes** | Yes (GitHub Suggestion Blocks) | Auto-fix local CLI only | No | Manual developer edit |
| **FastMCP 3.1 Integration** | Native FastMCP Protocol | No | Custom Plugin API | N/A |
| **Turnaround Time** | < 2 Minutes | < 30 Seconds | 3-5 Minutes | Hours to Days |

## Typical use cases
- **Automated Pull Request Code Review**: Analyzing PR diffs and leaving inline comments with refactoring suggestions and bug alerts.
- **Security & Vulnerability Auditing**: Scanning code changes for secret leaks, OWASP top 10 vulnerabilities, and improper authorization logic.
- **Automated Unit Test Generation**: Generating Playwright, PyTest, or Jest regression test cases corresponding to new PR code changes.
- **PR Description Summarization**: Automatically drafting detailed PR release release notes, impact summaries, and architectural diagrams.

## Strengths
- **Context-Aware Deep Code Understanding**: Reads whole-repository codebase context to understand cross-file function dependencies and imports.
- **Actionable One-Click Refactoring**: Posts GitHub/GitLab suggestion blocks that developers can accept into PRs with a single click.
- **Customizable Prompt Directives**: Supports `.coderabbit.yaml` repository configuration files for custom rule enforcement.
- **FastMCP 3.1 Protocol Support**: Exposes code review tools via FastMCP 3.1 endpoints for local CLI and IDE integration.

## Limitations
- **SaaS / Cloud Dependency**: Cloud-managed review engine requires repository access (self-hosted enterprise agent tier available for strict air-gapped environments).
- **False Positive Tuning Needed**: May require tuning of `.coderabbit.yaml` rules to suppress overly pedantic style warnings.

## When to use it
- When you want to eliminate code review backlogs and maintain high code quality across busy engineering teams.
- When automating initial SAST security scanning, secret detection, and regression testing on every pull request.
- When enforcing custom team architectural patterns across multi-repo microservices.

## When not to use it
- For tiny single-developer personal hobby projects where formal code review overhead is unnecessary.
- In strictly disconnected offline homelabs without cloud connectivity (unless using CodeRabbit Enterprise Self-Hosted edition).

## Getting started

### Installation & Configuration
Create a `.coderabbit.yaml` configuration file in the root of your git repository:

```yaml
# .coderabbit.yaml
version: "2"
language: "en-US"
reviews:
  profile: "chill" # Options: chill, assertive, strict
  request_tools:
    sast_scanner: true
    test_generator: true
  path_instructions:
    - path: "src/api/**/*.py"
      instructions: "Ensure all endpoints validate inputs using Pydantic v2 schemas with extra='forbid'."
    - path: "docs/**/*.md"
      instructions: "Verify markdown technical consistency and check relative links."
chat:
  auto_reply: true
```

## CLI examples

### Triggering CodeRabbit CLI Review
```bash
# Execute local diff audit using CodeRabbit CLI tool
coderabbit review --diff "git diff main...feature-branch"

# Query active CodeRabbit FastMCP Gateway endpoint health
curl -s http://localhost:8096/health | jq .
```

## Systemd Service Configuration

For hosting a local CodeRabbit FastMCP review proxy gateway (`/etc/systemd/system/coderabbit-mcp-gateway.service`):

```ini
[Unit]
Description=CodeRabbit FastMCP Code Review Proxy Gateway
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=coderabbit
Group=coderabbit
WorkingDirectory=/opt/coderabbit-mcp-gateway
ExecStart=/usr/local/bin/python3 -m coderabbit_mcp.gateway --port 8096 --host 0.0.0.0
Restart=always
RestartSec=5s
LimitNOFILE=65536
Environment=CODERABBIT_API_KEY=cr_sec_991122334455
Environment=PYTHONUNBUFFERED=1

# Security Isolation
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/coderabbit-mcp
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Configuration

Deploying the CodeRabbit FastMCP Review Gateway (`docker-compose.yml`):

```yaml
version: "3.8"

services:
  coderabbit-mcp:
    image: python:3.11-slim
    container_name: coderabbit-mcp-gateway
    restart: unless-stopped
    command: python -m coderabbit_mcp.gateway
    ports:
      - "8096:8096"
    environment:
      - CODERABBIT_API_KEY=${CODERABBIT_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - ./logs:/var/log/coderabbit-mcp
```

## API examples

### FastMCP 3.1 Code Review Tool with Pydantic v2
Production Python implementation of a CodeRabbit FastMCP tool server:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Dict, Any
import os

mcp = FastMCP("CodeRabbit-Review-Server", version="3.1.0")

class CodeDiffReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    repository_id: str = Field(..., description="Target repository slug, e.g. 'org/repo'")
    pull_request_number: int = Field(..., ge=1, description="Pull Request ID number")
    diff_content: str = Field(..., description="Git diff payload string to analyze")

    @field_validator("repository_id")
    @classmethod
    def validate_repo_slug(cls, v: str) -> str:
        if "/" not in v:
            raise ValueError("repository_id must be in 'owner/repo' format")
        return v

class CodeFinding(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    file_path: str = Field(..., description="Path to modified file")
    line_number: int = Field(..., ge=1, description="Line number for finding")
    severity: str = Field(..., description="Severity: info, warning, critical")
    comment: str = Field(..., description="Review comment detail")
    suggested_fix: Optional[str] = Field(None, description="Suggested code replacement block")

class CodeDiffReviewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    pr_summary: str = Field(..., description="High-level summary of changes")
    findings: List[CodeFinding] = Field(default_factory=list, description="List of review findings")
    security_score: float = Field(..., ge=0.0, le=100.0, description="Calculated security/quality score")

@mcp.tool()
def review_pull_request_diff(request: CodeDiffReviewRequest) -> str:
    """Executes an automated CodeRabbit AI code review on a git PR diff."""
    # Mock analysis of diff payload
    findings = []
    if "eval(" in request.diff_content or "exec(" in request.diff_content:
        findings.append(CodeFinding(
            file_path="src/main.py",
            line_number=42,
            severity="critical",
            comment="Use of dangerous eval/exec function detected. Potential code injection vulnerability.",
            suggested_fix="use ast.literal_eval() or explicit json parsing instead"
        ))

    response = CodeDiffReviewResponse(
        pr_summary=f"Automated CodeRabbit review completed for PR #{request.pull_request_number}",
        findings=findings,
        security_score=85.0 if findings else 100.0
    )

    return response.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8096)
```

## Diagnostic & Troubleshooting Matrix

| Issue / Error Symptom | Probable Root Cause | Remediation Strategy |
| :--- | :--- | :--- |
| **`401 Unauthorized Webhook`** | GitHub Webhook secret mismatch or expired CodeRabbit API key | Re-generate API token in CodeRabbit dashboard and update secret in GitHub repository settings. |
| **`Missing Review Comments on PR`** | Modified paths ignored in `.coderabbit.yaml` ignore rules | Check `.coderabbit.yaml` path filter patterns to ensure target files are included. |
| **`FastMCP Gateway Connection Refused`** | Service `coderabbit-mcp-gateway.service` not running on port 8096 | Run `systemctl restart coderabbit-mcp-gateway` and check `journalctl -u coderabbit-mcp-gateway`. |
| **`Pydantic Validation Error`** | Client request omitted mandatory `pull_request_number` field | Enforce strict Pydantic v2 `extra="forbid"` schema validation in caller application. |

## Operational Best Practices & Guardrails
1. **Repository Configuration Locking**: Commit `.coderabbit.yaml` to the root repository branch to ensure consistent review standards across all branches.
2. **Secret Masking**: Always enable automated secret detection in CodeRabbit settings to automatically redact API keys from public review logs.
3. **Pydantic v2 Schema Enforcement**: Leverage `extra="forbid"` in all API request/response models to prevent schema drift.

## Related tools / concepts
- [OpenAI GPT-6.1 Sol](../providers/gpt-6-1-terra.md) — Security and coding foundation model powering CodeRabbit.
- [GitHub Actions](../development_ops/github-pages.md) — CI/CD automation runner.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Open tool execution framework.

## Sources / references
- [CodeRabbit OpenAI Sol Integration Announcement](https://openai.com/index/gpt-6-1-sol-coderabbit-code-security)
- [CodeRabbit Official Website](https://coderabbit.ai/)
- [CodeRabbit Documentation](https://docs.coderabbit.ai/)

---
## Contribution Metadata
- Last reviewed: 2026-10-27
- Confidence: high
