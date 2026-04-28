from game_couch.models import SessionContext
from game_couch.plugins.registry import available_plugins, load_plugin


def test_loads_generic_screen_plugin():
    plugin = load_plugin("generic-screen")
    session = SessionContext(session_id="s1", game_id="generic-screen", channel="#games")

    assert "generic-screen" in available_plugins()
    assert plugin.game_id == "generic-screen"
    assert plugin.start_context(session)["mode"] == "manual-screen-moments"
