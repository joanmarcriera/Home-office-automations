# Omni Tools

Omni Tools is a self-hosted collection of powerful web-based utilities for everyday developer and office productivity tasks. As of early **January 2027**, it remains a top-tier choice for client-side data transformations, complementing [IT-Tools](it-tools.md) with enhanced media processing capabilities, client-side WebAssembly (WASM) execution, and native **FastMCP 3.1** / **MCP 3.1** discovery for local AI tool invocation.

```
+-----------------------------------------------------------------------------------+
|                        Omni Tools Local Security Architecture                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ User Browser / Local Client Agent / FastMCP 3.1 Client ]                      |
|                                     |                                             |
|                                     v                                             |
|  +-----------------------------------------------------------------------------+  |
|  | Reverse Proxy / Auth Layer (Authentik / Nginx / Caddy)                    |  |
|  +-----------------------------------------------------------------------------+  |
|                                     |                                             |
|                                     v                                             |
|  +-----------------------------------------------------------------------------+  |
|  | Omni Tools Static Web Container (Lightweight Nginx / Caddy Static Host)     |  |
|  |                                                                             |  |
|  |  +---------------------------+       +------------------------------------+  |  |
|  |  | Text & JSON Tools         |       | Client-Side WASM Media Engine      |  |  |
|  |  | (Formatting / Regex / JWT)|       | (FFmpeg WASM / PDF-Lib / Canvas)   |  |  |
|  |  +---------------------------+       +------------------------------------+  |  |
|  |                \                                   /                        |  |
|  |                 v                                 v                         |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | 100% Client-Side In-Browser Memory Processing (Zero Data Exfiltration)|  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|                                     |                                             |
|                                     v                                             |
|  [ Local Browser DOM / File System Access API / FastMCP Local Bridge ]            |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What it is
Omni Tools is a privacy-oriented, client-side browser toolbox for common data transformations such as JSON/YAML formatting, image conversion, PDF manipulation, hash generation, text sanitization, and date/time calculation. The application is distributed as a lightweight, static web container where all transformation workloads happen inside the user's browser runtime using client-side JavaScript and WebAssembly (WASM) rather than sending sensitive data to server-side queues.

## What problem it solves
It replaces the unsafe habit of pasting sensitive corporate configurations, API tokens, JWTs, customer data snippets, or private PDF documents into untrusted third-party online utility websites. For a home office or enterprise network, it keeps all micro-conversion jobs within the local area network (LAN) while providing non-technical team members with a clean, responsive web user interface.

In enterprise IT and security operations, auditing SaaS utility tool usage is a major compliance bottleneck. Omni Tools addresses this by offering a completely self-contained deployment model where no telemetry or input payloads leave the corporate network perimeter.

## Where it fits in the stack
Omni Tools belongs in the **Self-Hosted Productivity & Developer Utilities** layer, operating alongside tools like [IT-Tools](it-tools.md), CyberChef, and Stirling PDF. It is typically deployed behind a private reverse proxy (Caddy, Traefik, Nginx Proxy Manager) and secured with SSO authentication (Authentik, Authelia) for fast access across team devices.

## Typical use cases
- **Data Formatting & Validation**: Formatting, validating, or minifying JSON, XML, YAML, CSV, and SQL query snippets.
- **Client-Side Media Processing**: Converting PNG/JPG images to WebP, cropping images, merging/splitting PDFs, and trimming video clips without uploading files to remote servers.
- **Security & Developer Helpers**: Generating SHA-256 hashes, UUIDs, QR codes, secure passwords, decoding JWT tokens, and calculating cron schedules.
- **Agentic Utility Bridge**: Exposing transformation tools to local AI agents (e.g., [Gemma 3](../tools/ai_knowledge/local_llms.md), **Claude 5.6**, **GPT-5.6**) via FastMCP 3.1 endpoints.
- **Offline Emergency Utilities**: Operating as a self-contained offline developer toolbox on laptops during field operations or network partitions.
- **Network Diagnostic Assistance**: Calculating CIDR subnet ranges, parsing DNS records, and analyzing HTTP header strings.
- **Local Microservice Configuration**: Quickly generating environment variable templates and Docker Compose fragments for local homelab testing.

## Strengths
- **Low-Friction Deployment**: Single lightweight Docker container (< 25MB image size) serving static assets.
- **Zero-Trust Privacy Architecture**: Data stays in browser memory; no risk of server-side data leakage or third-party tracking.
- **Broad Utility Arsenal**: Covers dozens of daily developer, DevOps, and administrative tasks under a single unified web UI.
- **Offline & LAN Capable**: Functions seamlessly in air-gapped environments or during internet outages.
- **FastMCP 3.1 Integration Ready**: Clean mapping between Web UI logic and agent tool calling protocols.
- **Zero Database Dependency**: Stateless static application requiring no persistent SQL/NoSQL storage volumes.
- **Responsive PWA Support**: Can be installed as a Progressive Web App on mobile and desktop devices for immediate access.

## Limitations
- **Interactive UI Focus**: Designed primarily for human interaction; requires a FastMCP bridge or headless browser (Playwright) for automated server pipelines.
- **Browser Memory Boundaries**: Processing multi-gigabyte video or PDF files can exhaust client browser RAM limits.
- **Lack of Persistent State**: Does not store user conversion history across browser sessions by default.

## When to use it
- When you need a fast, safe, and self-hosted way to transform text, configuration, or media snippets locally.
- When working with sensitive credentials or proprietary code that must never touch external SaaS servers.
- When providing non-technical team members with a user-friendly interface for routine office file transformations.
- When deploying internal developer toolkits on isolated Kubernetes or Docker host nodes.
- For field engineers operating on air-gapped networks requiring offline utility conversion tools.

## When not to use it
Do not use Omni Tools as an automated batch pipeline for high-throughput background processing. Use CyberChef for complex multi-step data recipes, and dedicated background services like Paperless-ngx, Stirling PDF, or ImageMagick CLI scripts for scheduled server-side processing.

## Getting started

### Docker Quick Start
Run the published container on a local port:

```bash
docker run -d \
  --name omni-tools \
  --restart unless-stopped \
  -p 8080:80 \
  iib0011/omni-tools:latest
```

Access `http://localhost:8080` in your web browser to verify installation.

### Docker Compose Configuration

```yaml
services:
  omni-tools:
    image: iib0011/omni-tools:latest
    container_name: omni-tools
    restart: unless-stopped
    ports:
      - "8080:80"
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:80/"]
      interval: 30s
      timeout: 5s
      retries: 3
```

Start the container stack: `docker compose up -d`

## CLI examples

```bash
# Pull latest Omni Tools static container image
docker pull iib0011/omni-tools:latest

# Check container execution status and web server logs
docker logs -f omni-tools

# Confirm HTTP service availability locally
curl -I http://localhost:8080

# Run static security scan on container image
trivy image iib0011/omni-tools:latest

# Backup static assets or container export
docker export omni-tools > omni-tools-backup.tar
```

## API examples

### FastMCP 3.1 & Pydantic v2 Omni Tools Bridge Server
The following complete Python snippet implements a FastMCP 3.1 server exposing Omni Tools data transformation capabilities to local LLM agent swarms with Pydantic v2 schemas:

```python
import json
import base64
import hashlib
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# Define Pydantic v2 data models for transformation payloads
class TransformationRequest(BaseModel):
    operation: Literal["format_json", "generate_hash", "sanitize_string", "base64_encode"] = Field(...)
    input_text: str = Field(..., min_length=1, description="Raw input text string to transform.")
    hash_algorithm: Optional[Literal["sha256", "md5", "sha512"]] = Field("sha256")

    @field_validator("input_text")
    @classmethod
    def validate_json_if_formatting(cls, v: str, info) -> str:
        if info.data.get("operation") == "format_json":
            try:
                json.loads(v)
            except Exception as e:
                raise ValueError(f"Invalid JSON string provided for formatting: {str(e)}")
        return v

class TransformationResponse(BaseModel):
    operation: str
    success: bool
    output_text: str
    character_count: int

# Initialize FastMCP 3.1 server
mcp = FastMCP("omni-tools-agent-bridge")

@mcp.tool()
async def process_omni_transformation(request: TransformationRequest) -> TransformationResponse:
    """Executes a local data transformation equivalent to Omni Tools client-side utilities."""
    output = ""
    if request.operation == "format_json":
        parsed = json.loads(request.input_text)
        output = json.dumps(parsed, indent=2)
    elif request.operation == "generate_hash":
        if request.hash_algorithm == "sha256":
            output = hashlib.sha256(request.input_text.encode("utf-8")).hexdigest()
        elif request.hash_algorithm == "md5":
            output = hashlib.md5(request.input_text.encode("utf-8")).hexdigest()
        else:
            output = hashlib.sha512(request.input_text.encode("utf-8")).hexdigest()
    elif request.operation == "sanitize_string":
        output = request.input_text.strip().replace("\r\n", "\n")
    elif request.operation == "base64_encode":
        output = base64.b64encode(request.input_text.encode("utf-8")).decode("utf-8")

    return TransformationResponse(
        operation=request.operation,
        success=True,
        output_text=output,
        character_count=len(output)
    )

if __name__ == "__main__":
    mcp.run()
```

### Playwright Browser Automation Snippet
```python
from playwright.sync_api import sync_playwright

def format_json_via_browser(raw_json: str) -> str:
    """Automates JSON formatting using local Omni Tools web UI in headless browser."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/#/json-formatter")

        # Interact with UI elements
        page.fill("textarea.json-input", raw_json)
        page.click("button.btn-format")

        result = page.inner_text("textarea.json-output")
        browser.close()
        return result

print(format_json_via_browser('{"name":"OmniTools","version":"2027.1"}'))
```

## Troubleshooting & Common Configurations

### Reverse Proxy Header Configuration (Nginx)
When hosting behind Nginx reverse proxy, ensure standard static caching headers and MIME type mapping are preserved:

```nginx
server {
    listen 80;
    server_name omni.local;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        add_header Cross-Origin-Opener-Policy "same-origin";
        add_header Cross-Origin-Embedder-Policy "require-corp";
    }
}
```

### WebAssembly Memory Error in Restricted Browsers
- **Cause**: SharedArrayBuffer cross-origin isolation headers (`COOP`/`COEP`) missing from web server response.
- **Solution**: Configure reverse proxy headers as shown above to enable high-performance client-side WASM threading.

## Related tools / concepts
- [IT-Tools](it-tools.md) — Feature-rich developer utility web app.
- [Paperless-ngx](paperless-ngx.md) — Self-hosted document archiving and OCR system.
- [Authentik](authentik.md) — Identity provider and SSO authentication gateway.
- [CyberChef](https://github.com/gchq/CyberChef) — Advanced data transformation recipe workbench.
- [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) — Comprehensive PDF manipulation platform.
- [FastMCP](../tools/automation_orchestration/mcp.md) — Model Context Protocol tool framework.

## Sources / references
- [Omni Tools GitHub Repository](https://github.com/iib0011/omni-tools)
- [Omni Tools Docker Hub Image](https://hub.docker.com/r/iib0011/omni-tools)
- [CyberChef Open Source Repository](https://github.com/gchq/CyberChef)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/2026-03-31)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
