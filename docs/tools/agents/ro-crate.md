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
uv add rocrate
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

### 2. FastMCP 3.1 & Pydantic v2 RO-Crate Contract Validation
The following Python script demonstrates how an AI agent validates an RO-Crate manifest payload using Pydantic v2 and FastMCP 3.1 standards in early January 2027:

```python
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Any, Optional
import json

class CrateEntity(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(..., alias="@type")
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

class ROCrateMetadataManifest(BaseModel):
    context: str = Field("https://w3id.org/ro/crate/1.1/context", alias="@context")
    graph: List[Dict[str, Any]] = Field(..., alias="@graph", min_length=2)

def validate_rocrate_manifest(manifest_payload: dict) -> str:
    """Validates RO-Crate JSON-LD manifest structure using Pydantic v2."""
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

if __name__ == "__main__":
    sample_manifest = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {"@id": "ro-crate-metadata.json", "@type": ["CreativeWork"], "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}},
            {"@id": "./", "@type": ["Dataset"], "name": "Agentic Execution Crate", "description": "Automated task output"}
        ]
    }
    print(validate_rocrate_manifest(sample_manifest))
```

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
