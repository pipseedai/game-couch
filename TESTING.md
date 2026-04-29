# Testing

MVP coverage includes:

- Unit tests for moment payload shaping.
- Unit tests for plugin loading and `generic-screen` start context.
- Unit tests for journal JSONL writing and dry-run transport outbox writing.
- CLI smoke test for `game-couch start` and `game-couch share` with `--transport dry-run`.

Run locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e . pytest
pytest
```

Dry-run transport is the default for `game-couch share`, so CI and local tests do not send real Discord messages.

Manual Discord posting check, when a webhook is intentionally configured:

```bash
export GAME_COUCH_DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
game-couch start --game generic-screen --channel "#game-couch" --player-label "Saff"
game-couch share --note "manual webhook check" --screenshot /path/to/screenshot.png --transport discord
```
