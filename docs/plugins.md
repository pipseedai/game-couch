# Plugin Interface

Game Couch keeps the core game-agnostic. A plugin supplies the minimum game-specific context needed for a couch moment.

A plugin implements `GamePlugin` from `game_couch.plugins.base`:

- `game_id`: stable CLI id, for example `generic-screen`
- `start_context(session)`: lightweight context recorded when a play session starts
- `capture_moment_context(session, screenshot_path)`: context bundled with each shared moment
- `capture_screenshot(destination)`: optional helper for player-triggered capture when no screenshot path is supplied

## `generic-screen`

The MVP plugin is deliberately plain desktop context:

- no game API integration
- no WoW-specific behavior
- no always-on stream
- no autonomous control

`game-couch share --screenshot /path/to/file.png` is the safest path. On macOS, omitting `--screenshot` attempts a one-shot `screencapture` into the current session's `captures/` directory.
