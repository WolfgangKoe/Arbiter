# Plan · Zyklus 8

Etappe: [2 · Phasen und Bewegungsphase](../domaene/etappen/02-bewegen.md). Grundlage:
Zyklusziel aus [Review 7](review.md), ohne Abweichung.

## Dein Happy Path nach Zyklus 8
1. Ihr stellt beide Armeen auf wie bisher. Wer am Tisch den Roll-off gewinnt, wählt am
   Bildschirm, wer den ersten Zug hat. (Item 2)
2. Arbiter zeigt Schlachtrunde 1, den Spieler am Zug und die Phase. Jede Phase außer der
   Bewegungsphase ist leer, ihr beendet sie ohne Spielhandlung. (Item 2)
3. In der Bewegungsphase zieht ihr eine *Einheit* in einem Normal Move. Weiter als M, über
   eine fremde *Base* oder am Ende ohne *Kohärenz* sperrt Arbiter. (Item 3)
4. Nach der fünften Schlachtrunde endet die Schlacht. (Item 2)

Noch nicht: jede *Einheit* nur einmal ziehen, Advance, Zurücksetzen, über die Kante, Engagement Range, gemeinsam übergehen mit
*Protokoll*, Ork-Psioniker und Canoptek-Spinne, Loslassen neben der *Karte*. Sie bleiben für
die nächsten zwei bis drei Zyklen von Etappe 2.

## Items
1. [Architektur umordnen](../domaene/items/architekturUmordnen.md): am Bildschirm nichts.
   Deine Entscheidung aus Anliegen 2570 (F3).
2. [Phasen und Schlachtrunden](../domaene/items/phasenUndSchlachtrunden.md): Schritte 1, 2, 4;
   [QUE-9](../domaene/anforderungen/querschnitt/ersterZug.md),
   [QUE-10](../domaene/anforderungen/querschnitt/schlachtrunden.md).
3. [Normal Move](../domaene/items/normalMove.md): Schritt 3;
   [BEW-1](../domaene/anforderungen/phasen/bewegung/normalMove.md),
   [BEW-2](../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md),
   [AUF-20.6](../domaene/anforderungen/phasen/aufstellen/ebene.md): ein Klick auf ein
   *Modell* wählt die ganze *Einheit*, ein Zug verschiebt sie als Block.

Reihenfolge 1, 2, 3: Item 1 ordnet die Regeln, nach denen 2 und 3 gebaut werden; der Normal
Move braucht die Bewegungsphase aus Item 2. Das Risiko liegt bei Item 3, dem ersten Ziehen
außerhalb des Aufstellens.

## Noch nicht bereit
Die Anforderungen zu Items 2 und 3 stehen, die Items nennen ihre Kriterien. Ux zeichnet die
Mockups, Fachkritiker und Architekt prüfen die Anforderungen; danach ist der Plan zur
Freigabe bereit. Jede Anforderung nennt ihre Etappe; so zählt der Stand ab Retro 8 „Etappe
2: x von y Kriterien belegt“, wie du in Anliegen 3550 gewählt hast (Anliegen 3661).

## Empfehlung
Gib die drei Items frei, sobald die Kriterien stehen und Schritte 1 bis 4 deinem Bild
entsprechen.

## Offene Anliegen
- An dich, vom Anforderungsautor: [4280](anliegen/4280-begriffeUndAnnahmenZuPlan8.md),
  neue Begriffe, Kürzel BEW, wie der Weg gemessen wird, M des Overlords, Knöpfe. Wir bauen
  mit seinen Empfehlungen; „.“ genügt, wenn sie dir passen. Eine spätere Änderung kostet
  neue Kennungen und Tests.
- Sonst: [Moderation](moderation.md).

## Fortschritt
- [ ] Architekt: Vertrag zu Item architekturUmordnen, bei beiden Hälften
- [ ] Testautor: Tests zu Item architekturUmordnen
- [ ] Fachkritiker: Kritik an den Tests zu Item architekturUmordnen
- [ ] Architekt: Kritik an den Tests zu Item architekturUmordnen
- [ ] Implementierer: Tests zu Item architekturUmordnen grün
- [ ] Architekt: Kritik am Code zu Item architekturUmordnen
- [ ] Reviewer: Kritik am Code zu Item architekturUmordnen
- [ ] Fachkritiker: Item architekturUmordnen abgenommen
- [ ] Planer: Item architekturUmordnen gelöscht
- [ ] Architekt: Vertrag zu Item phasenUndSchlachtrunden, bei beiden Hälften
- [ ] Testautor: Tests zu Item phasenUndSchlachtrunden
- [ ] Fachkritiker: Kritik an den Tests zu Item phasenUndSchlachtrunden
- [ ] Architekt: Kritik an den Tests zu Item phasenUndSchlachtrunden
- [ ] Implementierer: Tests zu Item phasenUndSchlachtrunden grün
- [ ] Architekt: Kritik am Code zu Item phasenUndSchlachtrunden
- [ ] Reviewer: Kritik am Code zu Item phasenUndSchlachtrunden
- [ ] Fachkritiker: Item phasenUndSchlachtrunden abgenommen
- [ ] Planer: Item phasenUndSchlachtrunden gelöscht
- [ ] Architekt: Vertrag zu Item normalMove, bei beiden Hälften
- [ ] Testautor: Tests zu Item normalMove
- [ ] Fachkritiker: Kritik an den Tests zu Item normalMove
- [ ] Architekt: Kritik an den Tests zu Item normalMove
- [ ] Implementierer: Tests zu Item normalMove grün
- [ ] Architekt: Kritik am Code zu Item normalMove
- [ ] Reviewer: Kritik am Code zu Item normalMove
- [ ] Fachkritiker: Item normalMove abgenommen
- [ ] Planer: Item normalMove gelöscht
- [ ] Reviewer: DoD über das Inkrement
- [ ] Reviewer: Review geschrieben
- [ ] Fachkritiker: Kritik am Review
- [ ] Organisationsentwickler: Kritik am Review
- [ ] Stakeholder: Freigabe Review 8

## Freigabe
Freigabe: offen
Kommentar: .
