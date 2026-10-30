# Eingefahren verkehrt herum benannt

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf (Kritik: neuer Code verletzt Lesbarkeit, [Es](../../prozess/praemissen/es.md)
„der Name trägt die Bedeutung“, [Wir 2](../../prozess/praemissen/wir.md)), Diff
`039da85..b14cdf7`, Item gemeinsamUebergehen. In
[leisten.js](../../technik/frontend/leisten.js) heißt
`const eingefahren = griff.getAttribute("aria-expanded") === "true"`: Der Wert ist wahr, wenn
die *Leiste* ausgefahren ist. Das [Glossar](../../domaene/glossar.md) definiert *eingefahren*
als das Gegenteil (nur der *Griff* sichtbar). Das Verhalten stimmt (QUE-6.3, 6.4 grün), nur
der Name sagt das Umgekehrte.

Geprüft auf `b14cdf7` (Arbeitsbaum in `/tmp`): eslint und stylelint
(`frontendregeln.frontend`) grün, SonarLint ohne Funde, Benennung, Kommentare, Glossar und
Importvertrag grün; Tests von BEW-8, QUE-5, QUE-6 und alle Einheitstests grün. Rot sind nur
die Tests anderer Items (BEW-6, BEW-9, BEW-13).

**Kosten.** Keine am Bildschirm. Bleibt es, liest der Nächste die Zeile wörtlich und kehrt
beim Ändern (etwa *Leiste* beim Start eingefahren) die Logik falsch herum um. Eine Zeile.

**Gegenvorschlag.** `const ausgefahren = …` (oder `eingefahren = … === "false"` und
`String(eingefahren)`).

**Stellungnahme.**
