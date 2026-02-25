# Sweep.dev

## What it is
Sweep is an AI junior developer that transforms GitHub issues into pull requests. It can plan, write, and test code autonomously.

## What problem it solves
Automates the handling of small bugs and feature requests, allowing developers to focus on higher-level architecture.

## Where it fits in the pipeline
**Act (Development / Agent)**

## Typical use cases (in this homelab / family automation context)
- Opening an issue like "Add logging to the n8n sync script" and having Sweep generate the PR.
- Automatically fixing linting or documentation gaps identified in CI.

## Integration points
- **GitHub**: Tight integration via a GitHub App.
- **GitHub Actions**: Uses actions to run tests and verify its own code.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium
- **Free tier**: Yes (Limited tickets per month)
- **Self-hostable**: No

## Strengths
- High degree of autonomy.
- Native integration with the GitHub workflow.
- Includes testing in its "inner loop".

## Limitations
- Proprietary.
- Can be slow as it runs comprehensive planning and testing.

## Alternatives / Related tools
- **OpenHands**
- **Jules (Google)**

## Links
- [Official Website](https://sweep.dev)
- [GitHub](https://github.com/sweepai/sweep)
