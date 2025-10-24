"""Coleccion de modelos disponibles en la aplicacion."""

# TODO: exponer nuevos modelos cuando se creen.
from .movie import Movie  # noqa: F401
from .seasons import Season  # noqa: F401
from .series import Series  # noqa: F401
from .user import User  # noqa: F401
from .watch_entry import WatchEntry  # noqa: F401

__all__ = ["Movie", "Season", "Series", "User", "WatchEntry"]
