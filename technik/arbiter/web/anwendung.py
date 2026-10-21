"""Flask: liefert Frontend und Spielstand, nimmt Auswahl und Handlungen an (web.md; vertrag.md)."""

import json
import re
from fractions import Fraction
from http import HTTPStatus
from math import isfinite
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.sperre import Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.web.darstellung import spielstand, stellenBeimLoslassen, texteDerGründe
from arbiter.web.kennungen import (
    ablageNachNummer,
    einheitenNachNummer,
    modelleNachNummer,
    spielerNachNummer,
)

_frontend = Path(__file__).parents[2] / "frontend"
# Regel: vertrag.md, V4 (nur diese Hosts, gegen DNS-Rebinding)
_erlaubteHosts = ["127.0.0.1", "localhost"]
_jsonZahlText = re.compile(r"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?", re.ASCII)


def _zahl(körper: dict, name: str) -> Fraction:
    wert = körper.get(name)
    if isinstance(wert, bool) or not isinstance(wert, int | float):
        abort(HTTPStatus.BAD_REQUEST)
    # Warum: Die Seite rechnet in double; was dort nicht darstellbar ist, ist keine Zahl
    try:
        endlich = isfinite(float(wert))
    except OverflowError:
        endlich = False
    if not endlich:
        abort(HTTPStatus.BAD_REQUEST)
    # Regel: architektur.md, S2, die Dezimalzahl wie gesendet
    return Fraction(str(wert))


def _stelleDerAnfrage() -> Stelle:
    körper = request.get_json(silent=True)
    if not isinstance(körper, dict):
        abort(HTTPStatus.BAD_REQUEST)
    return Stelle(x=_zahl(körper, "x"), y=_zahl(körper, "y"))


def _jsonZahl(text: str | None) -> object:
    # Warum: Nur was JSON als Zahl schreibt (V5); float nähme auch "1_0" und " 3 "
    if text is None or not _jsonZahlText.fullmatch(text):
        return None
    try:
        return json.loads(text)
    except ValueError:
        # Warum: Python verweigert Ganzzahlen mit mehr als 4.300 Ziffern
        return None


def _stelleDerAbfrage() -> Stelle:
    # Regel: vertrag.md, V10, Zahlen wie V5; fehlt eine oder ist sie keine Zahl: 400
    angaben = {name: _jsonZahl(request.args.get(name)) for name in ("x", "y")}
    return Stelle(x=_zahl(angaben, "x"), y=_zahl(angaben, "y"))


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

    def ablageDerAnfrage() -> Spieler:
        ablage = request.args.get("ablage", type=int)
        if ablage is None:
            abort(HTTPStatus.BAD_REQUEST)
        return spielerMit(ablage)

    def einheitInDerAblage(spielernummer: int, einheitennummer: int) -> Einheit:
        spieler = spielerMit(spielernummer)
        einheit = ablageNachNummer(aufstellung, spieler).get(einheitennummer)
        if einheit is None:
            abort(HTTPStatus.NOT_FOUND)
        return einheit

    def einheitDerArmee(spielernummer: int, einheitennummer: int) -> Einheit:
        einheit = einheitenNachNummer(spielerMit(spielernummer)).get(einheitennummer)
        if einheit is None:
            abort(HTTPStatus.NOT_FOUND)
        return einheit

    def modellDerEinheit(einheit: Einheit, modellnummer: int) -> Modell:
        modell = modelleNachNummer(einheit).get(modellnummer)
        if modell is None:
            abort(HTTPStatus.NOT_FOUND)
        return modell

    def modellDerArmee(spielernummer: int, einheitennummer: int, modellnummer: int) -> Modell:
        return modellDerEinheit(einheitDerArmee(spielernummer, einheitennummer), modellnummer)

    def gesetztesModellDerAusgewählten(
        spielernummer: int, einheitennummer: int, modellnummer: int
    ) -> Modell:
        einheit = einheitDerArmee(spielernummer, einheitennummer)
        modell = modellDerEinheit(einheit, modellnummer)
        if not (aufstellung.ausgewählt(einheit) and aufstellung.gesetzt(modell)):
            abort(HTTPStatus.NOT_FOUND)
        return modell

    def modellAlsEbene(spielernummer: int, einheitennummer: int, modellnummer: int):
        aufstellung.ebeneWählen(
            gesetztesModellDerAusgewählten(spielernummer, einheitennummer, modellnummer)
        )
        return spielstandLiefern()

    def einheitAlsEbene(spielernummer: int, einheitennummer: int, modellnummer: int):
        aufstellung.ebeneAbwählen(
            gesetztesModellDerAusgewählten(spielernummer, einheitennummer, modellnummer)
        )
        return spielstandLiefern()

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

    def stelleBeimLoslassen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        abfrage = aufstellung.stellenBeimLoslassen(modell, _stelleDerAbfrage())
        return jsonify(stellenBeimLoslassen(aufstellung, abfrage))

    def modellAufAblageLoslassen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        aufstellung.modellAufAblageLoslassen(modell, ablageDerAnfrage())
        return spielstandLiefern()

    def karteAnklicken():
        aufstellung.karteAnklicken(_stelleDerAnfrage())
        return spielstandLiefern()

    def zurück():
        aufstellung.zurück()
        return spielstandLiefern()

    def aufstellenDerEinheitBeenden():
        aufstellung.aufstellenDerEinheitBeenden()
        return spielstandLiefern()

    def sperreMelden(sperre: Sperre):
        gründe = texteDerGründe(sperre.gründe)
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
    anwendung.add_url_rule(pfadDesModells, view_func=modellAufAblageLoslassen, methods=["DELETE"])
    pfadDerAbfrage = f"{pfadDerEinheit}/modelle/<int:modellnummer>/stelleBeimLoslassen"
    anwendung.add_url_rule(pfadDerAbfrage, view_func=stelleBeimLoslassen)
    pfadDerEbene = f"{pfadDerEinheit}/modelle/<int:modellnummer>/ebene"
    anwendung.add_url_rule(pfadDerEbene, view_func=modellAlsEbene, methods=["PUT"])
    anwendung.add_url_rule(pfadDerEbene, view_func=einheitAlsEbene, methods=["DELETE"])
    anwendung.add_url_rule("/api/karteAnklicken", view_func=karteAnklicken, methods=["PUT"])
    anwendung.add_url_rule("/api/zurück", view_func=zurück, methods=["PUT"])
    anwendung.add_url_rule(
        "/api/aufstellenDerEinheitBeenden", view_func=aufstellenDerEinheitBeenden, methods=["PUT"]
    )
    anwendung.register_error_handler(Sperre, sperreMelden)
    return anwendung
