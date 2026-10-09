"""Flask: liefert Frontend und Spielstand, nimmt die Auswahl an (web.md, W1, W2; vertrag.md, V2)."""

from http import HTTPStatus
from pathlib import Path

from flask import Flask, abort, jsonify, send_from_directory

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.spielobjekte import Einheit
from arbiter.web.darstellung import spielstand
from arbiter.web.kennungen import ablageNachNummer, spielerNachNummer

_frontend = Path(__file__).parents[2] / "frontend"
# Regel: vertrag.md, V4 (nur diese Hosts, gegen DNS-Rebinding)
_erlaubteHosts = ["127.0.0.1", "localhost"]


def anwendungFür(aufstellung: Aufstellung) -> Flask:
    anwendung = Flask(__name__, static_folder=_frontend, static_url_path="")
    anwendung.config["TRUSTED_HOSTS"] = _erlaubteHosts

    def startseite():
        return send_from_directory(_frontend, "index.html")

    def spielstandLiefern():
        return jsonify(spielstand(aufstellung))

    def einheitInDerAblage(spielernummer: int, einheitennummer: int) -> Einheit:
        spieler = spielerNachNummer(aufstellung).get(spielernummer)
        if spieler is None:
            abort(HTTPStatus.NOT_FOUND)
        einheit = ablageNachNummer(aufstellung, spieler).get(einheitennummer)
        if einheit is None:
            abort(HTTPStatus.NOT_FOUND)
        return einheit

    def einheitAuswählen(spielernummer: int, einheitennummer: int):
        aufstellung.auswählen(einheitInDerAblage(spielernummer, einheitennummer))
        return spielstandLiefern()

    def einheitAbwählen(spielernummer: int, einheitennummer: int):
        aufstellung.abwählen(einheitInDerAblage(spielernummer, einheitennummer))
        return spielstandLiefern()

    pfadDerAuswahl = "/api/spieler/<int:spielernummer>/einheiten/<int:einheitennummer>/ausgewählt"
    anwendung.add_url_rule("/", view_func=startseite)
    anwendung.add_url_rule("/api/spielstand", view_func=spielstandLiefern)
    anwendung.add_url_rule(pfadDerAuswahl, view_func=einheitAuswählen, methods=["PUT"])
    anwendung.add_url_rule(pfadDerAuswahl, view_func=einheitAbwählen, methods=["DELETE"])
    return anwendung
