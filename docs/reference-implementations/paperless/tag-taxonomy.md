# Reference Implementation: Paperless Tag Taxonomy

## What it is
A hierarchical tagging system designed for Paperless-ngx that organizes personal and household documents into actionable categories. It balances organizational needs (folders/categories) with workflow states (status/actions). As of June 2026, it is optimized for high-reasoning models like **Claude 4.7** and **GPT-5.5** to perform autonomous classification.

## What problem it solves
Flat document storage quickly becomes unmanageable as volume grows. Without a standardized taxonomy, users struggle to find files, and automated agents cannot reliably trigger specific workflows (like paying a bill or extracting a warranty). This taxonomy provides the "semantic hooks" necessary for both humans and machines to navigate the archive.

## Where it fits in the stack
The taxonomy sits at the **Organization/Metadata layer** of the document management system. It acts as the primary index used by **Search**, **Automated Workflows** (n8n, Python scripts), and **AI Agents** (leveraging **Model Context Protocol**) to filter and process documents.

## Typical use cases
- **Workflow Automation**: Moving a document from `inbox` to `needs-action` to trigger a reminder.
- **Tax Preparation**: Quickly retrieving all documents tagged with `Keep-7-years` or `Finance/Bill`.
- **Legacy Preservation**: Categorizing scanned physical photos and historical records for long-term archiving.
- **Agentic Routing**: Using **Llama 4 Maverick** to analyze document sentiment and apply urgent status tags.

## Strengths
- **Action-Oriented**: Clearly separates "State" (what needs to be done) from "Category" (what the document is).
- **Extensible**: The `Category/Subcategory` pattern allows for infinite growth without breaking existing logic.
- **Machine-Readable**: Simple, consistent naming conventions are easy for LLMs and scripts to parse.
- **MCP Compatibility**: Designed to be exposed via MCP servers to agentic IDEs and assistants.

## Limitations
- **Maintenance**: Requires discipline to ensure every document is tagged correctly (unless fully automated).
- **Tool Support**: While ideal for Paperless-ngx, other DMS tools may have different tagging limitations.
- **Over-Categorization**: Risk of creating too many niche tags that humans won't remember to use.

## When to use it
- When setting up a new Paperless-ngx instance.
- When designing automated "Scan-to-Action" pipelines.
- For managing multi-generational family archives with high-volume ingest.

## When not to use it
- For extremely small document sets (under 100 files) where a simple search is sufficient.
- If using a DMS that relies entirely on full-text search without robust tagging support.

## Agentic Implementation (June 2026)
With the release of **Claude 4.7** and **GPT-5.5**, tagging is no longer a manual chore.
- **Autonomous Inbox Management**: Agents monitor the `inbox` tag and apply category tags based on visual and text analysis.
- **MCP Integration**: The [Paperless Tool](../../scripts/paperless_tool.py) allows agents to query documents by tag and update taxonomy programmatically.
- **Llama 4 Maverick Optimization**: Local models can now perform high-accuracy tagging on-device, preserving privacy for sensitive financial documents.

## Core Status Tags
- `inbox`: Document just arrived, needs manual or auto review.
- `needs-action`: Requires a human to perform a task (e.g. pay bill).
- `processed`: Automation has finished its work (e.g. calendar event created).
- `automation-failed`: LLM or script hit an error.

## Category Tags
- `Admin/Warranty` (receipts/consumer protection)
- `Admin/Manual` (product manuals/troubleshooting)
- `Finance/Bill`
- `School/Correspondence`
- `Health/Record`
- `Admin/Government`

## History & Archive Tags
- `History/Family-Record`: Letters, journals, family trees.
- `History/Photo-Archive`: Scanned physical photos.
- `History/Genealogy`: Birth/Death certificates (historic), census records.

## Retention Tags
- `Keep-7-years`: Tax related.
- `Keep-forever`: Birth certificates, deeds.
- `Ephemeral`: Coupons, flyers.

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The implementation platform for this taxonomy.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md): A workflow that uses these tags to trigger tasks.
- [Warranty Extraction](../../reference-implementations/llm-prompts/warranty-extraction.md): Uses the `Admin/Warranty` tag as a trigger.
- [Manual Metadata Schema](../../reference-implementations/metadata-schemas/manuals.md): Uses the `Admin/Manual` tag.
- [Webhook Ingestion](../../reference-implementations/paperless/webhook-ingestion.md): How documents and tags enter the system.
- [n8n](../../services/n8n.md): The engine that processes tags and triggers actions.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): The "brain" that interacts with the tagged archive.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md): The interface for agents to interact with Paperless.

## Sources / References
- [Paperless-ngx Tags Documentation](https://docs.paperless-ngx.com/usage/#tags)
- [Tagging Strategies for Personal Documents](https://github.com/joanmarcriera/Home-office-automations)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-08
