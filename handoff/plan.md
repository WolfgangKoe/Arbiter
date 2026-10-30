# Plan · Zyklus 9

Etappe: [2 · Phasen und Bewegungsphase](../domaene/etappen/02-bewegen.md). Grundlage:
Zyklusziel aus [Review 8](review.md), Abweichungen unten.

## Dein Happy Path nach Zyklus 9
1. Arbiter startet, ihr stellt auf, wählt den ersten Zug und kommt in die *Bewegungsphase* wie
   bisher. (Item 1)
2. Sperrt Arbiter beim Loslassen ‚über eine Base‘, klickt ihr „gemeinsam übergehen“: Die
   *Modelle* stehen, wo ihr losgelassen habt, das *Protokoll* in der unteren *Leiste* nennt
   *Einheit*, *Spieler* und *Grund*. Jede *Leiste* fährt per *Griff* ein und aus. ‚keine
   Kohärenz‘ bleibt ohne Übergehen. (Item 2)
3. Zieht ihr an die *Spielfeldkante* oder auf einen Gegner zu, hält Arbiter an der Kante oder
   1″ vor seiner *Base* an. *Modelle* des Gegners lassen sich nicht ziehen. (Item 3)
4. Ein Klick auf einen Boy der *ausgewählten* Boyz: Nur er zieht. Noch ein Klick: wieder die
   ganze *Einheit*. Ein Klick auf die leere *Karte* hebt die *Auswahl* auf. Schon beim
   Aufstellen wählt ein Klick auch eine *aufgestellte* *Einheit* aus. (Item 3)
5. Um die *ausgewählte* *Einheit* zeigt die *Karte* leicht, bis wohin sie zieht (*Einhüllende*
   ihrer *Grenzkreise*), um jede gegnerische ihre *Nahkampfreichweite*. Nach „Vorrücken“
   erscheinen sechs Kreise +1″ bis +6″; ihr klickt in den Ring eures Wurfs, nur er bleibt, die
   *Modelle* ziehen bis *Bewegungsweite* plus Wurf. Verklickt: „Vorrücken zurücknehmen“, die
   *Modelle* stehen wieder, wo die Phase begann. Wählt ihr gezogene Boyz wieder aus, gelten
   die *Grenzkreise* ab ihren *Stellen* zu Beginn der Phase. (Item 4)

## Items
1. [Katalogwerte gliedern](../domaene/items/katalogwerteGliedern.md): Schritt 1; MIV-1.5.
2. [Gemeinsam übergehen mit Protokoll](../domaene/items/gemeinsamUebergehen.md): Schritt 2;
   BEW-8, QUE-5, QUE-6.
3. [Anhalten und Auswahl](../domaene/items/anhaltenUndAuswahl.md): Schritte 3 und 4; BEW-6,
   BEW-2.8, BEW-7, BEW-9, BEW-10, AUF-30.
4. [Grenzkreise und Vorrücken](../domaene/items/grenzkreise.md): Schritt 5; BEW-11, BEW-13,
   BEW-14, BEW-5, BEW-12, BEW-15.

Reihenfolge 1 bis 4: Arbiter startet seit der neuen *Ausgangslage* nicht; Item 1 behebt das.
Item 2 vor 3: BEW-2.8 *setzt* nach BEW-8.2. Item 3 vor 4: Ein Boy als *Ebene* (BEW-7) zeigt
seinen *Grenzkreis* (BEW-11.1), der Klick auf einen Kreis hebt die *Auswahl* nicht auf
(BEW-5.3, BEW-9.1). Item 4 kostet am meisten Code (*Einhüllende*, Anliegen 7004), darum
zuletzt: Hängt es, bekommst du Schritte 1 bis 4, Item 4 rückt in Plan 10.

## Abweichungen vom Zyklusziel
- Dazu Item 1 (4882 F1 A), BEW-7 (6420), BEW-10 und AUF-30 (6300, 6996), die *Grenzkreise*:
  Mit ihnen wählt ihr den *Vorrückwurf* (6998 F1), ohne sie kein *Vorrücken* (6999). Kosten:
  vier statt drei Items, die Technikphase dauert länger; ohne Item 4 käme *Vorrücken* erst
  mit Plan 10.
- Kante und *Nahkampfreichweite* halten an statt zu sperren (6400); der Test aus 6241 prüft
  dann BEW-6.2.
- „Jede *Einheit* nur einmal“ ohne neues Kriterium: Korrigieren bleibt (7000 F4 A).
- BEW-15 auf deine Frage: Sonst zeigten die *Grenzkreise* nach erneuter *Auswahl* zu weit.

Vorher in der Technikphase: Anliegen 6102, 6241, 6290.

## Danach
Zurücksetzen und was Arbiter an einer gezogenen *Einheit* zeigt (7000 F3), Anhalten übergehen
(7000 F2), Ork-Psioniker und Canoptek-Spinne, Loslassen neben der *Karte*, ruhige *Karte*, die
Lücken aus 6986, „Phase beenden“ nur im Zug (QUE-11). Ich schätze zwei Zyklen bis Etappe 2.

## Empfehlung
Gib die vier Items frei, wenn Schritte 1 bis 5 deinem Bild entsprechen; damit gelten die
Begriffe aus 6998, 7000, 7005.

## Offene Anliegen
- Von dir beantwortet, der Anforderungsautor prüft nach:
  Anliegen 6998,
  Anliegen 7000,
  Anliegen 7005.
- Deine Nachprüfung: [6400](anliegen/6400-anhaltenVorDerNahkampfreichweite.md),
  [6410](anliegen/6410-grenzkreiseNahkampfUndBewegung.md),
  [6420](anliegen/6420-einzelnesModellNachAuswahlDerEinheitZiehen.md).
- Übrige: [Moderation](moderation.md).

## Fortschritt
- [x] Architekt: Vertrag zu Item katalogwerteGliedern, bei beiden Hälften
- [x] Testautor: Tests zu Item katalogwerteGliedern
- [x] Fachkritiker: Kritik an den Tests zu Item katalogwerteGliedern
- [x] Architekt: Kritik an den Tests zu Item katalogwerteGliedern
  Hindernis: Architekt → Testautor: Eine Testhilfe sucht die Bewegungsweite noch in der alten Ausgangslage; die Tests der Bewegungsphase laufen darum nicht. (Anliegen 7150)
- [x] Implementierer: Tests zu Item katalogwerteGliedern grün
- [ ] Architekt: Kritik am Code zu Item katalogwerteGliedern
  Hindernis: Architekt → Implementierer: Zwei neue Dateien des Katalogs bringen Erklärtexte mit, die die Regel zum Code verbietet; eine Prüfung ist darum rot. (Anliegen 7190)
- [x] Reviewer: Kritik am Code zu Item katalogwerteGliedern
  Hindernis: Reviewer → Implementierer: Im Katalog heißt der Eintrag einer Modellart Profil, obwohl er auch den Durchmesser hält, und ein Einheitstest bindet eine Konstante per Standardargument; der Implementierer benennt um. (Anliegen 7200)
- [ ] Fachkritiker: Item katalogwerteGliedern abgenommen
- [ ] Planer: Item katalogwerteGliedern gelöscht
- [x] Architekt: Vertrag zu Item gemeinsamUebergehen, bei beiden Hälften
- [x] Testautor: Tests zu Item gemeinsamUebergehen
  Hindernis: Testautor → Planer: Die Tests zu BEW-8, QUE-5 und QUE-6 stehen vollständig, Formprüfungen grün. Das Häkchen setzt sich nicht, weil die Zeile Abhängigkeit in domaene/items/gemeinsamUebergehen.md BEW-2 nennt; die Prüfung zählt damit BEW-2 zum Item, und BEW-2.8 gehört zu Item 3 (anhaltenUndAuswahl) und hat dort noch keinen Test. Empfehlung: in der Abhängigkeit die Kennung streichen (die Sperren beim Ziehen stehen) statt BEW-2 zu nennen; Alternative für den Regelumsetzer: itemKriterienGetestet liest nur die Zeile Umfang. (Anliegen 7210)
- [x] Fachkritiker: Kritik an den Tests zu Item gemeinsamUebergehen
  Hindernis: Fachkritiker → Testautor: Ein Test zu „gemeinsam übergehen“ ist schon grün, obwohl es den Knopf noch nicht gibt; er prüft nicht, dass der Knopf erst da war und dann verschwindet. (Anliegen 7300)
- [x] Architekt: Kritik an den Tests zu Item gemeinsamUebergehen
  Hindernis: Architekt → Testautor: Ein Test übergab die übergangenen Gründe ohne Namen, anders als der Vertrag, und ein Test zu „gemeinsam übergehen nicht mehr angeboten“ war ohne Knopf schon grün; beides ist berichtigt, der Haken gilt seit der Nachprüfung. (Anliegen 7320)
- [ ] Implementierer: Tests zu Item gemeinsamUebergehen grün
- [ ] Architekt: Kritik am Code zu Item gemeinsamUebergehen
- [ ] Reviewer: Kritik am Code zu Item gemeinsamUebergehen
- [ ] Fachkritiker: Item gemeinsamUebergehen abgenommen
- [ ] Planer: Item gemeinsamUebergehen gelöscht
- [x] Architekt: Vertrag zu Item anhaltenUndAuswahl, bei beiden Hälften
- [x] Testautor: Tests zu Item anhaltenUndAuswahl
- [x] Fachkritiker: Kritik an den Tests zu Item anhaltenUndAuswahl
  Hindernis: Fachkritiker → Testautor: Drei Tests zum Klick auf das Modell der Ebene sind schon grün, obwohl ein Klick heute nie ein Modell zur Ebene macht; sie prüfen nicht, dass vorher ein Modell die Ebene war. (Anliegen 7400)
- [x] Architekt: Kritik an den Tests zu Item anhaltenUndAuswahl
  Hindernis: Architekt → Testautor: Ein Test zur Auswahl einer aufgestellten Einheit heißt „ohne Ebene“, obwohl die ganze Einheit ihre Ebene ist; der Testautor benennt ihn um. (Anliegen 7420); beseitigt: Commit „anhaltenUndAuswahl: Tests und Kritik an den Tests (7400, 7420, 7600)“
- [ ] Implementierer: Tests zu Item anhaltenUndAuswahl grün
- [ ] Architekt: Kritik am Code zu Item anhaltenUndAuswahl
- [ ] Reviewer: Kritik am Code zu Item anhaltenUndAuswahl
- [ ] Fachkritiker: Item anhaltenUndAuswahl abgenommen
- [ ] Planer: Item anhaltenUndAuswahl gelöscht
- [x] Architekt: Vertrag zu Item grenzkreise, bei beiden Hälften
- [x] Testautor: Tests zu Item grenzkreise
- [ ] Fachkritiker: Kritik an den Tests zu Item grenzkreise
  Hindernis: Fachkritiker → Testautor: 13 Testfälle zu Grenzkreisen und Vorrücken ziehen die ganze Einheit gegen die Nachbareinheit und werden so nie grün; ein Test der Seite prüft nicht, dass der Kreis des Wurfs verschwindet (Anliegen 7640)
- [ ] Architekt: Kritik an den Tests zu Item grenzkreise
  Hindernis: Architekt → Testautor: Die neuen Grenzen im Spielstand machen vier ältere Tests rot, die den ganzen Spielstand der Schlacht mit einem Beispiel vergleichen; drei Tests zur Seite sind ohne Code schon grün, einer prüft nach dem Zurücknehmen die Grenze nicht. Der Testautor vergleicht nur die Schlüssel des Beispiels und baut die drei Tests um. (Anliegen 7660)
- [ ] Implementierer: Tests zu Item grenzkreise grün
- [ ] Architekt: Kritik am Code zu Item grenzkreise
- [ ] Reviewer: Kritik am Code zu Item grenzkreise
- [ ] Fachkritiker: Item grenzkreise abgenommen
- [ ] Planer: Item grenzkreise gelöscht
- [ ] Reviewer: DoD über das Inkrement
- [ ] Reviewer: Review geschrieben
- [ ] Fachkritiker: Kritik am Review
- [ ] Organisationsentwickler: Kritik am Review
- [ ] Stakeholder: Freigabe Review 9

## Freigabe
Freigabe: ja
Kommentar: .
