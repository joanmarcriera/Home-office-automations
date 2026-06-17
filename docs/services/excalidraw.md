# Excalidraw

Excalidraw is a lightweight, open-source sketching tool that allows you to create diagrams with a distinct hand-drawn aesthetic, optimized for rapid visual communication in the June 2026 agentic ecosystem.

## What it is
Excalidraw is a lightweight, open-source sketching tool that allows you to create diagrams with a distinct hand-drawn aesthetic. It focuses on simplicity, speed, and real-time collaboration. As of June 2026, it features deep AI integration, allowing for "Sketch to Code" and "Sketch to Architecture" workflows.

## What problem it solves
It lowers the barrier to creating visual documentation and brainstorming. Unlike complex CAD or formal diagramming tools, Excalidraw encourages "lo-fi" sketching which is often better for early-stage ideas and quick explanations where formal notation would be a distraction. It also provides a structured JSON format that is easily parseable by LLMs.

## Where it fits in the stack
Excalidraw fits into the **Brainstorming and Visual Communication** layer. It is often used for documentation in READMEs and internal wikis, and serves as a visual playground for agents like Claude 4.8 Opus to "draw" their reasoning or architecture proposals.

## Typical use cases
- **UI/UX Wireframing**: Quickly sketching interface ideas for new agent-driven apps.
- **Process Brainstorming**: Mapping out high-level agentic workflows or n8n logic.
- **Visual Documentation**: Creating explanatory diagrams for software architecture in a "whiteboard" style.
- **Remote Collaboration**: Using the E2EE live collaboration feature to brainstorm with human and AI participants.
- **Sketch-to-Code**: Using the native "Diagram to Code" feature to generate React/Tailwind code from a drawing.

## Strengths
- **Simplicity**: Extremely intuitive interface with no learning curve.
- **Aesthetic**: Hand-drawn look makes diagrams feel approachable and "work-in-progress".
- **Portable**: Diagrams are stored as JSON and can be easily embedded or shared.
- **E2EE Collaboration**: Live sessions are end-to-end encrypted.
- **AI-Powered**: Native support for AI-assisted diagram generation and image-to-sketch conversion.

## Limitations
- **No Formal Notation**: Not suitable for strict UML, ERD, or complex technical specifications requiring precise alignment.
- **Manual Layout**: Lacks the auto-layout capabilities found in tools like [Draw.io](drawio.md) or [Mermaid](../knowledge_base/patterns/diagramming.md).
- **Versioning**: Native version control for diagrams is limited compared to Git-based Mermaid.

## When to use it
- When you need to quickly sketch a diagram during a meeting or brainstorming session.
- For creating approachable visuals for blog posts, documentation, or social media.
- When you want a lightweight, browser-based tool without a complex setup.
- If you use Obsidian and want a powerful, integrated sketching solution.

## When not to use it
- For professional engineering diagrams that require strict adherence to industry standards (UML, SysML).
- When you need automatic layout of nodes and edges (use Mermaid instead).
- If you require a deep hierarchy of objects or complex multi-page document management.

## Getting started

### Docker installation
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
2. Start sketching using the tools provided in the top toolbar.
3. To share your drawing, use the "Live collaboration" feature or export your work via the "Export" button.

## CLI examples
While Excalidraw is primarily a browser-based tool, you can use the `@excalidraw/utils` package for programmatic manipulation.

```bash
# Example: Using a custom script to convert Excalidraw JSON to SVG (Node.js)
node convert_to_svg.js my_diagram.excalidraw

# Docker management
docker logs excalidraw
docker restart excalidraw
```

## API examples

### React Integration
```javascript
import { Excalidraw } from "@excalidraw/excalidraw";

function App() {
  return (
    <div style={{ height: "500px" }}>
      <Excalidraw onChange={(elements, state) => console.log("Elements changed", elements)} />
    </div>
  );
}
```

### Obsidian Integration
Excalidraw integrates deeply with [Obsidian](../tools/ai_knowledge/obsidian.md) via the community plugin.

1.  In Obsidian, go to **Settings** > **Community plugins** > **Browse**.
2.  Search for "Excalidraw" and click **Install**, then **Enable**.
3.  Use `[[Note Name]]` to link elements to other notes.
4.  The plugin can perform local OCR on hand-written text within drawings.

## Related tools / concepts
- [Draw.io](drawio.md) — For professional-grade, formal technical diagrams.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Excellent integration via the Excalidraw plugin.
- [Mermaid](../knowledge_base/patterns/diagramming.md) — Text-to-diagram alternative with native support.
- [Nextcloud](nextcloud.md) — Can be used to store and sync `.excalidraw` files.
- [tldraw](https://www.tldraw.com/) — A similar lightweight sketching alternative.
- [Paperless-ngx](paperless-ngx.md) — For archiving exported diagram assets.
- [Authentik](authentik.md) — For securing the local Excalidraw instance.
- [N8N](n8n.md) — For automating the archival of Excalidraw JSON files to Git.

## Sources / References
- [Official Website](https://excalidraw.com/)
- [GitHub Repository](https://github.com/excalidraw/excalidraw)
- [Excalidraw+ Changelog](https://plus.excalidraw.com/changelog)
- [Obsidian Excalidraw Documentation](https://github.com/zsviczian/obsidian-excalidraw-plugin)

## Backlog
- [x] Perform technical freshness audit (June 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-16
