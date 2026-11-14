#!/usr/bin/env python3
"""Create a Bootstrap pull request without changing the current checkout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from uuid import uuid4

BRANCH_PREFIX = "docs/sdlc-bootstrap-"
PR_TITLE = "Bootstrap: Stefan's Development Lifecycle"


def command(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=check)


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return command("git", *args, cwd=root, check=check)


def github(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return command("gh", *args, cwd=root)


def bootstrap(root: Path, *, dry_run: bool = False) -> str:
    root = root.resolve()
    actual_root = Path(git(root, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if actual_root != root:
        raise ValueError(f"Run from the target repository root: {actual_root}")
    if git(root, "status", "--porcelain", "--untracked-files=all").stdout.strip():
        raise ValueError("The worktree is not clean; commit or stash unrelated edits first")

    repo_info = json.loads(
        github(root, "repo", "view", "--json", "nameWithOwner,defaultBranchRef").stdout
    )
    repository = repo_info["nameWithOwner"]
    default_branch = repo_info["defaultBranchRef"]["name"]
    if not repository or not default_branch:
        raise ValueError("Unable to resolve the GitHub repository or default branch")

    open_prs = json.loads(
        github(
            root, "pr", "list", "-R", repository, "--state", "open",
            "--json", "headRefName,url,title",
        ).stdout
    )
    existing = [
        pr for pr in open_prs
        if pr.get("headRefName", "").startswith(BRANCH_PREFIX)
        and pr.get("title", "").startswith("Bootstrap:")
    ]
    if existing:
        return f"An existing Bootstrap PR must be reviewed or updated: {existing[0]['url']}"

    git(root, "fetch", "--no-tags", "origin", default_branch)
    branch = f"{BRANCH_PREFIX}{uuid4().hex[:10]}"
    updater = Path(__file__).resolve().with_name("bootstrap.py")
    worktree_created = False

    with tempfile.TemporaryDirectory(prefix="sdlc-bootstrap-") as temporary:
        checkout = Path(temporary) / "checkout"
        try:
            git(root, "worktree", "add", "-b", branch, str(checkout), f"origin/{default_branch}")
            worktree_created = True
            updated = command(sys.executable, str(updater), "--root", str(checkout), cwd=checkout)
            if updated.stdout:
                print(updated.stdout, end="")

            git(checkout, "add", "--", "AGENTS.md", "HUMANS.md")
            diff = git(checkout, "diff", "--cached", "--quiet", check=False)
            if diff.returncode == 0:
                return "Guides are already current; no Bootstrap PR is necessary."
            if diff.returncode != 1:
                raise RuntimeError("Unable to determine whether the Bootstrap guides changed")

            git(checkout, "diff", "--cached", "--check")
            if dry_run:
                print(git(checkout, "diff", "--cached", "--", "AGENTS.md", "HUMANS.md").stdout)
                return "Dry run only; no branch was pushed or PR created."

            git(checkout, "commit", "-m", "docs: bootstrap Stefan's Development Lifecycle")
            git(checkout, "push", "-u", "origin", branch)
            body = (
                "## Bootstrap\n\n"
                "Install or refresh project-facing AGENTS.md and HUMANS.md "
                "from Stefan's Development Lifecycle skill.\n\n"
                "Only skill-managed sections were replaced. Existing custom "
                "instructions outside those sections are preserved. "
                "Please review any older guidance for conflicting rules.\n\n"
                "No project code, objective, version policy, or releases are changed. "
                "Merge only after human review and authorization."
            )
            github(
                root, "pr", "create", "-R", repository, "--base", default_branch,
                "--head", branch, "--title", PR_TITLE, "--body", body,
            )
            pr = json.loads(
                github(
                    root, "pr", "view", branch, "-R", repository,
                    "--json", "url,number,state",
                ).stdout
            )
            if pr.get("state") != "OPEN" or not pr.get("url"):
                raise RuntimeError("GitHub did not confirm an open Bootstrap pull request")
            return f"Bootstrap PR created: {pr['url']}"
        finally:
            if worktree_created:
                removed = git(root, "worktree", "remove", "--force", str(checkout), check=False)
                if removed.returncode:
                    print(f"Warning: could not remove temporary worktree: {removed.stderr}", file=sys.stderr)
                else:
                    deleted = git(root, "branch", "-D", branch, check=False)
                    if deleted.returncode:
                        print(f"Warning: could not delete local branch {branch}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true", help="Preview the proposed diff; don't push or open a PR")
    args = parser.parse_args()
    try:
        print(bootstrap(args.root, dry_run=args.dry_run))
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) and error.stderr else str(error)
        print(f"sdlc bootstrap: {detail}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
