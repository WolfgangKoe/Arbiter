# Klick auf ein Modell einer aufgestellten Einheit in der Aufstellung

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: rückfrage
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Randfall abseits des Happy Path). In der *Aufstellung* klickt
jemand ein *Modell* einer schon *aufgestellten* *Einheit* an. AUF-20.6 sagt: Sie ist danach
*ausgewählt*. AUF-5.10 sagt: Wird eine *Einheit* *aufgestellt*, ist sie nicht mehr
*ausgewählt*; nach dem [Vertrag, V3](../../technik/architektur/vertrag/aufstellen.md) prüft die
*Aufstellung* vor dem Auswählen, dass die *Einheit* nicht *aufgestellt* ist. Kein Test prüft
den Fall; der Klick auf ein *Modell* der *Einheit in Aufstellung* läuft.

**Kosten.** Bleibt es offen, entscheidet der Code nebenbei, und am Bildschirm kann es mal so,
mal so aussehen. Beide Antworten sind wenige Zeilen und ein Test.

**F1 · Wählt der Klick eine aufgestellte Einheit aus?** A: Nein, es geschieht nichts
(AUF-5.10, V3). B: Ja, die *Karte* kennzeichnet ihre
*Modelle*; ziehen lässt sie sich weiter nicht (AUF-20.6 wörtlich, AUF-16.8). Empfehlung: A.
Eine *aufgestellte* *Einheit* kann man in der *Aufstellung* nicht mehr bewegen, die
Kennzeichnung brächte nichts. Bei A ergänzt der Anforderungsautor AUF-20.6 um „nicht
*aufgestellt*“.
Annahme: A, der Klick ändert nichts.
Antwort: .

**Gegenvorschlag.** Beantworte F1 in der Domänenphase 9; „.“ heißt, die Empfehlung gilt.

**Stellungnahme.**
Kommentar: An sich stimme ich dir zu. Es sollte im Zweifelsfall möglich sein, eine bereits aufgestellte Einheit zu verschieben, damit die neu aufzustellende Einheit ggf. Platz hat. Dazu muss es möglich sein, die betreffende bereits aufgestellte Einheit auszuwählen und zu verschieben. Ein Zurücklegen dieser bereits aufgestellten Einheit sollte dagegen nicht möglich sein. Ist das abbildbar?
