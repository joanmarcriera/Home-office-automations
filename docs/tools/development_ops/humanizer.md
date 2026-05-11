# Humanizer

## What it is
Humanizer is a community repository focused on making AI-generated output feel more natural and human-readable.

## What problem it solves
It addresses the common issue of AI output sounding overly mechanical, generic, or obviously templated.

## Where it fits in the stack
**Development & Ops / Output Refinement**. It is best viewed as a workflow asset around generation quality rather than a foundation model product.

## Typical use cases
- Improving generated copy before publication
- Post-processing drafts from coding or writing agents
- Studying prompt patterns for more natural output

## Strengths
- Practical for teams publishing AI-assisted content
- Useful as a reference for style refinement patterns

## Limitations
- "Human-like" writing remains subjective
- Style polish does not fix weak underlying reasoning or research

## When to use it
- When generated output needs a more natural tone

## When not to use it
- When factual accuracy or source quality is still the primary problem.
- In technical documentation where standard "AI-like" clarity and bolded headers are actually preferred for readability.

## Getting started

### Installation
Humanizer is a skill for Claude Code and OpenCode. To install it, clone the repository into your local skills directory:

**Claude Code**
```bash
mkdir -p ~/.claude/skills
git clone https://github.com/blader/humanizer.git ~/.claude/skills/humanizer
```

**OpenCode**
```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/blader/humanizer.git ~/.config/opencode/skills/humanizer
```

### Initial Run
Launch Claude Code in your project directory. The skill is automatically loaded and ready for use.

## CLI examples
The skill is invoked using the `/humanizer` slash command within your AI terminal.

### Basic Humanization
```bash
/humanizer "This model marks a pivotal moment in the evolution of AI."
```

### Voice Calibration
Provide a sample of your own writing to match its style:
```bash
/humanizer
Here's a sample of my writing for voice matching:
[Paste 2-3 paragraphs of your own writing]

Now humanize this text:
[Paste AI text to humanize]
```

### Batch Processing
Ask your agent to process multiple blocks:
```bash
"Please use the humanizer skill to rewrite these three paragraphs to sound more natural."
```

## API examples
> [!NOTE]
> Humanizer is implemented as a Markdown-based skill (`SKILL.md`) for agentic tools; it does not currently provide a standalone programmatic API or library.

## How it works
Humanizer audits text against **29 patterns** of "AI-isms" based on the Wikipedia [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide. It performs a multi-pass rewrite to address:
- **Significance Inflation**: Removing phrases like "marking a pivotal moment" or "testament to."
- **Formulaic Structure**: Breaking up repetitive "Not only X, but also Y" sentence patterns.
- **AI Vocabulary**: Replacing overused words like "delve," "landscape," "showcasing," and "additionally."
- **Chatbot Artifacts**: Removing sycophantic pleasantries ("I hope this helps!").

## Related tools / concepts
- [AI Templates](../ai_knowledge/aitmpl.md)
- [Claude Cookbooks](claude-cookbooks.md)
- [Codeium](codeium.md)
- [Claude Code](claude-code.md)
- [OpenCode](opencode.md)
- [Andrej Karpathy Skills](../ai_knowledge/karpathy-skills.md)
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md)

## Sources / References
- [GitHub Repository](https://github.com/blader/humanizer)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
