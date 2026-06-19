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

## Aktueller Stand (nach S64, 2026-06-19)

**S64 — Token-Mess-Reads prompt-frei (Punkt 0 erledigt).** `python3`-Reads aus der
Token-Messung verbannt (würde sonst Arbitrary-Code allowlisten). **jq ist auf dem System
nicht installiert** → `grep`/`tail` statt jq. Kanonik jetzt in `CLAUDE.md` („Messen:"):
Live-Kontext = `grep -o '"usage":{[^}]*}' <transcript> | tail -1`, dann
`input_tokens + cache_creation_input_tokens + cache_read_input_tokens` summieren (Hauptfile
hat 0 sidechain-Zeilen → `tail -1` = letzter Haupt-Chain-Eintrag). Peak/Subagent-Anteil/
Verlauf liest man aus `docs/metrics/overview.md` (pytest-Hook schreibt sie bei jedem Lauf) —
nicht neu aus Transcripts rechnen. Verifiziert prompt-frei. Tests: 876 grün, Cov 88.45 %.

**S64 — Psychic-Render-Schuld getestet (Punkt 2, Ledger 15→10).** Fünf regeltragende
Berechnungen aus den `_render_*`-Funktionen in `psychicPhase.py` in reine, getestete Helfer
gezogen (verhaltenserhaltend): `smite_warp_charge` (R-PSYCHIC-17/18), `is_manifested`
(R-PSYCHIC-11), `perils_pending` (R-PSYCHIC-22), `faction_deny_used`/`can_attempt_deny`
(R-PSYCHIC-16). +16 Tests (892 grün), A-Abdeckung 38→43 (55 %). UI verhaltenserhaltend →
manuell zu prüfen (Smite/Perils/Deny rendern unverändert).

**S63 — Permission-Prompts reduziert (Punkt 6 erledigt).** Transcript-Scan (50 jüngste
Sessions, `/fewer-permission-prompts`): Die häufigsten Read-Befehle (`grep`/`sed`/`find`/`ls`/
`git diff/status/log` …) sind **auto-erlaubt** → prompten ohnehin nicht; `pytest`/`streamlit`
stehen schon in der Allowlist. Einzige sichere Ergänzung: `Bash(ruff check *)` in
`.claude/settings.json`.

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
2. **Ledger schrumpfen** (jetzt 10) — Ratchet: R-COMBAT-09/17, R-CMD-03/04/10/11/12,
   R-CHARGE-09/10, R-MORALE-02. Psychic-Schuld erledigt (S64). Verbleibende sind v. a.
   Command/Combat-Render-Logik → gleiches Muster (reine Funktion + Test, backlog §0/§2).
3. **Gates leser-orientiert prüfen (ADR-0002):** Debt-Scoreboard + Katalog-% gegen
   Stakeholder-Fragen durchsehen (backlog §2).
4. **INV-4b/INV-4 Ledger schrumpfen:** benannte Tokens/Allowlist aus `src/` in YAML ziehen.
5. **Operating-Model Phase C:** Refinement automatisieren (`Fotos/` → `docs/inbox/`, backlog §2).
6. ✅ **Permission-Prompts reduziert (S63):** `Bash(ruff check *)` allowlistet, Rest war schon
   auto-erlaubt. ✅ **Token-Mess-Reads prompt-frei (S64):** `grep`/`tail` + `overview.md` statt
   `python3` — Kanonik in `CLAUDE.md`.

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
