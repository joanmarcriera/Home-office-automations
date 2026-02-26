# Agent Skills Best Practices

## What it is
A practical pattern set for building high-signal, low-context-cost agent skills with clear triggering metadata, deterministic instructions, and progressive disclosure.

## What problem it solves
Poorly authored skills waste context, trigger incorrectly, and produce inconsistent execution. Best-practice structure improves routing accuracy and operational reliability.

## Where it fits in the stack
**Pattern**. This governs prompt/skill engineering for autonomous agent workflows.

## Typical use cases
- Creating reusable skills for repo automation tasks
- Reducing false-positive skill triggering
- Improving deterministic behavior in repeated operations

## Strengths
- Clear guidance for skill discoverability
- Emphasizes lean context windows and deterministic scripts
- Includes validation loop concepts for iterative quality

## Limitations
- Guidance is implementation-agnostic and needs local adaptation
- Strict conventions can feel heavy for very small projects
- Requires maintenance as agent runtime behavior evolves

## When to use it
- When maintaining a growing skill library across projects
- When skill misfires or context bloat are recurring problems

## When not to use it
- For one-off tasks where a dedicated skill is unnecessary
- When no autonomous skill routing is in use

## Related tools / concepts
- [Claude Code Setup](../../tools/development_ops/claude-code-setup.md)
- [Patterns Index](index.md)

## Sources / References
- [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: high
