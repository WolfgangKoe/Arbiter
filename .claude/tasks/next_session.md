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

## Aktueller Stand (nach S68, 2026-06-20)

**S68 — vier S67-Nutzerwünsche umgesetzt (Operating-Model/Tooling/Doku).**
(1) **Vorausschauender Review/Retro-Fragenkatalog** in `operating_model.md` Event 5 (Retro-
Schritt): Review+Retro schauen jetzt auch nach VORN (Qualität · Operating-Model · Hooks/Gates ·
blinde Flecken · Automatisierung · Doku/Backlog · Skalierung in kleinen Experimenten · Kontext-
Versorgung · Priorität · Engpass). (2) CLAUDE.md neue Subsection **„Haltung"** (ganzheitlich ·
konstruktiv-kritisch · lösungsorientiert · vorausschauend · stakeholder-verständlich) für
Planning + Abschluss. (3) **Composition-Bar-Legende + Zielwerte** in `token_report.py`
(input/cache_creation/cache_read/output; cache_read hoch = gut, Output gegen Qualität gewichtet —
nicht maximieren). (4) **Model-Mix-Zeichen** getauscht (Opus/Sonnet-Kontrast): `█` Opus · `·`
Sonnet · `▒` Haiku · `▓` sonstige; Test bewusst mitgezogen. **915 grün, Cov 91.88 %**, Nenner=121.

Frühere Sessions (S60–S67): Verlauf in `docs/goals/ziel6.md` (Session-Historie, ab Zeile ~1581).

### ▶ Nächster Schritt — frei wählbar (je eigene Freigabe)
0. ~~History-Rotation `next_session.md → ziel6.md` automatisieren~~ ✅ **S69** — `tools/rotate_history.py`
   (Helfer-Tool, manuell am Abschluss; Mechanik automatisiert, Verdichten bleibt Urteil).
0b. **Output↔Ziel-Fortschritt-Zeile** im Review verankern (`operating_model.md` Event 5): knappe
   „Ziel-Fortschritt: ja/teils/nein, woran sichtbar" — Soll-Ist ohne Token-Zielzahl. Token-Report
   bleibt reine Kosten/Effizienz-Linse (cache_read hoch = warmer, günstiger Kontext; Output = Spend).
1. **Regel-Katalog weiter:** Movement/Charge/Morale/Psychic/Battle-Round ✅; nächster Bereich
   offen (z. B. Deployment / Mission-Scoring — Sonnet-Subagent, eigene Session).
2. **Ledger schrumpfen** (10) — Ratchet: R-COMBAT-09/17, R-CMD-03/04/10/11/12, R-CHARGE-09/10,
   R-MORALE-02. Muster: reine Funktion + Test (backlog §0/§2).
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
