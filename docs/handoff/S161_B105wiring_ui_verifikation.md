STATUS: AWAITING-VERIFICATION

# S161 B-105-Wiring-Folge-Task — UI-Verifikation `invuln_source_label`

Folge-Task zu `docs/handoff/S161_B105_ui_verifikation.md` (Scope-Fund): der GO-Quellenname
für den Invuln-Save wird jetzt in `src/uiLayout/_common.py::compute_resolution_context`
ermittelt und an `_render_dice_save_block` durchgereicht.

## Was implementiert wurde

- `_stratagem_invuln_best(def_uid)` (neu, `src/uiLayout/_common.py`) liefert Wert **und**
  Quellenname (`active_modifiers[].source`) der besten aktiven Stratagem-Invuln in einem
  Scan. `_stratagem_invuln_save` bleibt als dünner Wrapper (nur Wert) bestehen — bestehende
  Aufrufer/Tests unverändert.
- `ResolutionContext` trägt jetzt `invuln_source_label: str | None`.
- Gewinner-Logik in `compute_resolution_context`: wenn der Bonus-Invuln (Stratagem oder
  Fähigkeit) den nativen Save schlägt, wird zusätzlich ermittelt, welcher der beiden Pfade
  den niedrigeren (gewinnenden) Wert stellt — Stratagem gewinnt das Label nur bei echt
  niedrigerem Wert, bei Gleichstand gewinnt die Fähigkeit (`ability_badge_label(...)`).
  Kein Bonus-Invuln aktiv → `invuln_source_label = None` (unverändertes Verhalten).
- Der einzige Aufrufer (`_render_defender_blocks`, Zeile ~2505) übergibt jetzt
  `invuln_source_label=ctx.invuln_source_label`.

Keine Fraktions-Strings/-Checks hinzugefügt — der Name kommt ausschließlich aus
`active_modifiers[].source` bzw. `ability_badge_label()`. Architektur-Gate
(`tests/architecture/`) bleibt grün.

## Regressionstests (neu, `tests/uiLayout/test_common.py`)

- `test_compute_resolution_context_stratagem_invuln_carries_stratagem_source_label`
- `test_compute_resolution_context_ability_invuln_carries_badge_label`
- `test_compute_resolution_context_invuln_winner_label_picks_lower_stratagem_value`
- `test_compute_resolution_context_no_invuln_source_keeps_label_none`

Alle grün, zusammen mit den 259 vorher bestehenden Tests in
`tests/uiLayout/test_common.py` + `tests/uiLayout/test_dice_html.py` (263 passed) und
`tests/architecture/` (8 passed, unverändert).

## Manuelle Prüfung (das, was JETZT im Spiel sichtbar sein sollte)

**Voraussetzungen:** Ein Roster mit einer Einheit, die durch ein aktives Stratagem einen
Invuln-Save erhält, dessen Wert **niedriger** ist als ein evtl. gleichzeitig aktiver
Fähigkeits-Invuln und niedriger als der native Save der Einheit — z. B. Necron-Einheit +
Quantum-Deflection-fähiges Stratagem (Inv 4+).

**Klickpfad:** App starten (`streamlit run src/app.py`) → Roster mit Necrons laden →
Shooting- oder Fight-Phase → gegnerischen Angriff gegen die Necron-Einheit deklarieren →
im Reactive-Stratagem-Kasten "Quantum Deflection" nutzen (`Use`) → Angriffsauflösung öffnen
(Waffen-Tab) → SAVE-Block betrachten.

**Erwartung:** Neben `Inv 4+` erscheint jetzt ein grüner GO-Quellen-Chip mit dem Namen
"Quantum Deflection" (Hover-Tooltip zeigt den vollen Namen). Ist stattdessen eine
Fraktions-Fähigkeit mit Invuln-Effekt aktiv (kein Stratagem, oder das Stratagem ist nicht
strikt besser), zeigt der Chip stattdessen den Badge-Namen der Fähigkeit. Ohne aktive
Bonus-Invuln-Quelle (nativer Save gewinnt) bleibt der Chip wie bisher weg.

## Ergebnis (vom Stakeholder auszufüllen)

- [ ] Invuln-Chip erscheint neben `Inv N+` mit dem Stratagem-Namen (Quantum Deflection)
- [ ] Bei aktiver Fähigkeits-Invuln ohne (besseres) Stratagem erscheint der Fähigkeits-Name
- Anmerkungen:
