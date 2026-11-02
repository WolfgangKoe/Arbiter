# Plan · Zyklus 10

Etappe: [2 · Phasen und Bewegungsphase](../domaene/etappen/02-bewegen.md). Grundlage:
Zyklusziel aus [Review 9](review.md), 9440 und 10160: sechs Items, Etappe 2 endet mit Zyklus 10.

## Dein Happy Path nach Zyklus 10
1. Aufstellen, erster Zug, *Bewegungsphase* wie bisher.
2. Hält Arbiter die Boyz an der *Bewegungsweite* oder vor einem Gegner an, bietet er nach dem
   Loslassen „gemeinsam übergehen“ an, ohne *Grund*. Klick: Die Boyz stehen, wo ihr sie
   hingezogen habt; das *Protokoll* nennt ‚Bewegungsweite‘, ‚Nahkampfreichweite‘ oder beide.
   Zieht ihr sie danach noch einmal, bleiben sie stehen, auch zurück, und Arbiter bietet
   wieder „gemeinsam übergehen“ an; zum Ausgangspunkt: „Einheit zurücksetzen“ (Schritt 6). (Item 1)
3. Lasst ihr ein *Modell* neben der *Karte* los, steht es, wo die *Karte* es zuletzt zeigte,
   beim Aufstellen für die *Einheit in Aufstellung*. (Item 2)
4. Zieht ihr einen Boy auf eine fremde *Base* zu, hält Arbiter davor an und gleitet entlang,
   auch beim Aufstellen, in der *Bewegungsphase* nie über *Bewegungsweite*, Kante oder
   *Nahkampfreichweite* hinaus. Loslassen *setzt* ihn dort, kein ‚über eine Base‘ mehr. (Item 3)
5. Die Canoptek-Spinne zieht ihr über fremde *Bases* hinweg; lasst ihr sie auf einer los, rückt
   sie an die nächste freie *Stelle*. (Item 4)
6. Bis zum Ende der *Bewegungsphase* setzt „Einheit zurücksetzen“ jede gezogene zurück. Aus
   *Nahkampfreichweite* bietet Arbiter kein *Vorrücken* an, „Phase beenden“ nur vom *ersten Zug*
   bis zum Ende der *Schlacht*. Der Weirdboy steht in der *Armee* der Orks. (Item 5)
7. Erscheint oder verschwindet etwas neben der *Karte*, bleibt jede *Stelle*, wo sie war. (Item 6)

## Items
1. [Anhalten übergehen](../domaene/items/anhaltenUebergehen.md): Schritt 2; BEW-8.3, BEW-8.4
   ohne BEW-17, BEW-8.5, BEW-25, QUE-5.6.
2. [Loslassen neben der Karte](../domaene/items/loslassenNebenDerKarte.md): Schritt 3;
   AUF-28.1, AUF-16.7, AUF-16.8, BEW-20.1.
3. [Anhalten auf dem Weg](../domaene/items/anhaltenAufDemWeg.md): Schritt 4; BEW-17 (auch
   BEW-17.3 und BEW-17.4), BEW-19, AUF-29, AUF-28.2, QUE-1.4, BEW-8.4 in BEW-17.
4. [Fliegen](../domaene/items/fliegen.md): Schritt 5; BEW-18, Spinne.
5. [Zurücksetzen und Lücken](../domaene/items/zuruecksetzenUndLuecken.md): Schritt 6;
   BEW-24, BEW-22.1, BEW-9.2, QUE-11.1, MIV-2.
6. [Ruhige Karte](../domaene/items/ruhigeKarte.md): Schritt 7; QUE-7.1.

Reihenfolge: Item 1 zuerst, sonst macht Item 3 Tests rot (9320, 9440). Item 2 vor 3,
sonst spränge zurück, wer vor einer *Base* anhält und neben der *Karte* loslässt (8840).
Item 4 nach 3: *Fliegen* ersetzt dessen Anhalten (BEW-17.1). Item 6 zuletzt (2361 F2, 8880).
Vor Item 4 und 5, neben Item 1: Fixtures für eine dritte *Einheit*, sonst brechen Tests ab
(10380), dann Daten zu Spinne (9340) und Weirdboy (10180).

Danach (8880 F2 A): Aufräumen aus Anliegen der Technikphase 10 und 7800, dann Review 10.
Vorgezogen: 7321 und 8261 in Item 1, 9401 in Item 3.

Andere Etappen: AUF-12.8, BEW-21.1 in 7 (10200), BEW-23 in 3 (F2 B), Flugzeug in 4 (F3 B).

## Abweichungen vom Zyklusziel
- Sechs Items statt höchstens drei (Domänenphase 6), mit deiner Ausnahme (F1 B): Die
  Technikphase dauert etwa doppelt so lang, dafür entfällt ein Zyklus. Hängt Item 3, rücken
  3 und 4 in Zyklus 11 (Schritte 4 und 5); hängt 4 oder 6, nur dieses.
- Anhalten übergehen ist dabei, nicht erst in Etappe 3 (9271).

## Empfehlung
Gib frei, wenn Schritte 1 bis 7 deinem Bild entsprechen. Item 3 und 4 sind Neuland, Item 4
etwa so teuer wie 1 und 2 zusammen: Der Architekt erprobt beide vor den Tests (10321); geht es
nicht, fragt dich ein Anliegen vor dem Vertrag (Ausweg 8840 F4 B).

## Offene Anliegen
- An den Anforderungsautor, in der Technikphase:
  [10180](anliegen/10180-etappe2LueckenNachPlan10.md), [9340](anliegen/9340-fliegenDerSpinne.md).
- Übrige: [Moderation](moderation.md).

## Fortschritt
- [x] Architekt: Vertrag zu Item anhaltenUebergehen, bei beiden Hälften
- [ ] Testautor: Tests zu Item anhaltenUebergehen
- [ ] Fachkritiker: Kritik an den Tests zu Item anhaltenUebergehen
  Hindernis: Fachkritiker → Testautor: Kein Test wählt nach BEW-25.1 erneut gemeinsam übergehen: Stelle am zweiten Punkt und Eintrag mit Gründen ungeprüft (Anliegen 10980); beseitigt: Commit „Tests zu Item anhaltenUebergehen: 10980 und 11001 beseitigt, Helfer zu 10560“
  Hindernis: Fachkritiker → Testautor: Diese Tests sind grün, bevor der Code besteht: testBew1_7DieStellenBeimLoslassenSindDieStellenDesEinenModells, testBew1_7DieStellenBeimLoslassenSindBeiDerGanzenEinheitDieStellenJedesModells, testBew1_7DieStellenBeimLoslassenÄndernNichtsAmSpielstand, testBew1_7DieStellenBeimLoslassenHaltenWeiterAlsDieBewegungsweiteAnDerBewegungsweiteAn, testBew1_7DerDienstNenntBeiDerGanzenEinheitDieStellenJedesModells, testBew1_7DerDienstNenntOhneEbeneEinheitNurDasGezogeneModell, testBew1_7DerDienstNenntWeiterAlsDieBewegungsweiteDieStelleDesAnhaltensWieDasLoslassen, testBew1_7DerDienstVerändertBeimAbfragenNichtsAmSpielstand, testBew1_7DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre[maus], testBew1_7DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre[finger], testBew1_7DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre[maus], testBew1_7DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre[finger], testBew1_7DieKarteZeigtWeiterAlsDieBewegungsweiteDasModellAnDerBewegungsweiteOhneSperrmeldung[maus], testBew1_7DieKarteZeigtWeiterAlsDieBewegungsweiteDasModellAnDerBewegungsweiteOhneSperrmeldung[finger], testBew8_3DieSeiteZeigtOhneAnhaltenKeinGemeinsamÜbergehen, testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[links], testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[rechts], testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[unten], testQue6_2NachDemStartIstKeineLeisteEingefahren[links], testQue6_2NachDemStartIstKeineLeisteEingefahren[rechts], testQue6_2NachDemStartIstKeineLeisteEingefahren[unten], testQue6_2NachDemStartZeigtJedeArmeelisteIhrenInhalt[links], testQue6_2NachDemStartZeigtJedeArmeelisteIhrenInhalt[rechts]. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. (Anliegen 11263)
  Hindernis: Fachkritiker → Organisationsentwickler: Der Befehl zum Abhaken lehnt ab, solange ein Test grün ist, auch wenn die Stelle genannt und geprüft ist (Anliegen 11360)
- [ ] Architekt: Kritik an den Tests zu Item anhaltenUebergehen
  Hindernis: Architekt → Testautor: Diese Tests sind grün, bevor der Code besteht: testBew1_7DieStellenBeimLoslassenSindDieStellenDesEinenModells, testBew1_7DieStellenBeimLoslassenSindBeiDerGanzenEinheitDieStellenJedesModells, testBew1_7DieStellenBeimLoslassenÄndernNichtsAmSpielstand, testBew1_7DieStellenBeimLoslassenHaltenWeiterAlsDieBewegungsweiteAnDerBewegungsweiteAn, testBew1_7DerDienstNenntBeiDerGanzenEinheitDieStellenJedesModells, testBew1_7DerDienstNenntOhneEbeneEinheitNurDasGezogeneModell, testBew1_7DerDienstNenntWeiterAlsDieBewegungsweiteDieStelleDesAnhaltensWieDasLoslassen, testBew1_7DerDienstVerändertBeimAbfragenNichtsAmSpielstand, testBew1_7DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre[maus], testBew1_7DieKarteZeigtBeimHaltenJedesModellDerEinheitDortWoEsBeimLoslassenStehtOhneSperre[finger], testBew1_7DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre[maus], testBew1_7DieKarteZeigtBeimHaltenNurDasGezogeneModellDortWoEsBeimLoslassenStehtOhneSperre[finger], testBew1_7DieKarteZeigtWeiterAlsDieBewegungsweiteDasModellAnDerBewegungsweiteOhneSperrmeldung[maus], testBew1_7DieKarteZeigtWeiterAlsDieBewegungsweiteDasModellAnDerBewegungsweiteOhneSperrmeldung[finger], testBew8_3DieSeiteZeigtOhneAnhaltenKeinGemeinsamÜbergehen, testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[links], testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[rechts], testQue6_1JedeLeisteStehtAnIhrerSeiteDerKarte[unten], testQue6_2NachDemStartIstKeineLeisteEingefahren[links], testQue6_2NachDemStartIstKeineLeisteEingefahren[rechts], testQue6_2NachDemStartIstKeineLeisteEingefahren[unten], testQue6_2NachDemStartZeigtJedeArmeelisteIhrenInhalt[links], testQue6_2NachDemStartZeigtJedeArmeelisteIhrenInhalt[rechts], testQue5_6DerDienstNenntNachDemLoslassenDasProtokollWieDavor. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. (Anliegen 11001); beseitigt: Commit „Tests zu Item anhaltenUebergehen: 10980 und 11001 beseitigt, Helfer zu 10560“
  Hindernis: Architekt → Testautor: Der Dienst-Test zu BEW-25.1 liest das Protokoll andersherum und prüft die Gründe des neuen Eintrags nicht (Anliegen 11380)
  Hindernis: Architekt → Organisationsentwickler: Abhaken nimmt die in 11001 genannten und von mir geprüften Stellen nicht an (wie beim Fachkritiker) (Anliegen 11360)
- [ ] Implementierer: Tests zu Item anhaltenUebergehen grün
- [ ] Architekt: Kritik am Code zu Item anhaltenUebergehen
- [ ] Reviewer: Kritik am Code zu Item anhaltenUebergehen
- [ ] Fachkritiker: Item anhaltenUebergehen abgenommen
- [ ] Planer: Item anhaltenUebergehen gelöscht
- [x] Architekt: Vertrag zu Item loslassenNebenDerKarte, bei beiden Hälften
- [x] Testautor: Tests zu Item loslassenNebenDerKarte
- [ ] Fachkritiker: Kritik an den Tests zu Item loslassenNebenDerKarte
  Hindernis: Fachkritiker → Testautor: Diese Tests sind grün, bevor der Code besteht: testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-aufDerArmeelisteVonSpielerEins], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-aufDerArmeelisteVonSpielerZwei], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-nebenDerKarte], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-aufDerArmeelisteVonSpielerEins], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-aufDerArmeelisteVonSpielerZwei], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-nebenDerKarte], testAuf28_1DerDienstSetztAmPunktDerLetztenStelleWieDasBeispielImVertrag. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. (Anliegen 11262)
- [ ] Architekt: Kritik an den Tests zu Item loslassenNebenDerKarte
  Hindernis: Architekt → Testautor: Drei neue Dienst-Tests vergleichen das Beispiel des Vertrags ganz statt nach T3 und werden rot, sobald Weirdboy oder Spinne in einer Armee stehen: testAuf28_1DerDienstSetztAmPunktDerLetztenStelleWieDasBeispielImVertrag (losgelassen.json), testAuf16_7DerDienstNenntNachDemZurücklegenKeineStelleWieDasBeispielImVertrag (Spielstand gegen zurückgelegt.json) und testAuf16_7DerDienstSetztNachDemZurücklegenNichtsWieDasBeispielImVertrag (zurückgelegt.json). Vergleiche mit imUmfangDes aus dienst.py wie in einheitZuruecklegenTest.py. (Anliegen 11260)
- [ ] Implementierer: Tests zu Item loslassenNebenDerKarte grün
- [ ] Architekt: Kritik am Code zu Item loslassenNebenDerKarte
- [ ] Reviewer: Kritik am Code zu Item loslassenNebenDerKarte
- [ ] Fachkritiker: Item loslassenNebenDerKarte abgenommen
- [ ] Planer: Item loslassenNebenDerKarte gelöscht
- [x] Architekt: Vertrag zu Item anhaltenAufDemWeg, bei beiden Hälften
- [ ] Testautor: Tests zu Item anhaltenAufDemWeg
- [ ] Fachkritiker: Kritik an den Tests zu Item anhaltenAufDemWeg
- [ ] Architekt: Kritik an den Tests zu Item anhaltenAufDemWeg
- [ ] Implementierer: Tests zu Item anhaltenAufDemWeg grün
- [ ] Architekt: Kritik am Code zu Item anhaltenAufDemWeg
- [ ] Reviewer: Kritik am Code zu Item anhaltenAufDemWeg
- [ ] Fachkritiker: Item anhaltenAufDemWeg abgenommen
- [ ] Planer: Item anhaltenAufDemWeg gelöscht
- [ ] Architekt: Vertrag zu Item fliegen, bei beiden Hälften
- [ ] Testautor: Tests zu Item fliegen
- [ ] Fachkritiker: Kritik an den Tests zu Item fliegen
- [ ] Architekt: Kritik an den Tests zu Item fliegen
- [ ] Implementierer: Tests zu Item fliegen grün
- [ ] Architekt: Kritik am Code zu Item fliegen
- [ ] Reviewer: Kritik am Code zu Item fliegen
- [ ] Fachkritiker: Item fliegen abgenommen
- [ ] Planer: Item fliegen gelöscht
- [ ] Architekt: Vertrag zu Item zuruecksetzenUndLuecken, bei beiden Hälften
- [ ] Testautor: Tests zu Item zuruecksetzenUndLuecken
- [ ] Fachkritiker: Kritik an den Tests zu Item zuruecksetzenUndLuecken
- [ ] Architekt: Kritik an den Tests zu Item zuruecksetzenUndLuecken
- [ ] Implementierer: Tests zu Item zuruecksetzenUndLuecken grün
- [ ] Architekt: Kritik am Code zu Item zuruecksetzenUndLuecken
- [ ] Reviewer: Kritik am Code zu Item zuruecksetzenUndLuecken
- [ ] Fachkritiker: Item zuruecksetzenUndLuecken abgenommen
- [ ] Planer: Item zuruecksetzenUndLuecken gelöscht
- [ ] Architekt: Vertrag zu Item ruhigeKarte, bei beiden Hälften
- [ ] Testautor: Tests zu Item ruhigeKarte
- [ ] Fachkritiker: Kritik an den Tests zu Item ruhigeKarte
- [ ] Architekt: Kritik an den Tests zu Item ruhigeKarte
- [ ] Implementierer: Tests zu Item ruhigeKarte grün
- [ ] Architekt: Kritik am Code zu Item ruhigeKarte
- [ ] Reviewer: Kritik am Code zu Item ruhigeKarte
- [ ] Fachkritiker: Item ruhigeKarte abgenommen
- [ ] Planer: Item ruhigeKarte gelöscht
- [ ] Anforderungsautor: Anliegen 10180 Etappe 2: Zurücksetzen, Ork-Psioniker, Weiterziehen nach dem Übergehen
- [ ] Testautor: Anliegen 7151 MIV-1.5: Armeen ohne Reihenfolge einmal vergleichen
- [x] Anforderungsautor: Anliegen 7800 Karte und Ebene klarer benennen
- [ ] Implementierer: Anliegen 8041 stelleAn in den Einheitstests einmal
- [ ] Implementierer: Anliegen 8261 Übergehen nach Vertrag, Angebot nach Auswahlwechsel
- [ ] Implementierer: Anliegen 8641 Namen und Wiederverwendung bei Grenzkreisen
- [ ] Testautor: Anliegen 8971 Mutationslücken in messen und im Katalog
- [ ] Anforderungsautor: Anliegen 9340 Fliegen der Canoptek-Spinne
- [ ] Testautor: Anliegen 9401 Test zu BEW-19
- [ ] Reviewer: DoD über das Inkrement
- [ ] Reviewer: Review geschrieben
- [ ] Fachkritiker: Kritik am Review
- [ ] Organisationsentwickler: Kritik am Review
- [ ] Stakeholder: Freigabe Review 10

## Freigabe
Freigabe: ja
Kommentar: .
