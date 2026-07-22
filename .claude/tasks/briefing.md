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

## Aktueller Stand (nach S178, 2026-07-22)

**S178 committet — B-113 „Reroll-Fähigkeiten verdrahten" (Teil A+B).** Erstanwendung von
`reroll_marker_row_html`. A: generischer Hit-Reroll-Konsument (`unit_hit_reroll_ones`) + HIT-Marker,
Skorpekh-Destroyer „Hardwired for Destruction" (`reroll_hit`/self). B: generischer Aura-Wound-Reroll
(`unit_wound_reroll_ones` + `_aura_source_alive`) + WOUND-Marker, Destroyer-Lord-Aura „United in
Destruction" (`reroll_wound_1`); Distanz nicht gemessen (konsistent `within_inches`-No-op);
Roster-Prep Skorpekh Lord in `necrons_test.yaml`. Fraktionsneutral (INV-4b unverändert), Suite
**2176/99,17 %**, Architektur grün. **UI-Verifikation POSITIV** (`docs/handoff/S178_B113_ui_verifikation.md`).
Reviewer GO nach DoD-7-Doku-Nachzug. Bereinigt: S177-Alt-Last `S177_review.md` gelöscht (roter Hygiene-Test).
**Offen S178 → `docs/handoff/S178_retro.md` (NEEDS-DECISION):** 3 UI-Folge-Befunde + Prozessmaßnahmen +
Backlog-Admin (B-113 archivieren, B-129/130/131 anlegen).

Frühere Sessions (S60–S177): Verlauf in `docs/metrics/session_archive.md` (Session-Historie).

### ▶ Nächster Schritt (S179)

1. **S178-Abschluss nachziehen** (`docs/handoff/S178_retro.md`, NEEDS-DECISION): B-113 formal
   archivieren (Detail-Abschnitt → `backlog_archive.md`, Zeile in `backlog.md` löschen);
   3 UI-Folge-Befunde als **B-129/130/131** aufnehmen (Lord-Hit-Reroll · Reroll-Marker Buff→Grün ·
   Aura-Reichweiten-Hinweis); Prozess-Entscheide (»start session«-Regel verankern, S177-Hygiene-Miss,
   UI-Verifikations-Persistenz); je 1 `rules.md`-Katalogzeile für die 2 Reroll-Regeln.
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
