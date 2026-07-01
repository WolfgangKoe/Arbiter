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

## Aktueller Stand (nach S115, 2026-07-01)

**S115** abgeschlossen — reine Doku-/Status-Session:
- **(a)** Retro-Maßnahmen S114 in Prozess-Docs verankert (Commit `c5fe153`).
- **(b)** P17-Scope entschieden → Vor-Auswahl+Lock akzeptiert = **P17 erledigt** (ziel6 abgehakt):
  Pre-Apply-Zielauswahl (`_render_subgroup_selector`, `_common.py`) + Wounded-Lock
  (`apply_damage`/`get_locked_group`, `unit_mutations.py`); ±-Zähler-Ansatz verworfen.
- **(c)** Plan 031 als bereits erledigt bestätigt (`533e313`) + README-Status nachgezogen.
- **(d)** Zwei neue Retro-Maßnahmen verankert (`docs/reference/agent_scopes.md`): Plan-Status
  im selben Commit; Mechanik- statt Binär-Status im Backlog.
- Vollsuite: **1371 passed, Coverage 99.10 %**, Architektur 8/8.

### ▶ Nächster Schritt — Ziel7-Cluster

**0. Design-System Schritt 1** [offen, ~35–45k, Sonnet; Gate: Token-Werte + Hinweis-Konvention
   erst bestätigen] (Design-System-Crew, operating_model.md:95):
   - `docs/spec/design_system.md` anlegen + `design_colors.md` konsolidieren (alles an einem Platz).
   - Badge vereinheitlichen: `_common._badge` + `unitCard._badge` + `armyCard.py` + Invuln-Block (`dice_html.py:188-204`).
   - Zentrale Symbol-Konstanten anlegen (▶◀✓✕＋⚔↺).
   - Token-Wertesatz (Radius/Padding/Font-Size je Badge-Klasse) + Hinweis-Konvention
     (info/warning/success/error) vorschlagen + vom User bestätigen lassen.
   - Entscheidungsgrundlage: `docs/handoff/design-system-proposal.md` (ANSWERED, S114).

**1. P18** [~25k, Sonnet]: Einheitlicher Deklarations-Flow + Untergruppen-Ziel-Anzeige in
   PlayerArea; manuelle UI-Verifikation Pflicht.

**2. Regel-Ledger auf 0**: Tests für `R-COMBAT-17` und `R-PROTO-02` nachziehen (impl. ohne Test).

### ⚠️ Carry-over (offen)

- **Manuelle UI-Verifikation (PFLICHT, im Ziel7-UI-Pass):** once_per_battle-Undo/Label-Pfade
  (Stratagem-Phase, Spielerwechsel); Mirror-Protokoll Necron-vs-Necron Befehlsphase; stationär+D1
  grünes +1-Save-Badge in den Würfeln. Checkliste: `docs/handoff/review-S113.md`.
- **ADR-0007-Reste:** (c) `docs/handoff/context-audit-S91.md` verarbeiten + löschen; (e) SessionStart-Regel-Injektion.
- **Retro-Maßnahmen (S110):** (1) DRY-Helper Hit/Wound ±1-Cap in `dice_html.py`; (2) st-Mock-Fixture.
- **Plan-029-Datei fehlt** (in README.md als Divergenz markiert) — vor Beauftragung anlegen oder REJECTED.

Frühere Sessions (S60–S114): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor **99 %**, `pyproject.toml`); **Schulden-Scoreboard** danach.
- Architektur: `pytest tests/architecture/ --no-cov -q`. Doku/Akzeptanz: `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, bei ~135k beenden; Fleißarbeit PROAKTIV an Sonnet-Subagent.
- **Token-Report + History (M4, PFLICHT beim Abschluss):** `python tools/token_report.py --write` + `python tools/rotate_history.py --session <N> --summary "…"` — Koordinator stößt an.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt.
