"""Configuracion general de la aplicacion Flask."""

from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from .extensions import db, migrate


def create_app(config_object: type[DevelopmentConfig] = DevelopmentConfig) -> Flask:
    """Crea y configura la aplicacion utilizando application factory."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    CORS(app)

    return app


def register_extensions(app: Flask) -> None:
    """Inicializa extensiones de terceros."""
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask) -> None:
    """Registra los blueprints del proyecto."""
    from .api import register_api_blueprints

    register_api_blueprints(app)
