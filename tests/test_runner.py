from pathlib import Path

import pytest

from game_couch.runner import FakeRunner, SshRunner, SshRunnerConfig, host_env_key, make_runner


def test_fake_runner_writes_artifact(tmp_path):
    dest = tmp_path / "screen.png"
    result = FakeRunner().capture_screenshot(dest, trigger="manual")
    assert dest.exists()
    assert result.operation == "capture_screenshot"
    assert result.host == "fake"
    assert result.metadata["trigger"] == "manual"


def test_ssh_runner_builds_allowlisted_commands_without_live_ssh(tmp_path):
    runner = SshRunner(SshRunnerConfig(name="bigchoof", target="saff@bigchoof", remote_dir="~/gc"))
    remote = "~/gc/moment.png"
    assert runner.build_ssh_command(remote) == [
        "ssh",
        "saff@bigchoof",
        "mkdir -p '~/gc' && screencapture -x '~/gc/moment.png'",
    ]
    assert runner.build_scp_command(remote, tmp_path / "moment.png") == [
        "scp",
        "saff@bigchoof:~/gc/moment.png",
        str(tmp_path / "moment.png"),
    ]


def test_make_runner_requires_named_host_config(monkeypatch):
    monkeypatch.delenv(host_env_key("bigchoof", "SSH"), raising=False)
    with pytest.raises(RuntimeError, match="No SSH target configured"):
        make_runner(host="bigchoof")


def test_make_runner_loads_named_host_from_env(monkeypatch):
    monkeypatch.setenv(host_env_key("bigchoof", "SSH"), "saff@bigchoof")
    monkeypatch.setenv(host_env_key("bigchoof", "REMOTE_DIR"), "~/captures")
    runner = make_runner(host="bigchoof")
    assert isinstance(runner, SshRunner)
    assert runner.config.target == "saff@bigchoof"
    assert runner.config.remote_dir == "~/captures"
