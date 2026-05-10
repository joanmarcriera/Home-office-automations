# API Pricing & Free Tier Matrix

## What it is
The API Pricing & Free Tier Matrix is a consolidated reference for the costs and free access policies of major Large Language Model (LLM) providers and AI platforms. It tracks pricing for tokens, developer program benefits, and specific model-level quotas.

## What problem it solves
LLM pricing is notoriously complex, with costs varying by several orders of magnitude between "mini" and "frontier" models. Furthermore, free tiers are often hidden or poorly documented. This matrix allows developers to perform a "budget-first" architectural selection, choosing models that fit their financial constraints and usage patterns.

## Where it fits in the stack
This document belongs to the **Layer 1: Providers** and **Layer 2: Models** analysis layer. It provides the economic context for the tools documented in `docs/tools/providers/` and `docs/tools/ai_knowledge/`.

## Typical use cases
- **Budgeting**: Estimating the monthly cost of running a specific agentic workflow (e.g., using GPT-5.4 mini for routine tasks).
- **Free-Tier Hunting**: Identifying which providers offer enough free credits to build and test a prototype without a credit card.
- **Provider Switching**: Comparing the "Intelligence-per-Dollar" value when deciding whether to migrate from one provider to another (e.g., Anthropic to Google).
- **Quota Management**: Checking Rate Per Minute (RPM) and Tokens Per Day (TPD) limits for free tiers to avoid service interruptions.

## Strengths
- **Consolidated**: Aggregates data from over 30 providers in a single view.
- **Agent-Optimized**: Specifically highlights "mini" models and high-speed providers ideal for autonomous agents.
- **Evidence-Based**: Includes direct links to official documentation for every claim.
- **Automated**: Uses scripts to maintain a "Capability Capacity Summary" of known free tokens.

## Limitations
- **High Volatility**: Prices and free-tier availability can change weekly.
- **Regional Variation**: Some free tiers or pricing models may not be available in all jurisdictions.
- **Tier Complexity**: Many providers use opaque "usage tiers" (Tier 1-5) that affect limits beyond simple price-per-token.

## When to use it
- Use it during the design phase of an AI application to select a model based on cost-efficiency.
- Use it when you hit a rate limit and need to find an alternative provider with higher free-tier capacity.
- Use it to verify if a "free trial" mentioned in a tutorial is still currently active.

## When not to use it
- Do not use it as a legally binding price list; always verify with the provider's official dashboard before committing to large-scale spend.
- Do not use it for consumer-facing chat app pricing (e.g., ChatGPT Plus vs. Claude Pro) unless it specifically mentions API benefits.

## Getting started
1. Identify your primary requirement (e.g., "Coding", "Fast", or "Budget").
2. Consult the **[Capability Capacity Summary](#capability-capacity-summary-auto-generated)** to see which models currently offer the best free-tier value.
3. Use the **[Canonical pricing matrix](#canonical-pricing-matrix-last-verified-2026-05-14)** to jump to the official pricing and documentation for your chosen provider.
4. Check the **[Model-level quota tracker](#model-level-quota-tracker-expanded-list)** for specific RPM/TPD limits.

## Status legend
- `Yes` = official free tier/trial access is currently documented.
- `Partial` = limited free usage exists (for example, selected models/features).
- `No` = no current free trial/tier is documented.
- `Unclear` = pricing/billing docs do not clearly confirm a standing free tier.

## Canonical pricing matrix (last verified: 2026-05-14)

| Provider / Platform | Official links | Free tier / trial | Evidence summary |
| :--- | :--- | :--- | :--- |
| OpenAI | [Docs](https://platform.openai.com/docs) · [Pricing](https://openai.com/api/pricing/) | No | Usage-priced API; current pricing centers GPT-5.5, GPT-5.4, and GPT-5.4 mini. |
| Anthropic (Claude API) | [Docs](https://docs.anthropic.com/) · [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) | Yes | New users receive small starter API credits. Current API pricing lists Claude Opus 4.7/4.6/4.5, Sonnet 4.6/4.5, and Haiku 4.5. |
| Google Gemini Developer API | [Docs](https://ai.google.dev/gemini-api/docs) · [Pricing](https://ai.google.dev/gemini-api/docs/pricing) | Yes | Pricing page documents a Free plan with selected free input/output token access; Gemini 3.1 Pro Preview is paid-only, while Gemini 3.1 Flash-Lite Preview has free rows. |
| OpenRouter | [Docs](https://openrouter.ai/docs/quickstart) · [Pricing](https://openrouter.ai/pricing) | Yes | Free plan and free-model routing are documented. |
| xAI (Grok API) | [Docs](https://docs.x.ai/docs/overview) · [Pricing](https://x.ai/api) | Yes | Docs mention monthly free requests/credits. |
| Z.ai (GLM API) | [Docs](https://docs.z.ai/) · [Pricing](https://open.bigmodel.cn/) | Yes | New users can claim free API token packages. |
| Alibaba DashScope (Qwen APIs) | [Docs](https://www.alibabacloud.com/help/en/model-studio/getting-started/models) · [Pricing](https://www.alibabacloud.com/help/en/model-studio/product-overview/billing-of-model-studio) | Yes | Many models show temporary free quota periods. |
| Cohere | [Docs](https://docs.cohere.com/) · [Pricing](https://cohere.com/pricing) | Yes | Trial API keys are free and rate-limited. |
| Mistral AI | [Docs](https://docs.mistral.ai/) · [Pricing](https://mistral.ai/pricing) | Yes | Experiment plan supports free API testing. |
| Together AI | [Docs](https://docs.together.ai/) · [Pricing](https://www.together.ai/pricing) | No | Billing docs indicate paid credits are required. |
| Groq | [Docs](https://console.groq.com/docs/overview) · [Pricing](https://groq.com/pricing/) | Yes | Free API plan and model-level limits are documented; exact current limits should be read from the account limits page for production budgeting. |
| Kiro | [Docs](https://kiro.dev/docs/) · [Pricing](https://kiro.dev/pricing/) | Yes | Perpetual free tier (50 credits/mo) + 500 bonus credits. |
| Fireworks AI | [Docs](https://fireworks.ai/docs) · [Pricing](https://fireworks.ai/pricing) | Yes | Public pricing notes starter free credits. |
| Replicate | [Docs](https://replicate.com/docs) · [Pricing](https://replicate.com/pricing) | Partial | Some models can be run free before billing. |
| DeepSeek API | [Docs](https://api-docs.deepseek.com/) · [Pricing](https://api-docs.deepseek.com/quick_start/pricing) | Unclear | Granted balances are mentioned, fixed free tier unclear. |
| Perplexity API | [Docs](https://docs.perplexity.ai/) · [Pricing](https://docs.perplexity.ai/guides/pricing) | No | Purchased credits and top-up requirements documented. |
| AI21 | [Docs](https://docs.ai21.com/) · [Pricing](https://www.ai21.com/pricing) | Yes | Pricing page advertises free trial credits. |
| Abacus.AI | [Docs](https://abacus.ai/) · [Pricing](https://abacus.ai/pricing) | Yes | Free trial and ChatLLM free access documented. |
| Voyage AI | [Docs](https://docs.voyageai.com/) · [Pricing](https://docs.voyageai.com/docs/pricing) | Unclear | Paid rates are clear; standing free tier not explicit. |
| Cloudflare Workers AI | [Docs](https://developers.cloudflare.com/workers-ai/) · [Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) | Yes | Free plan includes daily usage. |
| Hugging Face Inference Providers | [Docs](https://huggingface.co/docs/inference-providers) · [Pricing](https://huggingface.co/pricing) | Yes | Monthly included inference credits by account tier. |
| Cerebras Inference | [Docs](https://inference-docs.cerebras.ai/) · [Pricing](https://inference-docs.cerebras.ai/introduction) | Yes | Pricing references free-tier usage/credits. |
| NVIDIA API Catalog | [Docs](https://build.nvidia.com/docs) · [Pricing](https://build.nvidia.com/pricing) | Yes | Starter credits are referenced publicly. |
| SambaNova Cloud | [Docs](http://docs.sambanova.ai/) · [Pricing](https://cloud.sambanova.ai/plans/pricing) | Unclear | Public page shows paid plans; no stable free policy. |
| AWS Bedrock | [Docs](https://docs.aws.amazon.com/bedrock/) · [Pricing](https://aws.amazon.com/bedrock/pricing/) | No | Metered pay-as-you-go pricing. |
| Amazon Q | [Docs](https://docs.aws.amazon.com/amazonq/) · [Pricing](https://aws.amazon.com/q/pricing/) | Yes | Free tier for individuals/developers is documented. |
| Azure OpenAI Service | [Docs](https://learn.microsoft.com/azure/ai-services/openai/) · [Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) | Unclear | Metered service; only account-level cloud credits may apply. |
| Vertex AI (Gemini via GCP) | [Docs](https://cloud.google.com/vertex-ai/docs) · [Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) | Unclear | Metered pricing; no persistent API free-tier statement. |
| OCI Generative AI | [Docs](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm) · [Pricing](https://www.oracle.com/artificial-intelligence/generative-ai/generative-ai-service/pricing/) | Unclear | Paid rates are public; free tier not clearly documented. |
| MiniMax | [Docs](https://platform.minimaxi.com/docs/guides/models-intro) · [Pricing](https://platform.minimaxi.com/docs/guides/pricing-paygo) | Yes | Coding Plan provides a low-cost entry tier; trial credits available. |
| Moonshot AI | [Docs](https://platform.moonshot.cn/) · [Pricing](https://platform.moonshot.cn/) | Partial | Trial credits are typically granted to new developer accounts. |

## Enterprise Productivity Suite (2026 Benchmarks)

| Tool | Pricing Model | Free Tier / Trial | Notes |
| :--- | :--- | :--- | :--- |
| **Fyxer AI** | ~$30-$50/user/mo | 14-day Trial | Executive admin & inbox management. |
| **Glean** | Enterprise Quote | No | Unified search across 100+ SaaS apps. |
| **Hebbia** | Institutional Quote | No | High-precision analytical search for Finance/Law. |
| **tl;dv** | Freemium | Yes | Meeting recorder with free unlimited tier. |

## Developer Program Plans

These are the core subscription plans for developers that bundle AI access, cloud credits, and other professional benefits.

| Program / Plan | Cost | AI Access & Quotas | Cloud Credits & Benefits |
| :--- | :--- | :--- | :--- |
| **Google Developer Program — Standard** | Free | 10 Firebase Studio workspaces; Gemini Code Assist (Basic); Gemini CLI (60 RPM / 1000 RPD) | Monthly Google Skills credits (via GEAR); community access; private previews. |
| **Google Developer Program — Premium** | $24.99/mo or $299/yr | 30 Firebase Studio workspaces; Gemini Code Assist (Higher); Gemini CLI (120 RPM / 1500 RPD) | $45/mo ($550/yr) GenAI/Cloud credit; $500 bonus credit upon certification; 1 Cloud cert voucher; expert consultation. |
| **Google Developer Program — Enterprise** | Preview | Gemini Code Assist Enterprise; Gemini CLI (120 RPM / 2000 RPD) | $150/mo Google Cloud credit; centralized purchasing; developer sandboxes. |

## Model-level quota tracker (expanded list)

This section is grouped by provider with compact four-column tables for narrower screens.

- `Verified` = core limits are visible in official docs.
- `Partially verified` = provider free-tier stance is verified, but model-level quotas are dynamic or not fully published.
- `Unverified` = values come from community reports or account-specific observations not explicitly documented.

`Code Generation Quality` is subjective and treated as community-assessed, not an official benchmark metric.

Quick jump:
[Google Gemini](#google-gemini) · [OpenAI](#openai) · [Anthropic Claude](#anthropic-claude) · [Groq](#groq) · [Together AI](#together-ai) · [Hugging Face](#hugging-face) · [Mistral AI](#mistral-ai) · [DeepSeek](#deepseek) · [Cohere](#cohere) · [OpenRouter](#openrouter) · [Cerebras](#cerebras) · [xAI Grok](#xai-grok) · [Kiro](#kiro)

`Quotas` format is `context / RPM / RPD / TPM / daily token cap`.
`n/p` means "not published."

Capability tags:

- <span class="cap-tag cap-code">CODE</span> code generation and refactoring tasks.
- <span class="cap-tag cap-verify">VERIFY</span> cross-checking, factual validation, and test review.
- <span class="cap-tag cap-reason">REASON</span> complex reasoning and multi-step planning.
- <span class="cap-tag cap-longctx">LONGCTX</span> long documents, large prompts, and retrieval-heavy workflows.
- <span class="cap-tag cap-fast">FAST</span> low-latency interactions and interactive agent loops.
- <span class="cap-tag cap-budget">BUDGET</span> better free-tier value or lower-cost experimentation.
- <span class="cap-tag cap-open">OPEN</span> open-weight/open-model ecosystem affinity.

<!-- BEGIN AUTO-CAPABILITY-SUMMARY -->

### Capability Capacity Summary (auto-generated)

These summaries are generated from the model rows on this page using `scripts/update_api_pricing_capability_summary.py`.
Only rows with a numeric daily token cap are included in the capacity math.

#### Leaderboard By Capability (known daily token caps)

| Capability | Top models | Highest known daily cap | Known models |
| :--- | :--- | :--- | :--- |
| Coding | Cerebras — Llama 4 Maverick 400B (1M); Cerebras — Qwen3 Coder 235B (1M); Groq — Llama 4 Maverick 17B (500K) | 1M | 7 |
| Verification | n/a | n/a | 0 |
| Reasoning | Groq — GPT OSS 120B (200K) | 200K | 1 |
| Long-context | n/a | n/a | 0 |
| Low-latency | Cerebras — Llama 4 Maverick 400B (1M); Cerebras — Qwen3 Coder 235B (1M); Cerebras — Llama 3.1 8B (1M) | 1M | 7 |
| Budget/free-value | Cerebras — Llama 3.1 8B (1M); Groq — Llama 4 Maverick 17B (500K); Groq — Qwen3 32B (500K) | 1M | 5 |
| Open-model ecosystem | Cerebras — Llama 4 Maverick 400B (1M); Cerebras — Qwen3 Coder 235B (1M); Cerebras — Llama 3.1 8B (1M) | 1M | 7 |

#### 80% Shortlist (known-cap coverage)

| Capability | Models to reach >=80% of known capacity | Coverage | Total known daily cap |
| :--- | :--- | :--- | :--- |
| Coding | Cerebras — Llama 4 Maverick 400B (1M); Cerebras — Qwen3 Coder 235B (1M); Groq — Llama 4 Maverick 17B (500K); Groq — Qwen3 32B (500K); Groq — Llama 4 Scout 17B (500K) | 92.1% | 3.8M |
| Verification | n/a | n/a | n/a |
| Reasoning | Groq — GPT OSS 120B (200K) | 100.0% | 200K |
| Long-context | n/a | n/a | n/a |
| Low-latency | Cerebras — Llama 4 Maverick 400B (1M); Cerebras — Qwen3 Coder 235B (1M); Cerebras — Llama 3.1 8B (1M); Groq — Llama 4 Maverick 17B (500K); Groq — Qwen3 32B (500K) | 87.0% | 4.6M |
| Budget/free-value | Cerebras — Llama 3.1 8B (1M); Groq — Llama 4 Maverick 17B (500K); Groq — Qwen3 32B (500K); Groq — Llama 4 Scout 17B (500K) | 96.2% | 2.6M |
| Open-model ecosystem | Cerebras — Llama 4 Maverick 400B (1M); Cerebras — Qwen3 Coder 235B (1M); Cerebras — Llama 3.1 8B (1M); Groq — Llama 4 Maverick 17B (500K); Groq — Qwen3 32B (500K) | 87.0% | 4.6M |

#### Fast Recommendation (80% rule, known-cap data)

| Goal | Recommended free-first models | Why this set |
| :--- | :--- | :--- |
| Coding | Cerebras — Llama 4 Maverick 400B; Cerebras — Qwen3 Coder 235B; Groq — Llama 4 Maverick 17B; Groq — Qwen3 32B; Groq — Llama 4 Scout 17B | Reaches 92.1% of known daily capacity (3.8M total known). |
| Verification | n/a | No numeric daily-cap data available for this capability. |
| Reasoning | Groq — GPT OSS 120B | Reaches 100.0% of known daily capacity (200K total known). |

<!-- END AUTO-CAPABILITY-SUMMARY -->

### Alibaba DashScope (Qwen)

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Qwen3.6-35B-A3B | `262K / plan / plan / plan / plan` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-open">OPEN</span><br>Account: DashScope. Latest frontier variant with 3B active parameters. |
| Qwen3.5-35B-A3B | `128K / plan / plan / plan / plan` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-open">OPEN</span><br>Account: DashScope. SOTA agentic coding (37.8% SWE-bench Verified Hard). |

### Google Gemini

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Gemini 3.1 Pro Preview | `model / paid / paid / paid / paid` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-longctx">LONGCTX</span><br>Account: Google. Paid-only Pro preview; $2/MTok input and $12/MTok output for prompts up to 200K tokens. |
| Gemini 3.1 Flash-Lite Preview | `model / plan / plan / plan / n/p` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-longctx">LONGCTX</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: Google. Free input/output rows documented for Standard/Batch/Flex/Priority; paid Standard is $0.25/MTok text-image-video input and $1.50/MTok output. |
| Gemini Embedding | `model / plan / plan / plan / n/p` | Verified | <span class="cap-tag cap-budget">BUDGET</span> <span class="cap-tag cap-longctx">LONGCTX</span><br>Account: Google. Gemini Embedding is available on free and paid tiers; paid input is $0.15/MTok. |

### OpenAI

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| GPT-5.5 | `model / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-reason">REASON</span><br>Account: OpenAI. Frontier coding/professional-work model; $5/MTok input and $30/MTok output. No standing public free API tier documented. |
| GPT-5.4 | `model / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-reason">REASON</span><br>Account: OpenAI. More affordable coding/professional-work model; $2.50/MTok input and $15/MTok output. |
| GPT-5.4 mini | `model / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: OpenAI. Mini model for coding, computer use, and subagents; $0.75/MTok input and $4.50/MTok output. |

### Anthropic Claude

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Claude Opus 4.7 | `model / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-longctx">LONGCTX</span><br>Account: Anthropic. Current Opus line; $5/MTok input and $25/MTok output on the Claude API. |
| Claude Sonnet 4.6 | `model / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-longctx">LONGCTX</span><br>Account: Anthropic. Current Sonnet line; $3/MTok input and $15/MTok output. |
| Claude Haiku 4.5 | `model / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-budget">BUDGET</span> <span class="cap-tag cap-verify">VERIFY</span><br>Account: Anthropic. Current Haiku line; $1/MTok input and $5/MTok output. |

### Groq

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Llama 3.3 70B (llama-3.3-70b-versatile) | `128K / 30 / 1000 / 12K / 100K` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: Groq (no CC for free tier). Quality: Very Good. Official row differs from older community numbers. |
| Llama 4 Maverick 17B | `128K / 30 / 1000 / 6K / 500K` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: Groq (no CC for free tier). Quality: Good. Fast inference; revision limits can change. |
| Qwen3 32B | `128K / 60 / 1000 / 6K / 500K` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: Groq (no CC for free tier). Quality: Good. Current official free-plan row uses `qwen/qwen3-32b`. |
| Llama 4 Scout 17B | `128K / 30 / 1000 / 30K / 500K` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: Groq. 16E MoE variant optimized for low-latency tasks; official free-plan TPM is 30K. |
| GPT OSS 120B | `128K / 30 / 1000 / 8K / 200K` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-reason">REASON</span><br>Account: Groq. High performance open-weights model; official free-plan TPD is 200K. |
| Kimi K2 (kimi-k2-0905) | `256K / n/p / n/p / n/p / n/p` | Verified | <span class="cap-tag cap-longctx">LONGCTX</span> <span class="cap-tag cap-reason">REASON</span><br>Account: Groq. 1T parameter MoE with 256K context. |
| Compound AI (groq/compound) | `128K / 30 / 250 / 70K / n/p` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-code">CODE</span><br>Account: Groq (no CC for free tier). Quality: Good. Official docs do not publish TPD. |

### Kiro

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Auto (Frontier Mix) | `n/p / n/p / n/p / n/p / 50 credits` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: Kiro. Mixed agent using frontier models. Free tier includes 50 monthly credits. |

### Together AI

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Llama 4 Maverick | `131K / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Together + paid credits. Quality: Very Good. No standing free trial in current docs. |
| DeepSeek V3.1 | `64K / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Together + paid credits. Quality: Excellent. "$100 signup credits" not confirmed in current docs. |
| Mistral Small 3 | `128K / tier / tier / tier / tier` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Together + paid credits. Quality: Good. Limits are spend/account-tier dependent. |

### Hugging Face

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Various open models | `varies / provider / provider / provider / credit-based` | Verified | <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span> <span class="cap-tag cap-code">CODE</span><br>Account: Hugging Face. Quality: Varies. Limits depend on routed provider and plan. |
| Pro-tier routed providers | `varies / higher / provider / provider / credit-based` | Verified | <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-verify">VERIFY</span><br>Account: Hugging Face Pro. Quality: Very Good. Pro includes higher monthly credits. |

### Mistral AI

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Mistral Nemo 12B | `model / plan / plan / plan / plan` | Partially verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: Mistral (Experiment/Scale). Quality: Good. Free Experiment plan exists; quotas are dynamic. |
| Mistral Small 3.1 | `128K / plan / plan / plan / plan` | Partially verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Mistral (Experiment/Scale). Quality: Good. Access/limits depend on plan tier. |
| Codestral | `32K / plan / plan / plan / plan` | Partially verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Mistral (Experiment/Scale). Quality: Excellent. Code-oriented with plan gating. |
| Mistral Large 3 | `128K / plan / plan / plan / plan` | Partially verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-verify">VERIFY</span><br>Account: Mistral (Experiment/Scale). Quality: Excellent. Most capable tier usually paid. |

### DeepSeek

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| DeepSeek V3.2 (deepseek-chat) | `128K / n/p / n/p / n/p / n/p` | Partially verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: DeepSeek. Quality: Excellent. Pricing is public; fixed free quotas are not. |
| DeepSeek R1 / reasoner | `128K / n/p / n/p / n/p / n/p` | Unverified | <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-code">CODE</span><br>Account: DeepSeek. Quality: Excellent. "5M signup tokens" is not confirmed in official docs. |

### Cohere

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Command R7B | `128K / 20 / ~1000mo / endpoint / 1000mo` | Verified | <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-fast">FAST</span><br>Account: Cohere trial key. Quality: Good. Free trial usage is heavily rate-limited. |
| Command R+ | `128K / 20 / ~1000mo / endpoint / 1000mo` | Verified | <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-code">CODE</span><br>Account: Cohere trial key. Quality: Very Good. Trial cap is account-wide per month. |

### OpenRouter

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Qwen3 Coder 480B (`:free` variant when available) | `model / 20 / 50d (<$10) or 1000d (>= $10) / n/p / n/p` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: OpenRouter. Quality: Excellent. Free limits are account-plan based. |
| GPT-OSS-120B (`:free` variant when available) | `model / 20 / 50d or 1000d (>= $10) / n/p / n/p` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: OpenRouter. Quality: Very Good. Free variants can rotate. |
| Llama 3.3 70B (`:free` variant when available) | `model / 20 / 50d or 1000d (>= $10) / n/p / n/p` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: OpenRouter. Quality: Very Good. Free router pool is dynamic. |
| Mistral Small 3.1 (`:free` variant when available) | `model / 20 / 50d or 1000d (>= $10) / n/p / n/p` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: OpenRouter. Quality: Good. Best for low-volume testing. |
| DeepSeek R1 (`:free` variant when available) | `model / 20 / 50d or 1000d (>= $10) / n/p / n/p` | Verified | <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-verify">VERIFY</span> <span class="cap-tag cap-budget">BUDGET</span><br>Account: OpenRouter. Quality: Excellent. Current docs differ from older community RPD values. |

### Cerebras

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Llama 4 Maverick 400B | `128K (paid) / 30 / 14,400 / 60K / 1M` | Partially verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Cerebras. Quality: Very Good. Context/limits vary by tier and model page. |
| Qwen3 Coder 235B | `64K free, 131K paid / 30 / 14,400 / 60K / 1M` | Partially verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Cerebras. Quality: Excellent. Verify live limits on model page. |
| Llama 3.1 8B | `8K free, 32K paid / 30 / 14,400 / 60K / 1M` | Verified | <span class="cap-tag cap-fast">FAST</span> <span class="cap-tag cap-budget">BUDGET</span> <span class="cap-tag cap-open">OPEN</span><br>Account: Cerebras. Quality: Good. Free-tier limits are explicitly published. |

### xAI Grok

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| Grok 4.1 Fast | `model / credit / credit / credit / credit` | Unverified | <span class="cap-tag cap-reason">REASON</span> <span class="cap-tag cap-verify">VERIFY</span><br>Account: xAI. Quality: Very Good. Promotional credits may exist; fixed "$25 startup credits" not consistently documented. |

### MiniMax

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| MiniMax-M2.5 (Coding Plan Starter) | `200K / 40 prompts per 5h / n/p / n/p / n/p` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-budget">BUDGET</span> <span class="cap-tag cap-reason">REASON</span><br>Account: MiniMax. Quality: Excellent. Optimized for coding. Fixed-fee subscription. |
| MiniMax-M2.5 (Pay-as-you-go) | `200K / plan / plan / plan / plan` | Verified | <span class="cap-tag cap-code">CODE</span> <span class="cap-tag cap-fast">FAST</span><br>Account: MiniMax. Quality: Excellent. Competitive RMB pricing (2.1/8.4 per 1M tokens). |

### Moonshot AI

| Model | Quotas | Verification | Summary |
| :--- | :--- | :--- | :--- |
| moonshot-v1-128k | `128K / tier / tier / tier / tier` | Partially verified | <span class="cap-tag cap-longctx">LONGCTX</span> <span class="cap-tag cap-reason">REASON</span><br>Account: Moonshot AI. Quality: Very Good. Famous for pioneer long-context stability. |

## Model Intelligence-per-Dollar Value (2026 Triage)
Based on community analysis (April 2026), models are categorized by their efficiency relative to cost:
- **Top Intelligence**: GPT-5.4, Gemini 3.1 Pro. Use these for high-stakes reasoning where cost is secondary.
- **Best Value**: MiMo-V2-Flash. Offers the highest intelligence-per-dollar for high-volume tasks.
- **Balanced**: GLM-5, Kimi K2.5, Gemini 3 Flash. These models offer a strong middle ground for general-purpose agentic loops.

## Related tools / concepts
- [AI Tooling Landscape](ai_tooling_landscape.md) — The architectural overview of the entire AI stack.
- [Model Classes](model_classes.md) — Understanding the different "tiers" of models (Frontier, Performance, Mini).
- [OpenRouter](../tools/ai_knowledge/openrouter.md) — The primary provider used in this repo for multi-model access.
- [Groq](../tools/providers/groq.md) — Recommended for ultra-fast, low-latency free-tier inference.
- [Mistral](../tools/providers/mistral.md) — A key open-weights provider with a strong experiment plan.
- [DeepSeek](../tools/ai_knowledge/deepseek.md) — High-value Chinese provider often leading on cost-per-token.
- [Benchmarking](../tools/benchmarking/index.md) — How we verify the "Intelligence" part of the value equation.

## Sources / References
- [Kiro Pricing](https://kiro.dev/pricing/)
- [Abacus.AI Pricing](https://abacus.ai/pricing)
- [Amazon Q Pricing](https://aws.amazon.com/q/pricing/)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [OpenAI Prepaid Billing](https://help.openai.com/en/articles/8264644-how-can-i-set-up-prepaid-billing)
- [Model API pricing list on Reddit](https://www.reddit.com/r/openclaw/comments/1rt27st/i_made_a_list_of_models_and_their_api_pricing_on/)
- [Anthropic Claude API Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google Developer Program Plans & Pricing](https://developers.google.com/program/plans-and-pricing)
- [OpenRouter Pricing](https://openrouter.ai/pricing)
- [OpenRouter API rate limits](https://openrouter.ai/docs/api-reference/limits/)
- [OpenRouter Free Models Router](https://openrouter.ai/docs/guides/routing/routers/free-models-router)
- [Qwen3.5-35B-A3B SOTA Performance](https://www.reddit.com/r/AIToolsPerformance/comments/1sn9okz/qwen3635ba3b_drops_with_apache_20_agentic_coding/)
- [MiniMax Pricing](https://platform.minimaxi.com/docs/guides/pricing-paygo)
- [MiniMax Coding Plan](https://platform.minimaxi.com/docs/coding-plan/intro)
- [Moonshot AI Website](https://platform.moonshot.cn/)
- [xAI API](https://x.ai/api)
- [xAI Models/Pricing docs](https://docs.x.ai/docs/models)
- [xAI Billing](https://docs.x.ai/docs/models)
- [Z.ai Docs](https://docs.z.ai/)
- [Z.ai Model Pricing](https://open.bigmodel.cn/)
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
- [Voyage Pricing](https://docs.voyageai.com/docs/pricing)
- [Cloudflare Workers AI Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Hugging Face Pricing](https://huggingface.co/pricing)
- [Cerebras Pricing](https://inference-docs.cerebras.ai/introduction)
- [NVIDIA API Pricing](https://build.nvidia.com/pricing)
- [SambaNova Pricing](https://cloud.sambanova.ai/plans/pricing)
- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
- [Vertex AI GenAI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OCI Generative AI Pricing](https://www.oracle.com/artificial-intelligence/generative-ai/generative-ai-service/pricing/)
- [Google Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Groq rate limits](https://console.groq.com/docs/rate-limits)
- [Cerebras rate limits](https://inference-docs.cerebras.ai/support/rate-limits)
- [ChatGPT shared context (title only)](https://chatgpt.com/share/69a760fd-3520-8000-bfbd-19bdf623a333)

## Contribution Metadata
- Last reviewed: 2026-05-10
- Confidence: high
