# Retro 6: was P1 bis P5 und 1790 technisch brauchen

1850 · Kritik · von Architekt → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Zur [Retro 6](../retro.md); nach [Ich 3](../../prozess/praemissen/ich.md) hält alles
auf, die Prozessphase ist die deiner Perspektive (wie [1790](1790-dodUeberDasInkrementNurPerBefehl.md)).
1. P2, „gilt, solange Modul und Tests gleich bleiben“: Ob ein Mutant überlebt, hängt auch an
   Modulen ringsum, `conftest.py`, Hilfsmodulen und `domaene/daten`. Fängt ein Test den
   Mutanten in `messen.py` über `setzenPerKlick.py`, und erreicht dieses die Zeile nach einer
   Änderung nicht mehr, gälte „gefangen“ weiter.
2. P2, „nur die Tests, die sie ausführen“: Zeilen auf Modulebene (Tabellen, Katalogdaten)
   laufen beim Import, keinem Test zugeordnet; Tests über `python3 -m arbiter` (Fixture
   `befehl`) laufen in einem Prozess, den die Messung nicht sieht.
3. P2, „ein gleichwertiger zählt mit Begründung nicht“: Wo liest das Werkzeug sie?
   Zeilennummern wandern; ein Kommentar nähme jeden Mutanten der Zeile aus.
4. P3: Die [Sandbox](https://code.claude.com/docs/en/sandboxing) erlaubt Schreiben im
   Arbeitsordner; sperren muss `filesystem.denyWrite`, Wiederöffnen darin nennt die Doku nur
   fürs Lesen. Erlaubt schreiben im Projekt: die Fortschrittsbefehle (`abhaken.py`,
   `hindernis.py`), pytest, ruff, complexipy, coverage (Caches, `__pycache__`), künftig der
   Speicher aus P2. Ohne `allowUnsandboxedCommands: false` wiederholt eine Rolle den Befehl
   ohne Sandbox. Ob Chromium (Bildschirmtests) darin startet, ist offen.
5. P4, „nur freie Nummern“: Die Bereiche nennt der Koordinator im Auftrag (hier 1850–1859),
   in keiner Datei. Kein Skript kennt sie; gleichzeitige Läufe kollidieren weiter.
6. P5, „alte TODOs machen die DoD rot“: Die DoD gilt je Item, ein altes TODO sperrte jedes.
   [1660](1660-regelkommentareEntbehrlich.md) sagt „am Ende einer Technikphase“; offen dort
   F2 (Deckel, woran „alt“) und welche Werkzeugkommentare: `# noqa` ohne Liste umgeht jede
   ruff-Regel.
7. P1: Der Hook ohne Produkttests (P2) widerspricht [Ablauf, Commits](../../prozess/ablauf.md#commits)
   („prüft nur, was der Commit ändern kann“), P1 nennt ihn nicht. Befund 8 zählt 1.659 Zeilen
   Prüfcode samt Tests gegen 518 Produktcode ohne Tests; gleich gezählt 870 gegen 518 ohne,
   1.659 gegen 4.435 mit Tests.
8. 1790 lässt `review` stehen: Das Review zählt, sobald sein Kopf steht, in Zyklus 6 vor dem
   Ende der DoD (DoD 2: „nachdem der Implementierer … angepasst hat“).

**Kosten.** 1, 2, 8: Der Stand meldet „gefangen“ oder „DoD erfüllt“ ohne Prüfung, die Sorge
in [1671](1671-prozessphaseVorziehen.md). 3 bis 5: Der Regelumsetzer rät (Ich 1) oder bricht
Prüfungen und Fortschrittsbefehle. 6: Ein Item wartet auf fremde TODOs. 7: Die Kennzahl misst
die Zählweise.

**Gegenvorschlag.** Bestehend ([Ich 4](../../prozess/praemissen/ich.md)): Neuland erst als
Wegwerf-Versuch (Architekt), [Kennzahlen](../../prozess/kennzahlen.md).
1. P2: Ein Ergebnis gilt, solange `technik/`, `pyproject.toml` und `domaene/daten` gleich
   sind (ein Hash, außerhalb des Projekts). Modulebene, fremder Prozess: alle Tests. Erledigt,
   wenn gezielt und voll über `messen.py` dieselben Mutanten fangen.
2. P2: Gleichwertige in einer Datei beim Werkzeug (Modul, Zeilentext, Mutation, Begründung).
3. P3: Erst ein Wegwerf-Versuch an einer Kopie in `/tmp`: `denyWrite` auf `technik/`,
   `domaene/`, `prozess/`, keine Wiederholung ohne Sandbox, Caches nach `$TMPDIR`;
   Bildschirmtests und Fortschrittsbefehle laufen. Dann nennt P3, was `bashSchreiben.py` verliert.
4. P4: Der Bereich ist Eingabe des Befehls (`--bereich 1850-1859`), ohne ihn keine Nummer.
5. P5: „die DoD über das Inkrement“; Deckel und „alt“ fragst du in 1660; Werkzeugkommentare
   als geschlossene Liste mit Regelcode.
6. P1 nennt Commits; die Kennzahl zählt beide Seiten ohne Tests.
7. 1790: nur der Befehl; der Scheiter-Test auch mit geschriebenem Review.

**Stellungnahme.** Alles in [Retro 6](../retro.md), P2 und P3 verweisen auf 1850; 8 in 1790,
Fragen zu 6 in [1860](1860-todoDeckelUndWerkzeugkommentare.md).
