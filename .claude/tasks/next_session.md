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

## Aktueller Stand (nach S139, 2026-07-12)

S139 (Review **GO**, 0 Auflagen; Vollsuite 1755 passed / 99,14 %, mypy **62 → 54**):
**B12 komplett** — 5. GO-Karten-Zustand `used_elsewhere` + Auslöser-Buchhaltung
(`stratagem_use_anchors`), drei Karten-Mapper + Inline-Reroll auf Anker verdrahtet
(„Undo" nur am Auslöse-Anker, sonst gedimmt „Used"); Cut Them Down + Emergency
Disembarkation rendern dauerhaft (S138-Änderung). **Cut-Them-Down-Layout-Bug** gefixt
(Root Cause vorbestehend `b5c774b` — Box außerhalb der Spalten). Toter Code
`build_aura_range_hint_text` entfernt; INV-4b-Fehlalarm behoben; Doku §6.1/§6.3/§6.4
nachgezogen. Stakeholder-UI-verifiziert (Advance-Reroll, Cut Them Down, Layout beide
Rollen); Emergency Disembarkation mangels TRANSPORT-Roster nicht prüfbar (gleicher
Code-Pfad, unit-getestet).

Frühere Sessions (S60–S138): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S140)

1. **Dynastie↔Protokoll-Kopplung umsetzen (freigegeben, Effort S–M):** Konzept
   `S139_dynastie_protokoll_konzept.md` (ANSWERED) — Befund bestätigt = alter
   S96/S97-Backlog-Punkt: Feld `subfaction_affinity` existiert bereits (permanenter
   Zweig wertet aus), nur der Round-Zweig `_active_directive_effects` in
   `ability_engine.py` und `armyCard._render_directive_buttons` prüfen es nicht. Kein
   neues YAML-Feld nötig;
   Bedingungszweig + analoger UI-Zweig + Regressionstests je Dynastie. Nach Commit
   Konzept-Marker → DONE + löschen.
2. **mypy-Ratchet weiter senken:** Baseline 54 (S139: 62→54). Nächster größter Posten
   laut E2-Befund: `src/uiLayout/gameActionsArea.py` (generische dict/set-Argumente,
   `SessionStateProxy`-Mismatch).
3. **Dokumentierte Ratchet-Schulden aus S139 (kein Blocker):** (a) B12b-Header-Suffix
   „used on ⟨Einheit⟩" noch nicht verdrahtet (Mapper geben `None` als Grund; in §6.1
   vermerkt) — XS-Folge-Task; (b) Stil-Nit `undo_stratagem` in-place-Mutation → bei
   nächster Modul-Berührung mitziehen; (c) R-PROTO-02 `status: offen` (Aura-Tischhinweis
   entfernt, neuer Mechanismus offen).
4. **Rand-Design-Konzept** (heller Streifen links, beim 2. Spieler spiegeln, auf GOs
   übertragen); **GO-Keyword-Nachpflege** in YAML (systematisch, Subagent); **Rest
   unverändert (S137/S138):** 4c-Folge-Split (Paket 7/8) → B7/B9-Konzept + B2 Option A;
   Fold-Heuristik+Subfaction-Wiring (Retro-Maßnahme 3); Totalvernichtungs-Spielende;
   Kleinschulden (Smoke-Test `hook_pytest_foreground.py`, `_common.py`-Refactor,
   S130-GO-Verifikation, 037 Docker-Smoke, Deny-Caption, Direction-Entscheide,
   B4/B8-Welle-2-Screenshots + HI-UI-Ausrollung). Details → `backlog.md`.

**Retro-Leitlinie S139 (Stakeholder):** Kommentare/Docstrings im Code reduzieren — der
Code trägt sich selbst (deckt sich mit CLAUDE.md-Kommentar-Konvention). Kein
INV-4b-Scanner-Umbau; bei Fehlalarm auf Alltagswörter umformulieren.

**Prozess:** Vollsuite bei parallelen Wellen nur EINMAL zentral am Wellen-Ende
(`operating_model.md` Event 3).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur: `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent (Briefs ≤ M).
- **Token-Report + History (Abschluss-PFLICHT):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt (Ausnahmen: `docs/handoff/`, außerhalb Repo).
