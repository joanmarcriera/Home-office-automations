# MATH Benchmark

## What it is
The MATH benchmark is a dataset of 12,500 challenging mathematics competition problems designed to evaluate the mathematical reasoning capabilities of AI models. It was created by researchers at UC Berkeley led by Dan Hendrycks.

## What problem it solves
Many general-purpose benchmarks only test basic arithmetic or simple word problems. The MATH benchmark pushes models to solve complex, multi-step problems from high school competitions, requiring deep conceptual understanding and precise symbolic reasoning rather than just pattern matching.

## Where it fits in the stack
**Benchmarking**. It is a specialized tool for evaluating mathematical reasoning and advanced problem-solving skills in LLMs.

## Typical use cases
- **Mathematical Reasoning Evaluation**: Assessing how well a model can solve complex math problems across different subjects.
- **Difficulty Scaling Analysis**: Understanding a model's performance limit by testing across five distinct levels of difficulty.
- **CoT (Chain of Thought) Testing**: Evaluating the quality of a model's step-by-step reasoning using the detailed solutions provided in the dataset.

## Strengths
- **High Difficulty**: Includes problems from the AMC 10, AMC 12, and AIME competitions, which are difficult even for human experts.
- **Detailed Solutions**: Every problem comes with a step-by-step human-written solution, enabling fine-grained evaluation of reasoning paths.
- **Subject Variety**: Covers seven core subjects: Prealgebra, Algebra, Number Theory, Counting and Probability, Geometry, Intermediate Algebra, and Precalculus.
- **Standardized Scoring**: Uses a simple "correct/incorrect" metric based on the final answer, which is often boxed in LaTeX format.

## Limitations
- **LaTeX Heavy**: Requires the model to be proficient in reading and generating LaTeX notation.
- **Parsing Challenges**: Automated scoring can be tricky due to different ways of formatting mathematically equivalent answers (though tools like [MiniCPM](https://github.com/OpenBMB/MiniCPM) and [DeepSeek](https://github.com/deepseek-ai/DeepSeek-Math) have standardized some of this).
- **Data Contamination**: As one of the most famous benchmarks, it is highly likely that many models have seen some or all of the MATH dataset during pre-training.

## When to use it
- When you are developing or evaluating models for scientific, engineering, or educational applications.
- When you want to benchmark the "reasoning ceiling" of a large model.

## When not to use it
- For evaluating basic numeracy or elementary school math (use [GSM8K](gsm8k.md) instead).
- For general conversation or instruction-following tasks.

## Licensing and cost
- **Open Source**: Yes (MIT License for the dataset).
- **Cost**: Free.
- **Self-hostable**: Yes, the dataset is available on Hugging Face and GitHub.

## Related tools / concepts
- [GSM8K](gsm8k.md)
- [ASDiv](asdiv.md)
- [MMLU](mmlu.md) (which contains a math sub-section)
- **Latex**: The standard formatting used for math problems.

## Sources / References
- [GitHub Repository](https://github.com/hendrycks/math)
- [arXiv: Measuring Mathematical Problem Solving With the MATH Dataset](https://arxiv.org/abs/2103.03874)
- [Hugging Face Dataset](https://huggingface.co/datasets/hendrycks/competition_math)

## Contribution Metadata
- Last reviewed: 2026-03-30
- Confidence: high
