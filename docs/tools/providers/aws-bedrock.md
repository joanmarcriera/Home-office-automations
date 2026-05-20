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

## Getting started

### 1. Prerequisites
- An AWS account with Bedrock access enabled for the desired models (e.g., Anthropic Claude).
- AWS CLI configured with appropriate credentials.
- Python 3.8+ for SDK usage.

### 2. Installation
```bash
pip install boto3
```

### 3. Hello-world task (Python)
```python
import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

prompt = "Explain the benefit of AWS Bedrock in one sentence."
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": prompt}]
})

response = bedrock.invoke_model(
    body=body,
    modelId='anthropic.claude-3-sonnet-20240229-v1:0'
)

response_body = json.loads(response.get('body').read())
print(response_body['content'][0]['text'])
```

## Technical Architecture
AWS Bedrock operates as a serverless orchestrator between the user and the hosted models.
- **Bedrock Runtime**: The data plane API for model invocation and streaming.
- **Bedrock Control Plane**: The API for managing model access, custom models, and provisioning throughput.
- **Provisioned Throughput**: Allows for dedicated capacity for specific models to ensure consistent latency.
- **Knowledge Bases**: Integrates with vector databases (like Amazon OpenSearch or Aurora) for managed RAG.

## SDK Example: Streaming Response
For low-latency applications, streaming allows the UI to display tokens as they are generated.

```python
import boto3
import json

client = boto3.client(service_name='bedrock-runtime')

def stream_claude(prompt):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = client.invoke_model_with_response_stream(
        modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
        body=body
    )

    for event in response.get('body'):
        chunk = json.loads(event.get('chunk').get('bytes'))
        if chunk['type'] == 'content_block_delta':
            print(chunk['delta']['text'], end='', flush=True)

stream_claude("Write a short poem about cloud computing.")
```

## CLI Reference
Commonly used commands for inspecting model availability and performing quick tests.

```bash
# List available foundation models
aws bedrock list-foundation-models --region us-east-1

# Get details for a specific model
aws bedrock get-foundation-model --model-identifier anthropic.claude-3-5-sonnet-20240620-v1:0

# Invoke a model via CLI
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-sonnet-20240229-v1:0 \
  --body '{"anthropic_version": "bedrock-2023-05-31", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello!"}]}' \
  output.txt
```

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
- [LiteLLM](../../services/litellm.md) - Can proxy AWS Bedrock to provide an OpenAI-compatible API.
- [vLLM](../infrastructure/vllm.md) - Open-source alternative for hosting models yourself.
- [OpenCompass](../benchmarking/opencompass.md) - Can be used to evaluate models hosted on Bedrock.

## Sources / References
- [Official AWS Bedrock Page](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Boto3 Bedrock Runtime Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
