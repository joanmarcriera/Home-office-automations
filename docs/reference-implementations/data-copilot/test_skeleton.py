import pytest
import asyncio
from skeleton import DataCopilotPipeline, WorkspaceContext, IntentOutput

@pytest.mark.asyncio
async def test_pipeline_flow():
    pipeline = DataCopilotPipeline()
    query = "Test query"

    # 1. Router
    workspace = await pipeline.workspace_router(query)
    assert isinstance(workspace, WorkspaceContext)
    assert workspace.workspace_id == "inventory"

    # 2. Intent
    intent = await pipeline.intent_agent(query, workspace)
    assert isinstance(intent, IntentOutput)
    assert "quantity" in intent.metrics

    # 3. Tables
    tables = await pipeline.table_agent(intent)
    assert "items" in tables.selected_tables

    # 4. Prune
    pruned = await pipeline.column_prune_agent(tables.selected_tables, intent)
    assert len(pruned) > 0
    assert pruned[0].table_name == "items"

    # 5. SQL
    sql = await pipeline.sql_generator(intent, pruned)
    assert "SELECT" in sql

if __name__ == "__main__":
    asyncio.run(test_pipeline_flow())
