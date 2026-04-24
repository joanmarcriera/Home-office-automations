# VAKRA: Executable Benchmark for Enterprise Agents

## What it is
VAKRA is a tool-grounded, executable benchmark designed to evaluate how well AI agents reason and act in enterprise-like environments. Unlike traditional benchmarks that test isolated skills, VAKRA measures **compositional reasoning** across APIs and documents, using full execution traces to assess multi-step workflow completion.

## What problem it solves
It addresses the gap between surface-level tool competence and robust, end-to-end agent reliability. VAKRA provides an executable environment with over 8,000 locally hosted APIs across 62 domains, preventing models from relying on memorized outputs and forcing them to navigate real API interactions, multi-hop reasoning, and policy constraints.

## Where it fits in the stack
**Benchmarking**. It is used to evaluate the reasoning, tool-use, and failure modes of high-autonomy agents.

## Core Capabilities
VAKRA evaluates agents across four distinct task types:

1.  **API Chaining (Business Intelligence)**: Uses SLOT-BIRD (generic tools) and SEL-BIRD (specialized tools) collections to test the ability to sequence 1–12 tool calls.
2.  **Tool Selection (Dashboard APIs)**: Requires selecting the correct API from sets ranging from 6 to 328 tools (REST-BIRD collection).
3.  **Multi-Hop Reasoning**: Tests logical hops (1–5) using dashboard APIs to combine multiple pieces of evidence.
4.  **Multi-Hop Multi-Source Reasoning & Policy Adherence**: The most complex tier, involving RAG (Document Retrieval), API calls, multi-turn dialog, and plain-text tool-usage policies (e.g., "only use document retrievers for Technology topics").

## Evaluation Framework
VAKRA uses a waterfall-style evaluation pipeline:
- **Policy Verification**: Programmatically checks if tool-use constraints were followed.
- **Trajectory Comparison**: Executes predicted tool calls and compares intermediate results against ground truth. It supports alternative valid reasoning paths using a secondary LLM-based judge.
- **Final Response Evaluation**: An LLM judge ensures the final answer is grounded in tool outputs and factually consistent with the ground truth.

## Key Insights
- **Compositional Failure**: Models frequently break down when required to combine APIs, documents, and policy requirements.
- **Policy Struggles**: Agents often struggle to incorporate external constraints (policies) into their reasoning process.
- **Hop Degradation**: Performance markedly drops as the number of logical hops increases, especially beyond 3 hops.

## Related tools / concepts
- [SWE-bench](swe-bench.md)
- [HumanEval](human-eval.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md)

## Sources / References
- [Hugging Face Blog: Inside VAKRA](https://huggingface.co/blog/ibm-research/vakra-benchmark-analysis)
- [VAKRA Dataset on Hugging Face](https://huggingface.co/datasets/ibm-research/VAKRA)
- [VAKRA GitHub Repository](https://github.com/IBM/vakra)

## Contribution Metadata
- Last reviewed: 2026-04-16
- Confidence: high
