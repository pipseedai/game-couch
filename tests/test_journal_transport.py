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
