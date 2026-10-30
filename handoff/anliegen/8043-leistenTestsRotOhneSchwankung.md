# Leisten-Tests: rot, aber ohne Schwankung gemessen

Form: Fragen
Von: Reviewer
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Dein Hinweis: Die roten Tests der *Leisten* schwanken. Ich habe
[leistenTest.py](../../technik/tests/akzeptanz/querschnitt/leistenTest.py) sechsmal laufen
lassen: jedes Mal dieselben 21 rot (6 scheitern, 15 brechen in der Vorbereitung ab). Beides
ist erwartet, denn die Tests stehen vor dem Code (Item gemeinsamUebergehen):
- 15 brechen ab, weil das gemeinsame Übergehen noch fehlt: `modellLoslassen` kennt
  `übergehen` noch nicht.
- 6 scheitern, weil die Seite die *Leisten* noch nicht mit Namen (etwa „Armeeliste Spieler 1“)
  auszeichnet.
Eine Schwankung kann so entstehen: Mehrere Rollen ändern gleichzeitig Tests, ein Lauf mitten
darin zählt anders; oder ein Lauf mit `-x` hält früh an und zählt weniger (Anliegen 8042).

**Kosten.** Ohne deine Angabe, wo du die Schwankung gesehen hast, kann ich sie nicht
nachstellen. Nichts zu tun, wenn sie aus einem der beiden Gründe kam.

**F1 · Wo hast du die Schwankung gesehen?**
- a) Ich nehme die Erklärung an; der Reviewer prüft beim [DoD](../../prozess/ablauf/dod.md)
  über das Inkrement noch einmal, ob dieselben Tests rot bleiben (Ich 1). Empfehlung.
- b) Du nennst Lauf und Zahlen (Befehl, Ausgabe oder Dashboard); ich stelle sie nach (neu).
Antwort: .

**Stellungnahme.**
Kommentar: Ich bin gerade nicht sicher, wo ich diesen Hinweis geschrieben hatte? Bitte nochmal erläutern. Ich kann mich gerade nicht erinnern, dass ich von Schwankungen gesprochen hatte. Ich hatte bei der DoD lediglich geschrieben, dass ich die Mutationstests geschickt aufteilen ggf. gezielt durchführen (d.h. nur bei Tests und Code der verändert wurde) und falls wirklich alles durchlaufen muss, dass parallelisiert und der Fortschritt protokolliert wird.
