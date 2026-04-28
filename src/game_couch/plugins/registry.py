from __future__ import annotations

from game_couch.plugins.base import GamePlugin
from game_couch.plugins.generic_screen import GenericScreenPlugin

_PLUGINS: dict[str, type[GamePlugin]] = {
    GenericScreenPlugin.game_id: GenericScreenPlugin,
}


def load_plugin(game_id: str) -> GamePlugin:
    try:
        return _PLUGINS[game_id]()
    except KeyError as exc:
        known = ", ".join(sorted(_PLUGINS))
        raise ValueError(f"Unknown game plugin '{game_id}'. Known plugins: {known}") from exc


def available_plugins() -> list[str]:
    return sorted(_PLUGINS)
