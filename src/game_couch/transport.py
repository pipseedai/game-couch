from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
import json
import os
import urllib.request

from .models import MomentPayload, SessionContext


class Transport(ABC):
    @abstractmethod
    def send_moment(self, *, session: SessionContext, payload: MomentPayload) -> dict[str, Any]:
        """Send a moment bundle and return delivery metadata."""


class DryRunTransport(Transport):
    def __init__(self, outbox_path: Path | None = None):
        self.outbox_path = outbox_path

    def send_moment(self, *, session: SessionContext, payload: MomentPayload) -> dict[str, Any]:
        record = {"channel": session.channel, "payload": payload.to_dict()}
        if self.outbox_path:
            self.outbox_path.parent.mkdir(parents=True, exist_ok=True)
            with self.outbox_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        return {"transport": "dry-run", "delivered": False, "channel": session.channel, "outbox": str(self.outbox_path) if self.outbox_path else None}


class DiscordWebhookTransport(Transport):
    def __init__(self, webhook_url: str | None = None):
        self.webhook_url = webhook_url or os.environ.get("GAME_COUCH_DISCORD_WEBHOOK_URL") or os.environ.get("DISCORD_WEBHOOK_URL")
        if not self.webhook_url:
            raise RuntimeError("Discord transport requires GAME_COUCH_DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL")

    def send_moment(self, *, session: SessionContext, payload: MomentPayload) -> dict[str, Any]:
        body = {
            "content": format_discord_message(session=session, payload=payload),
            "allowed_mentions": {"parse": []},
        }
        request = urllib.request.Request(
            self.webhook_url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "game-couch/0.1"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=15) as response:  # noqa: S310 - user-configured Discord webhook
            status = response.getcode()
        return {"transport": "discord-webhook", "delivered": True, "channel": session.channel, "status": status}


def format_discord_message(*, session: SessionContext, payload: MomentPayload) -> str:
    lines = [
        f"🎮 **Game Couch moment** — `{payload.game_id}`",
        f"Session: `{payload.session_id}` | Player: **{payload.player_label}** | Trigger: `{payload.trigger}`",
        f"Time: {payload.timestamp}",
    ]
    if payload.note:
        lines.append(f"Note: {payload.note}")
    if payload.media_path:
        lines.append(f"Screenshot: `{payload.media_path}`")
    lines.append(f"Plugin context: ```json\n{json.dumps(payload.plugin_context, sort_keys=True)}\n```")
    return "\n".join(lines)


def make_transport(name: str, *, outbox_path: Path | None = None) -> Transport:
    if name == "dry-run":
        return DryRunTransport(outbox_path=outbox_path)
    if name == "discord":
        return DiscordWebhookTransport()
    raise ValueError("transport must be 'dry-run' or 'discord'")
