"""Flask: liefert Frontend und Spielstand, nimmt Auswahl und Handlungen an (web.md; vertrag/)."""

import json
import re
from fractions import Fraction
from http import HTTPStatus
from math import isfinite
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.querschnitt.schlachtrunden import Phase, Schlacht
from arbiter.domaene.sperre import Sperre
from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler, Stelle
from arbiter.web.darstellung import spielstand, stellenBeimLoslassen, texteDerGründe
from arbiter.web.kennungen import (
    armeelisteNachNummer,
    einheitenNachNummer,
    modelleNachNummer,
    nummerDesSpielers,
    spielerNachNummer,
)

_frontend = Path(__file__).parents[2] / "frontend"
_erlaubteHosts = ["127.0.0.1", "localhost"]
_größterNenner = 10**6
_jsonZahlText = re.compile(r"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?", re.ASCII)


def _zahl(körper: dict, name: str) -> Fraction:
    wert = körper.get(name)
    if isinstance(wert, bool) or not isinstance(wert, int | float):
        abort(HTTPStatus.BAD_REQUEST)
    try:
        endlich = isfinite(float(wert))
    except OverflowError:
        endlich = False
    if not endlich:
        abort(HTTPStatus.BAD_REQUEST)
    return Fraction(str(wert)).limit_denominator(_größterNenner)


def _stelleDerAnfrage() -> Stelle:
    körper = request.get_json(silent=True)
    if not isinstance(körper, dict):
        abort(HTTPStatus.BAD_REQUEST)
    return Stelle(x=_zahl(körper, "x"), y=_zahl(körper, "y"))


def _jsonZahl(text: str | None) -> object:
    if text is None or not _jsonZahlText.fullmatch(text):
        return None
    try:
        return json.loads(text)
    except ValueError:
        return None


def _stelleDerAbfrage() -> Stelle:
    angaben = {name: _jsonZahl(request.args.get(name)) for name in ("x", "y")}
    return Stelle(x=_zahl(angaben, "x"), y=_zahl(angaben, "y"))


def _ganzeZahl(körper: dict, name: str) -> int:
    wert = körper.get(name)
    if isinstance(wert, bool) or not isinstance(wert, int):
        abort(HTTPStatus.BAD_REQUEST)
    return wert


def _phaseDerAnfrage(körper: dict) -> Phase:
    try:
        return Phase(körper.get("phase"))
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST)


class _SchlachtDerAnwendung:
    """Hält die Schlacht und baut sie beim ersten Bedarf nach der Aufstellung (Schlacht, V11)."""

    def __init__(self, aufstellung: Aufstellung, schlacht: Schlacht | None) -> None:
        self._aufstellung = aufstellung
        self._schlacht = schlacht

    def laufende(self) -> Schlacht | None:
        if self._schlacht is None and self._aufstellung.beendet:
            self._schlacht = Schlacht(self._aufstellung)
        return self._schlacht

    def laufendeOder404(self) -> Schlacht:
        schlacht = self.laufende()
        if schlacht is None:
            abort(HTTPStatus.NOT_FOUND)
        return schlacht


def _phaseBeenden(schlacht: Schlacht, aufstellung: Aufstellung) -> None:
    """Beendet die Phase nur, wenn der Körper die laufende nennt (V13)."""
    körper = request.get_json(silent=True)
    if not isinstance(körper, dict):
        abort(HTTPStatus.BAD_REQUEST)
    gesehen = (
        _ganzeZahl(körper, "schlachtrunde"),
        _ganzeZahl(körper, "spieler"),
        _phaseDerAnfrage(körper),
    )
    laufende = (
        schlacht.schlachtrunde,
        nummerDesSpielers(aufstellung, schlacht.amZug),
        schlacht.phase,
    )
    if gesehen == laufende:
        schlacht.phaseBeenden()


def anwendungFür(aufstellung: Aufstellung, schlacht: Schlacht | None = None) -> Flask:
    anwendung = Flask(__name__, static_folder=_frontend, static_url_path="")
    anwendung.config["TRUSTED_HOSTS"] = _erlaubteHosts
    schlachtDerAnwendung = _SchlachtDerAnwendung(aufstellung, schlacht)
    laufendeSchlacht = schlachtDerAnwendung.laufende

    def spiel() -> Aufstellung | Schlacht:
        return laufendeSchlacht() or aufstellung

    schlachtOder404 = schlachtDerAnwendung.laufendeOder404

    def startseite():
        return send_from_directory(_frontend, "index.html")

    def spielstandLiefern():
        return jsonify(spielstand(aufstellung, laufendeSchlacht()))

    def spielerMit(spielernummer: int) -> Spieler:
        spieler = spielerNachNummer(aufstellung).get(spielernummer)
        if spieler is None:
            abort(HTTPStatus.NOT_FOUND)
        return spieler

    def einheitInDerArmeeliste(spielernummer: int, einheitennummer: int) -> Einheit:
        spieler = spielerMit(spielernummer)
        einheit = armeelisteNachNummer(aufstellung, spieler).get(einheitennummer)
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
        aufstellung.auswählen(einheitInDerArmeeliste(spielernummer, einheitennummer))
        return spielstandLiefern()

    def einheitAbwählen(spielernummer: int, einheitennummer: int):
        aufstellung.abwählen(einheitInDerArmeeliste(spielernummer, einheitennummer))
        return spielstandLiefern()

    def modellLoslassen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        spiel().modellLoslassen(modell, _stelleDerAnfrage())
        return spielstandLiefern()

    def modellAnklicken(spielernummer: int, einheitennummer: int, modellnummer: int):
        spiel().modellAnklicken(modellDerArmee(spielernummer, einheitennummer, modellnummer))
        return spielstandLiefern()

    def stelleBeimLoslassen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        abfrage = spiel().stellenBeimLoslassen(modell, _stelleDerAbfrage())
        return jsonify(stellenBeimLoslassen(aufstellung, abfrage))

    def karteAnklicken():
        aufstellung.karteAnklicken(_stelleDerAnfrage())
        return spielstandLiefern()

    def aufstellenDerEinheitBeenden():
        aufstellung.aufstellenDerEinheitBeenden()
        return spielstandLiefern()

    def zurücklegen():
        aufstellung.zurücklegen()
        return spielstandLiefern()

    def ersterZugWählen(spielernummer: int):
        spieler = spielerMit(spielernummer)
        schlachtOder404().ersterZugWählen(spieler)
        return spielstandLiefern()

    def phaseBeenden():
        _phaseBeenden(schlachtOder404(), aufstellung)
        return spielstandLiefern()

    def sperreMelden(sperre: Sperre):
        gründe = texteDerGründe(sperre.gründe)
        stand = spielstand(aufstellung, laufendeSchlacht())
        antwort = jsonify({"gründe": gründe, "spielstand": stand})
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
    pfadDerAbfrage = f"{pfadDerEinheit}/modelle/<int:modellnummer>/stelleBeimLoslassen"
    anwendung.add_url_rule(pfadDerAbfrage, view_func=stelleBeimLoslassen)
    pfadDesAnklickens = f"{pfadDerEinheit}/modelle/<int:modellnummer>/anklicken"
    anwendung.add_url_rule(pfadDesAnklickens, view_func=modellAnklicken, methods=["PUT"])
    pfadDerEbene = f"{pfadDerEinheit}/modelle/<int:modellnummer>/ebene"
    anwendung.add_url_rule(pfadDerEbene, view_func=modellAlsEbene, methods=["PUT"])
    anwendung.add_url_rule(pfadDerEbene, view_func=einheitAlsEbene, methods=["DELETE"])
    anwendung.add_url_rule("/api/karteAnklicken", view_func=karteAnklicken, methods=["PUT"])
    anwendung.add_url_rule(
        "/api/aufstellenDerEinheitBeenden", view_func=aufstellenDerEinheitBeenden, methods=["PUT"]
    )
    anwendung.add_url_rule("/api/zurücklegen", view_func=zurücklegen, methods=["PUT"])
    anwendung.add_url_rule(
        "/api/spieler/<int:spielernummer>/ersterZug", view_func=ersterZugWählen, methods=["PUT"]
    )
    anwendung.add_url_rule("/api/phaseBeenden", view_func=phaseBeenden, methods=["PUT"])
    anwendung.register_error_handler(Sperre, sperreMelden)
    return anwendung
