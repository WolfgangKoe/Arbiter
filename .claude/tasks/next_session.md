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

## Aktueller Stand (nach S67, 2026-06-20)

**S67 — #PSI verifiziert + abgeschlossen, Battle-Round-Katalog, Doku-Fixes (committet).**
(1) UI-Verifikation #PSI vom Nutzer bestätigt („passt alles") → 3 Regressionstests
`TestDenyRefundFlow` nageln die S65-Fix-End-Zustände fest (aktiv-Reset/Undo → Budget
refundiert, Power wieder denybar); Flow (c) „Skip" ist Render-Code, manuell verifiziert.
(2) Neuer Katalog-Bereich **Battle-Round-Struktur** R-ROUND-01..10 (Sonnet-Subagent +
Opus-Review): Turn-Struktur, fixer `first_player`, Phasenreihenfolge, Turn-Wechsel,
Rundenzähler, Spiellänge, Timing simultaner Regeln. (3) Doku-Drift gefixt:
`init_game_state`→`init_state` (3×, inkl. vorbestehender R-CMD-04); R-ROUND-06 mit
`test_init_state_sets_round_to_one` gedeckt → Ledger zurück auf **10**. (4) CLAUDE.md
Token-Messung zeigt nun auf den `tools/session_context.py`-Hook (statt rohem Regex).
**915 grün, Cov 91.88 %**, Nenner=121. Commits 61d6811, 1b264a4, c9504a4.

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
Committet (d2a9321/cc75490). **In S67 UI-verifiziert + per `TestDenyRefundFlow` regressionsgetestet → #PSI abgeschlossen.**

**S65 — Live-Token-Gauge-Hook** (committet d2a9321): `tools/session_context.py`. In S66
auf gestufte Eskalation erweitert (s. o.).

**S64 — Psychic-Render-Schuld getestet + Token-Messung prompt-frei.** 5 reine Helfer
extrahiert (`smite_warp_charge`, `is_manifested`, `perils_pending`, `faction_deny_used`,
`can_attempt_deny`); +16 Tests (892 grün). Token-Messung: `jq` nicht installiert →
`grep`/`tail` statt `jq`; Kanonik in `CLAUDE.md`. Test-Roster Weirdboy + Canoptek Spyder.
Befund (Nutzer): Deny nicht resettbar, Smite schon → asymmetrischer Reset → S65 gelöst.

Frühere Sessions (S60–S63): Verlauf in `docs/goals/ziel6.md`.

### ▶▶ TOP-PRIO nächste Session (S67-Nutzerwünsche — zuerst, je eigene Freigabe)
1. **Operating-Model: vorausschauender Review/Retro-Fragenkatalog.** Review+Retro sollen auch
   nach VORN schauen. Fragen (Nutzer): Qualität verbessern? · Operating-Model verbessern? ·
   Hooks/Gates nötig? · Was übersehen wir? · Was automatisieren? · Doku/Backlog besser
   strukturieren? · besser werden / Umsetzung skalieren (vorausschauend, kleine Experimente,
   KEIN großer Umbau)? · wie sicherstellen, dass Claude jederzeit die nötigen Infos/Hinweise
   bekommt (evtl. Haiku/Sonnet-Beobachter-Subagent)? — Claude ergänzt + nach operating_model.md.
2. **CLAUDE.md Kulturregeln:** ganzheitliche, konstruktiv-kritische, lösungsorientierte Haltung
   für Planning + Abschluss festhalten.
3. **Token-Bar-Legende + Zielwerte** (input/cache_creation/cache_read/output) in overview.md:
   erklären + anzustrebende Werte für effizientes Arbeiten (z. B. hoher cache_read-Anteil = gut).
4. **Model-Mix-Zeichen tauschen** (besserer Opus/Sonnet-Kontrast): `█ Opus · · Sonnet · ▒ Haiku ·
   ▓ sonstige` (Sonnet→Leerzeichen, sonstige→▓). In tools/token_report.py + overview.md.

### ▶ Nächster Schritt — frei wählbar (je eigene Freigabe)
✅ Erledigt in S67: UI-Verifikation #PSI · CLAUDE.md Token-Messung · Battle-Round-Katalog.
1. **Regel-Katalog weiter:** Movement/Charge/Morale/Psychic/Battle-Round ✅; nächster Bereich
   offen (z. B. Deployment / Mission-Scoring — Sonnet-Subagent, eigene Session).
2. **Ledger schrumpfen** (jetzt 10) — Ratchet: R-COMBAT-09/17, R-CMD-03/04/10/11/12,
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
