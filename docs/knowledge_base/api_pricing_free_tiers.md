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

This section is organized by provider (instead of one very wide table) for easier scanning.

- `Verified` = core limits are visible in official docs.
- `Partially verified` = provider free-tier stance is verified, but model-level quotas are dynamic or not fully published.
- `Unverified` = values come from community reports or account-specific observations not explicitly documented.

`Code Generation Quality` is subjective and treated as community-assessed, not an official benchmark metric.

Quick jump:
[Google Gemini](#google-gemini) · [OpenAI](#openai) · [Anthropic Claude](#anthropic-claude) · [Groq](#groq) · [Together AI](#together-ai) · [Hugging Face](#hugging-face) · [Mistral AI](#mistral-ai) · [DeepSeek](#deepseek) · [Cohere](#cohere) · [OpenRouter](#openrouter) · [Cerebras](#cerebras) · [xAI Grok](#xai-grok)

`Quotas` format is `context / RPM / RPD / TPM / daily token cap`.

### Google Gemini

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Gemini 2.5 Pro | `1M / 5 / 100 / 250K / ~25M` | Google account | Excellent | Verified | Region and compliance rules can affect access. |
| Gemini 2.5 Flash | `1M / 10 / 250 / 250K / ~62.5M` | Google account | Very Good | Verified | Official free-tier RPM is 10 (not 15). |
| Gemini 2.5 Flash-Lite | `1M / 15 / 1000 / 250K / ~250M` | Google account | Good | Verified | Highest free-tier RPD in listed Gemini models. |

### OpenAI

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| GPT-4o | `128K / tier-dependent / tier-dependent / tier-dependent / tier-dependent` | OpenAI account | Excellent | Partially verified | No standing public free API tier documented. |
| GPT-4o mini | `128K / tier-dependent / tier-dependent / tier-dependent / tier-dependent` | OpenAI account | Very Good | Partially verified | Limits depend on trust tier/account status. |

### Anthropic Claude

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Claude 3.5 Sonnet | `200K / tier-dependent / tier-dependent / tier-dependent / tier-dependent` | Anthropic console account | Excellent | Partially verified | Tier 1 requires purchased credits; caps vary. |
| Claude 3 Haiku | `200K / tier-dependent / tier-dependent / tier-dependent / tier-dependent` | Anthropic console account | Good | Partially verified | Fixed global daily/token caps are not published. |

### Groq

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Llama 3.3 70B (llama-3.3-70b-versatile) | `128K / 30 / 1000 / 12K / 100K` | Groq account (no CC for free tier) | Very Good | Verified | Official current free row differs from older community numbers. |
| Llama 4 Maverick 17B | `128K / 30 / 1000 / 6K / 500K` | Groq account (no CC for free tier) | Good | Verified | Fast inference; limits can change by model revision. |
| Qwen3 32B | `128K / 30 / 14,400 / 6K / 500K` | Groq account (no CC for free tier) | Good | Partially verified | Model IDs and limits can shift between releases. |
| Compound AI (groq/compound) | `128K / 30 / 250 / 70K / not published` | Groq account (no CC for free tier) | Good | Verified | Official table does not publish a TPD value. |

### Together AI

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Llama 4 Maverick | `131K / tier-dependent / tier-dependent / tier-dependent / tier-dependent` | Together account + paid credits | Very Good | Verified | No standing free trial in current billing docs. |
| DeepSeek V3.1 | `64K / tier-dependent / tier-dependent / tier-dependent / tier-dependent` | Together account + paid credits | Excellent | Verified | Current docs do not confirm "$100 signup credits." |
| Mistral Small 3 | `128K / tier-dependent / tier-dependent / tier-dependent / tier-dependent` | Together account + paid credits | Good | Verified | Limits are spend/account-tier dependent. |

### Hugging Face

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Various open models | `varies / provider-dependent / provider-dependent / provider-dependent / monthly credit-based` | Hugging Face account | Varies | Verified | Limits depend on routed provider and account plan. |
| Pro-tier routed providers | `varies / higher than free / provider-dependent / provider-dependent / credit-based` | Hugging Face Pro | Very Good | Verified | Pro includes higher monthly included credits. |

### Mistral AI

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Mistral Nemo 12B | `model-dependent / plan-dependent / plan-dependent / plan-dependent / plan-dependent` | Mistral account (Experiment/Scale) | Good | Partially verified | Free Experiment plan exists; per-model quotas are dynamic. |
| Mistral Small 3.1 | `128K / plan-dependent / plan-dependent / plan-dependent / plan-dependent` | Mistral account (Experiment/Scale) | Good | Partially verified | Access and limits depend on plan tier. |
| Codestral | `32K / plan-dependent / plan-dependent / plan-dependent / plan-dependent` | Mistral account (Experiment/Scale) | Excellent | Partially verified | Code-oriented model with account-tier gating. |
| Mistral Large 3 | `128K / plan-dependent / plan-dependent / plan-dependent / plan-dependent` | Mistral account (Experiment/Scale) | Excellent | Partially verified | Most capable tier generally tied to paid scale usage. |

### DeepSeek

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| DeepSeek V3.2 (deepseek-chat) | `128K / not published / not published / not published / not published` | DeepSeek account | Excellent | Partially verified | Pricing and granted-balance behavior are public, quotas are not fixed. |
| DeepSeek R1 / reasoner | `128K / not published / not published / not published / not published` | DeepSeek account | Excellent | Unverified | "5M free signup tokens" is not confirmed in official public pricing docs. |

### Cohere

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Command R7B | `128K / 20 (trial chat) / ~1000 calls/month / endpoint-dependent / 1000 calls/month` | Cohere account (trial key) | Good | Verified | Trial keys are free but heavily rate-limited. |
| Command R+ | `128K / 20 (trial chat) / ~1000 calls/month / endpoint-dependent / 1000 calls/month` | Cohere account (trial key) | Very Good | Verified | Monthly trial cap is account-wide for trial usage. |

### OpenRouter

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Qwen3 Coder 480B (`:free` variant when available) | `model-dependent / 20 / 50/day (<$10 credits) or 1000/day (>= $10 credits) / not published / not published` | OpenRouter account | Excellent | Verified | Free limits are account-plan based, not per-model fixed quotas. |
| GPT-OSS-120B (`:free` variant when available) | `model-dependent / 20 / 50/day or 1000/day (>= $10 credits) / not published / not published` | OpenRouter account | Very Good | Verified | Free variants can rotate over time. |
| Llama 3.3 70B (`:free` variant when available) | `model-dependent / 20 / 50/day or 1000/day (>= $10 credits) / not published / not published` | OpenRouter account | Very Good | Verified | Free router pool is dynamic. |
| Mistral Small 3.1 (`:free` variant when available) | `model-dependent / 20 / 50/day or 1000/day (>= $10 credits) / not published / not published` | OpenRouter account | Good | Verified | Best for low-volume experimentation. |
| DeepSeek R1 (`:free` variant when available) | `model-dependent / 20 / 50/day or 1000/day (>= $10 credits) / not published / not published` | OpenRouter account | Excellent | Verified | Prior community RPD values differ from current docs. |

### Cerebras

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Llama 4 Maverick 400B | `128K (paid tier) / 30 / 14,400 / 60K / 1M/day` | Cerebras account | Very Good | Partially verified | Context and limits vary by model page and tier. |
| Qwen3 Coder 235B | `64K free, 131K paid / 30 / 14,400 / 60K / 1M/day` | Cerebras account | Excellent | Partially verified | Good coding performance signals; verify live model page limits. |
| Llama 3.1 8B | `8K free, 32K paid / 30 / 14,400 / 60K / 1M/day` | Cerebras account | Good | Verified | Free-tier limits are explicitly published. |

### xAI Grok

| Model | Quotas | Account Type | Code Quality | Verification | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Grok 4.1 Fast | `model-dependent / credit-dependent / credit-dependent / credit-dependent / credit-dependent` | xAI account | Very Good | Unverified | Promotional free credits may exist; fixed "$25 startup credits" not consistently documented. |

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
