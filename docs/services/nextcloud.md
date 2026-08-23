# Nextcloud

## What it is

Nextcloud is a suite of client-server software for creating and using file hosting services. It is the most deployed self-hosted content collaboration platform, providing a safe home for all your data - files, contacts, calendars, and more. In early January 2027, Nextcloud Hub 10 has evolved into an **Agentic Collaboration Platform**, integrating deep AI reasoning and the [MCP 3.1 / FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) for automated productivity.

## What problem it solves

Public cloud services like Google Drive or Microsoft 365 offer great convenience but at the cost of data privacy and ownership. Nextcloud solves this by providing a comprehensive, enterprise-grade collaboration suite that you host on your own hardware, giving you full control over who has access to your data while maintaining the ease of use of a modern cloud platform. It eliminates "data silos" by providing a unified interface for files, communication, and AI-driven task execution.

## Where it fits in the stack

**Category**: Service / Productivity. It serves as the **unified content and collaboration hub**, acting as the primary repository for documents, personal data, and team communication in a home-office or small business environment. It bridges the gap between raw storage and agentic automation.

## Typical use cases

- **File Synchronization**: Keeping documents and photos synced across multiple computers and mobile devices.
- **Collaborative Editing**: Real-time document editing using integrated tools like OnlyOffice or Collabora Online.
- **Personal Information Management (PIM)**: Syncing calendars, contacts, and tasks using open standards like CalDAV and CardDAV.
- **Agentic AI Assistance**: Using the Hub 10 Context Agent to analyze local files, summarize meetings in Talk, and execute tasks via [Gemma 3](../tools/ai_knowledge/local_llms.md), [Claude 5.1](../tools/providers/anthropic.md), or [GPT-5.5](../tools/providers/huggingface.md).
- **Secure File Sharing**: Sharing large files with external parties via password-protected links with optional End-to-End Encryption (E2EE).

## Strengths

- **Extensible**: A vast App Store allows for adding features like Kanban boards, video conferencing (Talk), and music players.
- **AI-Native Reasoning**: Hub 10 features a native Context Agent for executing tasks within Nextcloud using [FastMCP 3.1](../tools/automation_orchestration/mcp.md) for low-latency tool discovery.
- **Open Standards**: Built on PHP and SQL, using WebDAV/CalDAV for maximum compatibility with third-party tools.
- **Privacy-First E2EE**: Support for client-side end-to-end encryption for sensitive folders.
- **Strong Ecosystem**: Massive community support and enterprise-grade security hardening.

## Limitations

- **Resource Intensive**: Requires significant RAM and CPU compared to lightweight single-purpose tools like [Syncthing](syncthing.md).
- **Configuration Overhead**: Proper optimization (Redis caching, background jobs) is necessary for a smooth experience on large libraries.
- **Database Dependency**: Performance is heavily tied to the efficiency of the underlying SQL database and PHP-FPM configuration.

## When to use it

- When you need a comprehensive, self-hosted suite for file storage, collaboration, and productivity.
- For users who want to maintain full control over their data while having access to features similar to Google Workspace or Microsoft 365.
- When you want an extensible platform with a wide range of apps (Talk, Calendar, Contacts, Office) that supports [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md).

## When not to use it

- If you only need simple file synchronization without the extra features (consider [Syncthing](syncthing.md)).
- If you have very limited server resources (e.g., < 2GB RAM for the full stack).

## Getting started

### Docker Deployment
The fastest way to get Nextcloud running is using the official Docker image:

```bash
docker run -d \
  --name nextcloud \
  -p 8080:80 \
  -v nextcloud:/var/www/html \
  nextcloud
```

### SSO & AI Setup
1.  **SSO (Authentik)**: Install the `user_oidc` app and configure it to point to your [Authentik](authentik.md) instance.
2.  **AI Assistant**: Install the **Nextcloud Assistant** and **Context Agent** apps. Configure a provider like [Ollama](ollama.md) (for [Gemma 3](../tools/ai_knowledge/local_llms.md)) or [Claude 5.1](../tools/providers/anthropic.md).
3.  **Office**: Run a Collabora Online container and point the Nextcloud Office app to its URL (e.g., `https://collabora.example.com`).

### Hello World
1. Navigate to `http://localhost:8080` and create an admin account.
2. Upload a text file to your "Documents" folder.
3. If the AI Assistant is enabled, click the "Smart Picker" and ask it to "Summarize the uploaded document."

## CLI examples
Nextcloud includes the `occ` (Nextcloud Command-line Control) tool for server management.

```bash
# List all available occ commands
docker exec --user www-data nextcloud php occ list

# Reset the admin password
docker exec --user www-data nextcloud php occ user:resetpassword admin

# Put the server into maintenance mode
docker exec --user www-data nextcloud php occ maintenance:mode --on

# Register an OpenID Connect provider (Authentik) programmatically
docker exec --user www-data nextcloud php occ user_oidc:provider authentik \
  --client-id="nextcloud-sso" \
  --client-secret="super-secret-sso-key" \
  --discovery-url="https://authentik.example.com/application/o/nextcloud/.well-known/openid-configuration"
```

## API examples

### Direct API via Curl
Nextcloud supports the OCS (Open Collaboration Services) API for remote management.

```bash
# Get user information
curl -u admin:password \
     -H "OCS-APIRequest: true" \
     -X GET "http://localhost:8080/ocs/v1.php/cloud/users/admin"
```

### Python (Create a Secure File Share with Pydantic v2 Validation)
The following script utilizes **Pydantic v2** to validate inputs and structures before invoking the Nextcloud OCS API to generate secure shareable links, ensuring compliance with strict data policies when driven by Claude 5.1, GPT-5.5, or Gemini 4.0.

```python
import requests
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class NextcloudShareRequest(BaseModel):
    path: str = Field(..., description="The path of the file or folder to share")
    shareType: int = Field(default=3, description="3 = Public Link, 0 = User, 1 = Group")
    permissions: int = Field(default=1, description="1 = Read Only, 15 = Read/Write/Update/Delete/Share")
    password: Optional[str] = Field(None, min_length=8, description="Optional password for public link")

class NextcloudShareResponse(BaseModel):
    id: str = Field(..., description="The share ID")
    url: str = Field(..., description="The public URL of the share")
    token: Optional[str] = Field(None, description="The share token")

def create_public_share(base_url: str, auth: tuple, share_data: NextcloudShareRequest) -> NextcloudShareResponse:
    url = f"{base_url}/ocs/v1.php/apps/files_sharing/api/v1/shares"
    headers = {
        "OCS-APIRequest": "true"
    }

    # Nextcloud OCS returns XML by default unless JSON is requested.
    # We append ?format=json to the URL.
    json_url = f"{url}?format=json"
    response = requests.post(json_url, auth=auth, headers=headers, data=share_data.model_dump())
    response.raise_for_status()

    payload = response.json()
    element = payload.get("ocs", {}).get("data", {})

    return NextcloudShareResponse(
        id=str(element.get("id")),
        url=element.get("url"),
        token=element.get("token")
    )

# Example usage:
# share_config = NextcloudShareRequest(path="/Documents/Report.pdf", password="SecurePassword123")
# share_res = create_public_share("http://localhost:8080", ("admin", "password"), share_config)
# print(share_res.url)
```

### List files via WebDAV
```bash
curl -u admin:password \
     -X PROPFIND "http://localhost:8080/remote.php/dav/files/admin/"
```

## Related tools / concepts

- [Syncthing](syncthing.md) — for a lighter, peer-to-peer file sync alternative.
- [Authentik](authentik.md) — for managing Nextcloud SSO/OIDC authentication.
- [Tailscale](tailscale.md) — for secure remote access to your Nextcloud instance.
- [Paperless-ngx](paperless-ngx.md) — can be integrated with Nextcloud for document archival.
- [Ollama](ollama.md) — for hosting [Gemma 3](../tools/ai_knowledge/local_llms.md) or other local LLMs for the Nextcloud Assistant.
- [n8n](n8n.md) — for automating file processing and notification workflows.
- [Rclone Automation](rclone-automation.md) — for backing up Nextcloud data to off-site cloud storage.
- [Docker](../tools/infrastructure/docker.md) — the recommended deployment method.
- [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md) — the protocol used for agentic tool integration.

## Sources / References

- [Official Nextcloud Website](https://nextcloud.com/)
- [Nextcloud Admin Documentation](https://docs.nextcloud.com/server/latest/admin_manual/)
- [Nextcloud Hub 10 AI Overview](https://nextcloud.com/blog/nextcloud-hub-10-ai-context-agent/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [Collabora Online for Nextcloud](https://www.collaboraoffice.com/collabora-online-for-nextcloud/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
