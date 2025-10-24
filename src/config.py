"""Configuraciones base para los distintos entornos."""

from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_PATH = BASE_DIR / "instance"


class BaseConfig:
    """Config comun a cualquier entorno."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{INSTANCE_PATH / 'app.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    """Config pensada para desarrollo local."""

    DEBUG = True


class TestingConfig(BaseConfig):
    """Config utilizada al ejecutar tests automaticos."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    """Config preparada para despliegues en produccion."""

    DEBUG = False
    TESTING = False
