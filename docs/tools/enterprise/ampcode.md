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

# List available agents in the enterprise registry
amp agents list
```

## API examples
Amp functionality is primarily exposed through its CLI and its integration with MCP servers. Configuration can be managed via environment variables for automation. You can also interact with the underlying Sourcegraph API that Amp utilizes for deeper repository insights.

### Python Example: Fetching Repository Context (via GraphQL)
Amp leverages Sourcegraph's GraphQL API for deep code search and context retrieval.

```python
import os
import requests
import json

def get_amp_repo_context(repo_name, query_text):
    api_key = os.getenv("AMP_API_KEY")
    url = "https://sourcegraph.com/.api/graphql"

    # GraphQL query for cross-repository search
    query = """
    query Search($query: String!) {
      search(query: $query, version: V2) {
        results {
          results {
            ... on FileMatch {
              file {
                path
                repository {
                  name
                }
              }
              lineMatches {
                lineNumber
                preview
              }
            }
          }
        }
      }
    }
    """

    search_string = f"repo:^{repo_name}$ {query_text}"
    variables = {"query": search_string}
    headers = {"Authorization": f"token {api_key}"}

    response = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status {response.status_code}: {response.text}")

# Example: Search for authentication logic in a specific repo
# context = get_amp_repo_context("github.com/org/project", "type:file login")
# print(json.dumps(context, indent=2))
```

### Data Contracts
AmpCode follows strict data contracts for agentic interaction:
- **Input**: Natural language task or structured JSON job definition.
- **Context**: Dynamic injection of repository snippets via Sourcegraph embeddings and symbol graphs.
- **Output**: Git diffs, log reports, or status updates conforming to standardized schemas.
- **Verification**: Automatic triggering of CI pipelines or test suites defined in the repository contract.

## Related tools / concepts

- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)
- [Claude Code](../development_ops/claude-code.md)
- [Sourcegraph Cody](https://sourcegraph.com/cody)

## Sources / references
- [AmpCode Official Site](https://ampcode.com/)
- [Sourcegraph API Documentation](https://sourcegraph.com/docs/api/graphql)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
