# Game Couch — Project Brief

## Purpose

Game Couch is a harness for letting AI companions enjoy games alongside humans in a “friend on the sofa / co-pilot” mode.

The harness is infrastructure, not a persona. Humans, Pip, and Coda should participate in Discord as themselves while the harness captures and routes game moments.

## MVP

- Local CLI/service starts a play session.
- Discord is the social room for the session.
- First plugin is `generic-screen`.
- A hotkey or CLI command captures a screenshot plus optional note/context.
- The moment posts to Discord as a structured bundle.
- The session is journaled locally.
- Plugin interface exists for later game-specific integrations.

## Design Principles

- Couch presence over assistant productivity.
- Player-triggered moments before constant watching.
- Cheap ambient context; rich analysis only when asked or interesting.
- Plugins make games feel native; core stays game-agnostic.
- Agents participate as themselves, not hidden behind one mascot bot.
- Game risks are acceptable in sandbox saves, but external services and privacy are not.

## Non-goals for v0

- No WoW-specific addon/API integration.
- No console capture-card workflow.
- No autonomous game control/wheel mode.
- No always-on vision/video stream.
- No synthetic merged “game companion” persona.
