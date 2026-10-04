"""Unit tests for scripts/ci/trusted_actor.py (offline; no gh calls).

Run: python3 -m unittest discover -s scripts/ci -p 'test_trusted_actor.py' -v
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import trusted_actor as ta  # noqa: E402

REPO = "joanmarcriera/Home-office-automations"
OWNER = {"login": "joanmarcriera", "is_bot": False}
ACTIONS = {"login": "app/github-actions", "is_bot": True}
OUTSIDER = {"login": "mallory", "is_bot": False}


def pr(number, *, author=OWNER, cross=False, title="docs: daily knowledge expansion",
       branch="docs/daily-knowledge-expansion-x", body="", labels=()):
    return {"number": number, "title": title, "body": body, "headRefName": branch,
            "labels": [{"name": n} for n in labels], "author": author,
            "isCrossRepository": cross}


def run_cli(args, stdin):
    out, err = io.StringIO(), io.StringIO()
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = ta.main(args + ["--repo", REPO])
    finally:
        sys.stdin = old_stdin
    return code, out.getvalue(), err.getvalue()


class TrustedAuthorTests(unittest.TestCase):
    def test_owner_is_trusted_case_insensitively(self):
        self.assertTrue(ta.is_trusted_author({"login": "JoanMarcRiera"}, "joanmarcriera"))

    def test_bot_forms_gh_rest_graphql(self):
        for author in ({"login": "app/github-actions", "is_bot": True},
                       {"login": "github-actions[bot]"},
                       {"login": "github-actions", "is_bot": True},
                       {"login": "app/google-labs-jules", "is_bot": True},
                       {"login": "google-labs-jules[bot]"}):
            with self.subTest(author=author):
                self.assertTrue(ta.is_trusted_author(author, "joanmarcriera"))

    def test_user_impersonating_bot_name_is_not_trusted(self):
        self.assertFalse(ta.is_trusted_author({"login": "github-actions", "is_bot": False},
                                              "joanmarcriera"))
        self.assertFalse(ta.is_trusted_author({"login": "google-labs-jules"}, "joanmarcriera"))

    def test_bot_named_like_owner_is_not_trusted(self):
        self.assertFalse(ta.is_trusted_author({"login": "app/joanmarcriera", "is_bot": True},
                                              "joanmarcriera"))

    def test_unknown_bot_outsider_and_ghost(self):
        self.assertFalse(ta.is_trusted_author({"login": "app/dependabot", "is_bot": True},
                                              "joanmarcriera"))
        self.assertFalse(ta.is_trusted_author(OUTSIDER, "joanmarcriera"))
        self.assertFalse(ta.is_trusted_author(None, "joanmarcriera"))


class FilterTests(unittest.TestCase):
    def kept(self, items, kind="prs", **kw):
        return [i["number"] for i in ta.filter_items(items, kind, "joanmarcriera", **kw)]

    def test_lookalike_from_outsider_or_fork_is_dropped(self):
        items = [pr(1), pr(2, author=OUTSIDER), pr(3, cross=True),
                 pr(4, author=ACTIONS), pr(5, author=OWNER, cross=True)]
        self.assertEqual(self.kept(items, bot_heuristic=True), [1, 4])

    def test_bot_heuristic_ignores_ordinary_owner_prs(self):
        items = [pr(1, title="ci: harden things", branch="ci/harden"),
                 pr(2, title="x", branch="jules-sprint-3"),
                 pr(3, title="x", branch="y", labels=["jules"]),
                 pr(4, title="x", branch="y", body="PR created automatically by Jules"),
                 pr(5, title="Weekly cross-link fix", branch="y")]
        self.assertEqual(self.kept(items, bot_heuristic=True), [2, 3, 4, 5])

    def test_jules_app_author_counts_as_bot_pr(self):
        jules = {"login": "app/google-labs-jules", "is_bot": True}
        self.assertEqual(self.kept([pr(9, author=jules, title="x", branch="y")],
                                   bot_heuristic=True), [9])

    def test_exclude_rollup(self):
        items = [pr(1, branch="automation/weekly-rollup", title="weekly rollup"), pr(2)]
        self.assertEqual(self.kept(items, bot_heuristic=True, exclude_rollup=True), [2])
        self.assertEqual(self.kept(items, bot_heuristic=True), [1, 2])

    def test_prs_without_heuristic_only_check_identity(self):
        items = [pr(1, title="anything", branch="automation/weekly-rollup"),
                 pr(2, author=OUTSIDER, branch="automation/weekly-rollup")]
        self.assertEqual(self.kept(items), [1])

    def test_cross_repository_must_be_strictly_false(self):
        item = pr(1)
        item["isCrossRepository"] = None
        self.assertEqual(self.kept([item]), [])

    def test_issues(self):
        items = [{"number": 1, "title": "Daily Knowledge Expansion - x", "author": ACTIONS},
                 {"number": 2, "title": "Daily Knowledge Expansion - x", "author": OUTSIDER},
                 {"number": 3, "title": "t", "author": OWNER}]
        self.assertEqual(self.kept(items, kind="issues"), [1, 3])

    def test_missing_fields_raise(self):
        with self.assertRaises(ta.InputError):
            ta.filter_items([{"number": 1, "author": OWNER}], "prs", "o")
        with self.assertRaises(ta.InputError):
            ta.filter_items([{"number": 1, "author": OWNER, "isCrossRepository": False}],
                            "prs", "o", bot_heuristic=True)
        with self.assertRaises(ta.InputError):
            ta.filter_items([{"number": 1}], "issues", "o")
        with self.assertRaises(ta.InputError):
            ta.filter_items({"not": "a list"}, "issues", "o")
        with self.assertRaises(ta.InputError):
            ta.filter_items(["str"], "issues", "o")


class CliTests(unittest.TestCase):
    def test_filters_and_emits_json(self):
        code, out, err = run_cli(["prs", "--bot-heuristic"],
                                 json.dumps([pr(1), pr(2, author=OUTSIDER), pr(3, cross=True)]))
        self.assertEqual(code, 0)
        self.assertEqual([i["number"] for i in json.loads(out)], [1])
        self.assertIn("::notice::", err)
        self.assertIn("#2", err)
        self.assertIn("#3", err)

    def test_empty_array_is_fine(self):
        code, out, _ = run_cli(["issues"], "[]")
        self.assertEqual((code, json.loads(out)), (0, []))

    def test_fail_safe_on_bad_input(self):
        for stdin in ("", "   \n", "not json", '{"a": 1}', '[{"number": 1}]'):
            with self.subTest(stdin=stdin):
                code, out, err = run_cli(["issues"], stdin)
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertIn("::error::", err)

    def test_missing_repo_is_an_error(self):
        out, err = io.StringIO(), io.StringIO()
        sys.stdin, old = io.StringIO("[]"), sys.stdin
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = ta.main(["issues", "--repo", ""])
        finally:
            sys.stdin = old
        self.assertEqual(code, 2)
        self.assertIn("repository unknown", err.getvalue())

    def test_pipefail_propagates_in_bash(self):
        # The workflows rely on `set -o pipefail`: a failing filter must fail
        # the whole `gh ... | trusted_actor.py ... | jq` pipeline.
        script = (f"set -euo pipefail; echo garbage | {sys.executable} "
                  f"{HERE / 'trusted_actor.py'} issues --repo {REPO} | jq length")
        res = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("::error::", res.stderr)


if __name__ == "__main__":
    unittest.main()
