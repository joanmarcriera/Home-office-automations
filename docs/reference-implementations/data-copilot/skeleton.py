from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import math

# --- 1. Schema Definitions (Pydantic for validation) ---

class WorkspaceContext(BaseModel):
    workspace_id: str
    description: str
    db_connection_string: str

class IntentOutput(BaseModel):
    metrics: List[str]
    dimensions: List[str]
    filters: Dict[str, str]
    time_range: Optional[str] = "last_30_days"

class TableSelection(BaseModel):
    selected_tables: List[str]
    rationale: str

class PrunedSchema(BaseModel):
    table_name: str
    columns: List[str]

class TokenStats(BaseModel):
    estimated_tokens: int
    pruning_ratio: float

# --- 2. Token Control & Pruning Utilities ---

def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars per token)."""
    return math.ceil(len(text) / 4)

def calculate_pruning_ratio(original_cols: int, pruned_cols: int) -> float:
    if original_cols == 0:
        return 0.0
    return 1 - (pruned_cols / original_cols)

# --- 3. Agent Interfaces (Skeleton) ---

class DataCopilotPipeline:
    def __init__(self):
        # In a real implementation, you'd initialize LLM clients here
        self.full_schema_mock = {
            "items": ["id", "name", "quantity", "purchase_price", "category_id", "room", "created_at", "updated_at", "tags", "notes", "location_detail"],
            "categories": ["id", "name", "description", "parent_id", "slug", "icon"],
            "orders": ["id", "order_date", "total_amount", "vendor_id", "status"]
        }

    async def workspace_router(self, query: str) -> WorkspaceContext:
        """Layer 1: Route query to a specific domain."""
        print(f"Routing query: {query}")
        # Mock logic: Small model (e.g. Qwen 2.5 0.8B) classification
        return WorkspaceContext(
            workspace_id="inventory",
            description="Home Inventory and Assets",
            db_connection_string="sqlite:///home_inventory.db"
        )

    async def intent_agent(self, query: str, context: WorkspaceContext) -> IntentOutput:
        """Layer 2: Extract structured intent."""
        print(f"Extracting intent for: {query}")
        # Mock logic: Extract metrics and filters
        return IntentOutput(
            metrics=["quantity", "purchase_price"],
            dimensions=["category"],
            filters={"room": "Kitchen"}
        )

    async def table_agent(self, intent: IntentOutput) -> TableSelection:
        """Layer 3: Select relevant tables."""
        print(f"Selecting tables for intent metrics: {intent.metrics}")
        # In practice, use semantic search over table descriptions.
        selection = TableSelection(
            selected_tables=["items", "categories"],
            rationale="Need 'items' for quantity/price and 'categories' for grouping."
        )

        # HITL Point: Table Approval
        print(f"\n[HITL] Table Approval: {selection.selected_tables}")
        print(f"Rationale: {selection.rationale}")
        print("Human approved tables: Yes\n")

        return selection

    async def column_prune_agent(self, tables: List[str], intent: IntentOutput) -> List[PrunedSchema]:
        """Layer 4: Prune columns to minimize prompt size (Token Control)."""
        print(f"Pruning columns for tables: {tables}")

        pruned_results = []
        total_original_cols = 0
        total_pruned_cols = 0

        for table in tables:
            all_cols = self.full_schema_mock.get(table, [])
            total_original_cols += len(all_cols)

            # Skeletal logic: keep primary keys and columns mentioned in intent.
            # In a real agent, the LLM would pick these based on the question.
            pruned_cols = [
                col for col in all_cols
                if col in ["id", "category_id"]
                or col in intent.metrics
                or col in intent.dimensions
                or col in intent.filters
            ]

            pruned_results.append(PrunedSchema(table_name=table, columns=pruned_cols))
            total_pruned_cols += len(pruned_cols)

        stats = TokenStats(
            estimated_tokens=estimate_tokens(str(pruned_results)),
            pruning_ratio=calculate_pruning_ratio(total_original_cols, total_pruned_cols)
        )
        print(f"Pruning Complete. Ratio: {stats.pruning_ratio:.2%}, Estimated Tokens: {stats.estimated_tokens}")

        # HITL Point: Column Approval
        print("[HITL] Pruned Schema Approval:")
        for p in pruned_results:
            print(f"  - {p.table_name}: {p.columns}")
        print("Human approved columns: Yes\n")

        return pruned_results

    async def sql_generator(self, intent: IntentOutput, schema: List[PrunedSchema]) -> str:
        """Layer 5: Generate the final SQL."""
        print("Generating SQL using pruned schema...")
        # Input to prompt: Only the pruned schema + intent JSON
        return "SELECT c.name, SUM(i.quantity) FROM items i JOIN categories c ON i.category_id = c.id WHERE i.room = 'Kitchen' GROUP BY c.name;"

# --- 4. Example Execution ---

async def main():
    pipeline = DataCopilotPipeline()

    # 1. Route
    query = "How much did I spend on kitchen items last month?"
    workspace = await pipeline.workspace_router(query)

    # 2. Intent
    intent = await pipeline.intent_agent(query, workspace)

    # 3. Tables
    tables = await pipeline.table_agent(intent)

    # 4. Prune (Critical Token Control Point)
    pruned_schema = await pipeline.column_prune_agent(tables.selected_tables, intent)

    # 5. Generate
    sql = await pipeline.sql_generator(intent, pruned_schema)

    print(f"\nFinal Generated SQL:\n{sql}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
