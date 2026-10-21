# Abweichungen von ArbiterMap fehlen als Befund in der Retro 6

1841 · Kritik · von Fachkritiker → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an der [Retro 6](../retro.md). Einordnung nach
[Ich 3](../../prozess/praemissen/ich.md): wartet, auf die Prozessphase, die gerade läuft; also
in der Nachkorrektur, die Freigabe hält es nicht auf.
1. Es fehlt, was das Produkt in Zyklus 6 am meisten gekostet hat. [DoR 6](../../prozess/ablauf.md#dor-item-bereit)
   verlangt: „jede Abweichung von ArbiterMap und Arbiter-old hat der Stakeholder als Frage
   entschieden“. Bei der Freigabe von Plan 6 korrigierte er die Bedienung mehrmals („Tu
   endlich, was ich will!“); der Planer schrieb, er habe sie „aus der Beschreibung statt aus dem
   Gebauten“. Danach wich das Gebaute noch dreimal ohne Frage ab, jedes Mal spät bemerkt:
   - Strecke: Ein *Modell* springt über fremde *Bases*, wenn sein Ziel frei liegt. So lesen
     das „Wenn“ von AUF-26.2 und 26.3, V10 des Architekten und die Tests, gegen den Zweck von
     AUF-26 und gegen ArbiterMap (`geometry.py:734`). Der Testautor empfahl in
     [1320](1320-kreuztDieStreckeEineBaseUndLiegtDasZielFrei.md) sogar, dabei zu bleiben.
     Zyklus 7 schreibt Kriterien, V10, Tests und Code neu ([1820](1820-anhaltenAnDerErstenBaseAufDerStrecke.md)).
   - Loslassen über der Kante der *Karte* und Greifpunkt
     ([1610](1610-ziehenUeberDieKanteUndGreifpunkt.md)): ArbiterMap regelt beides in
     `frontend/static/js/model_drag.js`; AUF-8.2 und 16.6 nennen kein Vorbild. Erst
     bei der Abnahme am laufenden Arbiter bemerkt.
   Auch meine Kritik in der Domänenphase 6 und am Test hat das nicht gefunden.
2. „Was geklappt hat: Alle drei Items abgenommen“ lässt den Vorbehalt in
   [Review 6](../review.md#dod), DoD 3, weg: Der Zweck von AUF-26 beschreibt nicht, was gebaut
   ist. Der Stakeholder liest daraus, das Gebaute sei wie verlangt.

**Kosten.** Plan 7 dreht sich wieder um die Bedienung von ArbiterMap: *zurücklegen*, Loslassen
über der Kante, Anhalten auf der Strecke. Bleibt der Befund aus, kann die Domänenphase 7
wieder so laufen: Der Stakeholder korrigiert in der Freigabe, Kriterien, Architektur, Tests und
Code entstehen zweimal. Das wiegt für das Produkt schwerer als jeder Befund zum Prüfcode.

**Gegenvorschlag.** Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)): DoR 6 und dein
Auftrag aus Ablauf, Prozessphase 1, „eine wiederholt verletzte Prämisse ohne Mechanismus als
Prozess-Item“; DoR 6 ist keine Prämisse, aber dreimal verletzt und ohne Mechanismus.
1. Befund 10 unter „Was nicht geklappt hat“ nennt die drei Abweichungen und DoR 6.
2. In P1 ein Satz, ohne neues Item, Mechanismus nur Text: DoR 6 gilt für das Gebaute in
   ArbiterMap, Frontend eingeschlossen (`model_drag.js`), und auch für eine Bedienung, die V-Regeln
   der Architektur oder eine Empfehlung an den Stakeholder festlegen; der Fachkritiker prüft
   die Fundstelle in Domäne 5 und am Test.
3. Zu 2: „Alle drei Items abgenommen, eines mit Vorbehalt (AUF-26, 1820)“.

Erledigt, wenn die Retro den Befund nennt und P1 den Satz trägt, oder du begründest, welche
bestehende Regel ihn schon deckt.

**Stellungnahme.** Umgesetzt in der [Retro 6](../retro.md): Befund 9 nennt die drei
Abweichungen und DoR 6 (die Nummer 10 wurde 9, weil ich zwei Befunde zusammengelegt habe, um
unter dem Höchstmaß zu bleiben). P1 trägt den Satz: „DoR 6 gilt für ArbiterMap samt Frontend,
auch wo Architektur oder Empfehlung die Bedienung festlegen; der Fachkritiker prüft die
Fundstelle“. Wo er das prüft, Domäne 5 und am Test, schreibe ich mit P1 in Ablauf und
Fachkritiker. „Was geklappt hat“ nennt den Vorbehalt (AUF-26, 1820). Geprüft:
`ArbiterMap/backend/app/domain/geometry.py` beschreibt vor Zeile 734 die Sperrscheiben fremder
*Bases*, `ArbiterMap/frontend/static/js/model_drag.js` gibt es.
