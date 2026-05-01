# Manual Eval: Testable Couch Session

## Purpose

Run one real or near-real Game Couch session and decide what features the project actually needs next.

This eval is about feel as much as plumbing: does it create the sense of Pip/Coda being present on the sofa while Saff plays?

The commentator lens matters: do not only ask whether a command executed. Ask whether the posted moment gives a watcher enough shared object, timing, and invitation to make a natural couch-side comment.

## Preconditions

- Game is running on the target machine, ideally `bigchoof`.
- Game Couch coordinator can start a session.
- A Discord couch room/thread exists or can be reused.
- Remote runner or local fallback can capture a screenshot.
- Dry-run mode has already passed.

## Script

1. Start a session.
   - Record game name, host, player label, Discord target.
   - Record whether Pip/Coda are already present in the Discord surface or need to be pulled in manually.
2. Trigger a first moment with a note.
   - Example: “opening scene / first impression”.
   - The note should be short enough that it could plausibly be typed while playing.
3. Confirm Discord receives the moment.
   - Screenshot/media visible.
   - Note and metadata understandable.
   - No unwanted pings.
4. Pip reacts in Discord as Pip, not as a hidden merged bot.
   - Assess whether the reaction refers to the actual posted object rather than generic encouragement.
5. Trigger a second moment without over-explaining.
   - Check whether the screenshot/context is enough to respond naturally.
   - If the watcher has to ask “what am I looking at?”, capture that as a context gap rather than papering it over with explanation.
6. Review the local journal.
   - Confirm session start and both moments are preserved.
7. Write a short after-action note.

## Pass Signals

- Saff can trigger moments without breaking game flow.
- Pip can understand/react enough from the posted moment.
- The Discord room feels like the shared surface.
- The journal is useful afterwards.
- The next missing feature is obvious from the session.

## Commentator Rubric

For each posted moment, score the watcher experience before discussing implementation fixes:

| Check | Pass | Fail |
| --- | --- | --- |
| Shared object | A specific visible thing can be pointed at. | The screenshot/note is too vague to know what matters. |
| Timing | The moment arrives close enough to feel live. | The post feels like a delayed scrapbook entry. |
| Invitation | A natural reaction is obvious: joke, question, surprise, advice, or sympathy. | The only possible response is generic “nice” or admin chatter. |
| Player flow | Triggering did not noticeably interrupt play. | Capturing the moment became the main activity. |
| Agent separateness | Pip/Coda can respond as themselves in the room. | The harness voice swallows the participants. |

If plumbing succeeds but the commentator rubric fails, treat the eval as a product failure with useful evidence, not a pass.

## Failure Signals

- Capture is too fiddly.
- Discord posts are noisy or ugly.
- Pip lacks enough context to react.
- Pip/Coda can only make generic comments because the moment lacks a clear object or invitation.
- Remote execution feels unsafe or opaque.
- The journal is too raw to review.

## Questions to Answer After the Eval

- Do we need hotkey support before richer Discord polish?
- Is SSH capture enough, or do we need a persistent event/RTC runner?
- Do we need OCR/vision summaries immediately?
- Should Coda be automatically included in the first testable version?
- What should become the first game-specific plugin spike?
