# Stefan's Development Lifecycle

A reusable **Codex skill** for a solo, GitHub-native, AI-assisted software development lifecycle. Install it once and use the same three actions in any project. The project repository keeps only lightweight operating guides and durable project-specific guidance, not a private copy of the skill.

Inspired by [Anthropic's AI-Native SDLC Playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook), adapted to GitHub Issues, Projects, PRs, and trunk-based development.

## Use it in Codex CLI/TUI

From a project directory, start `codex` and type:

| Action | Example | What happens |
| --- | --- | --- |
| **bootstrap** | `$sdlc bootstrap` | Open a **Bootstrap PR** creating/updating `AGENTS.md` and `HUMANS.md` from reusable templates, without changing your current checkout |
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

### Optional: install only for one Codex project

If you do not want user-wide installation, place a symlink to the same skill directory in just that repository:

```sh
cd /path/to/your/project
mkdir -p .agents/skills
ln -s "$HOME/.local/share/sdlc-skill/skills/sdlc" .agents/skills/sdlc
```

This does **not** copy the skill's content, but the symlink itself becomes project metadata if committed. Prefer the user-level installation above for your normal solo workflow.

## Planning is conversation-first

The **Codex conversation** is where you and the agent develop the objective or intent. Codex should show the current proposal, ask targeted questions, discuss tradeoffs, and present an approval summary **in chat**. You do **not** need to open a GitHub Issue to review or edit it yourself. Codex keeps the **Issue body** synchronized with confirmed decisions, making GitHub the durable system of record. You may edit an Issue directly if you want; Codex must re-read and respect those changes.

Example: after `$sdlc objective`, Codex should summarize the project direction, ask whether AI behavior or proposed exclusions are correct, update the Issue body as answers are confirmed, and request approval in Codex before proposing the `OBJECTIVE.md` PR.

## Start a new project

1. Create/open a repository and start Codex there.
2. Run `$sdlc bootstrap` to open a **Bootstrap: Stefan's Development Lifecycle** PR containing `AGENTS.md` and `HUMANS.md`. Review and merge that PR; bootstrap never merges automatically.
3. Run `$sdlc objective`. Codex asks focused questions about purpose, audience, outcomes, direction, non-goals, and principles. It records the proposal in a regular GitHub Intent Issue body, then opens a PR for `OBJECTIVE.md` after your approval.
4. Run `$sdlc intent <your idea>` whenever you want to begin another stream of work.

No special Issue #1, Version Issue, or version-based PR stack is required. For an existing repository, the skill adapts its guidance while retaining existing security and operational constraints.

## Where artifacts live

| Artifact | Scope | Purpose |
| --- | --- | --- |
| `skills/sdlc/SKILL.md` + references | **Global SDLC** | Rules for bootstrap, objective, intent, and the GitHub-native lifecycle |
| `skills/sdlc/assets/*` + bootstrap scripts | **Global SDLC** | Canonical managed sections, safe updater, and branch/PR orchestration |
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

Then from each project that you want to refresh, run `$sdlc bootstrap` again to **open a new Bootstrap PR**. If nothing has changed, Codex reports the guides are current without creating an empty PR.

The bootstrap script replaces only the text between `<!-- sdlc:managed:start -->` and `<!-- sdlc:managed:end -->`. It never overwrites custom text outside those markers. For **previously unmanaged** documents, it appends a managed section for review rather than replacing old rules. Codex should reconcile contradictory legacy instructions with you.

The actual `$sdlc bootstrap` action previews an isolated worktree and then opens a PR from a temporary branch based on the remote default branch. It only stages the two guide files, leaves your current checkout unchanged, and never merges the PR. It requires a **clean worktree**, a GitHub remote, Git identity, and an authenticated `gh` CLI. An existing open Bootstrap PR is reported instead of creating a duplicate.

You can inspect the proposed changes **without creating a PR**:

```sh
python3 "$HOME/.local/share/sdlc-skill/skills/sdlc/scripts/bootstrap_pr.py" --root . --dry-run
```

Codex normally runs this for you. The low-level `scripts/bootstrap.py` updates files in a provided directory and is used **only inside** the Bootstrap PR workflow; running that helper by itself is not a completed bootstrap. No project needs a copy of either script.

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
  scripts/bootstrap_pr.py
  tests/test_bootstrap.py
  tests/test_bootstrap_pr.py
```

Run tests from the skill repository root:

```sh
python3 -m unittest discover -s skills/sdlc/tests -v
```

The Bootstrap PR workflow requires Python 3.10+ and no third-party libraries. Codex needs Git and an authenticated GitHub CLI (`gh`) or an equivalent authorized GitHub integration for GitHub operations.

## Scope

This is built for **one developer working in a single repository or monorepo**. It should translate to teams, but shared ownership, concurrent work on a single intent, and multiple independent repositories require additional coordination decisions. A monorepo may make agentic work easier when related code needs to change together; that remains a working hypothesis rather than a universal rule.
