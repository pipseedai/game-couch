from __future__ import annotations

from pathlib import Path
import json
from typing import Any

from .models import MomentPayload, SessionContext


class Journal:
    def __init__(self, session: SessionContext):
        if not session.journal_path:
            raise ValueError("session.journal_path is required")
        self.path = Path(session.journal_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, kind: str, data: dict[str, Any]) -> None:
        record = {"kind": kind, "data": data}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def append_session_started(self, session: SessionContext, reused: bool) -> None:
        self.append("session.started", {**session.to_dict(), "reused": reused})

    def append_moment(self, payload: MomentPayload, transport_result: dict[str, Any]) -> None:
        self.append("moment.shared", {"payload": payload.to_dict(), "transport": transport_result})
