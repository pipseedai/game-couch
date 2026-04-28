# AGENT_WORKFLOW.md

Reusable work ritual for agents in this project.

## Before Coding

Agents must:

1. Read `AGENTS.md`, `PROJECT.md`, `ROADMAP.md`, and relevant ADRs.
2. Restate the goal.
3. Define non-goals.
4. Write acceptance criteria.
5. Identify likely files to change.
6. Name likely tests/checks before editing.

## During Work

Agents must:

- stay inside the stated acceptance criteria
- reuse existing abstractions before adding new ones
- add or update tests with behaviour changes
- update docs when user-facing or agent-facing behaviour changes
- capture side ideas as follow-up issues/notes instead of implementing them immediately

## After Work

Agents must produce a closeout summary with:

- completed work
- not completed / intentionally deferred work
- tests run
- docs updated
- issues to close
- follow-ups created or recommended

## Main Quest Rule

If an agent notices a broader idea while working, capture it as a follow-up. Do not implement it unless required by the current acceptance criteria.
