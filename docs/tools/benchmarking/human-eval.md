# HumanEval

HumanEval is a benchmark released by OpenAI to evaluate the code generation capabilities of Large Language Models.

## Description
It consists of 164 handwritten programming problems, each including a function signature, docstring, body, and several unit tests. The problems are designed to be self-contained and assess the model's ability to solve basic algorithmic tasks.

## Key Metrics
- **Pass@k**: The probability that at least one of the top $k$ generated code samples passes all unit tests.

## Links
- [GitHub Repository](https://github.com/openai/human-eval)

## Alternatives
- [MBPP (Mostly Basic Python Problems)](mbpp.md)
- [BigCodeBench](https://github.com/bigcode-project/bigcodebench)

## Backlog
- Add comparison with HumanEval-X for multilingual support.
