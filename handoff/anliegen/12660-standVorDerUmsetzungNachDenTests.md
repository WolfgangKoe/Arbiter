# Stand vor der Umsetzung: erster Produktcommit nach den Tests

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** `standregeln/standVorDerUmsetzung.py` nimmt den Produktcode aus HEAD, solange „Implementierer: Tests zu Item … grün“ fehlt. Ein committeter Teil der Umsetzung (096dfed „anhaltenAufDemWeg Teil 1“) gilt so als Stand davor: Abhaken meldet Tests als grün vor dem Code, die gegen 4d8ca81 rot sind (Anliegen 12521, 12522, 12600). Bestehende Regel: [standregeln](../../prozess/regeln/standregeln.md), Zeile Retro 9 P1, Anliegen 12000; sie wird angepasst, keine neue.

**Kosten.** Ohne Änderung je Teilcommit vor dem Abhaken ein Hindernis ohne Fehler im Test, im Zyklus noch bei anhaltenAufDemWeg Teil 2, fliegen und zuruecksetzenUndLuecken. Mit Änderung: eine Funktion und ein Scheiter-Test, kein Hook und keine Einstellung.

**Gegenvorschlag.** Stand vor der Umsetzung ist der Vorgänger des ersten Commits nach dem ersten Commit mit „- [x] Testautor: Tests zu Item …“, der `technik/arbiter` oder `technik/frontend` ändert; liegt der erste Commit mit „- [x] Implementierer: Tests zu Item … grün“ davor oder fehlt der Testautor-Haken, gilt wie bisher dessen Vorgänger; sonst HEAD. Die Obergrenze braucht es, weil der Haken des Testautors ein Fakt ist und nachhängen kann: bei anhaltenUebergehen kam er erst in 12a7aaa, zusammen mit der Umsetzung.

Erprobt an einer Kopie in `/tmp/probe12600` (`git diff` dort zeigt beide Dateien): `ersteUmsetzung` in `standVorDerUmsetzung.py`, dazu `testEinCommitteterTeilDerUmsetzungNachDenTestsMachtKeinenTestGrün` in `standregeln/abhakenTest.py`. Der neue Test ist mit dem alten Code rot, mit dem neuen sind alle 15 in `abhakenTest.py` grün; SonarLint grün nach einer Konstante für `--format=%H` (S1192). Am echten Verlauf ergibt sich für anhaltenAufDemWeg 4d8ca81, den Stand, gegen den der Fachkritiker die sieben Tests rot fand. Die übrigen Hooks scheiterten in der Kopie nur an fehlendem `node_modules` und nicht installiertem Commit-Hook. Rollen und Commits berührt es nicht: Nur `testsRot.py` ruft `mitKopie` auf.

Lücke, die bleibt: Ein Teilcommit, bevor der Haken des Testautors steht, zählt weiter als Stand davor; dann gilt der heutige Weg (Stelle nennen, Anliegen 11360).

Zeile in [standregeln](../../prozess/regeln/standregeln.md) mit Anliegen 12600 nachführen. Rückweg: `git revert` des Commits, der Rest bleibt.

**Stellungnahme.** Gegenvorschlag umgesetzt wie erprobt: `ersteUmsetzung` in [standVorDerUmsetzung.py](../../prozess/pruefungen/standregeln/standVorDerUmsetzung.py), Scheiter-Test `testEinCommitteterTeilDerUmsetzungNachDenTestsMachtKeinenTestGrün` in [abhakenTest.py](../../prozess/pruefungen/standregeln/abhakenTest.py), Zeile in [standregeln](../../prozess/regeln/standregeln.md) nachgeführt. Die Lücke (Teilcommit vor dem Haken des Testautors) bleibt wie genannt. Rückweg: `git revert`.
