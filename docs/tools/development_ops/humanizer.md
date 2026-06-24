# Humanizer

## What it is
Humanizer is a core community skill for **Claude Code** and **OpenCode** focused on removing robotic "AI-isms" and making AI-generated output feel more natural and human-readable.

## What problem it solves
It addresses the common issue of AI output sounding overly mechanical, generic, or obviously templated. It is the de facto standard for "de-botting" agentic outputs before they are shared with humans.

## Where it fits in the stack
**Development & Ops / Output Refinement**. It sits at the **Interaction Layer**, transforming the "raw" reasoning of an LLM into human-centric communication.

## Typical use cases
- **Copy Polish**: Improving generated marketing copy or blog posts before publication.
- **Agentic Communication**: Post-processing drafts from coding or writing agents to ensure they match a team's voice.
- **Voice Matching**: Calibrating an AI to write exactly like a specific human user based on writing samples.

## Strengths
- **Native Claude Code Integration**: Works as a simple slash command (`/humanizer`) inside the terminal.
- **Pattern-Based Auditing**: Derived from the Wikipedia [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide.
- **Voice Calibration**: Supports "soul injection" by matching sentence rhythm and rhythm from user-provided samples.
- **Privacy-First**: Operates entirely locally within the agent's context; no external API calls for the humanization logic itself.

## Limitations
- **Subjectivity**: "Human-like" writing is inherently subjective and varies by domain.
- **Model Dependent**: Success depends on the underlying model's ability to handle the "soul injection" step (Claude 3.5 Sonnet and newer are recommended).

## When to use it
- When generated output needs a natural, non-robotic tone for human consumption.
- When you want to maintain a consistent personal or brand voice across agentic outputs.

## When not to use it
- In technical documentation where standard "AI-like" clarity (bolded headers, bulleted lists) is actually preferred.
- When factual accuracy is the primary bottleneck; humanization does not fix underlying hallucinations.

## Getting started

### Installation
Humanizer is distributed as a Markdown-based skill (`SKILL.md`). Install it by cloning into your agent's skills directory:

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

## CLI examples
The skill is invoked using the `/humanizer` slash command within supported agentic terminals.

### Basic Humanization
```bash
/humanizer "This model marks a pivotal moment in the evolution of AI."
```

### Voice Calibration
Provide a sample of your own writing for the agent to match:
```bash
/humanizer
[Paste 2-3 paragraphs of your own writing]

Now humanize:
[Paste AI text]
```

## API examples

### Programmatic Invocation (Markdown Skill pattern)
While Humanizer is a text-based skill, it can be invoked programmatically by injecting the skill definition into a system prompt.

```python
# Conceptual example of injecting Humanizer skill into a system prompt
with open("~/.claude/skills/humanizer/SKILL.md", "r") as f:
    humanizer_skill = f.read()

system_prompt = f"You are a helpful assistant. Use the following skill when requested:\n{humanizer_skill}"
# Then call the model with "/humanizer <text>" in the user prompt
```

## Related tools / concepts
- [Claude Code](claude-code.md)
- [OpenCode](opencode.md)
- [Andrej Karpathy Skills](../ai_knowledge/karpathy-skills.md)
- [AITMPL](../ai_knowledge/aitmpl.md)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Aider](aider.md)
- [GPT Engineer](gpt_engineer.md)
- [Style Transfer](https://en.wikipedia.org/wiki/Style_transfer)

## Sources / References
- [GitHub Repository](https://github.com/blader/humanizer)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
