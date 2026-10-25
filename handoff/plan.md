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
   zuerst, vor Vertrag und Tests, die Kommentare im Code, die
   [Es 8](../prozess/praemissen/es.md) verbietet (deine Antwort A zu
   Anliegen 2360). Dann ohne sichtbare
   Änderung: die *Auswahl* entflechten (1652), `seite.js` teilen (1541), *Ablage* heißt auch
   im Code *Armeeliste* (2221). „zurück“ (AUF-17) entfällt samt Test, ebenso die *Sperre*
   ‚nicht wählbar‘ beim Ziehen auf eine *Armeeliste* (AUF-8.4): Das *Modell* springt still
   zurück (2220 F4 A, 2410).
2. [Einheit zurücklegen](../domaene/items/einheitZuruecklegen.md): Schritte 2, 3 und 5.

Reihenfolge 1, 2: Item 1 räumt auf, wo Item 2 baut. Das Risiko liegt bei Item 1.

Kommentare: Ab „Freigabe Plan 7“ prüft der Commit-Hook auch `technik/`. Dort stehen 78
verbotene Kommentare in 30 Dateien: 29 in Akzeptanztests (Testautor), 48 im Code und einer in
einem Einheitstest (Implementierer). Bis sie fort sind, scheitert jeder Commit; darum zuerst
(Anliegen 2510). Beide laufen gleichzeitig, der
Koordinator committet einmal nach beiden; davor committet niemand in der Technikphase. Kosten:
je ein Durchgang, am Bildschirm nichts. Was ein Kommentar erklärt, steht danach im Namen, in
einem einzeiligen Docstring oder in der Architektur, auf die er verweist; was dort schon
steht, entfällt.

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

Ausnahme im Ziel: Das [Ziel](../domaene/ziel.md) verspricht: „Die Spieler können eine
Sperre einvernehmlich übergehen.“ In 2361 F1 A hast du entschieden: Steht eine Einheit ohne
*Kohärenz*, bietet Arbiter das Übergehen gar nicht an, beim Aufstellen wie bei jeder
Bewegung. So widersprechen sich Ziel und deine Antwort. `domaene/ziel.md` ändert nur du,
darum liegt es bei dir. Vorschlag: „Die Spieler können eine Sperre einvernehmlich übergehen,
außer ‚keine Kohärenz‘; das wird protokolliert.“ Bis dahin gilt deine Antwort.

## Offene Anliegen
- An dich: keine. Vorschläge des Anforderungsautors: keine.
- Sonst: [Moderation](moderation.md).

## Fortschritt
- [x] Architekt: Vertrag zu Item aufraeumenUndFesteAdresse, bei beiden Hälften
- [x] Testautor: Tests zu Item aufraeumenUndFesteAdresse
- [x] Fachkritiker: Kritik an den Tests zu Item aufraeumenUndFesteAdresse
- [x] Architekt: Kritik an den Tests zu Item aufraeumenUndFesteAdresse
- [x] Implementierer: Tests zu Item aufraeumenUndFesteAdresse grün
- [x] Architekt: Kritik am Code zu Item aufraeumenUndFesteAdresse
- [x] Reviewer: Kritik am Code zu Item aufraeumenUndFesteAdresse
  Hindernis: Anliegen 2820: Pfeilfunktion als Hülle um einen Aufruf in anfragen.js (Es 7) (Anliegen 2861); beseitigt: Commit „aufraeumenUndFesteAdresse: Knopf ohne Hülle, Anliegen 1651, 2820 und 2861 angenommen“
- [x] Fachkritiker: Item aufraeumenUndFesteAdresse abgenommen
- [x] Planer: Item aufraeumenUndFesteAdresse gelöscht
- [x] Architekt: Vertrag zu Item einheitZuruecklegen, bei beiden Hälften
- [x] Testautor: Tests zu Item einheitZuruecklegen
- [x] Fachkritiker: Kritik an den Tests zu Item einheitZuruecklegen
  Hindernis: Anliegen 2770: AUF-23.1 ungeprüft, während andere Einheiten auf der Karte stehen (Anliegen 2783); beseitigt: Commit „aufraeumenUndFesteAdresse: Kommentare aufgeräumt, AUF-8.4 und AUF-17 entfernt, feste Adresse, Tests zu einheitZuruecklegen“
- [x] Architekt: Kritik an den Tests zu Item einheitZuruecklegen
  Hindernis: Anliegen 2780: Benennung rot (m, Zeile 130), Bildschirmtests mit page.route und den Beispielen zu AUF-23.1, 23.3, 23.4 fehlen (Anliegen 2782); beseitigt: Commit „aufraeumenUndFesteAdresse: Kommentare aufgeräumt, AUF-8.4 und AUF-17 entfernt, feste Adresse, Tests zu einheitZuruecklegen“
- [x] Implementierer: Tests zu Item einheitZuruecklegen grün
- [x] Architekt: Kritik am Code zu Item einheitZuruecklegen
- [x] Reviewer: Kritik am Code zu Item einheitZuruecklegen
- [x] Fachkritiker: Item einheitZuruecklegen abgenommen
- [x] Planer: Item einheitZuruecklegen gelöscht
- [x] Reviewer: DoD über das Inkrement
- [x] Reviewer: Review geschrieben
- [ ] Fachkritiker: Kritik am Review
- [ ] Organisationsentwickler: Kritik am Review
- [x] Stakeholder: Freigabe Review 7

## Freigabe
Freigabe: ja
Kommentar: Es hieß, folgendes läge noch bei mir: 
„.“ für Etappe 1 in der geänderten Fassung, ohne „vor fremden Bases“: 01-aufstellen.md. -> Das hier verstehe ich nicht. Wir haben die Etappen überarbeitet. Es sollte doch jetzt alles passen.
Die Ausnahme „keine Kohärenz“ im Ziel ergänzen, wie der Planer in plan.md empfiehlt. Was soll hier ergänzt werden. Warum liegt das bei mir?
In der Retro den Haken „Koordinator: nach dev gepusht“, falls er noch fehlt. -> Ist schon lange gesetzt.
Stellungnahme: Etappen: Du hast recht, sie passen; die Annahme dazu ist gestrichen. Ziel:
unter Empfehlung erklärt, warum und mit welchem Satz. Retro-Haken: ein veralteter Punkt aus
der Übergabe des Koordinators, nichts zu tun. 

