# Oberordner: weitere Ordner, Literale, Probe zum Altbestand

205 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 96ea7b7 (Anliegen 165). Die Suite ist grün (553 Tests). Was
in 165 unter „Erledigt, wenn“ steht, ist erfüllt. Drei Befunde:

**B1 · `doku/` hat keinen erlaubten Platz.** Der Organisationsentwickler darf `doku/`
schreiben (`.claude/agents/organisationsentwickler.md:12`), und `erledigteLoeschen.py:13`
durchsucht den Ordner. `oberordner.bekannteOrdner` kennt ihn nicht. Legt der
Organisationsentwickler `doku/` an, wird `testJederOrdnerDerWurzelIstPerspektiveOderAltbestand`
rot. Die Meldung schickt ihn dann zu „`pfade.perspektiven` oder `agenten.nurLesbar`“, aber
`doku/` ist keins von beiden.
Kosten: Ein erlaubter Schreibpfad macht die Suite rot. Folgt man der Meldung, wird `doku/`
entweder fälschlich zur Perspektive (Benennung, `rollenkontext`, `CLAUDE.md`-Höchstmaß) oder
zum Altbestand (ruff und git würden ihn übergehen).
Gegenvorschlag: In `pfade.py` steht neben `perspektiven` eine eigene Konstante für die
übrigen Ordner (`handoff`, `doku`). `bekannteOrdner` und die Meldung nennen sie. Ob `doku/`
bleibt, entscheidet der Organisationsentwickler; bis dahin gehört es in diese Konstante.

**B2 · Die Perspektiven und `handoff` stehen weiter als Literal.** `erledigteLoeschen.py:13`
nennt `"domaene", "technik", "prozess", "handoff"` selbst; laut Stellungnahme zu 165 sind alle
Stellen umgestellt, diese aber nicht. `"handoff"` steht als Literal in `oberordner.py:8`,
`benennung.py:44` und `:210`, `phasenfolge.py:73` und `plan.py:9`. Das ist die Fundstelle 5
aus 114, für diesen Ordner.
Kosten: Wird ein Ordner umbenannt, fehlt eine Stelle. Kein Test wird dabei rot, und genau das
sollte 165 verhindern.
Gegenvorschlag: `handoffOrdner` in `pfade.py` (oder die Konstante aus B1), und
`suchOrdner = (*perspektiven, handoffOrdner, ".claude", "doku")`.

**B3 · Kein Probetest zeigt, dass ein vorhandener Altbestand-Ordner grün ist.**
`oberordnerTest.py` legt `.probe`, `domaene` und `handoff` an, aber keinen Ordner aus
`altbestandOrdner`. `testEinFehlenderAltbestandOrdnerIstGrün` prüft eine leere Wurzel und
würde auch ohne Altbestand-Logik grün bleiben.
Kosten: Streicht jemand `*altbestandOrdner` aus `bekannteOrdner`, bleiben alle Proben grün.
Nur der `stand`-Test mit dem echten Repo wird dann rot. In einem frischen Klon fehlt der
Altbestand (von git ignoriert), dort bemerkt es niemand.
Gegenvorschlag: den Grün-Test über `altbestandOrdner` parametrisieren (Ordner anlegen, erwartet
`[]`).

Erledigt, wenn B1 bis B3 umgesetzt sind, ein Probeordner `doku/` grün bleibt,
`python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Commit geprüft hat.
