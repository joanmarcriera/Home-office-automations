# Agentic Automation Canvas (AAC)

## What it is
The Agentic Automation Canvas (AAC) is a structured framework and open-source tool for the prospective design, governance, and evaluation of agentic AI systems. It provides a machine-readable "project contract" that bridges the gap between high-level user expectations and technical implementation.

## What problem it solves
It addresses the **Expectation-Realisation Gap**: the systemic discrepancy where users expect high productivity gains from AI (e.g., 24% speedup) but often experience a decrease (e.g., 19% slowdown) due to unmeasured verification burdens, workflow friction, and human oversight costs. AAC requires explicit quantification of these factors during the planning phase.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as a **Planning & Design Framework** that precedes and guides implementation.

## Typical use cases
- **Full Project Planning**: Designing end-to-end agentic workflows, including complex components like **deterministic schedulers** and **LLM routers**.
- **Governance & Compliance**: Documenting data access, sensitivity, and staging for institutional or clinical AI deployments.
- **AI Coding Integration**: Generating implementation-ready instructions for AI coding assistants.

## Strengths
- **Six-Dimensional Framework**: Covers Scope, User Expectations, Feasibility, Governance, Data Access, and Outcomes.
- **RO-Crate Export**: Generates FAIR-compliant, machine-interoperable metadata packages following W3C and Schema.org standards.
- **AI-Ready Output**: Automatically generates an `AGENTS.md` file that translates the project specification into structured instructions for tools like [Cursor](../development_ops/cursor.md) or [GitHub Copilot](../development_ops/github_copilot.md).
- **Privacy-First**: Fully client-side web application with real-time validation; data never leaves the browser.

## Limitations
- **Beta Version**: Currently in version 0.14.0; the schema and documentation are subject to change before 1.0.0.
- **Human Input Required**: The quality of the output depends on the accuracy of the user's benefit quantification and feasibility assessments.

## When to use it
- Before starting the development of a new agentic system to ensure alignment between users and developers.
- When you need to justify the ROI of an AI automation project by factoring in human-in-the-loop costs.
- For complex projects requiring cross-backend model coordination and structured planning.

## When not to use it
- For trivial, single-prompt AI tasks that do not require tool-calling or multi-step reasoning.
- When a project's goals and constraints are already fully documented in a compatible machine-readable format.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free
- **Self-hostable**: Yes (Vue.js application)

## Related tools / concepts
- [AGENTS.md Pattern](../../knowledge_base/patterns/index.md)
- [Cursor](../development_ops/cursor.md)
- [Aider](../development_ops/aider.md)
- [RO-Crate Standard](https://www.researchobject.org/ro-crate/)

## Sources / References
- [Official Website](https://aac.slolab.ai/)
- [GitHub Repository](https://github.com/slolab/agentic-automation-canvas)
- [The Agentic Automation Canvas: a structured framework for agentic AI project design (arXiv:2602.15090)](https://arxiv.org/abs/2602.15090)
- [Quantifying the Expectation-Realisation Gap for Agentic AI Systems (arXiv:2602.20292)](https://arxiv.org/abs/2602.20292)

## Contribution Metadata
- Last reviewed: 2026-03-03
- Confidence: high
