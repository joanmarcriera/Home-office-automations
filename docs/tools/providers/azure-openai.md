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

### 1. Installation
Install the official Azure OpenAI and identity libraries:
```bash
pip install openai azure-identity
```

### 2. Resource Creation
Create an Azure OpenAI resource in the [Azure Portal](https://portal.azure.com/). Note your **Endpoint** (e.g., `https://my-resource.openai.azure.com/`) and **Key**.

### 3. Model Deployment
Deploy a model (e.g., `gpt-4o`) within your resource. The **Deployment Name** is required for all API calls.

### Hello World Example
Test your deployment using `curl`:
```bash
curl "https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/chat/completions?api-version=2024-02-15-preview" \
  -H "Content-Type: application/json" \
  -H "api-key: YOUR_API_KEY" \
  -d '{"messages": [{"role": "user", "content": "Hello world"}]}'
```

## CLI examples
```bash
# List all Azure OpenAI resources in your subscription
az cognitiveservices account list --kind OpenAI

# Create a new deployment via Azure CLI
az cognitiveservices account deployment create \
   --name my-resource-name \
   --resource-group my-resource-group \
   --deployment-name my-gpt4-deployment \
   --model-name gpt-4 \
   --model-version "0613" \
   --model-format OpenAI

# Get the endpoint and keys for a resource
az cognitiveservices account show --name my-resource-name --resource-group my-resource-group --query "properties.endpoint"
az cognitiveservices account keys list --name my-resource-name --resource-group my-resource-group
```

## API examples

### Python (Entra ID / Recommended)
Uses managed identities to avoid long-lived secrets:
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

### Node.js (Standard API Key)
```javascript
const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

const client = new OpenAIClient(
  "https://YOUR_RESOURCE_NAME.openai.azure.com/",
  new AzureKeyCredential("YOUR_API_KEY")
);

async function main() {
  const { choices } = await client.getChatCompletions("YOUR_DEPLOYMENT_NAME", [
    { role: "user", content: "Hello from Node.js" }
  ]);
  console.log(choices[0].message.content);
}
main();
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
