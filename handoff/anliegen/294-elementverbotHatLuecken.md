# Elementverbot im Frontend hat Lücken

294 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an der Linter-Konfiguration nach Anliegen 268 (`eslint.config.mjs`,
uncommittet). Die Regel hält, was 268 vorschlug; eine Probe zeigt, dass diese Formen trotzdem
grün bleiben und Markup an der `<template>` vorbei erzeugen
([Web](../../technik/architektur/web.md), O1):
1. `window.document.createElement("div")`, `element.ownerDocument.createElement("div")`:
   Das Verbot gilt nur für das Objekt `document`.
2. `document.writeln("…")`, die Schwester von `write`.
3. `element["innerHTML"] = "…"`: Der Selektor prüft nur `property.name`, nicht den Wert
   eines berechneten Zugriffs.
4. HTML aus einer Zeichenkette: `new DOMParser().parseFromString`,
   `createRange().createContextualFragment`, `setHTMLUnsafe`.
5. `new Option(name, wert)`, `new Image()`: `select.add(new Option(…))` ist das übliche Muster
   für eine Auswahlliste, also naheliegend, sobald die Aufstellung eine Einheit wählen lässt.

Dazu, nicht neu, aber in derselben Datei: Die Kopfzeile von `eslint.config.mjs` nennt
„`prozess/praemissen/wir.md` 1, 5, 8“, `eslintKommentare.mjs` „`wir.md` 8“. `wir.md` hat vier
Punkte; gemeint ist [es.md](../../prozess/praemissen/es.md) 1, 5, 8.

**Kosten.** Nur `eslint.config.mjs`, je Lücke ein Fall in `frontendTest.py` und die Zeile in
[regeln.md](../../prozess/regeln.md#frontendregeln). `technik/frontend/seite.js` nutzt keine
dieser Formen, nichts wird rot. Ohne die Ergänzung sperrt die Regel die erste Form, die jemand
tippt, und lässt die zweite durch; 1 und 5 sind keine Absicht, sondern übliche Schreibweisen.

**Gegenvorschlag.** In einer Wegwerf-Konfiguration geprüft, alle neun Proben rot, das Klonen
der Template und `textContent` grün:
- `no-restricted-properties`: `createElement`, `createElementNS` ohne `object` (jedes Objekt);
  `document.write`, `document.writeln`; `parseFromString`, `createContextualFragment`,
  `setHTMLUnsafe` ohne `object`.
- `no-restricted-syntax` zusätzlich:
  `AssignmentExpression[left.property.value=/^(innerHTML|outerHTML)$/]` und
  `NewExpression[callee.name=/^(Image|Option|Audio)$/]`.
- In beiden Kopfzeilen `wir.md` durch `es.md` ersetzen.

`Object.assign(element, {innerHTML: …})` und Ähnliches bleiben Urteil des Reviewers; ein
Linter fängt keine Absicht, nur übliche Schreibweisen.

Erledigt, wenn `frontendTest.py` je Form 1 bis 5 eine rote Probe hat, das Klonen grün bleibt
und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.**
Umgesetzt wie vorgeschlagen in `eslint.config.mjs`: `createElement`, `createElementNS`,
`parseFromString`, `createContextualFragment`, `setHTMLUnsafe` auf jedem Objekt gesperrt,
`document.write` und `writeln`; `no-restricted-syntax` ergänzt um berechnetes `innerHTML` und
`outerHTML` sowie `new Image`, `new Option`, `new Audio`. Beide Kopfzeilen nennen jetzt `es.md`.
`frontendregeln/frontendTest.py` hat je Form 1 bis 5 eine rote Probe, das Klonen der Template
bleibt grün. [Regeln](../../prozess/regeln.md#frontendregeln) führt die Fälle.
