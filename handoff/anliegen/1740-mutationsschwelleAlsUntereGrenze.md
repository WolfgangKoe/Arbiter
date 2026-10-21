# Mutationsschwelle als untere Grenze, wiederholter Lauf gezielt

1740 · Auftrag · von Stakeholder → Organisationsentwickler · Runde 1/3 · angenommen

## Runde 1
**Befund.** Entscheidung des Stakeholders in Zyklus 6, Anlass der Mutationslauf über Plan 6
mit 93 % (Anliegen 1632), im Wortlaut:

> Die 95 % sind eine untere Grenze. Wenn schon klar ist, welche Tests ein Problem sind, dann
> sollten auch alle angegangen werden. Die Richtlinie (keine harte Regel) wäre: Unterschreitet
> man die 95 %, müssen 100 % der Tests repariert werden.

Dazu seine Vorgabe aus demselben Zyklus: Ein wiederholter Mutationslauf prüft nur die
betroffenen Stellen gezielt, der volle Lauf läuft in der Retro.

Heute steht dazu nur: Unter 95 % gefangener Mutanten endet der Lauf mit 1, der Lauf geschieht
einmal je Item vor dem Review ([Regeln, mutationsregeln](../../prozess/regeln.md#mutationsregeln),
[Ablauf, DoD](../../prozess/ablauf.md#dod-item-fertig), Absatz nach Punkt 4). Was nach einem
Lauf unter der Schwelle zu tun ist und wie oft der volle Lauf läuft, regelt keine Stelle.

**Kosten.** Ohne die Regel reicht es, gerade so viele Lücken zu schließen, bis 95 % erreicht
sind; bekannte Lücken bleiben offen. Ein voller Lauf nach jeder Nachbesserung kostet über eine
Stunde (1570, [Retro 6](../retro.md), Befund 1).

**Gegenvorschlag.** In der Prozessphase nach `Freigabe Retro 6`, angepasst an die bestehenden
Stellen statt einer neuen Regel ([Ich 4](../../prozess/praemissen/ich.md)):
1. DoD, Absatz Mutation: Die Schwelle von 95 % ist eine untere Grenze. Liegt ein Lauf darunter,
   wird jeder überlebende Mutant angegangen, nicht nur so viele, bis die Schwelle erreicht ist.
   Richtlinie, keine harte Regel; Mechanismus: nur Text (das Werkzeug endet weiter mit 1 unter
   95 %).
2. Ablauf der Nachprüfung: Ein wiederholter Lauf prüft gezielt nur die betroffenen Stellen,
   der volle Lauf über alle seit `Freigabe Plan` geänderten Domänenmodule läuft in der Retro.
   Mechanismus baut der Regelumsetzer mit Retro 6, P2 (gezielter Lauf je Modul und Zeile).
3. Zusammen mit [1570](1570-mutationstestsEffizienter.md) beantworten, dort Frage 5 (wann ist
   der Lauf nötig) und Frage 2 (ein Ergebnis gilt weiter).

Offen für die Prozessphase, dort frage ich nach: Was heißt „repariert“ bei einem gleichwertigen
Mutanten, der dasselbe Ergebnis liefert und den kein Test fangen kann? In 1632 sind es 13 von
15. Meine Empfehlung dann: Ein Test, wo einer möglich ist; sonst gleichwertig mit Begründung im
Anliegen, die der Reviewer beurteilt, oder die Zeile vereinfachen, wenn die Gleichwertigkeit
überflüssigen Code zeigt.

Stand in 1632: Alle 15 Überlebenden sind angegangen, 13 als gleichwertig begründet (Reviewer
und Testautor), zwei mit Einheitstests in Anliegen 1710,
gezielt geprüft, ohne vollen Lauf.

**Stellungnahme.** Angenommen, [Ablauf, DoD](../../prozess/ablauf.md#dod-item-fertig), Absatz
Mutation: 1 „Unter 95 % wird jeder Überlebende angegangen, nicht nur bis zur Schwelle“, nur
Text; „repariert“ heißt ein Test, der ihn fängt, oder bei einem gleichwertigen eine Begründung
beim Werkzeug, dann zählt er nicht (dazu [1751](1751-gleichwertigeMutantenNichtUmDasWerkzeugBauen.md)).
2 gezielter Lauf je Item, voller Lauf in der Prozessphase; Mechanismus Retro 6, P2. 3 in
[1570](1570-mutationstestsEffizienter.md).
