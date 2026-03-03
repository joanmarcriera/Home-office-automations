# API Pricing & Free Tier Matrix

This is the canonical tracker for API pricing links and free-tier availability across LLM providers and API platforms.

## Scope and usage

- Focus: API access (not consumer chat subscriptions unless directly tied to API credits).
- Purpose: provider comparison, budgeting, and long-term maintenance reference.
- Update target: monthly, and after major provider announcements.

## Status legend

- `Yes` = official free tier/trial access is currently documented.
- `Partial` = limited free usage exists (for example, selected models/features).
- `No` = no current free trial/tier is documented.
- `Unclear` = pricing/billing docs do not clearly confirm a standing free tier.

## Canonical pricing matrix (last verified: 2026-03-03)

| Provider / Platform | API docs | Pricing link | Free tier / trial | Evidence summary | Last verified |
| :--- | :--- | :--- | :--- | :--- | :--- |
| OpenAI | [Platform docs](https://platform.openai.com/docs) | [API pricing](https://openai.com/api/pricing/) | No | API is usage-priced; prepaid billing docs require purchased credits (minimum purchase described). | 2026-03-03 |
| Anthropic (Claude API) | [Claude docs](https://docs.anthropic.com/) | [API pricing](https://platform.claude.com/docs/en/about-claude/pricing) | Yes | Pricing FAQ states new users get a small amount of free API credits to start. | 2026-03-03 |
| Google Gemini Developer API | [Gemini API docs](https://ai.google.dev/gemini-api/docs) | [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) | Yes | Pricing tables include Free Tier rows with "Free of charge" for supported usage. | 2026-03-03 |
| OpenRouter | [OpenRouter docs](https://openrouter.ai/docs/overview/introduction) | [OpenRouter pricing](https://openrouter.ai/pricing) | Yes | Pricing page documents a Free plan (25+ free models, free providers, daily limits). | 2026-03-03 |
| xAI (Grok API) | [xAI API docs](https://docs.x.ai/docs/overview) | [x.ai API](https://x.ai/api) | Yes | x.ai API page and docs reference monthly free requests/credits for users. | 2026-03-03 |
| Z.ai (GLM API) | [Z.ai API docs](https://docs.z.ai/) | [Model pricing](https://docs.z.ai/guides/model-pricing) | Yes | Pricing docs state new users can claim free token packages for API models. | 2026-03-03 |
| Alibaba DashScope (Qwen APIs) | [Model docs](https://www.alibabacloud.com/help/en/model-studio/getting-started/models) | [Model Studio pricing](https://www.alibabacloud.com/help/en/model-studio/product-overview/billing-of-model-studio) | Yes | Docs indicate most models provide free quota during initial release period. | 2026-03-03 |
| Cohere | [Cohere docs](https://docs.cohere.com/) | [Cohere pricing](https://cohere.com/pricing) | Yes | Pricing page states trial API key calls are free (rate-limited, non-production). | 2026-03-03 |
| Mistral AI | [Mistral docs](https://docs.mistral.ai/) | [Mistral pricing](https://mistral.ai/pricing) | Yes | Help docs describe a free Experiment plan for trying API models (no card required). | 2026-03-03 |
| Together AI | [Together docs](https://docs.together.ai/) | [Together pricing](https://www.together.ai/pricing) | No | Billing docs state there is no free trial and credits start with a paid minimum purchase. | 2026-03-03 |
| Groq | [Groq docs](https://console.groq.com/docs/overview) | [Groq pricing](https://groq.com/pricing/) | Yes | Pricing page exposes free API key; rate-limit docs include dedicated Free Plan limits. | 2026-03-03 |
| Fireworks AI | [Fireworks docs](https://fireworks.ai/docs) | [Fireworks pricing](https://fireworks.ai/pricing) | Yes | Pricing page states "Get started with $1 in free credits." | 2026-03-03 |
| Replicate | [Replicate docs](https://replicate.com/docs) | [Replicate pricing](https://replicate.com/pricing) | Partial | Billing docs state select models can be run for free before paid billing is required. | 2026-03-03 |
| DeepSeek API | [DeepSeek API docs](https://api-docs.deepseek.com/) | [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) | Unclear | Pricing docs reference topped-up and granted balances but no explicit standing free tier. | 2026-03-03 |
| Perplexity API | [Perplexity docs](https://docs.perplexity.ai/) | [Perplexity pricing guide](https://docs.perplexity.ai/guides/pricing) | No | Docs state usage draws from purchased credits with minimum top-up and card requirement. | 2026-03-03 |
| AI21 | [AI21 docs](https://docs.ai21.com/) | [AI21 pricing](https://www.ai21.com/pricing) | Yes | Pricing page advertises a 90-day free trial with included credits. | 2026-03-03 |
| Voyage AI | [Voyage docs](https://docs.voyageai.com/) | [Voyage pricing](https://www.voyageai.com/pricing) | Unclear | Public pricing page shows paid plans and token rates; no explicit free tier statement found. | 2026-03-03 |
| Cloudflare Workers AI | [Workers AI docs](https://developers.cloudflare.com/workers-ai/) | [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) | Yes | Pricing docs include a Free plan with daily included usage. | 2026-03-03 |
| Hugging Face Inference Providers | [HF Inference docs](https://huggingface.co/docs/inference-providers) | [HF pricing](https://huggingface.co/pricing) | Yes | HF pricing notes monthly included inference credits (amount depends on account tier). | 2026-03-03 |
| Cerebras Inference | [Cerebras docs](https://inference-docs.cerebras.ai/) | [Cerebras pricing](https://cloud.cerebras.ai/pricing) | Yes | Pricing page references monthly free usage/credits for its free tier. | 2026-03-03 |
| NVIDIA API Catalog | [NVIDIA API docs](https://build.nvidia.com/docs) | [NVIDIA API pricing](https://build.nvidia.com/pricing) | Yes | Pricing page references free credits to get started. | 2026-03-03 |
| SambaNova Cloud | [SambaNova docs](https://cloud.sambanova.ai/docs/) | [SambaNova pricing](https://cloud.sambanova.ai/pricing) | Unclear | Public pricing page exposes paid plans; no explicit free-tier policy found in listed docs. | 2026-03-03 |
| AWS Bedrock | [Bedrock docs](https://docs.aws.amazon.com/bedrock/) | [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) | No | Pricing model is pay-as-you-go with metered usage; no Bedrock-specific standing free tier listed. | 2026-03-03 |
| Azure OpenAI Service | [Azure OpenAI docs](https://learn.microsoft.com/azure/ai-services/openai/) | [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) | Unclear | Service pricing is metered; Azure account-level free credits may apply but are not an OpenAI-service-specific free tier. | 2026-03-03 |
| Vertex AI (Gemini via GCP) | [Vertex AI docs](https://cloud.google.com/vertex-ai/docs) | [Vertex AI generative pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) | Unclear | Pricing page provides metered model pricing; no persistent API free-tier statement confirmed here. | 2026-03-03 |
| OCI Generative AI | [OCI GenAI docs](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm) | [OCI pricing](https://www.oracle.com/artificial-intelligence/generative-ai/generative-ai-service/pricing/) | Unclear | Public pricing page provides paid rates; no explicit standing free-tier statement found. | 2026-03-03 |

## Notes and caveats

- Provider pricing and free-tier rules change frequently; always verify from official links before budgeting.
- Several vendors distinguish between product-level free plans and API-level free access.
- Account-level cloud credits (Azure/AWS/GCP) are not equivalent to a provider-specific API free tier.

## Maintenance protocol

When updating this page:

1. Validate each row against official docs/pricing pages.
2. Update `Free tier / trial`, `Evidence summary`, and `Last verified`.
3. Add providers only when official pricing and docs links are stable.
4. Use `Unclear` when evidence is ambiguous.

## Related pages

- [AI Tooling Landscape — 2026 Overview](ai_tooling_landscape.md)
- [Model Classes](model_classes.md)
- [OpenRouter](../tools/ai_knowledge/openrouter.md)
- [Providers Index](../tools/providers/index.md)

## Sources / References

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [OpenAI Prepaid Billing](https://help.openai.com/en/articles/8264644-how-can-i-set-up-prepaid-billing)
- [Anthropic Claude API Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [OpenRouter Pricing](https://openrouter.ai/pricing)
- [xAI API](https://x.ai/api)
- [xAI Models/Pricing docs](https://docs.x.ai/docs/models)
- [Z.ai Model Pricing](https://docs.z.ai/guides/model-pricing)
- [Alibaba Model Studio billing](https://www.alibabacloud.com/help/en/model-studio/product-overview/billing-of-model-studio)
- [Cohere Pricing](https://cohere.com/pricing)
- [Mistral Pricing](https://mistral.ai/pricing)
- [Mistral Experiment Plan (Free API)](https://help.mistral.ai/en/articles/455206-how-can-i-try-the-api-for-free-with-the-experiment-plan)
- [Together Pricing](https://www.together.ai/pricing)
- [Together Billing Credits](https://docs.together.ai/docs/billing-credits)
- [Groq Pricing](https://groq.com/pricing)
- [Groq Rate Limits](https://console.groq.com/docs/rate-limits)
- [Fireworks Pricing](https://fireworks.ai/pricing)
- [Replicate Pricing](https://replicate.com/pricing)
- [Replicate Billing](https://replicate.com/docs/topics/billing)
- [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing)
- [Perplexity API Pricing](https://docs.perplexity.ai/guides/pricing)
- [AI21 Pricing](https://www.ai21.com/pricing)
- [Voyage Pricing](https://www.voyageai.com/pricing)
- [Cloudflare Workers AI Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Hugging Face Pricing](https://huggingface.co/pricing)
- [Cerebras Pricing](https://cloud.cerebras.ai/pricing)
- [NVIDIA API Pricing](https://build.nvidia.com/pricing)
- [SambaNova Pricing](https://cloud.sambanova.ai/pricing)
- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- [Vertex AI GenAI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OCI Generative AI Pricing](https://www.oracle.com/artificial-intelligence/generative-ai/generative-ai-service/pricing/)
- [ChatGPT shared context (title only)](https://chatgpt.com/share/69a760fd-3520-8000-bfbd-19bdf623a333)

## Contribution Metadata

- Last reviewed: 2026-03-03
- Confidence: medium
