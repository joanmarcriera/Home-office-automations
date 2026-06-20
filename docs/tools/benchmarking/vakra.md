# VAKRA: Executable Benchmark for Enterprise Agents

## What it is
VAKRA (eValuating API and Knowledge Retrieval Agents) is a tool-grounded, executable benchmark designed to evaluate how well AI agents reason and act in enterprise-like environments. Unlike traditional benchmarks that test isolated skills, VAKRA measures **compositional reasoning** across APIs and documents, using full execution traces to assess multi-step workflow completion in June 2026.

## What problem it solves
It addresses the gap between surface-level tool competence and robust, end-to-end agent reliability. VAKRA provides an executable environment with over 8,000 locally hosted APIs across 62 domains, preventing models from relying on memorized outputs and forcing them to navigate real API interactions, multi-hop reasoning, and policy constraints. It solves the "hallucination" problem in tool-use by verifying results against actual databases.

## Where it fits in the stack
**Benchmarking / Agent Evaluation**. It is a primary framework for verifying "Agentic Shift" capabilities in production environments. It sits alongside frameworks like [OpenCompass](opencompass.md) but focuses specifically on tool-grounded reasoning.

## Typical use cases
- **Agent Architecture Validation**: Testing if a new agentic framework (e.g., [OpenClaw](../development_ops/openclaw.md)) can handle complex multi-step tasks.
- **Model Comparison**: Benchmarking different LLMs (Claude 4.8 vs GPT-5.5) on their ability to use tools and follow policies.
- **Regression Testing**: Ensuring that updates to an agent's reasoning logic or system prompts don't break existing compositional capabilities.
- **Policy Compliance Auditing**: Verifying that agents strictly adhere to negative constraints (e.g., "Never share user PII").

## Strengths
- **Executable**: Unlike static benchmarks, VAKRA actually runs the tool calls to verify results against persistent databases.
- **Multi-Source Reasoning**: Specifically targets the hard problem of combining structured API data with unstructured document retrieval (RAG).
- **Trajectory-Level Replay**: Replays full agent traces against live tools to support multiple valid execution paths.
- **Deterministic Evaluation**: Locally hosted tools ensure responses are verifiable and consistent across runs.
- **June 2026 Context**: Updated to support [MCP 3.0](../../tools/automation_orchestration/mcp.md) tool definitions.

## Limitations
- **Environment Complexity**: Requires a complex self-hosted environment to run the 8,000+ mock APIs and persistent databases.
- **Resource Intensive**: Full trajectory replay can be computationally expensive and time-consuming for large-scale benchmarking.
- **Steep Learning Curve**: Configuring custom enterprise domains within VAKRA requires significant effort.

## When to use it
- When evaluating the reliability of AI agents intended for complex enterprise workflows (customer support, business intelligence, compliance).
- To identify specific failure modes in agentic reasoning, such as entity disambiguation or policy interpretation.
- For developers seeking a benchmark that reflects enterprise complexity rather than simple toy tasks.
- When verifying the safety and policy adherence of autonomous agentic loops.

## When not to use it
- For testing basic chat, summarization, or creative writing capabilities.
- If you lack the infrastructure or technical expertise to host the VAKRA executable environment.
- For simple "vibe-checks" of a model's general knowledge.

## Getting started

### Environment Setup
VAKRA requires a containerized environment to host its mock APIs.

```bash
# Clone the repository
git clone https://github.com/IBM/VAKRA.git
cd VAKRA

# Start the executable environment (requires Docker)
docker-compose up -d
```

### Running an Evaluation
Execute a benchmarking run against a target agent:

```bash
python run_eval.py --agent_url http://localhost:18789 --suite enterprise_composition
```

## CLI examples
VAKRA provides tools for trajectory analysis and environment management:

```bash
# List available domains and APIs
python tools/list_tools.py

# Replay a specific trajectory for debugging
python tools/replay_trajectory.py --trace_id "trace_20260620_001"

# Export evaluation metrics to JSON
python tools/export_metrics.py --run_id "run_456" --format json
```

## API examples
The VAKRA environment can be interacted with via its orchestrator API:

```python
import requests

# Query the status of the mock API environment
response = requests.get("http://localhost:8080/status")
print(response.json())

# Submit a task for evaluation
task_data = {
    "task": "Find the total sales for the Q1 2026 region North and compare with South.",
    "policy": "PII_REDACTION_STRICT"
}
response = requests.post("http://localhost:8080/evaluate", json=task_data)
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) — Software engineering benchmark.
- [HumanEval](human-eval.md) — Coding capability benchmark.
- [OpenCompass](opencompass.md) — General model evaluation platform.
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md) — Design patterns for VAKRA-ready tools.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration patterns evaluated by VAKRA.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — The standard for the tools VAKRA evaluates.
- [LiteLLM](../../services/litellm.md) — Used to route model calls during VAKRA runs.

## Sources / references
- [IBM VAKRA GitHub](https://github.com/IBM/VAKRA)
- [IBM Newsroom: Introducing VAKRA Benchmark](https://www.ibm.com/new/announcements/introducing-vakra-benchmark)
- [Hugging Face Space: VAKRA Public Leaderboard](https://huggingface.co/spaces/ibm-research/vakra)
- [VAKRA: eValuating API and Knowledge Retrieval Agents (arXiv)](https://arxiv.org/abs/2505.17166)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
