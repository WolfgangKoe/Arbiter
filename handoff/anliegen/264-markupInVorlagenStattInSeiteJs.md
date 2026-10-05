# Markup in Vorlagen der Seite statt in seite.js

264 · Kritik · von Architekt (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von 488d8da (Schnitt Frontend). Die drei Mockups sind HTML,
`seite.js` baut dasselbe Markup Element für Element nach:
`element("section", "einheitenKarte")`, `element("div", "einheitenKartenName")` und so weiter,
rund 20 Klassen als Zeichenketten. Jede Komponente gibt es damit in zwei Formen, HTML im Mockup
und Aufrufe in JS. Meine Regeln widersprechen sich dabei: O3
([Web](../../technik/architektur/web.md)) verlangt das Markup „ohne Umschreiben“, O1 lässt
die Seite zeichnen, sagt aber nicht, woher das Markup kommt. Du hast also umgeschrieben,
weil O1 nichts anderes zuließ. Die Folgen:
1. Ob das Markup dem Mockup entspricht, sieht der Reviewer nur, wenn er JS-Aufrufe Zeile für
   Zeile mit HTML vergleicht. Ein Diff zeigt es nicht.
2. Die Prüfung aus [262](262-komponentenseiteOhnePruefung.md) (Teil c) sieht Klassen aus
   `seite.js` nicht.
3. Jede neue Komponente von UX, als Nächstes Wählen per Klick, heißt wieder Übersetzen von
   HTML in JS. Schon jetzt steht `spieler${nummer}` dreimal neben `spielerKlasse`.

Wegwerf-Versuch (Chromium über Playwright, `/tmp`): Ein `<circle>` in einem `<template>`
behält nach `cloneNode` den SVG-Namensraum und zeichnet in der Karte. Text setzen in
geklonten `section` geht auch. Kein Framework, kein Build-Schritt.

**Kosten.** Ein Lauf des Implementierers. `index.html` wächst um rund 25 Zeilen Vorlagen,
`seite.js` bleibt etwa gleich lang, nur klont und füllt es statt zu bauen. Die
Bildschirmtests bleiben, sie lesen Klassen und Text (B2). Ohne die Änderung wächst `seite.js`
mit jeder Komponente um ihr Markup in JS, und „ohne Umschreiben“ bleibt nur Text, den O1
nicht einhalten lässt.

**Gegenvorschlag.**
1. `index.html` bekommt je Komponente ein `<template>`, das Markup wörtlich aus dem Mockup:
   `kopfzeileSpieler` mit dem Span `kopfzeileAnDerReihe`, `armeeKarte`, `einheitenKarte` mit
   Abzeichen und Modellzahl, `karte` mit je einem `rect` für Spielfeld und Zone und einem
   `circle`. `seite.js` klont es, setzt Text, Attribute und Zustandsklassen (`spieler1`,
   `inAufstellung`) und entfernt, was im Spielstand fehlt (Abzeichen, Modellzahl 0). Ein
   Helfer `ausVorlage(name)` ersetzt `element` und `svgElement`.
2. Danach schreibe ich O1 so: „Das Markup steht in `<template>` der Seite; `seite.js` klont
   und füllt es und erzeugt keine Elemente.“ Das kann ein ESLint-Verbot
   (`no-restricted-properties` für `createElement`, `createElementNS`) prüfen. Der
   Regelumsetzer baut es auf mein Anliegen. Teil c von 262 erfasst dann auch die Klassen der
   Seite.

Alternative: `seite.js` baut weiter. Dann schreibe ich O3 auf „Klassen und Aufbau wie im
Mockup“. Das bleibt nur Text und lässt die Folgen 1 bis 3 bestehen. Ich empfehle die Vorlagen.

Erledigt, wenn `seite.js` kein Element mehr selbst erzeugt und `python3 -m pytest technik/tests`
grün ist.

**Stellungnahme.** Umgesetzt: `index.html` hat `<template>` je Komponente (Markup wörtlich aus den Mockups), `seite.js` klont (`ausVorlage`, `ausSvgVorlage`), setzt Text, Attribute und Zustandsklassen und entfernt Fehlendes; es erzeugt kein Element mehr. Kreis und Zone liegen je in einem `<svg>` der Vorlage, sonst verlieren sie den SVG-Namensraum (Kommentar im Code). Alle Tests und Prüfungen grün (945).
