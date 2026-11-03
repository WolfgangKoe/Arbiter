# Hindernis: Anliegen 9340 Fliegen der Canoptek-Spinne

Form: Kritik
Von: Anforderungsautor
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Mit der Canoptek-Spinne in der Armee der Necrons wird testBew11_5DieSeiteZeigtJedeEinhüllendeDurchIhreMaskeAusDenselbenGrenzkreisen (grenzkreiseTest.py:101) rot: Er zählt fest 3 Grenzen (eine Bewegungsweite, zwei Nahkampfreichweiten), mit der dritten gegnerischen Einheit sind es 4. Gemessen an einer Kopie in /tmp, sonst bleibt alles wie vorher; der Weirdboy steht schon in den Daten. Zähle die Nahkampfreichweiten aus den gegnerischen Einheiten wie die Fixtures nach 10380. Das hält den Schritt „Anliegen 9340 Fliegen der Canoptek-Spinne“ von Anforderungsautor im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Umgesetzt in [grenzkreiseTest.py](../../technik/tests/akzeptanz/phasen/bewegung/grenzkreiseTest.py): testBew11_5DieSeiteZeigtJedeEinhüllendeDurchIhreMaskeAusDenselbenGrenzkreisen erwartet eine Grenze der Bewegung plus je Einheit des Gegners eine Nahkampfreichweite (`1 + len(spielerZwei.armee.einheiten)`), wie testBew11_3DieSeiteZeigtJeEinheitDesAnderenSpielersDieNahkampfreichweite, statt fest 3. Mit den heutigen Daten grün; mit der Canoptek-Spinne zählt er 4.
