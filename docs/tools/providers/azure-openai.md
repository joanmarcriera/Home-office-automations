# Azure OpenAI Service

## What it is
Azure OpenAI Service provides REST API access to OpenAI's powerful language models including GPT-4o, GPT-4o-mini, and the latest 2026 models (GPT-5 series), with the enterprise capabilities of Microsoft Azure.

## What problem it solves
It allows enterprise organizations to use advanced LLMs with improved security, compliance, and data residency guarantees. It enables the use of existing Entra ID (formerly Azure AD) infrastructure for fine-grained access control.

## Where it fits in the stack
**Model Provider / Infrastructure Layer**. It serves as the primary endpoint for LLM capabilities in enterprise or hybrid-cloud environments.

## Typical use cases
- **Enterprise RAG**: Securely querying private data indexed in Azure AI Search.
- **Internal Tools**: Powering internal company agents with corporate identity integration.
- **Compliance-Heavy Apps**: Building AI features that must adhere to strict regulatory standards (HIPAA, GDPR).

## Strengths
- **Security**: Integration with Azure VNet, Private Link, and Entra ID.
- **SLA**: Enterprise-grade availability and performance guarantees.
- **Data Privacy**: Customer data is not used to train global OpenAI models.

## Limitations
- **Latency**: Can sometimes be higher than direct OpenAI API due to regional routing.
- **Complexity**: Resource/Deployment management adds overhead compared to simple API keys.

## When to use it
- When you require enterprise-grade security, data privacy, and compliance (HIPAA, SOC2, etc.).
- When you need to integrate LLMs with existing Azure infrastructure and Entra ID (Azure AD).
- When you need predictable performance and availability guaranteed by Microsoft SLAs.

## When not to use it
- For simple, non-enterprise projects where a low-latency direct API key is sufficient.
- If you prefer to avoid the complexity of managing Azure resources and deployments.
- If you need immediate access to new OpenAI models that may take time to roll out to all Azure regions.

## Getting started

### Minimal Concepts
1.  **Resource**: The Azure OpenAI instance created in your subscription.
2.  **Deployment**: A specific model instance (e.g., `gpt-4o-2024-05-13`) that has its own capacity limits.
3.  **Endpoint**: The unique URL for your resource (e.g., `https://my-resource.openai.azure.com/`).

### Installation
```bash
pip install openai azure-identity
```

### Python Example (Entra ID)
```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="my-gpt-4o-deployment",
    messages=[{"role": "user", "content": "Hello world"}]
)
```

## CLI examples
Azure OpenAI management is typically handled via the `az` CLI.

```bash
# List all Azure OpenAI accounts in a resource group
az cognitiveservices account list -g my-resource-group --query "[?kind=='OpenAI']"

# Create a new deployment for GPT-4o
az cognitiveservices account deployment create \
   -g my-resource-group \
   -n my-openai-resource \
   --deployment-name my-gpt4o \
   --model-name gpt-4o \
   --model-version "2024-05-13" \
   --model-format OpenAI \
   --sku-capacity 10 \
   --sku-name "Standard"

# Get the endpoint URL and API keys
az cognitiveservices account show -n my-openai-resource -g my-resource-group --query "properties.endpoint"
az cognitiveservices account keys list -n my-openai-resource -g my-resource-group
```

## API examples
The Azure OpenAI API is compatible with the standard OpenAI SDK, requiring minor configuration for the endpoint and version.

### Streaming Chat Completion (Python)
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="YOUR_AZURE_OPENAI_KEY",
    api_version="2024-02-15-preview",
    azure_endpoint="https://YOUR_RESOURCE_NAME.openai.azure.com/"
)

response = client.chat.completions.create(
    model="gpt-4o", # Deployment name
    messages=[{"role": "user", "content": "Explain quantum entanglement."}],
    stream=True
)

for chunk in response:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Related tools / concepts
- [OpenAI](../ai_knowledge/openai.md)
- [Microsoft Graph API](microsoft-graph.md)
- [Vercel AI Gateway](vercel-ai-gateway.md)
- [Anthropic](anthropic.md)
- [Mistral](mistral.md)
- [Together](together.md)
- [Fireworks](fireworks.md)
- [Groq](groq.md)

## Sources / References
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Microsoft Entra ID Overview](https://learn.microsoft.com/en-us/entra/fundamentals/whatis)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
