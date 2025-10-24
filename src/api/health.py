"""Endpoints de verificacion rapida de la API."""

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__, url_prefix="/health")


@bp.get("/")
def healthcheck() -> tuple[dict[str, str], int]:
    """Devuelve el estado actual de la aplicacion."""
    # TODO: agregar comprobaciones reales (db, cache, servicios externos).
    return jsonify({"status": "ok"}), 200
