# gitignoreTest.py: Marke `stand`, Prozessverweis im Docstring, Regel-Link

187 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Kritik am Code zu Commit `0e14791`. Die Prüfungen laufen grün (533), `gitignoreTest.py` mit
2 Fällen auch. Der Eintrag in `.gitignore` ist richtig.

**Befund.**
1. `testEineMessdateiVonCoverageIstIgnoriert` prüft die echte `.gitignore` im Repo, trägt
   aber nicht die Marke `stand`. `pyproject.toml` sagt: „`stand` kennzeichnet Prüfungen
   über das echte Repo; die Messung der Prüfskripte lässt sie aus“. Die Zeile zu DoD 1 in
   [regeln.md](../../prozess/regeln.md) sagt dasselbe („ohne Prüfungen über das Repo, Marke
   `stand`“). Der Test daneben, `testPreCommitPrüftSonarLintBeiPythonDateien`, liest
   `.pre-commit-config.yaml` und trägt die Marke.
2. Docstring: „Scheiter-Test: … (Anliegen 186).“ Das widerspricht
   [wir.md](../../prozess/praemissen/wir.md) 8: „kein TODO, FIXME oder Prozessverweis“.
   Sonst nennt kein Docstring in `prozess/pruefungen` eine Anliegen-Nummer.
3. Die neue Zeile in `regeln.md` verlinkt als Regel
   [Ablauf, Werkzeuge](../../prozess/ablauf.md#technikphase). Dort steht nichts über
   Messdateien oder `.gitignore`. Belegt ist die Regel nur in Anliegen 177 und 186.

**Kosten.** 1: Die Abdeckung der Prüfskripte zählt einen Test über das Repo mit, gegen ihre
eigene Festlegung. Wird die Marke weiter so vergessen, misst die Abdeckung nicht mehr, was
`regeln.md` behauptet. 2: Der Verweis veraltet, sobald 186 gelöscht ist (`erledigt`), und
`kommentare.py` fängt ihn nicht. 3: Wer dem Link folgt, findet die Regel nicht.

**Gegenvorschlag.**
1. `@pytest.mark.stand` über den Test.
2. Docstring ohne Verweis und ohne Prozesswort, etwa „Messdateien von coverage stehen in
   .gitignore.“
3. Als Regel-Spalte ohne Link nur „Messdateien von `coverage` bleiben aus Commits
   (Anliegen 177, 186)“. Braucht die Regel eine Stelle im Ablauf, ist das ein Anliegen an
   den Organisationsentwickler.
