# DeepTutor

## What it is
DeepTutor is an AI-powered educational framework designed for personalized learning and intelligent tutoring. It leverages advanced reasoning models, such as **Claude 4.8 Opus** and **GPT-5.5**, to guide students through complex topics by identifying knowledge gaps and providing scaffolding rather than direct answers.

## What problem it solves
It addresses the "tutor's dilemma"—the challenge of helping a student without doing the work for them. Standard LLMs often provide answers too quickly; DeepTutor implements a pedagogical layer that "teaches how to think," using multi-turn reasoning to probe student understanding and correct misconceptions incrementally.

## Where it fits in the stack
**Agentic Education Layer**. It sits between the user interface and the foundational reasoning models, providing a structured framework for educational agents. It is often integrated with knowledge bases to provide domain-specific expertise.

## Typical use cases
- **Personalized Coding Tutor**: Helping developers learn new frameworks (e.g., Mojo or Rust) by solving errors interactively.
- **Academic Research Assistant**: Guiding graduate students through the synthesis of complex literature.
- **Enterprise Upskilling**: Automating the onboarding and technical training of new employees in a homelab or corporate environment.

## Strengths
- **Pedagogy-First**: Designed around established educational theories (e.g., Vygotsky's Zone of Proximal Development).
- **Reasoning-Native**: Specifically optimized for high-reasoning models that can maintain complex state across long conversations.
- **Multi-Modal Support**: Can analyze student-drawn diagrams or handwritten math (via GPT-5.5 Vision).

## Limitations
- **Latency**: The multi-step reasoning required for pedagogical interventions can be slower than standard chat.
- **Cost**: Requires high-end models (Opus tier) for the most effective tutoring interactions.
- **Framework Complexity**: Requires significant configuration to set up custom "Souls" and knowledge bases.

## When to use it
- When building an educational platform that requires a "Socratic" approach to learning.
- When you need an agent that can track student progress and adapt its teaching style over time.
- In research settings exploring the intersection of AI and intelligent tutoring systems (ITS).

## When not to use it
- For simple question-answering tasks where the user just wants the facts.
- In low-latency environments where immediate responses are prioritized over educational depth.
- If using low-reasoning models that cannot follow complex pedagogical instructions.

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
2.  **Configuration**:
    Create a `.env` file with your `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.
3.  **Launch**:
    ```bash
    python scripts/start_tutor.py --model claude-4-8-opus
    ```

### Docker Deployment
```bash
docker compose up -d deeptutor-server
```

## CLI examples

### Interactive Tutoring Session
```bash
deeptutor chat --subject "Quantum Mechanics" --mode socratic
```

### Knowledge Base Management
```bash
# Ingest a textbook into the tutor's memory
deeptutor kb ingest ./docs/textbooks/physics_vol1.pdf --name physics-101
```

### Evaluating Student Intent
```bash
# Analyze a student's response for misconceptions
deeptutor analyze "The electron orbits the nucleus like a planet"
```

## API examples

### Python (Agent Setup)
```python
from deeptutor import TutorAgent

# Initialize an agent with a specific "Soul" (personality)
tutor = TutorAgent(
    model="claude-4-8-opus-20260528",
    soul="encouraging-mentor",
    kb="advanced-calculus"
)

# Conduct a tutoring turn
response = tutor.step("I don't understand why we use the chain rule here.")
print(response.content)
```

### Knowledge Retrieval
```python
# Query the educational knowledge base
context = tutor.kb.retrieve("chain rule derivation", top_k=3)
```

## Related tools / concepts
- [AutoReason](../agents/autoreason.md) — Multi-agent reasoning framework.
- [GPT Researcher](../agents/gpt-researcher.md) — Autonomous research assistant.
- [NotebookLM](notebooklm.md) — Google's knowledge synthesis tool.
- [Claude](claude.md) — Primary reasoning model for DeepTutor.
- [ChatGPT](chatgpt.md) — Alternative model provider.
- [DeepSeek R1](deepseek-r1.md) — Open-weight reasoning alternative.
- [Model Context Protocol](../../knowledge_base/patterns/mcp-patterns.md) — For connecting tutors to external tools.

## Sources / references
- [DeepTutor GitHub Repository](https://github.com/HKUDS/DeepTutor)
- [DeepTutor Paper (arXiv 2026)](https://arxiv.org/abs/2604.26962)
- [Official Documentation](https://deeptutor.ai/docs)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
