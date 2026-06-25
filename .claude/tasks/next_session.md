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

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).

---

## Aktueller Stand (nach S96, 2026-06-25)

**S96 — Plan 025 Step 1 erledigt (Command Protocols → 9E).** Sudden Storm D2 vom erfundenen
`advance_and_charge` auf die echte 9E-D2 (`shoot_during_action`, reiner B-Hinweis) korrigiert;
Undying-Legions Primary/Secondary **getauscht** → jetzt alle 6 Protokolle einheitlich **Primary =
9E-Direktive 1**. Nur Daten + Docstring + 8 Test-Migrationen, **keine** Engine-Logik (Reader sind
effekt-typ-basiert). 1135 grün / 93,11 %; UI verifiziert (Direktiv-Texte + Button-Reihenfolge ok).
**Zwei neue Befunde (backlog §2):** (1) Dynastie-Affinität „beide Direktiven" greift nur beim 6./
permanenten, **nicht** beim rundenzugewiesenen Protokoll — Engine+UI-Gap; (2) Sudden-Storm-B-Hinweis
braucht noch Render-Anzeige (im Zuge der Sudden-Storm-Anzeige einbauen).

**Vorher (S95):** Regeldrift gefunden + Entscheid (b) → Plan 025 angelegt (je Protokoll ein Step,
A/B-Effekt-Klassen). 016 Group A + Conquering-Tyrant-P-Morale werden durch 025 obsolet. Detail →
`session_archive.md` / git.

### Nächster Schritt
**Plan 025 Step 2 — Hungry Void (A-Effekte):** D1 `ap_on_unmod_wound_6` (melee), D2
`strength_if_charged` (Bedingung charged/charge/HI). Neue Engine-Typen + combat + Tests, eigener
Freigabe-Punkt + Vollsuite. Reihenfolge gesamt: 025(Rest) → 016(Rest) → 018 → 015 → 017.

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering / Regel-Kuratierung (eigene Session, Maßnahme C).** Quelle:
   `docs/reference/context-engineering-slides.md`. (a) SessionStart-Regel-Injektion (relevante Regeln je
   Ziel verbatim in den Kontext) — behebt Tiering-/Regel-Lücken. (b) Subagent-Ergebnis → `docs/handoff/`-
   Datei statt in Orchestrator-Kontext. (c) Handoff-Lebenszyklus (lesen→arbeiten→auslagern→löschen).
   (d) governance-Doc `context_engineering.md`; `docs/handoff/context-audit-S91.md` verarbeiten + löschen.
   **S95-Beleg (warum Kern):** Die Regelprüfung griff nur, weil sie *expliziter Plan-Schritt* war — nicht
   aus zuverlässiger Gewohnheit. Assurance braucht **Injektion oder Gate**, nicht „zufällig im Kontext".
1. **Plan 025** = aktive Hauptlinie (s. o.). Bug 3 (Zweitspieler-Direktiv-Wahl, armyCard.py:296/307) +
   INV-4b-Restschuld (`dynasty`/`gloom`/`prism`/`necrons`-Defaults) laufen nebenher, je eigene Freigabe.
2. **Manuelle UI-Verifikation (offen, PFLICHT, Render-Code):** (a) S91 Mirror-Protokoll — Necron-vs-Necron
   Befehlsphase: Spieler-1-Wahl lässt Spieler-2-Karte unverändert. (b) Bug 5: Runde-2-Fernkampf-Zielwahl.
   (Eternal-Guardian-Save / Undying-Legions-RP / Living-Metal-S waren S93 ✅.)

### Offene Fragen / Vormerke
- **Design-System-Crew (eigene Session):** Subagenten-Gespann Designsystem + Buff-/Direktiv-Hinweis-
  Komponente (RP-Hint deutlicher, konsistent mit MWBD/SAVE). Greift, sobald 025 die Effekte festlegt.
- **S95-Prozess-Vormerk (nicht entschieden):** Regelkonformität evtl. schon **beim YAML-Modellieren**
  prüfen, nicht erst bei Anzeige — als DoD-#1-Ergänzung erwägen.
- **Lehren:** „Engine oder Verdrahtung?" → erst prüfen, welche State-Klassen der Resolver liest (S93);
  Repro-zuerst (S92); Branch-Check (aktiv = `feature/016`).
- **Kleine Doku-Vormerke:** backlog #2 / ziel6 6e um Bug-3-Step + „Reset kampfrunden-weit" (S90);
  Freigabe-Gate Re-Arm nur bei echtem SessionStart prüfen; `CLAUDE.md` um ADR-0006-Verweis ergänzen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 90 %, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write`. **History:** `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
