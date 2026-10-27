# RO-Crate Standard

## What it is
**RO-Crate (Research Object Crate)** is an open, community-driven specification for packaging research metadata, digital datasets, code, workflow definitions, and computational execution environments into standardized, machine-readable archives. Built on top of **JSON-LD 1.1** and **Schema.org**, RO-Crate provides a lightweight structure (`ro-crate-metadata.json`) alongside dataset files to ensure long-term reproducibility, data provenance, and automated discovery.

In frontier AI and multi-agent systems (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**), RO-Crate serves as a standardized packaging format for agentic workflows, dataset ingestion, scientific copilots, and FastMCP 3.1 task execution artifacts.

```
+-----------------------------------------------------------------------------------+
|                              RO-CRATE METADATA ENGINE                             |
|                                                                                   |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |  JSON-LD 1.1 Schema    |  |  File & Context Graph  |  |  Provenance &       |  |
|  |  Manifest Generator    |  |  Parser / Validator    |  |  Author Metadata    |  |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |  FastMCP 3.1 Task      |  |  Pydantic v2 Contract  |  |  ZIP / BagIt        |  |
|  |  Artifact Packaging    |  |  Validation Engine     |  |  Archive Container  |  |
|  +------------------------+  +------------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                             STANDARDIZED RESEARCH CRATE                           |
|      (ro-crate-metadata.json, Data Files, Workflows, Execution Logs, Provenance)  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Research datasets and agentic execution logs are frequently published without adequate metadata, precise tool versioning, or provenance tracing, making reproducible execution nearly impossible. RO-Crate establishes a unified packaging standard that bridges human-readable documentation (`RO-Crate-preview.html`) with machine-readable semantic graphs (`ro-crate-metadata.json`).

For AI agents (such as those configured in the [Agentic Automation Canvas](agentic-automation-canvas.md)), RO-Crate enables autonomous tools to export complete experiment packages—containing input datasets, code scripts, intermediate reasoning steps, model parameters, and output artifacts—that can be parsed, verified, and re-executed across cloud and edge platforms.

## Where it fits in the stack
**Agents / Metadata & Data Exchange Layer**. RO-Crate acts as the standardized data interchange format between autonomous agent tools, research repositories (e.g., Zenodo, Figshare), data lakehouse storage, and scientific workflow management systems.

## RO-Crate Packaging & Agent Ingestion Flow

```
[Agent / Workflow Engine]          [RO-Crate Generator]             [Target Storage / Repo]
           |                                |                                 |
           | 1. Execute Multi-Step Task     |                                 |
           | 2. Collect Artifacts & Logs    |                                 |
           |------------------------------->|                                 |
           |                                | 3. Build JSON-LD Context Graph  |
           |                                | 4. Generate ro-crate-metadata   |
           |                                | 5. Package ZIP Container        |
           |                                |                                 |
           | 6. Return RO-Crate Package     |<--------------------------------|
           |----------------------------------------------------------------->|
           |                                | 7. Publish to Repository        |
```

## Data Packaging Standard Comparison Matrix

| Feature / Dimension | RO-Crate Standard | Frictionless Data Package | BagIt Container | Fairsharing Ontology |
| :--- | :--- | :--- | :--- | :--- |
| **Metadata Format** | JSON-LD 1.1 / Schema.org| JSON Schema | Plain Key-Value Text | RDF / OWL Ontologies |
| **Semantic Linked Data**| Native (URIs / Context)| Limited | None | Full |
| **Human Preview** | Auto HTML rendering | Via third-party tools | None | Web portals |
| **Workflow Provenance** | Native Workflow Profile | Basic file descriptions | File checksums | Domain-specific |
| **Agentic Tool Interop**| High (FastMCP / Pydantic)| Medium | Low (Filesystem only) | Medium |

## Typical use cases
- **Agentic Experiment Checkpointing**: Exporting multi-step data science experiments (code, prompt logs, generated plots, and datasets) into reproducible packages.
- **Scientific AI Copilot Ingestion**: Reading external research archives and extracting structured dataset entities, authors, and citation graphs automatically.
- **Fair Data Governance**: Enforcing FAIR (Findable, Accessible, Interoperable, Reusable) data principles across enterprise knowledge bases and agent memory stores.
- **Cross-Platform Workflow Exchange**: Transferring workflow execution graphs between Galaxy, Nextflow, Snakemake, and FastMCP servers.

## Strengths
- **Linked Data Standard**: Built on JSON-LD 1.1, allowing global semantic interoperability without inventing custom metadata formats.
- **Human & Machine Friendly**: Combines structured JSON-LD with optional self-contained HTML preview pages.
- **Extensible Profiles**: Supports specialized domain profiles (e.g., Workflow RO-Crate, Process Run RO-Crate) tailored for scientific computing.
- **Tooling Support**: Broad ecosystem support across Python, JavaScript, R, and Java libraries (`rocrate-py`).

## Limitations
- **JSON-LD Complexity**: Understanding deep linked-data context graphs requires familiarity with Semantic Web standards.
- **Schema Overhead**: Writing comprehensive metadata manifests by hand can be verbose without helper SDKs.

## When to use it
- When packaging complex datasets, workflow execution outputs, or agentic reasoning traces for long-term archival.
- When sharing scientific experiments across heterogeneous platforms and institutions.
- When building AI agents that publish or consume FAIR-compliant data artifacts.

## When not to use it
- For ephemeral, ultra-low-latency microservice RPC calls where lightweight JSON or Protocol Buffers are sufficient.
- For simple single-file text storage where linked metadata adds unnecessary overhead.

## Getting started

### 1. Installation
Install the official Python RO-Crate library (`rocrate`):
```bash
uv add rocrate pydantic fastmcp
```

### 2. Creating an RO-Crate Package in Python
```python
from rocrate.rocrate import ROCrate

crate = ROCrate()
crate.name = "Agentic Data Analysis Experiment"
crate.description = "Automated exploratory data analysis package generated by Claude 5.6"

# Add dataset file
sample_file = crate.add_file("dataset.csv", properties={
    "name": "Raw Survey Data",
    "encodingFormat": "text/csv"
})

# Write Crate directory
crate.write("my_rocrate_dir")
```

## CLI examples

### 1. Validate an RO-Crate Directory
Validate structure using the Python CLI:
```bash
rocrate validate my_rocrate_dir/
```

### 2. Export RO-Crate Directory to ZIP
```bash
rocrate zip my_rocrate_dir/ -o experiment_crate.zip
```

### 3. Inspect RO-Crate Metadata Context Graph
```bash
python3 -m json.tool my_rocrate_dir/ro-crate-metadata.json | head -n 30
```

## API examples

### 1. Adding Provenance Metadata to an RO-Crate
```python
from rocrate.rocrate import ROCrate

crate = ROCrate()

# Define Author Person Entity
author = crate.add_person("#agent-1", {
    "name": "Data Copilot Agent",
    "affiliation": "Autonomous Systems Lab"
})

# Add Executable Script
script = crate.add_file("analysis.py", properties={
    "name": "Data Analysis Script",
    "programmingLanguage": "Python",
    "author": author
})

crate.write_zip("agent_experiment.crate.zip")
```

### 2. FastMCP 3.1 & Pydantic v2 RO-Crate Contract Validation Server
The following Python script implements a complete FastMCP 3.1 server with Pydantic v2 schema validation for packaging and inspecting RO-Crate research objects:

```python
import json
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl
from fastmcp import FastMCP

mcp = FastMCP("RO-Crate Packaging & Semantic Validation Server")

class CrateEntity(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(..., alias="@type")
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

class ROCrateMetadataManifest(BaseModel):
    context: str = Field("https://w3id.org/ro/crate/1.1/context", alias="@context")
    graph: List[Dict[str, Any]] = Field(..., alias="@graph", min_length=2)

class PackageCrateRequest(BaseModel):
    crate_name: str = Field(..., description="Name of the research crate")
    description: str = Field(..., description="Description of research artifacts")
    dataset_paths: List[str] = Field(..., description="List of dataset file paths")
    agent_id: str = Field("agent-claude-5-6", description="Identifier of generating AI agent")

@mcp.tool()
def validate_rocrate_manifest(manifest_payload: dict) -> str:
    """Validates RO-Crate JSON-LD manifest structure using Pydantic v2 models."""
    try:
        manifest = ROCrateMetadataManifest.model_validate(manifest_payload)
        root_entity = next((e for e in manifest.graph if e.get("@id") == "./"), None)
        return json.dumps({
            "status": "success",
            "root_id": root_entity.get("@id") if root_entity else None,
            "entity_count": len(manifest.graph)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

@mcp.tool()
def build_agentic_rocrate(request: PackageCrateRequest) -> str:
    """Creates a standardized RO-Crate package directory and metadata graph."""
    try:
        graph = [
            {
                "@id": "ro-crate-metadata.json",
                "@type": ["CreativeWork"],
                "about": {"@id": "./"},
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}
            },
            {
                "@id": "./",
                "@type": ["Dataset"],
                "name": request.crate_name,
                "description": request.description,
                "creator": {"@id": f"#{request.agent_id}"}
            },
            {
                "@id": f"#{request.agent_id}",
                "@type": ["SoftwareApplication"],
                "name": f"Autonomous AI Agent ({request.agent_id})"
            }
        ]

        for path in request.dataset_paths:
            file_name = Path(path).name
            graph.append({
                "@id": file_name,
                "@type": ["File"],
                "name": file_name
            })

        manifest = {"@context": "https://w3id.org/ro/crate/1.1/context", "@graph": graph}
        validated = ROCrateMetadataManifest.model_validate(manifest)

        return json.dumps({
            "status": "created",
            "manifest": validated.model_dump(by_alias=True)
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Deployment & Containerization

### Docker Compose Service Setup
Deploy an automated RO-Crate packaging and validation microservice alongside a local MinIO object store for crate distribution:

```yaml
version: "3.8"

services:
  rocrate-server:
    image: python:3.12-slim
    container_name: rocrate-server
    working_dir: /app
    volumes:
      - ./:/app
      - /var/crates:/data/crates
    environment:
      - PYTHONUNBUFFERED=1
      - CRATE_STORAGE_PATH=/data/crates
    command: >
      bash -c "pip install rocrate pydantic fastmcp &&
               python3 rocrate_server.py"
    ports:
      - "8095:8095"
    restart: unless-stopped

  minio:
    image: minio/minio:RELEASE.2025-01-01T00-00-00Z
    container_name: crate-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadminpassword
    command: server /data --console-address ":9001"
    restart: unless-stopped
```

### Systemd Daemon Setup (`/etc/systemd/system/ro-crate-packager.service`)
Configure a dedicated background service for automated research crate aggregation:

```ini
[Unit]
Description=RO-Crate Packaging and Metadata Microservice
After=network.target minio.service
Wants=minio.service

[Service]
Type=simple
User=rocrate
Group=rocrate
WorkingDirectory=/opt/rocrate-service
ExecStart=/usr/bin/python3 /opt/rocrate-service/rocrate_server.py
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=CRATE_STORAGE_PATH=/var/lib/rocrate/crates

# Security Hardening
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Failure Mode | Root Cause Analysis | Corrective Resolution Strategy |
| :--- | :--- | :--- |
| **JSON-LD Context Expansion Error** | Missing or inaccessible `@context` URI (`https://w3id.org/ro/crate/1.1/context`). | Verify outbound internet connectivity or cache local context JSON file. |
| **Missing Root Dataset Entity** | `@graph` array does not contain an entity with `@id: "./"`. | Ensure the manifest builder explicitly initializes the `./` root Dataset block. |
| **Schema Validation Failure** | Non-standard entity types or missing required properties in `ro-crate-metadata.json`. | Pass raw JSON manifest payloads through `ROCrateMetadataManifest.model_validate()`. |
| **File Checksum Mismatch** | Data files altered after `ro-crate-metadata.json` checksum generation. | Re-run `rocrate zip` or regenerate SHA-256 hashes for updated entity nodes. |

## Production Operational Best Practices

### 1. Automatic Schema Validation
Run `rocrate-validator` checks in continuous integration pipelines to guarantee generated crates strictly conform to official RO-Crate 1.1 specifications.

### 2. Permanent Identifier Resolution
Use persistent URIs (DOIs, ORCIDs, W3ID URIs) within `@id` attributes for external persons, organizations, and ontologies to prevent link rot.

### 3. ZIP Archive Compression
Always distribute production crates as self-contained `.crate.zip` archives with embedded checksums for atomic download and integrity verification.

## Related tools / concepts
- [Agentic Automation Canvas](agentic-automation-canvas.md) — Agent architecture blueprint using RO-Crate.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Protocol for transferring agent task artifacts.
- [FastMCP](../frameworks/fastmcp.md) — Framework for building agent tool servers.
- [Pydantic](../frameworks/pydantic.md) — Schema validation engine for metadata payload parsing.

## Sources / references
- [RO-Crate Specification 1.1](https://www.researchobject.org/ro-crate/1.1/)
- [RO-Crate Python Library GitHub](https://github.com/ResearchObject/ro-crate-py)
- [W3ID Research Object Community](https://www.researchobject.org/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
