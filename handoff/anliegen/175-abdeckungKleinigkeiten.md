# Abdeckung: Kommentarform, Auslöser des Hooks, doppelter Test

175 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Kritik am Code zu Commit `f87a822`. [170](170-abdeckungMeldetFalschGruen.md) und
[171](171-abdeckungLaufzeitUndZuschnitt.md) sind damit erledigt; übrig sind drei kleine
Befunde.

**Befund.**
1. `abdeckung.py`, Zeile 15: `# Regel: vulture meldet 0 für nichts gefunden und 3 für toten
   Code …`. Nach [wir.md](../../prozess/praemissen/wir.md) 8 steht `# Regel:` mit einer
   Fundstelle für einen Regel-Sonderfall. Die Rückgabewerte von vulture sind eine
   Eigenschaft des Werkzeugs, also `# Warum:`. `kommentare.py` prüft nur die Form, darum ist
   der Kommentar grün.
2. Der Hook `abdeckungPruefskripte` läuft nur mit `files: ^prozess/pruefungen/`. Die Zahl
   hängt aber auch an `pyproject.toml`: `tool.coverage.report` (`exclude_also`) und die
   Marke `stand`. Ändert ein Commit nur dort, etwa weil `exclude_also` erweitert wird, misst
   niemand nach.
3. `testVultureNenntNurTestfunktionenAlsAusnahme` liest den Text von `ignore_names` aus
   `pyproject.toml`. Das Verhalten prüft schon `testEineTestfunktionImProduktMeldetVultureAuch`
   mit der echten `pyproject.toml`. Der Spiegeltest kommt dazu und muss bei jeder
   gleichwertigen Schreibweise angepasst werden.

**Kosten.** 1: Der Leser sucht eine Fundstelle, die es nicht gibt. 2: Eine Lockerung der
Messung bleibt bis zur nächsten Änderung an den Prüfskripten unbemerkt. 3: ein Test mehr
ohne zusätzliche Aussage. Je wenige Minuten.

**Gegenvorschlag.**
1. `# Warum: vulture endet mit 0 ohne Fund und mit 3 bei totem Code; alles andere ist ein
   Fehler.`
2. `files: ^(prozess/pruefungen/|pyproject\.toml$)`.
3. `testVultureNenntNurTestfunktionenAlsAusnahme` streichen.
