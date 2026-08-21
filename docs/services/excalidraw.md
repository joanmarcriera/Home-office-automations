# Excalidraw

Excalidraw is a lightweight, open-source sketching tool that allows you to create diagrams with a distinct hand-drawn aesthetic, optimized for rapid visual communication and AI-native reasoning in the early January 2027 agentic ecosystem.

## What it is
Excalidraw is a lightweight, open-source sketching tool that allows you to create diagrams with a distinct hand-drawn aesthetic. It focuses on simplicity, speed, and real-time collaboration. As of early January 2027, it serves as a primary canvas for **AI-native visual reasoning**, where autonomous agents use the whiteboard to externalize complex logic and architectural designs.

## What problem it solves
It lowers the barrier to creating visual documentation and brainstorming. Unlike complex CAD or formal diagramming tools, Excalidraw encourages "lo-fi" sketching which is often better for early-stage ideas and quick explanations where formal notation would be a distraction. It provides a structured JSON format that is easily parseable by LLMs, facilitating seamless human-AI co-creation.

## Where it fits in the stack
Excalidraw fits into the **Brainstorming and Visual Communication** layer. It is often used for documentation in READMEs and internal wikis, and serves as a visual playground for agents (e.g., GPT-5.5, Claude 5.1, Gemini 4.0, Llama 4) to "draw" their reasoning or architecture proposals using **MCP 3.1 visual design patterns**.

## Typical use cases
- **AI-Native Visual Reasoning**: Agents generating and modifying diagrams to explain multi-step planning.
- **UI/UX Wireframing**: Quickly sketching interface ideas for new agent-driven apps.
- **Process Brainstorming**: Mapping out high-level agentic workflows or [n8n](n8n.md) logic.
- **Visual Documentation**: Creating explanatory diagrams for software architecture in a "whiteboard" style.
- **MCP 3.1 Task Visualization**: Representing complex tool-calling sequences and task graphs visually.

## Strengths
- **Simplicity**: Extremely intuitive interface with no learning curve.
- **Aesthetic**: Hand-drawn look makes diagrams feel approachable and "work-in-progress".
- **Portable**: Diagrams are stored as JSON and can be easily embedded or shared.
- **E2EE Collaboration**: Live sessions are end-to-end encrypted.
- **AI-Powered**: Native support for AI-assisted diagram generation, including "Diagram to Code" and "Sketch to Architecture" workflows.

## Limitations
- **No Formal Notation**: Not suitable for strict UML, ERD, or complex technical specifications requiring precise alignment.
- **Manual Layout**: Lacks the auto-layout capabilities found in tools like [Draw.io](drawio.md) or Mermaid.
- **Versioning**: Native version control for diagrams is limited compared to Git-based Mermaid.

## When to use it
- When you need to quickly sketch a diagram during a meeting or brainstorming session.
- For creating approachable visuals for blog posts, documentation, or social media.
- When an agent needs a "scratchpad" to visualize its internal planning or state.
- If you use [Obsidian](../tools/ai_knowledge/obsidian.md) and want a powerful, integrated sketching solution.

## When not to use it
- For professional engineering diagrams that require strict adherence to industry standards (UML, SysML).
- When you need automatic layout of nodes and edges (use Mermaid or [Gumloop](../tools/automation_orchestration/gumloop.md) visual flows).
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

### Python: Programmatic Element List Validation with Pydantic v2
Because Excalidraw diagrams are stored as structured JSON, agents can programmatically generate, parse, and manipulate elements. The following example validates the structure of Excalidraw elements using Pydantic v2.

```python
from typing import List, Optional
from pydantic import BaseModel, Field

# Define Pydantic v2 schemas for Excalidraw JSON structures
class ExcalidrawElement(BaseModel):
    id: str = Field(..., description="Unique element identifier")
    type: str = Field(..., description="Type of element (e.g., rectangle, ellipse, arrow, text)")
    x: float = Field(..., description="The x-coordinate position")
    y: float = Field(..., description="The y-coordinate position")
    width: float = Field(..., description="Width of the element")
    height: float = Field(..., description="Height of the element")
    backgroundColor: str = Field("transparent", description="Fill color")
    strokeColor: str = Field("#000000", description="Line/outline color")
    strokeWidth: int = Field(1, description="Outline thickness")
    fillStyle: str = Field("hachure", description="Fill texture style")
    opacity: int = Field(100, description="Opacity percentage")
    isDeleted: bool = Field(False, description="Whether the element has been deleted")

class ExcalidrawDiagram(BaseModel):
    type: str = Field("excalidraw", description="Canvas file type")
    version: int = Field(2, description="Excalidraw schema version")
    source: Optional[str] = Field(None, description="Source generator")
    elements: List[ExcalidrawElement] = Field(default_factory=list, description="List of visual elements")

# Example validation logic
def validate_and_parse_diagram(json_data: dict) -> ExcalidrawDiagram:
    # Uses model_validate in Pydantic v2
    return ExcalidrawDiagram.model_validate(json_data)

# Test execution
sample_json = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [
        {
            "id": "rect-1",
            "type": "rectangle",
            "x": 100,
            "y": 150,
            "width": 200,
            "height": 80,
            "strokeColor": "#ff0000",
            "strokeWidth": 2,
            "fillStyle": "solid"
        }
    ]
}

parsed = validate_and_parse_diagram(sample_json)
print(f"Validated diagram with {len(parsed.elements)} elements under MCP 3.1.")
```

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
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Standardized protocol for agent-tool interaction, including visual reasoning (MCP 3.1 compatibility).
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Excellent integration via the Excalidraw plugin.
- [Gumloop](../tools/automation_orchestration/gumloop.md) — Visual AI automation platform.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Used for local AI-assisted sketching.
- [Nextcloud](nextcloud.md) — Can be used to store and sync `.excalidraw` files.
- [Paperless-ngx](paperless-ngx.md) — For archiving exported diagram assets.
- [Authentik](authentik.md) — For securing the local Excalidraw instance.
- [N8N](n8n.md) — For automating the archival of Excalidraw JSON files to Git.

## Sources / References
- [Official Website](https://excalidraw.com/)
- [GitHub Repository](https://github.com/excalidraw/excalidraw)
- [Excalidraw+ Changelog](https://plus.excalidraw.com/changelog)
- [Obsidian Excalidraw Documentation](https://github.com/zsviczian/obsidian-excalidraw-plugin)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2027-01-07
