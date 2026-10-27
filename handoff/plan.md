# Plan · Zyklus 8

Etappe: [2 · Phasen und Bewegungsphase](../domaene/etappen/02-bewegen.md). Grundlage:
Zyklusziel aus [Review 7](review.md), ohne Abweichung.

## Dein Happy Path nach Zyklus 8
1. Ihr stellt beide Armeen auf wie bisher. Wer am Tisch den Roll-off gewinnt, klickt in
   seiner *Armeeliste* „Erster Zug“. (Item 2)
2. Arbiter zeigt Schlachtrunde 1, den Spieler am Zug und die Phase. Jede Phase außer der
   Bewegungsphase ist leer, ihr beendet sie mit „Phase beenden“. (Item 2)
3. In der Bewegungsphase zieht ihr eine *Einheit* in einer *Normalen Bewegung* und klickt
   „Bewegung der Einheit beenden“. Weiter als *B* oder über eine fremde *Base* sperrt
   Arbiter beim Loslassen, ohne *Kohärenz* beim Beenden. (Item 3)
4. Nach der fünften Schlachtrunde endet die Schlacht. (Item 2)

Noch nicht: jede *Einheit* nur einmal ziehen, Advance, Zurücksetzen, über die Kante,
*Nahkampfreichweite*, *gemeinsam übergehen* mit *Protokoll*, Ork-Psioniker und
Canoptek-Spinne, Loslassen neben der *Karte*. Sie bleiben für die nächsten zwei bis drei
Zyklen von Etappe 2.

## Items
1. [Architektur umordnen](../domaene/items/architekturUmordnen.md): am Bildschirm nichts.
   Deine Entscheidung aus Anliegen 2570 (F3).
2. [Phasen und Schlachtrunden](../domaene/items/phasenUndSchlachtrunden.md): Schritte 1, 2, 4;
   [QUE-9](../domaene/anforderungen/querschnitt/ersterZug.md),
   [QUE-10](../domaene/anforderungen/querschnitt/schlachtrunden.md).
3. [Normale Bewegung](../domaene/items/normalMove.md): Schritt 3;
   [BEW-1](../domaene/anforderungen/phasen/bewegung/normaleBewegung.md),
   [BEW-2](../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md),
   [AUF-20.6](../domaene/anforderungen/phasen/aufstellen/ebene.md): ein Klick auf ein
   *Modell* wählt die ganze *Einheit*, ein Zug verschiebt sie als Block.

Reihenfolge 1, 2, 3: Item 1 ordnet die Regeln, nach denen 2 und 3 gebaut werden; die
*Normale Bewegung* braucht die Bewegungsphase aus Item 2. Das Risiko liegt bei Item 3, dem
ersten Ziehen außerhalb des Aufstellens.

## Noch nicht bereit
Anforderungen, Mockups und ihre Prüfung stehen; die Items verlinken ihre Mockups. Es fehlen:
- Anliegen 4402: Die *Distanz* zählt noch über
  „Phase beenden“ hinaus; vergisst ihr „Bewegung der Einheit beenden“, sperrt ‚weiter als B‘
  in eurer nächsten Bewegungsphase zu Unrecht. Der Anforderungsautor berichtigt es.
- Anliegen 4421: Ux schreibt ‚weiter als B‘ ins Mockup.

Jede Anforderung nennt ihre Etappe; so zählt der Stand ab Retro 8 „Etappe 2: x von y
Kriterien belegt“, wie du in Anliegen 3550 gewählt hast (Anliegen 3661).

## Empfehlung
Gib die drei Items frei, sobald 4402 und 4421 erledigt sind und Schritte 1 bis 4 deinem
Bild entsprechen.

## Offene Anliegen
- An dich, vom Anforderungsautor: Anliegen 4280.
  Umgesetzt sind deine Antworten: *Normale Bewegung* und *B* (F1), gerade Strecken (F3),
  Overlord 6″ (F4), Knöpfe (F5). Offen: F6, welches Kürzel, auf deine Rückfrage zu F2, und
  F7, wann wir über die Daten aus Arbiter-old entscheiden. Bis zu deiner Antwort gilt die
  Empfehlung A; ein anderes Kürzel kostet später neue Kennungen und Tests.
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
