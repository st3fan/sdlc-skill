# Stefan's Development Lifecycle

A reusable **Codex skill** for a solo, GitHub-native, AI-assisted software development lifecycle. Install it once and use the same three actions in any project. The project repository keeps only lightweight operating guides and durable project-specific guidance, not a private copy of the skill.

Inspired by [Anthropic's AI-Native SDLC Playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook), adapted to GitHub Issues, Projects, PRs, and trunk-based development.

## Use it in Codex CLI/TUI

From a project directory, start `codex` and type:

| Action | Example | What happens |
| --- | --- | --- |
| **bootstrap** | `$sdlc bootstrap` | Create/update `AGENTS.md` and `HUMANS.md` from reusable, non-destructive templates |
| **objective** | `$sdlc objective` | Discuss purpose and direction, capture a normal Intent Issue, and propose `OBJECTIVE.md` in a PR after approval |
| **intent** | `$sdlc intent Add target exclusions` | Clarify a workstream, write the GitHub Issue body, apply labels, and plan sub-issues and reviewable PRs |

`$sdlc` activates **one skill**. The next word is an *action argument*, not a shell subcommand or another skill. You can also invoke it using Codex's `/skills` picker. Codex may use it automatically for matching tasks, but explicit invocation is the clearest choice.

## Install once for all projects (recommended)

The simplest update-friendly installation is a checkout plus a user-level symlink:

```sh
git clone https://github.com/st3fan/sdlc-skill.git "$HOME/.local/share/sdlc-skill"
mkdir -p "$HOME/.agents/skills"
ln -s "$HOME/.local/share/sdlc-skill/skills/sdlc" "$HOME/.agents/skills/sdlc"
```

Codex loads user skills from `~/.agents/skills` and supports symlinked skill folders. Start a new Codex session if the skill does not appear immediately. See the [Codex skills documentation](https://developers.openai.com/codex/skills).

**Alternative:** in Codex, ask its built-in installer:

```text
$skill-installer Install https://github.com/st3fan/sdlc-skill/tree/main/skills/sdlc
```

The installer copies the skill into a Codex skill directory. The symlink approach above is preferable when you want ordinary `git pull` updates.

**If you already have a skill named `sdlc` installed**, inspect it first rather than overwriting it. You need only one installed copy.

## Start a new project

1. Create/open a repository and start Codex there.
2. Run `$sdlc bootstrap` to install the project-facing `AGENTS.md` and `HUMANS.md`.
3. Run `$sdlc objective`. Codex asks focused questions about purpose, audience, outcomes, direction, non-goals, and principles. It records the proposal in a regular GitHub Intent Issue body, then opens a PR for `OBJECTIVE.md` after your approval.
4. Run `$sdlc intent <your idea>` whenever you want to begin another stream of work.

No special Issue #1, Version Issue, or version-based PR stack is required. For an existing repository, the skill adapts its guidance while retaining existing security and operational constraints.

## Where artifacts live

| Artifact | Scope | Purpose |
| --- | --- | --- |
| `skills/sdlc/SKILL.md` + references | **Global SDLC** | Rules for bootstrap, objective, intent, and the GitHub-native lifecycle |
| `skills/sdlc/assets/*` + bootstrap script | **Global SDLC** | Canonical managed sections of generated guides and their safe updater |
| `AGENTS.md` | **Project-specific + managed global section** | Local agent instructions, safety constraints, and pointer to the skill |
| `HUMANS.md` | **Project-specific + managed global section** | How humans invoke the skill and interact with this repository |
| `OBJECTIVE.md` | **Project-specific** | Enduring project purpose, direction, outcomes, and non-goals |
| `VERSIONS.md` (optional) | **Project-specific** | Versioning and release policy; never assumed globally |
| GitHub Intent Issue **body** | **Per workstream** | Intent, requirements, design, plan, decisions, acceptance criteria |
| GitHub sub-issues, labels, Project | **Per workstream** | Deliverable decomposition, classification, status |
| GitHub PRs / PR stacks, CI | **Per workstream** | Reviewable code delivery and validation |
| GitHub Wiki | **Project-specific** | Durable technical and operational knowledge |

`OBJECTIVE.md` is a durable charter, not a detailed spec or a roadmap. Implementation plans remain in Issue bodies, **not** in committed `intent.md`/`spec.md`/`plan.md` or GitHub Issue Artifacts.

Work merges in small safe slices into the default branch; releases happen separately on human request, following that project's `VERSIONS.md` if present.

## Update the skill and project guides

```sh
git -C "$HOME/.local/share/sdlc-skill" pull --ff-only
```

Then from each project that you want to refresh, run `$sdlc bootstrap` again.

The bootstrap script replaces only the text between `<!-- sdlc:managed:start -->` and `<!-- sdlc:managed:end -->`. It never overwrites custom text outside those markers. For **previously unmanaged** documents, it appends a managed section for review rather than replacing old rules. Codex should reconcile contradictory legacy instructions with you.

You may inspect the results directly:

```sh
python3 "$HOME/.local/share/sdlc-skill/skills/sdlc/scripts/bootstrap.py" --root . --dry-run
python3 "$HOME/.local/share/sdlc-skill/skills/sdlc/scripts/bootstrap.py" --root . --check
```

`--check` returns 1 when updates are needed; default mode applies updates. No project needs a copy of the updater.

## Development and tests

Skill layout:

```text
skills/sdlc/
  SKILL.md
  agents/openai.yaml
  assets/AGENTS.md
  assets/HUMANS.md
  references/bootstrap.md
  references/objective.md
  references/intent.md
  scripts/bootstrap.py
  tests/test_bootstrap.py
```

Run tests from the skill repository root:

```sh
python3 -m unittest discover -s skills/sdlc/tests -v
```

The updater requires Python 3.10+ and no third-party libraries. Codex needs Git and an authenticated GitHub CLI (`gh`) or an equivalent authorized GitHub integration for GitHub operations.

## Scope

This is built for **one developer working in a single repository or monorepo**. It should translate to teams, but shared ownership, concurrent work on a single intent, and multiple independent repositories require additional coordination decisions. A monorepo may make agentic work easier when related code needs to change together; that remains a working hypothesis rather than a universal rule.
