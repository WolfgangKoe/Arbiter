# Abhaken sucht die Zeile „Umfang:“ zweimal

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 11

## Runde 1
**Befund.** Nachprüfung von 16240 (2df4c44): `testkennungenDesItems` in
`prozess/pruefungen/standregeln/testsRot.py` prüft mit `any(zeile.startswith(umfangMarke) …)`
selbst, ob das Item eine Zeile „Umfang:“ hat. Gleich danach sucht `umfangDes` dieselbe Zeile
noch einmal. Damit steht die Erkennung der Zeile zweimal im Code
([Wir 3](../../prozess/praemissen/wir.md), [Es, S](../../prozess/praemissen/es.md)).
Weicht eine der beiden Stellen einmal ab (etwa bei Leerraum vor der Marke), passen Meldung und
geprüfter Umfang nicht mehr zusammen. Das Verhalten stimmt heute, und die Prüfungen sind grün.
Deshalb hält der Befund nicht auf. Er gehört zu Namen und Ablage von Hilfsfunktionen
([Kritik](../../prozess/ablauf/kritik.md)).

**Kosten.** Wenige Zeilen, und die beiden bestehenden Fälle in `standregeln/abhakenTest.py`
decken die Änderung ab. Bleibt es, muss man die Marke bei einer Änderung an zwei Stellen
anfassen.

**Gegenvorschlag.** Ohne Probe in `/tmp`, sie gehört zur Umsetzung. Nur `umfangDes`
erkennt die Zeile. Findet die Funktion keine, wirft sie `UmfangFehlt`, oder
`testkennungenDesItems` wirft die Ausnahme, wenn das Ergebnis leer ist. Die eigene Prüfung
mit `any(…)` entfällt dann. Fall `testEinItemOhneUmfangMachtAbhakenRotUndNenntEs` bleibt grün.

**Stellungnahme.**
