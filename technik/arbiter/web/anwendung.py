import json
import re
from fractions import Fraction
from http import HTTPStatus
from math import isfinite
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

from arbiter.domaene.phasen.aufstellen import Aufstellung
from arbiter.domaene.phasen.aufstellen.anhaltenAufDemWeg import Weiterrücken
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


def _weiterrücken(angaben: dict, *, angehalten: bool) -> Weiterrücken | None:
    if not angaben and not angehalten:
        return None
    if not angaben:
        return Weiterrücken(None, angehalten)
    zuvor = Stelle(x=_zahl(angaben, "zuvorX"), y=_zahl(angaben, "zuvorY"))
    return Weiterrücken(zuvor, angehalten)


def _weiterrückenDerAbfrage() -> Weiterrücken | None:
    namen = ("zuvorX", "zuvorY")
    angaben = {name: _jsonZahl(request.args[name]) for name in namen if name in request.args}
    return _weiterrücken(angaben, angehalten=request.args.get("angehaltenAufDemWeg") == "true")


def _weiterrückenDerAnfrage() -> Weiterrücken | None:
    körper = request.get_json(silent=True)
    if not isinstance(körper, dict):
        abort(HTTPStatus.BAD_REQUEST)
    namen = ("zuvorX", "zuvorY")
    angaben = {name: körper[name] for name in namen if name in körper}
    return _weiterrücken(angaben, angehalten=körper.get("angehaltenAufDemWeg") is True)


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

    def einheitAuswählen(spielernummer: int, einheitennummer: int):
        aufstellung.auswählen(einheitInDerArmeeliste(spielernummer, einheitennummer))
        return spielstandLiefern()

    def einheitAbwählen(spielernummer: int, einheitennummer: int):
        aufstellung.abwählen(einheitInDerArmeeliste(spielernummer, einheitennummer))
        return spielstandLiefern()

    def modellLoslassen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        stelle = _stelleDerAnfrage()
        schlacht = laufendeSchlacht()
        if schlacht is None:
            aufstellung.modellLoslassen(modell, stelle, _weiterrückenDerAnfrage())
        else:
            schlacht.modellLoslassen(modell, stelle, _weiterrückenDerAnfrage())
        return spielstandLiefern()

    def modellAnklicken(spielernummer: int, einheitennummer: int, modellnummer: int):
        spiel().modellAnklicken(modellDerArmee(spielernummer, einheitennummer, modellnummer))
        return spielstandLiefern()

    def stelleBeimLoslassen(spielernummer: int, einheitennummer: int, modellnummer: int):
        modell = modellDerArmee(spielernummer, einheitennummer, modellnummer)
        stelle = _stelleDerAbfrage()
        schlacht = laufendeSchlacht()
        weiter = _weiterrückenDerAbfrage()
        if schlacht is None:
            abfrage = aufstellung.stellenBeimLoslassen(modell, stelle, weiter)
        else:
            abfrage = schlacht.stellenBeimLoslassen(modell, stelle, weiter)
        return jsonify(stellenBeimLoslassen(aufstellung, abfrage))

    def karteAnklicken():
        spiel().karteAnklicken(_stelleDerAnfrage())
        return spielstandLiefern()

    def vorrücken():
        schlachtOder404().vorrücken()
        return spielstandLiefern()

    def vorrückenZurücknehmen():
        schlachtOder404().vorrückenZurücknehmen()
        return spielstandLiefern()

    def einheitZurücksetzen():
        schlachtOder404().einheitZurücksetzen()
        return spielstandLiefern()

    def gemeinsamÜbergehen():
        schlachtOder404().gemeinsamÜbergehen()
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
    anwendung.add_url_rule("/api/karteAnklicken", view_func=karteAnklicken, methods=["PUT"])
    anwendung.add_url_rule("/api/vorrücken", view_func=vorrücken, methods=["PUT"])
    anwendung.add_url_rule(
        "/api/vorrückenZurücknehmen", view_func=vorrückenZurücknehmen, methods=["PUT"]
    )
    anwendung.add_url_rule(
        "/api/einheitZurücksetzen", view_func=einheitZurücksetzen, methods=["PUT"]
    )
    anwendung.add_url_rule("/api/gemeinsamÜbergehen", view_func=gemeinsamÜbergehen, methods=["PUT"])
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
