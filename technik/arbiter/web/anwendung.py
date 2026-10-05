"""Flask: liefert die Dateien des Frontends und den Spielstand als JSON (web.md, W1, W2)."""

from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.web.darstellung import spielstand

_frontend = Path(__file__).parents[2] / "frontend"


def anwendungFür(aufstellung: Aufstellung) -> Flask:
    anwendung = Flask(__name__, static_folder=_frontend, static_url_path="")

    def startseite():
        return send_from_directory(_frontend, "index.html")

    def spielstandLiefern():
        return jsonify(spielstand(aufstellung))

    anwendung.add_url_rule("/", view_func=startseite)
    anwendung.add_url_rule("/api/spielstand", view_func=spielstandLiefern)
    return anwendung
