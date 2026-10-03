# Review · Zyklus 1

Inkrement: Änderungen seit `Freigabe Plan 1` (`424afec`) unter `technik/`, Domäne für
[AUF-1](../domaene/anforderungen/phasen/aufstellen.md) und ihre Akzeptanz- und Einheitstests,
Stand `d7a468f`. Item: [Reihenfolge der Aufstellung](../domaene/items/reihenfolge-der-aufstellung.md).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 43 bestanden.
2. **Erfüllt, mit Befunden.** `python3 -m pytest prozess/pruefungen`: 294 bestanden
   (Benennung, Rückverfolgung, Höchstmaße, ruff). Nur Text: keine Kommentare, Komplexität
   gering, Spiegel `arbiter/domaene/phasen/` ↔ `tests/einheit/domaene/phasen/` mit Tests,
   Glossar ↔ Code stimmt für alle kursiven Begriffe. Ein unerreichbarer Teil einer Bedingung
   und eine Abfrage ohne Vorbedingung: [47](anliegen/47-aufstellungRandfaelle.md), Runde 2.
3. **Nicht erfüllt.** Das Item liegt noch; es löscht der Planer nach der Abnahme. Die
   Anforderung beschreibt das gebaute Verhalten bis auf zwei offene Fälle:
   [41](anliegen/41-dieselbeEinheitErneutWaehlen.md) (dieselbe Einheit erneut wählen, heute
   ‚Einheit begonnen‘) und [43](anliegen/43-aufstellungszoneNamen.md) (`nord`/`süd` ohne Quelle).
4. **Teilweise.** Dieses Review steht. Die fachliche Abnahme (Schritt 5) fehlt; der Stand
   führt sie nicht: [50](anliegen/50-standUeberspringtFachkritik.md).

## Code
Klein, lesbar, nur Standardbibliothek (A1), Identität per `eq=False` (D1), jede Handlung
sperrt vor der ersten Änderung (D2), Spielobjekte `frozen`, Zustand der Aufstellung in
`_`-Feldern (D3) bis auf `spieler`: [55](anliegen/55-zustandInDerAufstellung.md), Runde 2.
Sperrtests prüfen den unveränderten Zustand. Nichts nachgebaut, nichts ineffizient.

## Offene Anliegen zur Technik
- [47](anliegen/47-aufstellungRandfaelle.md) an den Implementierer: toter Teil der Bedingung
  in `aufstellenDerEinheitBeenden`, `aufstellungszone` für einen fremden Spieler.
- [55](anliegen/55-zustandInDerAufstellung.md) an den Implementierer: `spieler` frei schreibbar.
- [50](anliegen/50-standUeberspringtFachkritik.md) an den Organisationsentwickler.
- [45](anliegen/45-kennungBleibtStabil.md) an den Anforderungsautor.

## Empfehlung
Kein Befund blockiert AUF-1: Jedes Kriterium ist gebaut und grün getestet. Vor der
Prozessphase die fachliche Abnahme durch den Fachkritiker holen, dann löscht der Planer das
Item. 47 und 55 sind je wenige Zeilen und können in einem Lauf des Implementierers zu Beginn
der nächsten Technikphase erledigt werden.
