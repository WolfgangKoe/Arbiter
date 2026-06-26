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
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen. (Kandidat für SessionStart-Hook, O-Liste.)

---

## Aktueller Stand (nach S103, 2026-06-26)

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

### Nächster Schritt — Organisations- & Reporting-Umbau (delegiert, simplizistisch)
Stakeholder-Anliegen S103, geklärte Entscheidungen unten. **Zwei Pläne anlegen** (Planner-Subagent):
ein **Doku-Org**-Schritt + ein **Reporting**-Plan. Danach Plan-025-Linie fort (Reihenfolge:
025 Step 4 ✅ → 5 → 6 → 016 → 018 → 015 → 026 → 017).

**Geklärte Entscheidungen (S103):**
- **O1 Doku-Alignment:** `next_session`/`CLAUDE.md`/`operating_model.md` vollständig auf neue
  Arbeitsweise (ADR-0007 dünner Koordinator) bringen; `docs/reference/agent_scopes.md` einbinden.
  Querverweise über **stabile Abschnitts-Anker — KEINE Zeilennummern** (driften).
- **O2 Modellwahl-MUST (sofort befolgen):** reine Lookups/format-fixe Tasks → **Default Haiku**;
  Abweichung nach oben (Sonnet/Opus) nur mit **expliziter Begründung im Auftrag**. In `CLAUDE.md`
  + `operating_model.md` + feedback-Memory verankern. (User sieht kaum Haiku — Tiering wird ignoriert.)
- **O3 ⚠️-Schwelle:** Kontext-Warnung erst **>135k** (nicht 120k) — `tools/session_context.py`.
- **O4 Report-Überschreib-BUG:** User bekam korrekten Stand, danach mit **Altdaten überschrieben**
  (falsch) — `tools/token_report.py`/`overview.md`-Pipeline. Wurzel finden+fixen. User will eher
  **MEHR/Echtzeit**-Updates (bei Subagent-Start/-Ende), nicht weniger.
- **O5 Modellmix:** **Koordinator (Opus-Hauptthread) raus** aus dem „Modellmix" — nur Subagenten.
- **O6 Neue Kontext-Sicht:** „womit ist MEIN Fenster gefüllt" — Aufschlüsselung **nach Quelle**
  (Datei-Reads / Tool-Ausgaben / Subagent-Reports / System+Memory / Konversation). An die
  **Peter-Wegner-Präsentation** (im Repo — finden+lesen via Subagent) ausrichten.
- **O7 Bessere Planning-Darstellung:** Planning bleibt an Subagent delegiert, aber die Präsentation
  muss klarer/lesbarer werden.
- **Befund Overwatch-Anzeige:** „trifft auf 6+" ist falsch, sobald Hold Steady (5+) greift →
  gehört zu Plan 026/015; bei den GO-Hinweisen vermerken.

### ⚠️ Carry-over (offen)
0. **Kontext-Engineering — S101+S102 real adressiert (ADR-0007).** Dünner Koordinator,
   Mailbox-Pilot läuft (NEEDS-DECISION→ANSWERED verifiziert). **Neuer Befund S102:**
   Freigabe-Gate blockierte anfangs `docs/handoff/` → gefixt (Exemption). **Rest offen:**
   (a) `operating_model.md`-Diagramme A/B nachziehen; (b) „Pilot"-Vorbehalt nach echtem Einsatz
   streichen; (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen;
   (e) SessionStart-Regel-Injektion (S95-Beleg).
1. **Plan 025** aktive Hauptlinie (s. o.); Bug 3 (Zweitspieler-Direktiv-Wahl) + INV-4b-Restschuld laufen nebenher.
2. **Manuelle UI-Verifikation (offen, PFLICHT):** (a) Mirror-Protokoll Necron-vs-Necron
   Befehlsphase; (b) Bug 5: Runde-2-Fernkampf-Zielwahl; (c) **S103 Bug-Fixes:** stationär+D1 →
   grünes +1-Save-Badge IN den Würfeln + Eff.-Save besser; Checkbox-Badge grün statt blau.

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
