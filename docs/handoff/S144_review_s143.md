STATUS: ANSWERED

Retro S144: alle 4 Maßnahmen freigegeben + umgesetzt (Doku-Drift-Fix,
Cap-DRY-Backlogschuld, Worktree-Prune, Review-Budget-Regel in CLAUDE.md).

# S144 — Nachgeholter DoD-Review der Session S143

Prüfgegenstand: `432b837`, `5ccf345`, `3602ddb` (nach `3a191e8`) auf
`feature/016-protocol-rp-effects`. Der reguläre S143-Review entfiel durch Wind-down.

## Gesamturteil: GO mit Auflagen

Die drei fachlichen Änderungen in `432b837` (Natural-6-Cap, Morale-Selektion des
inaktiven Spielers, geteiltes `is_unit_scoped_effect`-Prädikat) sind **regelkonform,
generisch, vollständig getestet und sauber**. Alle Gates grün. Die beiden anderen
Commits (`5ccf345`, `3602ddb`) berühren nur `.claude/tasks/next_session.md`.

Eine **Auflage** vor Session-Abschluss: eine Doku-Drift schließen (Befund 1 — die
kanonische Zieldatei `ziel7.md` und `backlog.md` §3 nennen weiterhin die vom
Stakeholder gestrichene „Klan-Affinität" als offenen Verifikationspunkt). Zwei
Nice-to-have-Beobachtungen (Befunde 2 + 3) ohne Blocker-Charakter.

## DoD-Punkte im Einzelnen

1. **Regelkonform — ERFÜLLT.** Belegt gegen `docs/work/wahapedia_core_rules/core_rules.txt`:
   - Zeile 1708: „Unmodified hit rolls and wound rolls of 6 always succeed." → der neue
     `min(6, …)`-Cap in `combat.py` und `diceHtml._capped_modifier_threshold` ist korrekt
     (Eff. nie 7+).
   - Zeile 1707: „Unmodified hit rolls, wound rolls and saving throws of 1 always fail." →
     der beibehaltene `max(2, …)`-Floor ist korrekt (2+ = nur 1 scheitert).
   - Saves bewusst **unangetastet** — richtig: die 6-Autoerfolg-Regel gilt laut 1708 nur
     für Hit/Wound, nicht für Saves.
   - Morale: Zeile 2094 „Starting with the player whose turn is taking place, the players
     must alternate selecting a unit from their army" → beide Spieler wählen abwechselnd
     eigene Einheiten; der Fix, dass der inaktive Spieler in der Morale-Phase selbst
     selektieren darf (`_BOTH_PLAYERS_SELF_SELECT_PHASES={"morale"}`), ist regelkonform.

2. **Generisch — ERFÜLLT.** Keine neuen Fraktions-Strings/-Checks in `src/`. Die
   Prädikat-Logik dispatcht über Effekt-Typen aus YAML (`auto_pass_morale`, `invuln_save`,
   `move`+`fall_back_through_models`), nicht über Fraktionsnamen. Fraktionsnamen in den
   Kommentaren/Tests (`necrons`, `_shared`) sind Referenzen bzw. Testdaten, keine Logik.
   INV-4b-Wächter grün (siehe Punkt 4).

3. **Tests grün — ERFÜLLT.** `pytest --tb=short`: **1808 passed**, Coverage **99,12 %**
   (Gate 99 %). Jeder S143-Bugfix hat einen Regressionstest:
   - Natural-6-Cap: `test_combat_6d.py` (`test_wound_capped_at_6…`, `test_hit_capped_at_6…`,
     `test_wound_floor_at_2…`) + `test_resolution_tab.py`
     (`test_wound_eff_row_clamps_at_six…`).
   - Morale-Selektion: `test_unit_card.py` (3 Tests inkl. Gegenrichtung „inaktiv bleibt in
     rundenbasierten Phasen gesperrt").
   - `is_unit_scoped_effect`: `test_stratagem_engine.py` (5 Tests inkl. `grant_relic`-
     Gegenfall) + `test_game_protocoll.py` (Spend-Gegenfall).

4. **Architektur-Gate — ERFÜLLT.** `pytest tests/architecture/ --no-cov -q`: **8 passed**
   (alle vier Invarianten grün; INV-5 next_session.md 104/120 Zeilen — unter der harten
   Decke). Regel-Ledger (impl. ohne Test) = 0.

5. **Clean Code — ERFÜLLT (mit Housekeeping-Hinweis, Befund 3).** `black --check .` sauber
   (140 Dateien), `ruff check` sauber, `isort --check-only src/ tests/` sauber. Der einzige
   isort-Fehler betrifft `.claude/worktrees/agent-a6f336af14664d70d/…/game_state.py` — eine
   **nicht getrackte** verwaiste Agent-Worktree-Datei, nicht Teil des Prüfgegenstands.

6. **UI manuell verifiziert — ERFÜLLT (dokumentiert).** `next_session.md` trägt den
   Stakeholder-Stand nach: Wound-Cap ✅ und Morale-Selektion ✅ bestätigt; offene Punkte
   sind explizit als 🔲 dokumentiert (Spend-Guard — erst im Roster-Builder prüfbar; B12b
   3 Punkte). Ziel-7-Stufe-B-Verifikation (Necron-Roster) bleibt laut `ziel7.md:76` offen —
   korrekt als offen geführt.

7. **Artefakte aktuell — TEILWEISE (Befund 1).** Handoff-Marker konsistent (alle
   S143-Dateien ANSWERED, Review-Datei S142 laut Historie per Lifecycle gelöscht).
   Roster-Loader-Glob-Umstellung → `backlog.md` §4d abgehakt. **Aber:** die
   Klan-Affinitäts-Klärung aus S143 wurde nur in `next_session.md` (Commit `3602ddb`)
   nachgezogen, nicht in der kanonischen Zieldatei — siehe Befund 1.

---

## Befundliste

### Befund 1 — [MITTEL] Doku-Drift: „Klan-Affinität" in ziel7.md/backlog.md nicht nachgezogen

**Beleg:** Commit `3602ddb` hält in `.claude/tasks/next_session.md` fest, dass es
**keine** Klan-Affinität zu „Call da WAAAGH" gibt und der Verifikationspunkt gestrichen
ist (ersetzt durch fehlende Klan-Fähigkeiten/Dynastie-Fähigkeiten als Ziel-7-Feature).
Die kanonischen Artefakte tragen das nicht nach:
- `docs/goals/ziel7.md:89` (Stufe C) nennt weiterhin „Emergency Disembarkation +
  Klan-Affinität" als offenen manuellen Verifikationspunkt.
- `docs/goals/backlog.md:454-455` (§3) listet „Klan-Affinität am neuen Ork-Transport-
  Roster" als offenen Punkt.

Das ist genau die Drift, vor der DoD-Punkt 7 warnt: die Erkenntnis lebt nur in der
flüchtigen Stand-Datei, während die dauerhaften Zieldokumente einen widerlegten
Verifikationspunkt weiterführen — ein späterer Planner könnte ihn erneut einplanen.

**Lösungsvorschlag:** In `ziel7.md` Stufe C den Passus „+ Klan-Affinität" streichen bzw.
durch den neuen Scope „Klan-Fähigkeiten (Ork Kulturs) + Dynastie-Fähigkeiten (Necron
Dynastic Codes)" ersetzen; `backlog.md` §3 analog anpassen. Klein, kann im
S144-Abschluss miterledigt werden.

### Befund 2 — [NIEDRIG] Doppelte [2,6]-Cap-Implementierung (Sync-Risiko)

**Beleg:** Der 9E-Cap existiert jetzt an zwei Stellen: `combat.resolve_attack_modifiers`
(`src/gameMechanic/combat.py:207,213`) und `diceHtml._capped_modifier_threshold`
(`src/uiLayout/diceHtml.py:31`). Der Wound-Renderer konsumiert inzwischen den
combat-Wert (Parameter `modified`), fällt aber weiterhin auf die lokale Berechnung
zurück; die Zwischen-Modifier-Zeilen nutzen weiter die lokale Funktion. Beide wurden
identisch gefixt, sind also aktuell konsistent — aber wenn die Regel künftig nur an
einer Stelle angepasst wird, driften Anzeige und Rechnung auseinander.

**Lösungsvorschlag:** Kein akuter Handlungsbedarf (kein Bug). Als Backlog-Kleinschuld
notieren: langfristig `_capped_modifier_threshold` als dünnen Wrapper um die
combat-Cap-Logik führen oder die Zwischenzeilen ebenfalls aus `atk_result` speisen,
damit es genau eine Cap-Quelle gibt (DRY).

### Befund 3 — [NIEDRIG/Housekeeping] Verwaister Agent-Worktree bricht repo-weites isort

**Beleg:** `.claude/worktrees/agent-a6f336af14664d70d/src/gameMechanic/game_state.py`
(snake_case-Altstand) lässt `isort --check-only .` (repo-weit) fehlschlagen. Die Datei
ist **nicht** git-getrackt (`git ls-files | grep worktrees` = 0), also kein Code-Befund —
aber ein liegengebliebener Subagent-Worktree, der Formatter-Checks und ggf. Suchen
verrauscht.

**Lösungsvorschlag:** Worktree entfernen (`git worktree prune` bzw. Verzeichnis löschen,
sofern kein laufender Agent ihn hält). Rein hygienisch, kein Blocker.
