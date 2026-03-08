# MeTube

MeTube is a web GUI for youtube-dl / yt-dlp.

## Description
It provides a simple and easy-to-use interface for downloading videos from YouTube and other sites. It supports various formats and allows you to manage your downloads through the browser.

## When to use it
- When you want a user-friendly web interface for `yt-dlp`.
- For managing video downloads on a remote or headless server.
- When you need to quickly download videos from various platforms without using the terminal.

## When not to use it
- If you prefer the flexibility and advanced options of the `yt-dlp` command-line interface.
- For large-scale media archiving and organization (consider [Tube Archivist](tubearchivist.md) for this).

## Getting started

### Docker
MeTube is most easily deployed via Docker. Run the following command to start the container:

```bash
docker run -d \
  --name metube \
  -p 8081:8081 \
  -v /path/to/downloads:/downloads \
  alexta69/metube
```

The web interface will be available at `http://localhost:8081`.

## CLI examples
MeTube is primarily a web-based application and does not feature a dedicated CLI. Downloads are managed via the web UI or the REST API.

## API examples
You can programmatically add downloads to MeTube using its API.

### Add a download via curl
```bash
curl -X POST http://localhost:8081/add \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "quality": "best"}'
```

### Get current queue
```bash
curl http://localhost:8081/queue
```

## Links
- [GitHub Repository](https://github.com/alexta69/metube)

## Alternatives
- [Tube Archivist](tubearchivist.md)
- [Youtube-dl-gui](https://github.com/MrS0m30n3/youtube-dl-gui)

## Backlog
- Configure automated download folders for specific channels.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/alexta69/metube
- https://github.com/MrS0m30n3/youtube-dl-gui
