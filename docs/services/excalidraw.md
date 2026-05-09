# Excalidraw

## What it is
Excalidraw is a lightweight, open-source sketching tool that allows you to create diagrams with a distinct hand-drawn aesthetic. It focuses on simplicity, speed, and real-time collaboration.

## What problem it solves
It lowers the barrier to creating visual documentation and brainstorming. Unlike complex CAD or formal diagramming tools, Excalidraw encourages "lo-fi" sketching which is often better for early-stage ideas and quick explanations where formal notation would be a distraction.

## Where it fits in the stack
Excalidraw fits into the **Brainstorming and Visual Communication** layer. It is often used for documentation in READMEs, blog posts, and internal wikis where a "human" feel is preferred over rigid technical diagrams.

## Typical use cases
- **UI/UX Wireframing**: Quickly sketching interface ideas.
- **Process Brainstorming**: Mapping out high-level logic or workflows during meetings.
- **Documentation**: Creating explanatory diagrams for software architecture in a "whiteboard" style.
- **Remote Collaboration**: Using the live collaboration feature to brainstorm with others in real-time.

## Strengths
- **Simplicity**: Extremely intuitive interface with no learning curve.
- **Aesthetic**: Hand-drawn look makes diagrams feel approachable and "work-in-progress".
- **Portable**: Diagrams are stored as JSON and can be easily embedded or shared.
- **E2EE Collaboration**: Live sessions are end-to-end encrypted.

## Limitations
- **No Formal Notation**: Not suitable for strict UML, ERD, or complex technical specifications requiring precise alignment and standard icons.
- **Manual Layout**: Lacks the auto-layout capabilities found in tools like [Draw.io](drawio.md) or [Mermaid](../knowledge_base/patterns/diagramming.md).

## When to use it
- When you need to quickly sketch a diagram during a meeting or brainstorming session.
- For creating approachable visuals for blog posts, documentation, or social media.
- When you want a lightweight, browser-based tool without a complex setup or registration.
- If you use Obsidian and want a powerful, integrated sketching solution.

## When not to use it
- For professional engineering diagrams that require strict adherence to industry standards (UML, SysML).
- When you need automatic layout of nodes and edges (use Mermaid or Draw.io instead).
- If you require a deep hierarchy of objects or complex multi-page document management.

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
While Excalidraw is primarily a browser-based tool, you can use the `@excalidraw/utils` package if you need to manipulate Excalidraw data via Node.js:

```bash
# Example: Using a custom script to convert Excalidraw JSON to SVG
node convert_to_svg.js my_diagram.excalidraw

# Docker management
docker logs excalidraw
docker restart excalidraw
```

## API examples
Excalidraw can be embedded as a React component or controlled via its scene data.

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

### Exporting via API (using `@excalidraw/utils`)
```javascript
import { exportToSvg } from "@excalidraw/utils";

const svg = await exportToSvg({
  elements: diagramElements,
  appState: { exportWithBlur: false },
  files: null,
});
```

## Related tools / concepts
- [Draw.io](drawio.md) — For professional-grade, formal technical diagrams.
- [tldraw](https://www.tldraw.com/) — A similar lightweight sketching alternative.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Excellent integration via the Excalidraw plugin.
- [Mermaid](../knowledge_base/patterns/diagramming.md) — Text-to-diagram alternative.
- [Nextcloud](nextcloud.md) — Can be used to store and sync `.excalidraw` files.
- [Excalidraw Libraries](https://libraries.excalidraw.com/) — Community-contributed shapes and icons.
- [Excalidraw Scripting](https://plus.excalidraw.com/plus/scripts) — Extending functionality with custom scripts.

## Links
- [Official Website](https://excalidraw.com/)
- [GitHub Repository](https://github.com/excalidraw/excalidraw)

## Backlog
- Integrate with Obsidian via the Excalidraw plugin.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15

## Sources / References
- https://excalidraw.com/
- https://github.com/excalidraw/excalidraw
- https://www.tldraw.com/
