from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from uuid import uuid4
import json
import mimetypes
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
        media_path = Path(payload.media_path).expanduser() if payload.media_path else None
        record = {
            "channel": session.channel,
            "payload": payload.to_dict(),
            "media": media_record(media_path),
            "message": format_discord_message(session=session, payload=payload),
        }
        if self.outbox_path:
            self.outbox_path.parent.mkdir(parents=True, exist_ok=True)
            with self.outbox_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        return {
            "transport": "dry-run",
            "delivered": False,
            "channel": session.channel,
            "outbox": str(self.outbox_path) if self.outbox_path else None,
            "media": record["media"],
        }


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
        media_path = Path(payload.media_path).expanduser() if payload.media_path else None
        media = media_record(media_path)
        if media_path and media_path.exists():
            data, content_type = encode_multipart_payload(body=body, media_path=media_path)
        else:
            data = json.dumps(body).encode("utf-8")
            content_type = "application/json"
        request = urllib.request.Request(
            self.webhook_url,
            data=data,
            headers={"Content-Type": content_type, "User-Agent": "game-couch/0.1"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=15) as response:  # noqa: S310 - user-configured Discord webhook
            status = response.getcode()
        return {"transport": "discord-webhook", "delivered": True, "channel": session.channel, "status": status, "media": media}


def media_record(media_path: Path | None) -> dict[str, Any] | None:
    if not media_path:
        return None
    return {
        "path": str(media_path),
        "filename": media_path.name,
        "exists": media_path.exists(),
        "content_type": mimetypes.guess_type(media_path.name)[0] or "application/octet-stream",
    }


def encode_multipart_payload(*, body: dict[str, Any], media_path: Path) -> tuple[bytes, str]:
    boundary = f"game-couch-{uuid4().hex}"
    content_type = mimetypes.guess_type(media_path.name)[0] or "application/octet-stream"
    parts: list[bytes] = []

    def add_field(name: str, value: bytes, *, filename: str | None = None, field_content_type: str | None = None) -> None:
        disposition = f'form-data; name="{name}"'
        if filename:
            disposition += f'; filename="{filename}"'
        headers = [f"--{boundary}", f"Content-Disposition: {disposition}"]
        if field_content_type:
            headers.append(f"Content-Type: {field_content_type}")
        parts.append(("\r\n".join(headers) + "\r\n\r\n").encode("utf-8") + value + b"\r\n")

    add_field("payload_json", json.dumps(body).encode("utf-8"), field_content_type="application/json")
    add_field("files[0]", media_path.read_bytes(), filename=media_path.name, field_content_type=content_type)
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


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
