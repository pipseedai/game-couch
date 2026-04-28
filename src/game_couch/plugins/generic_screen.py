from __future__ import annotations

from pathlib import Path
import platform
import shutil
import subprocess
from typing import Any

from game_couch.models import SessionContext
from game_couch.plugins.base import GamePlugin


class GenericScreenPlugin(GamePlugin):
    game_id = "generic-screen"

    def start_context(self, session: SessionContext) -> dict[str, Any]:
        return {
            "plugin": self.game_id,
            "mode": "manual-screen-moments",
            "capture": "screenshot-path-or-local-screencapture",
            "channel": session.channel,
        }

    def capture_moment_context(self, *, session: SessionContext, screenshot_path: Path | None) -> dict[str, Any]:
        return {
            "plugin": self.game_id,
            "source": "generic desktop screen",
            "screenshot_provided": screenshot_path is not None,
            "screenshot_filename": screenshot_path.name if screenshot_path else None,
        }

    def capture_screenshot(self, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if platform.system() == "Darwin" and shutil.which("screencapture"):
            subprocess.run(["screencapture", "-x", str(destination)], check=True)
            return destination
        raise RuntimeError(
            "Automatic screenshot capture is only implemented for macOS with screencapture; "
            "pass --screenshot instead."
        )
