# Leisten-Tests: rot, aber ohne Schwankung gemessen

Form: Fragen
Von: Reviewer
An: Stakeholder
Runde: 2/3
Status: angenommen

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

## Runde 2
**Befund.** Du hast recht: Von dir steht nirgends etwas über Schwankungen. Der „Hinweis“ kam
im Auftrag des Koordinators an mich, als deiner ausgegeben; dieselbe Lesart steht im
Architekten-Anliegen [8022](8022-testlaufNurAufEinemFestenStand.md) („Der Stakeholder fand
die Schwankung … ungeklärt“). Ich habe sie übernommen, statt nach deinem Wortlaut zu suchen.
Runde 1 beruhte darauf; die Frage dort entfällt. In der Sache bleibt: Die roten Tests der
*Leisten* schwanken nicht, sie warten auf das Item gemeinsamUebergehen. 8022 gilt unabhängig
davon, wer es bemerkt hat (ein Testlauf, während andere Rollen Tests ändern, zählt falsch).

Dein Wunsch aus der DoD zum Mutationslauf, Stand heute
([Mutationsregeln](../../prozess/regeln/mutationsregeln.md)):
- Gezielt: gibt es. Der Lauf je Item verändert nur die seit `Freigabe Plan` geänderten Zeilen
  und lässt je Mutant nur die Tests laufen, die diese Zeile ausführen.
- Fortschritt protokollieren: kommt in der Prozessphase 9 (Retro P9, Anliegen
  [6960](6960-mutationslaufFrueherStarten.md)): eine Zeile je fertigem Modul, ein
  unterbrochener Lauf übernimmt die fertigen.
- Parallelisieren: fehlt. Der volle Lauf prüft alle Mutanten nacheinander in einer Kopie; der
  Rechner hat 8 Kerne.

**Kosten.** Parallelisieren: der volle Lauf wird kürzer (wie viel, misst der Regelumsetzer an
einer Kopie in `/tmp`); dafür mehr Prüfcode in `mutation.py` (je Kern eine Kopie) und Tokens für
einen Prozess-Item. Ohne: nichts zu tun, der volle Lauf bleibt so lang wie heute.

**F1 · Soll der volle Mutationslauf parallel laufen?**
- a) Ja: Ich gebe es als [8122](8122-vollerMutationslaufParallel.md) an den
  Organisationsentwickler für die Prozessphase 9, zusammen mit P9; 8043 schließe ich danach.
  Empfehlung.
- b) Nein: gezielt und mit Fortschritt (P9) genügt; ich setze 8122 und 8043 auf erledigt.
Antwort: Ja.
Annahme: Ich lege 8122 schon an; es wartet auf die Prozessphase 9.

**Stellungnahme.**
