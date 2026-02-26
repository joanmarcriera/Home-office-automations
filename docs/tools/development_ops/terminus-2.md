# Terminus 2 (Terminal-Bench)

## What it is
A minimal, terminal-native AI agent designed by the Terminal-Bench team. Unlike complex agents with multi-step reasoning engines, Terminus 2 takes a "raw" approach by giving the LLM direct access to a tmux session. The model sends commands as text and parses the terminal output itself. Despite its simplicity, it performs remarkably well on terminal-based benchmarks.

## What problem it solves
Demonstrates that a simple, direct approach to terminal-based AI agents (LLM + tmux) can achieve strong performance without complex orchestration layers.

## Where it fits in the stack
**Development & Ops**. Serves as a minimal terminal-native AI agent for executing tasks via tmux.

## Typical use cases
- Terminal-based task automation via a minimal AI agent
- Benchmarking AI agent performance in terminal environments
- Exploring simple agent architectures

## Strengths
- Minimal and simple architecture
- Strong benchmark performance despite simplicity
- Direct terminal access via tmux

## Limitations
- Minimal tooling; lacks the features of more complex agents
- Requires a tmux-based environment
- Limited documentation and setup guides

## When to use it
- When exploring minimal AI agent designs for terminal tasks
- When benchmarking terminal-based agent performance

## When not to use it
- When you need a full-featured AI coding agent with IDE integration
- When a non-terminal workflow is preferred

## Related tools / concepts
- [OpenHands](openhands.md)
- [Devin](https://www.cognition-labs.com/devin)

## Sources / references
- [Terminal-Bench GitHub](https://github.com/pro-puffin/terminal-bench)
- [Reference Blog Post](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
