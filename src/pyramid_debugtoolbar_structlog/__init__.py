"""Add a panel for ``structlog`` to the Pyramid DebugToolbar."""
from .panels.structlog_ import StructLogDebugPanel

__version__ = "0.1.0.dev0"


def includeme(config):
    config.add_debugtoolbar_panel(StructLogDebugPanel)
