from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import uuid


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def new_session_id(game_id: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{game_id}-{stamp}-{uuid.uuid4().hex[:8]}"


@dataclass(slots=True)
class SessionContext:
    session_id: str
    game_id: str
    channel: str
    player_label: str = "Player"
    host: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    journal_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionContext":
        return cls(**data)


@dataclass(slots=True)
class MomentPayload:
    session_id: str
    game_id: str
    player_label: str
    trigger: str
    timestamp: str
    note: str | None
    screenshot_path: str | None
    media_path: str | None
    plugin_context: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def shape_moment_payload(
    *,
    session: SessionContext,
    trigger: str,
    note: str | None,
    screenshot_path: str | Path | None,
    plugin_context: dict[str, Any],
    timestamp: str | None = None,
) -> MomentPayload:
    media_path = str(screenshot_path) if screenshot_path else None
    return MomentPayload(
        session_id=session.session_id,
        game_id=session.game_id,
        player_label=session.player_label,
        trigger=trigger,
        timestamp=timestamp or utc_now_iso(),
        note=note,
        screenshot_path=media_path,
        media_path=media_path,
        plugin_context=plugin_context,
    )
