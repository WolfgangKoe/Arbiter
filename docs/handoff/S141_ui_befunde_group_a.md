STATUS: ANSWERED (S141 — Befunde 1/2/3/5 → Fixes B–D; am Session-Ende löschen)

# S141 UI-Befunde Gruppe A — Root-Cause-Analyse (read-only Investigation)

Kontext: S141 B12b-Suffix „used on ⟨Einheit⟩" (Commit `cdb55e2`) frisch verdrahtet. Vier
manuelle Verifikations-Befunde, Root Cause + Fix-Ort je Befund. Keine Code-Änderung in
dieser Untersuchung — reines Read-only-Audit.

---

## Befund 1 — Movement-Timing (Advance-Reroll-Karte zeigt "Used" erst nach Advance-Klick)

**Root Cause:** `_advance_reroll_state()` (`src/gameMechanic/movementPhase.py:223-266`)
prüft `movement_choice != "advanced"` **vor** jeder used/used_elsewhere-Berechnung und
gibt dann sofort `("locked", "no Advance roll open")` zurück (Zeile 257-258) — die
Prüfung von `stratagem_undo_visible`/`used_here` (Zeile 259-266) wird für eine frisch
selektierte, noch nicht "advanced" Einheit nie erreicht. Die Eligibilität hängt also
tatsächlich an "Advance-Roll offen" statt am globalen Stratagem-Verbrauch — bestätigt
die Vermutung im Auftrag. Wurde das Advance-Reroll bereits auf Einheit A verwendet,
zeigt Einheit B vor ihrem eigenen Advance-Klick fälschlich "locked: no Advance roll
open" statt "used_elsewhere" (mit Suffix "used on A").

**Fix-Ort:** `src/gameMechanic/movementPhase.py::_advance_reroll_state` (Zeilen 255-266) —
Prioritätsreihenfolge der drei "locked"-Zweige (S133 K2 Item 1: in_melee → kein Advance
offen → CP/used) muss die used/used_elsewhere-Prüfung VOR (oder unabhängig von) der
"kein Advance offen"-Bedingung auswerten, damit ein bereits verwendetes GO als
"used_elsewhere" erscheint, unabhängig vom eigenen `movement_choice`-Zustand der gerade
selektierten Einheit. Betrifft eine bewusste S133-Entscheidung (Prioritätsreihenfolge)
— Konflikt mit der später (S139 B12b) getroffenen Anker-Logik; ggf. kurze
Stakeholder-Bestätigung vor Umsetzung sinnvoll.

**Aufwand:** S.

**Kopplung:** Gemeinsam mit Befund 2 fixen — siehe dort (identischer Code-Ort, ein Fix
behebt beide Symptome).

---

## Befund 2 — Fehlendes Inline-Abdunkeln (Movement-Karte wirkt nicht "used_elsewhere")

**Root Cause:** Kein Styling-Bug — `go_card_container_style()`
(`src/uiLayout/go_card.py:124-143`) dimmt "used_elsewhere"/"locked"/"dormant"
einheitlich (Opacity 0.55, gedimmter Rand, `_DIMMED_STATES` Zeile 90) für JEDEN Aufrufer
von `render_go_card` — Charge-Phase (Fire Overwatch, `chargephase.py:170-177` via
`render_reactive_stratagem_box`), zentrale Stratagems-Liste (`gameProtocoll.py`) und
Movement-Karte teilen exakt denselben Renderer und dieselbe CSS-Logik. Die zentrale
Liste zeigt das Advance-Reroll-GO gar nicht (es ist `timing: phase_reactive` und wird in
`gameProtocoll.py::_render_stratagem_column` Zeile 314-322 explizit übersprungen — kein
Duplikat-Rendering dort). Der einzige tatsächlich betroffene Ort ist die
Movement-Advance-Reroll-Karte: weil `_advance_reroll_state` (Befund 1) den State nie bis
"used_elsewhere" durchreicht, wird der bereits vorhandene Dimm-Code-Pfad schlicht nie
erreicht — kein separates Design-Loch. `docs/spec/design_system.md` §6.1 (Zeile
174-214) definiert das Abdunkeln explizit "einheitlich für jeden Anker ... inklusive
[...]" und nennt die Advance-Reroll-Karte namentlich (Zeile 199-200) als einen der vier
Anker, die dem gleichen Fünf-Zustands-Schema folgen — keine Lücke in der Spec.

**Fix-Ort:** identisch zu Befund 1 — `src/gameMechanic/movementPhase.py::_advance_reroll_state`
(Zeilen 255-266). Sobald der State korrekt "used_elsewhere" liefert, greift das
bestehende Styling automatisch.

**Aufwand:** in Befund 1 enthalten (kein zusätzlicher Aufwand).

**Kopplung:** MUSS mit Befund 1 zusammen gefixt werden (ein Fix, zwei Symptome).

---

## Befund 3 — Cross-Player-Area-Leak (Whirling Onslaught über beide Spielerbereiche)

**Root Cause:** Die Fraktions-/Spieler-Filterung selbst ist korrekt (kein Datenfehler):
`render_reactive_stratagem_box(def_faction, ...)` in `_render_resolution_tab`
(`src/uiLayout/_common.py:2035-2045` Hit-Anker, `:2074-2084` Wound-Anker — hier hängt
Whirling Onslaught, `:2107-2116` Save-Anker) lädt via `load_stratagems(faction_dir_for(def_faction))`
ausschließlich den GO-Pool der VERTEIDIGENDEN Fraktion; `player: inactive` +
`stratagem_usable_by_player()` grenzen zusätzlich korrekt ein. Der Leak ist strukturell/
layoutbedingt, nicht fraktionell: `render_attack_resolution()` wird in BEIDEN Phasen
außerhalb der Zwei-Spalten-Struktur aufgerufen —
`src/gameMechanic/fightPhase.py:395-397` (`_render_display()` liefert `attack_form_shown=True`
und die Methode `return`t VOR der `col1, col2 = st.columns(2)`-Zeile 403) sowie
`src/gameMechanic/shootingPhase.py:187` (gleiches Muster: außerhalb der Spalten bei
Zeile 106-120). Während der Attacken-Auflösung wird die komplette
Zwei-Spieler-Spalten-Ansicht durch EIN volles-Breite-Panel ersetzt (Angreifer- +
Verteidiger-Daten kombiniert in einem Tab je Waffe×Ziel) — dasselbe Bug-Muster, das
S139 E7 bereits für Cut Them Down behoben hat (damals: Box wurde einmal außerhalb
`st.columns()` gerendert statt pro Spalte). Hier wurde die per-Spalten-Behandlung nie
nachgezogen, weil die Resolution-Tabs beider Seiten Daten strukturell mischen — eine
reine "in die richtige Spalte verschieben"-Lösung ist nicht 1:1 übertragbar, da der Tab
selbst beide Spieler zeigt. Zusätzlicher, kleinerer Befund am selben Ort: der Aufruf von
`render_go_card` innerhalb `render_reactive_stratagem_box` (Zeile 876-889) übergibt kein
`target_name` — die Karte zeigt also nicht einmal an, welcher Einheit/welchem Spieler das
GO gehört, was die visuelle Unklarheit verstärkt (im Gegensatz zur zentralen Liste,
Zeile 361-372, die `target_name` setzt).

**Fix-Ort:** primär `src/gameMechanic/fightPhase.py::_render_display` (Zeile 558-573,
insb. Aufruf `render_attack_resolution("fight")` Zeile 572) und
`src/gameMechanic/shootingPhase.py` (Aufruf `render_attack_resolution("shooting")`
Zeile 187) — beide rendern die Resolution-Tabs strukturell außerhalb der
Spieler-Spalten. Sekundär `src/uiLayout/_common.py::render_reactive_stratagem_box`
(Zeile 876-889) — `target_name` ergänzen als Sofort-Linderung unabhängig vom
Layout-Fix. Eine echte Spalten-Bindung erfordert eine Entscheidung: Resolution-Tab
bewusst als geteilte Ansicht beibehalten (dann nur visuelle Kennzeichnung "gehört
Spieler X" nachrüsten) ODER strukturell in die verteidigende Spalte verlegen (größerer
Umbau, da Angreifer-Daten dann getrennt dargestellt werden müssten).

**Aufwand:** M (Scope-Entscheidung mit Stakeholder nötig, bevor Umsetzung beginnt —
reiner Layout-Fix vs. Komponenten-Umbau).

**Kopplung:** allein fixbar, aber Scope-Frage zuerst klären (siehe oben) — nicht mit
Befund 1/2 gekoppelt (andere Codepfade).

---

## Befund 5 — Insane-Bravery-Ziel-Bindung nicht erzwungen

**Root Cause:** `_effect_gate_met()` (`src/uiLayout/gameProtocoll.py:145-177`) kennt nur
EINE unit-State-Gate-Form: `effect.type == "move", handler == "fall_back_through_models"`
(Desperate Breakout). Insane Bravery (`data/wh40k_9e/_shared/stratagems.yaml:101-112`,
`effect.type: auto_pass_morale`, `conditions: []`) fällt durch dieses Gate durch — die
Karte wird "ready", SOBALD CP reichen, unabhängig davon, ob überhaupt eine Einheit
selektiert ist. Beim Klick auf Use ruft `_use_callback()`
(`src/uiLayout/gameProtocoll.py:249-262`) `spend_stratagem(strat, player,
_selected_state_key_for(player), anchor_id=_CENTRAL_LIST_ANCHOR_ID)` auf —
`_selected_state_key_for(player)` liefert `None`, wenn keine (oder eine gegnerische)
Einheit selektiert ist. In `spend_stratagem` (`src/uiLayout/_common.py:435-509`) greift
Zeile 507-508: `if strat.effect is not None and unit_key is not None:
_apply_stratagem_effect(...)` — bei `unit_key=None` wird CP abgezogen, das GO als
verbraucht markiert, aber `activate_morale_auto_pass()` NIE aufgerufen: der Effekt
verpufft lautlos. Der B12b-Suffix bleibt aus demselben Grund leer
(`stratagem_used_elsewhere_unit_name` liest denselben `unit_key`, der hier nie gesetzt
wurde) — die Vermutung im Auftrag trifft zu.

**Fix-Ort:** `src/uiLayout/gameProtocoll.py::_effect_gate_met` (Zeilen 145-177) — Gate um
`effect.type == "auto_pass_morale"` (und generisch: jeden unit-scoped Effekt-Typ ohne
eigene Bedingungs-Keywords) erweitern, der `unit_for_check`/`unit_state_for_check`
verlangt, bevor der State auf "ready" steht; alternativ/ergänzend
`_use_callback` (Zeilen 249-262) so härten, dass ein `unit_key=None` beim Klick den
Klick verweigert statt CP+Verbrauch ohne Effekt zu buchen.

**Aufwand:** S.

**Kopplung:** allein fixbar — anderer Codepfad als Befund 1/2/3, aber dieselbe
`spend_stratagem`-Infrastruktur; Regressionstest sollte auch den B12b-Suffix (jetzt mit
korrektem `unit_key`) mitabdecken.
