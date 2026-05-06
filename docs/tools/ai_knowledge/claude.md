# Claude

## What it is
Claude is a family of foundational large language models developed by Anthropic. It is designed to be helpful, honest, and harmless, with a strong focus on safety, steerability, and high-performance reasoning.

## What problem it solves
Claude provides state-of-the-art conversational and reasoning capabilities. It excels at complex tasks such as coding, creative writing, and data analysis, often with a more "human" and less robotic tone than other models. Its large context window allows it to process entire books or codebases in a single prompt.

## Where it fits in the stack
AI Model and Conversational Assistant. It can be accessed via the Claude.ai web interface, the Anthropic API, or through providers like AWS Bedrock and Google Cloud Vertex AI.

## Typical use cases
- Advanced coding assistance and software engineering tasks.
- Summarizing and analyzing large documents or datasets.
- Creative and technical writing.
- Building agentic workflows using its strong tool-calling capabilities.

## Strengths
- **Reasoning**: Particularly strong at logic and coding.
- **Tone**: Often perceived as more natural and nuanced than ChatGPT.
- **Context Window**: Supports very large contexts (up to 200k+ tokens).
- **Safety**: Built with "Constitutional AI" principles.

## Limitations
- **Availability**: Web interface access can be restricted in some regions.
- **Rate Limits**: Can be strict on the free tier.
- **Closed Source**: The model weights and training data are proprietary.

## When to use it
- When you need high-precision reasoning or coding assistance.
- When you are working with very long documents that exceed standard context limits.
- When you prefer a more conversational and less "assistant-like" tone.

## When not to use it
- If you require a fully local, offline model (use [Local LLMs](local_llms.md)).
- If you need a model with no censorship or safety filters.

## Licensing and cost
- **Open Source**: No (Proprietary).
- **Cost**: Free tier available; paid "Pro" subscription for higher limits; pay-as-you-go API.
- **Self-hostable**: No.

## Related tools / concepts
- [ChatGPT](chatgpt.md)
- [Gemini](gemini.md)
- [Anthropic](../providers/anthropic.md)
- [Claude Code](../development_ops/claude-code.md)
- [Everything Claude Code](everything-claude-code.md)
- [Claude How-To](claude-howto.md)

## Sources / References
- [Official Website](https://claude.ai/)
- [Anthropic Website](https://www.anthropic.com/)
- [Claude Documentation](https://docs.anthropic.com/claude/docs)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-28
