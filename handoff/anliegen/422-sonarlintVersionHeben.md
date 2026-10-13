# SonarLint-Erweiterung 6.1.0 statt 6.0.x

422 · Fragen · von Regelumsetzer → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** VS Code hat die SonarLint-Erweiterung auf 6.1.0 aktualisiert. Die Prüfung
`formregeln/sonarlint.py` erwartet 6.0.x (`erwarteteVersion`) und bricht ab. Seitdem sind drei
Tests in `formregeln/sonarlintTest.py` rot und `python3 prozess/pruefungen/gemeinsam/lauf.py
formregeln.sonarlint` endet mit 1. Die rote Gesamtprüfung blockiert jeden Commit.

**Kosten.** Solange sie rot ist, kann keine Rolle fertig melden. Die Versionsbindung ist
Absicht: Eine neue Version kann andere Funde liefern.

**Gegenvorschlag.** Siehe Optionen.

**F1 · Wie kommt die Prüfung wieder grün?**
A: `erwarteteVersion` auf 6.1. heben. Der Regelumsetzer prüft, ob die Funde gleich bleiben,
und meldet Abweichungen als Anliegen. Eine Zeile, nach Auftrag sofort erledigt.
B: Die Version 6.0.x wieder installieren und VS Code das Aktualisieren der Erweiterung
verbieten. Dauerhaft stabil, kostet aber Handarbeit auf jedem Gerät.
C: Die Bindung an die Hauptversion lockern (`6.`): Kleine Sprünge brechen nichts mehr. Dafür
fällt eine Änderung der Funde unbemerkt durch.
Empfehlung: A. Das Heben ist der im Fehlertext vorgesehene Weg, der Aufwand ist klein und die
Version bleibt festgelegt.
Antwort: A

**Stellungnahme (Regelumsetzer).** Nach deiner Antwort A umgesetzt: `erwarteteVersion` steht
auf `6.1.`, Tests und Zeile in [Regeln](../../prozess/regeln.md) angepasst. Mit 6.1.0 meldet
`formregeln.sonarlint` über alle geprüften Ordner keine Funde, es kommen also keine neuen
Abweichungen dazu.
