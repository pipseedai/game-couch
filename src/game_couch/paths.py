from __future__ import annotations

from pathlib import Path
import os


def couch_home() -> Path:
    return Path(os.environ.get("GAME_COUCH_HOME", Path.home() / ".local" / "share" / "game-couch")).expanduser()


def sessions_dir(home: Path | None = None) -> Path:
    return (home or couch_home()) / "sessions"


def current_session_path(home: Path | None = None) -> Path:
    return (home or couch_home()) / "current-session.json"
