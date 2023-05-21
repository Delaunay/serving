import serving.plugins
from serving.core import discover_plugins


def test_plugins():
    plugins = discover_plugins(serving.plugins)

    assert len(plugins) == 1
