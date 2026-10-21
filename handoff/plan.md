# Plan · Zyklus 7

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md). Grundlage: Zyklusziel aus
[Review 6](review.md).

## Dein Happy Path nach Zyklus 7
1. Du startest Arbiter, er nennt immer `http://127.0.0.1:8040/`. Läuft er schon, startet er
   nicht und sagt, dass die Adresse belegt ist. (Item 1)
2. Spieler 2 klickt die Boyz in seiner Spalte an und klickt in seine Zone: Sie stehen als
   *Formation* da, neben „Aufstellen der Einheit beenden“ steht „Einheit zurücklegen“.
   (gebaut, Knopf: Item 2)
3. Er klickt „Einheit zurücklegen“: Die *Karte* ist leer, die Boyz bleiben *ausgewählt*, ein
   Klick in die Zone stellt sie neu auf. (Item 2)
4. Er zieht die Boyz an den Rand, der Zeiger rutscht über die Kante hinaus, auch auf eine
   Spalte: Loslassen *setzt* sie, wo die *Karte* sie zuletzt zeigte. (Item 2)
5. Er zieht einen Boy weit weg und klickt „Aufstellen der Einheit beenden“: ‚keine
   Kohärenz‘, dazu „zurück“ und „gemeinsam übergehen“. (Item 3)
6. „gemeinsam übergehen“: Die Boyz sind *aufgestellt*, Spieler 1 ist *an der Reihe*. Unten
   steht im *Protokoll*: Boyz, Spieler 2, ‚keine Kohärenz‘. Jede *Leiste* fährt per *Griff*
   ein und aus. (Item 3)

## Items
1. [Aufräumen und feste Adresse](../domaene/items/aufraeumenUndFesteAdresse.md): Schritt 1;
   dazu ohne sichtbare Änderung: die *Auswahl* entflechten (deine Antwort in 1652) und
   `seite.js` teilen, die über dem Höchstmaß liegt (1541).
2. [Einheit zurücklegen, Loslassen neben der Karte](../domaene/items/einheitZuruecklegen.md):
   Schritte 2 bis 4.
3. [Gemeinsam übergehen mit Protokoll](../domaene/items/gemeinsamUebergehen.md): Schritte 5,
   6.

Reihenfolge 1, 2, 3: Item 1 räumt die Stellen auf, an denen 2 und 3 bauen; 2 vor 3, weil
„zurücklegen“ einfacher ist und „zurück“ in AUF-13.3 auf das *Zurücklegen* trifft. In Item 1
laufen Adresse, *Auswahl* und `seite.js` getrennt. Risiko: Item 3, neu sind *Protokoll* und
*Leisten*; klemmt es, siehst du 1 und 2 trotzdem.
Testautor: Mit Item 2 kommt der Test zu AUF-16.8 wieder (Annahme, siehe unten). Mit Item 1
benennen Testautor und Implementierer *Ablage* in Armeeliste um (2221), sobald der
Anforderungsautor es in Glossar und Anforderungen getan hat.

## Abweichung vom Zyklusziel
Review 6 sagt: nach Plan 7 ist Etappe 1 erreicht. Das schaffen wir nicht in einem Zyklus.
Vor die drei Schritte des Zyklusziels kommt Item 1 (deine Entscheidungen 1650, 1652). Es
fehlen danach noch das Anhalten nach mehreren Weiterrücken und das Entlanggleiten an einer
fremden *Base* (Item „Anhalten auf dem Weg“, 2180;
dazu ist AUF-29.2 noch offen, 2212) und die Randfälle: AUF-18.7, 27, 22, 20.6, 16.7, 12.8, 3.9, 8.7,
8.8, *ruhige Karte* (QUE-7). Das ist Plan 8, danach ist Etappe 1 erreicht.

## Annahmen
- Die Spalte heißt *Armeeliste* (2221, deine Antwort A); bis zur Umbenennung steht im
  Glossar noch *Ablage*.
- Etappe 1 gilt, wie sie steht; dein „.“ steht noch aus.
- Der Test zu AUF-16.8 (Loslassen eines Modells einer *aufgestellten* *Einheit* neben
  *Karte* und Spalten springt zurück) kommt mit Item 2 wieder. Empfehlung: ja, er sichert
  das Gegenstück zu Schritt 4.

## Empfehlung
Gib die drei Items frei, wenn Schritte 1 bis 6 deinem Bild entsprechen.

## Offene Anliegen
- Vor der Freigabe: Ux [2241](anliegen/2241-griffPfeilEingefahren.md) (Pfeil am *Griff*,
  Item 3).
- An dich: [2221](anliegen/2221-ablageHeisstArmeeliste.md) (Nachprüfung). Vorschläge des
  Anforderungsautors: keine weiteren.
- Sonst: [Moderation](moderation.md).

## Fortschritt
- [ ] Architekt: Vertrag zu Item aufraeumenUndFesteAdresse, bei beiden Hälften
- [ ] Testautor: Tests zu Item aufraeumenUndFesteAdresse
- [ ] Fachkritiker: Kritik an den Tests zu Item aufraeumenUndFesteAdresse
- [ ] Architekt: Kritik an den Tests zu Item aufraeumenUndFesteAdresse
- [ ] Implementierer: Tests zu Item aufraeumenUndFesteAdresse grün
- [ ] Architekt: Kritik am Code zu Item aufraeumenUndFesteAdresse
- [ ] Reviewer: Kritik am Code zu Item aufraeumenUndFesteAdresse
- [ ] Fachkritiker: Item aufraeumenUndFesteAdresse abgenommen
- [ ] Planer: Item aufraeumenUndFesteAdresse gelöscht
- [ ] Architekt: Vertrag zu Item einheitZuruecklegen, bei beiden Hälften
- [ ] Testautor: Tests zu Item einheitZuruecklegen
- [ ] Fachkritiker: Kritik an den Tests zu Item einheitZuruecklegen
- [ ] Architekt: Kritik an den Tests zu Item einheitZuruecklegen
- [ ] Implementierer: Tests zu Item einheitZuruecklegen grün
- [ ] Architekt: Kritik am Code zu Item einheitZuruecklegen
- [ ] Reviewer: Kritik am Code zu Item einheitZuruecklegen
- [ ] Fachkritiker: Item einheitZuruecklegen abgenommen
- [ ] Planer: Item einheitZuruecklegen gelöscht
- [ ] Architekt: Vertrag zu Item gemeinsamUebergehen, bei beiden Hälften
- [ ] Testautor: Tests zu Item gemeinsamUebergehen
- [ ] Fachkritiker: Kritik an den Tests zu Item gemeinsamUebergehen
- [ ] Architekt: Kritik an den Tests zu Item gemeinsamUebergehen
- [ ] Implementierer: Tests zu Item gemeinsamUebergehen grün
- [ ] Architekt: Kritik am Code zu Item gemeinsamUebergehen
- [ ] Reviewer: Kritik am Code zu Item gemeinsamUebergehen
- [ ] Fachkritiker: Item gemeinsamUebergehen abgenommen
- [ ] Planer: Item gemeinsamUebergehen gelöscht
- [ ] Reviewer: DoD über das Inkrement
- [ ] Reviewer: Review geschrieben
- [ ] Stakeholder: Freigabe Review 7

## Freigabe
Freigabe: offen
Kommentar: .
