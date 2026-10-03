# Review · Zyklus 1

Inkrement: Änderungen seit `Freigabe Plan 1` (`424afec`) unter `technik/`, Domäne für
[AUF-1](../domaene/anforderungen/phasen/aufstellen.md) und ihre Akzeptanz- und Einheitstests,
Stand `b0f06bb`. Item: [Reihenfolge der Aufstellung](../domaene/items/reihenfolge-der-aufstellung.md).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 45 bestanden.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 288 bestanden
   (Benennung, Rückverfolgung, Höchstmaße, ruff). Nur Text: ein Kommentar nach `wir.md`
   (`# Warum:`), Komplexität gering, Spiegel `arbiter/domaene/phasen/` ↔
   `tests/einheit/domaene/phasen/` mit Tests, Glossar ↔ Code stimmt für alle kursiven Begriffe.
3. **Nicht erfüllt.** Das Item liegt noch; es löscht der Planer nach der Abnahme. Die
   Anforderung beschreibt das gebaute Verhalten bis auf die Namen `nord`/`süd` ohne Quelle:
   [43](anliegen/43-aufstellungszoneNamen.md), gefragt in [58](anliegen/58-namenDerAufstellungszonen.md).
4. **Teilweise.** Dieses Review steht. Die fachliche Abnahme (Schritt 5) fehlt; der Stand
   führt sie nicht: [50](anliegen/50-standUeberspringtFachkritik.md).

## Code
Klein, lesbar, nur Standardbibliothek (A1), Identität per `eq=False` (D1), jede Handlung
sperrt vor der ersten Änderung (D2), Spielobjekte `frozen`, Zustand der Aufstellung in
`_`-Feldern (D3), fremde Spieler als Vorbedingung (`ValueError`).
Sperrtests prüfen den unveränderten Zustand. Nichts nachgebaut, nichts ineffizient.

## Offene Anliegen zur Technik
- [50](anliegen/50-standUeberspringtFachkritik.md): angenommen, Nachprüfung durch den Reviewer.

## Empfehlung
Kein Befund blockiert AUF-1: Jedes Kriterium ist gebaut und grün getestet. Vor der
Prozessphase die fachliche Abnahme durch den Fachkritiker holen, dann löscht der Planer das
Item. Aus diesem Review ist am Code nichts mehr offen.
