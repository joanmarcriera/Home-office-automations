# AmpCode

## What it is
AmpCode is an enterprise-grade platform for building and scaling AI agents with a focus on reliability, security, and developer productivity.

## What problem it solves
It provides the infrastructure needed to transition from experimental agent prototypes to production-ready enterprise applications.

## Where it fits in the stack
**Category**: Enterprise AI

## Typical use cases
- **Enterprise Repository Orchestration**: Managing complex tasks across massive, distributed codebases.
- **Secure Agent Deployment**: Running agents in environments with strict security and compliance requirements.
- **Developer Productivity at Scale**: Automating boilerplate, refactors, and tests across entire engineering organizations.
- **Automated Dependency Management**: Proactively identifying and updating stale dependencies across multiple projects.

## Strengths
- **Security-First**: Built for enterprise environments with robust authentication and auditing.
- **Sourcegraph Integration**: Leverages Sourcegraph's deep code intelligence (Cody) for better context and reasoning across massive, distributed repositories.
- **High Reliability**: Focuses on deterministic outcomes and production-grade stability.
- **Agentic Orchestration**: Capable of managing multi-step workflows like large-scale refactoring or automated test generation across entire organizations.

## Limitations
- **Closed Ecosystem**: Proprietary software that requires an enterprise license for full features.
- **Target Audience**: Less optimized for individual developers or small open-source projects.

## When to use it
- In corporate environments where security and scalability are the top priorities.
- When you need an agent that can reason across thousands of repositories safely.

## When not to use it
- For personal projects or small teams where free, open-source alternatives like Aider are sufficient.
- If you require a fully transparent, open-weight model stack.

## Licensing and cost
- **Open Source**: No (Proprietary)
- **Cost**: Paid (Enterprise subscription)
- **Self-hostable**: Yes (for Enterprise customers)

## Getting started

### Installation
Amp can be installed via a shell script or npm:

```bash
# Recommended for macOS, Linux, and WSL
curl -fsSL https://ampcode.com/install.sh | bash

# Via npm
npm install -g @sourcegraph/amp
```

### Basic usage
Start an interactive AI coding session:

```bash
amp
```

## CLI examples
```bash
# Run a one-shot command in non-interactive mode
amp --execute "Add error handling to the API endpoints"

# Specify a custom log level
amp --execute "Explain this project" --log-level debug

# Authenticate with an API key (for CI/CD)
export AMP_API_KEY="your-api-key"
amp --execute "run tests"
```

## API examples
Amp functionality is primarily exposed through its CLI and its integration with MCP servers. Configuration can be managed via environment variables for automation. You can also interact with the underlying Sourcegraph API that Amp utilizes for deeper repository insights.

### Python Example: Fetching Repository Context
```python
import os
import requests

def get_amp_repo_context(repo_name):
    api_key = os.getenv("AMP_API_KEY")
    # Amp leverages Sourcegraph GraphQL API
    url = "https://sourcegraph.com/.api/graphql"
    query = """
    query Repository($name: String!) {
      repository(name: $name) {
        id
        description
        url
      }
    }
    """
    headers = {"Authorization": f"token {api_key}"}
    response = requests.post(url, json={"query": query, "variables": {"name": repo_name}}, headers=headers)
    return response.json()

# Example usage
# context = get_amp_repo_context("github.com/sourcegraph/amp")
# print(context)
```

### Data Contracts
AmpCode follows strict data contracts for agentic interaction:
- **Input**: Natural language task or structured JSON job definition.
- **Context**: Dynamic injection of repository snippets via Sourcegraph embeddings.
- **Output**: Git diffs, log reports, or status updates conforming to standardized schemas.

## Related tools / concepts

- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)
- [Claude Code](../development_ops/claude-code.md)

## Sources / references
- [AmpCode Official Site](https://ampcode.com/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
