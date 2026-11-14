---
name: sdlc
description: Stefan's Development Lifecycle for Codex. Use when a developer asks to bootstrap or refresh AGENTS.md and HUMANS.md, establish or revise a project's OBJECTIVE.md, or start and plan a stream of work as a GitHub Intent Issue. Explicit actions: $sdlc bootstrap, $sdlc objective, $sdlc intent.
---

# Stefan's Development Lifecycle

A GitHub-native, intent-driven workflow for a solo developer working in one repository or monorepo. The human owns project direction and high-impact decisions. Codex assists with discovery, planning, GitHub organization, implementation, testing, and drafting PRs. Releases are independent of landing changes on trunk.

## Dispatch

Interpret the word after `$sdlc` as the **action argument** (not a separate installed skill or CLI command):

- `bootstrap`: create or refresh `AGENTS.md` and `HUMANS.md` using the packaged templates and updater.
- `objective`: clarify or revise enduring project direction and propose `OBJECTIVE.md`.
- `intent`: create/refine a GitHub Intent Issue, with optional sub-issues and proposed implementation slices.

If the action is unclear, ask which of the three the developer wants. Do not silently start implementing. Follow the action-specific reference files below.

## Global rules

1. Read existing repository guidance first: `AGENTS.md`, `HUMANS.md`, `OBJECTIVE.md`, and `VERSIONS.md` when present; preserve stricter project-specific security, testing, and operational requirements. Never treat the skill as authority to override those.
2. Planning and decision records belong in the **GitHub Issue body**. Do not create committed `intent.md`, `spec.md`, `plan.md`, or GitHub Issue Artifacts. Use Issue comments for discussion; keep the body current.
3. `OBJECTIVE.md` is a concise, durable description of *why this project exists* and its direction, not a backlog, design specification, or release calendar. It is the exception to keeping planning artifacts out of Git.
4. Use GitHub labels for type, area, priority, scope and risk; native sub-issues for distinct outcomes; Projects for status; Wiki for durable technical knowledge; PRs and CI for code review and delivery. Do not create a special authoritative Issue #1 or Version Issues.
5. `main` (or the repository's configured default branch) is trunk. Use short-lived branches and small, reviewable PRs. For dependent slices, prefer stacks of approximately 2–5 PRs. A stack is not a release boundary. Merge safe, approved slices independently of any release.
6. Human approval is required for significant scope, architecture, security, compatibility, cost or operational decisions; starting implementation; merging PRs; running impactful/live operations; tagging, publishing releases; and deploying. These are separate approvals. Never treat an Issue as implementation authorization.
7. Project-specific release/version policy belongs in `VERSIONS.md`, if present. Never assume numbering or auto-release after a merge. If no policy exists, ask for one when preparing a release.
8. Work inside the target repository. Inspect current modifications before editing. Never clobber project-specific instructions, change unrelated files, or imply a write succeeded without verifying it.
9. The design assumes one developer and one repository or monorepo. For teams or multiple independent repos, surface ownership and coordination questions instead of inventing policy.

## Actions

### `$sdlc bootstrap`

Read [references/bootstrap.md](references/bootstrap.md). The canonical templates are [assets/AGENTS.md](assets/AGENTS.md) and [assets/HUMANS.md](assets/HUMANS.md). Use [scripts/bootstrap.py](scripts/bootstrap.py) to update only the skill-managed Markdown sections while preserving everything else. Inspect changes and reconcile existing conflicting policies with the human; do not overwrite custom rules.

### `$sdlc objective`

Read [references/objective.md](references/objective.md). Ask a small series of useful questions, check existing project context, and draft the objective **in a normal GitHub Intent Issue body first**. Upon approval propose the durable `OBJECTIVE.md` in a PR. Never create or privilege Issue #1. No implementation without approval.

### `$sdlc intent`

Read [references/intent.md](references/intent.md). Check alignment with `OBJECTIVE.md`, discover duplicate work, then create or refine an Issue body with intent, criteria, design, decisions, risks and plan. Classify with labels, propose native sub-issues/dependencies for complex outcomes, and present the approval gate before coding.

## Expected reporting

End each action with a concise report: what changed (or was proposed), relevant Issue/PR URLs, unresolved decisions, and the next human approval needed. Do not merge, release, or deploy merely to complete the action.
