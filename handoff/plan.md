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
   *Modelle* stehen wieder, wo die Phase begann. (Item 4)

## Items
1. [Katalogwerte gliedern](../domaene/items/katalogwerteGliedern.md): Schritt 1; MIV-1.5.
2. [Gemeinsam übergehen mit Protokoll](../domaene/items/gemeinsamUebergehen.md): Schritt 2;
   BEW-8, QUE-5, QUE-6.
3. [Anhalten und Auswahl](../domaene/items/anhaltenUndAuswahl.md): Schritte 3 und 4; BEW-6,
   BEW-2.8, BEW-7, BEW-9, BEW-10, AUF-30.
4. [Grenzkreise und Vorrücken](../domaene/items/grenzkreise.md): Schritt 5; BEW-11, BEW-13,
   BEW-14, BEW-5, BEW-12.

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
- [ ] Architekt: Vertrag zu Item katalogwerteGliedern, bei beiden Hälften
- [ ] Testautor: Tests zu Item katalogwerteGliedern
- [ ] Fachkritiker: Kritik an den Tests zu Item katalogwerteGliedern
- [ ] Architekt: Kritik an den Tests zu Item katalogwerteGliedern
- [ ] Implementierer: Tests zu Item katalogwerteGliedern grün
- [ ] Architekt: Kritik am Code zu Item katalogwerteGliedern
- [ ] Reviewer: Kritik am Code zu Item katalogwerteGliedern
- [ ] Fachkritiker: Item katalogwerteGliedern abgenommen
- [ ] Planer: Item katalogwerteGliedern gelöscht
- [ ] Architekt: Vertrag zu Item gemeinsamUebergehen, bei beiden Hälften
- [ ] Testautor: Tests zu Item gemeinsamUebergehen
- [ ] Fachkritiker: Kritik an den Tests zu Item gemeinsamUebergehen
- [ ] Architekt: Kritik an den Tests zu Item gemeinsamUebergehen
- [ ] Implementierer: Tests zu Item gemeinsamUebergehen grün
- [ ] Architekt: Kritik am Code zu Item gemeinsamUebergehen
- [ ] Reviewer: Kritik am Code zu Item gemeinsamUebergehen
- [ ] Fachkritiker: Item gemeinsamUebergehen abgenommen
- [ ] Planer: Item gemeinsamUebergehen gelöscht
- [ ] Architekt: Vertrag zu Item anhaltenUndAuswahl, bei beiden Hälften
- [ ] Testautor: Tests zu Item anhaltenUndAuswahl
- [ ] Fachkritiker: Kritik an den Tests zu Item anhaltenUndAuswahl
- [ ] Architekt: Kritik an den Tests zu Item anhaltenUndAuswahl
- [ ] Implementierer: Tests zu Item anhaltenUndAuswahl grün
- [ ] Architekt: Kritik am Code zu Item anhaltenUndAuswahl
- [ ] Reviewer: Kritik am Code zu Item anhaltenUndAuswahl
- [ ] Fachkritiker: Item anhaltenUndAuswahl abgenommen
- [ ] Planer: Item anhaltenUndAuswahl gelöscht
- [ ] Architekt: Vertrag zu Item grenzkreise, bei beiden Hälften
- [ ] Testautor: Tests zu Item grenzkreise
- [ ] Fachkritiker: Kritik an den Tests zu Item grenzkreise
- [ ] Architekt: Kritik an den Tests zu Item grenzkreise
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
Freigabe: offen
Kommentar: .
