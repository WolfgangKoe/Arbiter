from flask import Blueprint

bp = Blueprint("main", __name__)


@bp.route("/")
def index() -> str:
    return "Arbiter läuft."
