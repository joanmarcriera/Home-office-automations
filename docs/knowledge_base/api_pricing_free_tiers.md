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

## Model-level quota tracker (expanded list)

This table incorporates your submitted model list and marks each row by verification strength:

- `Verified` = core limits are visible in official docs.
- `Partially verified` = provider free-tier stance is verified, but model-level quotas are dynamic or not fully published.
- `Unverified` = values come from community reports or account-specific observations not explicitly documented.

`Code Generation Quality` is a subjective field and is treated as community-assessed, not an official benchmark metric.

| Provider | Model | Free Context Length | RPM | RPD | TPM | Daily Token Limit | Code Generation Quality | Account Type Required | Special Notes | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Google Gemini | Gemini 2.5 Pro | 1M tokens | 5 | 100 | 250K | ~25M | Excellent | Google account | Commercial API usage supported; availability can vary by region/compliance. | Verified |
| Google Gemini | Gemini 2.5 Flash | 1M tokens | 10 | 250 | 250K | ~62.5M | Very Good | Google account | User-submitted RPM=15; official published RPM is 10 for free tier. | Verified |
| Google Gemini | Gemini 2.5 Flash-Lite | 1M tokens | 15 | 1000 | 250K | ~250M | Good | Google account | Highest free-tier RPD among listed Gemini 2.5 text models. | Verified |
| OpenAI | GPT-4o | 128K (API model context) | Tier-dependent | Tier-dependent | Tier-dependent | Tier-dependent | Excellent | OpenAI account | No standing public free API tier documented; web app limits differ from API limits. | Partially verified |
| OpenAI | GPT-4o mini | 128K | Tier-dependent | Tier-dependent | Tier-dependent | Tier-dependent | Very Good | OpenAI account | API limits depend on trust/rate-limit tier and account status. | Partially verified |
| Anthropic Claude | Claude 3.5 Sonnet | 200K | Tier-dependent | Tier-dependent | Tier-dependent | Tier-dependent | Excellent | Anthropic console account | Tier 1 requires credit purchase; monthly spend caps depend on usage tier. | Partially verified |
| Anthropic Claude | Claude 3 Haiku | 200K | Tier-dependent | Tier-dependent | Tier-dependent | Tier-dependent | Good | Anthropic console account | User-submitted fixed daily/token caps are not publicly fixed across all accounts. | Partially verified |
| Groq | Llama 3.3 70B (llama-3.3-70b-versatile) | 128K | 30 | 1000 | 12K | 100K | Very Good | Groq account (no CC for free tier) | User-submitted RPD (14,400) does not match current official free-plan row for this model. | Verified |
| Groq | Llama 4 Maverick 17B | 128K | 30 | 1000 | 6K | 500K | Good | Groq account (no CC for free tier) | Fast inference; exact limits are model-specific and can change. | Verified |
| Groq | Qwen3 32B | 128K | 30 | 14,400 | 6K | 500K | Good | Groq account (no CC for free tier) | Some Qwen/Groq model IDs and limits vary by release. | Partially verified |
| Groq | Compound AI (groq/compound) | 128K | 30 | 250 | 70K | Not published | Good | Groq account (no CC for free tier) | Official limits table does not publish a TPD value for this row. | Verified |
| Together AI | Llama 4 Maverick | 131K | Tier-dependent | Tier-dependent | Tier-dependent | Tier-dependent | Very Good | Together account + paid credits | Official docs currently state no free trial; minimum paid credit purchase required. | Verified |
| Together AI | DeepSeek V3.1 | 64K | Tier-dependent | Tier-dependent | Tier-dependent | Tier-dependent | Excellent | Together account + paid credits | User-submitted “$100 signup credits” conflicts with current official billing docs. | Verified |
| Together AI | Mistral Small 3 | 128K | Tier-dependent | Tier-dependent | Tier-dependent | Tier-dependent | Good | Together account + paid credits | Build-tier limits are spend-based; no standing free tier. | Verified |
| Hugging Face | Various open models | Varies by model | Provider-dependent | Provider-dependent | Provider-dependent | Monthly credit-based | Varies | Hugging Face account | HF routes to multiple providers; free monthly credits are small and subject to change. | Verified |
| Hugging Face | Pro-tier routed providers | Varies by model | Higher than free (provider-dependent) | Provider-dependent | Provider-dependent | Credit-based | Very Good | Hugging Face Pro | PRO adds higher monthly included credits and pay-as-you-go capabilities. | Verified |
| Mistral AI | Mistral Nemo 12B | Model-dependent | Plan-dependent | Plan-dependent | Plan-dependent | Plan-dependent | Good | Mistral account (Experiment/Scale) | Free Experiment plan exists; exact per-model quotas are not publicly fixed in one table. | Partially verified |
| Mistral AI | Mistral Small 3.1 | 128K | Plan-dependent | Plan-dependent | Plan-dependent | Plan-dependent | Good | Mistral account (Experiment/Scale) | Model access and limits vary by plan and may evolve. | Partially verified |
| Mistral AI | Codestral | 32K | Plan-dependent | Plan-dependent | Plan-dependent | Plan-dependent | Excellent | Mistral account (Experiment/Scale) | Code-oriented model; plan quotas are account-specific. | Partially verified |
| Mistral AI | Mistral Large 3 | 128K | Plan-dependent | Plan-dependent | Plan-dependent | Plan-dependent | Excellent | Mistral account (Experiment/Scale) | Frontier-tier capabilities typically tied to paid/scale plans. | Partially verified |
| DeepSeek | DeepSeek V3.2 (deepseek-chat) | 128K | Not published | Not published | Not published | Not published | Excellent | DeepSeek account | Pricing + granted balance behavior is documented; standing free-tier quotas are not clearly published. | Partially verified |
| DeepSeek | DeepSeek R1 / reasoner | 128K | Not published | Not published | Not published | Not published | Excellent | DeepSeek account | User-submitted “5M free tokens on signup” not confirmed in official public pricing docs. | Unverified |
| Cohere | Command R7B | 128K | 20 (trial chat) | ~1000/month (trial key total calls) | Endpoint-dependent | 1000 trial calls/month | Good | Cohere account (trial key) | Trial keys are free and limited; production keys are paid and much higher throughput. | Verified |
| Cohere | Command R+ | 128K | 20 (trial chat) | ~1000/month (trial key total calls) | Endpoint-dependent | 1000 trial calls/month | Very Good | Cohere account (trial key) | Monthly trial cap applies account-wide for trial keys. | Verified |
| OpenRouter | Qwen3 Coder 480B (:free variant when available) | Model-dependent | 20 | 50/day (<$10 credits) or 1000/day (>= $10 credits) | Not published | Not published | Excellent | OpenRouter account | Free model limits are account-plan based rather than fixed per-model quotas. | Verified |
| OpenRouter | GPT-OSS-120B (:free variant when available) | Model-dependent | 20 | 50/day or 1000/day (with >=$10 credits) | Not published | Not published | Very Good | OpenRouter account | Availability of specific free variants can change over time. | Verified |
| OpenRouter | Llama 3.3 70B (:free variant when available) | Model-dependent | 20 | 50/day or 1000/day (with >=$10 credits) | Not published | Not published | Very Good | OpenRouter account | Free router/model pool is dynamic. | Verified |
| OpenRouter | Mistral Small 3.1 (:free variant when available) | Model-dependent | 20 | 50/day or 1000/day (with >=$10 credits) | Not published | Not published | Good | OpenRouter account | Free inference is suitable for low-volume experimentation only. | Verified |
| OpenRouter | DeepSeek R1 (:free variant when available) | Model-dependent | 20 | 50/day or 1000/day (with >=$10 credits) | Not published | Not published | Excellent | OpenRouter account | User-submitted RPD=200 differs from current documented free-plan policy. | Verified |
| Cerebras | Llama 4 Maverick 400B | 128K (paid tier; model-specific) | 30 (typical free rows) | 14,400 (typical free rows) | 60K (typical free rows) | 1M/day (free tier) | Very Good | Cerebras account | Model-specific limits/context can differ; check model page + limits page. | Partially verified |
| Cerebras | Qwen3 Coder 235B | 64K free / 131K paid (model-dependent) | 30 | 14,400 | 60K | 1M/day | Excellent | Cerebras account | User-submitted coder-centric speed/capacity notes align with Cerebras model pages/blog signals. | Partially verified |
| Cerebras | Llama 3.1 8B | 8K free / 32K paid | 30 | 14,400 | 60K | 1M/day | Good | Cerebras account | Free tier is clearly documented with per-model limits in model pages. | Verified |
| xAI Grok | Grok 4.1 Fast | Model-dependent | Credit-dependent | Credit-dependent | Credit-dependent | Credit-dependent | Very Good | xAI account | xAI docs confirm promotional/free credits may exist, but fixed `$25` startup credits are not consistently documented. | Unverified |

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
- [OpenRouter API rate limits](https://openrouter.ai/docs/api-reference/limits/)
- [OpenRouter Free Models Router](https://openrouter.ai/docs/guides/routing/routers/free-models-router)
- [xAI API](https://x.ai/api)
- [xAI Models/Pricing docs](https://docs.x.ai/docs/models)
- [xAI Billing](https://docs.x.ai/docs/billing)
- [Z.ai Model Pricing](https://docs.z.ai/guides/model-pricing)
- [Alibaba Model Studio billing](https://www.alibabacloud.com/help/en/model-studio/product-overview/billing-of-model-studio)
- [Alibaba Model pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)
- [Cohere Pricing](https://cohere.com/pricing)
- [Cohere trial/production key rate limits](https://docs.cohere.com/docs/rate-limits)
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
- [Google Gemini rate limits](https://ai.google.dev/gemini-api/docs/quota)
- [Groq rate limits](https://console.groq.com/docs/rate-limits)
- [Cerebras rate limits](https://inference-docs.cerebras.ai/support/rate-limits)
- [ChatGPT shared context (title only)](https://chatgpt.com/share/69a760fd-3520-8000-bfbd-19bdf623a333)

## Contribution Metadata

- Last reviewed: 2026-03-03
- Confidence: medium
