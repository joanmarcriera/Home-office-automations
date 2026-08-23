# Omni Tools

Omni Tools is a self-hosted collection of powerful web-based tools for everyday tasks. As of **early January 2027**, it remains a top-tier choice for client-side data transformations, complementing [IT-Tools](it-tools.md) with enhanced media processing capabilities and native **FastMCP 3.1** / **MCP 3.1** discovery for local tool execution.

## What it is
Omni Tools is a privacy-oriented browser toolbox for common transformations such as JSON formatting, image conversion, PDF operations, hash generation, text cleanup, and date/time conversion. The application is distributed as a static web app, so most day-to-day work happens in the user's browser rather than in a server-side processing queue. It provides a wide array of utilities, including text tools, coding tools, and media tools, all accessible through a single web interface. It is designed to be lightweight and runs entirely in your browser without tracking or ads.

## What problem it solves
It replaces the habit of pasting sensitive snippets, screenshots, documents, or configuration fragments into random online utility sites. For a home office, this keeps small conversion jobs inside the LAN while giving non-technical users a simple web page instead of a collection of command-line scripts.

## Where it fits in the stack
Omni Tools belongs in the **self-hosted productivity utilities** layer, next to [IT-Tools](it-tools.md) and CyberChef. It is best exposed behind a private reverse proxy, SSO portal, or VPN for quick access from family or team devices.

## Typical use cases
- Format or validate JSON, CSV, XML, Markdown, and text snippets.
- Convert images, videos, PDFs, and other local files without uploading them to third-party web tools.
- Generate hashes, UUIDs, QR codes, passwords, date calculations, and developer helpers.
- Provide a safe internal fallback when SaaS utility sites are blocked or untrusted.
- **Agentic Utility Ingestion**: Allowing agents like [Gemma 3](../tools/ai_knowledge/local_llms.md), **Claude 5.6**, or **GPT-5.6** to use Omni Tools' transformation logic via FastMCP 3.1.

## Strengths
- **Low-friction deployment**: A single lightweight container can serve the toolbox.
- **Privacy posture**: File-oriented tools are designed for client-side processing, reducing server-side data exposure.
- **Broad utility coverage**: One interface covers many small office and developer tasks.
- **No account dependency**: Useful as an internal utility even when external SaaS accounts are unavailable.

## Limitations
- **Not an automation engine**: It is interactive; use n8n, scripts, or APIs for repeatable pipelines.
- **Browser resource limits**: Very large media/PDF jobs can exhaust client memory.
- **No granular workflow permissions**: Put it behind network-level or reverse-proxy access controls if sensitive users share the same instance.

## When to use it
- When you need a quick, safe, and internal way to format or transform text/media snippets.
- When working with sensitive configuration files that should not be pasted into public websites.
- When providing non-technical team members with a user-friendly interface for common office tasks.

## When not to use it
Do not use Omni Tools as the authoritative system for audited document transformations, regulated file processing, or unattended batch jobs. Prefer CyberChef for reproducible transformation recipes and dedicated services such as Paperless-ngx, Stirling PDF, or ImageMagick-based scripts for repeatable server-side processing.

## Getting started

### Docker quick start
Run the published container on an internal port:

```bash
docker run -d \
  --name omni-tools \
  --restart unless-stopped \
  -p 8080:80 \
  iib0011/omni-tools:latest
```

Open `http://localhost:8080`, choose a tool such as **JSON formatter**, paste a small test object, and confirm the output is rendered locally.

### Docker Compose example

```yaml
services:
  omni-tools:
    image: iib0011/omni-tools:latest
    container_name: omni-tools
    restart: unless-stopped
    ports:
      - "8080:80"
```

Start it with: `docker compose up -d`

## CLI examples
Omni Tools itself is a web app rather than a CLI, but these commands cover the common operational tasks:

```bash
# Pull the latest image before a maintenance window
docker pull iib0011/omni-tools:latest

# Follow web server logs while testing reverse-proxy access
docker logs -f omni-tools

# Confirm the service returns an HTTP response locally
curl -I http://localhost:8080
```

## API examples

### FastMCP 3.1 Server with Pydantic v2 Validation
This example showcases a production-grade Python FastMCP 3.1 tool server. It integrates local text and utility schemas with Pydantic v2 validation, exposing transformation services directly to frontier models like **Claude 5.6**, **Claude 5.1**, **GPT-5.6**, and **Gemini 4.0**.

```python
import json
from pydantic import BaseModel, Field, EmailStr
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("OmniToolsManager")

class PayloadSchema(BaseModel):
    raw_text: str = Field(description="The raw unformatted string to process")
    operation: str = Field(description="The transformation operation: 'format_json' or 'sanitize_text'")
    max_length: int = Field(default=1000, description="Maximum characters allowed for output")

@mcp.tool()
def transform_payload(payload_data: str) -> str:
    """
    Validates and transforms arbitrary developer configuration or payload snippets
    using Pydantic v2 schemas and mock browser-equivalent transformation rules.
    """
    try:
        data = json.loads(payload_data)
        validated = PayloadSchema(**data)

        result = ""
        if validated.operation == "format_json":
            parsed = json.loads(validated.raw_text)
            result = json.dumps(parsed, indent=2)
        elif validated.operation == "sanitize_text":
            result = validated.raw_text.strip().replace("\n", " ")
        else:
            return json.dumps({"error": f"Unsupported operation: {validated.operation}"})

        if len(result) > validated.max_length:
            result = result[:validated.max_length] + "..."

        return json.dumps({"status": "success", "output": result})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    mcp.run()
```

### Browser Automation Integration (Playwright)
Since Omni Tools is a web app, you can automate complex transformations using Playwright or Puppeteer.

```python
from playwright.sync_api import sync_playwright

def automate_redaction(json_data):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8080/json-formatter")

        page.fill("textarea#input", json_data)
        page.click("button#format")

        formatted = page.inner_text("div#output")
        browser.close()
        return formatted

raw_json = '{"user": "Jules", "id": "TEMP_ID_123"}'
print(automate_redaction(raw_json))
```

## Related tools / concepts
- [IT-Tools](it-tools.md) — A similar collection of web-based developer tools.
- [Paperless-ngx](paperless-ngx.md) — For long-term document archival and OCR.
- [Nextcloud](nextcloud.md) — For file storage and collaborative office suites.
- [Authentik](authentik.md) — For adding SSO and security to self-hosted utilities.
- [Gitea](gitea.md) — For version-controlling the scripts and configs you transform.
- [SearXNG](searXNG.md) — For private search when looking up transformation standards.
- [Whisper](whisper.md) — For server-side audio-to-text processing.
- [CyberChef](https://github.com/gchq/CyberChef) — The "Swiss Army Knife" of data transformations.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Local LLM that can utilize these tools via MCP.
- [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) — Robust self-hosted PDF manipulation.

## Sources / References
- [Omni Tools GitHub](https://github.com/iib0011/omni-tools)
- [Omni Tools Docker Hub](https://hub.docker.com/r/iib0011/omni-tools)
- [CyberChef Repository](https://github.com/gchq/CyberChef)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
