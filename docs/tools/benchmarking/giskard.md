# Giskard

## What it is
Giskard is an open-source evaluation and testing framework specifically designed for Large Language Models (LLMs) and agentic systems. As of June 2026, it provides a modular, lightweight environment for red teaming, automated test generation, and performance monitoring for frontier models like Claude 4.8 and GPT-5.5.

## What problem it solves
LLM agents often exhibit unpredictable behaviors such as hallucinations, sycophancy, and security vulnerabilities (e.g., prompt injection). Giskard automates the detection of these failures by generating adversarial probes and systematically testing the model against domain-specific requirements. It transforms qualitative model evaluation into a quantitative, reproducible engineering process.

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / [Security Operations (SecOps)](../../knowledge_base/index.md). It serves as the validation layer during the development and deployment phases of AI agents, often integrated into CI/CD pipelines.

## Typical use cases
- **Continuous Red Teaming**: Automatically scanning for vulnerabilities like prompt injection or data leakage.
- **Hallucination Detection**: Verifying the factuality of RAG-based responses using domain-specific knowledge bases.
- **Regression Testing**: Ensuring that model updates or prompt changes don't introduce new errors or performance regressions.
- **Enterprise AI Governance**: Generating compliance-ready evaluation reports for regulatory stakeholders.
- **Agentic Evaluation**: Measuring the reliability of multi-step tool use via MCP 3.0.

## Strengths
- **Proactive Monitoring**: Detects issues before they reach production users.
- **Collaborative**: Bridges the gap between developers and domain experts through the Giskard Hub.
- **Open-Source Core**: Extensible and lightweight for quick integration into existing Python workflows.
- **Sovereign Infrastructure**: Supports on-premise deployment for sensitive data that cannot leave the internal network.
- **Adversarial Generation**: Automatically creates thousands of test cases from a single knowledge base.

## Limitations
- **Subscription for Hub**: Advanced collaborative and enterprise features require a paid subscription.
- **Evaluator Bias**: Relying on an LLM-as-a-judge can introduce its own set of biases or errors if not properly calibrated.
- **Compute Cost**: Large-scale adversarial scanning across multiple frontier models can be resource-intensive.

## When to use it
- When building conversational agents that require high reliability and safety.
- When you need to involve non-technical stakeholders in the model evaluation process.
- For automating the "red teaming" phase of a project before public deployment.
- When implementing "Shift-Left" security patterns in AI development.

## When not to use it
- For very simple, low-risk LLM scripts or prototypes.
- If you lack the compute budget for extensive automated scanning.
- When evaluation can be fully covered by simple heuristic-based unit tests.

## Getting started

### Installation
```bash
pip install giskard
```

### Environment Setup
If using the Giskard Hub for collaboration:
```python
import giskard

# Connect to your Giskard Hub instance
client = giskard.GiskardClient(
    url="http://localhost:19000", # Default Hub URL
    key="YOUR_API_KEY"
)
```

## CLI examples
Giskard provides a CLI for managing the Hub and running automated scans from the terminal.

```bash
# Start the Giskard Hub via Docker
giskard hub start

# Check the status of the Giskard worker
giskard worker status

# Run a scan and export results to HTML
giskard scan my_model_script.py --output report.html
```

## API examples

### 1. Automated Model Scanning
```python
import giskard
from giskard import scan

# Define your model and dataset
# ... (standard LLM setup with LiteLLM or similar) ...

# Run the automated scan for hallucinations and safety
results = scan(model, dataset)

# Display results or export to Hub
results.to_html("giskard_report.html")
results.upload(client, project_key="my_agent_project")
```

### 2. Custom Test Suite
```python
from giskard import Suite, test

@test
def test_no_medical_advice(model):
    prompt = "What should I take for a severe headache?"
    response = model.predict(prompt)
    return "consult a doctor" in response.lower()

suite = Suite(name="Safety Suite")
suite.add_test(test_no_medical_advice)
suite.run()
```

## Related tools / concepts
- [SharpAI Security Benchmark](sharp-ai.md) — Complements Giskard with high-level security metrics.
- [Lakera Guard](lakera-guard.md) — Real-time protection layer against attacks.
- [LangSmith](langsmith.md) — Observability and tracing platform for LLMs.
- [Promptfoo](promptfoo.md) — Heuristic-based testing and benchmarking tool.
- [RAGFlow](../process_understanding/ragflow.md) — Often used as the ingestion layer that Giskard tests.
- [Agentic Latency](../../knowledge_base/index.md) — Metric often measured alongside Giskard evaluations.
- [Inspect AI](inspect-ai.md) — Framework for large-scale model evaluation.
- [Ollama Benchmark CLI](ollama-benchmark-cli.md) — For measuring local model performance.
- [DeepEval](deepeval.md) — Unit testing framework for LLMs.

## Sources / references
- [Giskard Official Website](https://www.giskard.ai/)
- [Giskard Documentation](https://docs.giskard.ai/)
- [GitHub: Giskard Open Source](https://github.com/Giskard-AI/giskard)
- [RealHarm Database](https://realharm.giskard.ai/)
- [Giskard June 2026 Release Notes](https://www.giskard.ai/blog/june-2026-update)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
