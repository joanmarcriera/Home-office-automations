# Azure OpenAI Service

## What it is
Azure OpenAI Service provides REST API access to OpenAI's powerful language models including GPT-4o, GPT-4o-mini, and the latest 2026 models (GPT-5 series), with the enterprise capabilities of Microsoft Azure.

## What problem it solves
It allows enterprise organizations to use advanced LLMs with improved security, compliance, and data residency guarantees. It enables the use of existing Entra ID (formerly Azure AD) infrastructure for fine-grained access control.

## Where it fits in the stack
**Model Provider / Infrastructure Layer**. It serves as the primary endpoint for LLM capabilities in enterprise or hybrid-cloud environments.

## Authentication Patterns

### 1. API Key Authentication
The simplest method, using a secret key provided in the Azure Portal.
- **Header**: `api-key: YOUR_KEY`
- **Use Case**: Quick prototyping or services that do not support OAuth.

### 2. Entra ID (Formerly Azure AD) Authentication
The recommended method for production environments, leveraging managed identities and service principals.
- **Mechanism**: OAuth 2.0 Bearer tokens.
- **Benefit**: No long-lived secrets; audit trails linked to identities; automatic rotation.

## Typical use cases
- **Enterprise RAG**: Securely querying private data indexed in Azure AI Search.
- **Internal Tools**: Powering internal company agents with corporate identity integration.
- **Compliance-Heavy Apps**: Building AI features that must adhere to strict regulatory standards (HIPAA, GDPR).

## Getting started

### Minimal Concepts
1.  **Resource**: The Azure OpenAI instance created in your subscription.
2.  **Deployment**: A specific model instance (e.g., `gpt-4o-2024-05-13`) that has its own capacity limits.
3.  **Endpoint**: The unique URL for your resource (e.g., `https://my-resource.openai.azure.com/`).

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

## Strengths
- **Security**: Integration with Azure VNet, Private Link, and Entra ID.
- **SLA**: Enterprise-grade availability and performance guarantees.
- **Data Privacy**: Customer data is not used to train global OpenAI models.

## Limitations
- **Latency**: Can sometimes be higher than direct OpenAI API due to regional routing.
- **Complexity**: Resource/Deployment management adds overhead compared to simple API keys.

## Related tools / concepts
- [OpenAI](../ai_knowledge/openai.md)
- [Microsoft Graph API](microsoft-graph.md)
- [Vercel AI Gateway](vercel-ai-gateway.md)

## Sources / References
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Microsoft Entra ID Overview](https://learn.microsoft.com/en-us/entra/fundamentals/whatis)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
