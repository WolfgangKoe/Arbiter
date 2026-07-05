# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel7.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. Ziel-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **Checkbox-Sync prüft auch Commit-Behauptungen:** Session-Start-Sync nicht nur gegen Ziel-Checkboxen,
  sondern auch Titel wie „archive/close" gegen Datei-Realität verifizieren (b3ebfd5 behauptete
  Archivierung ohne Vollzug, S119→S120-Befund). Restrisiko bewusst nicht test-bewacht — Kompensation:
  Reviewer-Pflicht + dieser Sync.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S123, 2026-07-05)

**S123:** Necron-Stratagem-Vollabgleich 59/59 erledigt (27 Befunde; „not loaded"-Header war
stale → alles Live-Bugs). Engine-Fix `stratagem_strength_bonus` jetzt `unit_key`-gescopt
(6 Alt-Tests bewusst angepasst, Regressions- + HTML-Tests neu, UI verifiziert ✅). 5 HOCH-
Datenfixes in `necrons/stratagems.yaml` (falsche Effekte entfernt statt falsch gelassen;
`resurrection_protocols_character` neu, jetzt 60 Einträge). Restbefunde als Plan 032
(`docs/audit/plans/032-necron-stratagem-semantics.md`, P2/L). Artefakt-Bereinigung: Pläne
016/030 DONE, Coverage-Angaben 92→99 %, Backlog-Sync; 27 DONE-Pläne nach
`docs/audit/plans/archive/` verschoben, nur noch 5 aktive (015/017/018/026/032). Review **GO**.

Frühere Sessions (S60–S122): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

**ZWINGEND (Stakeholder-Auftrag): /improve-Session** — Vorbereitung laut Backlog §2. Danach
Kandidaten: Plan 032 (Stufe-B-Semantik), Plan 015 Steps 2–4 (Mockup-Gate VOR Step 2), ziel7
Stufe C (Orks; inkl. Boarding-Actions-Entscheid + variable CP-Kosten-UI, Backlog §2).

**Offene Punkte / Merksätze:**
(a) Retro-Beobachtung S123: Archiv-Executor umging das wieder scharfe Freigabe-Gate per
Bash-Schreibzugriff statt zu eskalieren — Maßnahme in nächster Retro entscheiden.
(b) ADR-0006:32 referenziert alten Pfad des 024-Digests (kosmetisch, bei Gelegenheit).
(c) Merkposten `hand_of_the_phaeron`/ExtraUses steht in Plan 032.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
