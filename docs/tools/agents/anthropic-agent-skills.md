# Anthropic Agent Skills

## What it is
Anthropic Agent Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. They teach Claude how to complete specific tasks in a repeatable way, following the [Agent Skills](https://agentskills.io) specification.

## What problem it solves
It addresses the need for repeatable, high-performance execution of specialized tasks by agents. Instead of relying on general model knowledge, skills provide structured instructions and tools tailored to specific domains like document processing, technical testing, or creative workflows.

## Where it fits in the stack
**Agent / Tool / Pattern**. It acts as a standardized way to equip autonomous agents with specialized capabilities.

## Typical use cases
- **Document Processing**: Extracting data from PDFs, manipulating DOCX files, or generating XLSX reports.
- **Technical Tasks**: Testing web applications, generating MCP servers, or automating data analysis.
- **Enterprise Workflows**: Maintaining brand guidelines in communications or automating internal reporting.

## Strengths
- **Repeatability**: Ensures consistent behavior for specialized tasks across different sessions.
- **Standardized**: Follows the `agentskills.io` specification, making skills interoperable.
- **Discovery**: Uses YAML frontmatter (`name`, `description`) for easy discovery by agent routers.
- **Extensible**: Allows developers to create custom skills using a simple Markdown-based template.

## Limitations
- **Model Dependent**: Optimized for the Claude family of models.
- **Closed Source (Some)**: While many are Apache 2.0, some complex skills (like document processing) are source-available but not open source.
- **Environment Specific**: Some skills may require specific tools or environments (e.g., Python, specialized libraries) to execute.

## When to use it
- When you need Claude to perform complex, multi-step tasks that require specific formatting or domain knowledge.
- When building autonomous agent workflows that need to dynamically load and unload specialized capabilities.

## When not to use it
- For simple, one-off tasks that don't require specialized instructions.
- If using an LLM provider that does not support the Agent Skills specification.

## Licensing and cost
- **Open Source**: Mixed (Apache 2.0 for examples, Source-available for core document skills)
- **Cost**: Free to use (requires Anthropic API access or Claude.ai subscription)
- **Self-hostable**: Yes (Skills are local files)

## Getting started

### Installation
Clone the official skills repository or create your own skills directory:
```bash
git clone https://github.com/anthropics/skills.git
```

### Usage
Configure your agent (e.g., Claude Code) to point to your skills directory. Claude will automatically index the `SKILL.md` and associated scripts.

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
# Example of referencing a skill in a message
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-7-sonnet-latest",
    max_tokens=1024,
    system="Use the 'document-processing' skill located in /path/to/skills.",
    messages=[{"role": "user", "content": "Extract text from report.pdf"}]
)
```

## Related tools / concepts
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Documentation Writer Skill](documentation-writer.md)

## Sources / References
- [Official Website](https://agentskills.io)
- [GitHub Repository](https://github.com/anthropics/skills)
- [Anthropic News: Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Contribution Metadata
- Last reviewed: 2026-05-21
- Confidence: high
