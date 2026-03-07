# Grocy

Grocy is a self-hosted groceries & household management solution for your home.

## Description
It tracks your stock, shopping list, recipes, and more.

## Getting started

### Docker
The recommended way to install Grocy is via the LinuxServer.io Docker image:

```bash
docker run -d \
  --name=grocy \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -p 9283:80 \
  -v /path/to/config:/config \
  --restart unless-stopped \
  lscr.io/linuxserver/grocy:latest
```

Access the web interface at `http://localhost:9283`.

## CLI examples
Grocy does not have an official CLI. Management is performed through the web interface or the REST API.

## API examples
Grocy provides a RESTful API. Authenticate using an API key (generated in the web UI under "Manage API keys"):

```bash
# Get current stock
curl -X GET "http://localhost:9283/api/stock" \
     -H "GROCY-API-KEY: <your_api_key>"
```

## Links
- [Official Website](https://grocy.info/)
- [Demo](https://en.demo.grocy.info/)

## Alternatives
- [Homebox](homebox.md)
- [KitchenOwl](https://github.com/KitchenOwl/KitchenOwl)

## Backlog
- Set up barcode scanning via mobile app.

## Sources / References

- [Official Website](https://grocy.info/)
- [LinuxServer.io Grocy Documentation](https://docs.linuxserver.io/images/docker-grocy/)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
