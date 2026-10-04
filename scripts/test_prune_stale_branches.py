"""Unit tests for scripts/prune_stale_branches.py (no network: gh is mocked).

Run: python3 -m unittest discover -s scripts -p 'test_prune_stale_branches.py'
"""

from __future__ import annotations

import io
import json
import os
import re
import sys
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prune_stale_branches as psb  # noqa: E402

REPO = "owner/repo"
OLD = "2026-01-01T00:00:00Z"
CUTOFF = datetime(2026, 6, 1, tzinfo=timezone.utc)
KEEP = [re.compile(p) for p in psb.ALWAYS_KEEP]


def ref(name, oid="a" * 40, date=OLD, behind=3, prs=()):
    return {
        "name": name,
        "branchProtectionRule": None,
        "target": {"oid": oid, "committedDate": date},
        "compare": {"behindBy": behind},
        "associatedPullRequests": {"nodes": list(prs)},
    }


def pr(number, state, head_ref, oid="a" * 40, head_repo=REPO):
    return {"number": number, "state": state, "headRefName": head_ref, "headRefOid": oid,
            "headRepository": {"nameWithOwner": head_repo} if head_repo else None}


def classify(r, open_refs=frozenset()):
    return psb.classify(r, "main", KEEP, set(open_refs), CUTOFF, REPO)


class ClassifyTests(unittest.TestCase):
    def test_merged_branch_is_deletable(self):
        self.assertEqual(classify(ref("jules-1", behind=0))[0], "delete")

    def test_protected_names_never_deleted_even_if_merged(self):
        for name in ("main", "gh-pages", "automation/weekly-rollup"):
            self.assertEqual(classify(ref(name, behind=0))[0], "keep", name)

    def test_recent_tip_kept(self):
        recent = (datetime.now(timezone.utc)).isoformat().replace("+00:00", "Z")
        self.assertEqual(psb.classify(ref("x", behind=0, date=recent), "main", KEEP, set(),
                                      datetime.now(timezone.utc) - timedelta(days=3), REPO),
                         ("keep", "tip too recent"))

    def test_open_pr_ref_kept(self):
        self.assertEqual(classify(ref("x", behind=0), open_refs={"x"})[0], "keep")

    def test_own_closed_pr_with_unchanged_tip_deletable(self):
        r = ref("feat", prs=[pr(7, "CLOSED", "feat")])
        self.assertEqual(classify(r)[0], "delete")

    def test_own_closed_pr_but_new_commits_kept(self):
        r = ref("feat", oid="b" * 40, prs=[pr(7, "CLOSED", "feat", oid="a" * 40)])
        self.assertEqual(classify(r)[0], "keep")

    def test_fork_closed_pr_with_same_name_and_oid_does_not_make_branch_closed(self):
        r = ref("feat", prs=[pr(9, "CLOSED", "feat", head_repo="evil/fork")])
        self.assertEqual(classify(r), ("keep", "unmerged commits without a closed PR"))

    def test_deleted_fork_head_repo_does_not_count(self):
        r = ref("feat", prs=[pr(9, "MERGED", "feat", head_repo=None)])
        self.assertEqual(classify(r)[0], "keep")

    def test_pr_with_other_head_name_does_not_count(self):
        r = ref("feat", prs=[pr(9, "CLOSED", "other-name")])
        self.assertEqual(classify(r)[0], "keep")

    def test_own_open_pr_in_associated_prs_keeps(self):
        r = ref("feat", behind=0, prs=[pr(9, "OPEN", "feat")])
        self.assertEqual(classify(r), ("keep", "open PR"))

    def test_fork_open_pr_does_not_protect_merged_branch(self):
        r = ref("feat", behind=0, prs=[pr(9, "OPEN", "feat", head_repo="evil/fork")])
        self.assertEqual(classify(r)[0], "delete")


class OpenPrRefsTests(unittest.TestCase):
    def test_fork_head_not_protected_but_base_is(self):
        prs = [{"headRefName": "main-ish", "baseRefName": "release",
                "headRepository": {"nameWithOwner": "evil/fork"}}]
        self.assertEqual(psb.open_pr_refs(prs, REPO), {"release"})

    def test_same_repo_head_and_base_protected(self):
        prs = [{"headRefName": "feat", "baseRefName": "main",
                "headRepository": {"nameWithOwner": REPO}}]
        self.assertEqual(psb.open_pr_refs(prs, REPO), {"feat", "main"})


class FakeGh:
    """Records gh calls and answers the queries prune_stale_branches makes."""

    def __init__(self, refs, open_prs_scan=(), open_prs_recheck=None, fail_delete=()):
        self.refs, self.calls, self.fail_delete = refs, [], set(fail_delete)
        self.open_sequence = [list(open_prs_scan),
                              list(open_prs_scan if open_prs_recheck is None else open_prs_recheck)]

    def __call__(self, args):
        self.calls.append(args)
        if args[:2] == ["api", f"repos/{REPO}"]:
            return json.dumps({"default_branch": "main", "node_id": "R_1"})
        query = next(a for a in args if a.startswith("query="))
        if "updateRefs" in query:
            ref_name = next(a for a in args if a.startswith("ref=")).split("=", 1)[1]
            if ref_name.removeprefix("refs/heads/") in self.fail_delete:
                raise RuntimeError("stale beforeOid")
            return json.dumps({"data": {"updateRefs": {"clientMutationId": None}}})
        page = {"pageInfo": {"hasNextPage": False, "endCursor": None}}
        if "pullRequests(states: OPEN" in query:
            nodes = self.open_sequence.pop(0) if len(self.open_sequence) > 1 else self.open_sequence[0]
            return json.dumps({"data": {"repository": {"pullRequests": {**page, "nodes": nodes}}}})
        return json.dumps({"data": {"repository": {"refs": {**page, "nodes": self.refs}}}})

    def mutations(self):
        return [a for a in self.calls if any("updateRefs" in x for x in a)]


def run_main(fake, *argv):
    out = io.StringIO()
    with mock.patch.object(psb, "gh", fake), mock.patch.object(sys, "argv", ["prog", *argv]), \
            mock.patch.dict(os.environ, {"REPO": REPO}, clear=False), redirect_stdout(out):
        os.environ.pop("GITHUB_STEP_SUMMARY", None)
        psb.main()
    return out.getvalue()


class MainTests(unittest.TestCase):
    def refs(self, n):
        return [ref(f"jules-{i}", oid=f"{i:040d}", behind=0) for i in range(n)]

    def test_dry_run_is_default_and_never_mutates(self):
        fake = FakeGh(self.refs(5))
        out = run_main(fake)
        self.assertEqual(fake.mutations(), [])
        self.assertIn("DRY RUN", out)
        self.assertIn("candidates=5 deleted=0", out)

    def test_cap_limits_deletions(self):
        fake = FakeGh(self.refs(10))
        run_main(fake, "--apply", "--max-deletions", "3")
        self.assertEqual(len(fake.mutations()), 3)

    def test_delete_is_compare_and_swap_on_evaluated_oid(self):
        fake = FakeGh(self.refs(1))
        run_main(fake, "--apply")
        (call,) = fake.mutations()
        self.assertIn(f"before={0:040d}", call)
        self.assertIn("ref=refs/heads/jules-0", call)
        self.assertIn("repo=R_1", call)
        query = next(a for a in call if a.startswith("query="))
        self.assertIn("force: false", query)
        self.assertIn("beforeOid: $before", query)

    def test_branch_that_gains_open_pr_before_delete_is_skipped(self):
        recheck = [{"headRefName": "jules-0", "baseRefName": "main",
                    "headRepository": {"nameWithOwner": REPO}}]
        fake = FakeGh(self.refs(2), open_prs_recheck=recheck)
        out = run_main(fake, "--apply")
        self.assertEqual(len(fake.mutations()), 1)
        self.assertIn("skipped jules-0", out)

    def test_cas_rejection_is_reported_not_fatal(self):
        fake = FakeGh(self.refs(2), fail_delete={"jules-0"})
        out = run_main(fake, "--apply")
        self.assertIn("not deleted jules-0", out)
        self.assertIn("deleted=1 failed=1", out)


if __name__ == "__main__":
    unittest.main()
