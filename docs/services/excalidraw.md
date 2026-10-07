# Excalidraw

## What it is
Excalidraw is an open-source, lightweight virtual whiteboard and sketching ecosystem optimized for hand-drawn aesthetics, real-time collaboration, and structured visual reasoning in multi-agent AI networks. In modern developer environments, Excalidraw serves as both a human sketching tool and a machine-readable canvas where autonomous agents (e.g., [Claude Code](../tools/development_ops/claude-code.md), [Home Admin Agent](home-admin-tools.md)) externalize architectural ideas, sequence diagrams, and task dependency graphs.

Because Excalidraw scenes are stored as deterministic JSON documents containing precise coordinate, shape, arrow, and text bindings, AI models can inspect, generate, and edit visual layouts programmatically via [FastMCP 3.1](../tools/automation_orchestration/mcp.md) servers.

```
+--------------------------------------------------------------------------------------------------------------------+
|                                         EXCALIDRAW VISUAL REASONING STACK                                          |
+--------------------------------------------------------------------------------------------------------------------+
|                                                                                                                    |
|  +--------------------------------+      +---------------------------------+      +-----------------------------+  |
|  |   Human Whiteboard User        |      |   FastMCP 3.1 Tool Server       |      | Autonomous AI Agent         |  |
|  |   (Browser / Obsidian Canvas)  |      |   (Pydantic v2 Schema Engine)   |      | (Claude Code / Llama 4)     |  |
|  +---------------+----------------+      +----------------+----------------+      +--------------+--------------+  |
|                  |                                        |                                      |                 |
|                  +-------------------+--------------------+--------------------------------------+                 |
|                                      |                                                                             |
|                                      v                                                                             |
|                       +------------------------------+                                                             |
|                       |   Excalidraw JSON Data       |                                                             |
|                       |  (Elements, Bindings, x/y)   |                                                             |
|                       +--------------+---------------+                                                             |
|                                      |                                                                             |
|                                      v                                                                             |
|                       +------------------------------+                                                             |
|                       |  Self-Hosted Excalidraw App  |                                                             |
|                       |  (Docker Container / Node.js)|                                                             |
|                       +--------------+---------------+                                                             |
|                                      |                                                                             |
|                                      v                                                                             |
|                       +------------------------------+                                                             |
|                       | Exported SVG / PNG Artifacts |                                                             |
|                       | (Paperless / Git / Obsidian) |                                                             |
|                       +------------------------------+                                                             |
|                                                                                                                    |
+--------------------------------------------------------------------------------------------------------------------+
```

## What problem it solves
Formal diagramming suites (such as Visio or complex CAD applications) suffer from steep learning curves, rigid layout constraints, and proprietary binary formats that hinder automated LLM generation. Excalidraw solves these issues by offering:

1. **Human-Approachable Aesthetic**: Hand-drawn sketchy styling reduces "polish anxiety" during early-stage brainstorming.
2. **Structured Machine-Readable JSON**: Every rectangle, arrow, text block, and connector is represented as a structured object, allowing LLMs to manipulate elements with mathematical precision.
3. **E2EE Real-Time Collaboration**: End-to-end encrypted WebSocket relays enable concurrent live editing between human engineers and automated agent bots.
4. **Deep Knowledge Base Integration**: Integrates directly into [Obsidian](../tools/ai_knowledge/obsidian.md) for visual bi-directional linking.

## Where it fits in the stack
**Category**: Services / Visual Communication & Brainstorming.

```
+---------------------------------------------------------------------------------------+
|                                    EXCALIDRAW STACK                                    |
+---------------------------------------------------------------------------------------+
| Ingestion & Protocol: FastMCP 3.1, WebSocket E2EE Sync Engine                          |
| Rendering Layer     : React Web App, Canvas Engine, Export to SVG/PNG                 |
| Schema & Storage    : Pydantic v2 JSON Spec, Local Disk, Git, Obsidian Plugin          |
| Security & Auth     : Authentik SSO, Reverse Proxy (Cloudflare / Caddy)              |
+---------------------------------------------------------------------------------------+
```

## Technical Comparison Matrix

| Feature / Dimension | Excalidraw | Draw.io | Mermaid.js |
| :--- | :--- | :--- | :--- |
| **Visual Style** | **Hand-drawn / Sketchy** | Formal / Enterprise | Code-rendered SVG |
| **Agentic Manipulability** | **High (Direct JSON Element Manipulation)** | Moderate (XML parsing) | High (Markdown text syntax) |
| **Real-time Co-Editing** | **Native E2EE WebSocket** | Cloud plugin dependent | None (Static render) |
| **Local Self-Hosting** | **Single Docker Container** | Complex web server | NPM library / CLI |
| **FastMCP 3.1 Native** | **Yes (JSON element tools)** | No | Yes (Markdown tool wrappers) |

## Typical use cases
- **Multi-Agent Architecture Whiteboarding**: Autonomous agents plotting multi-service integration diagrams for human approval.
- **UI/UX Wireframing**: Programmatically generating low-fidelity UI mockups for mobile and web applications.
- **Obsidian Visual Knowledge Mapping**: Connecting ideas and notes via spatial visual graphs using the Obsidian Excalidraw plugin.
- **System Sequence Mapping**: Translating complex execution traces into visual flowcharts during incident post-mortems.

## Strengths
- **Instant Usability**: Zero setup required for web sketching with intuitive keyboard shortcuts.
- **Bi-directional AI Co-creation**: Agents read Excalidraw JSON, make edits or add annotations, and output updated canvas files.
- **Zero Lock-in**: Raw JSON schema is open source and easy to convert into SVG, PNG, or Markdown.
- **Lightweight Footprint**: Consumes minimal system resources when running in self-hosted Docker environments.

## Limitations
- **Lacks Auto-Layout Engine**: Nodes and connectors require explicit x/y coordinates; no built-in auto-graph layouter like Graphviz or Mermaid.
- **Scale Bottlenecks**: Large canvases with tens of thousands of individual elements can suffer performance degradation in browser DOMs.
- **No Native Database Schemas**: Not designed for automated relational database schema generation without custom script adapters.

## When to use it
- When you need to quickly sketch a diagram during a meeting or brainstorming session.
- For creating approachable visuals for blog posts, documentation, or social media.
- When an agent needs a "scratchpad" to visualize its internal planning or state.
- If you use [Obsidian](../tools/ai_knowledge/obsidian.md) and want a powerful, integrated sketching solution.

## When not to use it
- For professional engineering diagrams that require strict adherence to industry standards (UML, SysML).
- When you need automatic layout of nodes and edges (use Mermaid or visual flows).
- If you require a deep hierarchy of objects or complex multi-page document management.

## FastMCP 3.1 Integration Pattern

The Python code below provides a FastMCP 3.1 tool server capable of constructing and modifying Excalidraw scenes using strict Pydantic v2 validation:

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Tool Server for Excalidraw Diagram Generation
Enables AI agents to build hand-drawn canvas diagrams programmatically.
"""

import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("excalidraw-canvas-server")

class ExcalidrawElement(BaseModel):
    id: str = Field(..., description="Unique element string identifier")
    type: str = Field(..., description="Shape type (rectangle, ellipse, arrow, text)")
    x: float = Field(..., description="X-axis coordinate on canvas")
    y: float = Field(..., description="Y-axis coordinate on canvas")
    width: float = Field(..., description="Width of the element box")
    height: float = Field(..., description="Height of the element box")
    strokeColor: str = Field("#1e1e1e", description="Border/line color hex")
    backgroundColor: str = Field("transparent", description="Fill color hex")
    fillStyle: str = Field("hachure", description="Texture (hachure, cross-hatch, solid)")
    strokeWidth: int = Field(1, ge=1, le=5, description="Line stroke thickness")
    roughness: int = Field(1, ge=0, le=3, description="Hand-drawn roughness index")
    opacity: int = Field(100, ge=0, le=100, description="Opacity percentage")
    text: Optional[str] = Field(None, description="Text string content if type == 'text'")

class ExcalidrawScene(BaseModel):
    type: str = Field("excalidraw", description="File type specifier")
    version: int = Field(2, description="Schema version")
    source: str = Field("https://excalidraw.com", description="App generator signature")
    elements: List[ExcalidrawElement] = Field(default_factory=list)

@mcp.tool()
async def create_architecture_box(
    label: str,
    x: float,
    y: float,
    width: float = 180.0,
    height: float = 70.0
) -> str:
    """
    Constructs a styled Excalidraw rectangle element with attached text label.
    """
    rect_id = f"rect_{hash(label) & 0xffffff}"
    text_id = f"text_{hash(label) & 0xffffff}"

    rect_element = ExcalidrawElement(
        id=rect_id,
        type="rectangle",
        x=x,
        y=y,
        width=width,
        height=height,
        strokeColor="#2b6cb0",
        backgroundColor="#ebf8ff",
        fillStyle="solid"
    )

    text_element = ExcalidrawElement(
        id=text_id,
        type="text",
        x=x + 15,
        y=y + 20,
        width=width - 30,
        height=30,
        strokeColor="#2d3748",
        text=label
    )

    scene = ExcalidrawScene(elements=[rect_element, text_element])
    return scene.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Getting started

### Self-Hosting via Docker Compose
To host an isolated Excalidraw instance locally:

```yaml
version: "3.8"
services:
  excalidraw:
    image: excalidraw/excalidraw:latest
    container_name: excalidraw-app
    ports:
      - "3000:80"
    restart: unless-stopped
```

Deploy using Docker Compose:
```bash
docker compose up -d
```

Access the UI at `http://localhost:3000`.

## CLI examples

### Validating Diagram JSON Files
```bash
# Validate an Excalidraw file structure using Python Pydantic CLI wrapper
python3 -c "
import json, sys
from pydantic import BaseModel

class ExcalidrawCheck(BaseModel):
    type: str
    version: int
    elements: list

with open('diagram.excalidraw', 'r') as f:
    ExcalidrawCheck.model_validate(json.load(f))
print('Diagram structure valid!')
"
```

### Inspecting Docker Logs
```bash
docker logs -f excalidraw-app
```

## API examples

### Pydantic v2 Diagram Validation Handler
```python
import json
from pydantic import BaseModel, Field, ValidationError

class DiagramHeader(BaseModel):
    version: int = Field(..., ge=1)
    type: str = Field("excalidraw")
    elements_count: int = Field(..., ge=0)

def audit_excalidraw_file(file_path: str) -> None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        summary = {
            "version": raw_data.get("version", 0),
            "type": raw_data.get("type", ""),
            "elements_count": len(raw_data.get("elements", []))
        }

        header = DiagramHeader.model_validate(summary)
        print(f"Valid Excalidraw file: {header.elements_count} elements found.")
    except ValidationError as err:
        print(f"Invalid Excalidraw structure: {err.json()}")
    except FileNotFoundError:
        print("Diagram file not found on disk.")
```

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Excellent visual canvas integration via community plugin.
- [Draw.io](drawio.md) — Enterprise diagramming solution for strict UML/ERD specs.
- [FastMCP 3.1](../tools/automation_orchestration/mcp.md) — Standardized tool execution framework.
- [Paperless-ngx](paperless-ngx.md) — Document repository for exported diagram assets.

## Sources / References
- [Excalidraw Official Web Application](https://excalidraw.com/)
- [Excalidraw GitHub Repository](https://github.com/excalidraw/excalidraw)
- [Obsidian Excalidraw Plugin Manual](https://github.com/zsviczian/obsidian-excalidraw-plugin)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
