# Hindernis: Kritik an den Tests zu Item anhaltenUebergehen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testBew1_7DieStellenBeimLoslassenSindDieStellenDesEinenModells, testBew1_7DieStellenBeimLoslassenSindBeiDerGanzenEinheitDieStellenJedesModells, testBew1_7DieStellenBeimLoslassenÄndernNichtsAmSpielstand, testBew1_7DieStellenBeimLoslassenHaltenWeiterAlsDieBewegungsweiteAnDerBewegungsweiteAn, testBew1_7DerDienstNenntBeiDerGanzenEinheitDieStellenJedesModells, testBew1_7DerDienstNenntOhneEbeneEinheitNurDasGezogeneModell, testBew1_7DerDienstNenntWeiterAlsDieBewegungsweiteDieStelleDesAnhaltensWieDasLoslassen, testBew1_7DerDienstVerändertBeimAbfragenNichtsAmSpielstand, testBew1_7DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre[maus], testBew1_7DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre[finger], testBew1_7DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre[maus], testBew1_7DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre[finger], testBew1_7DieKarteZeigtWeiterAlsDieBewegungsweiteDasModellAnDerBewegungsweiteOhneSperrmeldung[maus], testBew1_7DieKarteZeigtWeiterAlsDieBewegungsweiteDasModellAnDerBewegungsweiteOhneSperrmeldung[finger], testBew8_3DieSeiteZeigtOhneAnhaltenKeinGemeinsamÜbergehen, testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[links], testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[rechts], testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[unten], testQue6_2NachDemStartIstKeineLeisteEingefahren[links], testQue6_2NachDemStartIstKeineLeisteEingefahren[rechts], testQue6_2NachDemStartIstKeineLeisteEingefahren[unten], testQue6_2NachDemStartZeigtJedeArmeelisteIhrenInhalt[links], testQue6_2NachDemStartZeigtJedeArmeelisteIhrenInhalt[rechts], testQue5_6DerDienstNenntNachDemLoslassenDasProtokollWieDavor. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item anhaltenUebergehen“ von Architekt im Fortschritt auf.

Meine Einordnung: Die Tests zu BEW-1.7 und QUE-6 erfüllt der Code früherer Items, hier ist
nur ihr Aufbau neu; `testBew8_3DieSeiteZeigtOhneAnhaltenKeinGemeinsamÜbergehen` verneint und
ist darum vorher grün. Für diese genügt die Stelle. Rot zu machen ist
`testQue5_6DerDienstNenntNachDemLoslassenDasProtokollWieDavor`: Er vergleicht ein leeres
*Protokoll* mit einem leeren und bliebe grün, wenn Loslassen es leerte; vorher einmal
`anhaltenUndÜbergehen` wie im Domänentest daneben.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Angenommen wie eingeordnet.
- Rot: `testQue5_6DerDienst…` in `querschnitt/uebergehenTest.py` übergeht vorher den Warboss,
  lässt dann einen Boy am Dienst los; das *Protokoll* hat davor einen *Eintrag* und danach
  denselben. Rot, weil `gemeinsamÜbergehenAngeboten` fehlt.
- BEW-1.7 erfüllen `Schlacht.stellenBeimLoslassen` (`domaene/querschnitt/schlachtrunden.py`),
  `stelleBeimLoslassen` (`web/anwendung.py`) und `stelleBeimLoslassenAbfragen`
  (`frontend/bedienung.js`).
- QUE-6.1 und 6.2: die Leisten mit `aria-expanded="true"` in `frontend/index.html`, ihre Lage
  in `frontend/komponenten.css` (`.leiste`, `.leisteRechts`, `.leisteUnten`).
- BEW-8.3 an der Seite: `frontend/anfragen.js` bietet den Knopf nur bei
  `übergehbareAnfrage !== null`; ohne Anhalten gibt es keine.
