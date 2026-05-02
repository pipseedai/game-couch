import json

from game_couch.journal import Journal
from game_couch.models import SessionContext, shape_moment_payload
from game_couch.transport import DryRunTransport


def test_journal_writes_jsonl_and_dry_run_transport_records_outbox(tmp_path):
    session = SessionContext(
        session_id="s1",
        game_id="generic-screen",
        channel="#games",
        journal_path=str(tmp_path / "journal.jsonl"),
    )
    payload = shape_moment_payload(
        session=session,
        trigger="manual",
        note=None,
        screenshot_path=tmp_path / "screen.png",
        plugin_context={"plugin": "generic-screen"},
        timestamp="2026-04-28T21:00:00Z",
    )
    outbox = tmp_path / "outbox.jsonl"

    result = DryRunTransport(outbox).send_moment(session=session, payload=payload)
    Journal(session).append_moment(payload, result)

    outbox_record = json.loads(outbox.read_text().splitlines()[0])
    journal_record = json.loads((tmp_path / "journal.jsonl").read_text().splitlines()[0])

    assert result["transport"] == "dry-run"
    assert result["delivered"] is False
    assert outbox_record["payload"]["session_id"] == "s1"
    assert journal_record["kind"] == "moment.shared"
    assert journal_record["data"]["payload"]["game_id"] == "generic-screen"

from game_couch.transport import encode_multipart_payload, format_discord_message


def test_dry_run_transport_records_media_and_safe_message(tmp_path):
    screenshot = tmp_path / "moment.png"
    screenshot.write_bytes(b"fake-png")
    session = SessionContext(
        session_id="s2",
        game_id="generic-screen",
        channel="#games",
        player_label="Saff",
        journal_path=str(tmp_path / "journal.jsonl"),
    )
    payload = shape_moment_payload(
        session=session,
        trigger="manual",
        note="look @everyone no ping",
        screenshot_path=screenshot,
        plugin_context={"plugin": "generic-screen"},
        timestamp="2026-04-28T21:00:00Z",
    )
    outbox = tmp_path / "outbox.jsonl"

    result = DryRunTransport(outbox).send_moment(session=session, payload=payload)
    outbox_record = json.loads(outbox.read_text().splitlines()[0])

    assert result["media"] == {
        "path": str(screenshot),
        "filename": "moment.png",
        "exists": True,
        "content_type": "image/png",
    }
    assert outbox_record["media"]["filename"] == "moment.png"
    assert "Player: **Saff**" in outbox_record["message"]
    assert "Trigger: `manual`" in outbox_record["message"]
    assert "look @everyone no ping" in outbox_record["message"]


def test_format_discord_message_contains_required_metadata(tmp_path):
    session = SessionContext(session_id="s3", game_id="generic-screen", channel="#games", player_label="Saff")
    payload = shape_moment_payload(
        session=session,
        trigger="hotkey",
        note="boss down",
        screenshot_path=tmp_path / "boss.png",
        plugin_context={"plugin": "generic-screen"},
        timestamp="2026-04-28T21:00:00Z",
    )
    text = format_discord_message(session=session, payload=payload)
    assert "generic-screen" in text
    assert "s3" in text
    assert "Saff" in text
    assert "hotkey" in text
    assert "2026-04-28T21:00:00Z" in text
    assert "boss down" in text


def test_multipart_payload_includes_json_and_media(tmp_path):
    screenshot = tmp_path / "moment.png"
    screenshot.write_bytes(b"fake-png")
    body = {"content": "hello", "allowed_mentions": {"parse": []}}

    data, content_type = encode_multipart_payload(body=body, media_path=screenshot)

    assert content_type.startswith("multipart/form-data; boundary=game-couch-")
    assert b'name="payload_json"' in data
    assert b'"allowed_mentions": {"parse": []}' in data
    assert b'name="files[0]"; filename="moment.png"' in data
    assert b"fake-png" in data
