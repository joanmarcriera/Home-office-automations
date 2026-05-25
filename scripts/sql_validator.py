import sqlglot
from sqlglot import exp

def enforce_sql_policy(
    sql: str,
    allowed_tables: list[str] = None,
    default_limit: int = 1000,
    sensitive_columns: list[str] = None
) -> str:
    """
    Parses a SQL query and enforces safety policies:
    1. Ensures SELECT queries have a LIMIT clause.
    2. Blocks mutation keywords (DDL/DML).
    3. Validates against a table allowlist.
    4. Excludes sensitive columns from SELECT outputs.
    """
    try:
        # sqlglot.parse can return multiple expressions if separated by semicolons
        expressions = sqlglot.parse(sql)
        modified_queries = []

        for expression in expressions:
            # 1. Check for forbidden mutation keywords
            forbidden_nodes = (
                exp.Delete, exp.Drop, exp.Update, exp.Insert,
                exp.Alter, exp.TruncateTable, exp.Create, exp.Grant
            )
            if any(isinstance(node, forbidden_nodes) for node in expression.walk()):
                raise ValueError("Mutation detected: DDL/DML operations are forbidden.")

            # 2. Verify table allowlist
            if allowed_tables is not None:
                for table in expression.find_all(exp.Table):
                    if table.name.lower() not in [t.lower() for t in allowed_tables]:
                        raise ValueError(f"Table '{table.name}' not in allowlist.")

            # 3. Ensure LIMIT is present for SELECT statements
            if isinstance(expression, exp.Select):
                # 4. PII/PHI Masking: Check for sensitive columns in SELECT
                if sensitive_columns is not None:
                    for column in expression.find_all(exp.Column):
                        if column.name.lower() in [c.lower() for c in sensitive_columns]:
                            # If the column is in a SELECT clause (not just a JOIN or WHERE)
                            # This is a bit simplified; in a real scenario we might allow it in WHERE but not SELECT.
                            # For safety, we block it if it appears anywhere in a SELECT-style query for now.
                            raise ValueError(f"Access to sensitive column '{column.name}' is forbidden.")

                if not expression.find(exp.Limit):
                    print(f"Warning: No LIMIT clause found. Appending default limit {default_limit}.")
                    expression = expression.limit(default_limit)
                else:
                    # Optional: enforce a hard cap even if LIMIT is present
                    limit_node = expression.find(exp.Limit)
                    if limit_node and hasattr(limit_node.expression, 'this'):
                        try:
                            current_limit = int(limit_node.expression.this)
                            if current_limit > default_limit:
                                print(f"Warning: Limit {current_limit} exceeds max {default_limit}. Capping.")
                                expression.set("limit", exp.Limit(expression=exp.Literal.number(default_limit)))
                        except (ValueError, TypeError):
                            pass

            modified_queries.append(expression.sql())

        return "; ".join(modified_queries)

    except sqlglot.errors.ParseError as e:
        raise ValueError(f"Syntax Error: {e}")

if __name__ == "__main__":
    # Example usage
    test_sql = "SELECT * FROM items"
    try:
        safe_sql = enforce_sql_policy(test_sql, allowed_tables=["items", "categories"])
        print(f"Original: {test_sql}")
        print(f"Safe:     {safe_sql}")
    except Exception as e:
        print(f"Error: {e}")
