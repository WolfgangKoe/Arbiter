# Griff zeigt eingefahren in die falsche Richtung

Form: Kritik
Von: Architekt
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet, das ist ein
Randfall abseits des Happy Path. In [que-5.html](../../domaene/mockups/que-5.html) zeigt der
Pfeil jedes *Griffs* nach außen (◀, ▶, ▼), also „einfahren“. Ist eine *Leiste* *eingefahren*
(QUE-6.3), zeigt er weiter nach außen, obwohl ein Klick sie jetzt ausfährt (QUE-6.4).
[vorschlag.css](../../domaene/mockups/vorschlag.css) regelt für diesen Zustand nur, dass der
Inhalt verschwindet. Ohne Regel müsste der Implementierer die Richtung selbst festlegen
([Ich 1](../../prozess/praemissen/ich.md)) oder `leisten.js` müsste den Text des *Griffs*
tauschen. Dann kennte das Skript mehr als Griff und Leiste
([O4](../../technik/architektur/oberflaeche.md)).

**Kosten.** Eine Regel in `vorschlag.css`, keine neue Klasse. Fehlt sie, zeigt der *Griff*
einer *eingefahrenen* *Leiste* in die falsche Richtung.

**Gegenvorschlag.** Den Pfeil per CSS am Zustand drehen, den es schon gibt, ohne Änderung am
Markup:
```css
.leistenGriff[aria-expanded="false"] {
  transform: scale(-1);
}
```
`scale(-1)` spiegelt in beiden Achsen, so wird ◀ zu ▶ und ▼ zu ▲. Der Knopf selbst ist
symmetrisch und sieht danach gleich aus. Bestehende Regel nach
[Ich 4](../../prozess/praemissen/ich.md): die Regel in `vorschlag.css`, die den Inhalt bei
`aria-expanded="false"` ausblendet; die neue liest denselben Zustand ab.

**Stellungnahme.** Einverstanden. Die Regel steht in
[vorschlag.css](../../domaene/mockups/vorschlag.css), das Markup von
[que-5.html](../../domaene/mockups/que-5.html) und
[auf-13.html](../../domaene/mockups/auf-13.html) bleibt unverändert, keine neue Klasse. Ist eine
*Leiste* *eingefahren*, zeigt der Pfeil des *Griffs* nach innen, ein Klick fährt sie aus.
