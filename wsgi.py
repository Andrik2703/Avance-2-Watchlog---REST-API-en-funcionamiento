"""Punto de entrada WSGI para servidores como Gunicorn."""

from src import create_app
from src.config import ProductionConfig

app = create_app(ProductionConfig)
