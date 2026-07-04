# AWS Bedrock

## What it is
AWS Bedrock is a fully managed service from Amazon Web Services that makes foundational models (FMs) available through an API. It provides a single interface to access models from leading AI providers including Amazon, Anthropic, AI21 Labs, Cohere, Meta, Mistral AI, and Stability AI. In July 2026, it is a primary enterprise gateway for deploying models like Claude 4.8 Opus, [Gemma 3](../ai_knowledge/local_llms.md), and Llama 4 Maverick, now featuring native support for the NVIDIA Rubin architecture and [MCP 3.0](../../automation_orchestration/mcp.md) tool integration.

## What problem it solves
It simplifies the process of building and scaling generative AI applications by removing the need to manage underlying infrastructure. It provides a unified API for multiple models, along with tools for fine-tuning, RAG (Knowledge Bases for Amazon Bedrock), and agentic workflows (Agents for Amazon Bedrock). It addresses enterprise concerns regarding data privacy, security, and high-performance execution on next-generation hardware.

## Where it fits in the stack
**Provider / Infrastructure**. It serves as an enterprise-grade gateway and orchestration layer for high-performance LLMs, often paired with [Docker](../infrastructure/docker.md) for specialized containerized deployments.

## Typical use cases
- **Enterprise AI Applications**: Building secure, scalable AI solutions within the AWS ecosystem.
- **Retrieval-Augmented Generation (RAG)**: Using "Knowledge Bases for Amazon Bedrock" to connect models to proprietary S3-hosted data.
- **Agentic Workflows**: Deploying autonomous agents that leverage the [MCP 3.0](../../automation_orchestration/mcp.md) Task Protocol to execute multi-step tasks across AWS resources.
- **Hardware-Accelerated Inference**: Utilizing NVIDIA Rubin GPUs for ultra-low latency inference of frontier models.

## Strengths
- **Enterprise-Grade Security**: Strong data privacy and compliance features (HIPAA, GDPR, etc.). Data is not used to train the underlying foundation models.
- **Model Variety**: Access to [Gemma 3](../ai_knowledge/local_llms.md), Claude 4.8, and Llama 4 through a single API.
- **NVIDIA Rubin Support**: Optimized for the latest GPU architectures to provide superior price-performance.
- **AWS Integration**: Seamless integration with S3, Lambda, IAM, and [MCP 3.0](../../automation_orchestration/mcp.md) servers.
- **Managed RAG**: Built-in support for automated vectorization and retrieval via Knowledge Bases.

## Limitations
- **AWS Ecosystem Lock-in**: Deeply tied to AWS; moving to another provider requires significant re-engineering (unless using [LiteLLM](../../services/litellm.md)).
- **Configuration Complexity**: AWS's extensive IAM and VPC requirements can be daunting for smaller teams.
- **Regional Availability**: Newest models (e.g., [Gemma 3](../ai_knowledge/local_llms.md)) and Rubin-based instances may not be available in all regions simultaneously.
- **API Latency**: Managed service overhead can be slightly higher than direct-to-metal self-hosting via [vLLM](../infrastructure/vllm.md).

## When to use it
- When building enterprise-scale AI applications requiring high security, compliance, and AWS-native scalability.
- If your organization is already standardized on the AWS ecosystem.
- When you need a managed RAG or agent framework that integrates natively with cloud resources via [MCP 3.0](../../automation_orchestration/mcp.md).
- For multi-model applications requiring a unified billing and security model.

## When not to use it
- For simple, low-volume projects where a direct API (OpenAI/Anthropic) is faster to implement.
- If you require a provider-agnostic solution (consider [LiteLLM](../../services/litellm.md)).
- When you need the absolute lowest latency possible for real-time applications (consider [vLLM](../infrastructure/vllm.md) on EC2).

## Getting started

### 1. Prerequisites
- An AWS account with Bedrock model access enabled.
- AWS CLI configured with appropriate credentials.
- Python 3.9+ and `boto3`.

### 2. Installation
```bash
pip install boto3
```

### 3. Hello-world task (Python)
```python
import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

# Note: Model IDs follow the July 2026 technical context.
prompt = "Explain the benefit of MCP 3.0 in one sentence."
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": prompt}]
})

response = bedrock.invoke_model(
    body=body,
    modelId='anthropic.claude-4-8-opus-20260528-v1:0'
)

response_body = json.loads(response.get('body').read())
print(response_body['content'][0]['text'])
```

## CLI examples
Commonly used commands for inspecting model availability and performing quick tests.

```bash
# List available foundation models (including Gemma 3)
aws bedrock list-foundation-models --region us-east-1

# Get details for a specific model
aws bedrock get-foundation-model --model-identifier google.gemma-3-27b-it-v1:0

# Invoke a model via CLI and save output
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-4-8-opus-20260528-v1:0 \
  --body '{"anthropic_version": "bedrock-2023-05-31", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello Bedrock!"}]}' \
  output.txt

# List Knowledge Bases for RAG
aws bedrock-agent list-knowledge-bases
```

## API examples
Using the `boto3` SDK for streaming responses and [MCP 3.0](../../automation_orchestration/mcp.md) tool integration.

### Streaming Response
```python
import boto3
import json

client = boto3.client(service_name='bedrock-runtime')

def stream_response(prompt):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = client.invoke_model_with_response_stream(
        modelId='anthropic.claude-4-8-opus-20260528-v1:0',
        body=body
    )

    for event in response.get('body'):
        chunk = json.loads(event.get('chunk').get('bytes'))
        if chunk['type'] == 'content_block_delta':
            print(chunk['delta']['text'], end='', flush=True)

stream_response("Write a short poem about the NVIDIA Rubin architecture.")
```

### Knowledge Base Retrieval
```python
import boto3

agent_client = boto3.client(service_name='bedrock-agent-runtime')

def retrieve_from_kb(kb_id, query):
    response = agent_client.retrieve(
        knowledgeBaseId=kb_id,
        retrievalQuery={'text': query}
    )
    return response['results']
```

## Related tools / concepts
- [Anthropic (Claude)](anthropic.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Mistral AI](mistral.md)
- [MCP 3.0](../../automation_orchestration/mcp.md) - Protocol for tool-calling integration.
- [Docker](../infrastructure/docker.md) - For consistent deployment.
- [LiteLLM](../../services/litellm.md) - Multi-cloud abstraction.
- [vLLM](../infrastructure/vllm.md) - Self-hosting alternative.
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md) - Tooling for Bedrock agents.

## Sources / references
- [Official AWS Bedrock Page](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Boto3 Bedrock Runtime Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [AWS News: NVIDIA Rubin Support on Bedrock](https://aws.amazon.com/blogs/aws/nvidia-rubin-support-announcement/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
