# OpenAPPA

## What it is
OpenAPPA is an open-source security engine from Archestra that aims to prevent data exfiltration caused by prompt injection or model hallucination. It runs outside the agent's prompt and execution loop and applies deterministic security rules, so the agent cannot talk its way around the policy. It is currently in preview. It accompanies the paper "APPA: Recoverable Information-Flow Control for Real-World LLM Agents".

## What problem it solves
Agents that read untrusted content and also hold tools or credentials can be tricked into leaking data. Prompt-level defences are probabilistic; OpenAPPA instead tracks where data came from and who may receive it, and enforces that outside the model.

## Where it fits in the stack
**Agent security / policy enforcement layer**, external to the agent process.

## Typical use cases
- Constraining tool-using agents that handle untrusted input.
- Declaring per-tool access contracts in configuration (`appa.toml`).
- Auditing which data flows an agent attempted.

## Strengths
- Configuration-driven policy (`appa.toml`) enforced outside the agent loop.
- Labels track data audience and trust level; labels only become more restrictive when combined (lattice algebra).
- Tool contracts declare `requires`, `delta` and `effects` (audit trail).
- Recovery mechanisms: sanitizers, authorities and disposable child branches.
- Vendor-reported results: 0% attack success on Bench-Corp and AgentThreatBench with 89% task completion, versus 10% for Claude Code auto mode and 31% for Microsoft FIDES as cited by InfoQ.

## Limitations
- Preview status.
- Benchmark figures are reported by the vendor via a news article and were not independently reproduced here.
- Strict enforcement can block legitimate work; the article notes the tension between safety and utility.
- The specific open-source licence was not stated in the article and was not verified.

## When to use it
- When agents combine untrusted input with sensitive data or powerful tools and you need deterministic guarantees.

## When not to use it
- For agents with no access to sensitive data or side-effecting tools.
- When a stable, non-preview component is required.

## Licensing and cost
- **Open Source**: Yes (licence not verified)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [AWS Dogwood](aws-dogwood.md) - another agent policy and safety layer.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - tool protocol whose calls such engines mediate.
- [Claude Code](../development_ops/claude-code.md) - compared against in the vendor's benchmark claims.

## Sources / References
- [InfoQ: Archestra's OpenAPPA Saturates Two Major Security Benchmarks with a 0% Attack Success Rate (2026-10-03)](https://www.infoq.com/news/2026/10/open-APPA-zero-security-breach/)
- [OpenAPPA documentation](https://openappa.com) (linked from the InfoQ article; not fetched directly)

## Contribution Metadata
- Last reviewed: 2026-10-05
- Confidence: medium
