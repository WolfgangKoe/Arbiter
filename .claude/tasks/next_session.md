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

## Aktueller Stand (nach S62, 2026-06-19)

**S62 — Doku-Drift R-COMBAT-32 geschlossen + Hook scharf bestätigt.** (a) Token-Report-Hook
empirisch verifiziert: `pytest`-Kommando ohne eigenen Schreibzugriff ließ `overview.md` neu
schreiben → Hook feuert (im `/hooks`-Menü gibt es **keinen** „scharf"-Knopf; Beweis = Auslösen).
(b) R-COMBAT-32 („Charging Units Fight First"): Verifikation ergab, dass nur die *Berechtigung*
getestet war, der *Reihenfolge*-Zweig (`can_fight_now`/`_any_charged_remain`) ungedeckt →
Regressionstest `test_non_charged_waits_while_charged_pending` ergänzt, dann Katalog auf
`implementiert`/`getestet: ja`/`code: fightPhase.py:can_fight_now`. A-Abdeckung 28→29 (50 %).
(c) **Regel-Katalog: Psychic Phase** `R-PSYCHIC-01..24` (Sonnet erfasst, Opus reviewt gegen
`psychicPhase.py`). Nenner 87→111; Ledger 10→15 (5 Render-Schuld R-PSYCHIC-11/16/17/18/22).
Review-Fix: R-PSYCHIC-23 `offen` (App revidiert `manifested` nach Perils nicht).

**S61 — Session-Hygiene maschinell verankert.** Token-Report-Hook in `settings.json` (bei
`pytest` läuft `token_report.py --write`); next_session-Gate auf **Hysterese** (Decke 120 /
Trim-Ziel 70); Doku-Schulden geroutet (Architektur → `architecture.md`, Regel-Gotchas →
`docs/spec/rules_insights.md`, Constraints → `CLAUDE.md`).

**S60 — Regel-Katalog: Charge + Morale.** `R-CHARGE-01..13` + `R-MORALE-01..13` in `rules.md`,
Nenner **87**. Scoreboard A 28/58 · B 0/19 · C 8/10. Ledger 10. Befund R-COMBAT-32 (impl.+
getestet, aber `offen` markiert → backlog §0). Details: `ziel6.md` / `backlog.md`.

Frühere Sessions (S52–S59): Verlauf in `docs/goals/ziel6.md`.

### ▶ Nächster Schritt — frei wählbar (je eigene Freigabe)
1. **Regel-Katalog weiter:** Movement/Charge/Morale/Psychic ✅; nächster Bereich offen
   (z. B. Deployment / Mission-Scoring / Battle-Round-Struktur — Sonnet-Subagent, eigene Session).
2. **Ledger schrumpfen** (jetzt 15) — Ratchet: R-COMBAT-09/17, R-CMD-03/04/10/11/12,
   R-CHARGE-09/10, R-MORALE-02 + R-PSYCHIC-11/16/17/18/22. Die Psychic-Schuld ist Smite-Manifest-
   Logik im Render-Code → in reine Funktionen ziehen + testen (backlog §0/§2).
3. **Gates leser-orientiert prüfen (ADR-0002):** Debt-Scoreboard + Katalog-% gegen
   Stakeholder-Fragen durchsehen (backlog §2).
4. **INV-4b/INV-4 Ledger schrumpfen:** benannte Tokens/Allowlist aus `src/` in YAML ziehen.
5. **Operating-Model Phase C:** Refinement automatisieren (`Fotos/` → `docs/inbox/`, backlog §2).
6. **Permission-Prompts reduzieren (Nutzerwunsch S62):** read-only-Bash-Muster (z. B. die
   `find`/`python3`-Lesebefehle für `*.meta.json` + Subagent-`*.jsonl` der Token-Messung) in
   `.claude/settings.json` `permissions.allow` aufnehmen — am besten via Skill
   `/fewer-permission-prompts` (scannt Transcripts, schlägt Allowlist vor). Ziel: freigegebene
   Pläne nicht durch wiederholte Read-only-Bestätigungen blockieren. Nur Lesen/Inspektion
   allowlisten, nichts Schreibendes/Löschendes.

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
