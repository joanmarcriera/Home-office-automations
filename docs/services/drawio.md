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

## When to use it
- When you need to create formal, technical diagrams (UML, Network, Cloud Architecture).
- When you want a professional Visio alternative that works across Windows, macOS, and Linux.
- When you need to export diagrams to multiple formats (PDF, PNG, SVG, XML) for documentation.

## When not to use it
Draw.io is not the best fit for text-native diagrams that must be reviewed primarily in pull requests, generated from code, or diffed line-by-line; use Mermaid or PlantUML for those cases. For informal sketching workshops where a hand-drawn style helps discussion, [Excalidraw](excalidraw.md) may be faster.

## Getting started

### Docker (Self-Hosted)
To run a private instance of Draw.io using Docker:

```bash
docker run -d --name="drawio" -p 8080:8080 -p 8443:8443 jgraph/drawio
```

Access your instance at `http://localhost:8080`.

### TrueNAS Deployment
To host Draw.io on TrueNAS:
1. **Create a Dataset**: Create a dataset for optional persistence (e.g., `/mnt/pool/apps/drawio`).
2. **Custom App (SCALE)**:
   - **Image**: `jgraph/drawio:latest`
   - **Ports**: Map a host port (e.g., 30081) to 8080.
3. **Environment**: Optionally configure `DRAWIO_VIEWER_URL` if hosting a custom viewer.

### Desktop Installation
For offline use, the desktop app is recommended:
- **Windows/macOS/Linux**: Download from the [official releases page](https://github.com/jgraph/drawio-desktop/releases).

## CLI examples
The Draw.io Desktop app includes a CLI for batch processing and conversion:

```bash
cat > sample.drawio <<'XML'
<mxfile><diagram name="Page-1"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel></diagram></mxfile>
XML

# Export a diagram to PDF via CLI (Desktop app required)
drawio -x -f pdf -o sample.pdf sample.drawio

# Export to PNG with a specific width
drawio -x -f png --width 1200 -o sample.png sample.drawio

# Check that the self-hosted container exists and inspect its state
docker inspect --format='{{.State.Status}}' drawio
```

### Advanced: CLI XML Manipulation
For automated architecture updates, you can manipulate the underlying XML of a `.drawio` file using standard CLI tools like `sed` or specialized XML parsers.

```bash
# Example: Automatically update a version label in a diagram
# Assuming the XML contains an attribute value="v1.0.0"

sed -i 's/value="v1\.0\.0"/value="v1.1.0"/g' architecture.drawio

# Example: Use a Python script to inject a new node into the XML
python3 -c '
import xml.etree.ElementTree as ET
tree = ET.parse("architecture.drawio")
root = tree.getroot()
# Find the mxGraphModel and add a new cell (highly simplified)
# In practice, use a library like drawio-tools
print("XML parsed successfully")
'
```

## API examples
Draw.io can be controlled via URL parameters for embedding or automated opening.

### Embedding via URL Parameters
You can pass parameters to the Draw.io URL to configure its behavior:

```html
<!-- Embed Draw.io with specific UI configuration -->
<iframe id="drawio-iframe"
        frameborder="0"
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
  xml: '<mxfile><diagram name="Page-1"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel></diagram></mxfile>'
}), '*');
```

## Related tools / concepts
- [Excalidraw](excalidraw.md) — For hand-drawn style sketching.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Can integrate Draw.io diagrams via plugins.
- [Mermaid](../knowledge_base/patterns/diagramming.md) — Text-based diagramming alternative.
- [Gitea](gitea.md) — For version-controlling diagram files.
- [Nextcloud](nextcloud.md) — Storage backend for Draw.io diagrams.
- [Paperless-ngx](paperless-ngx.md) — For archiving exported diagram PDFs.
- [Authentik](authentik.md) — For securing the self-hosted Draw.io interface.
- [Tailscale](tailscale.md) — For secure remote access to your self-hosted instance.

## Links
- [Official Website](https://www.draw.io/)
- [GitHub Repository](https://github.com/jgraph/drawio)
- [Docker Hub](https://hub.docker.com/r/jgraph/drawio)

## Backlog
- [ ] Perform quarterly technical freshness audit.
- [x] Set up self-hosted instance on TrueNAS for offline access.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-08

## Sources / References
- https://www.draw.io/
- https://github.com/jgraph/drawio
- https://www.diagrams.net/blog/drawio-docker-app
