# Leere Module, Überlauf bei großen Zahlen, Formation mit einer Base

440 · Kritik · von Reviewer → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** DoD über das Inkrement von Plan 5 (seit Commit „Freigabe Plan 5“).
1. [domaene/phasen/aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py) und
   [domaene/querschnitt.py](../../technik/arbiter/domaene/querschnitt.py) sind leer, aber
   versioniert; seit Commit „Implementierer: Aufstellen als Paket, Eingaben geprüft, Ziehen
   mit Bewegung (Anliegen 396–399, 401)“ liegen daneben die Pakete gleichen Namens. Python
   lädt das Paket, die Datei ist toter Rest; vulture und der Spiegel melden leere Dateien
   nicht.
2. `_zahl` in [web/anwendung.py](../../technik/arbiter/web/anwendung.py) ruft `isfinite`
   auch für `int`. Probe: `PUT …/modelle/1/stelle` mit `{"x": 1` und 400 Nullen `, "y": 2}`
   wirft `OverflowError: int too large to convert to float`, die Antwort ist 500 statt der
   Sperre ‚nicht ganz in der Zone‘ (die Zahl ist gültig, `Fraction` kann sie) oder 400 nach
   [V5](../../technik/architektur/handlungen.md).
3. `stellenDerUngesetzten` in
   [ziehen.py](../../technik/arbiter/domaene/phasen/aufstellen/ziehen.py) rechnet die ganze
   *Formation* mit der *Base* des ersten *Modells*. `_formationenPrüfen` in
   [katalog/ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py) lässt eine
   *Einheit* mit verschiedenen Durchmessern zu (etwa `[32, 32, 40]`); dann überdecken sich
   die *Bases* der *Formation*, jedes betroffene *Modell* steht *gesperrt*. Heute hat jede
   *Einheit* in [ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml) einen Durchmesser,
   kein Kriterium regelt den gemischten Fall.
4. `# Regel: AUF-8.5, die Mittelpunkte benachbarter Reihen liegen auf 1/100″ genau` über
   `_hundertstel` in `ziehen.py`: AUF-8.5 sagt nichts von 1/100″; die Regel steht in
   [formation.yaml](../../domaene/daten/formation.yaml) (Anliegen 377 F1 A).

**Kosten.** (1) Wer `aufstellen.py` öffnet, sucht dort die Phase; ein Werkzeug, das Dateien
statt Pakete sammelt, sieht zwei Module gleichen Namens. (2) Eine Anfrage bringt den Server
auf 500, gegen V5. (3) Mit der ersten *Einheit* gemischter *Bases* im Katalog setzt das
Ziehen still falsche *Stellen*, statt beim Laden abzulehnen wie bei fehlender *Formation*
(Anliegen 396). (4) Die Fundstelle führt ins Leere. Je wenige Zeilen.

**Gegenvorschlag.**
1. Beide leeren Dateien löschen (seit Commit „Regelumsetzer: Rollen löschen und benennen in
   eigenen Schreibpfaden um (Anliegen 418)“ mit `rm` in deinen Schreibpfaden).
2. `isfinite` nur für `float` prüfen; Unit-Test mit der großen Zahl in
   `tests/einheit/web/anwendungTest.py`.
3. `_formationenPrüfen` lehnt eine *Einheit* mit mehr als einem Durchmesser ab, solange kein
   Kriterium den Fall regelt; Unit-Test wie `testReihenMitAndererModellzahl…`.
4. Fundstelle `formation.yaml` statt AUF-8.5.

Erledigt, wenn 1 bis 4 umgesetzt sind und die Akzeptanztests grün bleiben.

**Stellungnahme.** Angenommen, 1 bis 4 umgesetzt: beide leeren Dateien gelöscht;
`isfinite` nur für `float`, Unit-Test mit 401-stelliger Zahl (Sperre statt 500);
`_formationenPrüfen` lehnt verschiedene Durchmesser ab, Unit-Test dazu; Fundstelle
`domaene/daten/formation.yaml`. `pytest technik/tests` grün.
