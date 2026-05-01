# Agent Development Kit (ADK)

## What it is
The Agent Development Kit (ADK) is an open-source framework by Google for building, debugging, and deploying reliable AI agents at enterprise scale. It is the same framework Google uses internally for production-grade AI agents.

## What problem it solves
It simplifies the transition from LLM prototyping to enterprise-grade agent deployment. It provides standardized orchestration, evaluation, and scaling tools, allowing developers to build everything from personal assistants to complex, mission-critical business workflows.

## Where it fits in the stack
**Category**: Frameworks / Enterprise Agent Framework

## Typical use cases
- **Enterprise Multi-Agent Systems**: Coordinating complex tasks across multiple specialized agents.
- **Mission-Critical Workflows**: Building agents that require high reliability and predictable execution paths.
- **Skill-Based Agents**: Extending agent capabilities using "Skills" (pre-defined action packages).
- **Scale-Out Deployment**: Deploying agents to Google Cloud (Cloud Run, GKE) with built-in scaling and management.

## Strengths
- **Production-Grade**: Based on Google's internal agent infrastructure.
- **Multi-Language**: Available in Python, TypeScript, Go, and Java.
- **Comprehensive Tooling**: Includes built-in support for debugging, evaluating, and monitoring agents.
- **Google Cloud Native**: Deep integration with Vertex AI and Gemini, while remaining open-source.

## Limitations
- **Enterprise Complexity**: May have a steeper learning curve compared to simpler frameworks like smolagents.
- **Ecosystem Maturity**: As a relatively new open-source release (late 2025/early 2026), the community ecosystem is still maturing.

## Getting started

### Installation (Python)
Detailed installation steps are provided in the Google Cloud Documentation and the GEAR (Google Developer Program).

```bash
pip install google-adk
```

### Key Concepts
- **Workflow Agents**: Define predictable, state-machine-like pipelines.
- **Skills**: Composable capabilities that agents can use to interact with external systems.
- **Runtime**: Local and cloud execution environments for ADK agents.

## Related tools / concepts
- [Google Gemini](../ai_knowledge/google-gemini.md)
- [Microsoft Agent Framework](microsoft-agent-framework.md)
- [LangGraph](langgraph.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / references
- [Google Cloud Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk)
- [GEAR Program](https://developers.google.com/program/gear)
- [Launch Announcement](https://www.reddit.com/r/vibecoding/comments/1raamgk/google_officially_launches_the_agent_development/)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
