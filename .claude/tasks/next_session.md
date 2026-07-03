# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → session_archive.md; Backlog → backlog.md. -->
<!-- Referenz NICHT hier: Architektur → architecture.md, Regel-Gotchas → rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start „start next session" → Planner-Subagent beauftragen** (liest `CLAUDE.md` + `docs/goals/ziel6.md`
  + `docs/goals/backlog.md`, Scope aus `docs/reference/agent_scopes.md`); Entwurf als Datei, Koordinator
  legt vor, erst nach Freigabe los. Shortcut „Plan ist freigegeben" = direkt los. Einstieg `LEITSTAND.md`;
  Rollen/Tier/Modi: `docs/governance/operating_model.md`.
- **ADR-0007 (verbindlich seit S102):** Koordinator routet — liest keine Quelldateien/Vollergebnisse;
  Detail-Planung → Planner-Subagent; finales Review → Reviewer-Subagent. Asynchrone Stakeholder-
  Entscheidungen über Mailbox (`docs/handoff/`, NEEDS-DECISION → ANSWERED), nicht Chat.
  Details: `docs/governance/operating_model.md` [#events].
- **Ende:** Review (Reviewer-SA) → Retro → **Maßnahmen-Entscheid** (Stakeholder wählt) →
  Abschluss: **diese Datei** aktualisieren (ZUERST lesen, dann ergänzen) + ggf. ziel6-Checkboxen.
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70** kürzen —
  Erledigtes → `backlog.md`/`session_archive.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Skill(datei-ändernd) ohne Freigabe; Subagenten =
  stehende Freigabe (proaktiv, ADR-0005); rote vorher-grüne Tests = STOP + fragen.** → `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `feature/016` (Arbeit), `main` (nur PR).
**App permanent laufen lassen:** bei Session-Start nur kurz prüfen (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200), nur bei Bedarf neu starten — nicht den Nutzer fragen.

---

## Aktueller Stand (nach S119, 2026-07-03)

**S119 committed** (Review GO uneingeschränkt, 1405 passed, 99,11 %, Arch-Gate 8/8;
`docs/handoff/review-S119.md`): Ziel7-Cluster gefixt — P21 Undo phase-scoped (dde16f3), P19
per-Spieler-Tracking (1f9d82b), P20 Rapid-Fire-Cap verdoppelt (dfebd27); Ziel6 GESCHLOSSEN/
archiviert (b3ebfd5). UI-Verifikation vollständig bestätigt inkl. S113-Carry-over
(Mirror-Befehlsphase, +1-Save-Badge) — Carry-over-Block damit leer, entfernt.
Live-Test-Befunde S119 (`backlog.md` §5): Stratagem-Doppelanzeige, Attributions-Bug
(`spending_faction` aus `s.player` statt Quell-Liste), globales phase-Set.

Frühere Sessions (S60–S118): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt

Stufe A aus `docs/handoff/plan-ziel7-restruktur.md` (Marker ANSWERED, FREIGEGEBEN): Task 0
YAML-Drift (Counter-Offensive + Insane Bravery → `player: both`) → Task 1 Spieler-Spalten-Split
(`first_player` links/`second_player` rechts, Attribution aus Quell-Liste,
`stratagem_usable_by_player()`) → Task 2 `used_stratagem_ids` auf Dict-Form. Entscheidungen:
Design Option 1 (nur Sektions-Header), Dict-Form-Konvention, ziel7-§0-Block übernehmen,
(inactive)-Suffix nach Split entfernen. Danach Stufe B (Necrons), C (Orks), UX-Pass vor Ziel8.

**Merksatz S119:** Per-Spieler-State nie über Fraktions-/Anzeigenamen keyen —
Player-Slot-Muster (`round_choice_state_key`); P19-Mirror-Lücke wird durch S120-Umbau geschlossen.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
