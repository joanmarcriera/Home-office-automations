# VAKRA: Executable Benchmark for Enterprise Agents

## What it is
VAKRA (eValuating API and Knowledge Retrieval Agents) is a tool-grounded, executable benchmark designed to evaluate how well AI agents reason and act in enterprise-like environments. Unlike traditional benchmarks that test isolated skills, VAKRA measures **compositional reasoning** across APIs and documents, using full execution traces to assess multi-step workflow completion.

## What problem it solves
It addresses the gap between surface-level tool competence and robust, end-to-end agent reliability. VAKRA provides an executable environment with over 8,000 locally hosted APIs across 62 domains, preventing models from relying on memorized outputs and forcing them to navigate real API interactions, multi-hop reasoning, and policy constraints.

## Where it fits in the stack
**Category**: Benchmarking / Agent Evaluation. It is the gold standard for verifying **Agentic Shift** capabilities in production environments.

## Typical use cases
- **Agent Architecture Validation**: Testing if a new agentic framework can handle complex multi-step tasks across diverse domains.
- **Model Comparison**: Benchmarking different LLMs on their ability to use tools and follow policies in a realistic environment.
- **Regression Testing**: Ensuring that updates to an agent's reasoning logic don't break existing compositional capabilities.
- **Trajectory Verification**: Pinpointing exactly where a reasoning chain broke (e.g., entity disambiguation vs. schema alignment).

## Strengths
- **Executable**: Unlike static benchmarks, VAKRA actually runs the tool calls to verify results against persistent databases.
- **Multi-Source Reasoning**: Specifically targets the hard problem of combining structured API data with unstructured document retrieval.
- **Trajectory-Level Replay**: Replays full agent traces against live tools to support multiple valid execution paths.
- **Deterministic Evaluation**: Locally hosted tools ensure responses are verifiable and consistent across runs.

## Limitations
- **Environment Complexity**: Requires a self-hosted environment to run the 8,000+ mock APIs and persistent databases.
- **Resource Intensive**: Full trajectory replay can be computationally expensive for high-volume benchmarking.

## Task Tiers (May 2026 Baseline)
VAKRA organizes evaluation into three progressively complex settings:

1.  **Diverse API Interaction Styles**: Agents must adapt to different interface abstractions, selecting from business-intelligence style APIs (expanded functions) vs. query-aligned endpoints.
2.  **Multi-Hop Reasoning over Structured APIs**: Tasks require 3–7 dependent API calls, where outputs from early steps (identifiers, tokens) must be correctly transformed to parameterize subsequent actions.
3.  **Multi-Hop Multi-Source Reasoning with Tool-Use Policies**: The "Lethal Tier" requiring reasoning across documents and APIs while strictly adhering to natural-language policies (e.g., "Always verify customer ID before checking order status").

## Evaluation Methodology
VAKRA moves beyond simple "exact match" answers to trajectory verification:
- **Intermediate Step Validation**: Every tool call and parameter set is checked for accuracy and logical flow.
- **Cross-Source Grounding**: Verifies that information retrieved from unstructured documents is correctly grounded into structured API calls.
- **Schema Alignment**: Measures how well agents handle mismatched identifiers or naming conventions across different systems.

## Key Insights from 2026 Benchmarks
- **Hop Degradation**: Success rates fall significantly beyond 3 hops, with most models failing at 5+ hops due to accumulated errors in state management.
- **Policy Violations**: Even frontier models frequently ignore negative constraints expressed in natural language.
- **Language-Mediated Reasoning**: Failures often occur not in the tool call itself, but in the "connective tissue" (reasoning) between calls.

## When to use it
- When evaluating the reliability of AI agents intended for complex enterprise workflows (customer support, business intelligence, compliance).
- To identify specific failure modes in agentic reasoning, such as entity disambiguation or policy interpretation.
- For developers seeking a benchmark that reflects enterprise complexity rather than toy tasks.

## When not to use it
- For testing basic chat, summarization, or creative writing capabilities.
- If you lack the infrastructure to host the VAKRA executable environment.

## Related tools / concepts
- [SWE-bench](swe-bench.md)
- [HumanEval](human-eval.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Model Comparison and Evaluation](../../knowledge_base/model_comparison_and_evaluation.md)
- [IBM VAKRA GitHub](https://github.com/IBM/VAKRA)

## Sources / References
- [IBM Newsroom: Introducing VAKRA Benchmark](https://www.ibm.com/new/announcements/introducing-vakra-benchmark)
- [Hugging Face Space: VAKRA Public Leaderboard](https://huggingface.co/spaces/ibm-research/vakra)
- [VAKRA: eValuating API and Knowledge Retrieval Agents (arXiv)](https://arxiv.org/abs/2505.17166)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
