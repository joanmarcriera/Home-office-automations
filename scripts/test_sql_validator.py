import unittest
from scripts.sql_validator import enforce_sql_policy

class TestSqlValidator(unittest.TestCase):
    def test_row_limit_enforcement(self):
        # Case 1: No limit provided
        sql = "SELECT * FROM items"
        expected = "SELECT * FROM items LIMIT 1000"
        self.assertEqual(enforce_sql_policy(sql), expected)

        # Case 2: Limit provided within bounds
        sql = "SELECT * FROM items LIMIT 500"
        expected = "SELECT * FROM items LIMIT 500"
        self.assertEqual(enforce_sql_policy(sql), expected)

        # Case 3: Limit exceeds hard cap
        sql = "SELECT * FROM items LIMIT 5000"
        expected = "SELECT * FROM items LIMIT 1000"
        self.assertEqual(enforce_sql_policy(sql), expected)

    def test_table_allowlist(self):
        allowed = ["items", "categories"]

        # Case 1: Allowed table
        sql = "SELECT * FROM items"
        self.assertTrue("items" in enforce_sql_policy(sql, allowed_tables=allowed))

        # Case 2: Forbidden table
        sql = "SELECT * FROM users"
        with self.assertRaisesRegex(ValueError, "Table 'users' not in allowlist"):
            enforce_sql_policy(sql, allowed_tables=allowed)

    def test_mutation_blocking(self):
        # Case 1: DROP TABLE
        sql = "DROP TABLE items"
        with self.assertRaisesRegex(ValueError, "Mutation detected"):
            enforce_sql_policy(sql)

        # Case 2: DELETE
        sql = "DELETE FROM items WHERE id = 1"
        with self.assertRaisesRegex(ValueError, "Mutation detected"):
            enforce_sql_policy(sql)

        # Case 3: Mixed queries (Semicolon injection)
        sql = "SELECT * FROM items; DROP TABLE items"
        with self.assertRaisesRegex(ValueError, "Mutation detected"):
            enforce_sql_policy(sql)

    def test_pii_masking(self):
        sensitive = ["ssn", "password_hash"]

        # Case 1: Safe column
        sql = "SELECT name FROM items"
        self.assertTrue("name" in enforce_sql_policy(sql, sensitive_columns=sensitive))

        # Case 2: Sensitive column
        sql = "SELECT ssn FROM users"
        with self.assertRaisesRegex(ValueError, "Access to sensitive column 'ssn' is forbidden"):
            enforce_sql_policy(sql, sensitive_columns=sensitive)

if __name__ == "__main__":
    unittest.main()
