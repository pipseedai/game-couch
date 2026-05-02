import json
from pathlib import Path

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

def test_cli_start_with_host_and_share_fake_runner(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("GAME_COUCH_HOME", str(tmp_path / "home"))

    assert main([
        "start",
        "--game", "generic-screen",
        "--channel", "#games",
        "--player-label", "Saff",
        "--host", "bigchoof",
        "--json",
    ]) == 0
    start_output = json.loads(capsys.readouterr().out)
    session = start_output["session"]
    assert session["host"] == "bigchoof"

    assert main(["share", "--note", "remote-ish", "--runner", "fake", "--transport", "dry-run", "--json"]) == 0
    share_output = json.loads(capsys.readouterr().out)
    runner = share_output["payload"]["plugin_context"]["runner"]
    assert runner["operation"] == "capture_screenshot"
    assert runner["host"] == "fake"
    assert Path(runner["artifact_path"]).exists()

