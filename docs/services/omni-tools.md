# Omni Tools

Omni Tools is a self-hosted collection of powerful web-based tools for everyday tasks. As of May 2026, it remains a top-tier choice for client-side data transformations, complementing [IT-Tools](it-tools.md) with enhanced media processing capabilities.

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

Start it with:

```bash
docker compose up -d
```

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
Omni Tools does not expose a stable public automation API for transformations. Treat it as a browser UI and use health checks for operations:

```bash
curl -fsS http://localhost:8080 >/dev/null && echo "omni-tools is reachable"
```

For scripted transformations, use dedicated CLIs instead. For example, a local JSON formatting fallback can be:

```bash
printf '%s\n' '{"service":"omni-tools","reachable":true}' > input.json
python3 -m json.tool input.json > formatted.json
cat formatted.json
```

## Troubleshooting
- If the page does not load, confirm the container is running with `docker ps --filter name=omni-tools` and that port `8080` is not already in use.
- If reverse proxy assets fail, verify the proxy forwards the original host and path without stripping static asset prefixes.
- If large files crash a browser tab, retry with a smaller file or switch to a server-side CLI designed for that media type.

## Links
- [GitHub Repository](https://github.com/iib0011/omni-tools)
- [Docker Hub](https://hub.docker.com/r/iib0011/omni-tools)

## Related tools / concepts
- [IT-Tools](it-tools.md) — A similar collection of web-based developer tools.
- [Paperless-ngx](paperless-ngx.md) — For long-term document archival and OCR.
- [Nextcloud](nextcloud.md) — For file storage and collaborative office suites.
- [Authentik](authentik.md) — For adding SSO and security to self-hosted utilities.
- [Gitea](gitea.md) — For version-controlling the scripts and configs you transform.
- [SearXNG](searXNG.md) — For private search when looking up transformation standards.
- [Whisper](whisper.md) — For server-side audio-to-text processing.
- [CyberChef](https://github.com/gchq/CyberChef) — The "Swiss Army Knife" of data transformations.

## Advanced Extensibility

Omni Tools can be extended by adding custom local modules or integrating with browser automation for repeatable tasks.

### Adding Custom Local Modules
To add your own tools to a self-hosted instance, you can mount custom JS modules into the container.

1.  **Create a Module**: Define your tool in a JavaScript file (e.g., `my-custom-tool.js`).
    ```javascript
    // my-custom-tool.js
    export const tool = {
      name: "Family Repo Cleaner",
      category: "Text",
      execute: (input) => {
        return input.replace(/TEMP_ID_(\d+)/g, "REDACTED");
      }
    };
    ```
2.  **Mount into Container**:
    ```yaml
    services:
      omni-tools:
        image: iib0011/omni-tools:latest
        volumes:
          - ./custom_tools:/app/public/tools/custom
    ```

### Browser Automation Integration (Playwright)
Since Omni Tools is a web app, you can automate complex transformations using Playwright or Puppeteer.

```python
# Example: Automating a JSON format and Redaction via Omni Tools UI
from playwright.sync_api import sync_playwright

def automate_redaction(json_data):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8080/json-formatter")

        # Paste data into the UI
        page.fill("textarea#input", json_data)
        page.click("button#format")

        # Extract the result
        formatted = page.inner_text("div#output")
        browser.close()
        return formatted

raw_json = '{"user": "Jules", "id": "TEMP_ID_123"}'
print(automate_redaction(raw_json))
```

## Maintenance & Health
Omni Tools is a static web application, so health monitoring focuses on the availability of the web server and the presence of key transformation modules in the UI.

### Automated Health Checks (Playwright)
A reference Playwright script is provided to verify the availability of key modules (JSON, Image, PDF) and confirm the interactive UI is responsive.

```python
# scripts/test_omni_tools_health.py
# Usage: python3 scripts/test_omni_tools_health.py http://your-omni-tools-url
```

Run this script as part of your homelab CI/CD or via a scheduled task to ensure your local utility suite is functioning correctly.

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-26)
- [x] Set up automated Playwright health checks for all modules. (Completed 2026-05-24)

## Sources / References
- https://github.com/iib0011/omni-tools
- https://hub.docker.com/r/iib0011/omni-tools
- https://github.com/gchq/CyberChef

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-26
