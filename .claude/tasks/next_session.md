# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planning vorlegen** (Prioritäten + Token-Schätzung), erst nach
  Freigabe los; Shortcut „Plan ist freigegeben" = direkt los. **Lesen:** `CLAUDE.md` +
  `docs/goals/ziel6.md` + `docs/goals/backlog.md`. Einstieg `LEITSTAND.md`; Rollen/Tier/Modi:
  `docs/governance/operating_model.md`.
- **Ende:** Review → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) → Abschluss: **diese
  Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.
- **⚠️ KOORDINATOR DELEGIERT MEHR (Retromaßnahme S102):** Detail-Sichtung, Planung, Implementierung
  UND Review laufen als Subagenten — der Koordinator routet, hält Gates, liest nur Marker/Pfade,
  nie Vollergebnisse. Entscheidungen gehören IN die Mailbox (`docs/handoff/`, NEEDS-DECISION →
  ANSWERED), NICHT in den Chat. S102-Lehre: Opus-Fenster lief auf ~112k, weil der Koordinator den
  Backlog selbst las und Entscheidungen im Chat ausgab statt über die Mailbox. Nicht selbst
  implementieren, wenn ein Executor-Subagent es kann.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).

---

## Aktueller Stand (nach S102, 2026-06-26)

**S102 — Gate-Fix + ADR-0007-Mailbox-Pilot real + D2-Neubewertung.**
- **Gate-Fix:** `tools/freigabe_gate.py` nimmt `docs/handoff/`-Writes aus dem Freigabe-Gate aus
  (ADR-0007-Mailbox ist Planungsartefakt, kein Code); +4 Regressionstests. Vollsuite grün (1158,
  93,20 %). Live-Hook verifiziert.
- **Mailbox-Pilot real:** Planner-Subagent (Sonnet) schrieb Detail-Planung für Plan 025 Step 4
  nach `docs/handoff/plan-025-step4.md`; Stakeholder antwortete IN der Datei (ANSWERED).
- **D2 neu bewertet:** Eternal Guardian D2 (Hold Steady/Set to Defend) ist kein reiner
  Tisch-Hinweis — Hold Steady = Overwatch 5+ statt 6; Set to Defend = +1 Hit next Fight. Hängt
  an Plan 015 (Overwatch nicht implementiert). **D2 herausgeschnitten**, eigener Plan.
- **4 Entscheidungen (A1/B1/B2/B3):** D1 nur im Shooting-Block (A1); D2 raus aus Step 4 (B1);
  D2-YAML als Übergang `hold_steady_or_set_to_defend` + TODO-Kommentar (B2); eigener D2-Plan
  deckt beide Hälften, abhängig Plan 015 (B3). Detail → `docs/handoff/plan-025-step4.md`.

**S101:** ADR-0007 + Mailbox-Pilot grün; dünner Koordinator, Planung/Review als Subagenten.
**S100:** Badge-Label-Bug gefixt. **S99:** Plan 025 Step 3 (Vengeful Stars) fertig.

### Nächster Schritt
**Plan 025 Step 4 = nur D1** (Eternal Guardian Light Cover bei stationär, Variante C,
nur Shooting-Block). Mailbox-Plan `docs/handoff/plan-025-step4.md` Teil A (D1) liegt bereit.
→ **Executor-Subagent** umsetzen lassen, nicht im Koordinator-Fenster.
D2 = eigener Plan (abhängig Plan 015 Overwatch). Reihenfolge: 025(Step 4→5→6) → 016 → 018 → 015 → 017.

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering — S101+S102 real adressiert (ADR-0007).** Dünner Koordinator,
   Mailbox-Pilot läuft (NEEDS-DECISION→ANSWERED verifiziert). **Neuer Befund S102:**
   Freigabe-Gate blockierte anfangs `docs/handoff/` → gefixt (Exemption). **Rest offen:**
   (a) `operating_model.md`-Diagramme A/B nachziehen; (b) „Pilot"-Vorbehalt nach echtem Einsatz
   streichen; (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen;
   (e) SessionStart-Regel-Injektion (S95-Beleg).
1. **Plan 025** aktive Hauptlinie (s. o.); Bug 3 (Zweitspieler-Direktiv-Wahl) + INV-4b-Restschuld laufen nebenher.
2. **Manuelle UI-Verifikation (offen, PFLICHT):** (a) Mirror-Protokoll Necron-vs-Necron
   Befehlsphase; (b) Bug 5: Runde-2-Fernkampf-Zielwahl.

### Offene Fragen / Vormerke
- **Design-System-Crew:** Buff-/Direktiv-Hinweis-Komponente, sobald 025 Effekte festlegt.
- **S95-Prozess-Vormerk:** Regelkonformität beim YAML-Modellieren prüfen (DoD-#1-Ergänzung).
- **Kleine Doku-Vormerke:** `CLAUDE.md` um ADR-0006-Verweis; backlog #2/ziel6 6e Bug-3-Step.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write`. **History:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
