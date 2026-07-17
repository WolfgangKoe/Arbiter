STATUS: AWAITING-VERIFICATION

# S161 Task 3 (B-105) — UI-Verifikation `go_source_chip`

Ausgeführt: `go_source_chip(label, color)` in `src/uiLayout/diceCompose.py` (generischer
GO-Quellen-Chip), verdrahtet an zwei Stellen in `src/uiLayout/diceHtml.py`:

1. **Rewire (bestehende Optik, keine Verhaltensänderung):** `_render_dice_wound_block`s
   Strength-Buff-Quellenchip (bisher `_strength_source_badge_html`) läuft jetzt über
   `go_source_chip`. Per-grep belegt: `src/uiLayout/diceHtml.py` ruft `go_source_chip` an
   dieser Stelle auf — Nicht-Test-Code nutzt den neuen Baustein bereits produktiv.
2. **Neue Fähigkeit (Infrastruktur, noch NICHT verdrahtet):** `_render_dice_save_block` hat
   jetzt einen optionalen Parameter `invuln_source_label: str | None = None` — wenn gesetzt,
   erscheint der GO-Name als Chip neben `Inv N+`. **Kein Aufrufer in `_common.py` übergibt
   diesen Parameter bisher** — der einzige Aufrufer (`_common.py:2475`,
   `_render_dice_save_block(ctx.save_result, ctx.ap, ability_invuln=ctx.invuln_from_ability)`)
   ist unverändert, weil `_common.py` außerhalb des Datei-Scopes dieser Aufgabe lag
   (`docs/handoff/S159_planning.md` Task 4 / `S161_planning.md` §3 nennen nur
   `diceCompose.py`/`diceHtml.py`/Testdatei).

## Scope-Fund (wie im Plan als Eskalationspfad vorgesehen)

`ability_badge_label(faction, unit)` (`abilityEngine.py:601`) existiert und liest den
Badge-Namen einer aktiven **Fraktions-Fähigkeit**. Der Stakeholder-Wunsch „Quantum Deflection"
ist aber ein **Stratagem**, dessen Name über `active_modifiers[].source`
(`stratagemEngine.py:55`, `_apply_stratagem_effect`) läuft, gelesen von
`_common.py::_stratagem_invuln_save` (die den Wert, aber noch nicht den Namen zurückgibt).
Um „Inv 4+ [Quantum Deflection]" tatsächlich im Spiel zu zeigen, braucht es einen
Folge-Task, der in `_common.py`:
- `_stratagem_invuln_save` (oder eine neue Schwesterfunktion) auch den `source`-Namen liefert,
- den Fraktions-Fähigkeit-Pfad (`ability_badge_label`) für den Fall eines
  Fähigkeits-Invuln analog anbindet,
- das Ergebnis (je nachdem, welcher der beiden Pfade laut der bestehenden
  `min(ability_inv, strat_inv)`-Logik "gewinnt") als `invuln_source_label` an
  `_render_dice_save_block` durchreicht.

Das ist bewusst **nicht** in dieser Aufgabe miterledigt (Datei-Scope), sondern hier als Fund
gemeldet statt improvisiert verdrahtet — bitte als eigenen kleinen Folge-Task (~XS/S) in den
Backlog/nächste Planung aufnehmen.

## Manuelle Prüfung (das, was JETZT sichtbar ist)

**Voraussetzungen:** Ein Roster mit einer Einheit, deren Fraktions-Fähigkeit einen aktiven
Strength-Buff mit Quellenname gewährt (z. B. Ork „Disruption Fields" o. ä. — je nach aktuell
verfügbarem Necron/Ork-Roster mit aktivierbarer Strength-Buff-Fähigkeit). App starten
(`streamlit run src/app.py`), Roster laden, in die Shooting- oder Fight-Phase wechseln, die
Fähigkeit aktivieren, einen Angriff gegen ein Ziel deklarieren.

**Klickpfad:** Angreifende Einheit auswählen → Fraktions-Fähigkeit aktivieren, die einen
Strength-Bonus gewährt → Ziel zuweisen → Angriffsauflösung öffnen (Waffen-Tab) → WOUND-Block
betrachten.

**Erwartung:** Neben der S-vs-T-Zeile erscheint weiterhin ein grüner Chip mit dem Namen der
Fähigkeit (z. B. „Disruption Fields") — optisch unverändert zum Stand vor dieser Session
(Rewire, keine Verhaltensänderung), jetzt aber mit Hover-Tooltip (title-Attribut) über dem
Chip, der den vollen Namen zeigt (neu, B-111-analoge Wrap-Absicherung).

**Nicht verifizierbar in dieser Session:** Der neue Invuln-Chip („Inv 4+ [Quantum
Deflection]") — Infrastruktur ist fertig und unit-getestet
(`tests/uiLayout/test_dice_html.py::test_render_dice_save_block_invuln_shows_go_source_label`),
erscheint aber erst im Spiel, sobald der oben genannte Folge-Task `_common.py` verdrahtet.

## Ergebnis (vom Stakeholder auszufüllen)

- [x] Strength-Buff-Chip sieht unverändert aus (grün, Name, jetzt mit Tooltip beim Hover)
- Anmerkungen: Ich kann die Badge für Disruption Fields sehen. sieht gut aus.
