# Agentic Automation Canvas (AAC)

## What it is
The Agentic Automation Canvas (AAC) is a structured framework and open-source tool for the prospective design, governance, and evaluation of agentic AI systems. It provides a machine-readable "project contract" that bridges the gap between high-level user expectations and technical implementation. As of July 2026, it serves as the industry standard for planning high-fidelity reasoning workflows for **Claude 4.8 Opus**, **GPT-5.5**, and **Gemma 3**, incorporating the latest **MCP 3.0 visual design patterns**.

## What problem it solves
It addresses the **Expectation-Realisation Gap**: the systemic discrepancy where users expect high productivity gains from AI (e.g., 24% speedup) but often experience a decrease (e.g., 19% slowdown) due to unmeasured verification burdens, workflow friction, and human oversight costs. AAC requires explicit quantification of these factors during the planning phase to ensure ROI for autonomous engineering projects. It also standardizes the visual representation of [Model Context Protocol (MCP 3.0)](../../knowledge_base/patterns/tool-calling-and-mcp.md) tool graphs.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as a **Planning & Design Framework** that precedes and guides implementation. It acts as the blueprint for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **Full Project Planning**: Designing end-to-end agentic workflows, including complex components like **deterministic schedulers** and **LLM routers**.
- **Governance & Compliance**: Documenting data access, sensitivity, and staging for institutional or clinical AI deployments.
- **AI Coding Integration**: Generating implementation-ready instructions for AI coding assistants like [Claude Code](../development_ops/claude-code.md).
- **Visual MCP Orchestration**: Mapping out [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) server connections and tool dependency graphs using standardized visual nodes.

## Strengths
- **Six-Dimensional Framework**: Covers Scope, User Expectations, Feasibility, Governance, Data Access, and Outcomes.
- **MCP 3.0 Native**: Built-in support for mapping the **MCP 3.0 Task Protocol** and visual design patterns for tool discovery.
- **RO-Crate Export**: Generates FAIR-compliant, machine-interoperable metadata packages following W3C and Schema.org standards.
- **AI-Ready Output**: Automatically generates an `AGENTS.md` file that translates the project specification into structured instructions for tools like [Cursor](../development_ops/cursor.md) or [Aider](../development_ops/aider.md).
- **Privacy-First**: Fully client-side web application with real-time validation; data never leaves the browser.

## Limitations
- **Stable Beta**: Currently in version 0.18.0; while stable for production planning, the core schema continues to evolve with the MCP standard.
- **Human Input Required**: The quality of the output depends on the accuracy of the user's benefit quantification and feasibility assessments.
- **Visual Complexity**: Large-scale multi-agent systems can lead to complex "node spaghetti" if not properly modularized.

## When to use it
- Before starting the development of a new agentic system to ensure alignment between users and developers.
- When you need to justify the ROI of an AI automation project by factoring in human-in-the-loop costs.
- For complex projects requiring cross-backend model coordination (e.g., GPT-5.5 for orchestration, Claude 4.8 for technical execution, and [Gemma 3](../ai_knowledge/local_llms.md) for local processing).

## When not to use it
- For trivial, single-prompt AI tasks that do not require tool-calling or multi-step reasoning.
- When a project's goals and constraints are already fully documented in a compatible machine-readable format.

## Getting started
### Online Access
Access the live version of the canvas at [aac.slolab.ai](https://aac.slolab.ai/). No installation is required as it is a client-side web application.

### Basic Workflow
1. **Define Scope**: Enter the primary goals and constraints of your agentic project.
2. **Design Visual Flow**: Map your agents and tools using [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) visual nodes.
3. **Quantify Benefits**: Input expected productivity gains and human verification costs.
4. **Export Metadata**: Save your project as an `AGENTS.md` file or an RO-Crate package for interoperability.

## CLI examples
```bash
# AAC is a web-based Vue.js tool, no direct CLI for canvas creation.
# However, the exported RO-Crate can be validated via:
rocrate validate ./exported-crate/

# To self-host the AAC application locally (requires Node.js 20+):
git clone https://github.com/slolab/agentic-automation-canvas.git
cd agentic-automation-canvas
npm install && npm run dev
```

## API examples
```json
{
  "@context": "https://w3id.org/ro/crate/1.1/context",
  "@graph": [
    {
      "@id": "./",
      "@type": "Dataset",
      "name": "My Agentic Project",
      "description": "An automated workflow for document synthesis using Claude 4.8",
      "hasPart": [
        { "@id": "AGENTS.md" }
      ],
      "conformsTo": { "@id": "https://aac.slolab.ai/schema/v0.18.0" }
    },
    {
      "@id": "AGENTS.md",
      "@type": "File",
      "about": "Project implementation contract"
    }
  ]
}
```

## Related tools / concepts
- [AGENTS.md Pattern](../../knowledge_base/patterns/index.md)
- [Claude Code](../development_ops/claude-code.md)
- [Cursor](../development_ops/cursor.md)
- [Aider](../development_ops/aider.md)
- [RO-Crate Standard](https://www.researchobject.org/ro-crate/)
- [Symphony](symphony.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Model Context Protocol (MCP 3.0)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Standards](../../standards.md)

## Sources / references
- [Official Website](https://aac.slolab.ai/)
- [GitHub Repository](https://github.com/slolab/agentic-automation-canvas)
- [The Agentic Automation Canvas: a structured framework for agentic AI project design (arXiv:2602.15090)](https://arxiv.org/abs/2602.15090)
- [Quantifying the Expectation-Realisation Gap for Agentic AI Systems (arXiv:2602.20292)](https://arxiv.org/abs/2602.20292)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
