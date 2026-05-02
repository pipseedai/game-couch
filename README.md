# Game Couch

A local game-presence harness for sharing play sessions with AI companions as real Discord participants.

Game Couch is stagehand infrastructure, not a merged bot persona. The player drives; Pip, Coda, and friends can react in Discord to player-triggered moments that include a screenshot, note, and lightweight plugin context.

## MVP model

- Local CLI starts or reuses a play session.
- `generic-screen` is the first game-agnostic plugin.
- `game-couch share` posts a manual moment bundle.
- Journals are written locally as JSONL per session.
- Automated tests use a dry-run transport so no Discord messages are sent.

Non-goals for v0: WoW-specific integration, wheel/autonomous control mode, console capture cards, and always-on video.

## Install for local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e . pytest
```

## Start a couch session

```bash
game-couch start --game generic-screen --channel "#game-couch" --player-label "Saff"
```

This writes session metadata under:

```text
~/.local/share/game-couch/sessions/<session-id>/
```

Set `GAME_COUCH_HOME=/path/to/dir` to use a different storage location.

## Share a manual moment

Safest dry-run flow:

```bash
game-couch share --note "look at this jump" --screenshot ~/Desktop/moment.png --transport dry-run
```

If `--screenshot` is omitted, `generic-screen` attempts a one-shot macOS `screencapture`. On other systems, pass a screenshot path explicitly.

Moment payloads include:

- session id
- game id
- player label
- trigger
- timestamp
- optional note
- screenshot/media path
- plugin context

## Discord config

The MVP Discord transport posts via webhook. For the testable stage, create or pick the couch room/thread in Discord first, create a webhook for that target, then start Game Couch with the same target label so the session and journal name where the moment went:

```bash
export GAME_COUCH_DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
game-couch start --game generic-screen --channel "#game-couch" --player-label "Saff"
game-couch share --note "boss down" --screenshot ~/Desktop/moment.png --transport discord
```

Moment posts include safe mention settings (`allowed_mentions.parse=[]`) and attach the screenshot/media file when the media path exists. If the file is missing, Game Couch still posts the structured text payload and records the missing media in delivery metadata.

Do not commit webhook URLs or bot tokens. Tests and local development should prefer `--transport dry-run`.

### Manual Discord media smoke

1. Start with dry-run and inspect `dry-run-outbox.jsonl` to confirm note, player, game, session, trigger, timestamp, and media metadata.
2. Set `GAME_COUCH_DISCORD_WEBHOOK_URL` for a private test channel/thread.
3. Run `game-couch share --note "media smoke" --screenshot <png> --transport discord`.
4. Confirm Discord shows one message with the screenshot attachment and no accidental pings.
5. Inspect the session journal for the `moment.shared` event and Discord transport status.

## Plugin interface

See [`docs/plugins.md`](docs/plugins.md). The implemented plugin is `generic-screen`.

## Tests

```bash
pytest
```
