# DeepTutor

## What it is
DeepTutor is an AI-powered educational framework designed for personalized learning and intelligent tutoring. As of July 2026, it leverages advanced reasoning models like **Claude 4.8 Opus** and **GPT-5.5** to guide students through complex topics using a pedagogical layer that focuses on scaffolding rather than providing direct answers.

## What problem it solves
It addresses the "tutor's dilemma"—the challenge of helping a student without doing the work for them. Standard LLMs often provide answers too quickly, which can hinder deep learning. DeepTutor implements a structured, multi-turn reasoning system that probes student understanding, identifies specific misconceptions, and provides incremental guidance to help the student "learn how to think."

## Where it fits in the stack
**Agentic Education Layer**. It sits between the user interface and the foundational reasoning models, providing a framework for deploying educational agents. It integrates with knowledge bases and **MCP 3.0** servers to provide domain-specific expertise grounded in verified curriculum data.

## Typical use cases
- **Personalized STEM Tutor**: Guiding students through complex physics or calculus problems with step-by-step Socratic questioning.
- **Coding Mentor**: Helping developers learn new languages (e.g., Mojo, Rust) by analyzing their logic and suggesting architectural improvements rather than just fixing syntax.
- **Professional Upskilling**: Automating technical onboarding for engineers in enterprise environments using grounded internal documentation.
- **Visual Reasoning**: Analyzing student-drawn diagrams or handwritten equations via multimodal vision models (GPT-5.5, Claude 4.8).

## Strengths
- **Pedagogical Scaffolding**: Specifically designed to follow established educational theories (e.g., Zone of Proximal Development).
- **Misconception Detection**: Uses multi-step reasoning to pinpoint exactly where a student's mental model is flawed.
- **Model Agnostic**: Supports all major reasoning-native frontier models.
- **Extensible**: Native support for **MCP 3.0**, allowing the tutor to pull context from local files, databases, or external educational APIs.

## Limitations
- **Interaction Latency**: The deep reasoning required for pedagogical interventions can result in slower response times compared to standard chat.
- **High Resource Cost**: Effective tutoring requires high-tier reasoning models (Opus/GPT-5.5), which may be cost-prohibitive for large-scale deployments.
- **Configuration Complexity**: Setting up custom "Souls" and specialized knowledge bases requires technical expertise in prompt engineering and RAG.

## When to use it
- When building a platform that requires a "Socratic" or guided approach to learning rather than simple information retrieval.
- When you need an agent that can track a student's progress and adapt its teaching style over time.
- For research and development in the field of Intelligent Tutoring Systems (ITS) and agentic education.

## When not to use it
- For simple question-answering tasks where the user only needs a fast, direct fact.
- In low-latency environments where immediate speed is more important than educational depth.
- If using low-reasoning "small" models that cannot maintain the complex state required for multi-turn pedagogical loops.

## Getting started

### Installation (Local)
DeepTutor requires Python 3.12+ and Node.js 22+.

1.  **Clone & Setup**:
    ```bash
    git clone https://github.com/HKUDS/DeepTutor.git
    cd DeepTutor
    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[server,reasoning]"
    ```
2.  **API Keys**:
    Create a `.env` file with your `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.
3.  **Launch**:
    ```bash
    python scripts/start_tutor.py --model claude-4-8-opus-20260528
    ```

### Docker Deployment
```bash
docker compose up -d deeptutor-server
```

## CLI examples

### Start a Socratic Session
```bash
deeptutor chat --subject "Thermodynamics" --mode socratic --model gpt-5.5-preview
```

### Knowledge Base Ingestion
```bash
# Ingest educational materials using MCP 3.0 protocols
deeptutor kb ingest ./curriculum/advanced_math/ --name math-advanced
```

### Analyze Student Intent
```bash
# Analyze a student response for latent misconceptions
deeptutor analyze "The heavier object falls faster because of its mass"
```

## API examples

### Python (Agent Initialization)
```python
from deeptutor import TutorAgent

# Initialize an agent with a specific "Soul" and knowledge grounding
tutor = TutorAgent(
    model="claude-4-8-opus-20260528",
    soul="encouraging-mentor",
    kb="organic-chemistry-v2"
)

# Perform a pedagogical turn
response = tutor.step("I don't see why the reaction is exothermic.")
print(f"Tutor Response: {response.content}")
```

### Custom Scaffolding Pattern
```python
# Define a custom intervention pattern for the agent
tutor.add_pattern(
    name="logic-check",
    prompt="If the student makes a logical leap, ask them to explain the intermediate step."
)
```

## Related tools / concepts
- [NotebookLM](notebooklm.md) — For knowledge synthesis and grounded research.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — For connecting tutors to external datasets.
- [Claude](claude.md) — The primary reasoning model for pedagogical depth.
- [ChatGPT](chatgpt.md) — Alternative reasoning model provider.
- [AutoReason](../agents/autoreason.md) — Multi-agent reasoning framework.
- [GPT Researcher](../agents/gpt-researcher.md) — For generating the grounded content used by tutors.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The architectural pattern behind DeepTutor.
- [Local LLMs](local_llms.md) — For running tutoring sessions with open-weights models like Llama 4.

## Sources / references
- [DeepTutor GitHub Repository](https://github.com/HKUDS/DeepTutor)
- [DeepTutor: Agentic Scaffolding in STEM Education (arXiv 2026)](https://arxiv.org/abs/2604.26962)
- [Official Documentation and Soul Gallery](https://deeptutor.ai/docs)

## Contribution Metadata
- Last reviewed: 2026-07-02
- Confidence: high
