# Action: objective

**Goal:** Establish or deliberately revise an enduring `OBJECTIVE.md` through a normal Intent Issue and reviewed PR.

1. Read the repository, README, current `OBJECTIVE.md` if any, active Issues and historical documents. Existing project guidance Issues (including #1 in old projects) may inform the draft but have **no privileged authority**.
2. Ask focused conversational questions in short rounds. Cover the problem and audience, purpose, desired outcomes, direction over time, scope/non-goals, and guiding principles. Skip questions already answered by the user or the repository. If a choice is consequential, surface alternatives and ask for a human decision.
3. Find an appropriate existing Intent Issue or create a **regular GitHub Issue** with no special number. Put the approved/revised purpose and outstanding questions **in its body**, along with acceptance criteria for the objective. Comments are discussion, not the canonical draft.
4. Draft a concise `OBJECTIVE.md` with these headings (adapt as justified):
   - Purpose
   - Problem and audience
   - Desired outcomes
   - Direction
   - Scope and non-goals
   - Guiding principles
   Do not add detailed feature plans, architecture designs, milestone dates, version numbers, or release calendars.
5. Request human approval of material project direction before opening the objective PR. Upon approval, use a short-lived branch and open a PR adding/updating `OBJECTIVE.md`, linked to the Intent Issue. Do not merge without separate authorization.
6. For a new project without a configured GitHub remote, prepare a reviewable draft locally, tell the human what is missing to open the Issue/PR, and do not invent an issue number or claim it has been saved in GitHub.
7. After approved merge, close the bootstrap/update Intent Issue when its criteria are met. Future work should be evaluated against the objective, but changing it requires a new or existing approved Intent Issue and PR.

Example prompt: `$sdlc objective Help me define the purpose and direction of this repository; ask questions before proposing the charter.`
