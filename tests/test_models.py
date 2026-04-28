from game_couch.models import SessionContext, shape_moment_payload


def test_moment_payload_shape_contains_required_fields():
    session = SessionContext(session_id="s1", game_id="generic-screen", channel="#games", player_label="Saff")
    payload = shape_moment_payload(
        session=session,
        trigger="manual",
        note="look at this",
        screenshot_path="/tmp/screen.png",
        plugin_context={"plugin": "generic-screen"},
        timestamp="2026-04-28T21:00:00Z",
    ).to_dict()

    assert payload == {
        "session_id": "s1",
        "game_id": "generic-screen",
        "player_label": "Saff",
        "trigger": "manual",
        "timestamp": "2026-04-28T21:00:00Z",
        "note": "look at this",
        "screenshot_path": "/tmp/screen.png",
        "media_path": "/tmp/screen.png",
        "plugin_context": {"plugin": "generic-screen"},
    }
