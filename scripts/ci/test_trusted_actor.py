"""Unit tests for scripts/ci/trusted_actor.py (offline: gh is faked).

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
from unittest import mock

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


def issue(number, author, title="Daily Knowledge Expansion - 2026-10-04"):
    return {"number": number, "title": title, "author": author}


class FakeGh:
    """Plays GitHub: holds ALL records and answers `gh <x> list --author A
    --limit N` server-side like the real API (author filter, then page cut)."""

    def __init__(self, records, fail_for=None, raw=None):
        self.records, self.fail_for, self.raw, self.calls = records, fail_for, raw, []

    @staticmethod
    def _login_matches(author, wanted):
        login = author.get("login", "")
        if wanted.endswith("[bot]"):
            return login in (wanted, "app/" + wanted[:-5])
        return login == wanted and not author.get("is_bot")

    def __call__(self, cmd, **_kw):
        self.calls.append(cmd)
        wanted = cmd[cmd.index("--author") + 1]
        limit = int(cmd[cmd.index("--limit") + 1])
        if wanted == self.fail_for:
            return subprocess.CompletedProcess(cmd, 1, "", "HTTP 502: Bad Gateway")
        if self.raw is not None:
            return subprocess.CompletedProcess(cmd, 0, self.raw, "")
        page = [r for r in self.records if self._login_matches(r["author"], wanted)][:limit]
        return subprocess.CompletedProcess(cmd, 0, json.dumps(page), "")


def run_cli(args, stdin=""):
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

    def test_search_logins_use_bot_suffix_form(self):
        # `app/<slug>` silently matches nothing in `gh issue list --author`.
        self.assertEqual(ta.trusted_search_logins("joanmarcriera"),
                         ["joanmarcriera", "github-actions[bot]", "google-labs-jules[bot]"])


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

    def test_cross_repository_must_be_strictly_false(self):
        item = pr(1)
        item["isCrossRepository"] = None
        self.assertEqual(self.kept([item]), [])

    def test_many_untrusted_items_are_simply_dropped(self):
        items = [issue(n, OUTSIDER) for n in range(1, 5001)] + [issue(9999, ACTIONS)]
        self.assertEqual(self.kept(items, kind="issues"), [9999])

    def test_malformed_input_raises(self):
        for items, kind, kw in (([{"number": 1, "author": OWNER}], "prs", {}),
                                ([{"number": 1, "author": OWNER, "isCrossRepository": False}],
                                 "prs", {"bot_heuristic": True}),
                                ([{"number": 1}], "issues", {}),
                                ({"not": "a list"}, "issues", {}),
                                (["str"], "issues", {})):
            with self.subTest(items=items), self.assertRaises(ta.InputError):
                ta.filter_items(items, kind, "o", **kw)


class ListTrustedTests(unittest.TestCase):
    def test_queries_only_trusted_authors_server_side(self):
        gh = FakeGh([issue(1, ACTIONS), issue(2, OUTSIDER)])
        got = ta.list_trusted("issues", REPO, fields=["title"], label="jules",
                              search="Daily Knowledge Expansion -", runner=gh)
        self.assertEqual([i["number"] for i in got], [1])
        self.assertEqual([c[c.index("--author") + 1] for c in gh.calls],
                         ["joanmarcriera", "github-actions[bot]", "google-labs-jules[bot]"])
        for c in gh.calls:
            self.assertIn("--label", c)
            self.assertIn("--search", c)
            self.assertIn("number,author,title", c)

    def test_outsider_flood_cannot_hide_trusted_item_or_trip_failure(self):
        # 5000 look-alikes (more than any page) must neither push the genuine
        # control issue out of the window nor make the lookup fail.
        flood = [issue(n, OUTSIDER) for n in range(10, 5010)]
        gh = FakeGh(flood + [issue(3, ACTIONS)])
        got = ta.list_trusted("issues", REPO, runner=gh, limit=100)
        self.assertEqual([i["number"] for i in got], [3])

    def test_fork_prs_by_trusted_login_still_dropped(self):
        gh = FakeGh([pr(1), pr(2, cross=True), pr(3, author=OUTSIDER)])
        got = ta.list_trusted("prs", REPO, bot_heuristic=True, runner=gh)
        self.assertEqual([p["number"] for p in got], [1])

    def test_merges_and_sorts_newest_first(self):
        gh = FakeGh([pr(5), pr(7, author=ACTIONS), pr(6)])
        got = ta.list_trusted("prs", REPO, runner=gh)
        self.assertEqual([p["number"] for p in got], [7, 6, 5])

    def test_trusted_page_full_is_an_error_unless_allowed(self):
        gh = FakeGh([issue(n, ACTIONS) for n in range(1, 4)])
        with self.assertRaises(ta.InputError):
            ta.list_trusted("issues", REPO, runner=gh, limit=3)
        got = ta.list_trusted("issues", REPO, runner=gh, limit=3, allow_truncated=True)
        self.assertEqual(len(got), 3)

    def test_lookup_error_raises(self):
        with self.assertRaises(ta.InputError):
            ta.list_trusted("issues", REPO, runner=FakeGh([], fail_for="github-actions[bot]"))
        for raw in ("", "not json", '{"a": 1}', '[{"title": "no number"}]'):
            with self.subTest(raw=raw), self.assertRaises(ta.InputError):
                ta.list_trusted("issues", REPO, runner=FakeGh([], raw=raw))

    def test_missing_repo_raises(self):
        with self.assertRaises(ta.InputError):
            ta.list_trusted("issues", None, runner=FakeGh([]))


class CliTests(unittest.TestCase):
    def test_list_emits_json(self):
        gh = FakeGh([issue(1, ACTIONS), issue(2, OUTSIDER)])
        with mock.patch.object(ta.subprocess, "run", gh):
            code, out, _ = run_cli(["list", "issues", "--fields", "title"])
        self.assertEqual((code, [i["number"] for i in json.loads(out)]), (0, [1]))

    def test_list_lookup_error_exits_2(self):
        with mock.patch.object(ta.subprocess, "run", FakeGh([], fail_for="joanmarcriera")):
            code, out, err = run_cli(["list", "prs", "--bot-heuristic"])
        self.assertEqual((code, out), (2, ""))
        self.assertIn("::error::", err)

    def test_filter_mode(self):
        code, out, err = run_cli(["filter", "prs", "--bot-heuristic"],
                                 json.dumps([pr(1), pr(2, author=OUTSIDER), pr(3, cross=True)]))
        self.assertEqual(code, 0)
        self.assertEqual([i["number"] for i in json.loads(out)], [1])
        self.assertIn("#2", err)
        self.assertIn("#3", err)

    def test_filter_fail_safe_on_bad_input(self):
        for stdin in ("", "   \n", "not json", '{"a": 1}', '[{"number": 1}]'):
            with self.subTest(stdin=stdin):
                code, out, err = run_cli(["filter", "issues"], stdin)
                self.assertEqual((code, out), (2, ""))
                self.assertIn("::error::", err)

    def test_pipefail_propagates_in_bash(self):
        # Workflows rely on `set -euo pipefail`: a failing lookup must fail the
        # whole `trusted_actor.py ... | jq` pipeline.
        script = (f"set -euo pipefail; echo garbage | {sys.executable} "
                  f"{HERE / 'trusted_actor.py'} filter issues --repo {REPO} | jq length")
        res = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("::error::", res.stderr)


if __name__ == "__main__":
    unittest.main()
