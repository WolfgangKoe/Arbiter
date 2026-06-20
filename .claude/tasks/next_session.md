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

## Aktueller Stand (nach S69, 2026-06-20)

**S69 — Prozess festgehalten + Ledger ehrlich geschrumpft.** (1) **ADR-0004**: Skill-/Claude-
Inhalte über die API nur per Subagent ziehen (direktes Laden kostete ~300k Token) — CLAUDE.md
(Token-Disziplin) + ADR + Memory. (2) **History-Rotation-Tool** `tools/rotate_history.py` (+Test):
hängt Stand-Einzeiler an `ziel6.md`, setzt Stand-Block hier zurück — am Ende dieser Session
selbst dogfood-genutzt. (3) **Ledger 10 → 8** via Sonnet-Subagent (34 % Token-Anteil, isoliert):
R-CMD-04 + R-CMD-12 ehrlich getestet. **Opus-Review fand zwei Katalog-Fehler:** R-COMBAT-09-Logik
liegt in `ability_engine.py:ability_invuln_save` (nicht `resolve_save`) → code-Ref korrigiert,
Test noch offen; R-COMBAT-17 rechnet die App gar nicht (nur Hinweis-Caption) → auf **Klasse C**
reklassifiziert. Vertragstests des Subagenten (resolve_save/_compute_attacks) bleiben als
Extra-Coverage. **R-CMD-03 Befund** (deine Frage c): CP-Grant-Button ist ungated — `game_mode`/
Battle-forged wird nicht geprüft; risikoarmer Bug (alle Rosters battle-forged), Fix = 1-Zeilen-
Guard, offen. **952 grün, Cov 91.88 %**, Nenner=121, Ledger=8.

Frühere Sessions (S60–S68): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — frei wählbar (je eigene Freigabe)
1. **ZUERST: R-COMBAT-09-Test** auf `ability_engine.py:ability_invuln_save` (zwei aktive Invuln-
   Effekte → kleinerer gewinnt) → dann `getestet: ja` setzen. Ledger 8 → 7. Schnell, fachlich.
2. **R-CMD-03-Fix klären + umsetzen** (Frage c offen): 1-Zeilen-Guard `game_mode == "matched"` vor
   CP-Grant in `commandPhase.py`; Render → Logik in testbaren Helfer ziehen + Test. Eigene Freigabe.
3. **Render-Ledger (Klasse 2)** in kleinen Extract-Refactors: R-CMD-10/11 (commandPhase),
   R-CHARGE-09/10 (chargephase), R-MORALE-02 (moralePhase) — je Phase-Datei, Logik raus + Test.
3b. **Output↔Ziel-Fortschritt-Zeile** im Review verankern (`operating_model.md` Event 5): knappe
   „Ziel-Fortschritt: ja/teils/nein, woran sichtbar" — Soll-Ist ohne Token-Zielzahl.
4b. **Regel-Katalog weiter:** nächster Bereich offen (Deployment / Mission-Scoring — Sonnet-Subagent).
3. **Gates leser-orientiert prüfen (ADR-0002):** Debt-Scoreboard + Katalog-% gegen
   Stakeholder-Fragen durchsehen (backlog §2).
4. **INV-4b/INV-4 Ledger schrumpfen:** benannte Tokens/Allowlist aus `src/` in YAML ziehen.
5. **Operating-Model Phase C:** Refinement automatisieren (`Fotos/` → `docs/inbox/`, backlog §2).

### Offene Frage / Retro-Vormerkung
- **Output ↔ cache_read als Tempo-Indikator** (S68): Output gegen Qualität gewichten, nicht
  maximieren — Interpretation in der Retro gemeinsam geschärft; ggf. Zielwert-Feintuning in
  `token_report.py`-Legende nachziehen, falls sich ein konkreter Korridor ergibt.

---

## Gate-Netz (Messbefehle)
- Tests + Coverage: `pytest --tb=short` (Floor 88 %, `pyproject.toml`).
- **Schulden-Scoreboard** erscheint nach jedem `pytest` (`tests/conftest.py`): Vokabular-
  Tokens, Allowlist, AC-IDs, next_session-Zeilen, Regel-Katalog-%. Ziel: Zahlen sinken.
- Architektur (INV-1..4b): `pytest tests/architecture/ --no-cov -q` · Ledger:
  `architecture_invariants.md`. Doku/Akzeptanz (INV-5): `pytest tests/docs/ tests/acceptance/ --no-cov -q`.
- **Regel-Katalog** (Nenner): `docs/spec/acceptance/rules.md` — Klasse A/B/C,
  `getestet: ja — <testname>`. Parser: `tests/acceptance/_rules.py`.
- **Token-Korridor:** <150k, bei ~135k Session beenden; Fleißarbeit an Sonnet-Subagent.
  `tools/session_context.py` eskaliert ab 120k/135k automatisch (S66).
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`
  (läuft automatisch bei `pytest`; PostToolUse-Reminder zum Teilen, S66).
- **History-Rotation (Abschluss):** `python tools/rotate_history.py --session <N> --summary "…"`
  hängt den Stand-Einzeiler an `ziel6.md` an und setzt den Stand-Block hier zurück (S69).
- **Freigabe-Gate (S66, hart):** Edit/Write blockiert bis `touch .claude/.freigabe`;
  SessionStart re-armt. Vollzieht die Freigabe-Pflicht über die Harness (ADR-0003).
