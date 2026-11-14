# Action: bootstrap

**Goal:** Open a **Bootstrap pull request** that installs or refreshes `AGENTS.md` and `HUMANS.md` in the target repository. Creating files in the user's current checkout alone is **not** a completed bootstrap.

## Required behavior

1. Identify the target GitHub repository and its default branch. Work in the **target project**, not the skill repository. Inspect the existing guides, any project-specific safety/operational instructions, and the Git worktree. Do not overwrite or commit unrelated user changes.
2. Preview the proposed Bootstrap PR by invoking the bundled orchestration script:

   ```sh
   python3 /path/to/installed/sdlc/scripts/bootstrap_pr.py --root . --dry-run
   ```

   Resolve the script path relative to the installed skill. The script uses a temporary Git worktree based on the remote default branch; it never changes the user's current checkout.
3. Review the diff for obsolete or conflicting rules. If the project contains older guidance (such as Issue #1 authority, Version Issues, or unsafe run instructions), flag it and propose a **specific reconciliation**, preserving stronger project-specific safeguards. Do not silently delete old instructions outside the managed section. If necessary, stop and request a human decision before publishing contradictory instructions.
4. **Complete the action by opening the PR**, using:

   ```sh
   python3 /path/to/installed/sdlc/scripts/bootstrap_pr.py --root .
   ```

   The script creates a short-lived branch from the configured default branch, applies [assets/AGENTS.md](../assets/AGENTS.md) and [assets/HUMANS.md](../assets/HUMANS.md) through [scripts/bootstrap.py](../scripts/bootstrap.py), stages **only those files**, commits, pushes, and opens an ordinary GitHub PR titled **Bootstrap: Stefan's Development Lifecycle**. It then verifies the PR exists and is open.
5. Return the **actual Bootstrap PR URL** and a brief summary of created/updated guide sections. **Do not merge**; the human must review and separately authorize merging. Do not create a special bootstrap Issue or make a release.
6. If both guides already match the templates, report **already up to date**; GitHub cannot open a useful no-diff PR. If an earlier Bootstrap PR is still open, link it rather than opening a duplicate, and make clear whether its content is current.
7. If GitHub access, `gh` authentication, a remote default branch, Git identity, or permissions are missing, report the precise blocker. **Do not claim success or stop after writing files locally.** The script requires a clean worktree for safety and does not stage unrelated changes.

## Safe updates

The low-level [scripts/bootstrap.py](../scripts/bootstrap.py) only updates documents in a directory. It is an internal building block, **not** the complete `$sdlc bootstrap` action. It refreshes text between `<!-- sdlc:managed:start -->` and `<!-- sdlc:managed:end -->`, preserving other sections. On first adoption of an unmanaged file, it appends the managed section instead of replacing project-specific guidance.

After upgrading the installed skill, run `$sdlc bootstrap` again to open a new PR containing any changes. The updater is idempotent and does not produce a new PR for identical templates.

Bootstrap does **not** create `OBJECTIVE.md` or `VERSIONS.md`. Suggest `$sdlc objective` if the project objective is missing.
