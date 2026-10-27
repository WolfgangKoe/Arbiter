# Hindernis: Kritik am Code zu Item normalMove

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** [S2](../../technik/architektur/domaene.md#stelle-und-rechnen) nennt jetzt die Rundung jeder Zahl einer Anfrage (Anliegen 6121), Prüft: [anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py); dort fehlt der Einheitstest. Empfehlung: ein Test, der x = 160/127 und y = 121/3 als JSON-double schickt, einmal als Körper von PUT …/stelle (V5), einmal als Abfrage …/stelleBeimLoslassen (V10), und in der Domäne genau diese Fraction findet; ohne limit_denominator ist er rot. Das hält den Schritt „Kritik am Code zu Item normalMove“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Implementierer beseitigt das Hindernis.

**Stellungnahme.** Angenommen. In [anwendungTest.py](../../technik/tests/einheit/web/anwendungTest.py) schicken zwei Tests x = 160/127 und y = 121/3 als double, einmal als Körper von PUT …/stelle, einmal als Abfrage …/stelleBeimLoslassen, und prüfen, dass `modellLoslassen` bzw. `stellenBeimLoslassen` der Aufstellung genau diese `Stelle` mit den Brüchen 160/127 und 121/3 erhält. Ohne `limit_denominator` in `anwendung.py` (an einer Kopie in /tmp erprobt) sind beide rot; mit ihm grün.
