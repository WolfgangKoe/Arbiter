# eslint und stylelint vor dem ersten JavaScript

242 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** In Zyklus 3 schreibt der Implementierer das erste Frontend: HTML, CSS und
JavaScript-Module in `technik/frontend/` ([Web](../../technik/architektur/web.md), O1 bis O3).
[Ablauf](../../prozess/ablauf.md#dod-item-fertig) (Werkzeuge) nennt eslint und stylelint,
[234](234-flaskUndPlaywrightFehlen.md) hat sie auf „mit dem ersten JavaScript“ gelegt. Heute
prüft nichts das Frontend: ruff, `formregeln/benennung.py`, `formregeln/glossar.py` und
`formregeln/kommentare.py` lesen nur `.py`. [wir.md](../../prozess/praemissen/wir.md) gilt
ausdrücklich auch fürs Frontend. Node 18.19 und npm liegen unter `/usr/bin`, ein
`package.json` fehlt.

**Kosten.** Ohne Prüfung gehen englische oder einbuchstabige Namen, `var`, Kommentare in
Prosa und kebab-case-Klassen ungeprüft durch; der Reviewer findet sie von Hand oder nicht.
Nach dem Einbau stehen sie in Seite, Komponentenseite und Bildschirmtests (Kosten wie in
[223](223-mockupsBenennungUndZonenfarbe.md) Befund 1). Es blockiert den ersten Lauf des
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

**Stellungnahme.**
