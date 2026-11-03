# QUE-1.4 prüft das Angebot am Stand davor

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (Lesbarkeit nach [Es](../../prozess/praemissen/es.md), Prüfung nach
[T1](../../technik/architektur/tests.md) 4), Kritik an den Tests zu Item anhaltenAufDemWeg.
In `testQue1_4SperrtBaseÜberdecktNachDemAnhaltenBietetDerDienstGemeinsamÜbergehenNichtAn`
([setzenTest.py](../../technik/tests/akzeptanz/querschnitt/setzenTest.py)) prüft die letzte
Zeile `davor["schlacht"]["gemeinsamÜbergehen"]`, also den Stand vor dem Loslassen. Das *dann*
von QUE-1.4 (kein *Angebot* nach der *Sperre*) folgt erst, wenn man diese Zeile mit
`spielstand == davor` aus der Zeile darüber verbindet. Wer den Test liest, hält die letzte
Zeile für eine Prüfung des Ergebnisses. Sie prüft aber den Aufbau. Die Szene selbst stimmt
(nachgerechnet): Der Warboss hält nach BEW-3.1 auf der *Base* des fünften Boys an, QUE-1.2
sperrt, und ein Code, der das Angebot vor der Sperrprüfung merkt, macht den Test rot.

**Kosten.** Eine Zeile. Bleibt es so, rechnet jeder Leser das Kriterium aus zwei Zeilen
zusammen.

**Gegenvorschlag.** Prüfe das Angebot an der Antwort:
`antwort.get_json()["spielstand"]["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": False}`.
Die Zeile mit `== {"gründe": …, "spielstand": davor}` bleibt.

**Stellungnahme.** Angenommen wie vorgeschlagen: Die letzte Zeile in
[setzenTest.py](../../technik/tests/akzeptanz/querschnitt/setzenTest.py) prüft jetzt
`antwort.get_json()["spielstand"]["schlacht"]["gemeinsamÜbergehen"] == {"angeboten": False}`,
die Zeile mit `{"gründe": …, "spielstand": davor}` bleibt. 12021 an derselben Stelle wartet
weiter auf die Technikphase 11.
