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

If `--screenshot` is omitted, Game Couch asks a runner to capture one screenshot. The default `local` runner uses one-shot macOS `screencapture`; tests can use `--runner fake` without touching the real screen.

## Remote runner seam

A session can remember a named host, and `share` can target a named SSH runner when no screenshot path is provided:

```bash
export GAME_COUCH_HOST_BIGCHOOF_SSH="saff@bigchoof"
export GAME_COUCH_HOST_BIGCHOOF_REMOTE_DIR="~/game-couch-captures"  # optional

game-couch start --game generic-screen --channel "#game-couch" --player-label "Saff" --host bigchoof
game-couch share --note "look at this jump" --transport dry-run
```

The SSH runner has an allowlisted first operation only: `capture_screenshot`. It constructs `ssh` + `scp` commands for that operation and does not expose arbitrary remote shell passthrough.

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

The MVP Discord transport posts via webhook:

```bash
export GAME_COUCH_DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
game-couch share --note "boss down" --screenshot ~/Desktop/moment.png --transport discord
```

Do not commit webhook URLs or bot tokens. Tests and local development should prefer `--transport dry-run`.

## Plugin interface

See [`docs/plugins.md`](docs/plugins.md). The implemented plugin is `generic-screen`.

## Tests

```bash
pytest
```
