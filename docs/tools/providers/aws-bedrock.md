# AWS Bedrock

## What it is
AWS Bedrock is a fully managed service from Amazon Web Services that makes foundational models (FMs) available through an API. It provides a single interface to access models from leading AI providers including Amazon, Anthropic, AI21 Labs, Cohere, Meta, Mistral AI, and Stability AI.

## What problem it solves
It simplifies the process of building and scaling generative AI applications by removing the need to manage underlying infrastructure. It provides a unified API for multiple models, along with tools for fine-tuning, RAG (Knowledge Bases for Amazon Bedrock), and agentic workflows (Agents for Amazon Bedrock).

## Where it fits in the stack
**Provider / Infrastructure**. It serves as an enterprise-grade gateway to multiple high-performance LLMs.

## Typical use cases
- **Enterprise AI Applications**: Building secure, scalable AI solutions within the AWS ecosystem.
- **Retrieval-Augmented Generation (RAG)**: Using "Knowledge Bases for Amazon Bedrock" to connect models to proprietary data.
- **Agentic Workflows**: Deploying autonomous agents that can execute multi-step tasks using AWS resources.
- **Model Fine-tuning**: Customizing foundation models with private data.

## Strengths
- **Enterprise-Grade Security**: Strong data privacy and compliance features (HIPAA, GDPR, etc.). Data is not used to train the underlying foundation models.
- **Model Variety**: Access to a broad range of models (Claude, Llama, Mistral, Titan) through a single API.
- **Serverless Experience**: No infrastructure to manage; scales automatically.
- **AWS Integration**: Seamless integration with S3, Lambda, IAM, and other AWS services.

## Limitations
- **AWS Ecosystem Lock-in**: Deeply tied to AWS; moving to another provider requires significant re-engineering.
- **Complexity**: AWS's extensive configuration options can be daunting for simple projects.
- **Regional Availability**: Not all models or features are available in all AWS regions.

## When to use it
- When building enterprise-scale AI applications that require high security, compliance, and scalability.
- If your organization is already heavily invested in the AWS ecosystem.
- When you need a managed RAG or agent framework that integrates natively with cloud resources.

## When not to use it
- For simple, low-volume projects where a direct API like OpenAI or Anthropic might be simpler.
- If you require a provider-agnostic solution that can easily move between clouds.

## Related tools / concepts
- [Anthropic (Claude)](anthropic.md)
- [Meta (Llama)](../ai_knowledge/local_llms.md)
- [Mistral AI](mistral.md)
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md)
- [Docker](../infrastructure/docker.md)

## Sources / References
- [Official AWS Bedrock Page](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)

## Contribution Metadata
- Last reviewed: 2026-04-06
- Confidence: high
