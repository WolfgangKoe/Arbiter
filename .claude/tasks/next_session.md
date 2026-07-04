# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/archive/ziel6.md`
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

## Aktueller Stand (nach S120, 2026-07-04)

**S120 committed:** deckte auf, dass der Design-System-Konsens (Retro-Vorschlag) eine
**Wiedervorlage** war — Code seit S116–S118 längst fertig (Commits 143d848/3915f8c/29f4f81).
Umgesetzt: Doku-Drift-Fixes (design_system.md §1.1, backlog §4c geschlossen), neuer
Handoff-Hygiene-Wächter `tests/docs/test_handoff_hygiene.py` (STATUS-Marker-Pflicht,
DONE blockiert den Build), CLAUDE.md-Verankerungen (Thema ≠ Planning-Skip, Entscheidung ≠
Umsetzungs-Freigabe; DoD-7: Doku-Nachzug im selben Schritt sonst NO-GO), Handoff-Ordner
11→3 Dateien, `ziel6.md` nach `archive/` verschoben + Rotationsziel jetzt `session_archive.md`.
Review S120: **GO mit Auflagen** (A1 umgesetzt, A2 → M3 notiert, A3 → M4 umgesetzt).

Frühere Sessions (S60–S119): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt

Stufe A aus `docs/handoff/plan-ziel7-restruktur.md` (Marker ANSWERED, FREIGEGEBEN): Task 0
YAML-Drift (Counter-Offensive + Insane Bravery → `player: both`) → Task 1 Spieler-Spalten-Split
(`first_player` links/`second_player` rechts, Attribution aus Quell-Liste,
`stratagem_usable_by_player()`) → Task 2 `used_stratagem_ids` auf Dict-Form. Entscheidungen:
Design Option 1 (nur Sektions-Header), Dict-Form-Konvention, ziel7-§0-Block übernehmen,
(inactive)-Suffix nach Split entfernen. Danach Stufe B (Necrons), C (Orks), UX-Pass vor Ziel8.

**Merksatz S120:** Umsetzung ohne Haken + Doku-Nachzug = nicht fertig; „folgt der Empfehlung"
beantwortet nur die Entscheidungsfrage, ist keine Umsetzungs-Freigabe.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
