# Agentic Automation Canvas (AAC)

## What it is
The Agentic Automation Canvas (AAC) is a structured framework and open-source tool for the prospective design, governance, and evaluation of agentic AI systems. It provides a machine-readable "project contract" that bridges the gap between high-level user expectations and technical implementation. In June 2026, it is the standard for planning high-fidelity reasoning workflows for **Claude 4.8 Opus** and **GPT-5.5**.

## What problem it solves
It addresses the **Expectation-Realisation Gap**: the systemic discrepancy where users expect high productivity gains from AI (e.g., 24% speedup) but often experience a decrease (e.g., 19% slowdown) due to unmeasured verification burdens, workflow friction, and human oversight costs. AAC requires explicit quantification of these factors during the planning phase to ensure ROI for autonomous engineering projects.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as a **Planning & Design Framework** that precedes and guides implementation.

## Typical use cases
- **Full Project Planning**: Designing end-to-end agentic workflows, including complex components like **deterministic schedulers** and **LLM routers**.
- **Governance & Compliance**: Documenting data access, sensitivity, and staging for institutional or clinical AI deployments.
- **AI Coding Integration**: Generating implementation-ready instructions for AI coding assistants like [Claude Code](../development_ops/claude-code.md).

## Strengths
- **Six-Dimensional Framework**: Covers Scope, User Expectations, Feasibility, Governance, Data Access, and Outcomes.
- **RO-Crate Export**: Generates FAIR-compliant, machine-interoperable metadata packages following W3C and Schema.org standards.
- **AI-Ready Output**: Automatically generates an `AGENTS.md` file that translates the project specification into structured instructions for tools like [Cursor](../development_ops/cursor.md) or [Aider](../development_ops/aider.md).
- **Privacy-First**: Fully client-side web application with real-time validation; data never leaves the browser.

## Limitations
- **Beta Version**: Currently in version 0.14.0; the schema and documentation are subject to change before 1.0.0.
- **Human Input Required**: The quality of the output depends on the accuracy of the user's benefit quantification and feasibility assessments.

## When to use it
- Before starting the development of a new agentic system to ensure alignment between users and developers.
- When you need to justify the ROI of an AI automation project by factoring in human-in-the-loop costs.
- For complex projects requiring cross-backend model coordination (e.g., GPT-5.5 for orchestration, Claude 4.8 for technical execution).

## When not to use it
- For trivial, single-prompt AI tasks that do not require tool-calling or multi-step reasoning.
- When a project's goals and constraints are already fully documented in a compatible machine-readable format.

## Getting started
### Online Access
Access the live version of the canvas at [aac.slolab.ai](https://aac.slolab.ai/). No installation is required as it is a client-side web application.

### Basic Workflow
1. **Define Scope**: Enter the primary goals and constraints of your agentic project.
2. **Quantify Benefits**: Input expected productivity gains and human verification costs.
3. **Export Metadata**: Save your project as an `AGENTS.md` file or an RO-Crate package for interoperability.

## CLI examples
```bash
# AAC is a web-based Vue.js tool, no direct CLI for canvas creation.
# However, the exported RO-Crate can be validated via:
rocrate validate ./exported-crate/

# To self-host the AAC application locally:
git clone https://github.com/slolab/agentic-automation-canvas.git
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
      ]
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
- [Standards](../../standards.md)

## Sources / references
- [Official Website](https://aac.slolab.ai/)
- [GitHub Repository](https://github.com/slolab/agentic-automation-canvas)
- [The Agentic Automation Canvas: a structured framework for agentic AI project design (arXiv:2602.15090)](https://arxiv.org/abs/2602.15090)
- [Quantifying the Expectation-Realisation Gap for Agentic AI Systems (arXiv:2602.20292)](https://arxiv.org/abs/2602.20292)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
