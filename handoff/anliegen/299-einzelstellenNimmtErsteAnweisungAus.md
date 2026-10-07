# Einzelstellen nimmt jede erste Anweisung als Docstring aus

299 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 17747a1 (Anliegen 272, dort erledigt: die Gegenbeispiele sind
rot). `docstrings` in `formregeln/einzelstellen.py` nimmt die erste Anweisung jedes Moduls,
jeder Klasse und Funktion aus, sobald sie ein `ast.Expr` ist, nicht nur bei einer
Text-Konstante. Probe über `stellenIn`: `def f():\n    os.system("git add -A")\n` und
`subprocess.run("git status", shell=True)` als erste Zeile eines Moduls ohne Docstring sind
grün; dieselbe Zeile als zweite Anweisung ist rot.

**Kosten.** Der Prozessaufruf `"git …"` ist der Weg, den 272, Punkt 2 schließt; ein Hook, dessen
Funktion mit dem Aufruf beginnt, geht still vorbei. Eine Zeile und ein Test.

**Gegenvorschlag.** In `docstrings` nur aufnehmen, wenn `textVon(erste.value)` nicht `None`
ist. Scheiter-Test: `def f():\n    os.system("git add -A")\n` ist rot.

**Stellungnahme.**
