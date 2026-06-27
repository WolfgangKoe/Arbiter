# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planning vorlegen** (Prioritäten + Token-Schätzung), erst nach
  Freigabe los; Shortcut „Plan ist freigegeben" = direkt los. **Lesen:** `CLAUDE.md` +
  `docs/goals/ziel6.md` + `docs/goals/backlog.md`. Einstieg `LEITSTAND.md`; Rollen/Tier/Modi:
  `docs/governance/operating_model.md`. **Subagent-Briefing:** Scope aus
  `docs/reference/agent_scopes.md` wählen (Pflicht-Lesen-Spalte → erlaubte Quellen im Brief).
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent (Opus). Asynchrone
  Stakeholder-Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#ablauforganisation-events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen. (Kandidat für SessionStart-Hook, O-Liste.)

---

## Aktueller Stand (nach S104, 2026-06-26)

**S104 — Org-/Reporting-Vorbereitung (O2 verankert + Pläne 027/028 angelegt).**
- **A (O2-MUST):** Tiering-Default Haiku in `CLAUDE.md` + `operating_model.md` geschärft
  (Abweichung nach oben nur mit Begründung im Auftrag); feedback-Memory existierte schon.
- **B:** Pläne **027** (Doku-Org/ADR-0007, O1) + **028** (Reporting/Kontext, O3–O7) + README-Queue.
- **Retro-Lehren (S104):** (1) Plan-Subagent ist READ-ONLY → gab vollen Plan-Text zurück
  (70k→126k-Sprung); Plan-Dateien künftig per Executor-SA **mit Write** (gibt nur Pfad zurück).
  (2) Live-Gauge (`session_context.py`) ist die verlässliche Kontextzahl, nicht die overview-Tabelle (O4).

**S103 — Plan 025 Step 4 (Eternal Guardian D1) + Bug-Fixes + Plan 026.**
- **Step 4 committed (`a060345`):** D1 `light_cover_if_stationary` (Klasse A) — Auto-Light-Cover
  im Shooting-SAVE-Block bei stationär (Variante C: Checkbox vorgehakt+disabled). D2-secondary als
  9E-Übergang (`hold_steady_or_set_to_defend`, `enforcement: table`); erfundenes `reroll_save_1` raus.
  Engine-Fn liest State layer-sicher via `units_key_for` (kein uiLayout-Import).
- **UI-Verifikation fand 2 Bugs → gefixt (UNCOMMITTED):** (1) Auto-Light-Cover floss nicht in die
  Würfel (Render-Reihenfolge: `auto_light_cover` jetzt VOR `resolve_save` in `light_cover` gefaltet);
  (2) Badge blau→grün (`design_colors.md §3`). Schema-Beispiel `round_choice.example.yaml` entdriftet.
  Vollsuite 1164 grün, 93,22 %, Arch-Gate 8.
- **Plan 026 angelegt:** `docs/audit/plans/026-eternal-guardian-d2-...md` (D2 Hold Steady/Set to
  Defend, abhängig Plan 015 Overwatch); README + Plan 015 mit Abhängigkeits-Vermerk.

**S102:** Gate-Fix (`docs/handoff/`-Exemption) + Mailbox-Pilot real. **S101:** ADR-0007 dünner Koordinator.

### Nächster Schritt — 025-Linie fort (027 ✅ + 028 ✅ DONE)
**Plan 027 DONE (S105, 2026-06-26):** Pilot-Vorbehalt gestrichen (operating_model + ADR-0007);
Diagramme A/B nachgezogen (Planner+Reviewer als Subagenten); next_session ADR-0007-Regeln;
agent_scopes Reporting/Token-Tooling + als Pflichtlektüre; CLAUDE.md ADR-0006-Verweis.
**Plan 028 DONE (S105, 2026-06-26):** O3 (135k-Schwelle), O4 (peak-Upsert), O5–O7 fertig.
Nächste Pläne: **025-Linie** (025 → 016 → 018 → 015 → 026 → 017). Executor-SA mit **Write**.

**Reliability-Vermerk:** Live-Gauge (`session_context.py`) = verlässliche Zahl; overview.md archiv-abgeleitet.
- **M1 — Befund Overwatch-Anzeige:** statische Caption `chargephase.py:144` („trifft auf 6+")
  ist erst mit Overwatch/Hold-Steady korrekt → in **Plan-015-Scope** aufnehmen (durch echtes Overwatch ersetzen).

### ⚠️ Carry-over (offen)
0. **ADR-0007 vollständig umgesetzt (O1 ✅).** Offen noch:
   (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen;
   (e) SessionStart-Regel-Injektion (S95-Beleg);
   (f) **M3:** Governance-Doku bis auf Zeilennummer indizieren (präzise Querverweise);
   (g) **M4:** diese Datei auf ≤70 Zeilen kürzen — Erledigtes (S103/S104-Detail) → `session_archive.md`.
1. **Plan 025** aktive Hauptlinie; Bug 3 (Zweitspieler-Direktiv-Wahl) + INV-4b-Restschuld nebenher.
2. **Manuelle UI-Verifikation (offen, PFLICHT):** (a) Mirror-Protokoll Necron-vs-Necron
   Befehlsphase; (b) Bug 5: Runde-2-Fernkampf-Zielwahl; (c) **S103 Bug-Fixes:** stationär+D1 →
   grünes +1-Save-Badge IN den Würfeln + Eff.-Save besser; Checkbox-Badge grün statt blau.

### Offene Fragen / Vormerke
- **Design-System-Crew:** Buff-/Direktiv-Hinweis-Komponente, sobald 025 Effekte festlegt.
- **S95-Prozess-Vormerk:** Regelkonformität beim YAML-Modellieren prüfen (DoD-#1-Ergänzung).
- **Kleine Doku-Vormerke:** backlog #2/ziel6 6e Bug-3-Step.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write`. **History:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
