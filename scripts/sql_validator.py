import sys
import sqlglot
from sqlglot import exp, parse_one

def validate_sql(sql, allowlist_tables=None, sensitive_columns=None, row_limit=1000):
    """
    Validates a SQL query against security and governance guardrails.
    Returns (is_valid, modified_sql, error_message)
    """
    try:
        # 1. Parse the SQL
        expression = parse_one(sql)

        # 2. Block Mutations (Detection of DROP, DELETE, etc.)
        forbidden_types = (exp.Delete, exp.Drop, exp.Update, exp.Insert, exp.Alter, exp.Create, exp.TruncateTable)
        # Check if the root expression or any sub-expression is a mutation
        if any(expression.find(t) for t in forbidden_types) or not isinstance(expression, (exp.Select, exp.Union)):
             return False, None, "Mutation detected. Only SELECT queries are allowed."

        # 3. Table Allowlist Validation
        if allowlist_tables:
            tables = [t.name.lower() for t in expression.find_all(exp.Table)]
            for table in tables:
                if table not in [a.lower() for a in allowlist_tables]:
                    return False, None, f"Access to table '{table}' is not allowed."

        # 4. PII/PHI Masking (Sensitive Column Exclusion)
        if sensitive_columns:
            # We check if any sensitive columns are explicitly selected
            projections = expression.find_all(exp.Column)
            for col in projections:
                if col.name.lower() in [s.lower() for s in sensitive_columns]:
                    return False, None, f"Access to sensitive column '{col.name}' is blocked."

            # Block SELECT * if sensitive columns are defined for any table in the query
            # (In a more advanced version, we'd check if the * expands to sensitive columns)
            if any(isinstance(s, exp.Star) for s in expression.find_all(exp.Star)):
                return False, None, "SELECT * is blocked when sensitive columns are present in the environment. Please specify columns explicitly."

        # 5. Row Limit Enforcement
        # Check if LIMIT exists, if not, add it. If it exists and is higher than row_limit, reduce it.
        limit_clause = expression.find(exp.Limit)
        if limit_clause:
            try:
                current_limit = int(limit_clause.expression.this)
                if current_limit > row_limit:
                    limit_clause.set("expression", exp.Literal.number(row_limit))
            except (ValueError, TypeError):
                # If limit is not a simple integer, overwrite it for safety
                limit_clause.set("expression", exp.Literal.number(row_limit))
        else:
            expression = expression.limit(row_limit)

        return True, expression.sql(), None

    except sqlglot.errors.SqlglotError as e:
        return False, None, f"SQL Parsing Error: {str(e)}"
    except Exception as e:
        return False, None, f"Internal Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sql_validator.py \"<sql_query>\"")
        sys.exit(1)

    query = sys.argv[1]
    # Default example config
    allowed = ["users", "orders", "products", "inventory"]
    sensitive = ["email", "password", "ssn", "phone", "credit_card"]

    success, result, error = validate_sql(query, allowlist_tables=allowed, sensitive_columns=sensitive)

    if success:
        print(f"VALIDATED_SQL: {result}")
    else:
        print(f"ERROR: {error}")
        sys.exit(1)
