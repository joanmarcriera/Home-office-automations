# Draw.io (diagrams.net)

Draw.io (now diagrams.net) is a free, open-source, and cross-platform graph drawing software developed in HTML5 and JavaScript. In the late October / November 2026 agentic era, it has evolved into a primary interface for AI-driven architecture visualization through native Model Context Protocol (MCP 3.1) support, FastMCP 3.1 setups, and the MCP 3.1 Task Protocol for automated execution of visual changes.

## What it is
Draw.io (v32.2.x as of late 2026) is a professional-grade diagramming tool that provides a wide range of features for creating flowcharts, process diagrams, organizational charts, UML, ER, and network diagrams. It supports both a web-based interface and a standalone desktop application, with deep integration for local-first and cloud storage, now featuring AI-native visual reasoning patterns and advanced state-machine rendering.

## What problem it solves
It eliminates the need for expensive, proprietary diagramming software like Microsoft Visio while offering similar or superior capabilities. It provides a platform-agnostic way to create, store, and share visual documentation without vendor lock-in. For frontier AI models like [Claude 5.1](../tools/ai_knowledge/claude.md), GPT-5.5, and Gemini 4.0, it provides a structured XML-based target (mxGraph) for automated diagram generation and manipulation via the MCP 3.1 Task Protocol.

## Where it fits in the stack
Draw.io sits in the **Documentation and Design** layer of the home-office stack. It serves as the primary tool for visualizing architecture, workflows, and complex systems. With the introduction of `@drawio/mcp` and FastMCP 3.1 hosting, it now acts as a "visual output device" for LLMs to communicate complex structural designs and agentic session states to human operators.

## Typical use cases
- **Network Architecture**: Designing and documenting home lab or enterprise network layouts.
- **Software Design**: Creating UML diagrams, ER diagrams for databases, and software flowcharts.
- **Agentic Diagram Generation**: Using Claude 5.1, GPT-5.5, or Gemini 4.0 to generate complex system diagrams from natural language or CSV data via MCP 3.1.
- **Text-to-Diagram**: Generating visuals from [Mermaid](../knowledge_base/patterns/diagramming.md) or PlantUML syntax directly within the GUI.
- **Cloud Infrastructure**: Visualizing AWS, Azure, or GCP deployments using built-in icon sets and AI-assisted layout optimization.

## Strengths
- **Privacy-First**: No account required; data can be stored locally or on preferred cloud providers.
- **MCP 3.1 / FastMCP 3.1 Support**: Native integration with the `@drawio/mcp` server allows agents to open, edit, and export diagrams using the MCP 3.1 Task Protocol and high-fidelity structured schemas.
- **Extensive Library**: Huge collection of icons for networking, cloud, UI design, and more.
- **Highly Compatible**: Can import/export Visio (.vsdx), Lucidchart, and other formats.
- **Cross-Platform**: Available as a web app, desktop app, and can be self-hosted via Docker.

## Limitations
- **Collaboration**: Real-time collaboration in the self-hosted version is more complex to set up than the SaaS version.
- **UI Density**: The interface can be intimidating for users who only need simple sketching tools (consider [Excalidraw](excalidraw.md) for those cases).
- **XML Complexity**: While the `.drawio` format is XML-based, it uses a compressed `mxGraph` format that requires specific decoding for direct text-based manipulation.

## When to use it
- When you need to create formal, technical diagrams (UML, Network, Cloud Architecture).
- When you want a professional Visio alternative that works across Windows, macOS, and Linux.
- When you need to export diagrams to multiple formats (PDF, PNG, SVG, XML) for documentation.
- When orchestrating automated architecture updates via AI agents using MCP 3.1.

## When not to use it
Draw.io is not the best fit for text-native diagrams that must be reviewed primarily in pull requests, generated from code, or diffed line-by-line; use [Mermaid](../knowledge_base/patterns/diagramming.md) or PlantUML for those cases. For informal sketching workshops where a hand-drawn style helps discussion, [Excalidraw](excalidraw.md) may be faster.

## Getting started

### Docker (Self-Hosted)
To run a private instance of Draw.io using Docker:

```bash
docker run -d --name="drawio" -p 8080:8080 -p 8443:8443 jgraph/drawio
```

Access your instance at `http://localhost:8080`.

### TrueNAS Deployment
To host Draw.io on TrueNAS SCALE:
1. **Create a Dataset**: Create a dataset for optional persistence (e.g., `/mnt/pool/apps/drawio`).
2. **Custom App**:
   - **Image**: `jgraph/drawio:latest`
   - **Ports**: Map a host port (e.g., 30081) to 8080.
3. **Environment**: Optionally configure `DRAWIO_VIEWER_URL` if hosting a custom viewer.

### Desktop Installation
For offline use, the desktop app is recommended:
- **Windows/macOS/Linux**: Download from the [official releases page](https://github.com/jgraph/drawio-desktop/releases).

### Agentic Integration (MCP 3.1 / FastMCP 3.1)
To allow Claude or other MCP-capable agents to interact with Draw.io, add the following to your configuration:

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["-y", "@drawio/mcp@3.1.0"]
    }
  }
}
```

## CLI examples

### Desktop CLI
The Draw.io Desktop app includes a CLI for batch processing and conversion:

```bash
cat > sample.drawio <<'XML'
<mxfile><diagram name="Page-1"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel></diagram></mxfile>
XML

# Export a diagram to PDF via CLI (Desktop app required)
drawio -x -f pdf -o sample.pdf sample.drawio

# Export to PNG with a specific width
drawio -x -f png --width 1200 -o sample.png sample.drawio
```

### Advanced: CLI XML Manipulation
For automated architecture updates, you can manipulate the underlying XML using standard CLI tools.

```bash
# Example: Automatically update a version label in a diagram
sed -i 's/value="v1\.0\.0"/value="v1.1.0"/g' architecture.drawio

# Example: Inspect a container state
docker inspect --format='{{.State.Status}}' drawio
```

## API examples

### MCP Tool Usage (Gemini 4.0 / Claude 5.1)
The `@drawio/mcp` server provides tools that agents can call via the MCP 3.1 Task Protocol:

- `open_diagram`: Opens a `.drawio` file or XML string in the editor.
- `import_csv`: Converts CSV data (e.g., an org chart) into a diagram.
- `render_mermaid`: Converts Mermaid syntax into an editable Draw.io graph.

### Programmatic Python Parsing with Pydantic v2
For advanced workflows, developers can use Pydantic v2 to parse, modify, and validate diagram structures before exporting them to `.drawio` files.

```python
import xml.etree.ElementTree as ET
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class MXCell(BaseModel):
    """Represents a single cell element inside an mxGraphModel."""
    id: str = Field(..., description="Unique cell identifier")
    value: Optional[str] = Field(None, description="The text or label of the cell")
    parent: Optional[str] = Field(None, description="Parent cell ID")
    vertex: Optional[str] = Field(None, description="Vertex indicator ('1' if vertex)")
    edge: Optional[str] = Field(None, description="Edge indicator ('1' if edge)")
    source: Optional[str] = Field(None, description="Source node ID for edges")
    target: Optional[str] = Field(None, description="Target node ID for edges")

class Diagram(BaseModel):
    """Represents an individual diagram sheet in Draw.io."""
    id: str = Field(..., description="Unique diagram sheet identifier")
    name: str = Field(..., description="Sheet name")
    cells: List[MXCell] = Field(default_factory=list, description="List of all nodes and edges")

class DrawioFile(BaseModel):
    """Validates the root structure of a Draw.io diagram file."""
    agent: Optional[str] = Field("Claude 5.1", description="AI Agent performing validation")
    diagrams: List[Diagram] = Field(..., description="List of diagram sheets")

    @field_validator("diagrams")
    @classmethod
    def validate_diagram_sheets(cls, v: List[Diagram]) -> List[Diagram]:
        if not v:
            raise ValueError("A valid Draw.io document must contain at least one diagram sheet.")
        return v

def parse_and_validate_drawio(xml_str: str, agent_name: str = "Claude 5.1") -> DrawioFile:
    """Parses draw.io raw xml and validates model compliance."""
    root_el = ET.fromstring(xml_str)
    diagrams_list = []

    for diag in root_el.findall(".//diagram"):
        diag_id = diag.get("id", "default-id")
        diag_name = diag.get("name", "Page-1")

        cells_list = []
        for cell in diag.findall(".//mxCell"):
            cells_list.append(MXCell(
                id=cell.get("id"),
                value=cell.get("value"),
                parent=cell.get("parent"),
                vertex=cell.get("vertex"),
                edge=cell.get("edge"),
                source=cell.get("source"),
                target=cell.get("target")
            ))
        diagrams_list.append(Diagram(id=diag_id, name=diag_name, cells=cells_list))

    return DrawioFile(agent=agent_name, diagrams=diagrams_list)

# Test XML structure with FastMCP 3.1 context
raw_xml_payload = """
<mxfile agent="Claude 5.1">
  <diagram id="sheet-1" name="Home Lab Topology">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="server-host" value="Tailscale Gateway" parent="1" vertex="1" />
        <mxCell id="server-db" value="PostgreSQL" parent="1" vertex="1" />
        <mxCell id="con-1" source="server-host" target="server-db" edge="1" parent="1" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

# Execute parsing & validation
validated_diagram = parse_and_validate_drawio(raw_xml_payload)
print(f"Validated by agent: {validated_diagram.agent}")
for sheet in validated_diagram.diagrams:
    print(f"Sheet Name: '{sheet.name}' (Contains {len(sheet.cells)} elements)")
```

### JSON Protocol
When embedding, you can send actions via `postMessage`:

```javascript
const iframe = document.getElementById('drawio-iframe');
iframe.contentWindow.postMessage(JSON.stringify({
  action: 'load',
  xml: '<mxfile><diagram name="Page-1"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel></diagram></mxfile>'
}), '*');
```

## Related tools / concepts
- [Excalidraw](excalidraw.md) — For hand-drawn style sketching and wireframing.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Can integrate Draw.io diagrams via the "Diagrams.net" plugin.
- [Mermaid](../knowledge_base/patterns/diagramming.md) — Text-based diagramming alternative for version control.
- [Gitea](gitea.md) — Recommended for version-controlling `.drawio` XML files.
- [Nextcloud](nextcloud.md) — Self-hosted storage backend for diagram synchronization.
- [Paperless-ngx](paperless-ngx.md) — For archiving exported diagram PDFs with searchable metadata.
- [Authentik](authentik.md) — For securing the self-hosted Draw.io interface.
- [Tailscale](tailscale.md) — For secure remote access to your self-hosted instance.
- [Trilium](trilium.md) — For embedding diagrams into a hierarchical personal knowledge base.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for agentic tool use and integration.

## Sources / references
- [Official Website](https://www.draw.io/)
- [GitHub Repository](https://github.com/jgraph/drawio)
- [draw.io MCP Server](https://www.npmjs.com/package/@drawio/mcp)
- [Docker Hub - jgraph/drawio](https://hub.docker.com/r/jgraph/drawio)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
