# seite.js erzeugt keine Elemente: ESLint-Verbot

268 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 9977e0e. Nach [264](264-markupInVorlagenStattInSeiteJs.md)
steht das Markup in `<template>` von `technik/frontend/index.html`, `seite.js` klont und füllt
es. O1 ([Web](../../technik/architektur/web.md)) sagt jetzt: „`seite.js` … erzeugt keine
Elemente.“ Das ist nur Text. Ein `document.createElement("span")` oder ein `innerHTML = "<span
class=…>"` für die nächste Komponente bliebe grün. Dann hätte das Markup wieder zwei Formen,
und Teil c der Prüfung aus [262](262-komponentenseiteOhnePruefung.md) sähe die Klassen nicht.

**Kosten.** Eine Regel in `eslint.config.mjs` und ein Scheiter-Test in
`frontendregeln/frontendTest.py`. Heute erfüllt `seite.js` die Regel, nichts wird rot. Ohne
die Regel fällt das Muster beim ersten Eilfall zurück, und erst ein Reviewer bemerkt es.

**Gegenvorschlag.** Für `technik/frontend/**/*.js`:
- `no-restricted-properties` für `document.createElement`, `document.createElementNS`,
  `document.write`;
- `no-restricted-syntax` für Zuweisungen an `innerHTML` und `outerHTML` und für Aufrufe von
  `insertAdjacentHTML`.

Die Meldung nennt O1 („Markup aus einer `<template>` der Seite klonen“). Scheiter-Test: eine
Probe mit `document.createElement("div")` ist rot, eine mit
`document.getElementById("x").content.firstElementChild.cloneNode(true)` grün. Danach setze ich
in O1 „Prüft“ auf diese Regel.

Erledigt, wenn der Scheiter-Test grün ist und `python3 -m pytest prozess/pruefungen` grün
bleibt.

**Stellungnahme.**
