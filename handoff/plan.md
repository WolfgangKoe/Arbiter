# Plan · Zyklus 8

Etappe: [2 · Phasen und Bewegungsphase](../domaene/etappen/02-bewegen.md). Grundlage:
Zyklusziel aus [Review 7](review.md), ohne Abweichung.

## Dein Happy Path nach Zyklus 8
1. Ihr stellt beide Armeen auf wie bisher. Wer am Tisch den Roll-off gewinnt, klickt in
   seiner *Armeeliste* „Erster Zug“. (Item 2)
2. Arbiter zeigt Schlachtrunde 1, den Spieler am Zug und die Phase. Jede Phase außer der
   Bewegungsphase ist leer, ihr beendet sie mit „Phase beenden“. (Item 2)
3. In der Bewegungsphase zieht ihr eine *Einheit* in einer *Normalen Bewegung* und
   korrigiert sie nach Belieben. Weiter als ihre *Bewegungsweite* hält Arbiter sie an, über eine fremde *Base*
   sperrt er beim Loslassen, „Phase beenden“ ohne *Kohärenz*. (Item 3)
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
   [BEW-3](../domaene/anforderungen/phasen/bewegung/anhaltenAnDerBewegungsweite.md),
   [BEW-4](../domaene/anforderungen/phasen/bewegung/beenden.md),
   [AUF-20.6](../domaene/anforderungen/phasen/aufstellen/ebene.md): ein Klick auf ein
   *Modell* wählt die ganze *Einheit*, ein Zug verschiebt sie als Block.

Reihenfolge 1, 2, 3: Item 1 ordnet die Regeln, nach denen 2 und 3 gebaut werden; die
*Normale Bewegung* braucht die Bewegungsphase aus Item 2. Am meisten Code kostet Item 2: Die
*Stellen* gehören danach der *Schlacht*, nicht mehr der *Aufstellung*. Neu ist in Item 3 nur
das exakte Messen der *Distanz*.

Anforderungen, Mockups und ihre Prüfung stehen; die Items verlinken ihre Mockups. Jede
Anforderung nennt ihre Etappe; so zählt der Stand ab Retro 8 „Etappe 2: x von y Kriterien
belegt“, wie du in Anliegen 3550 gewählt hast (Anliegen 3661).

## Empfehlung
Gib die drei Items frei, wenn Schritte 1 bis 4 deinem Bild entsprechen.

## Offene Anliegen
- An dich: keine. Deine Antworten aus Anliegen 4280 stehen in den Items; das Datenmodell
  aus F7 prüft der Architekt in Anliegen 4621.
- Sonst: [Moderation](moderation.md).

## Fortschritt
- [x] Architekt: Vertrag zu Item architekturUmordnen, bei beiden Hälften
- [x] Testautor: Tests zu Item architekturUmordnen
- [x] Fachkritiker: Kritik an den Tests zu Item architekturUmordnen
- [x] Architekt: Kritik an den Tests zu Item architekturUmordnen
- [x] Implementierer: Tests zu Item architekturUmordnen grün
- [x] Architekt: Kritik am Code zu Item architekturUmordnen
- [x] Reviewer: Kritik am Code zu Item architekturUmordnen
- [x] Fachkritiker: Item architekturUmordnen abgenommen
- [x] Planer: Item architekturUmordnen gelöscht
- [x] Architekt: Vertrag zu Item phasenUndSchlachtrunden, bei beiden Hälften
- [x] Testautor: Tests zu Item phasenUndSchlachtrunden
- [x] Fachkritiker: Kritik an den Tests zu Item phasenUndSchlachtrunden
  Hindernis: Fachkritiker → Testautor: QUE-10.3 und 10.4 prüfen den ersten Zug nur bei Spieler 1 (Anliegen 4900); beseitigt: Commit „Technikphase 8: Architektur umgeordnet, Verträge und rote Tests“
  Hindernis: Fachkritiker → Testautor: QUE-10.1 prüft die Nummer der Schlachtrunde nur bei 1 (Anliegen 5240); beseitigt: Commit „Tests nachgebessert, 5180 in Runde 2“
- [x] Architekt: Kritik an den Tests zu Item phasenUndSchlachtrunden
- [x] Implementierer: Tests zu Item phasenUndSchlachtrunden grün
- [x] Architekt: Kritik am Code zu Item phasenUndSchlachtrunden
  Hindernis: Architekt → Implementierer: Knöpfe nicht als Tabelle (O5), Spielernummer außerhalb kennungen.py (W2) (Anliegen 5680); beseitigt: Commit „phasenUndSchlachtrunden: Knöpfe als Tabelle, Auswahl bleibt bei der Aufstellung“
- [x] Reviewer: Kritik am Code zu Item phasenUndSchlachtrunden
- [x] Fachkritiker: Item phasenUndSchlachtrunden abgenommen
- [x] Planer: Item phasenUndSchlachtrunden gelöscht
- [x] Architekt: Vertrag zu Item normalMove, bei beiden Hälften
- [x] Testautor: Tests zu Item normalMove
- [x] Fachkritiker: Kritik an den Tests zu Item normalMove
  Hindernis: Fachkritiker → Testautor: BEW-2.4 ohne Überdeckung, Distanz nur auf Achsen, BEW-2.3 nie zwei Gründe (Anliegen 4900); beseitigt: Commit „Technikphase 8: Architektur umgeordnet, Verträge und rote Tests“
  Hindernis: Fachkritiker → Testautor: BEW-1.4 verlangt beim Halten über die Bewegungsweite ein Bild, das weder Kriterium noch V10 nennen (Anliegen 5240); beseitigt: Commit „Tests nachgebessert, 5180 in Runde 2“
  Hindernis: Fachkritiker → Testautor: Kein Test sperrt den Block, wenn ein nicht gezogenes Modell über eine fremde Base geht (BEW-2.5) (Anliegen 5760); beseitigt: Commit „normalMove: Bewegungsphase ohne Ende je Einheit“
- [x] Architekt: Kritik an den Tests zu Item normalMove
- [x] Implementierer: Tests zu Item normalMove grün
  Hindernis: Implementierer → Testautor: testAuf8_2EinModellBleibtBeiWenigerAlsDerZugschwelleAbweichungAnSeinerStelle (ziehenTest.py) fordert, dass eine Bewegung unter der Zugschwelle keine ändernde Anfrage sendet. Sie ist aber ein Klick auf ein gesetztes Modell einer nicht ausgewählten Einheit in der Aufstellung; AUF-20.6 und V14 verlangen dafür PUT …/anklicken (Einheit wird ausgewählt). Beides zugleich ist nicht erfüllbar. Empfehlung: der Test wählt zuvor die Einheit der Boyz aus (dann sendet der Klick nur ebene, auch eine ändernde Anfrage; besser: Test prüft nur, dass die Stellen unverändert bleiben und keine PUT …/stelle gesendet wird) oder nimmt anklicken ausdrücklich aus. (Anliegen 6060); beseitigt: Commit „normalMove: Zug folgt dem Zeiger, Kritik am Code“
- [x] Architekt: Kritik am Code zu Item normalMove
  Hindernis: Architekt → Testautor: AUF-8.7 hat keinen Akzeptanztest, bedienung.js setzt es aber schon um (stelleDesZugs: vorige Stelle plus Weg des Zeigers seit dem Greifen; Anliegen 6100 F1 A); Akzeptanztests entstehen vor dem Code. Empfehlung: in ziehenTest.py ein gesetztes Modell abseits seiner Mitte greifen, mit Maus und Finger ziehen und loslassen; die Stelle danach ist die vorige plus der Weg des Zeigers, auf einen Pixel genau (B5), nicht der Punkt unter dem Zeiger. (Anliegen 6101); beseitigt: Commit „normalMove: Gründe als Tabelle, Test zu AUF-8.7, Rundung in S2“
  Hindernis: Architekt → Implementierer: S2 nennt jetzt die Rundung jeder Zahl einer Anfrage (technik/architektur/domaene.md, Anliegen 6121), Prüft: anwendungTest.py; dort fehlt der Einheitstest. Empfehlung: ein Test, der x = 160/127 und y = 121/3 als JSON-double schickt, einmal als Körper von PUT …/stelle (V5), einmal als Abfrage …/stelleBeimLoslassen (V10), und in der Domäne genau diese Fraction findet; ohne limit_denominator ist er rot. (Anliegen 6180); beseitigt: Commit „normalMove: Gründe als Tabelle, Test zu AUF-8.7, Rundung in S2“
- [x] Reviewer: Kritik am Code zu Item normalMove
  Hindernis: Reviewer → Implementierer: Grund des Setzens und Ziehens als Zweig statt Zeile der Tabelle (D4) (Anliegen 6120); beseitigt: Commit „normalMove: Gründe als Tabelle, Test zu AUF-8.7, Rundung in S2“
  Hindernis: Reviewer → Architekt: Rundung jeder Zahl der Anfrage auf Nenner 10^6 steht nicht in S2 (Anliegen 6121); beseitigt: Commit „normalMove: Kritik des Architekten am Code abgeschlossen“
- [x] Fachkritiker: Item normalMove abgenommen
- [ ] Planer: Item normalMove gelöscht
- [ ] Reviewer: DoD über das Inkrement
- [ ] Reviewer: Review geschrieben
- [ ] Fachkritiker: Kritik am Review
- [ ] Organisationsentwickler: Kritik am Review
- [ ] Stakeholder: Freigabe Review 8

## Freigabe
Freigabe: ja
Kommentar: .
