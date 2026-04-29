# Game Couch Testable Stage Plan

## Goal

Get Game Couch from a local CLI MVP to a testable couch session where Saff can play on `bigchoof`, Pip/Coda can participate from Discord, and the system can prove the core loop without pretending to be finished.

The testable stage is not “production game companion.” It is the smallest end-to-end setup that lets us answer: does this feel like having friends on the sofa while a game is happening?

## Experience Target

A successful test session should look like this:

1. Saff starts a Game Couch session for a game running on `bigchoof`.
2. A Discord couch room/thread exists for that session.
3. Saff can trigger a moment with a hotkey or simple command.
4. The moment captures the current game screen on `bigchoof`.
5. The moment appears in Discord with screenshot, note/context, and session metadata.
6. Pip and/or Coda can react naturally in Discord as themselves.
7. The session journal preserves what happened.
8. We can inspect the session afterwards and decide what should become richer.

## Guiding Architecture

Separate four responsibilities:

- **Coordinator**: owns session state, journal, Discord routing, and policy.
- **Runner**: executes safe game-machine operations on `bigchoof`, such as screenshot capture.
- **Plugin**: describes game-specific context and capture semantics; `generic-screen` stays the first plugin.
- **Transport/RTC layer**: carries commands, events, and media between coordinator, runner, and Discord.

The current MVP has coordinator/plugin/transport collapsed into local CLI code. The next stage should pull them apart without overbuilding.

## RTC Direction

Use “RTC” as a project question, not an immediate commitment to WebRTC everywhere.

For the testable stage, we need near-real-time couch events, not low-latency video streaming. Candidate layers:

1. **SSH command runner** — easiest first path for `bigchoof` operations.
   - Good for screenshots, artifact fetches, health checks.
   - Poor for continuous event streams or bidirectional browser-like presence.

2. **Local runner process with WebSocket/event channel** — likely next after SSH.
   - Good for hotkeys, moment events, lightweight status, future agent-requested peeks.
   - Can still be reached through an SSH tunnel.

3. **WebRTC** — later, only if we need live media/low-latency streams.
   - Good for live screen/audio presence.
   - Too much for the first testable stage unless the test specifically needs continuous media.

Decision for now: **do SSH-first runner plumbing with a clean RTC/event seam**, so WebSocket/WebRTC can replace or augment it later.

## Scope for Testable Stage

### In scope

- Named host config for `bigchoof` outside the repo.
- Remote runner abstraction with allowlisted operations.
- `generic-screen` remote screenshot capture.
- Artifact copy/fetch from runner to coordinator.
- Discord session room/thread posting with image attachment if supported.
- Dry-run and fake-runner tests.
- A documented manual test script for one real play session.
- Session scrapbook/journal enough to review afterwards.

### Out of scope

- Always-on video stream.
- Autonomous game control / wheel mode.
- WoW-specific integration.
- Anti-cheat/ToS-sensitive hooks.
- Voice channel awareness.
- Rich OCR/vision automation beyond optional follow-up hooks.
- Arbitrary shell execution from Discord.

## Safety and Privacy Constraints

- Remote runner exposes allowlisted operations only.
- Secrets and hostnames live in local config/env, not repo.
- Discord posting should avoid `@everyone`/role pings by default.
- Moment capture is player-triggered first.
- Agent-requested peeks must be explicit and visible in the session room.
- External/online game integrations require separate review.

## Proposed Milestones

### Milestone 1 — Remote runner seam

Done when:

- `game-couch` has a runner interface.
- Local runner and fake runner exist.
- SSH runner can be configured for a named host.
- Tests cover command construction and allowlist validation without live SSH.

### Milestone 2 — Remote generic-screen capture

Done when:

- `game-couch share --host bigchoof --note "..."` can ask the remote runner for a screenshot.
- The screenshot artifact is fetched or copied into the session directory.
- Dry-run/fake-runner tests cover the capture path.
- Manual docs explain setup for bigchoof.

### Milestone 3 — Discord couch room transport

Done when:

- A session can create/reuse a Discord target for the couch session.
- Moment posts include screenshot media, note, game/session metadata, and safe mention behavior.
- Transport has dry-run coverage.
- Webhook-only mode is either kept as a fallback or replaced by OpenClaw-native messaging.

### Milestone 4 — Test session protocol

Done when:

- `docs/evals/` contains a repeatable manual evaluation script.
- The script defines setup, start, capture, reaction, journal review, and pass/fail prompts.
- We run at least one real session and capture findings as follow-up issues.

### Milestone 5 — RTC/event seam spike

Done when:

- We decide whether SSH is enough for near-term couch presence.
- If not, we prototype a runner event channel, likely WebSocket over SSH tunnel.
- WebRTC is explicitly deferred unless the test session proves live media is needed.

## Open Questions

- Is bigchoof reachable directly by SSH from Pip-Mansion, or do we need a tunnel/reverse tunnel?
- Should the runner be a Python package installed on bigchoof, or a single script copied/executed by SSH?
- Should Discord session creation be handled by OpenClaw tooling, a Discord bot token, or webhook plus existing channel conventions?
- What is the first real game/test scenario? Generic desktop capture is enough technically, but the feel test needs an actual game.
- Do Pip and Coda both need automatic notification/participation routing in v1, or is Pip-only acceptable for the first test?

## Goblin Wrangler Notes

Implementation work should be split into issues with launch packets. Each issue should include:

- context and experience target
- non-goals
- acceptance criteria
- likely files
- test commands
- manual verification steps
- explicit “do not implement side quests” notes

Goblin tasks should not make architecture decisions silently. If a decision changes runner/transport/plugin boundaries, add or update an ADR first.
