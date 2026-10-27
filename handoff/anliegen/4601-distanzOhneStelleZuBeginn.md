# Die Distanz zählt die erste Strecke einer Bewegungsphase nicht

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Im [Glossar](../../domaene/glossar.md) ist die *Distanz* die „Summe der geraden
Strecken zwischen den *Stellen*, an die ein *Modell* in der laufenden *Bewegungsphase*
nacheinander *gesetzt* wurde“. Die *Stelle*, an der es zu Beginn der Phase steht, wurde aber
nicht in ihr *gesetzt*, sondern in der *Aufstellung* oder einem früheren Zug.

Beispiel: Ein Boy (*B* 5″) wird in der *Bewegungsphase* einmal 6″ gezogen. In ihr ist er an
genau eine *Stelle* *gesetzt*; zwischen einer Stelle gibt es keine Strecke, seine *Distanz*
ist 0, und [BEW-2.1](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md) sperrt
nicht. Erst ein zweites Ziehen zählt, und dann nur seine Strecke.

Hält auf ([Ich 3](../../prozess/praemissen/ich.md)): Schritt 3 des Happy Path in
[Plan 8](../plan.md) („weiter als *B* sperrt Arbiter beim Loslassen“) steht nach dem Wortlaut
in keinem Kriterium. Ein Test, der nach der Absicht schreibt, prüft etwas anderes, als das
Kriterium sagt; ein Implementierer, der nach dem Wortlaut baut, sperrt nie beim ersten Ziehen.

**Kosten.** Ein Halbsatz im Glossar. Ohne ihn hängt ‚weiter als B‘ daran, wie Testautor und
Implementierer das Glossar lesen.

**Gegenvorschlag.** *Distanz*: „Summe der geraden Strecken von der *Stelle* eines *Modells* zu
Beginn der laufenden *Bewegungsphase* über jede *Stelle*, an die es darin nacheinander
*gesetzt* wurde, in *Zoll* (…)“. Quellen bleiben.

**Stellungnahme.** Angenommen: Der Befund trifft zu, nach dem Wortlaut zählte das erste
Ziehen nicht. Die *Distanz* im [Glossar](../../domaene/glossar.md) lautet jetzt wie im
Gegenvorschlag: von der *Stelle* des *Modells* zu Beginn der laufenden *Bewegungsphase* über
jede *Stelle*, an die es darin nacheinander *gesetzt* wurde; Quellen unverändert. BEW-2.1
bleibt wörtlich, sein Begriff trägt jetzt das erste Ziehen.
