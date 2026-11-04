# Handlung ohne Wenn in den Tests zu zuruecksetzenUndLuecken

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf: neuer Code verletzt [T1](../../technik/architektur/tests.md) (4), „ohne
**wenn** keine Handlung“. BEW-24.1, BEW-22.1 und QUE-11.1 haben kein **wenn**, diese Tests
haben trotzdem einen eigenen Block mit einer Handlung:
- [einheitZuruecksetzenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/einheitZuruecksetzenTest.py):
  `testBew24_1DerDienstNenntZurücksetzenAngebotenWieImBeispielDesVertrags` (Loslassen).
- [keinVorrueckenAusDerNahkampfreichweiteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/keinVorrueckenAusDerNahkampfreichweiteTest.py):
  `testBew22_1InDerNahkampfreichweiteLässtVorrückenDieEinheitNichtWarten`,
  `testBew22_1DerDienstNenntInDerNahkampfreichweiteVorrückenNichtAngebotenUndÄndertNichts`
  (Vorrücken).
- [phaseBeendenTest.py](../../technik/tests/akzeptanz/querschnitt/phaseBeendenTest.py):
  `testQue11_1VorDemErstenZugÄndertPhaseBeendenNichts`,
  `testQue11_1NachDemEndeDerSchlachtÄndertPhaseBeendenNichts` (Phase beenden).

Wer sie liest, sucht das **wenn**, das sie prüfen, und findet es in einer anderen Anforderung.
Der Bestand legt solche Tests zum Kriterium mit dem Klick: `testBew5_2OhneAngebotWartetNachVorrückenKeineEinheit`,
`testBew12_2OhneAngebotBleibtJedesModellWoEsHingezogenWurde`,
`testQue10_2DerDienstÄndertNichtsBeimKörperEinerSchonBeendetenPhase`. Die Tests selbst
braucht es: Erst dass Vorrücken und Phase beenden ohne Angebot nichts ändern, *sperrt* (Ziel).

**Kosten.** Testautor, etwa eine halbe Stunde; die Fixture `inDerNahkampfreichweite` zieht in
ein Hilfsmodul (`vorruecken.py`), weil zwei Dateien sie brauchen.

**Gegenvorschlag.**
1. BEW-24.1: Das Loslassen gehört zum Aufbau, ohne Leerzeile davor; die Prüfung liest die
   Antwort wie bisher.
2. BEW-22.1: Die beiden Handlungen ziehen nach
   [vorrueckenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/vorrueckenTest.py) als
   `testBew5_2InDerNahkampfreichweite…` (5.2: „nach 5.1“, und 22.1 ändert 5.1). In 22.1 bleibt
   ein Dienst-Test ohne PUT: `spielstandVon` nennt `vorrücken` `{"angeboten": false,
   "zurücknehmen": false}`, wie `testBew5_1DerDienstNenntOhneAuswahlVorrückenNichtAngeboten`.
3. QUE-11.1: Die beiden Handlungen ziehen nach
   [schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py) als
   `testQue10_2…`.

**Stellungnahme.** Angenommen, 1 bis 3 umgesetzt.
1. `testBew24_1DerDienstNenntZurücksetzenAngebotenWieImBeispielDesVertrags`: Das Loslassen
   steht im Aufbau ohne Leerzeile davor.
2. Nach [vorrueckenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/vorrueckenTest.py)
   gezogen als `testBew5_2InDerNahkampfreichweiteWartetNachVorrückenDieEinheitNicht` und
   `testBew5_2DerDienstÄndertInDerNahkampfreichweiteBeimVorrückenNichts`. In 22.1 steht
   `testBew22_1DerDienstNenntInDerNahkampfreichweiteVorrückenNichtAngeboten` ohne PUT. Abweichung:
   Die Fixture `inDerNahkampfreichweite` steht in
   [conftest.py](../../technik/tests/akzeptanz/conftest.py) statt in `vorruecken.py`, denn
   geteilte Fixtures stehen dort (`einheitAmZug`); aus einem Hilfsmodul importiert, wäre sie im
   Test als Parameter neu gebunden (ruff F811). Ihren Inhalt ändert erst 13051.
3. Nach [schlachtrundenTest.py](../../technik/tests/akzeptanz/querschnitt/schlachtrundenTest.py)
   gezogen als `testQue10_2VorDemErstenZugÄndertPhaseBeendenNichts` und
   `testQue10_2NachDemEndeDerSchlachtÄndertPhaseBeendenNichts`.
