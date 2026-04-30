# Manual Eval: Testable Couch Session

## Purpose

Run one real or near-real Game Couch session and decide what features the project actually needs next.

This eval is about feel as much as plumbing: does it create the sense of Pip/Coda being present on the sofa while Saff plays?

## Preconditions

- Game is running on the target machine, ideally `bigchoof`.
- Game Couch coordinator can start a session.
- A Discord couch room/thread exists or can be reused.
- Remote runner or local fallback can capture a screenshot.
- Dry-run mode has already passed.
- The evaluator has a safe place to store the after-action note, such as `state/evals/<date>-couch-session.md`.

## Dry-run rehearsal

Run this before involving the real game/Discord path:

```bash
game-couch start --game generic-screen --channel "#game-couch" --player-label "Saff"
game-couch share --note "dry-run moment" --screenshot ./fixtures/moment.png --transport dry-run
```

Confirm:

- no Discord message was sent;
- a session directory exists;
- the moment is journaled;
- the payload includes game id, player label, note, trigger, and media path.

## Script

1. Start a session.
   - Record game name, host, player label, Discord target.
2. Trigger a first moment with a note.
   - Example: “opening scene / first impression”.
3. Confirm Discord receives the moment.
   - Screenshot/media visible.
   - Note and metadata understandable.
   - No unwanted pings.
4. Pip reacts in Discord as Pip, not as a hidden merged bot.
5. Trigger a second moment without over-explaining.
   - Check whether the screenshot/context is enough to respond naturally.
6. Review the local journal.
   - Confirm session start and both moments are preserved.
7. Write a short after-action note.

Use this after-action note shape:

```markdown
# Game Couch eval — YYYY-MM-DD

- Game / scene:
- Host / runner:
- Discord target:
- Moments triggered:
- What felt sofa-like:
- What broke flow:
- What Pip/Coda could infer from the moment:
- Next missing feature:
- Follow-up issues:
```

## Pass Signals

- Saff can trigger moments without breaking game flow.
- Pip can understand/react enough from the posted moment.
- The Discord room feels like the shared surface.
- The journal is useful afterwards.
- The next missing feature is obvious from the session.

## Failure Signals

- Capture is too fiddly.
- Discord posts are noisy or ugly.
- Pip lacks enough context to react.
- Remote execution feels unsafe or opaque.
- The journal is too raw to review.

## Questions to Answer After the Eval

- Do we need hotkey support before richer Discord polish?
- Is SSH capture enough, or do we need a persistent event/RTC runner?
- Do we need OCR/vision summaries immediately?
- Should Coda be automatically included in the first testable version?
- What should become the first game-specific plugin spike?
