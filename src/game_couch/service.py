from __future__ import annotations

from pathlib import Path
import json

from .journal import Journal
from .models import SessionContext, new_session_id, shape_moment_payload
from .paths import couch_home, current_session_path, sessions_dir
from .plugins.registry import load_plugin
from .transport import make_transport


def start_session(
    *,
    game_id: str,
    channel: str,
    player_label: str = "Player",
    home: Path | None = None,
    force_new: bool = False,
) -> tuple[SessionContext, bool, dict]:
    home = home or couch_home()
    current_path = current_session_path(home)
    if not force_new and current_path.exists():
        current = SessionContext.from_dict(json.loads(current_path.read_text(encoding="utf-8")))
        if current.game_id == game_id and current.channel == channel and current.player_label == player_label:
            plugin_context = load_plugin(game_id).start_context(current)
            Journal(current).append_session_started(current, reused=True)
            return current, True, plugin_context

    session_id = new_session_id(game_id)
    session_dir = sessions_dir(home) / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    session = SessionContext(
        session_id=session_id,
        game_id=game_id,
        channel=channel,
        player_label=player_label,
        journal_path=str(session_dir / "journal.jsonl"),
    )
    plugin_context = load_plugin(game_id).start_context(session)
    (session_dir / "session.json").write_text(json.dumps(session.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    current_path.parent.mkdir(parents=True, exist_ok=True)
    current_path.write_text(json.dumps(session.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    Journal(session).append_session_started(session, reused=False)
    return session, False, plugin_context


def load_current_session(*, home: Path | None = None) -> SessionContext:
    path = current_session_path(home or couch_home())
    if not path.exists():
        raise RuntimeError("No active Game Couch session. Run 'game-couch start --game generic-screen --channel <target>' first.")
    return SessionContext.from_dict(json.loads(path.read_text(encoding="utf-8")))


def share_moment(
    *,
    note: str | None,
    screenshot: Path | None,
    trigger: str = "manual",
    transport_name: str = "dry-run",
    home: Path | None = None,
) -> tuple[SessionContext, dict, dict]:
    home = home or couch_home()
    session = load_current_session(home=home)
    plugin = load_plugin(session.game_id)

    screenshot_path = screenshot
    if screenshot_path is None:
        captures_dir = sessions_dir(home) / session.session_id / "captures"
        screenshot_path = plugin.capture_screenshot(captures_dir / f"{trigger}.png")
    else:
        screenshot_path = screenshot_path.expanduser().resolve()
        if not screenshot_path.exists():
            raise FileNotFoundError(f"Screenshot does not exist: {screenshot_path}")

    plugin_context = plugin.capture_moment_context(session=session, screenshot_path=screenshot_path)
    payload = shape_moment_payload(
        session=session,
        trigger=trigger,
        note=note,
        screenshot_path=screenshot_path,
        plugin_context=plugin_context,
    )
    outbox_path = sessions_dir(home) / session.session_id / "dry-run-outbox.jsonl"
    transport = make_transport(transport_name, outbox_path=outbox_path)
    result = transport.send_moment(session=session, payload=payload)
    Journal(session).append_moment(payload, result)
    return session, payload.to_dict(), result
