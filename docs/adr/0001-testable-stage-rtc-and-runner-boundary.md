# ADR 0001: Testable Stage Uses SSH-First Runner With RTC Seam

## Status

Accepted for planning.

## Context

Game Couch needs to become testable in the real household setup. Saff is likely to play games on `bigchoof`, while Pip/OpenClaw may coordinate from Pip-Mansion and Discord.

The current MVP assumes local capture: the same machine that runs `game-couch` can see the screen. That is insufficient for real testing.

Saff also raised RTC as a possible guide. The project needs near-real-time couch presence, but the first testable stage does not necessarily need continuous low-latency media.

## Decision

For the next stage, Game Couch will separate:

- coordinator/session state
- runner/game-machine operations
- plugin/game context
- transport/RTC/event delivery

The first remote runner path will be SSH-first, with allowlisted operations, because it is the smallest realistic way to capture screenshots from `bigchoof` and fetch artifacts.

The design must keep a clean RTC/event seam so that a persistent runner channel, likely WebSocket over SSH tunnel, can be added later without rewriting plugins or session logic.

For this ADR, “RTC seam” means an internal boundary for commands/events/results. It does **not** mean the testable stage must ship WebRTC, a signalling server, or a continuous media stream.

WebRTC is deferred until a test session proves that continuous media or low-latency streaming is needed.

## Consequences

- The project can reach a real test session sooner than if it starts with WebRTC.
- Remote operations stay auditable and narrow.
- Plugins should not know whether they run locally or remotely; runner plumbing owns that.
- CLI/API surfaces should accept a host/runner target without leaking raw SSH commands everywhere.
- Dry-run, fake-runner, and local-runner tests can prove most behaviour before touching `bigchoof`.
- If the couch feel depends on live continuous presence, a later ADR should choose WebSocket/WebRTC explicitly.

## Boundary invariants

- The coordinator assembles moments and writes the journal; it does not execute raw remote commands.
- The runner returns artifact/result metadata; it does not decide Discord wording or session policy.
- The plugin supplies game/context semantics; it does not know whether capture happened locally, over SSH, or through a future event channel.
- The transport receives an already-assembled moment payload; it does not capture screenshots or mutate runner state.

## Non-goals

- No arbitrary remote shell passthrough.
- No always-on screen/video stream in this stage.
- No autonomous game control.
- No online-game-specific hooks.

## Related

- `docs/testable-stage-plan.md`
- GitHub issue #3: remote runner/SSH tunnel mode
