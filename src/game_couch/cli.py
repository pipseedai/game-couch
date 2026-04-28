from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

from .plugins.registry import available_plugins
from .service import share_moment, start_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="game-couch", description="Share player-triggered game moments into a couch session.")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Create or reuse a play session context.")
    start.add_argument("--game", required=True, choices=available_plugins())
    start.add_argument("--channel", required=True, help="Discord channel/thread target label or id.")
    start.add_argument("--player-label", default="Player")
    start.add_argument("--new", action="store_true", help="Force a new session instead of reusing the current matching one.")
    start.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    share = sub.add_parser("share", help="Capture or send a manual moment bundle.")
    share.add_argument("--note", default=None)
    share.add_argument("--screenshot", type=Path, default=None, help="Existing screenshot/media path. If omitted, generic-screen tries local capture.")
    share.add_argument("--trigger", default="manual")
    share.add_argument("--transport", choices=["dry-run", "discord"], default="dry-run")
    share.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    sub.add_parser("plugins", help="List available game plugins.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            session, reused, plugin_context = start_session(
                game_id=args.game,
                channel=args.channel,
                player_label=args.player_label,
                force_new=args.new,
            )
            output = {"session": session.to_dict(), "reused": reused, "plugin_context": plugin_context}
            if args.json:
                print(json.dumps(output, indent=2, sort_keys=True))
            else:
                verb = "Reusing" if reused else "Started"
                print(f"{verb} Game Couch session {session.session_id} for {session.game_id} in {session.channel}")
                print(f"Journal: {session.journal_path}")
            return 0
        if args.command == "share":
            session, payload, result = share_moment(
                note=args.note,
                screenshot=args.screenshot,
                trigger=args.trigger,
                transport_name=args.transport,
            )
            output = {"session": session.to_dict(), "payload": payload, "transport": result}
            if args.json:
                print(json.dumps(output, indent=2, sort_keys=True))
            else:
                print(f"Shared moment for session {session.session_id} via {result['transport']}")
                print(f"Journal: {session.journal_path}")
            return 0
        if args.command == "plugins":
            for plugin in available_plugins():
                print(plugin)
            return 0
    except Exception as exc:  # CLI boundary
        print(f"game-couch: error: {exc}", file=sys.stderr)
        return 1
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
