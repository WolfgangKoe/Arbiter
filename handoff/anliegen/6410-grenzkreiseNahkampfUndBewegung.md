# Grenzen von Nahkampfreichweite und Bewegung als leichter Kreis

Form: Auftrag
Von: Stakeholder
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wortlaut des Stakeholders: „Eine Anregung noch für die nächste Domänenphase. Es wäre gut, wenn Grenzen für Nahkampfreichweite und Bewegung jeweils durch einen Kreis leicht angezeigt würden. UX soll in der nächsten Domänenphase ein Mockup vorstellen. Eine Idee dazu gibt es auch schon in ArbiterMap und auch wie das Verhalten sein soll.“

Fundstellen in ArbiterMap: [Reichweiten und Ringe, Spezifikation](../../ArbiterMap/docs/spec/interaction_map.md) (Abschnitt 5, Distanzen und Reichweiten, mit Buffs auf Bewegungsreichweite und Advance-Ringen), [Mockup der Reichweiten-Varianten](../../ArbiterMap/docs/spec/mockups/013_reichweiten_varianten.html), [Item 013](../../ArbiterMap/steering/backlog/items/013-spike-reichweiten-darstellung.md).

**Kosten.** Offen.

**Gegenvorschlag.** Keiner.

**Stellungnahme.** Umgesetzt in [bew-11](../../domaene/mockups/bew-11.html): Die *Boyz* sind *ausgewählt*; je *Modell* ein durchgezogener *Grenzkreis* (BEW-11.1), um die *Modelle* des anderen *Spielers* ein gestrichelter bei 1″ (BEW-11.3). Die Regeln für `grenzkreis` stehen in [vorschlag.css](../../domaene/mockups/vorschlag.css), da [komponenten.css](../../technik/frontend/komponenten.css) sie erst in der Technikphase erhält. Vorrückringe nach 6998 F1 A angenommen: nach der Wahl nur ein Kreis, weiteres Mockup dafür nicht nötig (BEW-11.2 ändert nur den Radius). Antwortet der Stakeholder in 6998 mit B, folgt ein neues Kriterium und ein neues Mockup.
Kommentar: Ich habe mir das Mockup angeschaut. An sich gefällt mir die Richtung gut. Ich hätte es gerne folgendermaßen: 1. Ein Modell wird ausgewählt -> Der Kreis für dieses Modell wird sichtbar (Reichweite für Bewegung oder zusätzlich für Vorrücken, Nahkampf, Angriffsreichweite, Aura,...). Beim Vorrücken erwarte ich zwei Kreise. Einmal bis zur maximalen Bewegungsreichweite und dann noch ein weiterer Kreis für die zusätzliche Bewegung durch das Vorrücken. Diese Art von Darstellung ist eine wichtige UI-Komponente, die es an vielen Stellen braucht. Bei anderen Baseformen muss entsprechend die Baseform "ausgedehnt" werden. Auch das gilt es zu gegebener Zeit zu beachten. 2. Wird eine ganze Einheit ausgewählt, möchte ich NICHT die Kreise einzelner Modelle sehen, sondern die Einhüllende von allen diesen KReisen. Sonst wird es unübersichtlich. Entsprechend wird diese Prinzip auf alle vorher unter 1 genannten fahclichen Aspekte übertragen. Das hier wäre wie gesagt eine typische UI-Komponente für mich, die unabhängig von der Fachlichkeit immer wiederverwendet werden kann. Die Farbe, Linienart und -dicke sind ggf. Parameter. Denke hierüber also ordentlich nach. 3. Vielleicht lässt sich diese Komponente noch weiter verallgemeinern, weil es manchmal auch Regeln gibt "innerhalb von x Zoll der Aufstellungszone des Gegners" Es ist dasselbe Prinzip, wo man diesen Bereich angezeigt bekommen sollte. Schau mal, wie du die Komponente sinnvoll bauen könntest. Der Akzeptanztest gilt gleichermaßen, aber vielleicht wird er einfach dem Frontend zugeordnet?
Stellungnahme: Alle Punkte sind richtig, tragen aber noch kein Kriterium; bew-11 bleibt deshalb unverändert (ein Kreis je Modell, ein Kreis beim Vorrücken). Zwei Kreise beim Vorrücken und die Einhüllende der Einheit (Punkt 1 und 2) sowie die weiteren Grenzen (Punkt 3 und 4, nur wenn eine Regel sie braucht) gehen als Anliegen 7003 an den Anforderungsautor. Die wiederverwendbare Komponente mit Parametern und der Ort des Akzeptanztests gehen als Anliegen 7004 an den Architekten. Sobald 7003 ein Kriterium hat, zeichne ich bew-11 neu.
