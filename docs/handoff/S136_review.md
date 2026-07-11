STATUS: ANSWERED

# S136 — DoD-Review (Reviewer-Subagent, Opus)

**Verdikt: GO**

Ganzheitliches Review (Code ↔ App ↔ Spielregeln ↔ Architektur ↔ Doku) über die
unkommitteten S136-Änderungen. Branch `feature/016-protocol-rp-effects`.
Lifecycle: dieses Review wird beim S136-Commit mit-committet und beim S137-Abschluss
(wie `S135_review.md` in `77b807b`) als konsumierter Handoff gelöscht.

## Prüfergebnis je DoD-Punkt

1. **Baum ↔ Erzählung** — deckungsgleich. 18 geänderte + 5 neue/gelöschte Pfade
   entsprechen 1:1 der Koordinator-Zusammenfassung: Handoff-Bereinigung (2 Screenshots,
   `go_ui_concept_s131.md`, `S135_B1_probe.patch`, `S136_4c_platzierung.md` gelöscht),
   `src/gameMechanic/attack_math.py` + `src/uiLayout/_common.py` + `src/uiLayout/gameHeader.py`,
   Tests, rules.md/design_system.md/backlog.md, Retro-Dateien. Keine unerklärte Änderung.
   Keine zweite Stand-/Backlog-Datei entstanden. `S136_plan.md`/`_4cc_befund.md`/`_B1_probe.md`
   sind Handoff-Marker, keine Stand-Duplikate.

2. **Code-Qualität (Stichprobe `git diff src/`)** — sauber. `_is_variable_attacks` ist
   generisch (keine Fraktions-Strings), Type Hints vollständig, spiegelt die int()-
   Erfolg/Fehler-Aufteilung von `_total_attacks_int` ohne Modellzahlen, kein direktes
   `int(strength)`-Casting. `label_context`-Param sauber optional (Default ""). Die drei
   Resolution-Tab-Anker + der gesammelte Fight-Anker folgen dem etablierten
   `render_inline_command_reroll`-Muster. Kommentare sind Warum-/Spec-Verweise
   (R-CMD-12, design_system §6.2/§6.3, Regelquelle) — konform zur Kommentar-Konvention.
   B1-Fix (`overflow-anchor: none`) mit Verweis auf die Playwright-Probe kommentiert.

3. **Regelkonformität (Save-Zahler)** — korrekt. Hit-/Wound-Anker → `atk_faction`
   (Angreifer würfelt Hit/Wound), Save-Anker → `def_faction` (Verteidiger wirft die
   Rettung). Deckt sich mit core_rules COMMAND RE-ROLL und der Zahler-Logik in rules.md.

4. **Artefakte aktuell** — R-CMD-12 auf 9/9 „verdrahtet", Drift 4/9→6/9→9/9 korrekt
   nachgezogen; alle 12 zitierten Testnamen existieren (Konsistenz-Test:
   „alle Testnamen existieren"). design_system.md §6.2 zieht die Hit-/Wound-/Save-Fenster
   nach. backlog.md B6 als ERLEDIGT markiert. Handoff-Marker sauber (B1 ANSWERED,
   4cc als Befund, kein DONE-Lingerer). Ledger leer (0), INV-4b 17 (deckt sich mit
   Backlog 18→17).

5. **Gates** — Schnellcheck `pytest tests/docs/ tests/architecture/ --no-cov -q`:
   18 passed. Ledger 0, Konsistenz grün, Architektur 8/8 (im Lauf enthalten).
   Vollsuite (1691 passed / 99,12 % / mypy 62 == Baseline) zentral vom Koordinator
   gefahren, hier nicht neu ausgeführt (Auflage).

6. **Retro-Maßnahmen verdrahtet** — `.claude/settings.json` registriert den neuen
   PreToolUse-Bash-Hook `tools/hook_pytest_foreground.py` (fail-open, blockt nur
   backgrounded pytest); `agent_scopes.md` Selbst-Stopp 150k→100k; `CLAUDE.md` +
   `next_session.md` zweistufiger Korridor (Wind-down ~120k).

## Offene Punkte / Empfehlungen S137 (nicht GO-blockierend)

- **Testlücke Charge-Aufrufstelle** `chargephase.py:114`: kein dedizierter Test, nur
  die generische `render_inline_command_reroll`-Suite deckt den Mechanismus. In rules.md
  transparent als „kleine verbleibende Testlücke (keine Ledger-Schuld)" dokumentiert —
  in S137 schließen.
- **design_system.md §6.3** Wertfeld-/Familie-2-Formulierung präzisierungsbedürftig
  (Restschuld aus Befund).
- **B1-Option „Dropdown-Höhen stabilisieren"** bewusst nicht umgesetzt (Playwright-
  Messung: Delta 0 nach `overflow-anchor: none`, nicht nötig) — als erledigt betrachten,
  nur bei erneutem Scroll-Sprung wieder aufgreifen.
- **`next_session.md`** bei 86/120 Zeilen (Soft-Ziel ≤70) — beim nächsten Kürzen straffen.
- **Neuer Hook** `tools/hook_pytest_foreground.py` selbst ohne Test (fail-open, tools/
  außerhalb der Coverage) — vertretbar; optional in S137 ein Smoke-Test.

**Begründung GO:** Baum deckt sich vollständig mit der Erzählung, Code ist generisch und
konventionskonform, Regel-Zahlerlogik korrekt, alle zitierten Tests existieren, Doku-Drift
(R-CMD-12) sauber korrigiert, Schnell-Gates grün. Die verbleibenden Punkte sind
dokumentierte, nicht-blockierende Schulden mit klarem S137-Anschluss.
