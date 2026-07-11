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
- **Handoff-Marker-Pflicht (S131):** jeder Brief, der nach `docs/handoff/` schreibt, nennt den STATUS-Marker für Zeile 1 (S137: Haiku-Agent vergaß ihn trotz Brief → im Brief als ERSTE Schreibaktion vorgeben).
- **Grundannahmen-Block (S131):** Konzept-Dokumente starten mit bestätigungspflichtigen Grundannahmen (App würfelt NICHT — Tischwürfe!) → `agent_scopes.md`.
- **Executor-Klausel:** Dateiänderungen nur über Edit/Write, Bash nur lesend/git/pytest (S123); Selbstprüfliste enthält `python tools/mypy_gate.py` (S128).
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (Stand S138: 62 — zwei Sessions überfällig, S139 P1-Pflicht).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` explizit setzen. Playwright = Standard für funktionale UI-Befunde.
- **Session-Limit-Abbrüche (S137):** Bricht ein Subagent mit „session limit" ab, NICHT neu starten — per `SendMessage` resumen (Kontext intakt, hat 6/6 funktioniert). Freigabe-Gate re-armt sich beim Neustart → Koordinator re-armt nur bei dokumentierter Chat-Freigabe.
- **markdownlint-Trial (S137–S139):** `.markdownlint.jsonc` + `npm run lint:md` (cli2 v0.14, Node-18-Pin). IDE-Diagnosen erreichen den Koordinator nach Edits. Nach S139: Stakeholder entscheidet behalten/entfernen.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S138, 2026-07-11)

S138 (Review **GO**, Auflage erfüllt: Powerklaw-Badge-Fix + finale Vollsuite 1735 passed /
99,14 %): **WAAAGH-Endstand gefixt** — Stufen-Anker = Command-Phase des Besitzers
(`_reset_turn_state`), Once-per-Battle-Ledger `used_once_per_battle_abilities` +
armyCard-Gate; **Spielende fix nach Runde 5** (`MAX_BATTLE_ROUNDS`, `battle_over`,
`prev_phase()` hebt auf, Endstand-Anzeige in gameHeader); **unitCard-Keyword-Leck**
gefixt (`_resolve_keyword_placeholders` generisch + `_fold_faction_keyword`, Subfaction-
Wiring bleibt offen); **YAML-Trunkierung:** 47 Einträge (Ork 42/Necron 5) vervollständigt,
Wächter `test_data_quality.py`; **Badge-Wert-Doppelung** generisch gefixt (Power klaw,
Killsaw, Beast-Snagga-Klaw, Fall-Back). B12-Entscheidungen in `S137_B12_konzept.md`
gesichert (ANSWERED). Alles Stakeholder-UI-verifiziert. mypy 62 — **NICHT gesenkt, 2
Sessions überfällig.**

Frühere Sessions (S60–S137): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S139)

1. **B12 umsetzen (Teil-Briefs ≤ M):** Entscheidungen in `S137_B12_konzept.md`
   (ANSWERED) — a) Auslöser-Tracking, b) Undo nur am Auslöse-Anker (Inline bekommt
   Undo, 4a revidiert), c) Once-per-Phase erzwungen (Wound/Save „used" nach Hit-Einsatz).
2. **mypy-Ratchet senken (P1-Pflicht):** Baseline 62 seit S137 unverändert — S139 muss
   sie senken, sonst droht Review-NO-GO.
3. **Dynastie↔Protokoll-Kopplung (neuer Befund):** „beide Direktiven" gilt laut
   `faction_overview.txt:908-936` für ALLE 6 Dynastien; YAML-Feld `linked_protocol`
   fehlt → Konzept + Datenmodell-Ergänzung.
4. **Cut-Them-Down-Bug:** GO-Karte erscheint über beide Spielerflächen (laut Design
   verboten) — GO-Card/UI-Layout prüfen.
5. **Toter Code entfernen (Retro-Maßnahme 2, XS):** `build_aura_range_hint_text` +
   Tests, `acceptance/rules.md`-Referenz nachziehen.
6. **Rand-Design-Konzept** (heller Streifen links, beim 2. Spieler spiegeln, auf GOs
   übertragen); **GO-Keyword-Nachpflege** in YAML (systematisch, Subagent); **Rest
   unverändert (S137/S138):** 4c-Folge-Split (Paket 7/8) → B7/B9-Konzept + B2 Option A;
   Fold-Heuristik+Subfaction-Wiring (Retro-Maßnahme 3); Totalvernichtungs-Spielende;
   Kleinschulden (Smoke-Test `hook_pytest_foreground.py`, `design_system.md` §6.3,
   `_common.py`-Refactor, S130-GO-Verifikation, 037 Docker-Smoke, Deny-Caption,
   Direction-Entscheide, B4/B8-Welle-2-Screenshots + HI-UI-Ausrollung). Details →
   `backlog.md`.

**Prozess:** Vollsuite bei parallelen Wellen nur EINMAL zentral am Wellen-Ende
(`operating_model.md` Event 3).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
