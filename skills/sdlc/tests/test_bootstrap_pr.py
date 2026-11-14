"""End-to-end tests for the Bootstrap PR workflow using local Git and a fake gh."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_pr.py"
spec = importlib.util.spec_from_file_location("sdlc_bootstrap_pr", SCRIPT)
assert spec is not None and spec.loader is not None
bootstrap_pr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap_pr)


def execute(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(
        args, cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


class BootstrapPullRequestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.origin = root / "origin.git"
        self.project = root / "project"
        self.bin = root / "bin"
        self.log = root / "gh.log"
        self.project.mkdir()
        self.bin.mkdir()

        execute("git", "init", "--bare", str(self.origin))
        execute("git", "init", "-b", "main", str(self.project))
        execute("git", "config", "user.name", "Test Developer", cwd=self.project)
        execute("git", "config", "user.email", "dev@example.invalid", cwd=self.project)
        (self.project / "README.md").write_text("Project\n", encoding="utf-8")
        execute("git", "add", "README.md", cwd=self.project)
        execute("git", "commit", "-m", "initial", cwd=self.project)
        execute("git", "remote", "add", "origin", str(self.origin), cwd=self.project)
        execute("git", "push", "-u", "origin", "main", cwd=self.project)
        execute(
            "git", f"--git-dir={self.origin}", "symbolic-ref", "HEAD", "refs/heads/main"
        )
        self.original_head = execute("git", "rev-parse", "HEAD", cwd=self.project)

        stub = self.bin / "gh"
        stub.write_text(
            f"#!{sys.executable}\n"
            + """
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
with Path(os.environ["SDLC_GH_LOG"]).open("a", encoding="utf-8") as out:
    out.write(json.dumps(args) + "\\n")

if args[:2] == ["repo", "view"]:
    print(json.dumps({
        "nameWithOwner": "example/project",
        "defaultBranchRef": {"name": "main"},
    }))
elif args[:2] == ["pr", "list"]:
    print(os.environ.get("SDLC_EXISTING_PRS", "[]"))
elif args[:2] == ["pr", "create"]:
    print("https://github.com/example/project/pull/42")
elif args[:2] == ["pr", "view"]:
    print(json.dumps({
        "url": "https://github.com/example/project/pull/42",
        "number": 42,
        "state": "OPEN",
    }))
else:
    sys.exit(1)
""",
            encoding="utf-8",
        )
        stub.chmod(0o755)
        environment = {
            "PATH": f"{self.bin}{os.pathsep}{os.environ['PATH']}",
            "SDLC_GH_LOG": str(self.log),
        }
        self.env_patch = patch.dict(os.environ, environment)
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

    def gh_calls(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def remote_bootstrap_branches(self) -> list[str]:
        output = execute(
            "git", f"--git-dir={self.origin}", "for-each-ref",
            "--format=%(refname:short)", "refs/heads/docs/sdlc-bootstrap-"
        )
        return output.splitlines() if output else []

    def assert_checkout_unchanged(self) -> None:
        self.assertEqual(
            execute("git", "rev-parse", "HEAD", cwd=self.project),
            self.original_head,
        )
        self.assertEqual(
            execute("git", "branch", "--show-current", cwd=self.project), "main"
        )
        self.assertEqual(
            execute("git", "status", "--porcelain", cwd=self.project), ""
        )

    def test_creates_bootstrap_pr_without_touching_checkout(self) -> None:
        result = bootstrap_pr.bootstrap(self.project)
        self.assertIn("https://github.com/example/project/pull/42", result)
        self.assert_checkout_unchanged()
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / "HUMANS.md").exists())
        branches = self.remote_bootstrap_branches()
        self.assertEqual(len(branches), 1)
        for name in ("AGENTS.md", "HUMANS.md"):
            content = execute(
                "git", f"--git-dir={self.origin}", "show", f"{branches[0]}:{name}"
            )
            self.assertIn("<!-- sdlc:managed:start -->", content)
        create = [x for x in self.gh_calls() if x[:2] == ["pr", "create"]]
        self.assertEqual(len(create), 1)
        self.assertIn("Bootstrap: Stefan's Development Lifecycle", create[0])

    def test_dry_run_does_not_push_or_open_pr(self) -> None:
        result = bootstrap_pr.bootstrap(self.project, dry_run=True)
        self.assertIn("Dry run only", result)
        self.assert_checkout_unchanged()
        self.assertEqual(self.remote_bootstrap_branches(), [])
        self.assertFalse(any(x[:2] == ["pr", "create"] for x in self.gh_calls()))

    def test_up_to_date_guides_do_not_open_an_empty_pr(self) -> None:
        assets = SCRIPT.parents[1] / "assets"
        for name in ("AGENTS.md", "HUMANS.md"):
            (self.project / name).write_text((assets / name).read_text(), encoding="utf-8")
        execute("git", "add", "AGENTS.md", "HUMANS.md", cwd=self.project)
        execute("git", "commit", "-m", "existing guides", cwd=self.project)
        execute("git", "push", "origin", "main", cwd=self.project)
        self.original_head = execute("git", "rev-parse", "HEAD", cwd=self.project)

        result = bootstrap_pr.bootstrap(self.project)
        self.assertIn("already current", result)
        self.assert_checkout_unchanged()
        self.assertEqual(self.remote_bootstrap_branches(), [])
        self.assertFalse(any(x[:2] == ["pr", "create"] for x in self.gh_calls()))

    def test_dirty_checkout_is_rejected(self) -> None:
        (self.project / "uncommitted.txt").write_text("retain", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not clean"):
            bootstrap_pr.bootstrap(self.project)
        self.assertEqual((self.project / "uncommitted.txt").read_text(), "retain")
        self.assertEqual(self.remote_bootstrap_branches(), [])
        self.assertFalse(self.gh_calls())

    def test_existing_bootstrap_pr_is_reported_instead_of_duplicate(self) -> None:
        existing = [{
            "title": "Bootstrap: Stefan's Development Lifecycle",
            "headRefName": "docs/sdlc-bootstrap-abcd",
            "url": "https://github.com/example/project/pull/30",
        }]
        with patch.dict(os.environ, {"SDLC_EXISTING_PRS": json.dumps(existing)}):
            result = bootstrap_pr.bootstrap(self.project)
        self.assertIn("https://github.com/example/project/pull/30", result)
        self.assert_checkout_unchanged()
        self.assertEqual(self.remote_bootstrap_branches(), [])
        self.assertFalse(any(x[:2] == ["pr", "create"] for x in self.gh_calls()))


if __name__ == "__main__":
    unittest.main()
