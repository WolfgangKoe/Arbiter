# Review · Zyklus 1

Inkrement: Änderungen seit `Freigabe Plan 1` (`424afec`) unter `technik/`, Domäne für
[AUF-1](../domaene/anforderungen/phasen/aufstellen.md) (`afe3205`) und ihre Akzeptanztests.
Item: [Reihenfolge der Aufstellung](../domaene/items/reihenfolge-der-aufstellung.md).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 44 bestanden.
2. **Erfüllt, mit Befunden.** `python3 -m pytest prozess/pruefungen`: 286 bestanden
   (Benennung, Rückverfolgung, Höchstmaße, ruff). Nur Text: keine Kommentare, Komplexität
   gering, Spiegel `arbiter/domaene/phasen/` ↔ `tests/einheit/domaene/phasen/` angelegt,
   Glossar ↔ Code stimmt für alle kursiven Begriffe. Toter Zweig und ableitbarer Zustand:
   [47](anliegen/47-aufstellungRandfaelle.md), Befund 3.
3. **Nicht erfüllt.** Das Item liegt noch; es löscht der Planer nach der Abnahme. Die
   Anforderung beschreibt das gebaute Verhalten bis auf zwei offene Fälle:
   [41](anliegen/41-dieselbeEinheitErneutWaehlen.md) (dieselbe Einheit erneut wählen, heute
   ‚Einheit begonnen‘) und [43](anliegen/43-aufstellungszoneNamen.md) (`nord`/`süd` ohne Quelle).
4. **Teilweise.** Dieses Review steht. Die fachliche Abnahme (Schritt 5) fehlt; der Stand
   führt sie nicht: [50](anliegen/50-standUeberspringtFachkritik.md).

## Code
Klein, lesbar, nur Standardbibliothek (A1), Identität per `eq=False` (D1), jede Handlung
sperrt vor der ersten Änderung (D2). Nichts nachgebaut, nichts ineffizient.

## Offene Anliegen aus diesem Review
- [47](anliegen/47-aufstellungRandfaelle.md) an den Implementierer: fremder Spieler als
  Gewinner ergibt einen inkonsistenten Zustand; eine leere Armee führt in eine Sackgasse;
  `beendet` ist ableitbar.
- [48](anliegen/48-sperrtestsOhneUnveraendertenZustand.md) an den Testautor: sieben
  Sperrtests prüfen den unveränderten Zustand nicht (D2), ein doppelter Test.
- [49](anliegen/49-zustandDerAufstellungInSpielobjekten.md) an den Architekten: Zustand der
  Aufstellung frei schreibbar und in `spielobjekte.py`.
- [50](anliegen/50-standUeberspringtFachkritik.md) an den Organisationsentwickler.

Weiter offen zur Technik: [44](anliegen/44-akzeptanztestDateiZuLang.md),
[45](anliegen/45-kennungBleibtStabil.md), [46](anliegen/46-sprungKriteriumUndTest.md).

## Empfehlung
Kein Befund blockiert AUF-1: Jedes Kriterium ist gebaut und grün getestet. Vor der
Prozessphase die fachliche Abnahme durch den Fachkritiker holen, dann löscht der Planer das
Item. 47 und 48 sind kleine Änderungen und gehören noch in diesen Zyklus, damit Zyklus 2 auf
festen Zustandsregeln aufbaut; 49 entscheidet der Architekt vor dem ersten Item mit `web/`.
