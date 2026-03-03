# API Pricing & Free Tier Matrix

This is the canonical tracker for API pricing links and free-tier availability across major LLM providers used in this repository.

## Scope and usage

- Focus: provider/API access (not chat subscription plans unless explicitly tied to API access).
- Purpose: quick provider comparison and maintenance reference for contributors and agents.
- Update target: review at least monthly, and after major provider announcements.

## Status legend

- `Yes` = official free tier/trial access is currently documented.
- `Partial` = limited free usage exists (for example, selected models/features).
- `No` = no current free trial/tier is documented.
- `Unclear` = pricing docs mention grants/credits, but no explicit standing free tier.

## Canonical pricing matrix (last verified: 2026-03-03)

| Provider | API pricing link | Free tier / trial | Evidence summary | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| OpenAI | [openai.com/api/pricing](https://openai.com/api/pricing/) | No | API is usage-priced; billing docs describe prepaid credits with minimum purchase. | 2026-03-03 |
| Anthropic (Claude API) | [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) | Yes | Pricing FAQ states new users receive a small amount of free API credits. | 2026-03-03 |
| Google Gemini Developer API | [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) | Yes | Pricing tables include Free Tier rows with "Free of charge" for selected usage. | 2026-03-03 |
| OpenRouter | [openrouter.ai/pricing](https://openrouter.ai/pricing) | Yes | Free plan lists 25+ free models, free providers, and free-plan rate limits. | 2026-03-03 |
| Cohere | [cohere.com/pricing](https://cohere.com/pricing) | Yes | Trial API key calls are explicitly free (rate-limited, non-production). | 2026-03-03 |
| Mistral AI | [mistral.ai/pricing](https://mistral.ai/pricing) | Yes | Help center documents free API access via Experiment plan (no credit card required). | 2026-03-03 |
| Together AI | [together.ai/pricing](https://www.together.ai/pricing) | No | Billing docs state no free trial; access requires minimum $5 credit purchase. | 2026-03-03 |
| Groq | [groq.com/pricing](https://groq.com/pricing) | Yes | Pricing page exposes free API key entry point; rate-limit docs include a Free Plan section. | 2026-03-03 |
| Fireworks AI | [fireworks.ai/pricing](https://fireworks.ai/pricing) | Yes | Serverless pricing section states "Get started with $1 in free credits." | 2026-03-03 |
| Replicate | [replicate.com/pricing](https://replicate.com/pricing) | Partial | Billing docs state select models can be run for free before billing setup is required. | 2026-03-03 |
| DeepSeek API | [api-docs.deepseek.com/quick_start/pricing](https://api-docs.deepseek.com/quick_start/pricing) | Unclear | Pricing docs reference topped-up and granted balances but do not define a standing free tier. | 2026-03-03 |

## Notes and caveats

- Provider pricing and free-tier rules change frequently; always confirm from the official links above before budgeting.
- Some providers separate product-level free plans from API-level free access.
- Regional restrictions, tax handling, and enterprise contracts can materially change effective costs.

## Maintenance protocol

When updating this page:

1. Verify each provider from official pricing/billing docs.
2. Update `Free tier / trial`, `Evidence summary`, and `Last verified`.
3. Add new providers only when official pricing links are stable.
4. If a status is uncertain, set `Unclear` rather than guessing.

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
- [ChatGPT shared context (title only)](https://chatgpt.com/share/69a760fd-3520-8000-bfbd-19bdf623a333)

## Contribution Metadata

- Last reviewed: 2026-03-03
- Confidence: medium
