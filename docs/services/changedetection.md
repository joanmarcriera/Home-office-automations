# Changedetection.io

Changedetection.io is an open-source tool to monitor websites for content changes.

## What it is
Changedetection.io is a self-hosted web monitoring tool that tracks changes in website content. It provides a clean web interface to add URLs, set up filters, and configure notification triggers for when specific parts of a page change.

## What problem it solves
It eliminates the need for manual checking of websites for updates. Whether it's tracking price drops on e-commerce sites, monitoring software release pages, or watching for new posts on a blog that lacks an RSS feed, Changedetection.io automates the observation process and pushes alerts to you.

## Where it fits in the stack
In an automation ecosystem, Changedetection.io acts as a **Web Event Trigger**. It can send webhooks to n8n or Apprise, allowing you to kick off complex workflows (like automatically downloading a new software version or updating a budget spreadsheet) based on external website changes.

## Typical use cases
- **Price Tracking**: Monitoring Amazon or specialized retail sites for discounts.
- **Stock Alerts**: Checking if a "Sold Out" item has come back into stock.
- **Regulatory Monitoring**: Tracking changes to government or corporate policy pages.
- **Visual Regression**: Capturing screenshots over time to see how a site's design evolves.

## Strengths
- **Multiple Fetchers**: Supports basic fast fetching as well as Playwright/Selenium for Javascript-heavy sites.
- **Granular Filters**: Use CSS selectors, XPath, or JSONPath to monitor only specific parts of a page.
- **Snapshot History**: Keeps a history of changes, allowing you to see exactly what was added or removed.
- **Massive Notification Support**: Integrates with Apprise to support 70+ notification services.

## Limitations
- **Captcha Blocks**: Can struggle with sites that use aggressive anti-bot measures like Cloudflare Turnstile or reCAPTCHA.
- **Resource Usage**: Using the Playwright/WebDriver fetchers for many sites can be memory-intensive.
- **Complexity**: Monitoring complex SPAs (Single Page Applications) may require advanced CSS selector knowledge.

## When to use it
- When you want to monitor websites for content changes or price drops.
- To receive automated notifications when a specific page updates.
- For tracking software releases or news without manual checking.

## When not to use it
- For high-frequency monitoring of rapidly changing data (consider specialized trading or scraping tools).
- If you need to monitor content behind complex, multi-step authentication that isn't easily scriptable.

## Getting started

### Docker Compose
To run Changedetection.io using Docker Compose:

```yaml
services:
  changedetection:
    image: dgtlmoon/changedetection.io
    container_name: changedetection
    ports:
      - "5000:5000"
    volumes:
      - ./data:/datastore
    restart: unless-stopped
```

Access the interface at `http://localhost:5000`.

## CLI examples
You can monitor the service via Docker:

```bash
# View service logs
docker logs changedetection

# Check the version
docker exec changedetection python3 -c "import changedetectionio; print(changedetectionio.__version__)"

# Restart the service
docker restart changedetection
```

## API examples
Changedetection.io features a REST API. Authenticate with your API key from the Settings tab:

### curl (List Watches)
```bash
# List all watches
curl http://localhost:5000/api/v1/watch \
     -H "x-api-key: <your_api_key>"
```

### Python (Get Watch Status)
```python
import requests

API_URL = "http://localhost:5000/api/v1/watch"
API_KEY = "your_api_key_here"

headers = {"x-api-key": API_KEY}
response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    watches = response.json()
    for watch_uuid, watch_data in watches.items():
        print(f"Watch: {watch_data.get('title')} | Last Checked: {watch_data.get('last_checked')}")
else:
    print(f"Error: {response.status_code}")
```

## Related tools / concepts
- [n8n](n8n.md) — Automate workflows based on content changes.
- [Linkwarden](linkwarden.md) — Archive and manage links found during monitoring.
- [Authentik](authentik.md) — Secure the Changedetection instance with SSO.
- [Paperless-ngx](paperless-ngx.md) — Ingest tracked documents for OCR and archival.
- [Immich](immich.md) — Monitor and archive visual changes to galleries.
- [Nextcloud](nextcloud.md) — Store snapshots and change logs.
- [Home Assistant](home-assistant.md) — Trigger home alerts based on web changes.
- [Apprise](https://github.com/caronc/apprise) — Notification engine for 70+ services.
- [Playwright](https://playwright.dev/) — Headless browser for JS-heavy sites.

## Filters & Noise Reduction
Effective website monitoring requires filtering out dynamic content that changes on every load (e.g., timestamps, session IDs, ads) to avoid false positive alerts.

### CSS Selectors
Use CSS selectors to focus the monitor on specific elements. For example, to monitor only the main article content and ignore sidebars:
- **Include**: `main#content` or `article.post`
- **Exclude**: `.sidebar`, `.footer`, `.advertisement`

### Ignoring Text (Regex)
In the "Filters" tab, use the "Ignore text" field to strip out patterns using regular expressions. Common patterns include:
- `[0-9]{2}:[0-9]{2}:[0-9]{2}` (Timestamps)
- `[0-9]+ comments` (Comment counts)
- `\d+ views` (View counts)

### Visual Filters
When using the Playwright/Selenium fetcher, you can use the "Visual Filter" selector in the UI to click and hide elements directly from a rendered preview of the site.

## Backlog
- [x] Perform quarterly technical freshness audit.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-26

## Sources / References
- [Changedetection.io Official Site](https://changedetection.io/)
- [GitHub Repository](https://github.com/dgtlmoon/changedetection.io)
- [Huginn GitHub Repository](https://github.com/huginn/huginn)
