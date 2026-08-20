# AmpCode

## What it is
AmpCode is an enterprise-grade platform for building and scaling AI agents with a focus on reliability, security, and developer productivity. Developed by Sourcegraph, it serves as the production-grade agentic runtime for Cody-powered workflows, supporting FastMCP 3.1 integration across enterprise repositories.

## What problem it solves
It provides the infrastructure needed to transition from experimental agent prototypes to production-ready enterprise applications. It leverages frontier models like **Claude 5.1** and **GPT-5.5** to manage complex, multi-step engineering tasks across massive distributed codebases with deterministic verification loops.

## Where it fits in the stack
**Category**: Enterprise AI / Development & Ops. It sits at the intersection of code intelligence and agentic orchestration, integrating directly with enterprise MCP servers and repository indices.

## Typical use cases
- **Enterprise Repository Orchestration**: Managing complex tasks across massive, distributed codebases with trillions of lines of code.
- **Secure Agent Deployment**: Running agents in environments with strict security, compliance, and auditing requirements.
- **Developer Productivity at Scale**: Automating boilerplate, large-scale refactors, and tests across entire engineering organizations.
- **Automated Dependency Management**: Proactively identifying and updating stale dependencies across multiple projects using **Llama 4** and **Qwen 3.6** for local analysis.

## Strengths
- **Security-First**: Built for enterprise environments with robust authentication, auditing, sandboxed execution, and zero-trust policies.
- **Sourcegraph Integration**: Leverages Sourcegraph's deep code intelligence ([Cody](../development_ops/sourcegraph_cody.md)) for multi-repo context and graph-based reasoning.
- **High Reliability**: Focuses on deterministic outcomes and production-grade stability with built-in evaluation and verification loops.
- **SOTA 2027 Ready**: Native support for **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro** for advanced reasoning and code synthesis.

## Limitations
- **Closed Ecosystem**: Proprietary software that requires an enterprise license for full features.
- **Target Audience**: Less optimized for individual developers or small open-source projects compared to alternatives such as [Aider](../development_ops/aider.md).
- **Complexity**: Enterprise-scale features require significant configuration and infrastructure (e.g., dedicated Sourcegraph instance).
- **Cost**: Paid enterprise subscription model typically co-located with Sourcegraph deployment.

## When to use it
- In corporate environments where security and scalability are the top priorities for AI-assisted engineering.
- When you need an agent that can reason across thousands of repositories safely and consistently.
- If you are already invested in the Sourcegraph ecosystem and require FastMCP 3.1 protocol capabilities.

## When not to use it
- For personal projects or small teams where free, open-source alternatives like [Aider](../development_ops/aider.md) or [Claude Code](../development_ops/claude-code.md) are sufficient.
- If you require a fully transparent, open-weight model stack for all operations without enterprise infrastructure.

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

# Specify a custom log level and model (Early 2027 SOTA)
amp --execute "Explain this project" --model claude-5.1 --log-level debug

# Authenticate with an API key (for CI/CD pipelines)
export AMP_API_KEY="your-api-key"
amp --execute "run tests"

# List available agents in the enterprise registry
amp agents list
```

## API examples
Amp functionality is primarily exposed through its CLI and its integration with [Model Context Protocol (MCP 3.1)](../automation_orchestration/mcp.md) servers. Configuration can be managed via environment variables for automation. You can also interact with the underlying Sourcegraph API that Amp utilizes for deeper repository insights.

### Python Example: Fetching Repository Context with Pydantic v2 Validation
Amp leverages Sourcegraph's GraphQL API for deep code search and context retrieval. This example queries the endpoint and validates the payload strictly using **Pydantic v2**.

```python
import os
from typing import List, Optional
import requests
from pydantic import BaseModel, Field, ValidationError

# Pydantic v2 Response Models
class Repository(BaseModel):
    name: str = Field(description="The unique canonical repository identifier")

class FileInfo(BaseModel):
    path: str = Field(description="Relative file path within the repository")
    repository: Repository

class LineMatch(BaseModel):
    line_number: int = Field(validation_alias="lineNumber", description="Line number of match")
    preview: str = Field(description="Excerpt of matching code text")

class FileMatch(BaseModel):
    file: FileInfo
    line_matches: List[LineMatch] = Field(validation_alias="lineMatches", default_factory=list)

class SearchResult(BaseModel):
    results: List[FileMatch] = Field(default_factory=list)

class SearchResponseData(BaseModel):
    search: SearchResult

class GraphQLResponse(BaseModel):
    data: Optional[SearchResponseData] = None
    errors: Optional[List[dict]] = None

def get_amp_repo_context(repo_name: str, query_text: str) -> GraphQLResponse:
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
        try:
            # Parse and validate response with Pydantic v2
            validated_response = GraphQLResponse.model_validate(response.json())
            return validated_response
        except ValidationError as e:
            raise ValueError(f"Schema validation failed: {e.errors()}")
    else:
        raise Exception(f"Query failed with status {response.status_code}: {response.text}")

# Example usage:
# if __name__ == "__main__":
#     try:
#         context = get_amp_repo_context("github.com/org/project", "type:file login")
#         print(context.model_dump_json(indent=2))
#     except Exception as err:
#         print(f"Error: {err}")
```

## Related tools / concepts
- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)
- [Claude Code](../development_ops/claude-code.md)
- [Sourcegraph Cody](../development_ops/sourcegraph_cody.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude 5.1](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Llama 4](../ai_knowledge/local_llms.md)
- [Qwen 3.6](../ai_knowledge/local_llms.md)
- [Gemma 3](../ai_knowledge/local_llms.md)

## Sources / references
- [AmpCode Official Site](https://ampcode.com/)
- [Sourcegraph API Documentation](https://sourcegraph.com/docs/api/graphql)
- [AmpCode Release Notes - Early 2027](https://releasebot.io/updates/ampcode)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
