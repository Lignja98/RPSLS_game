"""Game service application package."""

# Re-export this package under the top-level name ``app`` so that
# absolute imports like ``import app.core.config`` keep working even when
# the project is executed with ``python -m uvicorn services.game.app.main:app``
# (i.e. without installing the package or adding it to PYTHONPATH).
import sys as _sys

_sys.modules.setdefault("app", _sys.modules[__name__])
