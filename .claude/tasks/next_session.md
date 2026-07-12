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
- **Auftragsgrößen-Gate (S130):** kein Executor-Brief > Effort M; Test-Budget (EINE Vollsuite zentral am Wellen-Ende, `run_in_background` für pytest VERBOTEN) + harter Selbst-Stopp in jedem Brief → `agent_scopes.md` (S143 gehärtet: Stopp-Schwelle ~1,5× Budget + „DONE = Datei im selben Schritt löschen").
- **Handoff-Marker-Pflicht (S131):** STATUS-Marker als ERSTE Schreibaktion, Format exakt `STATUS: <WERT>` als nackte erste Zeile — kein HTML-Kommentar (S140).
- **Planner-Schreibrecht (S140):** Planner als general-purpose-Subagent — legt Entwurf selbst nach `docs/handoff/` ab.
- **Grundannahmen-Block (S131):** Konzept-Dokumente starten mit bestätigungspflichtigen Grundannahmen (App würfelt NICHT — Tischwürfe!) → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (Stand S143: **28** — 11 `gameMechanic/` + 17 `uiLayout/`, `backlog.md` §4; abilityEngine Option A löst 4 davon, freigegeben).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` explizit setzen. Playwright = Standard für funktionale UI-Befunde.
- **Session-Limit-Abbrüche (S137):** Subagent nicht neu starten — per `SendMessage` resumen; Freigabe-Gate re-armt nur bei dokumentierter Chat-Freigabe.
- **markdownlint-Trial (S137–S139):** `.markdownlint.jsonc` + `npm run lint:md`; Stakeholder-Entscheid behalten/entfernen steht aus.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S143, 2026-07-12)

S143: (1) **Review S142 nachgeholt** (Reviewer-Opus): GO mit Auflagen; P1-Regression
(über-breiter `_use_callback`-Guard → stiller No-Op-Klick bei tisch-aufgelösten
Stratagems) noch in S143 gefixt; Review-Datei per Lifecycle gelöscht. **Retro S142:**
Maßnahmen 1–3 freigegeben + umgesetzt (P1-Fix; `agent_scopes.md`-Briefvorlage: harter
Selbst-Stopp + DONE-Lifecycle); Maßnahme 4 (Rename-vor-Parallel-Regel) NICHT freigegeben.
(2) **Welle 1 (7 Subagenten):** Bugfix Wound/Hit-Cap — `resolve_attack_modifiers`
(`combat.py`) deckelt Zielwert auf [2,6], `diceHtml.py`-Eff.-Zeile konsumiert den Wert
(natürliche 6 = Erfolg, 1 = Fehlschlag; Saves unangetastet), 4 neue Tests. Bugfix
Morale-Selektion: inaktiver Spieler konnte in der Morale-Phase keine eigene Einheit
wählen (Root-Cause `unitCard.py` `_TARGET_PHASES` ohne morale — NICHT S141-Befund 5!)
→ `_self_select_eligible` + `_BOTH_PLAYERS_SELF_SELECT_PHASES={"morale"}`. Neues
Prädikat `is_unit_scoped_effect` (`stratagemEngine.py`) an Gate, Spend-Guard und
`target_name`-Pfeil + Gegenfall-Regressionstest. Roster-Loader-Test auf Glob (8 Roster,
`backlog.md` §4d ✅). (3) **Drei ANSWERED-Konzepte** in `docs/handoff/`:
`S143_abilityengine_refactor.md` (Option A+B freigegeben), `S143_stratagem_kodex_abgleich.md`
(Necrons: 16 White-Dwarf-Einträge entfernen; Orks: 8 Vigilus-Kandidaten klären),
`S143_on_target_anker_konzept.md` (Option A freigegeben). (4) **FixD-Plan freigegeben**
(`docs/audit/plans/S142_fixD_resolution_tabs.md`, 3 Teil-Briefe, Mockup-Gate vor Brief 2).
(5) Stakeholder-UI-Verifikation: Insane Bravery ✅, Emergency Disembark ✅.
Vollsuite **1808 passed / 99,12 %**, Architektur-Gates grün, mypy 28 == Baseline.
Planning: `docs/handoff/S143_planning.md` ANSWERED.

Frühere Sessions (S60–S142): `docs/metrics/session_archive.md`.

### ▶ Nächste Schritte (S144, Reihenfolge)

1. **Review + Retro S143** (regulär am Session-Ende S143 durch Wind-down entfallen —
   wie S142 nachholen, bevor neue Arbeit beginnt).
2. **Manuelle UI-Verifikation der zwei Bugfixes** beim Stakeholder abfragen (Schritte unten).
3. **Stratagem-Datenpflege:** 16 Necron-Supplement-Einträge entfernen (Liste ANSWERED in
   `S143_stratagem_kodex_abgleich.md`) + Ork-Vigilus-Klärung (8 Einträge, eigene Aufgabe).
4. **mypy-Ratchet gameMechanic** (11 Fehler) inkl. abilityEngine Option A (freigegeben);
   danach Option B (gemeinsamer Filter+Akkumulier-Helfer).
5. **FixD-Ausführung** (3 Teil-Briefe) + **on_target-Anker Option A**
   (`S143_on_target_anker_konzept.md`) — nicht parallel zu mypy-uiLayout (Datei-Überschneidung).
6. **mypy-Ratchet uiLayout** (17 Fehler).

**Manuelle UI-Verifikation — Stand nach Stakeholder-Rückmeldung (2026-07-12 spät):**

- ✅ Wound-Cap bestätigt („Eff. 6+", 6 als Erfolg). ✅ Morale-Selektion bestätigt.
- 🔲 Spend-Guard (tisch-aufgelöstes Stratagem ohne Einheit → CP-Abzug + „used"): laut
  Stakeholder erst im Roster-Builder prüfbar (Relic-Vergabe) — offen halten.
- 🔲 B12b-Punkte (3) weiter offen.
- ✂️ **Klan-Affinität als Verifikationspunkt GESTRICHEN (Stakeholder-Klärung):** Es gibt
  keine Klan-Affinität zu Call da WAAAGH. Stattdessen fehlen **Klan-Fähigkeiten (Ork-
  Kulturs)** als Feature — analog stehen **Dynastie-Fähigkeiten (Necron Dynastic Codes)**
  noch aus. Beides Teil von **Ziel 7** → S144-Planner nimmt es als Planungsgegenstand auf
  (gegen `ziel7.md`/`backlog.md` verorten; Datenlage: kein `klan`-Schlüssel in Rosters,
  kein Fähigkeits-Block in `data/wh40k_9e/orks/`).
- Whirling-Onslaught-Position vom Stakeholder erneut bestätigt: Box soll am
  Ziel-Zuweisungs-Screen erscheinen („✓ Skorpekh Destroyers"-Toggle) — deckt sich exakt
  mit dem freigegebenen on_target-Konzept Option A (S144 Schritt 5, war nicht Teil S143).

**Erkenntnisse/Retro-Kandidaten S143:** (a) Budget-Selbstwahrnehmung der Executor
unzuverlässig — W1-A verbrauchte ~99k (Budget 30k) und meldete „unter Selbst-Stopp",
W1-E 36k (Budget 8k); gehärtete Vorlagen-Regel greift erst ab S144 → Wirkung prüfen,
ggf. Messkommando in den Brief. (b) Lehre aus Review-Befund 1 (umgesetzt): Gate +
Spend-Site teilen EIN Prädikat; Regressionstest am Gegenfall aufhängen. (c) Symptom-
Gleichheit ≠ Ursachen-Gleichheit: Morale-Selektions-Bug sah aus wie S141-Befund 5, war
aber eigenständig — Root-Cause-Verifikation im Brief hat sich ausgezahlt. (d) Tool↔Doku-
Drift: `tools/rotate_history.py` erwartet Marker `### ▶ Nächster Schritt`, die Datei heißt
seit Sessions `### ▶ Nächste Schritte (…)` → Stand-Reset schlägt fehl (Archiv-Zeile kommt
trotzdem an); S144 entscheiden: Marker im Tool lockern oder Überschrift angleichen.

**Ratchet/Rest unverändert:** `on_declaration`-Befund (`chargePhase.py`/`fightPhase.py`);
Stil-Nit `undo_stratagem` in-place; R-PROTO-02; Rand-Design-Konzept; GO-Keyword-Nachpflege
(bis B13); 4c-Folge-Split; Fold-Heuristik; Totalvernichtungs-Spielende; Kleinschulden →
`backlog.md`. Custodes hat noch keine Stratagem-Daten (W1-F-Befund).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
