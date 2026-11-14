# Action: bootstrap

**Goal:** Make a repository ready to use Stefan's Development Lifecycle while keeping all reusable workflow logic in the globally installed skill.

1. Verify which directory is the *target project* (not the skill source repository). Inspect the existing `AGENTS.md` and `HUMANS.md`, and check the worktree for unsaved or unrelated edits. If an existing target file has uncommitted changes, explain what will be updated before proceeding.
2. Run the bundled updater from the target project root:

   ```sh
   python3 /path/to/installed/sdlc/scripts/bootstrap.py --root .
   ```

   Resolve the script path from this skill's installed folder rather than assuming `~/.agents/skills` or a project-local copy. Use `--dry-run` to preview, `--check` to report whether updates are needed.
3. The updater creates missing guides, replaces only blocks between `<!-- sdlc:managed:start -->` and `<!-- sdlc:managed:end -->`, and leaves everything outside the markers untouched. On first adoption of a previously unmanaged document it **appends** the current skill-managed block instead of replacing the old document. Do not blindly overwrite custom project instructions.
4. After updating, **read the full files**, check for contradictory older rules (e.g., special Issue #1, Version Issues, releases tied to merges, unsafe operational instructions), and propose a focused reconciliation. Protect project-specific safety constraints even if the generic template is newer.
5. Confirm that `OBJECTIVE.md` exists or suggest `$sdlc objective` as the next action. Do **not** generate `OBJECTIVE.md` or `VERSIONS.md` from this action.
6. Report created/updated/unchanged files and proposed follow-up. Do not commit or merge unless requested.

Future skill template changes are applied by running `$sdlc bootstrap` again after the installed skill has been updated. The updater is idempotent: the same templates do not produce another diff.
