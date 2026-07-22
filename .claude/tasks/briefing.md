# Koordinator-Briefing

<!-- Kanonisch: .claude/tasks/briefing.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Zweck: Koordinator-Briefing bei Session-Start + Kontext-Zwischenspeicher -->
<!-- über Kontextfenster-Grenzen hinweg. Regeln → CLAUDE.md/operating_model.md/agent_scopes.md. -->

## Was ist Arbiter?

Digitaler Spielbegleiter WH40k 9E, Streamlit (Python). Start: `streamlit run src/app.py`
(Port 8501; **venv:** `source .venv/bin/activate`). Branch `dev` (Arbeit), `main` (nur PR).

**Die App muss dauerhaft laufen** (Stakeholder-Anweisung S152): bei Session-Start prüfen
(`curl -s -o /dev/null -w "%{http_code}" http://localhost:8501` → 200) und andernfalls im
Hintergrund starten (`streamlit run src/app.py --server.headless true`) — nicht beenden.

---

## Session-Routine — nur Verweise

- **Workflow/Freigabe-Gates/Session-Ablauf:** `CLAUDE.md`
- **Rollen/Model-Tier/Events:** `docs/governance/operating_model.md`
- **Scopes + Brief-Pflichten je Aufgabentyp:** `docs/reference/agent_scopes.md`
- **Einstieg für den Stakeholder:** `LEITSTAND.md`
- **Retro-Maßnahmen-Entscheid am Session-Start:** docs/governance/operating_model.md Event 1 (§ev1)

---

## Aktueller Stand (nach S177, 2026-07-22)

**S177 committet — reine Governance-/Doku-Session (kein `src/`).** Drei Stakeholder-Punkte + offene S176-Maßnahmen:
- **Punkt 1 / ADR-0010:** Koordinator-Sitz = **Opus** (Fable nicht verfügbar). ADR-0010 angelegt, löst ADR-0008 Punkt 1 ab (0008 append-only mit Status-Verweis, Rest gültig); 6 Fable-Koordinator-Stellen in `operating_model.md` angeglichen. Planner-Tier/ADR-0009 unberührt.
- **Punkt 2:** Dauer-Ratchets **B-024 + B-124 aus dem Backlog aufgelöst** → neue Sektion `## Stehende Ratchet-Praktiken` in `operating_model.md` (Leitsatz „Laufende Ratchets sind Regeln, keine Backlog-Items"). Konkrete Rest-Facharbeit (a Warnhinweis kürzen / b Apply-Damage vereinheitlichen) → neues Item **B-128**. Prosa in `design_system.md` (5 Stellen) + `agent_scopes.md` umgebogen; Archiv-Nachzug „in stehende Regel überführt".
- **Punkt 3:** Neues 10. Feld **„Geltende Prozess-Regeln"** im `backlog_details.md`-Feldschema (Abgrenzung zu „Benötigte Regeln-Scopes" = Spielregeln); Backfill in B-113, B-028c3/c4/c5, B-128; Nachtrag-Ratchet als 3. Punkt der Ratchet-Sektion.
- **S176-Zusatz:** Planner/Reviewer Tool-Zugriff „Read + Write nur `docs/handoff/`" (`operating_model.md` + `agent_scopes.md`-Klausel — genau in dieser Session erstmals genutzt: der Reviewer schrieb `S177_review.md` selbst); M3a Pfad `src/gameState.py`→`src/gameMechanic/gameState.py` (B-028c4/c5); M3b B-116-Aussage korrigiert (`reroll_marker_row_html` unverdrahtet, 0 Call-Sites → B-113 Erstanwendung); M1 Marker-Liste vervollständigt; M2 Planner-Rangfolge-Klausel (backlog.md-Rangfolge maßgeblich, briefing-Hint nachrangig).

Review S177: **GO** — Vollsuite **2151 passed, Coverage 99,20 %, Architektur grün**; keine toten B-124/B-024-Verweise, keine Widersprüche.

**Retro-Maßnahmen S177 (zur Sichtung/Entscheid durch Stakeholder, `docs/handoff/S177_retro.md`):** R1 Subagent-Ausfall-Wiederaufnahme, R2 Parallel-Split-Muster, R3 „In Progress/laufend"-Wildwuchs (B-007) prüfen.

Frühere Sessions (S60–S176): Verlauf in `docs/metrics/session_archive.md`.

### ▶ Nächster Schritt (S178)

1. **B-113 — Reroll-Fähigkeiten verdrahten** (Discovery-Ergebnis S176; DoR jetzt reifer durch neues Prozess-Regel-Feld + M3b-Korrektur): Skorpekh-Destroyer-Hit-Reroll (`reroll_hit`, `subfaction_abilities.yaml:150`) + beide DESTROYER-CULT-Lords (Lokhust + Skorpekh Lord) Wound-Reroll (`reroll_wound_1`, Aura). **Kernbefund:** `reroll_hit`/`reroll_wound_1` engine-seitig unkonsumiert, `reroll_marker_row_html` 0 Call-Sites → Erstanwendung. Split: (a) Skorpekh-Hit + generischer Reroll-Konsument, (b) Lord-Aura. Beide M → je eigener Teil-Brief.
2. **B-128 — UI-Facharbeit (neu):** (a) Warnhinweis im Subgruppen-Selector kürzen, (b) Apply-Damage-Bereich vereinheitlichen. Scopes: `design_system.md` §1.4/§3.1. Render-Code → manuelle UI-Verifikation.
3. **B-028c3/c4/c5** (backlog.md Rang folgend) — Regel-Scope („Benötigte Regeln-Scopes") vor Umsetzung befüllen; „Geltende Prozess-Regeln" bereits backgefüllt.
4. **B-005 Direktiv-Lock-Rest** — nachrangig, DoR-Regel-Scope noch leer.

**Offene Handoff-Marker:** `Stakeholder_Beobachtungen.md` (STANDING).

---

## Gate-Netz (Messbefehle)

- Tests + Coverage: `pytest --tb=short` (Floor **99 %**); Architektur:
  `pytest tests/architecture/ --no-cov -q`; Doku/Akzeptanz:
  `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Token-Korridor** <150k, ab ~120k Wind-down, spätestens ~135k beenden; ab ~100k nichts
  Neues bei ausstehendem Review.
- **Abschluss-PFLICHT:** `python tools/token_report.py --write` +
  `python tools/rotate_history.py --session <N> --summary "…"`.
- **Freigabe-Gate:** Edit/Write blockiert bis `touch .claude/.freigabe`; SessionStart re-armt
  (Ausnahmen: `docs/handoff/`, außerhalb Repo).
