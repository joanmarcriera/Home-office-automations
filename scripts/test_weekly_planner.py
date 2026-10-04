"""Unit tests for the weekly planner's dedupe gate (no network: gh is mocked).

Run: python3 -m unittest discover -s scripts -p 'test_weekly_planner.py'
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import coverage_gap_scan  # noqa: E402
import weekly_planner as wp  # noqa: E402


def completed(stdout="", returncode=0, stderr=""):
    return subprocess.CompletedProcess(args=["gh"], returncode=returncode,
                                       stdout=stdout, stderr=stderr)


def bot(title):
    return {"title": title, "author": {"login": "app/github-actions", "is_bot": True}}


class FakeGh:
    """Answers `gh issue list` with a canned response and records creations."""

    def __init__(self, list_response):
        self.list_response, self.created, self.list_calls = list_response, [], []

    def __call__(self, cmd, **_kwargs):
        if cmd[:3] == ["gh", "issue", "list"]:
            self.list_calls.append(cmd)
            return self.list_response
        if cmd[:3] == ["gh", "issue", "create"]:
            self.created.append(cmd[cmd.index("--title") + 1])
            return completed("https://github.com/o/r/issues/1\n")
        raise AssertionError(f"unexpected command {cmd}")


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = os.getcwd()
        os.chdir(self.tmp.name)
        Path("data").mkdir()
        Path("data/growth-metrics.json").write_text(json.dumps({
            "shallow_docs": ["docs/a.md"], "underdeveloped_categories": ["agents"],
            "by_category": {"agents": 2},
        }))
        # No tool pages in the temp dir -> no cross-link issue either way.

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def run_main(self, fake):
        out = io.StringIO()
        with mock.patch.object(wp.subprocess, "run", fake), redirect_stdout(out):
            rc = wp.main()
        return rc, out.getvalue()

    def test_creates_when_lookup_succeeds_and_nothing_open(self):
        fake = FakeGh(completed("[]"))
        rc, _ = self.run_main(fake)
        self.assertEqual(rc, 0)
        self.assertEqual(len(fake.created), 2)

    def test_lookup_only_trusts_bot_author(self):
        fake = FakeGh(completed("[]"))
        self.run_main(fake)
        (cmd,) = fake.list_calls
        self.assertEqual(cmd[cmd.index("--author") + 1], "github-actions[bot]")

    def test_existing_bot_issues_suppress_duplicates(self):
        fake = FakeGh(completed(json.dumps([bot("Weekly deepening: x"),
                                            bot("Category gap fill: expand agents")])))
        rc, out = self.run_main(fake)
        self.assertEqual((rc, fake.created), (0, []))
        self.assertIn("already exists", out)

    def test_outsider_lookalike_issue_does_not_suppress(self):
        outsider = {"title": "Weekly deepening: spam", "author": {"login": "mallory"}}
        fake = FakeGh(completed(json.dumps([outsider])))
        rc, _ = self.run_main(fake)
        self.assertEqual(rc, 0)
        self.assertIn("Weekly deepening: add code examples to 1 docs", fake.created)

    def test_api_error_fails_closed(self):
        fake = FakeGh(completed(returncode=1, stderr="HTTP 502"))
        rc, out = self.run_main(fake)
        self.assertEqual((rc, fake.created), (wp.EXIT_LOOKUP_FAILED, []))
        self.assertIn("::warning::", out)

    def test_unparsable_output_fails_closed(self):
        fake = FakeGh(completed("<html>rate limited</html>"))
        rc, _ = self.run_main(fake)
        self.assertEqual((rc, fake.created), (wp.EXIT_LOOKUP_FAILED, []))

    def test_empty_output_fails_closed(self):
        fake = FakeGh(completed(""))
        rc, _ = self.run_main(fake)
        self.assertEqual((rc, fake.created), (wp.EXIT_LOOKUP_FAILED, []))

    def test_non_list_output_fails_closed(self):
        fake = FakeGh(completed('{"message": "error"}'))
        rc, _ = self.run_main(fake)
        self.assertEqual((rc, fake.created), (wp.EXIT_LOOKUP_FAILED, []))

    def test_malformed_record_fails_closed(self):
        fake = FakeGh(completed('[{"number": 1}]'))
        rc, _ = self.run_main(fake)
        self.assertEqual((rc, fake.created), (wp.EXIT_LOOKUP_FAILED, []))

    def test_possibly_truncated_result_fails_closed(self):
        many = [bot(f"Other {i}") for i in range(wp.LOOKUP_LIMIT)]
        fake = FakeGh(completed(json.dumps(many)))
        rc, _ = self.run_main(fake)
        self.assertEqual((rc, fake.created), (wp.EXIT_LOOKUP_FAILED, []))


class CoverageGapThrottleTests(unittest.TestCase):
    FRONTIER = [{"name": "tool"}]

    def call(self, response):
        fake = FakeGh(response)
        out = io.StringIO()
        with mock.patch.object(coverage_gap_scan.subprocess, "run", fake), redirect_stdout(out):
            made = coverage_gap_scan.create_issue("report", self.FRONTIER)
        return made, fake

    def test_lookup_error_fails_closed(self):
        made, fake = self.call(completed(returncode=1, stderr="boom"))
        self.assertEqual((made, fake.created), (None, []))

    def test_unparsable_fails_closed(self):
        made, fake = self.call(completed("not json"))
        self.assertEqual((made, fake.created), (None, []))

    def test_lookup_is_bot_author_only(self):
        made, fake = self.call(completed("[]"))
        self.assertTrue(made)
        (cmd,) = fake.list_calls
        self.assertEqual(cmd[cmd.index("--author") + 1], "github-actions[bot]")

    def test_existing_issue_throttles(self):
        made, fake = self.call(completed(json.dumps([{"title": "Coverage gap fill: x"}])))
        self.assertEqual((made, fake.created), (False, []))


if __name__ == "__main__":
    unittest.main()
