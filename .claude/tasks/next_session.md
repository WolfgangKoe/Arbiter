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

## Aktueller Stand (nach S66, 2026-06-19)

**S66 — Operating-Model-Events Hook-vollzogen (committet).** Wurzel: die Events
waren Prosa, „feuerten gar nicht von selbst" (Stakeholder-Befund). Vollzug aus der
Prosa in die Harness verlagert: (1) `tools/session_context.py` eskaliert gestuft
(`gauge_message`: ≥120k ⚠️ + Retro-Vorankündigung, ≥135k ⛔ Stopp). (2) **Hartes
Freigabe-Gate** `tools/freigabe_gate.py` (PreToolUse Edit/Write/NotebookEdit, Exit 2)
blockiert, solange Marker `.claude/.freigabe` fehlt; Freigabe physisch via
`touch .claude/.freigabe`; SessionStart-Hook löscht den Marker → jede Session neu
scharf. (3) `tools/test_report_reminder.py` (PostToolUse pytest) injiziert die
Token-Report-Teilen-Pflicht. Subagent-Routing **bewusst nicht** automatisiert (Urteil,
kein Konditionalprogramm). ADR-0003 + operating_model.md (🔧-Marker) gepflegt. +11
Tests, **911 grün**, Cov 88.45 %. Bekannte Lücke: Bash-Writes (`>`, `sed -i`) nicht
gegated. **Manueller Check:** Nach `/clear` Marker weg → erster Edit blockiert bis
`touch .claude/.freigabe`; ≥120k/≥135k-Eskalation real erst bei hohem Kontext sichtbar.

**S65 — #PSI implementiert (committet, UI-Verifikation noch ausstehend).**
`refund_deny(denies_used, faction)` + `cleared_deny(psi)` in `src/gameMechanic/psychicPhase.py`
— reine, nicht-mutierende Helfer. Alle drei aktiv-seitigen Resets routen durch einen
einheitlichen `_reset_active_power()`: cleart den Power UND refundiert das Deny-Budget der
inaktiven Fraktion → fixt den Core-Bug (denied+reset = permanent verbranntes Budget).
Neues symmetrisches **„Undo deny"**-Button (`_render_undo_deny_button`) im Deny-Column:
gibt Power + Budget zurück. „Skip Deny" verbraucht kein Budget. `deny_faction`-Feld in
`psi_result` (gesetzt bei Attempt + Skip). +8 Tests (`TestRefundDeny`/`TestClearedDeny`),
**900 grün**, Cov **88.45 %**. black/isort/ruff clean. Committet (d2a9321/cc75490).
**UI-Verifikation noch offen** — manuelle Checks:
(a) „Undo deny" nach erfolgreichem Deny → Power zurück + Budget frei;
(b) aktiv-Reset nach Deny → nächste Power im Zug denybar (Budget refundiert, kein falsches
„already used"); (c) „Skip Deny" = kein Budgetverbrauch; (d) „Undo deny" nach fehlgeschlagenem
Deny funktioniert.

**S65 — Live-Token-Gauge-Hook** (committet d2a9321): `tools/session_context.py`. In S66
auf gestufte Eskalation erweitert (s. o.).

**S64 — Psychic-Render-Schuld getestet + Token-Messung prompt-frei.** 5 reine Helfer
extrahiert (`smite_warp_charge`, `is_manifested`, `perils_pending`, `faction_deny_used`,
`can_attempt_deny`); +16 Tests (892 grün). Token-Messung: `jq` nicht installiert →
`grep`/`tail` statt `jq`; Kanonik in `CLAUDE.md`. Test-Roster Weirdboy + Canoptek Spyder.
Befund (Nutzer): Deny nicht resettbar, Smite schon → asymmetrischer Reset → S65 gelöst.

Frühere Sessions (S60–S63): Verlauf in `docs/goals/ziel6.md`.

### ▶ Nächster Schritt — frei wählbar (je eigene Freigabe)
1. **★ UI-Verifikation #PSI (Checkliste S65 oben) + Commit.** Code + Tests grün (S65);
   UI-Checks (a)–(d) manuell abhaken → #PSI + Token-Gauge-Hook gemeinsam committen.
2. **CLAUDE.md Token-Messung aktualisieren.** `Messen:`-Absatz auf `tools/session_context.py`
   / Hook umzeigen statt rohem `grep [^}]*` (verschachtelte `usage`-Objekte brechen den
   Regex — s. S65-Befund).
3. **Regel-Katalog weiter:** Movement/Charge/Morale/Psychic ✅; nächster Bereich offen
   (z. B. Deployment / Mission-Scoring / Battle-Round-Struktur — Sonnet-Subagent, eigene Session).
4. **Ledger schrumpfen** (jetzt 10) — Ratchet: R-COMBAT-09/17, R-CMD-03/04/10/11/12,
   R-CHARGE-09/10, R-MORALE-02. Verbleibende v. a. Command/Combat-Render-Logik → gleiches
   Muster (reine Funktion + Test, backlog §0/§2).
5. **Gates leser-orientiert prüfen (ADR-0002):** Debt-Scoreboard + Katalog-% gegen
   Stakeholder-Fragen durchsehen (backlog §2).
6. **INV-4b/INV-4 Ledger schrumpfen:** benannte Tokens/Allowlist aus `src/` in YAML ziehen.
7. **Operating-Model Phase C:** Refinement automatisieren (`Fotos/` → `docs/inbox/`, backlog §2).

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
  `tools/session_context.py` eskaliert ab 120k/135k automatisch (S66).
- **Token-Report:** `python tools/token_report.py --write` → `docs/metrics/overview.md`
  (läuft automatisch bei `pytest`; PostToolUse-Reminder zum Teilen, S66).
- **Freigabe-Gate (S66, hart):** Edit/Write blockiert bis `touch .claude/.freigabe`;
  SessionStart re-armt. Vollzieht die Freigabe-Pflicht über die Harness (ADR-0003).
