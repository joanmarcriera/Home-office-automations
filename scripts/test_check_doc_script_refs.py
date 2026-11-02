"""Unit tests for scripts/check_doc_script_refs.py (synthetic temp tree, no network).

Run: python3 -m unittest discover -s scripts -p 'test_check_doc_script_refs.py'
"""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_doc_script_refs as cdsr  # noqa: E402


class FindMissingTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "real.py").write_text("print('hi')\n")
        (self.root / "docs" / "services").mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, text):
        (self.root / "docs" / "services" / name).write_text(text, encoding="utf-8")

    def test_existing_reference_is_clean(self):
        self.write("good.md", "Run `python3 scripts/real.py --check` nightly.\n")
        self.assertEqual(cdsr.find_missing(self.root), [])
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(cdsr.main(["--root", str(self.root)]), 0)

    def test_missing_reference_is_reported_with_line(self):
        self.write("bad.md", "# Title\n\nSee `scripts/ghost.py` and `scripts/real.py`.\n")
        self.assertEqual(cdsr.find_missing(self.root),
                         [("docs/services/bad.md", 3, "scripts/ghost.py", "inline")])
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            self.assertEqual(cdsr.main(["--root", str(self.root)]), 1)
        self.assertIn("docs/services/bad.md:3: missing scripts/ghost.py", out.getvalue())

    def test_fenced_blocks_and_plain_text_are_ignored(self):
        self.write("fence.md", "```\npython3 `scripts/ghost.py`\n```\nplain scripts/ghost.py\n"
                               "`/opt/app/scripts/ghost.py`\n")
        self.assertEqual(cdsr.find_missing(self.root), [])


class ExtendedScanTests(unittest.TestCase):
    """Recursive docs/** scan, `-m scripts.<module>` forms, code-block class, allowlist."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "scripts" / "pkg").mkdir(parents=True)
        (self.root / "scripts" / "real.py").write_text("print('hi')\n")
        (self.root / "scripts" / "pkg" / "mod.py").write_text("")
        (self.root / "docs" / "services").mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        path = self.root / "docs" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cdsr.main(["--root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_default_scans_docs_recursively(self):
        self.write("tools/agents/deep.md", "Run `scripts/ghost.py`.\n")
        self.write("top.md", "Run `scripts/ghost2.py`.\n")
        self.assertEqual(cdsr.find_missing(self.root), [
            ("docs/tools/agents/deep.md", 1, "scripts/ghost.py", "inline"),
            ("docs/top.md", 1, "scripts/ghost2.py", "inline"),
        ])

    def test_docs_dir_option_limits_scan(self):
        self.write("tools/deep.md", "Run `scripts/ghost.py`.\n")
        self.write("services/svc.md", "Run `scripts/ghost3.py`.\n")
        self.assertEqual(cdsr.find_missing(self.root, "docs/services"),
                         [("docs/services/svc.md", 1, "scripts/ghost3.py", "inline")])
        code, out, _ = self.run_main("--docs-dir", "docs/services")
        self.assertEqual(code, 1)
        self.assertNotIn("tools/deep.md", out)

    def test_dotted_module_inline_is_resolved(self):
        self.write("a.md", "Use `python3 -m scripts.real` or `python -m scripts.pkg.mod --x`.\n"
                           "Not `python3 -m scripts.nope`.\n")
        self.assertEqual(cdsr.find_missing(self.root),
                         [("docs/a.md", 2, "scripts.nope", "inline")])

    def test_dotted_module_in_fence_is_code_block_class(self):
        self.write("b.md", "```bash\npython3 -m scripts.rotate_engines --dry-run\n"
                           "python3 -m scripts.real\nExecStart=/usr/bin/python3 -m scripts.pkg.mod\n"
                           "```\n")
        self.assertEqual(cdsr.find_missing(self.root),
                         [("docs/b.md", 2, "scripts.rotate_engines", "code-block")])
        code, out, _ = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("docs/b.md:2: missing scripts.rotate_engines (code-block)", out)

    def test_tilde_fence_and_unrelated_modules_are_handled(self):
        self.write("c.md", "~~~\npython3 -m scripts.ghost_mod\n~~~\n"
                           "```\npython3 -m myapp.scripts.thing\npython3 -m scriptsx.y\n```\n")
        self.assertEqual(cdsr.find_missing(self.root),
                         [("docs/c.md", 2, "scripts.ghost_mod", "code-block")])

    def test_package_directory_module_resolves(self):
        (self.root / "scripts" / "tool").mkdir()
        (self.root / "scripts" / "tool" / "__main__.py").write_text("")
        self.write("d.md", "`python3 -m scripts.tool`\n")
        self.assertEqual(cdsr.find_missing(self.root), [])

    def test_allowlist_suppresses_intentional_examples(self):
        self.write("e.md", "```\npython3 -m scripts.sketch_only\n```\nSee `scripts/ghost.py`.\n")
        allow = self.root / "allow.txt"
        allow.write_text("# comment\n\ndocs/e.md scripts.sketch_only  # design sketch\n")
        self.assertEqual(cdsr.find_missing(self.root, allowlist=cdsr.load_allowlist(allow)),
                         [("docs/e.md", 4, "scripts/ghost.py", "inline")])
        code, out, _ = self.run_main("--allowlist", str(allow))
        self.assertEqual(code, 1)
        self.assertNotIn("sketch_only", out)

    def test_default_allowlist_is_read_from_root(self):
        self.write("f.md", "```\npython3 -m scripts.sketch_only\n```\n")
        (self.root / "scripts" / "doc_script_refs_allowlist.txt").write_text(
            "docs/f.md scripts.sketch_only\n")
        self.assertEqual(self.run_main()[0], 0)

    def test_stale_allowlist_entry_is_warned(self):
        self.write("g.md", "nothing here\n")
        allow = self.root / "allow.txt"
        allow.write_text("docs/g.md scripts.gone\n")
        code, _, err = self.run_main("--allowlist", str(allow))
        self.assertEqual(code, 0)
        self.assertIn("stale allowlist entry: docs/g.md scripts.gone", err)

    def test_malformed_allowlist_line_raises(self):
        allow = self.root / "allow.txt"
        allow.write_text("just-one-field\n")
        with self.assertRaises(ValueError):
            cdsr.load_allowlist(allow)


if __name__ == "__main__":
    unittest.main()
