from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import os
import shlex
import shutil
import subprocess
from typing import Any, Protocol

from .models import utc_now_iso


@dataclass(slots=True)
class RunnerCaptureResult:
    operation: str
    host: str
    artifact_path: str
    media_type: str = "image/png"
    captured_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Runner(Protocol):
    name: str

    def capture_screenshot(self, destination: Path, *, trigger: str = "manual") -> RunnerCaptureResult:
        ...


class LocalRunner:
    name = "local"

    def capture_screenshot(self, destination: Path, *, trigger: str = "manual") -> RunnerCaptureResult:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if shutil.which("screencapture"):
            subprocess.run(["screencapture", "-x", str(destination)], check=True)
            return RunnerCaptureResult(
                operation="capture_screenshot",
                host=self.name,
                artifact_path=str(destination),
                metadata={"runner": self.name, "trigger": trigger, "command": "screencapture"},
            )
        raise RuntimeError("Local screenshot capture requires macOS screencapture; pass --screenshot or use --runner fake.")


class FakeRunner:
    name = "fake"

    def capture_screenshot(self, destination: Path, *, trigger: str = "manual") -> RunnerCaptureResult:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(b"fake-game-couch-screenshot\n")
        return RunnerCaptureResult(
            operation="capture_screenshot",
            host=self.name,
            artifact_path=str(destination),
            metadata={"runner": self.name, "trigger": trigger},
        )


ALLOWED_OPERATIONS = {"capture_screenshot"}


@dataclass(slots=True)
class SshRunnerConfig:
    name: str
    target: str
    remote_dir: str = "~/game-couch-captures"
    ssh_bin: str = "ssh"
    scp_bin: str = "scp"


def host_env_key(name: str, suffix: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in name.upper())
    return f"GAME_COUCH_HOST_{safe}_{suffix}"


def load_ssh_config(name: str) -> SshRunnerConfig:
    target = os.environ.get(host_env_key(name, "SSH"))
    if not target:
        raise RuntimeError(f"No SSH target configured for host '{name}'. Set {host_env_key(name, 'SSH')}.")
    return SshRunnerConfig(
        name=name,
        target=target,
        remote_dir=os.environ.get(host_env_key(name, "REMOTE_DIR"), "~/game-couch-captures"),
    )


class SshRunner:
    def __init__(self, config: SshRunnerConfig):
        self.config = config
        self.name = config.name

    def build_remote_capture_command(self, remote_path: str) -> list[str]:
        quoted_dir = shlex.quote(str(Path(remote_path).parent))
        quoted_path = shlex.quote(remote_path)
        # Allowlisted operation only: create dir and capture screenshot on the remote macOS host.
        return ["mkdir", "-p", quoted_dir, "&&", "screencapture", "-x", quoted_path]

    def build_ssh_command(self, remote_path: str) -> list[str]:
        remote_script = " ".join(self.build_remote_capture_command(remote_path))
        return [self.config.ssh_bin, self.config.target, remote_script]

    def build_scp_command(self, remote_path: str, destination: Path) -> list[str]:
        return [self.config.scp_bin, f"{self.config.target}:{remote_path}", str(destination)]

    def capture_screenshot(self, destination: Path, *, trigger: str = "manual") -> RunnerCaptureResult:
        operation = "capture_screenshot"
        if operation not in ALLOWED_OPERATIONS:
            raise RuntimeError(f"Operation not allowlisted: {operation}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        remote_path = f"{self.config.remote_dir.rstrip('/')}/{destination.name}"
        subprocess.run(self.build_ssh_command(remote_path), check=True)
        subprocess.run(self.build_scp_command(remote_path, destination), check=True)
        return RunnerCaptureResult(
            operation=operation,
            host=self.config.name,
            artifact_path=str(destination),
            metadata={
                "runner": "ssh",
                "target": self.config.target,
                "remote_path": remote_path,
                "trigger": trigger,
            },
        )


def make_runner(name: str | None = None, *, host: str | None = None) -> Runner:
    if host:
        return SshRunner(load_ssh_config(host))
    if not name or name == "local":
        return LocalRunner()
    if name == "fake":
        return FakeRunner()
    if name.startswith("ssh:"):
        return SshRunner(load_ssh_config(name.split(":", 1)[1]))
    raise ValueError(f"Unknown runner: {name}")
