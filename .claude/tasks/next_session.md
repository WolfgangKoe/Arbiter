# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start:** „start next session" → Planner-Subagent (`CLAUDE.md`+`docs/goals/ziel7.md`+`docs/goals/backlog.md`, Scope `docs/reference/agent_scopes.md`) legt Entwurf vor, Koordinator zeigt ihn, erst nach Freigabe los; „Plan ist freigegeben" = Shortcut direkt los. Einstieg `LEITSTAND.md`, Rollen/Tier `docs/governance/operating_model.md`.
- **ADR-0007:** Koordinator routet, liest keine Quelldateien/Vollergebnisse — Detail-Planung/Review laufen als Subagenten; Stakeholder-Entscheidungen async über Mailbox (`docs/handoff/`, NEEDS-DECISION→ANSWERED), nicht Chat.
- **Ende:** Review (Reviewer-SA) → Retro → Maßnahmen-Entscheid (Stakeholder) → Abschluss: diese Datei aktualisieren (ZUERST lesen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke 120 Zeilen (Test rot darüber); beim Reißen tief auf ≤ 70 kürzen (Erledigtes → `backlog.md`/`session_archive.md`).
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten = stehende Freigabe (ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Auftragsgrößen-Gate (S130):** kein Executor-Brief > Effort M; Test-Budget (EINE Vollsuite zentral am Wellen-Ende, `run_in_background` für pytest VERBOTEN) + Selbst-Stopp in jedem Brief → `agent_scopes.md`.
- **Handoff-Marker-Pflicht (S131):** jeder Brief, der nach `docs/handoff/` schreibt, nennt den STATUS-Marker für Zeile 1 (S137: Haiku-Agent vergaß ihn trotz Brief → im Brief als ERSTE Schreibaktion vorgeben). Format exakt `STATUS: <WERT>` als nackte erste Zeile — **kein** HTML-Kommentar `<!-- … -->`, der reißt den Hygiene-Test (S140-Maßnahme 1).
- **Planner-Schreibrecht (S140-Maßnahme 2):** Planner als general-purpose-Subagent beauftragen (nicht Plan-Agent-Typ) — der legt den Entwurf selbst nach `docs/handoff/` ab, statt ihn durchs Koordinator-Fenster zu schleusen.
- **Grundannahmen-Block (S131):** Konzept-Dokumente starten mit bestätigungspflichtigen Grundannahmen (App würfelt NICHT — Tischwürfe!) → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (Stand S138: 62 — zwei Sessions überfällig, S139 P1-Pflicht; **S141: 48 → 28**, `state`-Contract-Fix erledigt, Rest 17 `uiLayout/` + 11 `gameMechanic/`-Restfehler anderer Klasse, s. `backlog.md` §4).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` explizit setzen. Playwright = Standard für funktionale UI-Befunde.
- **Session-Limit-Abbrüche (S137):** Bricht ein Subagent mit „session limit" ab, NICHT neu starten — per `SendMessage` resumen (Kontext intakt, hat 6/6 funktioniert). Freigabe-Gate re-armt sich beim Neustart → Koordinator re-armt nur bei dokumentierter Chat-Freigabe.
- **markdownlint-Trial (S137–S139):** `.markdownlint.jsonc` + `npm run lint:md` (cli2 v0.14, Node-18-Pin). IDE-Diagnosen erreichen den Koordinator nach Edits. Nach S139: Stakeholder entscheidet behalten/entfernen.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S142, 2026-07-12)

S142 (Commit `1621117`, Branch `feature/016-protocol-rp-effects`): (1) **Rename-Welle:**
13 src/-Module snake_case→camelCase inkl. Imports/pyproject/Wächter/lebender Doku.
(2) **Option B umgesetzt:** neues Modul `src/gameMechanic/stratagemEngine.py` konsolidiert
`_apply_stratagem_effect`, `_effect_gate_met`, `stratagem_strength_bonus`. (3) **FixC
(Insane Bravery):** Formentabelle `_UNIT_SCOPED_EFFECT_TYPES` im Gate + `unit_key=None`-
Härtung in `gameProtocoll._use_callback`; 3 B12b-Regressionstests. (4) **FixD-
Sofortlinderung:** Reaktiv-GO-Box zeigt Ziel „Einheit · Spieler" (Helper
`reactive_box_target_label` in `goCard.py`); 5 Alt-Tests mit Freigabe angepasst
(`name_en` an Attrappen). (5) **FixD-Detail-Plan** liegt in
`docs/audit/plans/S142_fixD_resolution_tabs.md` — **WARTET AUF FREIGABE** (3 Teil-Briefe,
Mockup-Gate vor Brief 2). (6) Insassen-Feature runterpriorisiert → `backlog.md` §2;
`S141_ui_befunde_group_b.md` gemäß Lifecycle gelöscht. (7) Doku-Hygiene
Stakeholder_Beobachtungen erledigt. Vollsuite **1788 passed / 99,12 %**, Wächter grün.
Planning: `docs/handoff/S142_planning.md` Revision 3, ANSWERED. **Review + Retro S142
stehen noch aus** (fielen dem Kontext-Korridor zum Opfer → S143 Punkt 1).

## Stand nach S141 (2026-07-12)

S141: mypy-Baseline **48 → 28** (`state`-Contract-Fix, Commits `42af867`/`292b3ad`);
Ork-Transport-Roster `orks_transport.yaml` (`cbaeeb2`); B12b-Suffix verdrahtet (`cdb55e2`);
zwei UI-Verifikations-Bugfixes: Emergency-Disembark-Sichtbarkeit (`f36f1e7`),
Movement-Timing/Abdunkeln (`7fc8b16`). Vollsuite **1783 / 99,15 %**. Zwei weitere gemeldete
Bugs (Insane-Bravery-Ziel, Cross-Player-Leak) diagnostiziert, wegen Korridor nach S142
vertagt — Fix-Orte in `docs/handoff/S141_ui_befunde_group_a.md`.

## Stand nach S140 (2026-07-12)

S140 (Review **GO**, 0 Auflagen; Vollsuite 1772 passed / 99,14 %, mypy **54 → 48**):
**Dynastie↔Protokoll-Kopplung komplett** — Round-Zweig wertet `subfaction_affinity`
jetzt aus: Gate `has_round` auf `bool(active_id)` gelockert + Affinitäts-Check in
`_active_directive_effects` (`abilityEngine.py`) und `active_round_choice_buff_labels`
(`gameState.py`, Unit-Card-Badges); UI-Zweig in `armyCard._render_round_choice_ui`
rendert bei Treffer sofort „… BONUS (BOTH)"-Badge statt Primary/Secondary-Buttons.
Regressionstests je 6 Dynastien in beiden Schichten; Regelzuordnung vom Reviewer gegen
Wahapedia bestätigt. Stakeholder-UI-verifiziert: positiv. Zusätzlich
`gameActionsArea.py` voll typisiert (0 neue `type: ignore`). Backlog: Affinitäts-Punkt
✅, NEU 🔲 „Dynastie-Code je Einheit statt Roster-Ebene" (Konzept-Frage 2,
Stakeholder-Entscheid S140: erfassen, nicht umsetzen).

Frühere Sessions (S60–S139): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächste Schritte (S143, Reihenfolge)

1. **Review + Retro S142 nachholen** (fiel dem Kontext-Korridor zum Opfer).
2. **mypy-Ratchet gameMechanic-Rest** (11 Fehler, Baseline 28 → senken; Plan-Aufgabe 8).
3. **abilityEngine-Refactor-Recherche** (read-only, Design-Vorschlag; Plan-Aufgabe 5 —
   Konsolidierung via `stratagemEngine.py` ist jetzt da).
4. **mypy-Ratchet uiLayout** (17 Fehler; Aufgabe 9).
5. **Roster-Loader-Test auf Glob** (Aufgabe 10; `backlog.md` §4d).
6. **FixD-Plan-Freigabe beim Stakeholder einholen**
   (`docs/audit/plans/S142_fixD_resolution_tabs.md`).

**Offene manuelle UI-Verifikation (Stakeholder):** B12b-Punkte (3) + Insane Bravery:
ohne gewählte Einheit „locked: select an eligible unit" statt „ready", mit Einheit
Klick → Morale-Auto-Pass; Reaktiv-Box-Ziel-Label an Hit-/Wound-/Save-Ankern (z. B.
Whirling Onslaught beim Verteidiger); Klan-Affinität Ork-Transport-Roster.

**Erkenntnisse/Retro-Kandidaten S142:** (a) Session-Limit brach alle 4 Subagenten ab —
Resume per SendMessage mit git-status-Zwischenstand funktionierte gut. (b) A3-Executor
überzog XS-Budget massiv (~102k statt ~10k) — Budget-Durchsetzung in Briefs prüfen.
(c) Haiku-Brief setzte DONE-Marker ohne Lifecycle-Löschung → Hygiene-Test rot;
Brief-Vorlage: „DONE = Datei löschen". (d) Wellen-Commit statt Rename-Slice, weil
verschränkte Edits in denselben Dateien — Rename-Aufträge künftig VOR Parallel-Arbeit
committen.

**Ratchet/Rest unverändert:** mypy-Baseline 28 weiter Richtung 0 (`uiLayout/` 17 +
`gameMechanic/` 11, `backlog.md` §4); `on_declaration`-Befund (`chargePhase.py`/
`fightPhase.py` ohne `unit_for_conditions`) → `backlog.md`; Stil-Nit `undo_stratagem`
in-place; R-PROTO-02 offen; Rand-Design-Konzept; GO-Keyword-Nachpflege (zurückgestellt
bis B13, Schema-Befund); 4c-Folge-Split, Fold-Heuristik, Totalvernichtungs-Spielende,
Kleinschulden → `backlog.md`.

**Prozess:** Vollsuite bei parallelen Wellen nur EINMAL zentral am Wellen-Ende
(`operating_model.md` Event 3).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
