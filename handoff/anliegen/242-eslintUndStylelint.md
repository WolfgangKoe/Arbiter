# eslint und stylelint vor dem ersten JavaScript

242 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** In Zyklus 3 schreibt der Implementierer das erste Frontend: HTML, CSS und
JavaScript-Module in `technik/frontend/` ([Web](../../technik/architektur/web.md), O1 bis O3).
[Ablauf](../../prozess/ablauf.md#dod-item-fertig) (Werkzeuge) nennt eslint und stylelint,
Anliegen 234 hat sie auf „mit dem ersten JavaScript“ gelegt. Heute
prüft nichts das Frontend: ruff, `formregeln/benennung.py`, `formregeln/glossar.py` und
`formregeln/kommentare.py` lesen nur `.py`. [wir.md](../../prozess/praemissen/wir.md) gilt
ausdrücklich auch fürs Frontend. Node 18.19 und npm liegen unter `/usr/bin`, ein
`package.json` fehlt.

**Kosten.** Ohne Prüfung gehen englische oder einbuchstabige Namen, `var`, Kommentare in
Prosa und kebab-case-Klassen ungeprüft durch; der Reviewer findet sie von Hand oder nicht.
Nach dem Einbau stehen sie in Seite, Komponentenseite und Bildschirmtests (Kosten wie in
Anliegen 223 Befund 1). Es blockiert den ersten Lauf des
Implementierers im Frontend, nicht den Testautor.

**Gegenvorschlag.** Vor dem ersten Lauf des Implementierers in `technik/frontend/`:
- `package.json` in der Wurzel mit eslint 9 und stylelint 16, je feste Minor-Version und
  einer Zeile „Warum“ wie in `pyproject.toml`; `node_modules/` in `.gitignore`.
- eslint über `technik/frontend/**/*.js`: `camelcase`, `id-length` mindestens 3 mit den
  Ausnahmen `x` und `y` (wir.md 5), `no-var`, `prefer-const`, `eqeqeq`, `no-unused-vars`,
  `complexity` 15 (Ablauf, Werkzeuge); Kommentare nur `// Regel: …` oder `// Warum: …`
  (wir.md 8).
- stylelint über `technik/frontend/**/*.css`: `selector-class-pattern` und
  `custom-property-pattern` camelCase mit Umlauten (`^[a-zäöüß][a-zA-ZäöüÄÖÜß0-9]*$`),
  Farbwerte nur in `:root`, sonst nur als Variable (wie `vorschlag.css`); welche Regel das
  durchsetzt, wählst du.
- Aufruf im Lauf von `python3 -m pytest prozess/pruefungen` wie ruff
  (`formregeln/konfigurationTest.py`); fehlt `node_modules`, ist der Test rot mit dem
  Befehl zum Installieren, nicht übersprungen.
- Dateinamen in `technik/frontend/` camelCase, ASCII: `formregeln/benennung.py`.

Erledigt, wenn je Regel ein Scheiter-Test rot wird (englischer Name, `var`,
kebab-case-Klasse, Hex-Farbe in einer Komponente) und die Prüfungen auf dem leeren Ordner
grün sind.

**Stellungnahme.** Umgesetzt. `package.json` (eslint 9.39.\*,
stylelint 16.26.\*, „warum“ je Paket), `node_modules/` in `.gitignore`, `eslint.config.mjs`,
`.stylelintrc.json`; die zwei eigenen Regeln (Kommentare, Farben nur in `:root`) liegen in
`prozess/pruefungen/frontendregeln/*.mjs`. Aufruf und Scheiter-Tests (je Regel ein Gegenbeispiel,
grün auf leerem Ordner, ohne `npm install` rot mit dem Befehl): `frontendregeln/frontend.py`,
`frontendregeln/frontendTest.py`, im Lauf von pytest. Dateinamen: `formregeln/benennung.py`.
Grenzen: Ein „englischer Name“ ist für kein Werkzeug erkennbar; eslint sperrt einbuchstabige,
zu kurze und snake_case-Namen, englische Wörter bleiben Urteil des Reviewers. Farbnamen
(`red`) sind auch in `:root` gesperrt. Einmal `npm install` aus der Wurzel.
