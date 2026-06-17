# Changedetection.io

## What it is
Changedetection.io is a self-hosted open-source tool designed to monitor websites for content changes. It provides a clean web interface to add URLs, set up filters, and configure notification triggers, allowing users to track modifications in specific parts of a page with high precision. In 2026, it is the standard for triggering agentic workflows based on external web events.

## What problem it solves
It eliminates the need for manual website checking by automating the observation process. It solves the problem of "information decay" by pushing alerts when price drops, software releases, or policy updates occur. It acts as a bridge between static web content and dynamic automation pipelines, providing reliable change detection for pages that lack RSS feeds or official APIs.

## Where it fits in the stack
In the automation ecosystem, Changedetection.io acts as a **Web Event Trigger**. It sits in the ingestion layer, sending webhooks to [n8n](n8n.md) or Apprise, which then kick off complex workflows using Claude 4.8 Opus and GPT-5.5.

## Typical use cases
- **Price Tracking**: Monitoring retail sites for discounts or stock availability.
- **Software Release Monitoring**: Watching GitHub or product pages for new versions.
- **Regulatory Monitoring**: Tracking changes to government or corporate legal/policy pages.
- **Visual Regression**: Capturing screenshots over time to see how a site's design evolves.
- **AI Dataset Ingestion**: Triggering fresh scraping for local AI knowledge bases when a source updates.

## Strengths
- **Multiple Fetchers**: Supports fast basic fetching and Playwright/Selenium for JS-heavy Single Page Applications (SPAs).
- **Granular Filters**: Use CSS selectors, XPath, or JSONPath to monitor only specific, relevant page elements.
- **Snapshot History**: Keeps a versioned history of changes, allowing for detailed diff analysis.
- **Extensive Notifications**: Integrates with Apprise to support over 70 notification services (Telegram, Discord, etc.).

## Limitations
- **Bot Detection**: Can be blocked by aggressive anti-bot measures like Cloudflare Turnstile without advanced proxy management.
- **Resource Intensity**: Running multiple Playwright/WebDriver fetchers simultaneously can be memory-intensive on smaller servers.
- **Configuration Complexity**: Monitoring highly dynamic sites may require deep knowledge of CSS/XPath to avoid false positives.

## When to use it
- When you need to monitor specific website elements for changes without manual effort.
- To receive automated notifications for price drops or critical software updates.
- For building automated ingestion pipelines that respond to external web content modifications.

## When not to use it
- For high-frequency, millisecond-level data monitoring (e.g., high-frequency stock trading).
- If the target site has an official, reliable, and free API that provides the same data.
- If the content is behind complex, multi-step authentication that Changedetection cannot easily navigate.

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

### Filters & Noise Reduction
Effective website monitoring requires filtering out dynamic content that changes on every load (e.g., timestamps, session IDs, ads).
- **CSS Selectors**: Use selectors like `main#content` or `article.post` to focus the monitor. Exclude elements like `.sidebar` or `.footer`.
- **Ignoring Text (Regex)**: Use regex in the "Filters" tab to strip patterns:
    - `[0-9]{2}:[0-9]{2}:[0-9]{2}` (Timestamps)
    - `[0-9]+ comments` (Comment counts)
    - `\d+ views` (View counts)
- **Visual Filters**: When using Playwright/Selenium, use the "Visual Filter" selector to click and hide elements directly from the rendered preview.

## CLI examples
The service can be managed and inspected via Docker:

```bash
# View live logs to debug fetcher issues
docker logs changedetection

# Check the installed version inside the container
docker exec changedetection python3 -c "import changedetectionio; print(changedetectionio.__version__)"

# Force a restart of the monitoring service
docker restart changedetection
```

## API examples
Changedetection.io features a REST API for programmatic control. Authenticate using the API key found in the Settings tab.

### Listing All Watches (curl)
```bash
curl http://localhost:5000/api/v1/watch \
     -H "x-api-key: <your_api_key>"
```

### Checking Watch Status (Python)
```python
import requests

API_URL = "http://localhost:5000/api/v1/watch"
headers = {"x-api-key": "your_api_key_here"}

response = requests.get(API_URL, headers=headers)
if response.status_code == 200:
    for uuid, data in response.json().items():
        print(f"Watch: {data.get('title')} | Last Checked: {data.get('last_checked')}")
```

## Related tools / concepts
- [n8n](n8n.md) — For orchestrating advanced workflows triggered by detected changes.
- [Linkwarden](linkwarden.md) — For archiving and managing links discovered during monitoring.
- [Authentik](authentik.md) — For securing Changedetection.io with SSO and MFA.
- [Paperless-ngx](paperless-ngx.md) — For ingesting and indexing PDF snapshots of changed pages.
- [Gitea](gitea.md) — For version-controlling configuration or scripts related to monitoring.
- [Nextcloud](nextcloud.md) — For storing and syncing exported snapshots.
- [Home Assistant](home-assistant.md) — For triggering physical home alerts based on web content changes.
- [Playwright](../tools/development_ops/playwright.md) — The underlying engine used for monitoring Javascript-heavy sites.
- [Apprise](https://github.com/caronc/apprise) — Notification engine for 70+ services.

## Sources / references
- [Official Website](https://changedetection.io/)
- [GitHub Repository](https://github.com/dgtlmoon/changedetection.io)
- [Apprise Documentation](https://github.com/caronc/apprise)
- [Changedetection.io REST API Docs](https://github.com/dgtlmoon/changedetection.io/wiki/API)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
