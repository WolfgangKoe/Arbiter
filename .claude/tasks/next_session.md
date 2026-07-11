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
- **mypy Zero-Error-Ratchet:** Baseline sinkt jede Session Richtung 0 (Stand S137: 62 — diese Session nicht gesenkt, S138 fällig).
- **Vollsuite-Timeout (S136):** Bash-`timeout: 600000` explizit setzen. Playwright = Standard für funktionale UI-Befunde.
- **Session-Limit-Abbrüche (S137):** Bricht ein Subagent mit „session limit" ab, NICHT neu starten — per `SendMessage` resumen (Kontext intakt, hat 6/6 funktioniert). Freigabe-Gate re-armt sich beim Neustart → Koordinator re-armt nur bei dokumentierter Chat-Freigabe.
- **markdownlint-Trial (S137–S139):** `.markdownlint.jsonc` + `npm run lint:md` (cli2 v0.14, Node-18-Pin). IDE-Diagnosen erreichen den Koordinator nach Edits. Nach S139: Stakeholder entscheidet behalten/entfernen.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py` (Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR). App bei Session-Start nur per curl prüfen, bei Bedarf selbst neu starten.

---

## Aktueller Stand (nach S137, 2026-07-11)

S137 (Review **GO**, `S137_review.md`): Beobachtungs-Welle komplett, alle Fixes vom
Stakeholder UI-verifiziert — unitCard-Badge-Trennung + CAST (`unitCard.py`, 8 Tests);
**Stikkbomb-Fix:** Inline-Attacken-Reroll war nur im Nahkampf-Zweig verdrahtet (alle 45
Würfel-Attacken-Waffen sind Fernkampf → Feature griff nirgends), Fernkampf-Zweig + Phase-
Key-Fix fight/shooting (`_common.py`, 4 Tests); Wound→Save-Doppel-Trenner + Power-klaw-
Doppelbadge raus; Chargephase-Testlücke zu. **B12-Konzept** liegt vor
(`S137_B12_konzept.md`, 18 Render-Stellen, Teil-Briefs a/b/c) — **Stakeholder-Kommentare
in der Datei, S138 ZUERST lesen**. YAML-Trunkierungs-Scan: 55-Zeichen-Limit, 44 Einträge
(`S137_yaml_trunkierung_scan.md`) → Backlog §2 WICHTIG. Backlog B12/B13/B14 neu;
markdownlint-Trial eingerichtet. Vollsuite 1708 passed / 99,12 %, mypy 62.

Frühere Sessions (S60–S136): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S138)

1. **B12 umsetzen:** Stakeholder-Kommentare in `S137_B12_konzept.md` lesen →
   Teil-Briefs B12a→b→c (Auslöser-Tracking; Undo nur am Auslöse-Anker; Inline nie
   Undo; Once-per-Phase erzwungen). Der offene „S136-Rest: Verhalten" hängt daran.
2. **Neue Beobachtungen triagieren** (`Stakeholder_Beobachtungen.md`, 9 Einträge vom
   11.07., je Screenshot daneben): leere Ork-Badge; Cut-them-down-Karte über BEIDE
   Spielerflächen (laut Design verboten); Keyword-Badges-Farbe + Fraktions-Keyword
   „Ork" darf nicht in unitCard (Fehler unitCard vs. YAML prüfen); Rand-Design
   Spieler 2 vertikal spiegeln + auf GOs übertragen (zu grell); GO-Keywords in YAML
   systematisch nachpflegen (Subagent); 2026-07-09-Screenshots 21-29-43/21-36-36 noch
   ungeplant (= B8/B4-Welle-2-Bezug prüfen); HI-UI-Konzept auf andere Phasen
   ausrollen — wo eingeplant?; Conquering-Tyrant-Hinweis in gameActionsArea
   (kann weg, steht in armyCard); **WAAAGH-End-State endet nie (Regelverstoß?
   gegen Wahapedia prüfen!)**.
3. **YAML-Vervollständigung (WICHTIG, Stakeholder):** Scraper prüfen (war angeblich
   schon gegen Trunkierung gefixt — alter Stand?), 55-Zeichen-Limit beheben,
   44 Einträge re-scrapen, Vollsuite. → Backlog §2.
4. **Kleinigkeit (Entscheid S137):** Debuff-Badge-Label kürzen auf exakt „-1 to Hit"
   (Badge kleiner).
5. **P3 aus S137 verschoben:** 4c-Folge-Split scopen (Paket 7/8, `design_system.md`
   §6.2) → B7/B9-Konzept + B2 Option A → Welle 2 (Task 7 Dakka `S133_plan.md`, Task 8
   `before_battle`, B8, B4-Sofortteil).
6. **Kleinschulden (unverändert aus S136):** Smoke-Test `hook_pytest_foreground.py`;
   `design_system.md` §6.3 präzisieren; mypy 62→runter; `_common.py`-Refactor (Backlog
   §4); S130-GO-Verifikation; 037 Docker-Smoke; Deny-Caption blockiert; Direction-
   Entscheide vertagt (Backlog §5).

**Prozess:** Vollsuite bei parallelen Wellen nur EINMAL zentral am Wellen-Ende
(`operating_model.md` Event 3).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
