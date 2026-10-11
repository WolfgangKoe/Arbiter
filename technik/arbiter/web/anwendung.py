"""Flask: liefert Frontend und Spielstand, nimmt Auswahl und Handlungen an (web.md; vertrag.md)."""

from fractions import Fraction
from http import HTTPStatus
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Grund, Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.web.darstellung import spielstand
from arbiter.web.kennungen import (
    ablageNachNummer,
    einheitenNachNummer,
    modelleNachNummer,
    spielerNachNummer,
)

_frontend = Path(__file__).parents[2] / "frontend"
# Regel: vertrag.md, V4 (nur diese Hosts, gegen DNS-Rebinding)
_erlaubteHosts = ["127.0.0.1", "localhost"]


def _zahl(körper: dict, name: str) -> Fraction:
    wert = körper.get(name)
    if isinstance(wert, bool) or not isinstance(wert, int | float):
        abort(HTTPStatus.BAD_REQUEST)
    # Regel: architektur.md, S2, die Dezimalzahl wie gesendet
    return Fraction(str(wert))


def _stelleDerAnfrage() -> Stelle:
    körper = request.get_json(silent=True)
    if not isinstance(körper, dict):
        abort(HTTPStatus.BAD_REQUEST)
    return Stelle(x=_zahl(körper, "x"), y=_zahl(körper, "y"))


def anwendungFür(aufstellung: Aufstellung) -> Flask:
    anwendung = Flask(__name__, static_folder=_frontend, static_url_path="")
    anwendung.config["TRUSTED_HOSTS"] = _erlaubteHosts

    def startseite():
        return send_from_directory(_frontend, "index.html")

    def spielstandLiefern():
        return jsonify(spielstand(aufstellung))

    def spielerMit(spielernummer: int) -> Spieler:
        spieler = spielerNachNummer(aufstellung).get(spielernummer)
        if spieler is None:
            abort(HTTPStatus.NOT_FOUND)
        return spieler

    def einheitInDerAblage(spielernummer: int, einheitennummer: int) -> Einheit:
        spieler = spielerMit(spielernummer)
        einheit = ablageNachNummer(aufstellung, spieler).get(einheitennummer)
        if einheit is None:
            abort(HTTPStatus.NOT_FOUND)
        return einheit

    def modellDerArmee(spielernummer: int, einheitennummer: int, modellnummer: int) -> Modell:
        einheit = einheitenNachNummer(spielerMit(spielernummer)).get(einheitennummer)
        modell = modelleNachNummer(einheit).get(modellnummer) if einheit else None
        if modell is None:
            abort(HTTPStatus.NOT_FOUND)
        return modell

    def einheitAuswählen(spielernummer: int, einheitennummer: int):
        aufstellung.auswählen(einheitInDerAblage(spielernummer, einheitennummer))
        return spielstandLiefern()

    def einheitAbwählen(spielernummer: int, einheitennummer: int):
        aufstellung.abwählen(einheitInDerAblage(spielernummer, einheitennummer))
        return spielstandLiefern()

    def modellLoslassen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        aufstellung.modellLoslassen(modell, _stelleDerAnfrage())
        return spielstandLiefern()

    def modellZurücklegen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        ablage = request.args.get("ablage", type=int)
        if ablage is None:
            abort(HTTPStatus.BAD_REQUEST)
        aufstellung.modellZurücklegen(modell, spielerMit(ablage))
        return spielstandLiefern()

    def einheitLoslassen(spielernummer: int, einheitennummer: int):
        einheit = einheitInDerAblage(spielernummer, einheitennummer)
        aufstellung.einheitLoslassen(einheit, _stelleDerAnfrage())
        return spielstandLiefern()

    def zurück():
        aufstellung.zurück()
        return spielstandLiefern()

    def aufstellenDerEinheitBeenden():
        aufstellung.aufstellenDerEinheitBeenden()
        return spielstandLiefern()

    def sperreMelden(sperre: Sperre):
        gründe = [grund.value for grund in Grund if grund in sperre.gründe]
        antwort = jsonify({"gründe": gründe, "spielstand": spielstand(aufstellung)})
        antwort.status_code = HTTPStatus.CONFLICT
        return antwort

    pfadDerEinheit = "/api/spieler/<int:spielernummer>/einheiten/<int:einheitennummer>"
    pfadDesModells = f"{pfadDerEinheit}/modelle/<int:modellnummer>/stelle"
    anwendung.add_url_rule("/", view_func=startseite)
    anwendung.add_url_rule("/api/spielstand", view_func=spielstandLiefern)
    pfadDerAuswahl = f"{pfadDerEinheit}/ausgewählt"
    anwendung.add_url_rule(pfadDerAuswahl, view_func=einheitAuswählen, methods=["PUT"])
    anwendung.add_url_rule(pfadDerAuswahl, view_func=einheitAbwählen, methods=["DELETE"])
    anwendung.add_url_rule(pfadDesModells, view_func=modellLoslassen, methods=["PUT"])
    anwendung.add_url_rule(pfadDesModells, view_func=modellZurücklegen, methods=["DELETE"])
    anwendung.add_url_rule(f"{pfadDerEinheit}/stelle", view_func=einheitLoslassen, methods=["PUT"])
    anwendung.add_url_rule("/api/zurück", view_func=zurück, methods=["PUT"])
    anwendung.add_url_rule(
        "/api/aufstellenDerEinheitBeenden", view_func=aufstellenDerEinheitBeenden, methods=["PUT"]
    )
    anwendung.register_error_handler(Sperre, sperreMelden)
    return anwendung
