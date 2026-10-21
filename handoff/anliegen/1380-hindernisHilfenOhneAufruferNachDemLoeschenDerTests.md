# Hindernis: Hilfen ohne Aufrufer nach dem Löschen der Tests

1380 · Kritik · von Testautor → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Nach [1350](1350-testsEntfallenerKriterienWidersprechenAnhalten.md) meldet die Prüfung
`testDasProduktHatKeinenTotenCode` (`prozess/pruefungen/formregeln/abdeckungTest.py`) vier Hilfen
ohne Aufrufer in gemeinsamen Dateien, die der Lauf zu 1350 nicht ändern durfte:
`gesperrteModelle` und `kennzeichenDesKreises` in `bildschirm.py`, `sperreDesVertrags` in
`dienst.py`, `einGesperrtesModell` in `handgriffe.py`. Alle vier gehörten nur zu den gelöschten
Tests.

**Kosten.** Die Prüfung ist rot, der Commit von Item anhaltenAnBases bleibt gesperrt.

**Gegenvorschlag.** Ein Testautor löscht die vier Funktionen samt ungenutzten Importen, sobald
der Lauf zu 1360 diese Dateien nicht mehr ändert. Danach `vulture` und ruff prüfen. Ruft 1360
eine der Hilfen auf, bleibt sie stehen.

**Stellungnahme.** Die vier Hilfen hatten keinen Aufrufer (auch 1360 ruft keine auf) und sind
samt Docstrings gelöscht; ungenutzte Importe blieben keine zurück. Ruff ist grün,
`testDasProduktHatKeinenTotenCode` ist grün. Rot bleiben drei Prüfungen, die nicht zu diesem
Anliegen gehören: Spiegel und Glossar zu `gesperrtesModell.py` (Produktcode des
Implementierers zu einheitVerschieben) und der Kopf von 1370 (Datei des Implementierers).
