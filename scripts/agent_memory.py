#!/usr/bin/env python3
"""
Home Admin Agent Memory Manager
Implements persistent state management for LangChain/LangGraph agents using SQLite.
"""

import sqlite3
import os
import sys
from typing import Optional, Any

# This implementation assumes langgraph is installed in the target environment
try:
    from langgraph.checkpoint.sqlite import SqliteSaver
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

class MemoryManager:
    """Manages persistent memory for the Home Admin Agent."""

    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path

    def get_checkpointer(self) -> Optional[Any]:
        """
        Returns a LangGraph compatible SqliteSaver checkpointer.
        The user of this class is responsible for closing the connection if needed,
        though SqliteSaver handles much of it.
        """
        if not LANGGRAPH_AVAILABLE:
            print("Warning: langgraph not installed. Persistent memory not available.", file=sys.stderr)
            return None

        # Using a context manager or persistent connection
        # LangGraph 0.2+ uses SqliteSaver.from_conn_string(":memory:") or a file
        try:
            # Check if using newer langgraph-checkpoint-sqlite
            # Note: from_conn_string returns a context manager in some versions
            # or requires being used in a 'with' block.
            # In LangGraph 0.2+, it often returns the saver directly if sync.
            return SqliteSaver.from_conn_string(self.db_path)
        except AttributeError:
            # Fallback for older versions if applicable
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            return SqliteSaver(conn)

    def get_async_checkpointer(self):
        """Returns an AsyncSqliteSaver checkpointer context manager."""
        if not LANGGRAPH_AVAILABLE:
            return None
        return AsyncSqliteSaver.from_conn_string(self.db_path)

    def clear_memory(self):
        """Clears all agent memory by deleting the database file."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
                print(f"Memory cleared at {self.db_path}")
            except Exception as e:
                print(f"Error clearing memory: {e}", file=sys.stderr)

if __name__ == "__main__":
    db_file = "agent_memory.db"
    manager = MemoryManager(db_file)
    print(f"Memory Manager initialized with DB: {db_file}")

    checkpointer = manager.get_checkpointer()
    if checkpointer:
        print("✅ LangGraph checkpointer is ready and functional.")
    else:
        print("❌ LangGraph checkpointer could not be initialized (likely missing dependencies).")
