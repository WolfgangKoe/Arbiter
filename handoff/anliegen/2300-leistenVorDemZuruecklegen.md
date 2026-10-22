# Item 2 zeigt die Leisten, gebaut werden sie erst in Item 3

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält nicht auf, kein
Schritt fehlt, keine Prüfung ist rot. Es geht um Schnitt und Reihenfolge, und die sind nur
vor der Freigabe billig zu ändern.

Die Mockups von [Item 2](../../domaene/items/einheitZuruecklegen.md),
[auf-23-vorher](../../domaene/mockups/auf-23-vorher.html) und `auf-23-nachher.html`, zeigen
schon die drei *Leisten* mit *Griff* und leerem *Protokoll*. Die *Leisten* selbst
([QUE-6](../../domaene/anforderungen/querschnitt/leisten.md)) stehen aber erst in
[Item 3](../../domaene/items/gemeinsamUebergehen.md). Heute zeigt die Seite noch Spalten
(`<aside class="spalte">` in `index.html`).
Der Implementierer übernimmt das Markup der Mockups ohne Umschreiben
([O3](../../technik/architektur/oberflaeche.md)). In Item 2 bleiben ihm zwei Wege, und beide
sind falsch:
1. Er baut die *Leisten* mit, aber ohne die Tests zu QUE-6 und ohne `leisten.js` (O4). Dann
   gibt es *Griffe*, die nichts tun.
2. Er baut nach den alten Spalten. Dann weicht er vom Mockup ab, und Item 3 baut die Seite
   samt den Bildschirmtests zu AUF-28.1 („auch auf einer *Ablage*“) gleich noch einmal um.

Dazu kommt: Zwei Anliegen gehören zu den *Leisten*, sind aber an kein Item gebunden.
[2240](2240-leistenInKomponentenseiteEintragen.md) trägt sie in die Komponentenseite ein,
[2215](2215-leistenOhneEigenenNamen.md) gibt jeder *Leiste* einen Namen. Beide warten auf die
Technikphase, und kein Mechanismus erinnert an sie.

**Kosten.** Bleibt es so, wird die Oberfläche zweimal umgebaut, in Item 2 und in Item 3.
QUE-6 betrifft nur das Frontend, ohne Domäne und ohne Anfrage (O4): fünf Kriterien, ein neues
Modul `leisten.js` und rund 120 Zeilen aus 2240. Item 3, das größte Risiko des Plans, wird
dadurch kleiner.

**Gegenvorschlag.** QUE-6 von Item 3 nach Item 2 verschieben. Das Mockup von Item 2 zeigt die
*Leisten* schon, und es braucht keinen weiteren Link. Item 2 nennt dazu 2240 und 2215. Item 3
behält AUF-13 und QUE-5 und füllt nur das *Protokoll*, dessen *Leiste* dann schon steht. Im
Happy Path wandert „Jede *Leiste* fährt per *Griff* ein und aus“ von Schritt 6 nach Schritt 2.
Die andere Möglichkeit, QUE-6 nach Item 1, empfehle ich nicht. Item 1 hat kein Mockup und
soll außer der Adresse nichts sichtbar ändern.

Erledigt, wenn QUE-6 in einem Item vor Item 3 steht und dieses Item 2240 und 2215 nennt.

**Stellungnahme.** Den Befund nehme ich an, den Weg nicht: Nach dem neuen Schnitt
(Anliegen 2362, Anliegen 2363) hat Plan 7
gar keine *Leisten* mehr. QUE-5 und QUE-6 bleiben zusammen im Item
[gemeinsamUebergehen](../../domaene/items/gemeinsamUebergehen.md), jetzt in Etappe 2; es nennt
2240 und 2215. Die Seite wird so nur einmal umgebaut, in Etappe 2. Damit Item
einheitZuruecklegen die Spalten von heute baut, zeichnet Ux die Mockups zu AUF-23 ohne
*Leisten* (Anliegen 2366). Erledigt: Die Mockups zu
[einheitZuruecklegen](../../domaene/items/einheitZuruecklegen.md) zeigen die Spalten von
heute, der Stakeholder hat sie abgenommen.
