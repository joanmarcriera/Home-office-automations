# Fiddler AI

## What it is
Fiddler is an Enterprise-grade Model Performance Management (MPM) platform that has expanded to include specialized tools for LLM observability and monitoring (Fiddler Auditor and Fiddler AI Observability).

## What problem it solves
For enterprises, AI reliability isn't just about accuracy; it's about governance, safety, and bias. Fiddler provides a robust framework for monitoring AI models in production, detecting drift, and ensuring models remain compliant and safe.

## Where it fits in the stack
**Category**: Process & Understanding / Enterprise AI Observability. It serves as the **governance and reliability layer** for models deployed in regulated or high-stakes environments.

## Typical use cases
- **LLM Safety Monitoring**: Detecting PII, toxicity, and hallucinations in production LLM traffic.
- **Drift Detection**: Identifying when model performance begins to degrade over time as real-world data changes.
- **Root Cause Analysis**: Using "Explainable AI" (XAI) features to understand why a model made a specific prediction or generated a specific response.
- **Bias Auditing**: Ensuring AI applications are fair and non-discriminatory across different demographic groups.

## Strengths
- **Enterprise-Ready**: Robust security, RBAC, and scalability designed for large-scale deployments.
- **Multimodal Support**: Can monitor traditional machine learning models as well as modern Large Language Models (LLMs).
- **Specialized LLM Metrics**: Includes advanced metrics for faithfulness, grounding, and instruction-following.
- **Focus on Trust**: Strong emphasis on AI ethics, governance, and transparent model behavior.

## Limitations
- **Target Audience**: Primarily built for large enterprises and data science teams; may be overly complex for individual developers or small projects.
- **Commercial Focus**: It is a commercial platform, with community tiers and trials that may have limited features.
- **Integration Overhead**: Requires instrumenting model code with the Fiddler SDK for full observability.

## When to use it
- When deploying high-stakes AI models in regulated industries such as Finance, Healthcare, or Legal.
- When you need enterprise-grade governance, audit trails, and model explainability.
- To monitor model performance and safety for frontier models like Claude 4.8 Opus or GPT-5.5.

## When not to use it
- For early-stage prototyping, solo hobby projects, or personal research where simple logging suffices.
- If you prefer a strictly open-source observability stack without a commercial vendor.

## Getting started

Install the Fiddler Python client:

```bash
pip install fiddler-client
```

Connect to your Fiddler instance:

```python
import fiddler as fdl
client = fdl.FiddlerApi(url="YOUR_URL", org_id="YOUR_ORG", auth_token="YOUR_TOKEN")
```

## CLI examples

### fiddler-client
(Note: Fiddler primarily uses a Python SDK; CLI is often used via `pip` or custom wrappers.)
```bash
pip show fiddler-client
```

### curl (Publish Events)
Publishing an event to the Fiddler API:
```bash
curl -X POST https://app.fiddler.ai/api/v1/events \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{"project_id": "p1", "model_id": "m1", "data": {...}}'
```

### python -m fiddler
Checking version and connectivity:
```bash
python -m fiddler --version
```

## API examples

### Python (Evaluating Answer Relevance)
```python
import fiddler as fdl

# Initialize evaluator
evaluator = fdl.AnswerRelevance()

# Run evaluation
result = evaluator.evaluate(
    question="What is Fiddler?",
    answer="Fiddler is an AI observability platform."
)
print(result)
```

## Related tools / concepts
- [Arize AI](./arize-ai.md) — Alternative AI observability platform.
- [Weights & Biases](./wandb-weave.md) — For experiment tracking and model monitoring.
- [Datadog](./datadog.md) — Unified monitoring and security for cloud applications.
- [Sentry](./sentry.md) — Application performance monitoring and error tracking.
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md) — Architectural patterns for secure AI.
- [LangSmith](../benchmarking/langsmith.md) — Platform for debugging and testing LLM applications.
- [Comet Opik](./comet-opik.md) — Open-source platform for LLM tracing and observability.

## Sources / references
- [Fiddler AI Website](https://www.fiddler.ai/)
- [Fiddler SDK Documentation](https://docs.fiddler.ai/api)
- [Fiddler LLM Observability Guide](https://www.fiddler.ai/llm-observability)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
