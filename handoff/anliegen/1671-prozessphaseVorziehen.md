# Prozessphase vorziehen: Items und Grenzen

1671 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · rückfrage

## Runde 1
**Befund.** Du willst schon jetzt zur Prozessphase; die [Retro 6](../retro.md) steht als
Entwurf. Der [Ablauf](../../prozess/ablauf.md) lässt das Vorziehen an diesen Stellen nicht zu:
1. Die Prozessphase beginnt mit dem Commit „Freigabe Review 6“. Erst dann schreibt
   `standregeln/fortschritt.py` den Fortschritt in die Retro, und die Kritiker können ihren
   Haken setzen.
2. Regeln, Prämissen und Rollen ändern sich erst nach „Freigabe Retro 6“; die Schreibgrenze
   sperrt `prozess/` bis dahin, P1 lässt sich nicht vorbereiten.
3. Die DoD ist nicht durch ([Review 6](../review.md#dod)): SonarLint rot
   ([1630](1630-sonarlintRotInAnwendung.md)), Mockups liegen noch
   ([1631](1631-mockupsNachDemEinbau.md)), der Mutationslauf läuft. Der Commit-Hook lässt
   keinen Commit mit rotem SonarLint durch. Endet der Lauf unter 95 %, ist ein Item nach
   der DoD nicht fertig; davon weicht nur deine Entscheidung ab.
4. Lücken aus dem Mutationslauf warten nach [Ich 3](../../prozess/praemissen/ich.md) auf
   die nächste Phase der Perspektive ihres Autors: Tests und Code auf die Technikphase 7,
   nur ein fehlendes Kriterium auf die Domänenphase 7.
5. Nach „Freigabe Review 6“ korrigiere ich die Retro nach: Aufträge aus dem Rundgang
   Prüfcode und die Kennzahlen bis dahin.

Zu deinem Kommentar im Review („der Fortschritt für die Prozessphase und retro.md fehlen“):
Ja. Nach [Ablauf, Fortschritt](../../prozess/ablauf.md#fortschritt) trägt das Review die
Zeilen der Domänenphase 7, die Retro die der Prozessphase. Die Retro gab es bis eben nicht;
ihre Zeilen erscheinen mit dem Commit „Freigabe Review 6“.

**Kosten.** Ohne Antwort zu F1 hat die Retro mehr Items, als die Regel aus 630 erlaubt
(höchstens zwei, je aus einem Befund, der das Produkt aufgehalten hat).

**Gegenvorschlag.** Bestehende Regeln (Ich 4): [Ablauf, Prozessphase](../../prozess/ablauf.md#prozessphase)
Schritt 1 („oder der Stakeholder vorher will“), 630 F2 über [730](730-werKritisiertUndZurueckgenommeneRegeln.md).

**F1 · Welche Prozess-Items in Zyklus 6?**
A: P1 bis P5: zwei aus Befunden (P1, P3), dazu deine Aufträge 1570, 1670, 1660 (P2, P4, P5).
B: P1, P2, P4, P5; P3 (Lücke 510) in den Backlog.
C: Höchstens zwei: P1 und P4; die übrigen in den Backlog.
Empfehlung: A. Deine Aufträge sind das, was du vorher willst; P3 nutzt ein Bordmittel und
senkt den Prüfcode, statt ihn zu mehren.
Annahme: Die Retro 6 nennt P1 bis P5.
Antwort: A

**F2 · Wohin gehen Lücken aus dem laufenden Mutationslauf?**
A: Nach Ich 3: Tests und Code in die Technikphase 7, ein fehlendes Kriterium in die
Domänenphase 7.
B: Alle in die Domänenphase 7.
Empfehlung: A. Wer die Lücke schließt, arbeitet in der Technikphase.
Antwort: .

**Stellungnahme.**
Kommentar: Ich möchte den aktuellen Lauf nicht grundsätzlich ändern. Aber ich finde es schwierig, dass wir inzwischen 100 Minuten auf einen Mutationstest warten, dessen Befunde wir vermutlich erst im nächsten Zyklus bearbeiten werden und welche die Prozessphase möglicherweise nicht blockieren. Sei hier bitte nochmal kritisch, damit wir nicht aus Versehen ein Inkrement abnehmen, dass fehlerhaft ist. Und vor allem sollten keine Tests aus Sonarlint rot sein.
