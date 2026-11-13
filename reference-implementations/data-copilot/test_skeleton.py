import asyncio

from skeleton import (
    DataCopilotPipeline,
    HumanReviewDecision,
    IntentOutput,
    ReviewStatus,
    TableSelection,
    PrunedSchema,
    WorkspaceContext,
)


def test_pipeline_flow():
    asyncio.run(_pipeline_flow())


async def _pipeline_flow():
    pipeline = DataCopilotPipeline()
    query = "Test query"

    workspace = await pipeline.workspace_router(query)
    assert isinstance(workspace, WorkspaceContext)
    assert workspace.workspace_id == "inventory"

    intent = await pipeline.intent_agent(query, workspace)
    assert isinstance(intent, IntentOutput)
    assert "quantity" in intent.metrics

    tables = await pipeline.table_agent(intent)
    assert "items" in tables.selected_tables

    pruned, stats = await pipeline.column_prune_agent(tables.selected_tables, intent)
    assert len(pruned) > 0
    assert pruned[0].table_name == "items"
    assert stats.pruning_ratio > 0

    sql = await pipeline.sql_generator(intent, pruned, stats)
    assert "SELECT" in sql.sql
    assert sql.model_route.primary_model.startswith("hosted:")


def test_human_table_correction_point():
    pipeline = DataCopilotPipeline()
    selection = pipeline.review_table_selection(
        selection=TableSelection(
            selected_tables=["orders"],
            rationale="Ambiguous spend language.",
            confidence=0.51,
        ),
        decision=HumanReviewDecision(
            status=ReviewStatus.NEEDS_CORRECTION,
            corrected_tables=["items", "categories"],
            note="Inventory spend should use item purchase prices.",
        ),
    )
    assert selection.selected_tables == ["items", "categories"]


def test_human_column_correction_point():
    pipeline = DataCopilotPipeline()
    schema = [
        {"table_name": "items", "columns": ["id", "quantity"]},
        {"table_name": "categories", "columns": ["id", "name"]},
    ]
    corrected = pipeline.review_pruned_schema(
        schema=[PrunedSchema.model_validate(item) for item in schema],
        decision=HumanReviewDecision(
            status=ReviewStatus.NEEDS_CORRECTION,
            corrected_columns={"items": ["id", "quantity", "purchase_price", "category_id"]},
        ),
    )
    assert "purchase_price" in corrected[0].columns
