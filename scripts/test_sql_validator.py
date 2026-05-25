import unittest
from sql_validator import validate_sql

class TestSQLValidator(unittest.TestCase):
    def setUp(self):
        self.allowlist = ["users", "orders", "products"]
        self.sensitive = ["ssn", "credit_card"]
        self.row_limit = 500

    def test_basic_select(self):
        sql = "SELECT * FROM users"
        # Since we have sensitive columns, SELECT * should be blocked
        success, result, error = validate_sql(sql, self.allowlist, self.sensitive, self.row_limit)
        self.assertFalse(success)
        self.assertIn("SELECT * is blocked", error)

    def test_basic_select_safe(self):
        sql = "SELECT name, age FROM users"
        success, result, error = validate_sql(sql, self.allowlist, self.sensitive, self.row_limit)
        self.assertTrue(success)
        self.assertIn("LIMIT 500", result)

    def test_mutation_block(self):
        sqls = [
            "DELETE FROM users",
            "DROP TABLE users",
            "UPDATE users SET name='hacker'",
            "INSERT INTO users (name) VALUES ('hacker')",
            "CREATE TABLE evil (id int)"
        ]
        for sql in sqls:
            success, result, error = validate_sql(sql, self.allowlist, self.sensitive, self.row_limit)
            self.assertFalse(success, f"Failed to block mutation: {sql}")
            self.assertIn("Mutation detected", error)

    def test_table_allowlist(self):
        sql = "SELECT * FROM secrets"
        # Blocked because 'secrets' is not in allowlist
        # Note: Even without sensitive columns, allowlist check happens first
        success, result, error = validate_sql(sql, ["users"], None, self.row_limit)
        self.assertFalse(success)
        self.assertIn("Access to table 'secrets' is not allowed", error)

    def test_sensitive_column(self):
        sql = "SELECT ssn FROM users"
        success, result, error = validate_sql(sql, self.allowlist, self.sensitive, self.row_limit)
        self.assertFalse(success)
        self.assertIn("sensitive column 'ssn' is blocked", error)

    def test_limit_enforcement(self):
        # Case 1: No limit provided
        sql = "SELECT name FROM users"
        success, result, error = validate_sql(sql, self.allowlist, None, 100)
        self.assertTrue(success)
        self.assertIn("LIMIT 100", result)

        # Case 2: High limit provided
        sql = "SELECT name FROM users LIMIT 10000"
        success, result, error = validate_sql(sql, self.allowlist, None, 100)
        self.assertTrue(success)
        self.assertIn("LIMIT 100", result)
        self.assertNotIn("10000", result)

        # Case 3: Acceptable limit provided
        sql = "SELECT name FROM users LIMIT 50"
        success, result, error = validate_sql(sql, self.allowlist, None, 100)
        self.assertTrue(success)
        self.assertIn("LIMIT 50", result)

if __name__ == "__main__":
    unittest.main()
