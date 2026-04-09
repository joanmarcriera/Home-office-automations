# Excalidraw

Excalidraw is a virtual whiteboard for sketching hand-drawn like diagrams.

## Description
It is a simple and intuitive tool for creating sketches and diagrams that look like they were drawn by hand. It supports real-time collaboration and is highly accessible via the browser.

## When to use it
- When you need a quick, hand-drawn style diagram for documentation or brainstorming.
- For real-time collaborative sketching with team members.
- When you want a tool that works offline and supports end-to-end encryption.

## When not to use it
- For highly technical architectural diagrams that require strict adherence to UML or other formal notations.
- When you need a tool with advanced layout engines (consider [Draw.io](drawio.md) instead).

## Getting started

### Docker
To run Excalidraw locally using Docker Compose:

```yaml
services:
  excalidraw:
    image: excalidraw/excalidraw:latest
    ports:
      - "3000:80"
    restart: on-failure
```

Alternatively, run it using a single Docker command:

```bash
docker run -d --name excalidraw -p 3000:80 excalidraw/excalidraw:latest
```

### Usage
1. Navigate to `http://localhost:3000` in your browser.
2. Start sketching using the tools provided in the top toolbar (Rectangle, Diamond, Arrow, etc.).
3. To share your drawing, use the "Live collaboration" feature or export your work via the "Export" button.

## CLI examples
Management of the Excalidraw service is typically done via Docker:

```bash
# View service logs
docker logs excalidraw

# Update the Excalidraw image
docker pull excalidraw/excalidraw:latest
docker restart excalidraw

# Execute a shell within the container (for inspection)
docker exec -it excalidraw /bin/sh
```

## Links
- [Official Website](https://excalidraw.com/)
- [GitHub Repository](https://github.com/excalidraw/excalidraw)

## Alternatives
- [Draw.io](drawio.md)
- [tldraw](https://www.tldraw.com/)

## Backlog
- Integrate with Obsidian via the Excalidraw plugin.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://excalidraw.com/
- https://github.com/excalidraw/excalidraw
- https://www.tldraw.com/
