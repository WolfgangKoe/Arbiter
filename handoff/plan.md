# Plan · Zyklus 7

Etappe: [1 · Aufstellen](../domaene/etappen/01-aufstellen.md), neu gefasst nach deinem Schnitt
(Anliegen 2361 bis Anliegen 2364);
die nächste ist [2 · Phasen und Bewegungsphase](../domaene/etappen/02-bewegen.md). Grundlage:
Zyklusziel aus [Review 6](review.md).

## Dein Happy Path nach Zyklus 7
1. Du startest Arbiter, er nennt immer `http://127.0.0.1:8040/`. Läuft er schon, startet er
   nicht und sagt, dass die Adresse belegt ist. (Item 1)
2. Spieler 2 klickt die Necron Warriors in seiner *Armeeliste* an und klickt in seine Zone:
   Sie stehen als *Formation* da, neben „Aufstellen der Einheit beenden“ steht „Einheit
   zurücklegen“. (gebaut, Knopf: Item 2)
3. Er klickt „Einheit zurücklegen“: Die *Karte* ist leer, die Necron Warriors bleiben
   *ausgewählt*, ein Klick in die Zone stellt sie neu auf. (Item 2)
4. Er klickt einen Necron Warrior an, nur er ist golden umrandet, und zieht ihn weit weg.
   „Aufstellen der Einheit beenden“ bringt ‚keine Kohärenz‘, nichts zum Übergehen. (gebaut)
5. Er klickt „Einheit zurücklegen“ und stellt die Necron Warriors per Klick neu auf.
   „Aufstellen der Einheit beenden“: Spieler 1 ist *an der Reihe*. (Item 2)

## Items
1. [Aufräumen und feste Adresse](../domaene/items/aufraeumenUndFesteAdresse.md): Schritt 1;
   dazu ohne sichtbare Änderung: die *Auswahl* entflechten (deine Antwort in 1652),
   `seite.js` teilen, die über dem Höchstmaß liegt (1541), *Ablage* heißt auch in Code und
   Tests *Armeeliste* (2221), und „zurück“ ohne *Sperre* (AUF-17) samt Test entfernen, denn
   „zurück“ gibt es nicht mehr. Ebenso die *Sperre* ‚nicht wählbar‘ für ein *Modell*, das
   jemand auf eine *Armeeliste* zieht (AUF-8.4): Dort springt es künftig still zurück, denn
   in die *Armeeliste* zieht man nicht mehr (2220 F4 A, Anliegen 2410).
2. [Einheit zurücklegen](../domaene/items/einheitZuruecklegen.md): Schritte 2, 3 und 5.

Reihenfolge 1, 2: Item 1 räumt die Stellen auf, an denen Item 2 baut. Beide sind klein;
das Risiko liegt bei Item 1, wo *Auswahl*, `seite.js` und Adresse getrennt laufen.

## Abweichung vom Zyklusziel
Review 6 nennt drei Schritte. Nach deinem Schnitt bleibt in Plan 7 nur „Einheit
zurücklegen“. Gemeinsam übergehen und das *Protokoll* kommen mit den *Sperren* des Normal
Move in Etappe 2, ebenso das Loslassen neben der *Karte*, das der Normal Move mitbenutzt
(2361 F1, F2). Davor kommt Item 1
(deine Entscheidungen 1650, 1652). Nach Plan 7 ist Etappe 1 erreicht, wie das Zyklusziel sagt. Die Randfälle nur des Aufstellens (Item
randfaelleDesAufstellens) warten auf Etappe 7.

## Annahmen
- Etappen 1 und 2 gelten, wie sie jetzt stehen; dein „.“ gibt sie frei. Das Anhalten vor
  fremden *Bases* steht nur noch in Etappe 3, wie deine Antwort 2361 F2 A es legt (Anliegen
  2420).

## Empfehlung
Gib die zwei Items frei, wenn Schritte 1 bis 5 deinem Bild entsprechen. Ergänze bitte im
[Ziel](../domaene/ziel.md) die Ausnahme: ‚keine Kohärenz‘ ist nicht zu übergehen (2361 F1 A,
das Ziel änderst nur du); bis dahin gilt deine Antwort dort.

## Offene Anliegen
- An dich: keine. Vorschläge des Anforderungsautors: keine.
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
- [ ] Reviewer: DoD über das Inkrement
- [ ] Reviewer: Review geschrieben
- [ ] Stakeholder: Freigabe Review 7

## Freigabe
Freigabe: offen
Kommentar: .

