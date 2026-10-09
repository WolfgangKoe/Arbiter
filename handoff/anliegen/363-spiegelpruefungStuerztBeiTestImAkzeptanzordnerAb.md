# Spiegelprüfung stürzt bei einem Test direkt im Akzeptanzordner ab

363 · Kritik · von Testautor (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** In [benennung.py](../../prozess/pruefungen/formregeln/benennung.py) bricht
`spiegelVerstoß` mit `ValueError: PosixPath('.') has an empty name` ab, wenn eine Datei
`<name>Test.py` direkt in `technik/tests/akzeptanz/` liegt (Beispiel war `spielobjekteTest.py`).
Dann ist `pfad.parent.relative_to(ordner)` der Pfad `.`, und `.with_suffix(".md")` in der
Zeile für `gebündelt` wirft. Der Absturz besteht nach dem Umbenennen nicht fort: die Tests liegen
jetzt in Unterordnern. Er kann wiederkehren bei jeder Testdatei direkt im Ordner, deren
Anforderung nicht als `anforderungen/<name>.md` existiert. Ein Verstoß sollte als Meldung
erscheinen, nicht als Absturz.

**Kosten.** Ein falsch abgelegter Test lässt `testDasRepoHältDieBenennung` abstürzen statt
mit dem Grund zu scheitern; wer den Test ablegt, sieht die Ursache nicht.

**Gegenvorschlag.** Liegt `pfad.parent` im Akzeptanzordner selbst, meldet die Prüfung „Akzeptanztest
gehört in den Ordner seiner Anforderung“, bevor sie `with_suffix` aufruft; ein Test dazu in
`benennungTest.py`.

**Stellungnahme.**
