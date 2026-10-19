# Gitea

## What it is
Gitea is a community-managed lightweight code hosting solution written in Go. It provides a complete Git service including repository management, issue tracking, code review, and CI/CD integration, with a focus on simplicity and high performance. It is a painless self-hosted Git service that serves as the backbone for private DevOps ecosystems in the early January 2027 era, featuring native support for [FastMCP 3.1 / MCP](../tools/automation_orchestration/mcp.md) for agentic integration.

## What problem it solves
It allows developers and home lab enthusiasts to host their own private Git repositories without the resource overhead of GitLab or the privacy concerns of public cloud providers like GitHub.

In early January 2027, it specifically addresses the need for local, air-gapped code storage for proprietary AI training datasets and sensitive automation scripts that utilize [Gemma 3](../tools/ai_knowledge/local_llms.md), [Qwen 3.6](../tools/ai_knowledge/local_llms.md), [GPT-5.6](../tools/providers/index.md), and [Claude 5.6](../tools/providers/anthropic.md). It provides a central hub for code collaboration, issue tracking, and multi-agent automation that can run on low-power hardware.

## Webhook & Event Architecture Flow

```
                                +-----------------------------------+
                                | Developer Push / Pull Request     |
                                +-----------------+-----------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                | Gitea Instance (v1.27+)           |
                                | - Repositories & Internal Git     |
                                | - Webhook Dispatch Engine         |
                                +--------+-----------------+--------+
                                         |                 |
                        Webhook Payload  |                 | FastMCP 3.1 JSON-RPC
                                         v                 v
+------------------+           +------------------+    +-----------------------+
| Authentik SSO    | <-------> | n8n Automation   |    | Autonomous AI Agents  |
| (OIDC Identity)  |           | Webhook Listener |    | (Claude 5.6 / Jules)  |
+------------------+           +------------------+    +-----------------------+
```

## Where it fits in the stack
Gitea sits in the **Development & DevOps** layer. It serves as the primary source of truth for code, configuration files, and automation workflows. It is the central registry for local GitOps, often triggering pipelines that deploy services across the entire homelab stack. It integrates with the [FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) to allow AI agents to manage repositories, issues, and pull requests autonomously.

## Code Hosting Platform Comparison

| Feature / Dimension | Gitea (v1.27+) | Forgejo | GitHub (SaaS) | GitLab Community Edition |
| :--- | :--- | :--- | :--- | :--- |
| **Footprint / Memory** | Low (~100 MB RAM) | Low (~100 MB RAM) | Cloud-Hosted | High (4 GB+ RAM) |
| **CI/CD Integration** | Gitea Actions (act_runner) | Forgejo Actions | GitHub Actions | GitLab Runners |
| **FastMCP 3.1 Support** | Native API / Webhooks | Native API / Webhooks | Via API Gateways | Via API Gateways |
| **Database Backend** | SQLite / Postgres / MariaDB | SQLite / Postgres | Proprietary DB | PostgreSQL |
| **SSO / OIDC** | Native OIDC / LDAP | Native OIDC / LDAP | SAML / SSO (Enterprise) | Native OIDC / LDAP |

## Diagnostic Troubleshooting Matrix

| Issue Symptom | Root Cause | Diagnostic Check Command | Resolution Path |
| :--- | :--- | :--- | :--- |
| **HTTP 500 Database Locked** | SQLite concurrent write lock during heavy CI/CD | `grep "database is locked" /data/gitea/log/gitea.log` | Migrate SQLite backend to PostgreSQL 16+ or enable WAL mode in `app.ini`. |
| **Gitea Actions Runner Offline**| Secret registration token mismatch or network error | `docker logs act_runner` | Re-register the runner using `act_runner register` with a fresh admin token. |
| **SSH Permission Denied** | Port collision with host SSH or missing SSH key | `ssh -T -p 222 git@localhost` | Remap Gitea SSH port to `2222` and verify public keys in Gitea user settings. |
| **OIDC Redirect Loop** | Mismatched redirect URI in Authentik configuration | Inspect browser network headers on OAuth callback | Align `REDIRECT_URL` in `app.ini` with Authentik OAuth application settings. |
| **LFS Push Rejection** | Exceeded local disk storage or bad authorization | `git lfs push origin main --verbose` | Verify `[lfs]` endpoint settings in `app.ini` or switch LFS backend to MinIO S3 bucket. |

## Typical use cases
- **Private Code Hosting**: Maintaining internal tools and projects away from public eyes.
- **GitOps**: Storing infrastructure-as-code (Ansible, Terraform, K3s manifests) and triggering deployments.
- **AI Dataset Management**: Hosting versioned datasets for fine-tuning local models like [Gemma 3](../tools/ai_knowledge/local_llms.md) and Qwen 3.6.
- **Local CI/CD**: Running Gitea Actions for automated testing and deployment.
- **Documentation**: Hosting project documentation via Gitea's built-in wiki or Markdown support.
- **Mirrors**: Maintaining local mirrors of critical public repositories for offline access.
- **SSO Integration**: Using OIDC for centralized authentication via [Authentik](authentik.md).

## Strengths
- **Performance**: Extremely lightweight and fast; runs comfortably on a Raspberry Pi 5 or low-power NAS.
- **GitHub-Like UX**: Familiar interface that requires minimal learning for existing Git users.
- **Built-in CI/CD**: Gitea Actions provides high compatibility with GitHub Actions workflows, including concurrency support and reusable workflows from private repositories.
- **v1.27+ Features**: Keyboard shortcuts (e.g., `s` for search), subpath archives, Vite-based front-end toolchain, Terraform registry/state backend support, and automatic release notes generation.
- **Self-Contained**: Can be run as a single binary or a small Docker container with minimal dependencies.
- **Enterprise Ready**: Supports OIDC, LDAP, and advanced repository mirroring.

## Limitations
- **Ecosystem**: Smaller plugin and integration ecosystem compared to GitHub or GitLab.
- **Scaling**: Lacks the massive horizontal scaling capabilities (like GitLab Geo) for multi-region global teams.
- **Native AI Features**: While it supports local LLM integration via Actions, it lacks the deeply integrated, first-party AI coding assistants found in GitHub (Copilot).

## When to use it
- When you want a lightweight, self-hosted alternative to GitHub or GitLab.
- For managing GitOps workflows on home lab infrastructure with low resource overhead.
- To maintain private copies of code and configuration without cloud dependencies.
- When running Git services on edge devices or low-resource hardware like a NAS.

## When not to use it
- If you require advanced enterprise features like geo-replication or deep compliance auditing found in GitLab.
- When you need the massive social ecosystem and public visibility of GitHub.
- If your team relies heavily on proprietary third-party integrations that only support GitHub/GitLab APIs specifically.

## Getting started

### Docker Compose
To run Gitea using Docker Compose:

```yaml
services:
  server:
    image: gitea/gitea:1.27.0
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "222:22"
```

### SSO & OIDC Integration (Authentik)
1. Navigate to **Site Administration > Authentication Sources > Add Authentication Source**.
2. Set **Authentication Type** to `OpenID Connect`.
3. Configure the following:
    - **Authentication Name**: `authentik`
    - **OAuth2 Provider**: `OpenID Connect`
    - **Client ID (Key)**: `<Your Client ID>`
    - **Client Secret**: `<Your Client Secret>`
    - **OpenID Connect Auto Discovery URL**: `https://authentik.example.com/application/o/gitea/.well-known/openid-configuration`
    - **Additional Scopes**: `email profile`

### Enabling Gitea Actions
1. In your `app.ini`, ensure Actions are enabled:
```ini
[actions]
ENABLED = true
```
2. **Set up a Runner**: Gitea Actions requires a separate "Gitea Runner" (formerly `act_runner`).
3. **Registration**: Registration tokens are managed via the administrative UI or CLI.

## Systemd Service Unit Configuration

To run Gitea as a native binary system service on Linux hosts, create `/etc/systemd/system/gitea.service`:

```ini
[Unit]
Description=Gitea (Painless Self-Hosted Git Service)
After=syslog.target
After=network.target
After=postgresql.service

[Service]
RestartSec=2s
Type=simple
User=git
Group=git
WorkingDirectory=/var/lib/gitea/
ExecStart=/usr/local/bin/gitea web --config /etc/gitea/app.ini
Restart=always
Environment=USER=git HOME=/home/git GITEA_WORK_DIR=/var/lib/gitea
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

Enable and start the Gitea service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gitea.service
sudo systemctl status gitea.service
```

## Disaster Recovery & Operational Best Practices
- **Automated Dumps**: Schedule nightly `gitea dump` commands via cron or n8n, saving archives (`gitea-dump-*.zip`) to offsite storage or encrypted S3 targets.
- **Database Backends**: For environments hosting >50 repositories or heavy Gitea Actions workflows, migrate from SQLite to PostgreSQL 16+ to handle concurrent locking smoothly.
- **Git LFS Offloading**: Enable S3-compatible object storage offloading in `app.ini` for Large File Storage (LFS) to keep the primary container storage lightweight.
- **SSH Port Remapping**: Avoid port conflicts with host SSH services by remapping Gitea's SSH listener to port `2222` or `222`.

## CLI examples
The `gitea` binary inside the container can be used for administrative tasks:

```bash
# Create an admin user
docker exec -u 1000 -it gitea gitea admin user create --username admin --password secret --email admin@example.com --admin

# Dump database and configuration for backup
docker exec -u 1000 -it gitea gitea dump

# List all repositories on the instance
docker exec -u 1000 -it gitea gitea admin repo list

# Check server health via HTTP API
curl -s http://localhost:3000/api/v1/version
```

## API examples

### Programmatic Webhook & Issue Validation with FastMCP 3.1 (Python & Pydantic v2)
Defining and validating Gitea webhook and issue payloads using modern FastMCP 3.1 and Pydantic v2 syntax.

```python
import os
import requests
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server for Gitea Management
mcp = FastMCP("Gitea-Agentic-Server", version="3.1.0")

class GiteaIssueCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=3, max_length=200, description="Title of the issue.")
    body: str = Field(..., min_length=5, description="Markdown body content of the issue.")
    assignees: List[str] = Field(default_factory=list, description="Gitea usernames assigned to the issue.")
    labels: List[int] = Field(default_factory=list, description="List of label IDs to attach.")

class GiteaWebhookPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    webhook_id: int = Field(..., alias="id", description="Unique identifier of the webhook", ge=1)
    type: str = Field(..., description="Webhook payload format type (e.g. gitea, slack)")
    active: bool = Field(default=True, description="Whether the webhook is enabled")
    config: Dict[str, Any] = Field(..., description="Configuration parameters mapping")

    @field_validator("config")
    @classmethod
    def validate_payload_url(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if "url" not in v:
            raise ValueError("Webhook config dictionary must contain a target payload URL")
        return v

@mcp.tool()
def create_gitea_issue(owner: str, repo: str, payload: Dict[str, Any]) -> str:
    """Create a new issue on a Gitea repository via FastMCP 3.1."""
    try:
        validated = GiteaIssueCreatePayload.model_validate(payload)
        gitea_url = os.getenv("GITEA_URL", "http://localhost:3000")
        token = os.getenv("GITEA_TOKEN", "mock_token")

        headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
        response = requests.post(
            f"{gitea_url}/api/v1/repos/{owner}/{repo}/issues",
            json=validated.model_dump(),
            headers=headers,
            timeout=10
        )
        if response.status_code in (200, 201):
            return f"Issue successfully created in {owner}/{repo}: {validated.title}"
        return f"Gitea API returned HTTP {response.status_code}: {response.text}"
    except Exception as err:
        return f"Failed to create Gitea issue: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

### Automated Code Review Pattern (Ollama Integration)
Trigger a local LLM to review a pull request diff programmatically.

```python
# Simulated automated PR reviewer
import json
import urllib.request

def run_local_pr_review():
    code_diff = "diff --git a/main.py b/main.py\n+print('Hello, January 2027!')"
    payload = {
        "model": "qwen36",
        "prompt": f"Review this Git diff and suggest improvements:\n\n{code_diff}",
        "stream": False
    }

    req = urllib.request.Request(
        "http://ollama-server:11434/api/generate",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print("Local LLM Review:\n", res_data.get("response"))
    except Exception as e:
        print("Review API offline:", e)

if __name__ == "__main__":
    run_local_pr_review()
```

## Related tools / concepts
- [Authentik](authentik.md) — For centralized SSO and user management.
- [Docker](../tools/infrastructure/docker.md) — For containerized Gitea deployments.
- [Syncthing](syncthing.md) — For syncing documentation and larger LLM fine-tuning binary datasets.
- [n8n](n8n.md) — For orchestrating workflows triggered by Gitea webhooks.
- [Vikunja](vikunja.md) — For project management integrated with Gitea issues.
- [Paperless-ngx](paperless-ngx.md) — For archiving documentation generated from Git repositories.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for integrating Gitea into AI agent workflows.
- [Changedetection.io](changedetection.md) — For monitoring repository status and web release updates.

## Sources / references
- [Official Website](https://gitea.com/)
- [GitHub Repository](https://github.com/go-gitea/gitea)
- [Gitea Documentation](https://docs.gitea.com/)
- [Gitea 1.27.0 Release Notes](https://blog.gitea.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
