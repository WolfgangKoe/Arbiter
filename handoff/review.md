# Review · Zyklus 1

Inkrement: Änderungen seit `Freigabe Plan 1` (`424afec`) unter `technik/`, Domäne für
[AUF-1](../domaene/anforderungen/phasen/aufstellen.md) und ihre Akzeptanz- und Einheitstests,
Stand `dc321c1`. Item: *Reihenfolge der Aufstellung* (abgenommen, gelöscht in `dc321c1`).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 46 bestanden.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 282 bestanden
   (Benennung, Rückverfolgung, Höchstmaße, ruff). Nur Text: ein Kommentar nach `wir.md`
   (`# Warum:`), Komplexität gering, Spiegel `arbiter/domaene/phasen/` ↔
   `tests/einheit/domaene/phasen/` mit Tests, Glossar → Code stimmt für alle kursiven Begriffe.
   Code → Glossar ebenso, mit `Aufstellungszone (erste, zweite)` (Anliegen 74).
3. **Erfüllt.** Das Item ist gelöscht. AUF-1.3 regelt den Zwischenzustand, der Akzeptanztest
   `testAuf1_3SolangeDieAufstellungszoneOffenIstIstKeinerAnDerReihe` ist grün (Anliegen 25).
   Die Zonen tragen keine erfundenen Namen mehr: `Aufstellungszone.erste`, `.zweite`
   (Anliegen 63).
4. **Erfüllt.** Dieses Review steht; der Fachkritiker hat ohne Befund abgenommen. Den Schritt
   nennt jetzt der Stand (Anliegen 50); offen ist nur ein Plan ohne Item-Link
   ([76](anliegen/76-planOhneItemLink.md)).

## Code
Klein, lesbar, nur Standardbibliothek (A1), Identität per `eq=False` (D1), jede Handlung
sperrt vor der ersten Änderung (D2), Spielobjekte `frozen`, Zustand der Aufstellung in
`_`-Feldern (D3), fremde Spieler als Vorbedingung (`ValueError`).
Sperrtests prüfen den unveränderten Zustand. Nichts nachgebaut, nichts ineffizient.
Seit der Retro geprüft, ohne Befund: `8ac70b7` und `265dac7` (Zonenwerte), `a969610`
(`pyproject.toml` nur noch `*Test.py`; keine Datei `test_*.py` übrig).

## Offene Anliegen zur Technik
- [79](anliegen/79-kritikCommitsFehlen.md): Kritik-Commits seit Retro 1, an den
  Organisationsentwickler.

## Empfehlung
DoD für das Item erfüllt, AUF-1 ist abgenommen. Aus diesem Review ist am Code nichts offen.
