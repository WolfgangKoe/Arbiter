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
   dazu ohne sichtbare Änderung: die *Auswahl* entflechten (1652), `seite.js` teilen (1541),
   *Ablage* heißt auch im Code *Armeeliste* (2221). „zurück“ (AUF-17) entfällt samt Test,
   ebenso die *Sperre* ‚nicht wählbar‘ beim Ziehen auf eine *Armeeliste* (AUF-8.4): Das
   *Modell* springt still zurück (2220 F4 A, 2410). Zuletzt die Kommentare im Code, die
   [Es 8](../prozess/praemissen/es.md) verbietet (deine Antwort A zu
   [2360](anliegen/2360-es8MechanismusNachziehenUndHakenP5.md)).
2. [Einheit zurücklegen](../domaene/items/einheitZuruecklegen.md): Schritte 2, 3 und 5.

Reihenfolge 1, 2: Item 1 räumt auf, wo Item 2 baut. Das Risiko liegt bei Item 1.

Kommentare: Ab „Freigabe Plan 7“ prüft die DoD auch `technik/`. Dort stehen 78 verbotene
Kommentare in 30 Dateien, 48 im Code, 30 in Tests. Bis sie fort sind, ist die DoD jedes Items
rot; darum Item 1. Kosten: je ein Durchgang für Testautor und Implementierer, am Bildschirm
nichts. Was ein Kommentar erklärt, geht in einen Namen oder einzeiligen Docstring.

## Abweichung vom Zyklusziel
Review 6 nennt drei Schritte; nach deinem Schnitt bleibt nur „Einheit zurücklegen“.
Gemeinsam übergehen, das *Protokoll* und das Loslassen neben der *Karte* kommen mit dem
Normal Move in Etappe 2 (2361 F1, F2). Davor kommt Item 1 (1650, 1652). Nach Plan 7 ist
Etappe 1 erreicht. Die Randfälle nur des Aufstellens warten auf Etappe 7.

## Annahmen
- Deine Antwort A nennt die 38 Kommentare `Regel:`. Ich nehme die 40 `Warum:` dazu: Es 8
  verbietet sie ebenso, sonst bliebe die DoD rot. Sollen sie bleiben, braucht Es 8 eine
  Ausnahme (Organisationsentwickler).

## Empfehlung
Gib die zwei Items frei, wenn Schritte 1 bis 5 deinem Bild entsprechen.

Das [Ziel](../domaene/ziel.md) sagt: Jede *Sperre* können die Spieler einvernehmlich
übergehen. Deine Antwort 2361 F1 A nimmt ‚keine Kohärenz‘ aus. Das Ziel ändert nur du,
darum liegt es bei dir. Vorschlag: „Die Spieler können eine Sperre einvernehmlich übergehen,
außer ‚keine Kohärenz‘; das wird protokolliert.“ Bis dahin gilt deine Antwort.

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
Kommentar: Es hieß, folgendes läge noch bei mir: 
„.“ für Etappe 1 in der geänderten Fassung, ohne „vor fremden Bases“: 01-aufstellen.md. -> Das hier verstehe ich nicht. Wir haben die Etappen überarbeitet. Es sollte doch jetzt alles passen.
Die Ausnahme „keine Kohärenz“ im Ziel ergänzen, wie der Planer in plan.md empfiehlt. Was soll hier ergänzt werden. Warum liegt das bei mir?
In der Retro den Haken „Koordinator: nach dev gepusht“, falls er noch fehlt. -> Ist schon lange gesetzt.
Stellungnahme: Etappen: Die Annahme ist gestrichen, sie gelten, wie sie stehen. Ziel: unter
Empfehlung erklärt, mit Vorschlag für den Satz. Retro-Haken: nichts für mich. 

