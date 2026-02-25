# Humanity's Last Exam (HLE)

## What it is
Humanity's Last Exam (HLE) is a high-difficulty language model benchmark consisting of 2,500 questions across a broad range of subjects, designed to test the reasoning prowess of state-of-the-art AI models.

## What problem it solves
It addresses the problem of "benchmark saturation," where frontier models achieve near-perfect scores on traditional tests like MMLU. HLE provides expert-level questions that even graduate-level specialists find challenging, offering a more precise measurement of advanced model capabilities.

## Where it fits in the pipeline
**Reason (Benchmark)**

## Typical use cases (in this homelab / family automation context)
- Evaluating whether a new local LLM (run via Ollama) is capable of handling complex administrative or technical reasoning tasks.
- Comparing frontier models (GPT-4o, Claude 3.5) for high-stakes decision-making in automation workflows.

## Integration points
- **Artificial Analysis**: Often cited in leaderboard comparisons.
- **Hugging Face**: Results and datasets are frequently hosted and discussed on the Open LLM Leaderboard.

## Licensing and cost
- **Open Source**: The dataset is publicly available for research.
- **Cost**: Free to access the dataset; costs associated with model inference.

## Strengths
- High subject diversity (Mathematics, Physics, Biology, CS, etc.).
- Systematically difficult; current frontier models still exhibit low accuracy.
- Experts-vetted and filtered to ensure reasoning over memorization.

## Limitations
- Computationally expensive to run across the entire set.
- Primarily focused on academic knowledge rather than specific tool use.

## Alternatives / Related tools
- **MMLU** (Massive Multitask Language Understanding)
- **GPQA** (Graduate-Level Google-Proof Q&A)

## Links
- [Official Website](https://scale.com/leaderboard/humanitys_last_exam)
- [Wikipedia](https://en.wikipedia.org/wiki/Humanity%27s_Last_Exam)
