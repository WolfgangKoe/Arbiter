# Pfadverweise auf Prüfskripte veralten bei jedem Umzug

284 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Nach 253 P1 und P2 nannte der [Ablauf](../../prozess/ablauf.md) sieben Module oder Funktionen am alten Ort (Anliegen 282, berichtigt). In `prozess/regeln.md` stehen noch:
1. Z. 66 und 93 `standregeln/plan.py` (jetzt `lesen/plan.py`); Z. 66 `wartendeAlsText` in `stand.py` (jetzt `kriterienregeln/rueckverfolgung.py`).
2. Z. 73 `rollenregeln/belegung.py`, `belegungTest.py` (jetzt `standregeln/`).
3. Z. 90 `offeneItems` (jetzt `lesen/plan.py`), `lage` (jetzt `standregeln/phasenfolge.py`) unter `stand.py`; Z. 95 `domänenphase`, `planOhneFreigabe` ebenso nach `phasenfolge.py`.
4. Z. 74 `bashPositivliste.py` ruft `gitShowZulässig`: prüfen, ob der Aufruf nach `gitBefehle.py` gezogen ist.

Gefunden per Skript: jeder `<ordner>/<datei>.py` in `ablauf.md` und `regeln.md` gegen `prozess/pruefungen`, Namen in Klammern dahinter gegen `def`, `class` und Konstanten. 253 P5 und P7 ziehen weiter um (`hoechstmassTest.py`, `komplexitaetTest.py`).

**Kosten.** Wer einer Regel folgt, findet die Datei nicht oder prüft das falsche Modul; die Kritik am Code findet es nur nebenbei, je Umzug eine Runde Anliegen.

**Gegenvorschlag.** Bestehende Regel geprüft (ich.md 4): `anliegenregeln/erledigteLoeschen.py` (`linksErsetzen`) deckt nur Links auf Anliegen, die Benennungsprüfung keine Verweise in Text. Daher:
1. `regeln.md` Punkte 1 bis 4 auf die heutigen Orte.
2. Mechanismus, Regel „Ein Verweis auf ein Prüfskript zeigt auf eine vorhandene Datei“: jeder Pfad `<themenordner>/<name>.py` in `prozess/**/*.md`, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md` und den `CLAUDE.md` existiert unter `prozess/pruefungen/`; ein Name in Klammern dahinter oder nach „ruft“ ist dort definiert, außer bei `*Test.py`. Im Lauf von `python3 -m pytest prozess/pruefungen`; Schicht `formregeln`. Scheiter-Test: alter Pfad rot, Funktion am falschen Modul rot, Testdatei mit Beispielwort grün.

Erledigt, wenn die Prüfung über das Repo grün ist, ihr Scheiter-Test an je einem Gegenbeispiel rot wird und die Zeile in `regeln.md` steht. Den Ablauf ziehe ich bei roter Prüfung selbst nach. Reihenfolge: nach 253 P5 und P7 (dieselben Dateien, der Kopf kennt `wartet auf` erst mit 274).

**Stellungnahme.** Ergänzung aus 253 P7 (b800ee7): `hoechstmassTest.py` ist zu `formregeln/hoechstmass.py` (Maße, Zählung), `ruffAufrufen`, `complexipyAufrufen`, `pyproject` zu `formregeln/werkzeugaufruf.py` umgezogen. `regeln.md` ist nachgezogen; in `ablauf.md` nennen die Zeilen 19, 102, 106, 181, 240, 311 noch alte Pfade oder Orte (`hoechstmassTest.py`, `konfigurationTest.py`). Der Organisationsentwickler zieht sie nach.

Stellungnahme: Entfällt mit dem Rückbau.
