# Bootstrap technology discussion

`TECHNOLOGY.md` is a **project-specific, durable technology policy**. It describes chosen technologies, preferences for how to use them, the reasoning behind important choices, and meaningful constraints. The SDLC skill must not prescribe a single stack across projects.

## Conversation-first discovery

Before opening a Bootstrap PR for a new project:

1. Inspect existing code, dependency manifests, configuration, README, deployment setup, and any existing `TECHNOLOGY.md`. Derive only what the repository actually establishes.
2. Ask **a few focused questions at a time** in Codex, not a long mandatory questionnaire. Cover only relevant choices:
   - Programming languages and runtime versions, including preferences such as typing conventions or supported platforms
   - Application style and framework choices: API, CLI, UI, SSR/SPA, and key libraries
   - Persistence and messaging, if needed
   - Deployment and infrastructure preferences: local-first, containers, cloud, IaC, environments
   - Testing, tooling, code style, package/dependency management, and CI
   - Constraints, choices deliberately avoided, and why a choice was made
3. Where the user has not chosen something, offer a compact set of reasonable alternatives and your recommended default with tradeoffs. Do not invent a decision. Mark truly unresolved options as **Undecided** instead of making up a stack.
4. **Present the proposed technology policy in conversation for explicit approval.** Do not send the human to a file or Issue for manual editing. Bootstrap does not need a special Issue number.
5. Once approved, draft a complete `TECHNOLOGY.md` outside the current project worktree (a temporary file is fine). Reuse that exact draft during the dry run and final Bootstrap PR command. Check that it contains no tokens, passwords, private infrastructure secrets, or irrelevant implementation plans.

For an **existing project**, read and preserve its current `TECHNOLOGY.md` by default. Ask targeted questions about gaps or revisions; only replace the file when the human explicitly approves a new draft. If it is missing, produce an approved draft based on the confirmed existing stack and preferences.

## Suggested TECHNOLOGY.md shape

Use the headings that materially describe this project; keep it concise.

```markdown
# Technology

## Stack
- Language/runtime: ...
- Backend/frontend/CLI frameworks: ...
- Storage/messaging: ...
- Infrastructure and deployment: ...

## Engineering preferences
- Typing/style/architecture: ...
- Tests and quality checks: ...
- Package/build tooling: ...

## Rationale and tradeoffs
- Choice: ... because ...
- Deliberately avoided: ... because ...

## Constraints and open choices
- Must support: ...
- Undecided: ...
```

Avoid empty placeholder bullets or invented version numbers. Separate *selected technology* from *preference* and *reasoning*. This is not a detailed architecture design, product objective, implementation plan, or release policy. The objective belongs in `OBJECTIVE.md`; implementation decisions belong in GitHub Issue bodies; releases belong in `VERSIONS.md`.

## Passing the draft to the Bootstrap PR script

Create an approved file outside the project checkout. For example:

```sh
technology_draft="$(mktemp /tmp/sdlc-technology.XXXXXX)"
# Codex writes the approved TECHNOLOGY.md Markdown to "$technology_draft"
python3 /path/to/installed/sdlc/scripts/bootstrap_pr.py --root . \
  --technology-file "$technology_draft" --dry-run
python3 /path/to/installed/sdlc/scripts/bootstrap_pr.py --root . \
  --technology-file "$technology_draft"
```

Only after the human approves the choices should Codex execute the final command. Handle the temporary draft securely and remove it when it is no longer needed.

If the remote default branch already has an approved `TECHNOLOGY.md` and no changes are proposed, omit `--technology-file`; the script leaves that file unchanged. If the file is absent, `--technology-file` is mandatory. Never complete bootstrap by committing a generic, unfilled technology template.
