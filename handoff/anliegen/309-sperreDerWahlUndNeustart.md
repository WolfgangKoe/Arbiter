# Plan 4: Wo die Sperre einer Wahl steht, was ein Neustart zeigt

309 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · angenommen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Nach deiner Antwort in [308](308-startDerAufstellung.md) sieht Plan 4 so aus: Ihr
startet Arbiter, Spieler 1 hat den Roll-off schon gewonnen und die Zone neben seiner *Ablage*
(AUF-6), Spieler 2 ist *an der Reihe*. Spieler 2 klickt eine seiner *Einheiten* in seiner
*Ablage* an, sie wird *Einheit in Aufstellung* (AUF-5). Arbiter merkt sich das: Lädt jemand
die Seite neu, steht es noch da (QUE-3). Kriterien:
[aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md),
[querschnitt.md](../../domaene/anforderungen/querschnitt.md).

Zwei Dinge sagen weder Regeln noch Ziel:
1. Klickt Spieler 1 eine seiner *Einheiten* an, obwohl Spieler 2 *an der Reihe* ist, lehnt
   Arbiter das ab (*Sperre* ‚nicht wählbar‘, AUF-1.5). Eine *Sperre* nennt ihren *Grund*
   (Glossar); sonst wirkt der Klick, als sei das Programm kaputt. Offen ist, wo der
   Satz steht, wie lange und wie er lautet.
2. Arbiter speichert ab Plan 4 jede Wahl. Offen ist, was ihr seht, wenn ihr Arbiter beendet
   und neu startet.

**Kosten.** Ohne Antwort zu F1 ändert ein abgelehnter Klick nichts und sagt nichts (AUF-5.2
gilt trotzdem). Ohne Antwort zu F2 entscheidet die Technik den Neustart, und das wäre eine
erfundene Regel.

**F1 · Wo, wie lange und mit welchem Satz zeigt Arbiter, dass eine Wahl abgelehnt ist?**
- A: Direkt an der angeklickten *Einheit* in der *Ablage*, bis zum nächsten Klick. Für
  ‚nicht wählbar‘ steht dort „Jetzt nicht wählbar.“, für ‚Einheit begonnen‘ (eine andere
  Einheit ist schon zum Teil gesetzt, AUF-1.6) „Erst die begonnene Einheit fertig
  aufstellen.“
- B: Wie A, aber an einem festen Ort für Meldungen über oder unter der *Karte*. Den Ort
  gibt es noch nicht; er kommt ohnehin mit Plan 6, wenn Arbiter fragt, wer den Roll-off
  gewonnen hat (dort hieß er *Spielaktionsbereich*).
- C: Du nennst andere Sätze oder einen anderen Ort.

Empfehlung A: Der Satz steht dort, wo der Spieler gerade hinschaut. Das passt zu Etappe 1:
Ein *Modell*, dessen *Setzen* gesperrt ist, bleibt mit seinem *Grund* auf der *Karte* stehen,
also auch dort, wo gehandelt wurde. Später, mit „gemeinsam übergehen“, bleibt der Satz
stehen, bis die *Spieler* „zurück“ oder „gemeinsam übergehen“ wählen. Das Ziel lässt jede
*Sperre* übergehen.

Antwort: Eine Einheit kann immer angeklickt werden. Und zwar egal, welcher Spieler dran ist. Die Einheit eines Spielers, der NICHT an der Reihe ist, darf im Zug des Spielers, der an der Reihe ist, beispielswesie nicht in der Bewegungsphase bewegt werden. Schau nochmal in ArbiterMap, wie es gemacht wurde. Dort ist die Regelung in Ordnung gewesen.

**F2 · Was seht ihr, wenn ihr Arbiter beendet und neu startet?** Arbiter ist ein Programm,
das ihr mit einem Befehl startet (QUE-2.1). Neuladen der Seite behält den Stand (QUE-3.2).
Hier geht es darum, das Programm selbst zu beenden, etwa wenn der Rechner neu startet.
- A: Eine neue Partie: die *Ausgangslage*, mit Gewinner und Zone nach AUF-6. Die alte
  Partie bleibt in der Datei gespeichert, wird aber nicht gezeigt.
- B: Die letzte Partie, so wie ihr sie verlassen habt. Dann braucht ihr einen Knopf „Neue
  Partie“, sonst könnt ihr nie neu anfangen; das wird eine eigene Anforderung.

Empfehlung A: Etappe 1 kennt keinen Knopf „Neue Partie“, und das Aufstellen dauert Minuten.
Wichtig wird B, wenn eine Partie Stunden dauert (Etappe 3); dann frage ich neu.

Antwort: A

**Stellungnahme.**
