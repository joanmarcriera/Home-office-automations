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
                         [("docs/services/bad.md", 3, "scripts/ghost.py")])
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            self.assertEqual(cdsr.main(["--root", str(self.root)]), 1)
        self.assertIn("docs/services/bad.md:3: missing scripts/ghost.py", out.getvalue())

    def test_fenced_blocks_and_plain_text_are_ignored(self):
        self.write("fence.md", "```\npython3 `scripts/ghost.py`\n```\nplain scripts/ghost.py\n"
                               "`/opt/app/scripts/ghost.py`\n")
        self.assertEqual(cdsr.find_missing(self.root), [])


if __name__ == "__main__":
    unittest.main()
