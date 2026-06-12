# DREAM: Deep Research Evaluation with Agentic Metrics

## What it is
DREAM (Deep Research Evaluation with Agentic Metrics) is an agentic evaluation framework for deep research agents. It uses tool-calling agents to independently verify the factual correctness and temporal validity of research reports.

## What problem it solves
It addresses the "Mirage of Synthesis"—a defect in static LLM evaluation where fluent writing and plausible citations hide factual errors or reasoning flaws. Static judges cannot verify claims against real-world evidence; DREAM solves this by making the evaluator as capable (agentic) as the agent it is testing.

## Where it fits in the stack
**Eval**: It is a framework for benchmarking and evaluating advanced LLM agentic performance, particularly for models like `claude-4-8-opus-20260528` and GPT-5.5 when used in research loops.

## Typical use cases
- **Benchmarking Research Agents**: Comparing how well different models or agent architectures (like OpenHands or custom research loops) generate accurate analyst-grade reports.
- **Reasoning Probes**: Systematically identifying reasoning defects in long-form generation.
- **Fact-checking automation**: Scaling the verification of AI-generated content against live web data.

## Strengths
- **Parity-based Evaluation**: Uses agents to evaluate agents, ensuring the evaluator has the tools necessary to verify modern information.
- **Sensitivity to Decay**: Significantly more sensitive to factual and temporal decay than static benchmarks.
- **Scalable and Reference-Free**: Does not require a pre-defined ground truth for every query, allowing for flexible evaluation of open-ended research.

## Limitations
- **Operational Complexity**: Requires a tool-calling environment for the evaluation agent, making it more complex to run than static Q&A.
- **Cost**: Agentic evaluation involves multiple LLM turns, increasing the cost of benchmarking.

## When to use it
- When evaluating agents that perform active research or use external tools.
- When static benchmarks are suspected of suffering from data contamination or lack of temporal awareness.

## When not to use it
- For evaluating simple base models on static knowledge.
- When a fast, low-cost evaluation signal is needed for iterative model tuning.

## Getting started

DREAM requires an environment where evaluation agents can execute search and browsing tools.

### 1. Installation
```bash
pip install dream-eval-framework
```

### 2. Environment Setup
Configure your LLM provider and search API keys:
```bash
export OPENAI_API_KEY="your-key"
export TAVILY_API_KEY="your-key"
```

### 3. Basic Verification
Run a verification check on a local report file:
```bash
dream-eval verify --report ./my_research_report.md
```

## CLI examples

### 1. Running a Benchmark
Run the DREAM benchmark suite against a research agent endpoint:
```bash
dream-eval benchmark --agent-url "http://localhost:8080/chat" --tasks research_tasks_v1.json
```

### 2. Temporal Sensitivity Check
Check if a report is outdated by forcing the agent to prioritize recent news sources:
```bash
dream-eval verify --report report.md --temporal-weight 0.8
```

### 3. Exporting Results
Export the verification results to a structured JSON format for further analysis:
```bash
dream-eval verify --report report.md --output results.json
```

## API examples

### Python Verification Loop
A conceptual implementation of the DREAM verification step using the Python SDK.

```python
from dream_eval import DreamEvaluator

# Initialize the agentic evaluator with search tools
evaluator = DreamEvaluator(
    model="claude-4-8-opus-20260528",
    tools=["google_search", "web_browsing"]
)

report_content = "..." # The output from the research agent

# DREAM starts its independent verification
verification_results = evaluator.verify_claims(report_content)

for claim in verification_results.claims:
    print(f"Claim: {claim.text}")
    print(f"Status: {claim.verification_status}") # Verified | Refuted | Unverifiable
```

## Related tools / concepts
- [Humanity's Last Exam (HLE)](./humanitys-last-exam.md)
- [LM Evaluation Harness](./lm-evaluation-harness.md)
- [GPQA](./gpqa.md)
- [Terminal-Bench](./terminal-bench.md)
- [OpenHands](../development_ops/openhands.md)
- [Letta](../agents/letta.md)
- [SWE-bench](./swe-bench.md)

## Sources / references
- [Hugging Face Paper Page](https://huggingface.co/papers/2602.18940)
- [arXiv Preprint (arXiv:2602.18940)](https://arxiv.org/abs/2602.18940)


## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
