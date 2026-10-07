# Sammelanliegen Zyklus 3: Nachschliff an Prüfskripten

302 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** Befunde ohne Fehlverhalten aus der Kritik am Code, gesammelt nach
[Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code) (Anliegen 296, F3 A). Ein
Abschnitt je Datei; nimm einen mit, wenn du die Datei ohnehin änderst. Offene übernimmt das
Sammelanliegen des nächsten Zyklus.

1. `formregeln/importvertrag.py` (94a94f9): `importierteNamen` wiederholt die Schleife von
   `importierteModule` und fügt nur `modul.name` hinzu; `aufgelöst(knoten, paket) or "?"`
   steht dreimal. Die Sortierung in `vorlagenImporte` vertauscht das Paar zweimal.
2. `formregeln/zustandsschutz.py` (94a94f9): `textKonstante` baut `einzelstellen.textVon`
   nach (gleiche Schicht `formregeln`). Der Docstring von `umwegVerstöße` sagt „Lesen“, die
   Prüfung meldet auch Schreiben über `__dict__`.
3. `formregeln/sonarlintTest.py` (94a94f9): In
   `testDieAusnahmeVonS4502GiltNurSolangeDieAnwendungKeineRouteAußerGetHat` liest jede Datei
   zweimal von der Platte, je einmal für `routenAußerLesen` und `ansichtsKlassen`.
4. `prozess/regeln.md`, Zeile Ablauf, Werkzeuge (94a94f9): Die Scheiter-Tests nennen
   „S4502-Ausnahme rot bei Route außer GET“, nicht die Klassenansicht.

**Kosten.** Lesbarkeit und doppelte Stellen; kein falsches Ergebnis. Je wenige Zeilen.

**Gegenvorschlag.**
1. `importierteNamen` aus `importierteModule` ableiten oder umgekehrt; das Auflösen mit `?`
   in eine Funktion; `sorted(treffer, key=itemgetter(1, 0))`.
2. `textVon` wiederverwenden (`or ""` am Aufruf), Docstring „Zugriff auf `_`-Attribute ohne
   Punkt“.
3. Den Quelltext einmal je Datei lesen.
4. „Klassenansicht“ zu den Scheiter-Tests der Zeile.

Erledigt, wenn alle Abschnitte umgesetzt oder an das Sammelanliegen des nächsten Zyklus
übergeben sind.

**Stellungnahme.**
