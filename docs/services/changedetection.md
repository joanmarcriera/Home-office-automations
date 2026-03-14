# Changedetection.io

Changedetection.io is an open-source tool to monitor websites for content changes.

## Description
It provides a simple way to track changes on any website and receive notifications via various channels (Discord, Slack, Email, etc.). It is highly useful for tracking price drops, software releases, or news updates.

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
```

## API examples
Changedetection.io features a REST API. Authenticate with your API key from the Settings tab:

```bash
# List all watches
curl http://localhost:5000/api/v1/watch \
     -H "x-api-key: <your_api_key>"
```

## Links
- [Official Website](https://changedetection.io/)
- [GitHub Repository](https://github.com/dgtlmoon/changedetection.io)

## Alternatives
- [Huginn](https://github.com/huginn/huginn)
- [WebCheck](https://github.com/Lissy93/web-check)

## Backlog
- Configure visual filter to ignore dynamic elements like timestamps.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://changedetection.io/
- https://github.com/dgtlmoon/changedetection.io
- https://github.com/huginn/huginn
