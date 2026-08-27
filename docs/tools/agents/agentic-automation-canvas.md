# Agentic Automation Canvas (AAC)

## What it is
The Agentic Automation Canvas (AAC) is a structured framework and open-source tool for the prospective design, governance, and evaluation of agentic AI systems. It provides a machine-readable "project contract" that bridges the gap between high-level user expectations and technical implementation. As of early January 2027, it serves as the industry standard (v1.3+) for planning high-fidelity reasoning workflows for **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **Gemma 4**, incorporating the latest **FastMCP 3.1 visual design patterns** and multi-agent coordination topologies.

## What problem it solves
It addresses the **Expectation-Realisation Gap**: the systemic discrepancy where users expect high productivity gains from AI (e.g., 24% speedup) but often experience a decrease (e.g., 19% slowdown) due to unmeasured verification burdens, workflow friction, and human oversight costs. AAC requires explicit quantification of these factors during the planning phase to ensure ROI for autonomous engineering projects. It also standardizes the visual representation of [Model Context Protocol (MCP 3.1)](../../knowledge_base/patterns/tool-calling-and-mcp.md) tool graphs and multi-model agent contracts.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as a **Planning & Design Framework** that precedes and guides implementation. It acts as the blueprint for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **Full Project Planning**: Designing end-to-end agentic workflows, including complex components like **deterministic schedulers**, **speculative decoding routers**, and **LLM routers**.
- **Governance & Compliance**: Documenting data access, sensitivity, and staging for institutional or clinical AI deployments.
- **AI Coding Integration**: Generating implementation-ready instructions for AI coding assistants like [Claude Code](../development_ops/claude-code.md) and [Jules](../ai_knowledge/jules.md).
- **Visual MCP Orchestration**: Mapping out [MCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) server connections and tool dependency graphs using standardized visual nodes.

## Strengths
- **Six-Dimensional Framework**: Covers Scope, User Expectations, Feasibility, Governance, Data Access, and Outcomes.
- **MCP 3.1 & FastMCP Native**: Built-in support for mapping the **MCP 3.1 / FastMCP 3.1 Task Protocol** and visual design patterns for tool discovery.
- **RO-Crate Export**: Generates FAIR-compliant, machine-interoperable metadata packages following W3C and Schema.org standards.
- **AI-Ready Output**: Automatically generates an `AGENTS.md` file that translates the project specification into structured instructions for tools like [Cursor](../development_ops/cursor.md) or [Aider](../development_ops/aider.md).
- **Privacy-First**: Fully client-side web application with real-time validation; data never leaves the browser.

## Limitations
- **Evolving Standard**: Currently in version 1.3.1; while highly stable for production planning, the core schema continues to evolve with the MCP and FastMCP standards.
- **Human Input Required**: The quality of the output depends on the accuracy of the user's benefit quantification and feasibility assessments.
- **Visual Complexity**: Large-scale multi-agent systems can lead to complex "node spaghetti" if not properly modularized into sub-canvases.

## When to use it
- Before starting the development of a new agentic system to ensure alignment between users and developers.
- When you need to justify the ROI of an AI automation project by factoring in human-in-the-loop costs.
- For complex projects requiring cross-backend model coordination (e.g., GPT-5.6 for orchestration, Claude 5.6 for technical execution, and [Gemma 4](../ai_knowledge/local_llms.md) / [Qwen 3.6](../ai_knowledge/local_llms.md) for local processing).

## When not to use it
- For trivial, single-prompt AI tasks that do not require tool-calling or multi-step reasoning.
- When a project's goals and constraints are already fully documented in a compatible machine-readable format.

## Getting started
### Online Access
Access the live version of the canvas at [aac.slolab.ai](https://aac.slolab.ai/). No installation is required as it is a client-side web application.

### Basic Workflow
1. **Define Scope**: Enter the primary goals and constraints of your agentic project.
2. **Design Visual Flow**: Map your agents and tools using [MCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) visual nodes.
3. **Quantify Benefits**: Input expected productivity gains and human verification costs.
4. **Export Metadata**: Save your project as an `AGENTS.md` file or an RO-Crate package for interoperability.

## CLI examples
```bash
# AAC is a web-based Vue.js tool, no direct CLI for canvas creation.
# However, the exported RO-Crate can be validated via:
rocrate validate ./exported-crate/

# To self-host the AAC application locally (requires Node.js 22+):
git clone https://github.com/slolab/agentic-automation-canvas.git
cd agentic-automation-canvas
npm install && npm run dev
```

## API examples

### Schema of the RO-Crate Project Contract
The visual nodes and core schema exported by the Agentic Automation Canvas are validated via a machine-readable JSON-LD structure conforming to the following profile.

```json
{
  "@context": "https://w3id.org/ro/crate/1.1/context",
  "@graph": [
    {
      "@id": "./",
      "@type": "Dataset",
      "name": "My Agentic Project",
      "description": "An automated workflow for document synthesis using Claude 5.6",
      "hasPart": [
        { "@id": "AGENTS.md" }
      ],
      "conformsTo": { "@id": "https://aac.slolab.ai/schema/v1.3.0" }
    },
    {
      "@id": "AGENTS.md",
      "@type": "File",
      "about": "Project implementation contract"
    }
  ]
}
```

### Scripted RO-Crate Metadata Validator (Python & Pydantic v2)
To automate compliance audits for agent projects, developers use Pydantic v2 to validate exported project contracts before executing deployment routines on Kubernetes or local engines:

```python
from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class ROContext(BaseModel):
    id: str = Field(..., alias="@id")
    type: str = Field(..., alias="@type")
    name: str
    description: str
    hasPart: List[Dict[str, str]] = Field(default_factory=list)
    conformsTo: Dict[str, str]

class AACProjectContract(BaseModel):
    schema_version: Literal["1.2.4", "1.3.0", "1.3.1"] = Field("1.3.1")
    canvas_title: str = Field(..., min_length=3)
    target_models: List[str] = Field(..., description="E.g., Claude 5.6, GPT-5.6, Gemini 4.0 Ultra")
    expected_speedup: float = Field(..., ge=-100.0, le=500.0, description="Productivity delta percentage")
    verification_overhead: float = Field(..., ge=0.0, le=100.0, description="Manual audit time percentage required")
    mcp_servers_mapped: List[str] = Field(default_factory=list)
    exported_at: datetime = Field(default_factory=datetime.utcnow)

# Example parsing and auditing an exported canvas specification
sample_contract_payload = {
    "schema_version": "1.3.1",
    "canvas_title": "Enterprise RAG Audit Pipeline",
    "target_models": ["Claude 5.6", "GPT-5.6", "Gemini 4.0 Ultra"],
    "expected_speedup": 45.0,
    "verification_overhead": 8.5,
    "mcp_servers_mapped": [
        "https://github.com/modelcontextprotocol/servers/tree/main/src/postgres",
        "https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive"
    ]
}

contract = AACProjectContract(**sample_contract_payload)
print(f"Validated Contract: '{contract.canvas_title}' under Schema v{contract.schema_version}")
print(f"Primary Target: {contract.target_models[0]}")
print(f"Net expected gain: {contract.expected_speedup - contract.verification_overhead}%")
```

## Related tools / concepts
- [AGENTS.md Pattern](../../knowledge_base/patterns/index.md)
- [Claude Code](../development_ops/claude-code.md)
- [Jules](../ai_knowledge/jules.md)
- [Cursor](../development_ops/cursor.md)
- [Aider](../development_ops/aider.md)
- [RO-Crate Standard](https://www.researchobject.org/ro-crate/)
- [Symphony](symphony.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Model Context Protocol (MCP 3.1)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Standards](../../standards.md)

## Sources / references
- [Official Website](https://aac.slolab.ai/)
- [GitHub Repository](https://github.com/slolab/agentic-automation-canvas)
- [The Agentic Automation Canvas: a structured framework for agentic AI project design (arXiv:2602.15090)](https://arxiv.org/abs/2602.15090)
- [Quantifying the Expectation-Realisation Gap for Agentic AI Systems (arXiv:2602.20292)](https://arxiv.org/abs/2602.20292)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
