STATUS: DONE

# S135 — DoD-Review (Reviewer, Opus)

Geprüfter Bereich: Commits `4bf311f..9993771` (5 Commits) gegen die DoD aus `CLAUDE.md`.
Gates selbst ausgeführt (2026-07-10). Vollsuite lief laut Auftrag zuletzt grün
(1673 passed / 99,12 %) — hier nur die schnellen Gates nachgeprüft.

## Gate-Ergebnisse

| Gate | Ergebnis |
|---|---|
| `pytest tests/architecture/ tests/docs/ tests/acceptance/ --no-cov -q` | **26 passed** (4,7 s) |
| INV-4b (Ratchet) | 6 Tokens / 17 Fundstellen / 3 Dateien — unverändert, kein Zuwachs durch S135 |
| Regel-Ledger (impl. ohne Test) | 0 (leer) |
| `python tools/mypy_gate.py` | **62 errors == baseline 62 — OK** |

## Urteil: GO

Die S135-Arbeit (Paket 4a/4b/4c-Anker, B6-Setup-Layout, B1-Probe, S134-Entscheide + B10)
ist regelkonform, generisch, getestet und in den Specs nachgezogen; es bleiben zwei
mechanische Doku-Nachzüge für den Abschluss-Commit und die offene manuelle UI-Checkliste.

## DoD-Prüfung im Einzelnen

1. **Regelkonform** — Anker-Platzierung folgt der P-08-Auflösungsreihenfolge
   (`docs/spec/processes.md`): Hit-Anker nach dem HIT-Block, Wound-Anker nach dem
   Wound-Block, Save-Anker am Save-Block, Damage-/Anzahl-Attacken-Fenster an den
   jeweiligen Eingabefeldern. Scoping über `effect_type`/`effect_stat` verhindert,
   dass GOs mit gemeinsamem `(phase, event)`-Fenster am falschen Wurf erscheinen
   (Stichprobe: Shadows of Drazak nur Hit, Whirling Onslaught nur Wound, Quantum
   Deflection nur Save — je mit Positiv- UND Negativ-Test in
   `tests/uiLayout/test_common.py`). `rules.md` R-CMD-12 ehrlich nachgezogen
   (4/9 Wurf-Arten verdrahtet, 5 als dokumentierte Schuld mit Begründung). ✓
2. **Generisch** — keine neuen Fraktions-Strings in `src/`; Keyword-Gate läuft
   datengetrieben über `stratagem_conditions_met(conditions, unit)` (YAML-Conditions),
   INV-4b-Scoreboard unverändert. ✓
3./4. **Tests + Architektur-Gate grün** — s. Gate-Tabelle; 106 Tests in
   `test_common.py`, neue Render-/HTML-Tests für alle drei Anker + Anzahl-Attacken-
   Reroll (Positiv- und Negativ-Fälle). ✓
5. **Clean Code (Stichprobe)** — neue Helper sinnvoll benannt und richtig verortet:
   `stratagem_conditions_met` in `src/gameObjects/stratagem.py` (gemeinsame Heimat für
   zentrale Liste + Inline-Anker, ersetzt Doppel-Implementierung aus
   `gameProtocoll._conditions_met`); `render_round_choice_directives` in
   `src/uiLayout/_common.py` (eine Quelle für armyCard-In-Game-UI und
   Setup-Lese-Dropdown, ersetzt 4 Copy-Paste-Stellen). Docstrings erklären das
   *Warum* mit Spec-Verweis (B10-Konvention bereits gelebt). ✓
6. **UI manuell** — B6 (5 Schritte) vom Stakeholder im Browser verifiziert;
   Restpunkte s. offene Checkliste unten (kein NO-GO-Kriterium laut Auftrag). ◐
7. **Artefakte** — `design_system.md` §6.2 (Schuld-Tabelle 14→11 offene GOs, drei
   fehlende Ereignis-Fenster benannt, Paket-5/6-Empfehlung), `go_klassifikation.md`
   (Nachzug ohne Duplizierung, verweist für den Umsetzungsstand auf §6.2),
   `rules.md` R-CMD-12, `S134_offene_punkte.md` (ANSWERED, alle Entscheide
   eingetragen), `CLAUDE.md` (B10 exakt wie freigegeben) — alles konsistent
   nachgezogen. `session_archive.md` + `next_session.md` laut Koordinator soeben
   aktualisiert (als gegeben gewertet). Zwei Rest-Drifts s. Befunde 1+2. ◐

## Befunde

1. **MINOR — Backlog-Drift Paket 4 (`docs/goals/backlog.md`):** Paket-4-Checkbox
   (Z. ~136) steht noch 🟢 (offen), obwohl 4a/4b/4c committet sind; ebenso nennt der
   Punkt „Command Re-Roll auf alle 9 Wurf-Arten" (Z. ~147) noch „3/9", `rules.md`
   führt jetzt 4/9. Mechanischer Nachzug im Abschluss-Commit: Paket 4 auf ✅ (mit
   Verweis „Rest → Paket 5/6 laut §6.2"), 3/9 → 4/9. Keine Stakeholder-Entscheidung
   nötig (Aufteilungs-Empfehlung Paket 5/6 steht bereits dokumentiert in §6.2).
2. **MINOR — Stale Statuszeile in `docs/handoff/S135_planning.md`:** Zeile 2 sagt
   „Umsetzung gestoppt nach Aufgabe 1 (Nutzungslimit)" — tatsächlich sind die
   Aufgaben 1–5 und 10 umgesetzt (5 Commits). Zeile im Abschluss-Commit korrigieren
   (z. B. „Umgesetzt: Aufgaben 1–5, 10; offen: 6–9 → next_session.md").
3. **INFO — Plan-Aufgaben 6–9 offen** (before_battle/PHASES, B8 Statusbereich,
   B4-Sofortteil ++/OC, Dakka): nicht umgesetzt wegen Limit-Stopp; laut Koordinator
   in `next_session.md` übernommen — kein Befund, nur zur Vollständigkeit.
4. **INFO — `S135_B1_probe.md` steht korrekt auf NEEDS-DECISION:** Probe-Patch
   liegt bereit (`S135_B1_probe.patch`, unangewendet — Arbeitsbaum clean, korrekt),
   Browser-Zwei-Stufen-Test wartet auf den Stakeholder. Kein Drift, gehört in die
   Checkliste unten.
5. **INFO — Fail-safe-Design bestätigt:** `render_reactive_stratagem_box` versteckt
   Keyword-gebundene GOs, wenn kein `unit_for_conditions` übergeben wird (statt sie
   für jede Einheit zu zeigen) — deckungsgleich mit dem Gate der zentralen Liste,
   im Docstring dokumentiert. Bewusst als positives Muster festgehalten.

## Offene manuelle UI-Checkliste (Stakeholder, Browser)

- [ ] **B6-Rest:** Trennlinie (`st.divider`) zwischen den sechs Slot-Dropdowns und dem
      „Read directive"-Dropdown sichtbar; Lese-Dropdown wechselt NUR den Text, nie
      die Zuweisung; nach „Start Game" verschwindet der Block.
- [ ] **4a Hit-Anker:** Shooting/Fight → Angriff auflösen → am HIT-Block erscheint die
      Kompaktkarte des Verteidigers (z. B. Shadows of Drazak) nur bei passender
      Ziel-Einheit; Use bucht CP.
- [ ] **4a Wound-Anker:** dito am Wound-Block (z. B. Whirling Onslaught), erscheint
      NICHT am Hit-Block.
- [ ] **4b Save-Anker:** Quantum Deflection am Save-Block; Damage-/Psychic-/Deny-
      Reroll jetzt als GO-Karte (kein Inline-Link mehr), Undo/Reopen funktioniert.
- [ ] **4c Anzahl-Attacken:** Melee-Gruppenzuweisung → Command-Re-Roll-Angebot am
      „‹Weapon› — Attacks"-Feld, nur bei CP ≥ 1 und einmal pro Phase.
- [ ] **B1 Zwei-Stufen-Test** gemäß `S135_B1_probe.md` (Stufe 1 ohne Patch, ggf.
      Stufe 2 mit Patch) — Ergebnis in die Probe-Datei eintragen.
