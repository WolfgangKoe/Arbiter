# Vier Annahmen zur Bewegungsphase

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Die Verträge zu [Schlacht](../../technik/architektur/vertrag/schlacht.md) und
[Bewegung](../../technik/architektur/vertrag/bewegung.md) regeln vier Fälle, die keine
Anforderung nennt. Ich arbeite mit den Empfehlungen; Tests und Code von Zyklus 8 folgen ihnen.

**Kosten.** Je Frage: Was du am Bildschirm siehst und was eine andere Antwort kostet.

**F1 · Wann steht „Bewegung der Einheit beenden“ da?** A: Nur wenn eine *Einheit in
Bewegung* ist, also nachdem du ein *Modell* gezogen hast; davor nur „Phase beenden“
(Mockups que-10, bew-1). B: Immer in der *Bewegungsphase*; ohne *Einheit in Bewegung*
geschieht beim Klick nichts (neu). Empfehlung: A, ein Knopf ohne Wirkung verwirrt. B kostet
eine Zeile im Frontend und einen Test.
Annahme: Der Knopf steht nur bei einer *Einheit in Bewegung*.
Antwort: Hmm, ich gebe mal meine Vorstellung wieder. Die Bewegungsphase beginnt. Ich wähle eine Einheit und bewege diese nicht, soweit wie ich möchte bis zum maximalen Bewegungswert. Einen Knopf "Bewegung beenden" braucht es nicht. Ich wähle einfach die nächste Einheit. Es braucht eher eine Art Markierung, dass sich die Einheit bewegt hat, bzw. welche Art der Bewegung sie in der Bewegungsphase ausgeführt hat (Es gibt m.W. drei, wenn man "Stationär" nicht als vierte Art mitzählt).

**F2 · Wo zeigt die Karte ein Modell, solange du es weiter als sein B ziehst?** Beim
Loslassen dort steht es wieder, wo es vor dem Ziehen war (BEW-2.3); offen ist nur das
Bild während des Ziehens. A: Es bleibt an der letzten *Stelle* ohne *Sperre* stehen, der
Zeiger geht allein weiter; so siehst du, wie weit es kommt (V10, wie in der *Aufstellung*).
B: Es springt sofort an die *Stelle* vor dem Ziehen zurück (BEW-1.4 mit BEW-2.3 wörtlich).
Empfehlung: A. Gilt A, ergänzt der Anforderungsautor BEW-1.4 um diesen Fall; B kostet eine
Ausnahme in V10 nur für die *Schlacht* und Tests dazu.
Annahme: A, die *Karte* zeigt die letzte *Stelle* ohne *Sperre*.
Antwort: Ich bin mir nicht sicher, ob ich die Frage richtig verstehe. Normalerweise sollte ich eine Einheit nicht über das B der einzelnen MOdelle ziehen können. ALles andere wäre eine bewusst gesetzte ÜBersteuerung, die vermutlich nur dann geschieht, wenn man beispielsweise auf dem Tisch misst, dass eine Einheit in Angriffsreichweite ist, die App diesen Zustand aber nicht abbildet. ANsonten würde ich erwarten, dass die Einheit in der Bewegung am maximalen Wert stoppt.

**F3 · Kann man in der Schlacht ein einzelnes Modell einer ausgewählten Einheit zur Ebene
machen?** In der *Aufstellung* macht ein Klick auf ein *Modell* der *ausgewählten* *Einheit*
es zur *Ebene* (AUF-25). A: In der *Schlacht* nicht: Ein Klick auf ein *Modell* wählt seine
*Einheit* als Ganzes (AUF-20.6). Willst du ein *Modell* allein ziehen, klickst du vorher ein
*Modell* einer anderen *Einheit* an; ziehst du dann eins der nicht *ausgewählten* *Einheit*,
geht es allein (AUF-20.4; AUF-25 steht unter *Aufstellung*). B: Wie in der *Aufstellung*, ein
zweiter Klick macht das *Modell* zur *Ebene* (ArbiterMap `model_selection.js:336`, in jeder
Phase gleich). Empfehlung: A für Etappe 2, der Happy Path läuft, und keine Anforderung
verlangt B. B ist bequemer beim Nachziehen einzelner Boyz; es kostet in der Domänenphase
eine Anforderung, dann je eine Route und einen Schlüssel im Spielstand, den Klick der Seite
und Tests, großteils aus AUF-25 übernommen.
Annahme: A.
Antwort: B, es ist wie in der Aufstellungsphase

**F4 · Was geschieht, wenn ein Klick doppelt ankommt?** Etwa ein Doppelklick auf „Phase
beenden“ oder ein Klick auf einer zweiten Seite mit altem Stand (QUE-3.2). A: Er wirkt
einmal: Es endet nur die *Phase*, die die Seite zeigte; „Erster Zug“ ändert nichts mehr,
sobald ein *Spieler* ihn hat (V5, wie V2 in der *Aufstellung*). B: Jeder Klick wirkt, ein
Doppelklick überspringt eine *Phase* (neu). Empfehlung: A, eine übersprungene *Phase* holt
niemand zurück. A ist gebaut; B spart nur den Abgleich der *Phase* im Dienst, wenige Zeilen.
Annahme: A.
Antwort: A

**Gegenvorschlag.** Beantworte F1 bis F4; „.“ heißt, die Empfehlung gilt. Bei B ändere ich
den Vertrag, und der Testautor zieht die Tests nach.

**Stellungnahme.**
