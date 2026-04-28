# AGENTS.md

Repo-local instructions for agents working in this project. Read this file first, before changing code or docs.

## Start Here

Before editing, read:

1. `PROJECT.md` — purpose, non-goals, and design principles
2. `ROADMAP.md` — current priorities and parking-lot ideas
3. `AGENT_WORKFLOW.md` — reusable before/during/after work ritual
4. relevant ADRs in `docs/adr/`
5. the issue, task brief, or human request that defines the current work

## Main Quest

Stay on the main quest.

If you notice a broader idea while working, capture it as a follow-up issue or note. Do not implement a side quest unless it is required by the current acceptance criteria.

## Default Workflow

Before coding:

- restate the goal
- name non-goals
- define acceptance criteria
- identify likely files to change
- name tests/checks you expect to run

During work:

- stay inside scope
- reuse existing abstractions
- add or update tests for behaviour changes
- update docs for user-facing or agent-facing changes
- record durable design decisions as ADRs

After work:

- run the smallest meaningful verification gate
- summarize completed work, deferred work, tests run, docs changed, and follow-ups

## Project-Specific Notes

- Add repo-specific commands, constraints, owners, environments, and gotchas here.
- Keep this guidance specific to this repository; reusable rituals belong in `AGENT_WORKFLOW.md`.
