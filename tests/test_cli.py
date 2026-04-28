import json

from game_couch.cli import main


def test_cli_start_and_share_dry_run(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("GAME_COUCH_HOME", str(tmp_path / "home"))
    screenshot = tmp_path / "screen.png"
    screenshot.write_bytes(b"fake-png")

    assert main(["start", "--game", "generic-screen", "--channel", "#games", "--player-label", "Saff", "--json"]) == 0
    start_output = json.loads(capsys.readouterr().out)
    session = start_output["session"]

    assert session["game_id"] == "generic-screen"
    assert session["channel"] == "#games"
    assert session["player_label"] == "Saff"

    assert main(["share", "--note", "nice jump", "--screenshot", str(screenshot), "--transport", "dry-run", "--json"]) == 0
    share_output = json.loads(capsys.readouterr().out)

    assert share_output["payload"]["session_id"] == session["session_id"]
    assert share_output["payload"]["note"] == "nice jump"
    assert share_output["transport"]["transport"] == "dry-run"
    assert (tmp_path / "home" / "sessions" / session["session_id"] / "journal.jsonl").exists()
