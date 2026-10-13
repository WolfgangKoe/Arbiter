"""Mini-Server des Dashboards (WSGI): zeigt die Anliegen, legt Züge des Stakeholders sofort ab."""

import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import WSGIServer, make_server

from gemeinsam.pfade import projektordner
from rollenregeln.dashboard import dashboardSchreiben
from rollenregeln.dashboardAnliegenSeiten import (
    anliegenNach,
    anliegenSeite,
    einzelSeite,
    navigation,
    neuladenSkript,
    seitenStil,
    stand,
)
from rollenregeln.dashboardHinweise import adresse, lokalesSchema, vorgabePort
from rollenregeln.eingang import Zug, verworfeneLeeren, zugVormerken
from rollenregeln.zuegeUebernehmen import übernehmen

htmlTyp = "text/html; charset=utf-8"
anliegenPfad = "/anliegen/"
prüfskripteOrdner = "prozess/pruefungen"
neustartPrüfIntervall = 1


@dataclass(frozen=True)
class Antwort:
    status: HTTPStatus
    typ: str = htmlTyp
    inhalt: bytes = b""
    ort: str | None = None


def text(inhalt: str, status: HTTPStatus = HTTPStatus.OK, typ: str = htmlTyp) -> Antwort:
    return Antwort(status, typ, inhalt.encode("utf-8"))


def weiterleitung(ort: str) -> Antwort:
    return Antwort(HTTPStatus.SEE_OTHER, ort=ort)


def tokenbericht(ordner: Path) -> Antwort:
    datei = dashboardSchreiben(ordner)  # Warum: der Hinweis auf offene Fragen soll aktuell sein
    zusatz = (
        f"<style>{seitenStil}</style>{navigation('Tokenbericht')}<script>{neuladenSkript}</script>"
    )
    return text(datei.read_text(encoding="utf-8").replace("<body>", f"<body>{zusatz}", 1))


def feldwert(felder: dict[str, list[str]], name: str) -> str:
    return (felder.get(name) or [""])[0].strip()


def zügeAusFormular(nummer: int, felder: dict[str, list[str]]) -> list[Zug]:
    """Die Züge in der Folge Status, Runde, Antworten, Kommentar; leere Felder entfallen."""
    züge = []
    if feldwert(felder, "status"):
        züge.append(Zug(nummer, "status", feldwert(felder, "status")))
    if feldwert(felder, "runde") == "senken":
        züge.append(Zug(nummer, "runde"))
    for name in sorted(felder):
        if name.startswith("antwort_") and feldwert(felder, name):
            frage = name.removeprefix("antwort_")
            züge.append(Zug(nummer, "antwort", feldwert(felder, name), frage=frage))
    if feldwert(felder, "kommentar"):
        züge.append(Zug(nummer, "kommentar", feldwert(felder, "kommentar")))
    return züge


def zugsendung(ordner: Path, nummer: int, körper: bytes) -> Antwort:
    if anliegenNach(ordner, nummer) is None:
        return text("Kein solches Anliegen.", HTTPStatus.NOT_FOUND)
    felder = parse_qs(körper.decode("utf-8"))
    for zug in zügeAusFormular(nummer, felder):
        zugVormerken(ordner, zug)
    übernehmen(ordner)
    return weiterleitung(f"{anliegenPfad}{nummer}")


def nummerAus(pfad: str) -> int | None:
    rest = pfad.removeprefix(anliegenPfad)
    return int(rest) if pfad.startswith(anliegenPfad) and rest.isdigit() else None


def fremderUrsprung(kopf: dict[str, str | None]) -> bool:
    """Ein Formular von einer anderen Seite im Browser darf keine Züge vormerken."""
    herkunft = kopf.get("Origin")
    return herkunft is not None and herkunft != f"{lokalesSchema}://{kopf.get('Host')}"


def lesen(ordner: Path, pfad: str) -> Antwort:
    if pfad == "/":
        return text(anliegenSeite(ordner))
    if pfad == "/tokens":
        return tokenbericht(ordner)
    if pfad == "/stand":
        return text(stand(ordner), typ="text/plain; charset=utf-8")
    nummer = nummerAus(pfad)
    seite = einzelSeite(ordner, nummer) if nummer is not None else None
    return text(seite) if seite else text("Nicht gefunden.", HTTPStatus.NOT_FOUND)


def schreiben(ordner: Path, pfad: str, körper: bytes) -> Antwort:
    if pfad == "/verworfeneLeeren":
        verworfeneLeeren(ordner)
        return weiterleitung("/")
    nummer = nummerAus(pfad)
    if nummer is None:
        return text("Nicht gefunden.", HTTPStatus.NOT_FOUND)
    return zugsendung(ordner, nummer, körper)


def antworten(
    ordner: Path, methode: str, pfad: str, körper: bytes, kopf: dict[str, str | None]
) -> Antwort:
    """Die Antwort auf eine Anfrage; ohne Netz, damit die Tests sie aufrufen können."""
    if methode == "GET":
        return lesen(ordner, pfad)
    if fremderUrsprung(kopf):
        return text("Fremder Ursprung.", HTTPStatus.FORBIDDEN)
    return schreiben(ordner, pfad, körper)


def anwendung(ordner: Path) -> Callable:
    """Die WSGI-Anwendung, die Anfragen an `antworten` weiterreicht."""

    def anwenden(umgebung: dict, antwortStart: Callable) -> list[bytes]:
        länge = int(umgebung.get("CONTENT_LENGTH") or 0)
        körper = umgebung["wsgi.input"].read(länge)
        kopf = {"Origin": umgebung.get("HTTP_ORIGIN"), "Host": umgebung.get("HTTP_HOST", "")}
        pfad = umgebung.get("PATH_INFO", "/")
        antwort = antworten(ordner, umgebung["REQUEST_METHOD"], pfad, körper, kopf)
        zeilen = [("Content-Type", antwort.typ), ("Content-Length", str(len(antwort.inhalt)))]
        if antwort.ort:
            zeilen.append(("Location", antwort.ort))
        antwortStart(f"{antwort.status.value} {antwort.status.phrase}", zeilen)
        return [antwort.inhalt]

    return anwenden


def serverErzeugen(ordner: Path, port: int) -> WSGIServer:
    return make_server(adresse, port, anwendung(ordner))


def quellenStand(ordner: Path) -> tuple[tuple[str, int], ...]:
    """Änderungszeiten aller Prüfskripte; ändern sie sich, läuft der Server mit altem Code."""
    skripte = sorted((ordner / prüfskripteOrdner).rglob("*.py"))
    return tuple((str(skript), skript.stat().st_mtime_ns) for skript in skripte)


def hauptlauf(argumente: list[str]) -> None:
    port = int(argumente[0]) if argumente else vorgabePort
    ordner = projektordner()
    server = serverErzeugen(ordner, port)
    server.timeout = neustartPrüfIntervall
    anfang = quellenStand(ordner)
    print(f"{lokalesSchema}://{adresse}:{port}/  (beenden mit Strg+C)")
    try:
        while quellenStand(ordner) == anfang:
            server.handle_request()
    except KeyboardInterrupt:
        return
    # Warum: Der Stakeholder startet den Server nicht neu, wenn sich der Code geändert hat
    server.server_close()
    os.execv(sys.executable, [sys.executable, *sys.argv])


if __name__ == "__main__":
    hauptlauf(sys.argv[1:])
