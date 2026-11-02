# Übergehen nach dem Anhalten: BEW-8.4, 8.5 und QUE-5.1 prüfbar fassen

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Für drei Kriterien braucht der Testautor eine Entscheidung, sonst prüft
ein Test nicht sein Kriterium.
1. [BEW-8.4](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md) *setzt* dort,
   wo die *Karte* „ohne BEW-3.1 und 6.2 zuletzt gezeigt hätte“. Bis Item 3 ist das die gerade
   Strecke zum Zeiger. Ab Item 3 hängt das Gezeigte vom Weg ab (AUF-29.1 je Weiterrücken,
   29.2, BEW-17.1). Dann ist die *Stelle* ohne Anhalten ein zweiter Weg, den die *Karte* nie
   zeigt. Beispiel: Die Boyz halten an der *Bewegungsweite*, danach führt der Zeiger um den
   Warboss herum. Die *Karte* zeigt die Boyz still, der gedachte Weg gleitet am Warboss
   entlang. Item 3 nennt BEW-8.4 nicht. Danach prüft also kein Test, ob BEW-8.4 noch gilt.
2. [BEW-8.5](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md), wenn beide
   anhalten würden: Boyz 10″ gezogen, *Bewegungsweite* bei 5″, *Nahkampfreichweite* ab 7″. Die
   *Karte* hält bei 5″ (BEW-6.3). BEW-8.4 lässt beides weg, die Boyz enden bei 10″ in
   *Nahkampfreichweite*, die keiner gesehen hat. Ob der *Eintrag* nur ‚Bewegungsweite‘ nennt
   oder beide, entscheidet „für BEW-3.1 und für BEW-6.2“ nicht.
3. [QUE-5.1](../../domaene/anforderungen/querschnitt/uebergehen.md) gilt „bei einer *Sperre*“.
   Item 1 baut seine Tests auf das Übergehen eines Anhaltens um (9320), das keine *Sperre*
   ist. Nach Item 3 bietet in Etappe 2 keine *Sperre* beim Loslassen mehr Übergehen an:
   QUE-1.2 nie (QUE-1.4), QUE-1.3 verhindert BEW-6.2, Kohärenz nie (QUE-5.5). Ein Test
   `testQue5_1…` prüfte also BEW-8.4.

**Kosten.**
1. Wie geschrieben: Jede Abfrage beim Ziehen liefert auch die *Stellen* ohne Anhalten, die
   Seite hält beide Wege. Das Loslassen schickt beide mit, denn gespeichert werden Handlungen,
   keine Abfragen ([P2](../../technik/architektur/speicher.md)). Die Schnittstelle von Ziehen
   und Loslassen wird doppelt so groß, Item 3 bekommt Tests mit mehreren Weiterrücken zu
   BEW-8.4. Ziehen mit Gedächtnis ist Neuland (Anliegen 2180; der
   [Vertrag](../../technik/architektur/vertrag/aufstellen/ziehen.md) rechnet bisher nur ab der
   *gesetzten* *Stelle*). Für Item 3 mache ich ohnehin vorher einen
   Wegwerf-Versuch.
   Mit dem Gegenvorschlag ist das Übergehen ein weiteres Weiterrücken ab der angehaltenen
   *Stelle*: eine Rechnung, nichts zusätzlich gespeichert.
2. Beides gleich billig, nur entschieden muss es sein.
3. Eine neue Kennung, die Tests aus 9320 werden umbenannt.

**Gegenvorschlag.**
1. BEW-8.4 hat noch keinen Test, darf also neu gefasst werden: „… *setzt* Arbiter die
   gezogenen *Modelle* so, wie BEW-1.5 sie ohne BEW-3.1 und 6.2 von der *Stelle*, an der sie
   angehalten wurden, an die *Stelle* des Loslassens *setzen* würde, …“. Anders als heute
   nur, wenn der Zeiger nach dem Anhalten um eine fremde *Base* herumführt. Grund aus dem Ziel:
   „Die *Karte* bildet den Spielstand ab, nicht den exakten Tisch“. Weil das 8840 F1 A
   berührt, empfehle ich die Frage an den Stakeholder: A wie heute (Anliegen 8840 F1 A),
   B wie hier (neu); Empfehlung B.
2. Der *Eintrag* nennt jedes von BEW-3.1 und 6.2, das auf dem Weg nach BEW-8.4 anhalten würde
   (Ziel: „das wird protokolliert“). Fachlich anders wäre: Übergehen lässt nur weg, was
   angehalten hat, BEW-6.2 hält dann bei 7″ erneut an. Das entscheidest du oder der
   Stakeholder.
3. Eine neue Kennung, etwa QUE-5.7: QUE-5.1 „bei einer *Sperre* oder nach einem Anhalten“ (wie
   der Zweck von QUE-5). QUE-5.1 fällt weg oder bleibt für AUF-31.

**Stellungnahme.** Angenommen in
[BEW-8](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md): 1 wie vorgeschlagen,
Frage an den Stakeholder in 9941; 2 beide *Gründe* (Ziel), deckt 9902; 3 BEW-8.5 nennt den
*Eintrag* selbst, QUE-5.1 bleibt bei der *Sperre*; Folgen: 9940.
