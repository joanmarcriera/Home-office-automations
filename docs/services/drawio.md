# Draw.io (diagrams.net)

Draw.io (now diagrams.net) is a free, open-source, and cross-platform graph drawing software developed in HTML5 and JavaScript.

## What it is
Draw.io is a professional-grade diagramming tool that provides a wide range of features for creating flowcharts, process diagrams, organizational charts, UML, ER, and network diagrams.

## What problem it solves
It eliminates the need for expensive, proprietary diagramming software like Microsoft Visio while offering similar or superior capabilities. It provides a platform-agnostic way to create, store, and share visual documentation without vendor lock-in.

## Where it fits in the stack
Draw.io sits in the **Documentation and Design** layer of the home-office stack. It serves as the primary tool for visualizing architecture, workflows, and complex systems before or during implementation.

## Typical use cases
- **Network Architecture**: Designing and documenting home lab or enterprise network layouts.
- **Software Design**: Creating UML diagrams, ER diagrams for databases, and software flowcharts.
- **Project Planning**: Building Gantt charts and process maps for project management.
- **Cloud Infrastructure**: Visualizing AWS, Azure, or GCP deployments using built-in icon sets.

## Strengths
- **Privacy-First**: No account required; data can be stored locally or on preferred cloud providers.
- **Extensive Library**: Huge collection of icons for networking, cloud, UI design, and more.
- **Highly Compatible**: Can import/export Visio (.vsdx), Lucidchart, and other formats.
- **Cross-Platform**: Available as a web app, desktop app, and can be self-hosted.

## Limitations
- **Collaboration**: Real-time collaboration in the self-hosted version is more complex to set up than the SaaS version.
- **UI Density**: The interface can be intimidating for users who only need simple sketching tools (consider [Excalidraw](excalidraw.md) for those cases).

## Getting started

### Docker (Self-Hosted)
To run a private instance of Draw.io using Docker:

```bash
docker run -d --name="drawio" -p 8080:8080 -p 8443:8443 jgraph/drawio
```

Access your instance at `http://localhost:8080`.

### Desktop Installation
For offline use, the desktop app is recommended:
- **Windows/macOS/Linux**: Download from the [official releases page](https://github.com/jgraph/drawio-desktop/releases).

## CLI examples
The Draw.io Desktop app includes a CLI for batch processing and conversion:

```bash
# Export a diagram to PDF via CLI (Desktop app required)
drawio -x -f pdf -o output.pdf input.drawio

# Export to PNG with a specific width
drawio -x -f png --width 1200 -o diagram.png architecture.drawio

# Check Docker container health
docker inspect --format='{{.State.Health.Status}}' drawio
```

## API examples
Draw.io can be controlled via URL parameters for embedding or automated opening.

### Embedding via URL Parameters
You can pass parameters to the Draw.io URL to configure its behavior:

```html
<!-- Embed Draw.io with specific UI configuration -->
<iframe frameborder="0"
        width="100%"
        height="600px"
        src="https://embed.diagrams.net/?embed=1&ui=atlas&spin=1&proto=json">
</iframe>
```

### JSON Protocol
When embedding, you can send actions via `postMessage`:

```javascript
// Example: Sending a 'load' action to an embedded Draw.io iframe
const iframe = document.getElementById('drawio-iframe');
iframe.contentWindow.postMessage(JSON.stringify({
  action: 'load',
  xml: '<mxfile>...</mxfile>'
}), '*');
```

## Related tools / concepts
- [Excalidraw](excalidraw.md) — For hand-drawn style sketching.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Can integrate Draw.io diagrams via plugins.
- [Mermaid](../knowledge_base/patterns/diagramming.md) — Text-based diagramming alternative.
- [Gitea](gitea.md) — For version-controlling diagram files.
- [Nextcloud](nextcloud.md) — Storage backend for Draw.io diagrams.

## Links
- [Official Website](https://www.draw.io/)
- [GitHub Repository](https://github.com/jgraph/drawio)
- [Docker Hub](https://hub.docker.com/r/jgraph/drawio)

## Backlog
- Set up self-hosted instance on TrueNAS for offline access.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-20

## Sources / References
- https://www.draw.io/
- https://github.com/jgraph/drawio
- https://www.diagrams.net/blog/drawio-docker-app
