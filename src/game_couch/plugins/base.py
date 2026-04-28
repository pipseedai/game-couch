from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from game_couch.models import SessionContext


class GamePlugin(ABC):
    """Interface implemented by game-specific context providers."""

    game_id: str

    @abstractmethod
    def start_context(self, session: SessionContext) -> dict[str, Any]:
        """Return lightweight context saved when a session starts."""

    @abstractmethod
    def capture_moment_context(self, *, session: SessionContext, screenshot_path: Path | None) -> dict[str, Any]:
        """Return plugin-specific context for a player-triggered moment."""

    def capture_screenshot(self, destination: Path) -> Path:
        """Capture a screenshot into destination, if supported by the plugin/environment."""
        raise NotImplementedError(f"{self.game_id} does not support automatic screenshot capture here")
