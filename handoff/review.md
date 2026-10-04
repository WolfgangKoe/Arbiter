# Review · Zyklus 2

Inkrement: Änderungen seit `Freigabe Plan 2` (`1553538`) unter `technik/`, Stand `ef7ef88`.
Items aus [Plan 2](plan.md): *Ausgangslage von Only War*, *Sperren beim Setzen*,
*Nahkampfreichweite beim Setzen*; abgenommen in `1e725cd`, gelöscht in `52eedbd`.

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 150 bestanden. Die Grenzfälle aus S2
   (Berühren, ein Millionstel Zoll zu nah oder zu weit, Rand der Zone) laufen exakt.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 427 bestanden (Benennung, Spiegel,
   Rückverfolgung, Höchstmaße, Komplexität, Glossar, Kommentare, Importvertrag, ruff). Zur
   Probe auch ruff mit ARG, PLR2004, PLR0913, FBT, ERA, C901 über `technik/arbiter`: ohne
   Fund. Toter Code (nur Text): keiner gefunden, jede Funktion und jeder `Grund` hat einen
   Aufrufer. Glossar → Code (Urteil): *überdecken*, *ganz in*, *Abstand*,
   *Nahkampfreichweite*, *Stelle*, *Tiefe*, *Ausgangslage* stehen wörtlich im Code.
3. **Erfüllt.** `domaene/items/` ist leer; AUF-2, AUF-3, QUE-1 und OBJ-1 beschreiben das
   gebaute Verhalten.
4. **Erfüllt.** Der Fachkritiker hat die drei Items in `1e725cd` abgenommen, sein Anliegen
   dazu ist erledigt; dieses Review steht.

## Code
Domäne nur mit Standardbibliothek (A1), Katalog liest über `yaml.safe_load` und prüft die
Daten beim Laden (A3, S2: ganze mm, beide Zonen, Kante der zweiten Seitenlänge). Gemessen
wird nur in `messen.py` mit `Fraction`, Abstände als Quadrate (M1, S2). `modellSetzen`
sammelt alle Gründe, bevor es den Zustand ändert (D2, AUF-3.5), und prüft die Stelle nicht,
wenn AUF-1.4 sperrt (AUF-3.6). Spielobjekte `frozen`, Tiefen als `MappingProxyType` (D3).
Nichts nachgebaut, nichts ineffizient. Der einzige Befund (QUE-1.2 in der Aufstellung statt
in `querschnitt.py`) ist in `68a2797` behoben und erledigt (Anliegen 149); danach
`technik/tests` 153 grün.
Kritik am Code ist für jeden Code-Commit seit der Freigabe gelaufen; aus den Prüfskripten
sind 147 und 148 erledigt.

## Offene Anliegen zur Technik
- Anliegen 146: Schnitt der ersten Oberfläche, an den
  Architekten, vor Plan 3.
- [124](anliegen/124-sprungPerKlickErproben.md): Sprung per Klick, Nachprüfung durch den
  Architekten.
- [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md): Prüfskripte ordnen, an den
  Regelumsetzer.

## Empfehlung
Die DoD ist für alle drei Items erfüllt, Plan 2 ist abgenommen. Aus diesem Review ist am
Code nichts offen.
