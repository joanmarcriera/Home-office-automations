# ASTA

## What it is
**ASTA** (Adaptive Scientific Task Assistant) is an open-source research automation framework and agent orchestration platform developed by Allen AI (Allen Institute for AI) specifically engineered to accelerate scientific discovery, automated literature analysis, hypothesis generation, and experimental code execution across biomedical, chemical, and physical science domains. By unifying domain-specialized LLMs, tool retrieval indices, semantic paper graph connections (Semantic Scholar API), and sandbox Python code execution backends, ASTA enables researchers to execute complex multi-step scientific workflows using natural language instructions.

While general-purpose developer agents excel at software engineering or web search, scientific workflows present unique challenges: complex domain taxonomies, dense citation graphs, high precision requirements, and domain-specific code dependencies (Biopython, RDKit, ASE, PyTorch Geometric). ASTA solves this by combining specialized scientific memory modules, structured literature reasoning chains, and secure tool execution sandboxes into a robust, extensible agentic architecture.

```
+-----------------------------------------------------------------------------------+
|                                ASTA ARCHITECTURE                                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------------+       +-----------------------------------------+  |
|  | Scientific Query / Task   | ----> | ASTA Agent Orchestrator Engine          |  |
|  | "Analyze PDB structure"   |       | (Literature Retriever & Task Decomposer)|  |
|  +---------------------------+       +-----------------------------------------+  |
|                                                           |                       |
|                                                           v                       |
|                                      +-----------------------------------------+  |
|                                      | Scientific Context & Tool Selector      |  |
|                                      | - Semantic Scholar Graph Index          |  |
|                                      | - RDKit / Biopython / ASE Tool Registry |  |
|                                      | - FastMCP 3.1 Tool Connector           |  |
|                                      +-----------------------------------------+  |
|                                                           |                       |
|                                                           v                       |
|  +---------------------------+       +-----------------------------------------+  |
|  | Research Report & Code    | <---- | Ephemeral Scientific Code Sandbox       |  |
|  | Synthesis (Markdown / PDF)|       | (Jupyter Kernel / Python Execution)     |  |
|  +---------------------------+       +-----------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
- **Scientific Literature Fragmentation**: Connects millions of research papers, preprints, and citation graphs (Semantic Scholar) directly into agent reasoning context without manual keyword searching.
- **Domain-Specific Tool Integration**: Automates execution of specialized scientific libraries (RDKit for chemical structures, Biopython for genomic sequences, PyG for molecular graphs) without requiring manual script assembly.
- **Hypothesis Formulation & Verification**: Helps researchers generate testable research hypotheses grounded in peer-reviewed literature and validate them against benchmark datasets.
- **Reproducibility & Provenance Tracking**: Tracks full reasoning logs, citation links, execution code snippets, and data provenance steps for complete scientific transparency.

## Where it fits in the stack
**Frameworks / Scientific AI / Research Automation**. ASTA operates as a domain-specialized agent framework sitting above foundational LLMs and research databases, serving as an intelligent middleware orchestrator for scientific research labs.

```
+-----------------------------------------------------------------------------------+
|                             SCIENTIFIC RESEARCH STACK                             |
+-----------------------------------------------------------------------------------+
| Research Interface Layer: Web Studio / Jupyter Lab / CLI / IDE Extensions         |
+-----------------------------------------------------------------------------------+
| Scientific Orchestrator : ASTA Framework (AllenAI Research Automation Engine)     |
+-----------------------------------------------------------------------------------+
| Tool & Data Providers   : FastMCP 3.1 Tools / Semantic Scholar API / ChemBL / PDB   |
+-----------------------------------------------------------------------------------+
| Compute Execution       : Python Scientific Sandbox / PyTorch / RDKit / CUDA      |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Automated Literature Review**: Summarizing hundreds of relevant research papers, synthesizing consensus findings, and identifying gaps in current literature.
- **Molecular & Genomic Data Analysis**: Writing and running Python scripts using RDKit or Biopython to analyze protein structures, gene expressions, or small molecule properties.
- **Experimental Protocol Design**: Drafting laboratory experimental procedures, safety checklists, and chemical synthesis routes based on published research protocols.
- **Scientific Benchmark Evaluation**: Evaluating performance metrics for novel machine learning models across standardized scientific benchmark datasets.

## Strengths
- **Allen AI Scientific Ecosystem**: Built with deep native access to Semantic Scholar, SciSight, and specialized open-weights scientific models (e.g., OLMo, MolMo).
- **Domain-Grounded Reasoning**: Trained to minimize scientific hallucinations by enforcing strict paper citation mapping and quantitative verification.
- **Extensible FastMCP Tool Architecture**: Easily connects custom laboratory hardware APIs, database tools, and proprietary computational chemistry algorithms.
- **Open-Source & Transparent**: Fully open-source codebase and model weights, ensuring complete privacy for sensitive proprietary research.

## Limitations
- **High Computational Requirements**: Running full local ASTA stacks with specialized scientific models requires GPU acceleration (NVIDIA RTX/A100/H100).
- **Domain Precision Boundaries**: Complex physical chemistry or quantum mechanics problems still require human domain expert validation.
- **Third-Party API Rates**: High-volume Semantic Scholar API querying requires API key management to avoid throughput rate limits.

## When to use it
- When conducting automated literature search, paper summarization, and citation network mapping across scientific fields.
- To build autonomous research assistants that perform data analysis using RDKit, Biopython, or specialized scientific libraries.
- For academic labs, pharmaceutical companies, and AI research organizations seeking reproducible, traceable agentic research pipelines.

## When not to use it
- For general web software development or web scraping tasks unrelated to scientific research.
- In lightweight mobile or embedded applications without access to scientific compute runtimes.
- When simple static database queries are sufficient without multi-step literature synthesis or code execution.

## Getting started

### Prerequisites
- Python 3.10+ with `pip` and PyTorch.
- Semantic Scholar API Key (optional, for higher rate limits).

### Installation via Pip
```bash
# Install ASTA research framework
pip install asta-ai rdkit biopython fastmcp pydantic
```

### Quickstart Execution with Python
```python
from asta import ScientificAgent

# Initialize ASTA Agent
agent = ScientificAgent(model="allenai/olmo-7b-instruct", enable_sandbox=True)

# Run literature review and code analysis task
response = agent.run(
    task="Search recent 2026 papers on CRISPR gene editing efficiency in mammalian cells, identify key protein markers, and write a Python script to filter sequence motifs."
)

print("Research Summary:\n", response.summary)
print("Generated Code:\n", response.generated_code)
```

## CLI examples

### Executing Literature Query via ASTA CLI
```bash
# Query literature and generate Markdown research report
asta query \
  --prompt "Synthesize current approaches for small molecule binding affinity prediction using Graph Neural Networks" \
  --output report.md \
  --format markdown
```

### Running Scientific Code Sandbox Test
```bash
# Run ASTA agent with RDKit chemical validation sandbox
asta sandbox run \
  --code "from rdkit import Chem; mol = Chem.MolFromSmiles('CC(=O)OC1=CC=CC=C1C(=O)O'); print('Aspirin MW:', Chem.Descriptors.ExactMolWt(mol))"
```

## API examples

### FastMCP 3.1 Scientific Tool Server Integration
This example demonstrates a FastMCP 3.1 tool server providing ASTA agents with automated RDKit chemical structure analysis tools:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional

mcp = FastMCP("ASTA-Chemical-Analysis-Server")

class ChemicalAnalysisRequest(BaseModel):
    smiles_string: str = Field(..., description="SMILES representation of chemical structure (e.g. Aspirin: 'CC(=O)OC1=CC=CC=C1C(=O)O')")
    calculate_descriptors: bool = Field(default=True, description="Calculate molecular weight and logP")

class ChemicalAnalysisResponse(BaseModel):
    is_valid: bool = Field(..., description="Whether SMILES string is valid")
    molecular_weight: Optional[float] = Field(default=None, description="Exact molecular weight in g/mol")
    log_p: Optional[float] = Field(default=None, description="Calculated Partition Coefficient (LogP)")
    formula: Optional[str] = Field(default=None, description="Chemical molecular formula")

@mcp.tool()
def analyze_chemical_structure(request: ChemicalAnalysisRequest) -> ChemicalAnalysisResponse:
    """Analyzes chemical structures for ASTA scientific agent workflows."""
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors, rdMolDescriptors

        mol = Chem.MolFromSmiles(request.smiles_string)
        if mol is None:
            return ChemicalAnalysisResponse(is_valid=False)

        mw = round(float(Descriptors.ExactMolWt(mol)), 4)
        logp = round(float(Descriptors.MolLogP(mol)), 4)
        formula = rdMolDescriptors.CalcMolFormula(mol)

        return ChemicalAnalysisResponse(
            is_valid=True,
            molecular_weight=mw,
            log_p=logp,
            formula=formula
        )
    except Exception as ex:
        return ChemicalAnalysisResponse(is_valid=False)

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Scientific Research Plan Schema
```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class PaperCitation(BaseModel):
    paper_id: str = Field(..., description="Semantic Scholar Paper ID or DOI")
    title: str = Field(...)
    year: int = Field(..., ge=1900, le=2030)
    primary_author: str = Field(...)

class ResearchPlan(BaseModel):
    hypothesis: str = Field(..., description="Core scientific hypothesis being tested")
    key_citations: List[PaperCitation] = Field(default_factory=list)
    required_libraries: List[str] = Field(default_factory=lambda: ["rdkit", "biopython"])
    confidence_score: float = Field(..., ge=0.0, le=1.0)

    @field_validator("hypothesis")
    @classmethod
    def validate_hypothesis_length(cls, v: str) -> str:
        if len(v.strip()) < 20:
            raise ValueError("Research hypothesis must be descriptive (at least 20 characters)")
        return v

# Schema validation demonstration
try:
    plan = ResearchPlan(
        hypothesis="Targeting protein kinase C alpha increases small molecule permeability across cell membranes.",
        key_citations=[
            PaperCitation(paper_id="10.1038/s41586-025-00001", title="CRISPR Gene Editing Innovations", year=2025, primary_author="Doudna et al.")
        ],
        confidence_score=0.92
    )
    print("Validated Research Plan:", plan.model_dump_json(indent=2))
except ValidationError as ex:
    print("Schema Error:", ex.json())
```

## Related tools / concepts
- [GraphRAG](../frameworks/graphrag.md) — Knowledge graph-based retrieval augmented generation engine.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Universal protocol for agent tool integrations.
- [Paperless-AI](../../services/paperless-ai.md) — Local AI document management and indexing platform.
- [Smolagents](../frameworks/smolagents.md) — Lightweight agent framework developed by Hugging Face.

## Sources / references
- [ASTA AllenAI Release Announcement](https://huggingface.co/blog/allenai/astabrief)
- [Allen Institute for AI Research Platform](https://allenai.org/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
