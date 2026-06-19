# Startprompt — Nächste Session
<!-- Kanonisch: .claude/tasks/next_session.md — nie ins Root-Verzeichnis anlegen. -->
<!-- Nur „Stand + nächster Schritt + offene Fragen". Historie → ziel6.md; Backlog → backlog.md. -->
<!-- Referenzwissen NICHT hier: Architektur-Muster → architecture.md, Regel-Gotchas →
     rules_insights.md, Constraints → CLAUDE.md. -->

## ⚠️ Session-Regeln
- **Start lesen:** `CLAUDE.md` (Freigabe-Pflicht, bei Unklarheit zuerst fragen)
  + `docs/goals/ziel6.md` (Aufgaben/Historie) + `docs/goals/backlog.md` (Backlog).
  Einstieg: `LEITSTAND.md`; Rollen/Tier/Events/Modi: `docs/governance/operating_model.md`.
- **Ende:** Checkboxen in `ziel6.md` + Historien-Zeile; **diese Datei** aktualisieren
  (ZUERST lesen, dann ergänzen — nie blind überschreiben).
- **Doku-Gate:** Decke **120** Zeilen (Test rot darüber). Beim Reißen **tief auf ≤ 70**
  kürzen, nicht knapp drunter — Erledigtes → `backlog.md`/`ziel6.md`, Referenz → s. o.
- **Freigabe vor Umsetzung; kein Memory/Subagent/Skill ohne Freigabe; rote vorher-grüne
  Tests = STOP + fragen.** Details: `CLAUDE.md`.

## Was ist Arbiter?
Digitaler Spielbegleiter für WH40k 9E, Streamlit (Python). Start:
`streamlit run src/app.py` (Port 8501). Branch `dev` (Arbeit), `main` (nur per PR).

---

## Aktueller Stand (nach S61, 2026-06-19)

**S61 — Session-Hygiene maschinell verankert.** (a) Token-Report-Hook in `settings.json`:
bei `pytest` läuft `python tools/token_report.py --write` mit → `overview.md` ist beim
Session-Abschluss frisch ([[feedback_session_close_routine]] jetzt erzwungen). (b) next_session-
Gate auf **Hysterese** umgestellt: Decke 120 / Trim-Ziel 70 (`test_doc_health.py`,
`conftest.py`) — kein Schwellen-Geklingel mehr. (c) Doku-Schulden reduziert: Referenz aus
next_session in kanonische Häuser geroutet — Architektur-Muster → `architecture.md`,
Regel-Gotchas → neue `docs/spec/rules_insights.md`, Domänen-Constraints → `CLAUDE.md`.

**S60 — Regel-Katalog: Charge + Morale.** `R-CHARGE-01..13` + `R-MORALE-01..13` in `rules.md`,
Nenner **87**. Scoreboard A 28/58 · B 0/19 · C 8/10. Ledger 10. Befund R-COMBAT-32 (impl.+
getestet, aber `offen` markiert → backlog §0). Details: `ziel6.md` / `backlog.md`.

Frühere Sessions (S52–S59): Verlauf in `docs/goals/ziel6.md`.

### ▶ Nächster Schritt — frei wählbar (je eigene Freigabe)
1. **Regel-Katalog weiter:** Movement/Charge/Morale ✅; nächster Bereich **Psychic Phase**
   (Sonnet-Subagent, eigene Session).
2. **Ledger schrumpfen** (jetzt 10) — Ratchet. Plus **R-COMBAT-32** als impl.+getestet
   nachziehen (Doku-Drift, backlog §0).
3. **Gates leser-orientiert prüfen (ADR-0002):** Debt-Scoreboard + Katalog-% gegen
   Stakeholder-Fragen durchsehen (backlog §2).
4. **INV-4b/INV-4 Ledger schrumpfen:** benannte Tokens/Allowlist aus `src/` in YAML ziehen.
5. **Operating-Model Phase C:** Refinement automatisieren (`Fotos/` → `docs/inbox/`, backlog §2).

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 88 %, `pyproject.toml`).
- **Schulden-Scoreboard** erscheint nach jedem `pytest` (`tests/conftest.py`): Vokabular-
  Tokens, Allowlist, AC-IDs, next_session-Zeilen, Regel-Katalog-%. Ziel: Zahlen sinken.
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q` · Ledger:
  `architecture_invariants.md`. Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Regel-Katalog** (Nenner): `docs/spec/acceptance/rules.md` — Klasse A/B/C,
  `getestet: ja — <testname>`. Parser: `tests/acceptance/_rules.py`. Noch kein hart-roter Gate.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit an Sonnet-Subagent.
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`
  (läuft jetzt automatisch bei `pytest`).
