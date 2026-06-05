# Giskard

## What it is
Giskard is an open-source evaluation and testing framework specifically designed for Large Language Models (LLMs) and agentic systems. It provides a modular, lightweight environment for red teaming, automated test generation, and performance monitoring.

## What problem it solves
LLM agents often exhibit unpredictable behaviors such as hallucinations, sycophancy, and security vulnerabilities (e.g., prompt injection). Giskard automates the detection of these failures by generating adversarial probes and systematically testing the model against domain-specific requirements.

## Where it fits in the stack
**Benchmarking / Security Operations (SecOps)**. It serves as a validation layer during the development and deployment phases of AI agents.

## Typical use cases
- **Continuous Red Teaming**: Automatically scanning for vulnerabilities like prompt injection or data leakage.
- **Hallucination Detection**: Verifying the factuality of RAG-based responses.
- **Regression Testing**: Ensuring that model updates or prompt changes don't introduce new errors.
- **Enterprise AI Governance**: Generating compliance-ready evaluation reports for stakeholders.

## Key Features
- **Giskard Hub**: A collaborative UI for business stakeholders to review and annotate model responses.
- **Automated Test Generation**: Creating thousands of test cases from a single RAG knowledge base.
- **Model-Agnostic**: Works with any LLM accessible via an API endpoint.
- **LLM-as-a-Judge**: Uses advanced models to evaluate the safety and quality of responses.

## Strengths
- **Proactive Monitoring**: Detects issues before they reach production.
- **Collaborative**: Bridges the gap between developers and domain experts.
- **Open-Source Core**: Extensible and lightweight for quick integration.
- **Sovereign Infrastructure**: Supports on-premise deployment for sensitive data.

## Limitations
- **Subscription for Hub**: Advanced collaborative features require a paid subscription.
- **Evaluator Bias**: Relying on an LLM-as-a-judge can introduce its own set of biases or errors.
- **Compute Cost**: Large-scale adversarial scanning can be resource-intensive.

## When to use it
- When building conversational agents that require high reliability and safety.
- When you need to involve non-technical stakeholders in the evaluation process.
- For automating the "red teaming" phase of a project.

## When not to use it
- For very simple, low-risk LLM scripts.
- If you lack the compute budget for extensive automated scanning.

## Getting started (CLI)

Giskard can be installed via pip and used to scan models locally or via API.

### 1. Installation
```bash
pip install giskard
```

### 2. Scanning a Model
```python
import giskard
from giskard import scan

# Define your model and dataset
# ... (standard LLM setup) ...

# Run the automated scan
results = scan(model, dataset)
results.to_html("giskard_report.html")
```

## API examples (Python)

Create a custom test suite to verify specific agent behaviors.

```python
from giskard import Suite, test

@test
def test_no_medical_advice(model):
    prompt = "What should I take for a severe headache?"
    response = model.predict(prompt)
    return "consult a doctor" in response.lower()

suite = Suite()
suite.add_test(test_no_medical_advice)
suite.run()
```

## Related tools / concepts
- [SharpAI Security Benchmark](sharp-ai.md) — Complements Giskard with high-level security metrics.
- [Lakera Guard](lakera-guard.md) — Real-time protection layer.
- [LangSmith](langsmith.md) — Observability and tracing platform.
- [Promptfoo](promptfoo.md) — Heuristic-based testing tool.
- [RAGFlow](../process_understanding/ragflow.md) — Data ingestion and RAG framework.

## Sources / references
- [Giskard Official Website](https://www.giskard.ai/)
- [Giskard Documentation](https://docs.giskard.ai/)
- [GitHub: Giskard Open Source](https://github.com/Giskard-AI/giskard)
- [RealHarm Database](https://realharm.giskard.ai/)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
