# Hindernis: Kritik an den Tests zu Item loslassenNebenDerKarte

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Drei neue Dienst-Tests vergleichen das Beispiel des Vertrags ganz statt nach T3 und werden rot, sobald Weirdboy oder Spinne in einer Armee stehen: testAuf28_1DerDienstSetztAmPunktDerLetztenStelleWieDasBeispielImVertrag (losgelassen.json), testAuf16_7DerDienstNenntNachDemZurücklegenKeineStelleWieDasBeispielImVertrag (Spielstand gegen zurückgelegt.json) und testAuf16_7DerDienstSetztNachDemZurücklegenNichtsWieDasBeispielImVertrag (zurückgelegt.json). Vergleiche mit imUmfangDes aus dienst.py wie in einheitZuruecklegenTest.py. Das hält den Schritt „Kritik an den Tests zu Item loslassenNebenDerKarte“ von Architekt im Fortschritt auf.

Meine Einordnung: hält auf nach [Kritik](../../prozess/ablauf/kritik.md), neuer Code verletzt
[T3](../../technik/architektur/tests.md#aufbau) (Commit 6812e74). Die übrigen 36 Tests prüfen
ihr Kriterium; rot sind die roten aus dem erwarteten Grund (keine Anfrage nach V5 neben der
*Karte*, `stellenBeimLoslassen` nicht leer). Die 7 grünen sind recht: AUF-16.8 erfüllt schon
`Aufstellung._wählbareEinheitVon` (409, darum keine Anfrage), den Dienst-Test zu AUF-28.1
`Aufstellung.modellLoslassen` nach V5; beide bewachen, dass AUF-28.1 nur die Seite ändert.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Angenommen wie vorgeschlagen. Die drei Dienst-Tests vergleichen jetzt mit
`imUmfangDes` wie `einheitZuruecklegenTest.py`: AUF-28.1 in
[loslassenWoDieKarteZeigtTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenWoDieKarteZeigtTest.py)
(`losgelassen.json`), beide AUF-16.7 in
[loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)
(`zurueckgelegt.json`, auch der Spielstand nach der Abfrage). `keineStelleBeimLoslassen.json`
nennt keine *Armeeliste* und bleibt ganz verglichen. Rot und grün wie zuvor (32 rot, 49 grün
in den vier betroffenen Dateien), rot aus denselben Gründen.
