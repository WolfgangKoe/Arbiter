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

## Aktueller Stand (nach S70, 2026-06-20)

**S70 — Regel-Ledger 8 → 1 + Overview-Ausbau.** (1) **R-COMBAT-09** getestet
(`ability_invuln_save`, kleinster Invuln gewinnt). (2) **Render-Ledger via Sonnet-
Subagent** extrahiert: R-CMD-03 (Battle-forged-Gate `can_gain_command_point`, gated
matched/crusade), R-CMD-10 (`apply_buff_to_unit` → `unit_mutations.py`, idempotent),
R-CMD-11 (`resolve_gain_cp_roll`), R-CHARGE-09/10 (`hi_eligible_units`/
`hi_already_performed`), R-MORALE-02 (`morale_test_required`). **Opus-Review-Befund:**
der Subagent hatte 3 von 6 Helfern als *verwaiste Parallel-Implementierungen* angelegt
(grün getestet, aber nie vom Render-Code aufgerufen) — Opus hat alle drei verdrahtet,
`apply_buff_to_unit` in die richtige Heimat (`unit_mutations`) verschoben und Katalog-
`code:`-Refs korrigiert. **Lehre → [[feedback-proactive-subagent-prep]]:** Subagenten
künftig Selbstprüf-Checkliste „grep belegt: Nicht-Test-Code ruft jeden Helfer auf"
mitgeben. (3) **Overview erweitert** (token_report.py, Sonnet-Subagent): Subagent-
**Peak-Korridor (150k)**-Diagramm + Peak-Spalte in „wer wofür" — wir sehen jetzt, ob
Subagenten selbst im Korridor bleiben. **985 grün, Cov 92.25 %, Ledger=1** (nur
R-COMBAT-17, Rapid-Fire-Distanz = reiner Tisch-Anteil, kein sinnvoller Test).

**Vorausschauend arbeiten (Nutzer-Direktive S70, [[feedback-proactive-subagent-prep]]):**
ToDos der nächsten Session(s) im Blick halten und Subagenten **vorarbeiten** lassen,
sodass im besten Fall nur Review bleibt. Subagent-Peak im Overview-Diagramm beobachten.

Frühere Sessions (S60–S69): Verlauf in `docs/goals/ziel6.md` (Session-Historie).

### ▶ Nächster Schritt — frei wählbar (je eigene Freigabe)
**Vorab prüfen:** Welcher Schritt lässt sich als Fleißarbeit an einen Subagenten
vorab geben (nur Review bleibt)? Subagent-Peak im Overview-Korridor-Diagramm checken.
1. **Regel-Katalog weiter (Nenner wächst):** nächster Bereich offen — Deployment /
   Mission-Scoring. **Subagent-Vorarbeit-Kandidat** (Klasse A/B/C-Entwurf nach Format;
   Opus reviewt). Selbstprüf-Checkliste „Helfer verdrahtet?" mitgeben.
2. **Output↔Ziel-Fortschritt-Zeile** im Review verankern (`operating_model.md` Event 5):
   knappe „Ziel-Fortschritt: ja/teils/nein, woran sichtbar" — Soll-Ist ohne Token-Zielzahl.
3. **Gates leser-orientiert prüfen (ADR-0002):** Debt-Scoreboard + Katalog-% gegen
   Stakeholder-Fragen durchsehen (backlog §2).
4. **INV-4b/INV-4 Ledger schrumpfen:** benannte Tokens/Allowlist aus `src/` in YAML ziehen
   (20 Tokens, 10 Allowlist-Einträge). **Subagent-Vorarbeit-Kandidat** je Token.
5. **Operating-Model Phase C:** Refinement automatisieren (`Fotos/` → `docs/inbox/`, backlog §2).
6. **Hook-Idee (Nutzer S70):** wenn Subagent-Peak verlässlich im Overview steht, später
   einen Hook bauen, der mehr Subagenten-Nutzung erlaubt, ohne Überblicksverlust.

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
