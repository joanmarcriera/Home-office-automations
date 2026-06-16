# Anthropic Agent Skills

## What it is
Anthropic Agent Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. They teach Claude how to complete specific tasks in a repeatable way, following the [Agent Skills](https://agentskills.io) specification. In June 2026, these skills are the primary mechanism for extending the capabilities of frontier models like **Claude 4.8 Opus** (`claude-4-8-opus-20260528`).

## What problem it solves
It addresses the need for repeatable, high-performance execution of specialized tasks by agents. Instead of relying on general model knowledge, skills provide structured instructions and tools tailored to specific domains like document processing, technical testing, or creative workflows, significantly reducing hallucination in complex operations.

## Where it fits in the stack
**Agent / Tool / Pattern**. It acts as a standardized way to equip autonomous agents with specialized capabilities, sitting between the raw model and the execution environment.

## Typical use cases
- **Document Processing**: Extracting data from PDFs, manipulating DOCX files, or generating XLSX reports with high fidelity.
- **Technical Tasks**: Testing web applications using Playwright, generating MCP servers, or automating data analysis in sandboxed environments.
- **Enterprise Workflows**: Maintaining brand guidelines in communications or automating internal reporting for large-scale operations.

## Strengths
- **Repeatability**: Ensures consistent behavior for specialized tasks across different sessions and environments.
- **Standardized**: Follows the `agentskills.io` specification, making skills interoperable across different agent harnesses.
- **Discovery**: Uses YAML frontmatter (`name`, `description`) for easy discovery and automated selection by agent routers.
- **Extensible**: Allows developers to create custom skills using a simple Markdown-based template.

## Limitations
- **Model Optimization**: While following an open spec, many skills are specifically optimized for the Claude family (e.g., Claude 4.8 Opus).
- **Environment Specificity**: Some skills require specific tools or runtimes (e.g., Python 3.12+, Node.js 22+) to execute successfully.
- **Context Overhead**: Loading too many complex skills can consume significant portions of the model's context window.

## When to use it
- When you need Claude to perform complex, multi-step tasks that require specific formatting or deep domain knowledge.
- When building autonomous agent workflows that need to dynamically load and unload specialized capabilities to manage context efficiency.
- When you need to provide a standardized interface for tool-use across a multi-agent system.

## When not to use it
- For simple, one-off tasks that can be handled via a single well-crafted prompt.
- If using an LLM provider that does not support the Agent Skills specification or lacks native tool-calling capabilities.
- When strict local-only execution is required without the ability to load external instruction folders.

## Getting started

### Installation
Clone the official skills repository or create your own skills directory:
```bash
git clone https://github.com/anthropics/skills.git
```

### Usage
Configure your agent (e.g., Claude Code) to point to your skills directory. Claude will automatically index the `SKILL.md` and associated scripts during initialization.

## CLI examples
```bash
# List available skills in a directory
ls -R ./skills

# Test a specific skill (if test scripts are provided)
python3 ./skills/document-processing/test.py

# Create a new skill from the template
cp -r ./templates/skill-template ./skills/my-new-skill
```

## API examples
```python
import anthropic

# Skills are typically loaded via system prompt or as tool definitions
# In June 2026, Claude 4.8 Opus uses these skills for autonomous task execution
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-4-8-opus-20260528",
    max_tokens=2048,
    system="Use the 'document-processing' skill located in /path/to/skills.",
    messages=[{"role": "user", "content": "Extract text from report.pdf"}]
)
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Documentation Writer Skill](documentation-writer.md)
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md)
- [Roo Code](roo-code.md)
- [OpenHands](../development_ops/openhands.md)

## Sources / References
- [Official Website](https://agentskills.io)
- [GitHub Repository](https://github.com/anthropics/skills)
- [Anthropic News: Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude 4.8 Opus Release Notes](https://www.anthropic.com/news/claude-4-8-opus)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
