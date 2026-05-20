# DeepTutor

## What it is
DeepTutor is an AI-powered educational framework designed for personalized learning and intelligent tutoring, leveraging advanced reasoning models to guide students through complex topics.

## What problem it solves
It addresses the limitations of standard chatbots in education by providing a structured, pedagogical approach to learning. It focuses on "teaching how to think" rather than just providing answers, using multi-turn reasoning to identify student misconceptions.

## Where it fits in the stack
**Category**: Tool / AI Assistants & Knowledge

## Typical use cases
- Personalized coding tutor for students.
- Intelligent assistant for complex technical documentation.
- Research-driven educational agent experiments.

## Strengths
- Pedagogy-first design.
- Leverages reasoning models for deep understanding of student intent.
- Open-source framework for building educational agents.

## Limitations
- Requires high-reasoning models (e.g., GPT-4, Claude 3.5 Opus) for optimal performance.
- Primarily a research/development framework rather than a finished consumer product.

## When to use it
- When building educational platforms that require more than simple Q&A.
- When studying how agents can be used for persistent, structured learning.

## When not to use it
- When seeking a simple Q&A chatbot without the pedagogical overhead.
- In production environments where latency and cost of multi-turn reasoning are primary concerns.

## Getting started

### Installation (Local)
DeepTutor requires Python 3.11+ and Node.js 20.9+.

1.  **Clone & Setup**:
    ```bash
    git clone https://github.com/HKUDS/DeepTutor.git
    cd DeepTutor
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -e ".[server]"
    ```
2.  **Frontend**:
    ```bash
    cd web && npm install && cd ..
    ```
3.  **Launch**:
    ```bash
    python scripts/start_web.py
    ```

### Docker Deployment
```bash
docker compose -f docker-compose.ghcr.yml up -d
```

## CLI Reference

DeepTutor provides a powerful agent-native CLI for interaction and management.

### Interactive Chat
```bash
deeptutor chat --capability deep_solve --kb my-kb
```

### One-shot Execution
```bash
deeptutor run deep_research "Transformer attention mechanisms"
```

### Knowledge Base Management
```bash
deeptutor kb create my-kb --doc textbook.pdf
deeptutor kb add my-kb --docs-dir ./papers/
```

## Architecture & Key Concepts

### TutorBot
TutorBots are autonomous agents powered by [nanobot](https://github.com/HKUDS/nanobot). Each bot has its own workspace, memory, and "Soul" (personality template), allowing it to initiate proactive check-ins and evolve alongside the learner.

### Book Engine
A multi-agent pipeline that transforms document collections into interactive "living books." It automatically generates outlines, retrieves relevant RAG context, and compiles pages with interactive block types (quizzes, animations, concept graphs).

## Licensing and cost
- **Open Source**: Yes (Apache-2.0)
- **API Usage**: Dependent on the underlying LLM provider.

## Related tools / concepts
- [AutoReason](../agents/autoreason.md) — Multi-agent reasoning framework.
- [GPT Researcher](../agents/gpt-researcher.md) — Autonomous research agent.
- [Claude Code](../development_ops/claude-code.md) — Agentic coding CLI.
- [NotebookLM](notebooklm.md) — Google's AI research and note-taking tool.
- [DeepSeek R1](deepseek-r1.md) — Reasoning-focused LLM.
- [ChatGPT](chatgpt.md) — General-purpose AI assistant.
- [Claude](claude.md) — Anthropic's flagship AI assistant.

## Sources / References
- [DeepTutor GitHub](https://github.com/HKUDS/DeepTutor)
- [DeepTutor arXiv Paper](https://arxiv.org/abs/2604.26962)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
