# Actual Budget

Actual is a local-first personal finance tool, a 100% free and open-source application.

## Description
Actual is a super fast, privacy-focused budgeting tool that lets you manage your finances with ease. It features a local-first architecture, ensuring your data stays on your device while allowing for synchronization across multiple devices.

## When to use it
- When you want a privacy-focused, local-first budgeting tool.
- For users who want full control over their financial data.
- When you need a 100% free and open-source alternative to YNAB.

## When not to use it
- If you require advanced investment tracking or complex portfolio management.
- If you are not comfortable managing a self-hosted server for synchronization.

## Getting started

### Docker
To run Actual Budget using Docker:

```bash
docker run -d \
  --name actual_server \
  -p 5006:5006 \
  -v actual-data:/data \
  --restart unless-stopped \
  actualbudget/actual-server:latest
```

Access the web interface at `http://localhost:5006`.

## CLI examples
Actual Budget is primarily a web application, but you can manage the container:

```bash
# View server logs
docker logs actual_server

# Check version (if supported by the image)
docker exec actual_server node src/app.js --version
```

## API examples
Actual Budget provides a REST API for programmatic interaction:

```bash
# Get server info
curl http://localhost:5006/info
```

## Links
- [Official Website](https://actualbudget.com/)
- [GitHub Repository](https://github.com/actualbudget/actual)

## Alternatives
- [Firefly III](https://www.firefly-iii.org/)
- [YNAB](https://www.ynab.com/) (Non-OSS)

## Backlog
- Set up automated bank synchronization via GoCardless/Nordigen.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://actualbudget.com/
- https://github.com/actualbudget/actual
- https://www.firefly-iii.org/
