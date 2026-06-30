# Planning-Entwurf — Session S112

**Datum:** 2026-06-30
**Erstellt von:** Planner-Subagent (Sonnet)
**Status:** NEEDS-DECISION (Ziel7-Frage, s. u.)

## Kurz-Zusammenfassung

S112 hat einen klaren Schwerpunkt: Plan 031 (Protokoll-Meta-Timing-Bugs) ist P-hoch und
regelwidrig — zwei Schritte, davon Step 1 trivial (XS). Step 2 ist die eigentliche
Arbeit (S–M): Pending-Flag in `game_state.py:_reset_round_choice_state()` einführen und
`is_active`-Gate in `armyCard.py:_render_round_choice_ui()` auf dieses Flag umstellen.
Doku-Drift (Coverage-Zahlen 92 % → 99 %) ist eine kleinere Aufräumarbeit (XS) und passt
als zweite Aufgabe rein, wenn Headroom bleibt. Ziel6-Konsolidierung ist P-mittel für
danach. Ziel7-Bundling ist eine offene Stakeholder-Entscheidung — nicht einplanen.

---

## Aufgabe 1 — Plan 031 Step 1: „Change extra directive"-Button entfernen

**Ziel:** Den Button auf Z. 219–225 in `armyCard.py` entfernen, der eine nachträgliche
Änderung der Extra-Direktive in jeder Phase erlaubt. Das ist regelwidrig: laut Wahapedia
`faction_overview.txt` Z. 579 wird die Extra-Direktive „at the start of each battle round"
gewählt — danach gesperrt bis zum nächsten Rundenanfang.

**Schritte:**
1. Block Z. 219–225 in `_render_extra_round_choice()` entfernen:
   `if is_active and st.button("Change extra directive", ...):`
   Der gesamte `if extra_directive:`-Zweig bleibt, nur der Change-Button entfällt.
2. Den `else:`-Zweig (Z. 226–249, Direktiven-Wahl-Buttons) prüfen: diese Buttons sollen
   erhalten bleiben — aber nur in einem definierten Zeitfenster (Rundenanfang = Command
   Phase, bevor irgendwer einen Zug gemacht hat). Das Fenster-Gate folgt in Step 2.
   Für Step 1 bleibt der `else:`-Zweig unverändert (er zeigt bereits nur bei
   `is_active`).

**Betroffene Dateien:**
- `src/uiLayout/armyCard.py` (Z. 219–225 entfernen)

**Tests:**
- Regressionstest: `test_change_extra_directive_button_absent_after_directive_set` in
  einem neuen oder dem vorhandenen Render-Test-File. Da `armyCard.py` Render-Code ist
  (von Coverage ausgeschlossen), reicht ein minimaler Unit-Test, der prüft dass der
  Session-State-Key `round_choice_extra_directive_<player>` nach dem ersten Setzen nicht
  durch einen `None`-Write überschreibbar ist ohne expliziten Reset
  (d.h. `_reset_round_choice_state()` ist der einzige Reset-Pfad — bestehender Test
  `test_reset_clears_each_player_independently` in `test_round_choice_player_keyed.py`
  deckt das bereits).
- Manuelle UI-Prüfung: Nach Direktiven-Wahl für Extra-Protokoll erscheint kein
  „Change extra directive"-Button mehr in Bewegungsphase oder Schussphase.

**Token-Schätzung:** ~3k (XS — Single-File, 7 Zeilen entfernen + 1 Test)

**Tier-Empfehlung:** Executor-Subagent **Haiku** — mechanische Änderung, eindeutig
spezifiziert, kein Designspielraum.

---

## Aufgabe 2 — Plan 031 Step 2: Pending-Flag-Mechanik + is_active-Entkoppelung

**Ziel:** Die Direktiven-Wahl (primär UND extra) darf nur im Zeitfenster „Start der
Runde, bevor ein Spieler seinen Zug beginnt" erfolgen. Beides gilt für BEIDE Spieler
gleichzeitig — nicht erst wenn der Spieler aktiv ist.

**Regelgrundlage (verifiziert):**
- Wahapedia `faction_overview.txt` Z. 568: „At the start of each battle round ... reveal
  it to your opponent and **select one of its directives**." → Wahl am Rundenanfang, nicht
  im Zug. Beide Spieler wählen zeitgleich (Simultanität = Information-Symmetrie).
- Z. 579: Extra-Protokoll-Direktive: „select which directive your units will benefit from
  **at the start of each battle round**." → Gleiche Zeitregel wie die Hauptdirektive.

**Designentscheidung (Bug 1 in next_session.md):** Aktuell ist die Direktiven-Wahl
hinter `is_active` gebunden (`is_active = faction == st.session_state.get("active")`).
Der zweite Spieler sieht daher den Wahlbereich erst in seinem Zug — regelwidriger
Informationsvorteil für Spieler 1.

**Vorgeschlagene Lösung:**
- Neuer Session-State-Key pro Spieler: `round_choice_directive_pending_<player>: bool`.
  Wird in `_reset_round_choice_state()` auf `True` gesetzt (Rundenanfang = neues Pending).
  Wird auf `False` gesetzt, sobald der Spieler seine Direktive(n) gewählt hat.
- `_render_round_choice_ui()` nutzt `directive_pending` statt `is_active` als Gate für die
  Direktiven-Wahl-Buttons: Beide Spieler können wählen, solange pending=True.
  Nach Wahl → pending=False → Buttons verschwinden.
- `_render_extra_round_choice()` analog: Extra-Direktiven-Wahl-Buttons an
  `directive_pending` binden (nicht `is_active`).
- Explizites Fenster: Wenn `directive_pending=False` UND `active_directive is None`
  (Spieler hat noch nicht gewählt trotz neuem Rundenanfang — theoretisch nicht erreichbar
  nach Reset, aber defensiv absichern), Fallback-Caption.

**Achtung — kein Fraktions-String in src/:**
`round_choice_directive_pending_<player>` ist per Slot gekeyt (wie `round_choice_active_*`)
→ kein `"necrons"` oder ähnliches im Code. Konvention: `round_choice_state_key(player, "directive_pending")`.

**Schritte:**
1. `game_state.py:round_choice_state_key()` — docstring ergänzen: `directive_pending`
   als neuen `kind`-Wert dokumentieren (kein Code-Change nötig, die Fn ist generisch).
2. `game_state.py:_reset_round_choice_state()` — Pending-Flag für beide Slots auf `True`
   setzen (nach dem Reset von `active` und `directive`).
3. `game_state.py:init_state()` — Pending-Flag initial auf `False` setzen
   (Setup = kein Direktiven-Fenster offen).
4. `armyCard.py:_render_round_choice_ui()` — Gate für `_render_directive_buttons()`
   von `is_active` auf `directive_pending_key` umstellen. Wenn pending=True UND kein
   `active_directive` gesetzt → Buttons zeigen. Nach `st.session_state[directive_key] = ...`
   auch `st.session_state[directive_pending_key] = False` setzen.
5. `armyCard.py:_render_extra_round_choice()` — analog: Direktiven-Wahl-Buttons
   (Z. 230–249 nach Step-1-Bereinigung) an `directive_pending` binden.

**Betroffene Dateien:**
- `src/gameMechanic/game_state.py` (`_reset_round_choice_state`, `init_state`)
- `src/uiLayout/armyCard.py` (`_render_round_choice_ui`, `_render_extra_round_choice`)

**Tests (Regressions + neue):**
- `test_round_choice_player_keyed.py`: bestehende Tests grün halten (Reset-Verhalten
  bleibt kompatibel, nur extra `directive_pending`-Keys werden zusätzlich gesetzt).
- Neuer Test: `test_reset_round_choice_sets_directive_pending_true_for_both_slots` in
  `test_round_choice_player_keyed.py` oder `test_game_state.py`.
- Neuer Test: `test_directive_pending_cleared_after_directive_chosen` — simuliert Wahl +
  prüft pending=False danach (Unit-Test, kein Streamlit-Mock nötig wenn Render-Code
  ausgeschlossen; Logik steckt in game_state).
- `test_game_state.py`: prüfen ob `init_state()` pending=False setzt.
- `pytest --tb=short` Vollsuite: Coverage-Floor 99 % darf nicht brechen.

**Manuelle UI-Prüfung (Pflicht, da Render-Code):**
1. Rundenanfang (Command Phase, Runde 2+): BEIDE Armeeleisten zeigen Direktiven-Buttons —
   auch für den inaktiven Spieler.
2. Nach Wahl Spieler A: dessen Buttons verschwinden, Badge erscheint. Spieler B kann noch
   wählen.
3. Nach Wahl Spieler B: dessen Buttons ebenfalls weg.
4. Wechsel in Bewegungsphase: keine Wahl-Buttons mehr bei keinem Spieler.
5. Extra-Protokoll (6. Protokoll): gleicher Ablauf wie Haupt-Direktive.
6. Mirror-Match (Necrons vs. Necrons): keine Überschneidung, jeder Spieler wählt
   unabhängig.

**Token-Schätzung:** ~12k (S — 2 Dateien, ~30 Zeilen effektive Änderung, 3–4 neue Tests)

**Tier-Empfehlung:** Executor-Subagent **Sonnet** — mehrere Dateien, Session-State-Design
mit kleinem Spielraum (Fenster-Logik), Tests müssen Coverage-Floor halten. Nicht Haiku,
weil Interaktion zwischen `game_state.py` und `armyCard.py` Kontext braucht.

---

## Aufgabe 3 — Doku-Drift: Coverage-Zahlen 92 % → 99 % nachziehen (optional, wenn Headroom)

**Ziel:** Alle Erwähnungen von „92 %" in Artefakten, die sich auf das Coverage-Gate
beziehen, auf „99 %" aktualisieren. Laut `next_session.md` betrifft das:
`CLAUDE.md`, `docs/goals/backlog.md`, `docs/governance/operating_model.md`,
`docs/reference/agent_scopes.md`, `docs/spec/architecture_invariants.md`.

**Schritte:** grep-Suche nach `92 %`/`92%`, nur Gate-Bezug ersetzen (nicht jede
historische Erwähnung), diff zeigen, Freigabe einholen.

**Betroffene Dateien:** 5 Doku-Dateien (s. o.)

**Tests:** keine (reine Doku)

**Token-Schätzung:** ~2k (XS)

**Tier-Empfehlung:** Executor-Subagent **Haiku** — reine Suchen+Ersetzen in Textdateien.

---

## Aufgabe 4 — Ziel6 konsolidieren (P-mittel, wenn Zeit bleibt)

**Ziel:** Offenen Backlog in `ziel6.md` (6f, 6g-Rest, 6h Kat1–3, Relics Phase 2,
subfaction Execute-Logik) je Punkt bewerten: erledigt / bewusst-offen (daten-first) /
in aktivem Plan. Keine Implementierung — nur Status-Update und Priorisierung für S113.

**Schritte:**
1. `ziel6.md` Abschnitte 6f, 6g, 6h Kat.2+3, 6l Phase 2 lesen.
2. Gegen `git log --oneline` abgleichen (was ist bereits committet?).
3. Jeden offenen Punkt kategorisieren: erledigt / blocked-by-YAML / aktiver Plan / bewusst zurückgestellt.
4. `docs/goals/backlog.md` entsprechend aktualisieren.

**Betroffene Dateien:** `docs/goals/ziel6.md`, `docs/goals/backlog.md`

**Token-Schätzung:** ~8k (S)

**Tier-Empfehlung:** Planner-Subagent **Sonnet** (liest + bewertet Backlog, kein Code).

---

## Empfohlene Reihenfolge

| Reihenfolge | Aufgabe | Effort | Token | Subagent + Tier | Begründung |
|---|---|---|---|---|---|
| 1 | Plan 031 Step 1: Button entfernen | XS | ~3k | Executor Haiku | Trivial, regelwidrig, sofort lösbar |
| 2 | Plan 031 Step 2: Pending-Flag | S–M | ~12k | Executor Sonnet | Kern-Fix, braucht 2-Datei-Kontext |
| 3 | Doku-Drift 92→99 % | XS | ~2k | Executor Haiku | Aufräumen, kein Risiko |
| 4 | Ziel6 konsolidieren | S | ~8k | Planner Sonnet | Planung, kein Code |

**Gesamt-Schätzung:** ~25k (gut unter 90-%-Korridor-Grenze von ~135k).

---

## Offene Stakeholder-Entscheidung (NEEDS-DECISION)

**Frage:** Soll Ziel7 = „Gefechtsoptionen + subfaction-Mechanik bündeln"?
Renumbering der Folge-Ziele bestätigen?
→ Nicht einplanen, bis Entscheidung vorliegt. Koordinator leitet vor.

---

## Architektur-Gate-Hinweis

Nach Plan 031 Step 2 muss `pytest tests/architecture/ --no-cov -q` grün bleiben.
Risiko: `round_choice_directive_pending_<player>` ist ein neuer Session-State-Key in
`game_state.py` — kein Generic-src-Verstoß, da kein Fraktions-String. INV-4b-Scanner
in `tests/architecture/_vocab.py` sollte sauber bleiben.
