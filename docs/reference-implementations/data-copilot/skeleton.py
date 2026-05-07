"""Reference skeleton for the layered Data Copilot Text-to-SQL pipeline.

The module intentionally uses deterministic mock logic instead of live LLM calls so
it can be executed in documentation CI. Replace the methods that return static
values with provider calls while preserving the Pydantic contracts.
"""

from __future__ import annotations

import asyncio
import math
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


# --- 1. Schema Definitions (Pydantic for validation) ---


class WorkspaceContext(BaseModel):
    workspace_id: str
    description: str
    db_connection_string: str


class IntentOutput(BaseModel):
    metrics: list[str]
    dimensions: list[str]
    filters: dict[str, str]
    time_range: str | None = "last_30_days"
    clarification_needed: str | None = None


class TableSelection(BaseModel):
    selected_tables: list[str]
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)


class PrunedSchema(BaseModel):
    table_name: str
    columns: list[str]


class TokenStats(BaseModel):
    estimated_tokens: int
    pruning_ratio: float


class ModelRoute(BaseModel):
    layer: str
    primary_model: str
    fallback_model: str
    max_prompt_tokens: int
    reason: str


class ReviewStatus(StrEnum):
    APPROVED = "approved"
    NEEDS_CORRECTION = "needs_correction"
    REJECTED = "rejected"


class HumanReviewDecision(BaseModel):
    status: ReviewStatus
    corrected_tables: list[str] | None = None
    corrected_columns: dict[str, list[str]] | None = None
    note: str | None = None


class SqlOutput(BaseModel):
    sql: str
    assumptions: list[str]
    model_route: ModelRoute
    estimated_prompt_tokens: int


# --- 2. Token Control & Pruning Utilities ---


def estimate_tokens(text: str) -> int:
    """Rough token estimation for routing decisions (4 chars per token)."""
    return math.ceil(len(text) / 4)


def calculate_pruning_ratio(original_cols: int, pruned_cols: int) -> float:
    if original_cols == 0:
        return 0.0
    return 1 - (pruned_cols / original_cols)


# --- 3. Agent Interfaces (Skeleton) ---


class DataCopilotPipeline:
    """Deterministic skeleton showing each Text-to-SQL layer and review point."""

    def __init__(self) -> None:
        # In production, initialize LLM clients, embeddings, and schema catalogs here.
        self.full_schema_mock: dict[str, list[str]] = {
            "items": [
                "id",
                "name",
                "quantity",
                "purchase_price",
                "category_id",
                "room",
                "created_at",
                "updated_at",
                "tags",
                "notes",
                "location_detail",
            ],
            "categories": ["id", "name", "description", "parent_id", "slug", "icon"],
            "orders": ["id", "order_date", "total_amount", "vendor_id", "status"],
        }
        self.model_routes = {
            "router": ModelRoute(
                layer="router",
                primary_model="local:qwen3:1.7b",
                fallback_model="local:qwen3:8b",
                max_prompt_tokens=500,
                reason="The workspace router is a low-token classification task.",
            ),
            "intent": ModelRoute(
                layer="intent",
                primary_model="local:qwen3:8b",
                fallback_model="hosted:gpt-5.4-mini",
                max_prompt_tokens=1_500,
                reason="Intent extraction needs stronger metric and date reasoning.",
            ),
            "table": ModelRoute(
                layer="table",
                primary_model="hosted:groq-open-model",
                fallback_model="hosted:gpt-5.4-mini",
                max_prompt_tokens=2_000,
                reason="Table selection benefits from stronger reasoning but only sees table summaries.",
            ),
            "prune": ModelRoute(
                layer="prune",
                primary_model="local:qwen3:8b",
                fallback_model="hosted:claude-haiku-4.5",
                max_prompt_tokens=2_000,
                reason="Column pruning is structured-output heavy and cheap to verify.",
            ),
            "sql": ModelRoute(
                layer="sql",
                primary_model="hosted:gpt-5.4-mini",
                fallback_model="hosted:claude-haiku-4.5",
                max_prompt_tokens=3_000,
                reason="SQL syntax generation should use the most reliable low-cost route.",
            ),
        }

    async def workspace_router(self, query: str) -> WorkspaceContext:
        """Layer 1: Route query to a specific domain."""
        print(f"Routing query with {self.model_routes['router'].primary_model}: {query}")
        return WorkspaceContext(
            workspace_id="inventory",
            description="Home Inventory and Assets",
            db_connection_string="sqlite:///home_inventory.db",
        )

    async def intent_agent(self, query: str, context: WorkspaceContext) -> IntentOutput:
        """Layer 2: Extract structured intent."""
        print(f"Extracting intent for workspace {context.workspace_id}: {query}")
        return IntentOutput(
            metrics=["quantity", "purchase_price"],
            dimensions=["category"],
            filters={"room": "Kitchen"},
            time_range="last_month",
        )

    async def table_agent(self, intent: IntentOutput) -> TableSelection:
        """Layer 3: Select relevant tables."""
        print(f"Selecting tables for intent metrics: {intent.metrics}")
        return TableSelection(
            selected_tables=["items", "categories"],
            rationale="Need 'items' for quantity/price and 'categories' for grouping.",
            confidence=0.82,
        )

    def review_table_selection(
        self,
        selection: TableSelection,
        decision: HumanReviewDecision | None = None,
    ) -> TableSelection:
        """Human correction point for wrong-table failures."""
        if decision is None or decision.status == ReviewStatus.APPROVED:
            return selection
        if decision.status == ReviewStatus.NEEDS_CORRECTION and decision.corrected_tables:
            return selection.model_copy(update={"selected_tables": decision.corrected_tables})
        raise ValueError(f"Table selection rejected: {decision.note or 'no reason provided'}")

    async def column_prune_agent(
        self,
        tables: list[str],
        intent: IntentOutput,
    ) -> tuple[list[PrunedSchema], TokenStats]:
        """Layer 4: Prune columns to minimize prompt size."""
        print(f"Pruning columns for tables: {tables}")

        pruned_results: list[PrunedSchema] = []
        total_original_cols = 0
        total_pruned_cols = 0

        for table in tables:
            all_cols = self.full_schema_mock.get(table, [])
            total_original_cols += len(all_cols)

            pruned_cols = [
                col
                for col in all_cols
                if col in ["id", "category_id"]
                or col in intent.metrics
                or col in intent.dimensions
                or col in intent.filters
            ]

            pruned_results.append(PrunedSchema(table_name=table, columns=pruned_cols))
            total_pruned_cols += len(pruned_cols)

        stats = TokenStats(
            estimated_tokens=estimate_tokens(str(pruned_results)),
            pruning_ratio=calculate_pruning_ratio(total_original_cols, total_pruned_cols),
        )
        print(
            "Pruning complete. "
            f"Ratio: {stats.pruning_ratio:.2%}, Estimated Tokens: {stats.estimated_tokens}"
        )
        return pruned_results, stats

    def review_pruned_schema(
        self,
        schema: list[PrunedSchema],
        decision: HumanReviewDecision | None = None,
    ) -> list[PrunedSchema]:
        """Human correction point for wrong-column or wrong-metric failures."""
        if decision is None or decision.status == ReviewStatus.APPROVED:
            return schema
        if decision.status == ReviewStatus.NEEDS_CORRECTION and decision.corrected_columns:
            corrected: list[PrunedSchema] = []
            for table_schema in schema:
                columns = decision.corrected_columns.get(table_schema.table_name, table_schema.columns)
                corrected.append(table_schema.model_copy(update={"columns": columns}))
            return corrected
        raise ValueError(f"Pruned schema rejected: {decision.note or 'no reason provided'}")

    async def sql_generator(
        self,
        intent: IntentOutput,
        schema: list[PrunedSchema],
        stats: TokenStats,
    ) -> SqlOutput:
        """Layer 5: Generate the final SQL from only the pruned schema + intent."""
        prompt_payload: dict[str, Any] = {
            "intent": intent.model_dump(),
            "schema": [table.model_dump() for table in schema],
        }
        estimated_prompt_tokens = estimate_tokens(str(prompt_payload))
        route = self.model_routes["sql"]
        if estimated_prompt_tokens > route.max_prompt_tokens:
            route = route.model_copy(update={"primary_model": route.fallback_model})

        print(f"Generating SQL using {route.primary_model} and {stats.estimated_tokens} schema tokens")
        return SqlOutput(
            sql=(
                "SELECT c.name, SUM(i.quantity * i.purchase_price) AS estimated_spend "
                "FROM items i JOIN categories c ON i.category_id = c.id "
                "WHERE i.room = 'Kitchen' GROUP BY c.name;"
            ),
            assumptions=["purchase_price is the spend proxy because no order line table was selected"],
            model_route=route,
            estimated_prompt_tokens=estimated_prompt_tokens,
        )


# --- 4. Example Execution ---


async def main() -> None:
    pipeline = DataCopilotPipeline()

    query = "How much did I spend on kitchen items last month?"
    workspace = await pipeline.workspace_router(query)
    intent = await pipeline.intent_agent(query, workspace)
    tables = await pipeline.table_agent(intent)
    reviewed_tables = pipeline.review_table_selection(tables)
    pruned_schema, stats = await pipeline.column_prune_agent(reviewed_tables.selected_tables, intent)
    reviewed_schema = pipeline.review_pruned_schema(pruned_schema)
    sql = await pipeline.sql_generator(intent, reviewed_schema, stats)

    print(f"\nFinal Generated SQL:\n{sql.sql}")
    print(f"Assumptions: {sql.assumptions}")


if __name__ == "__main__":
    asyncio.run(main())
