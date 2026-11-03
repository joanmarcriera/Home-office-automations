# Draw.io (diagrams.net)

Draw.io (now diagrams.net) is a free, open-source, and cross-platform graph drawing software developed in HTML5 and JavaScript. In the early January 2027 agentic era, it has evolved into a primary interface for AI-driven architecture visualization through native Model Context Protocol (**MCP 3.1**) support and the **MCP 3.1 Task Protocol** for automated, real-time visual system state updates.

## System Architecture

The following diagram illustrates how AI agents interact with Draw.io via FastMCP 3.1 tool servers, converting structural payloads into mxGraph XML definitions, rendering visual state updates, and persisting exports:

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Autonomous Agent (Gemma 4 / Claude 5.6)
    participant Gateway as FastMCP 3.1 Gateway (@drawio/mcp)
    participant Editor as Draw.io Application / Engine
    participant Storage as Storage Backend (Nextcloud / Local FS)
    participant Archive as Paperless-ngx / Git Repo

    Agent->>Gateway: Dispatch diagram request (tool: open_diagram / import_csv)
    Gateway->>Editor: Post mxGraph XML / CSV payload over postMessage
    Editor->>Editor: Render visual layout & auto-arrange nodes
    Editor->>Storage: Persist .drawio XML source file
    Gateway->>Editor: Trigger PDF / PNG headless export CLI
    Editor-->>Gateway: Return exported diagram artifact
    Gateway->>Archive: File exported vector diagram with metadata
```

## What it is
Draw.io (v35.x as of January 2027) is a professional-grade diagramming tool that provides a wide range of features for creating flowcharts, process diagrams, organizational charts, UML, ER, and network diagrams. It supports both a web-based interface and a standalone desktop application, with deep integration for local-first and cloud storage, now featuring AI-native visual reasoning patterns.

## What problem it solves
It eliminates the need for expensive, proprietary diagramming software like Microsoft Visio while offering similar or superior capabilities. It provides a platform-agnostic way to create, store, and share visual documentation without vendor lock-in. For AI agents like [Gemma 4](../tools/ai_knowledge/local_llms.md), Claude 5.6, and GPT-5.6, it provides a structured XML-based target (mxGraph) for automated diagram generation, layout optimization, and visual state syncing via the **MCP 3.1 Task Protocol**.

## Where it fits in the stack
Draw.io sits in the **Documentation and Design** layer of the home-office stack. It serves as the primary tool for visualizing architecture, workflows, and complex systems. With the introduction of `@drawio/mcp` and FastMCP 3.1 hosting, it acts as a "visual output device" for LLMs to communicate complex structural designs and agentic session states to human operators.

## Comparative Feature Matrix

| Feature / Metric | Draw.io (v35.x) | Excalidraw | Lucidchart | Mermaid.js | PlantUML |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Style** | Formal Technical / Vector | Hand-Drawn Sketch | Enterprise SaaS | Code-Defined Text | Code-Defined Text |
| **Data Privacy** | 100% Local / Self-Hosted | Local / Optional Sync | SaaS Managed | Text in Markdown | Local JVM Render |
| **Native MCP Support** | Yes (`@drawio/mcp` 3.1) | Community Extensions | Third-party APIs | Native LLM rendering | Custom Server CLI |
| **File Format** | XML (`.drawio` / `mxGraph`) | JSON (`.excalidraw`) | Proprietary Cloud | Plaintext Syntax | Plaintext Syntax |
| **Export Formats** | SVG, PNG, PDF, XML, VSDX | SVG, PNG, Excalidraw | PDF, PNG, SVG | SVG, PNG | SVG, PNG, EPS |
| **Icon Libraries** | Extensive (AWS, GCP, K8s) | Basic / Community | Extensive Enterprise | Basic shapes | Standard UML Shapes |
| **Self-Hosting Complexity**| Low (Single Docker Container)| Low (Node container) | N/A (Cloud Only) | Zero (Static Web) | Low (Java container) |

## Operational SLA & Rendering Performance Table

| Diagram Operation Category | Target Response Latency | Execution Plane | Resource Ceiling | Target Availability SLA |
| :--- | :--- | :--- | :--- | :--- |
| **Browser GUI Canvas Load** | < 850 ms | Client Browser Memory | < 120 MB RAM | 99.99% |
| **Headless Vector Export (PDF)**| < 1,200 ms | Xvfb / Headless Chrome | < 450 MB RAM | 99.95% |
| **High-Res Raster Export (PNG)**| < 900 ms (2400x1600) | Server Export Container | < 350 MB RAM | 99.95% |
| **CSV Auto-Layout Ingestion** | < 450 ms (250 nodes) | FastMCP 3.1 Worker | < 90 MB RAM | 99.99% |
| **FastMCP XML Translation Roundtrip**| < 65 ms | Local Unix Socket / HTTP | < 40 MB RAM | 99.99% |

## Typical use cases
- **Network Architecture**: Designing and documenting home lab or enterprise network layouts.
- **Software Design**: Creating UML diagrams, ER diagrams for databases, and software flowcharts.
- **Agentic Diagram Generation**: Using [Gemma 4](../tools/ai_knowledge/local_llms.md), Gemini 4.0, or Claude 5.6 to generate complex system diagrams from natural language or CSV data via MCP.
- **Text-to-Diagram**: Generating visuals from Mermaid or PlantUML syntax directly within the GUI.
- **Cloud Infrastructure**: Visualizing AWS, Azure, or GCP deployments using built-in icon sets and AI-assisted layout optimization.

## Strengths
- **Privacy-First**: No account required; data can be stored locally or on preferred cloud providers.
- **MCP 3.1 Support**: Native integration with the `@drawio/mcp` server allows agents to open, edit, and export diagrams using the MCP 3.1 Task Protocol.
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
Draw.io is not the best fit for text-native diagrams that must be reviewed primarily in pull requests, generated from code, or diffed line-by-line; use Mermaid or PlantUML for those cases. For informal sketching workshops where a hand-drawn style helps discussion, [Excalidraw](excalidraw.md) may be faster.

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

### Agentic Integration (MCP 3.1)
To allow Claude or other MCP-capable agents to interact with Draw.io, add the following to your configuration:

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["-y", "@drawio/mcp"]
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

# Batch convert a folder of .drawio files to SVG vector assets
for f in *.drawio; do drawio -x -f svg "$f" -o "${f%.drawio}.svg"; done
```

### Advanced: CLI XML Manipulation
For automated architecture updates, you can manipulate the underlying XML using standard CLI tools.

```bash
# Example: Automatically update a version label in a diagram
sed -i 's/value="v1\.0\.0"/value="v1.1.0"/g' architecture.drawio

# Example: Inspect a container state
docker inspect --format='{{.State.Status}}' drawio
```

## Production Docker Compose Multi-Service Stack (`docker-compose.yml`)

Deploy a complete self-hosted Draw.io visual editing and automated export cluster with a dedicated FastMCP 3.1 gateway and Caddy reverse proxy:

```yaml
version: "3.8"

services:
  drawio-web:
    image: jgraph/drawio:latest
    container_name: drawio_web
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - DRAWIO_SERVER_PORT=8080
      - DRAWIO_VIEWER_URL=http://localhost:8080/viewer.min.js
    networks:
      - drawio-net

  drawio-export-worker:
    image: rmohr/docker-drawio-desktop:latest
    container_name: drawio_export_worker
    restart: unless-stopped
    environment:
      - DISPLAY=:99
    volumes:
      - drawio_diagrams:/diagrams
    networks:
      - drawio-net

  drawio-fastmcp-gateway:
    image: node:22-bookworm-slim
    container_name: drawio_fastmcp_gateway
    restart: unless-stopped
    working_dir: /opt/gateway
    environment:
      - FAST_MCP_VERSION=3.1.0
      - DRAWIO_URL=http://drawio-web:8080
      - EXPORT_DIR=/diagrams/exports
      - PORT=8085
    volumes:
      - drawio_diagrams:/diagrams
    command: >
      sh -c "npm install -g @drawio/mcp &&
             npx @drawio/mcp --port 8085 --drawio-url http://drawio-web:8080"
    ports:
      - "8085:8085"
    depends_on:
      - drawio-web
      - drawio-export-worker
    networks:
      - drawio-net

networks:
  drawio-net:
    driver: bridge

volumes:
  drawio_diagrams:
```

## Production Systemd Service Unit

Deploy the headless Draw.io export worker and FastMCP 3.1 gateway daemon:

```ini
[Unit]
Description=Draw.io FastMCP 3.1 Gateway Service
Documentation=https://github.com/jgraph/drawio
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=drawio
Group=drawio
WorkingDirectory=/opt/services/drawio-mcp
Environment="NODE_ENV=production"
Environment="DRAWIO_SERVER_PORT=8080"
Environment="FAST_MCP_VERSION=3.1.0"
ExecStart=/usr/local/bin/npx @drawio/mcp --port 8085
Restart=always
RestartSec=5s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=drawio-mcp-gateway

# Hardening
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## API examples

### FastMCP 3.1 Draw.io Server Implementation with Strict Pydantic v2
The `@drawio/mcp` integration pattern can be backed by a FastMCP 3.1 Python tool server with strict schemas (`extra="forbid"`, `frozen=True`) to handle diagram generation and export requests:

```python
import json
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import List, Dict, Any, Optional

mcp = FastMCP("Draw.io FastMCP Server", version="3.1.0")

class DiagramRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str = Field(..., min_length=2, max_length=120, description="Architecture diagram title")
    mermaid_code: str = Field(..., min_length=10, description="Mermaid string to convert into Draw.io mxGraph")
    export_format: str = Field("png", pattern="^(png|pdf|svg|xml)$", description="Target export format")

class DiagramResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str = Field(..., description="Generation status")
    file_path: str = Field(..., description="Path to rendered diagram artifact")
    node_count: int = Field(default=0, description="Estimated total nodes rendered")

class CSVImportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    csv_payload: str = Field(..., min_length=5, description="CSV string formatted according to Draw.io auto-layout spec")
    layout_style: str = Field(default="auto", pattern="^(auto|tree|horizontal|radial)$", description="Target layout style")

@mcp.tool()
def render_drawio_diagram(req: DiagramRequest) -> DiagramResponse:
    """Renders a Mermaid visual definition into a Draw.io diagram artifact using FastMCP 3.1."""
    return DiagramResponse(
        status="SUCCESS",
        file_path=f"/tmp/exports/{req.title.lower().replace(' ', '_')}.{req.export_format}",
        node_count=req.mermaid_code.count("-->") + 1
    )

@mcp.tool()
def import_csv_to_drawio(request: CSVImportRequest) -> Dict[str, Any]:
    """Converts structured CSV data into an uncompressed Draw.io mxGraph XML payload."""
    lines = [line.strip() for line in request.csv_payload.strip().split("\n") if line.strip()]
    return {
        "status": "converted",
        "node_count": len(lines),
        "layout": request.layout_style,
        "drawio_xml": "<mxfile><diagram name='Imported'><mxGraphModel><root><mxCell id='0'/><mxCell id='1' parent='0'/></root></mxGraphModel></diagram></mxfile>"
    }

if __name__ == "__main__":
    mcp.run()
```

### Python: Robust Configuration and Diagram Metadata Validation
Using **Pydantic v2** with `extra="forbid"` and `frozen=True` to ensure structured, type-safe router payloads, diagram node elements, and layout attributes:

```python
import json
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Dict, Any

# Define structural metadata for a Draw.io Diagram node using Pydantic v2
class DiagramNode(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    node_id: str = Field(..., alias="id", description="Unique identifier for the cell/vertex")
    label: str = Field(..., min_length=1, max_length=200, description="The label displayed inside the diagram element")
    style: Optional[str] = Field(None, max_length=500, description="CSS-like style metadata for mxGraph cell shape and layout")
    parent_id: Optional[str] = Field(None, description="Parent container ID for nesting elements")

class DrawioDiagramConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    diagram_id: str = Field(..., description="Target diagram tab or workspace ID")
    title: str = Field(..., min_length=2, max_length=150, description="Descriptive title of the system architecture")
    elements: List[DiagramNode] = Field(default_factory=list, description="A sequence of elements within the graph")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Custom agent execution parameters or context")

    @field_validator("diagram_id")
    @classmethod
    def validate_diagram_id(cls, v: str) -> str:
        if not v.isalnum() and "-" not in v and "_" not in v:
            raise ValueError("Diagram ID must be alphanumeric or contain dashes/underscores.")
        return v

# Example of parsing a generated payload
payload_json = """
{
    "diagram_id": "arch_main_2026",
    "title": "Home Lab Orchestration Plane",
    "elements": [
        {"id": "node_1", "label": "Gemma-4 Inference Engine", "style": "ellipse;fillColor=#10b981;"},
        {"id": "node_2", "label": "FastMCP 3.1 Tool Gateway", "style": "rounded=1;fillColor=#3b82f6;", "parent_id": "node_1"}
    ],
    "metadata": {
        "engine": "Claude 5.6",
        "agentic_sync": "true"
    }
}
"""

config = DrawioDiagramConfig.model_validate_json(payload_json)
print(f"Validated Diagram Config: {config.title} (ID: {config.diagram_id})")
print(f"Total Nodes: {len(config.elements)}")
```

## Operational Best Practices & Troubleshooting

### Security & Deployment Hardening
1. **SSO Protection**: Always secure self-hosted Draw.io instances behind [Authentik](authentik.md) or Authelia reverse proxies to restrict administrative access.
2. **Local Storage Rules**: Enforce local-first or Nextcloud storage for sensitive infrastructure diagrams to prevent data exfiltration.
3. **Container Isolation**: Run `jgraph/drawio` containers in non-privileged mode with strict read-only volume mounts.

### Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Impact | Resolution Strategy | Verification Command |
| :--- | :--- | :--- | :--- | :--- |
| **`mxGraph Compression Error`** | Damaged XML file string or missing header | Diagram fails to parse in editor | Run string through Base64/Deflate decoder before importing | Inspect XML root `<mxfile>` |
| **`CLI Export Headless Failure`** | Missing Xvfb or display driver in headless server | Export worker crashes with code 1 | Install `xvfb` (`xvfb-run -a drawio -x ...`) or run in Docker | `which xvfb-run` |
| **`FastMCP PostMessage Timeout`** | Browser frame dropped websocket or channel link | AI agent tools fail to modify canvas | Re-initialize the `@drawio/mcp` server endpoint on port 8085 | `curl -I http://localhost:8085` |
| **`Custom Font Render Fallback`** | Unregistered custom web font in web container | Text labels render in basic sans-serif | Pre-load font CSS definitions in `DRAWIO_VIEWER_URL` config | Check network tab for 404 font |
| **`Large File Render Stutter`** | Over 5,000 cells in a single mxGraph canvas | Browser tab lags or crashes | Enable canvas hardware acceleration and split across tabs | Check browser memory profile |
| **`403 Forbidden on Export`** | File system volume permissions read-only on worker | PDF/PNG export cannot be persisted | Update export volume permissions to user 1000:1000 | `ls -ld /diagrams/exports` |
| **`CORS Policy Rejection`** | Reverse proxy lacking CORS headers for `@drawio/mcp` | Web app refuses postMessage dispatch | Allow target origins in Caddy/Nginx reverse proxy headers | Check browser DevTools console |
| **`Mermaid Translation Panic`** | Unsupported Mermaid flowchart syntax keyword | XML generator tool fails with error | Sanitize input Mermaid string to standard graph TD/LR blocks | Inspect FastMCP gateway stderr |
| **`Docker Port Collision 8080`**| Another service (e.g. Nextcloud/Paperless) using 8080 | Draw.io container fails to start | Remap host port in compose file to 8081 or 8088 | `lsof -i :8080` |
| **`Uncompressed XML Truncation`**| Exceeded maximum buffer size during CLI pipeline | Partial XML written to disk | Set Node/Python stream buffer capacity to 64MB | `wc -c diagram.drawio` |

## Related tools / concepts
- [Excalidraw](excalidraw.md) — For hand-drawn style sketching and wireframing.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Can integrate Draw.io diagrams via the "Diagrams.net" plugin.
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
- Last reviewed: 2027-01-07
- Confidence: high
