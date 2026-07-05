# Anthropic Agent Skills

## What it is
Anthropic Agent Skills are encapsulated "micro-playbooks" consisting of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. They teach Claude how to complete specific tasks in a repeatable way, following the [Agent Skills](https://agentskills.io) specification. By July 2026, they have evolved to support multi-model orchestration, often used in conjunction with **Gemma 3** for local processing and **Claude 4.8 Opus** for complex reasoning.

## What problem it solves
It addresses the need for repeatable, high-performance execution of specialized tasks by agents. Instead of relying on general model knowledge or long, brittle system prompts, skills provide structured instructions and validated tools tailored to specific domains. This reduces hallucinations and ensures "System 2" reasoning is applied consistently, especially when integrated with the **MCP 3.0 Task Protocol** for automated execution.

## Where it fits in the stack
**Agent / Tool / Pattern**. It acts as a standardized way to equip autonomous agents with specialized capabilities, sitting between the core model (e.g., **Claude 4.8 Opus**) and the specific application logic. It increasingly interfaces with the **MCP 3.0** ecosystem for tool discovery and execution.

## Typical use cases
- **Advanced Document Processing**: Extracting structured data from high-fidelity PDFs, manipulating DOCX files, or generating complex XLSX reports.
- **Technical Infrastructure**: Automatically generating and testing MCP servers, performing security audits on local code, or automating multi-repo data analysis.
- **Enterprise Workflows**: Enforcing brand guidelines in multi-channel communications or automating internal financial reporting.
- **Research & Synthesis**: Performing deep-research loops using tools like [DeerFlow](deerflow.md).
- **Automated Benchmarking**: Running standardized evals using the MCP 3.0 Task Protocol.

## Strengths
- **Repeatability**: Ensures consistent behavior for specialized tasks across different sessions and users.
- **Standardized**: Follows the `agentskills.io` specification, making skills interoperable across different agent harnesses like [Claude Code](../development_ops/claude-code.md) or [Aider](../development_ops/aider.md).
- **Discovery**: Uses YAML frontmatter for easy discovery and automated selection by agent routers.
- **Extensible**: Allows developers to create custom skills using a simple Markdown-based template and local Python/TypeScript scripts.
- **Task Protocol Support**: Native integration with MCP 3.0 for structured task management.

## Limitations
- **Model Dependent**: Highly optimized for the Claude family of models; performance may vary on other frontier models like **GPT-5.5** or **Gemma 3**.
- **Execution Environment**: Requires a local or sandboxed execution environment (like a Docker container) for the associated scripts to run.
- **Licensing**: While many skills are Apache 2.0, some complex enterprise-grade skills are source-available but require specific licenses for commercial redistribution.

## When to use it
- When you need Claude to perform complex, multi-step tasks that require specific formatting, domain knowledge, or external tool execution.
- When building autonomous agent workflows that need to dynamically load and unload specialized capabilities based on user intent.
- When you want to share "best practice" agent behaviors across a team or organization.
- When implementing automated workflows that require strict adherence to the MCP 3.0 Task Protocol.

## When not to use it
- For simple, one-off tasks that can be handled by standard prompt engineering.
- If your execution environment is strictly restricted and cannot run local scripts (Python/Node.js).
- If you are using a model that does not yet support the tool-use patterns required by the Agent Skills spec (though [Gemma 3](../ai_knowledge/local_llms.md) has significantly improved this support).

## Getting started

### Installation
Clone the official skills repository or create your own skills directory:
```bash
git clone https://github.com/anthropics/skills.git
```

### Configuration
Configure your agent (e.g., [Claude Code](../development_ops/claude-code.md)) to point to your skills directory. The agent will automatically index the `SKILL.md` files.

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
# In July 2026, Claude 4.8 Opus is the recommended model for skill execution.
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-4-8-opus-20260528",
    max_tokens=4096,
    system="Use the 'document-processing' skill located in /path/to/skills.",
    messages=[{"role": "user", "content": "Extract text from report.pdf"}]
)
```

## Related tools / concepts
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Claude Code](../development_ops/claude-code.md)
- [Aider](../development_ops/aider.md)
- [Roo Code](roo-code.md)
- [Cline](cline.md)
- [Documentation Writer Skill](documentation-writer.md)
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Gemma 3](../ai_knowledge/local_llms.md)

## Sources / References
- [Official Website](https://agentskills.io)
- [GitHub Repository](https://github.com/anthropics/skills)
- [Anthropic News: Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
