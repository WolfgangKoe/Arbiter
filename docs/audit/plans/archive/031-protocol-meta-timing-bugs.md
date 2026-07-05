# Plan 031 — Protokoll-Meta-Timing: Direktiven-Wahl am Rundenanfang + Sperre nach Wahl

## Status

- **Priority**: P-HOCH — beide Bugs sind regelwidrig und verschaffen dem zweiten Spieler
  bzw. dem aktiven Spieler einen unerlaubten Informationsvorteil.
- **Effort**: S–M (Bug 1: State-Entkoppelung in `armyCard.py` + `game_state.py`; Bug 2: Block entfernen).
- **Risk**: MITTEL — beide Änderungen berühren `armyCard.py` und `game_state.py`; Render-Code
  ist test-ausgeschlossen → manuelle UI-Verifikation zwingend.
- **Depends on**: 025 ✅ (Direktiven-Struktur 9E-konform), 016 (Direktiven-Anzeige).
- **Category**: Bugfix (je Regressionstest PFLICHT, DoD).

## Regelgrundlage

- `docs/work/wahapedia_necrons/faction_overview.txt` Z. 564–579: Command Protocol und
  Direktive werden „**at the start of each battle round**" gewählt — **beide Spieler**,
  vor dem ersten Zug der Runde. Bei Simultaneität: Roll-Off (core_rules.txt Z. 511–517).
- Direktive gilt für die gesamte Runde; einmal gewählt, keine nachträgliche Änderung.

## Bug 1 — Protokoll-Direktiven-Wahl-Timing (zweiter Spieler)

### Ist-Zustand

`armyCard.py` Z. 267–300: Die Direktiven-Wahl-UI ist an `is_active` gekoppelt
(`is_active = faction == st.session_state["active"]`). Der zweite Spieler sieht den
Wahl-Button erst in seiner eigenen Command Phase — also nachdem der erste Spieler seinen
vollständigen Zug abgeschlossen hat. Das gibt dem zweiten Spieler einen unerlaubten
Informationsvorteil (er kann nach Kenntnis des Gegenzugs wählen).

### Soll-Zustand

Beide Spieler wählen ihre Direktive **am Rundenanfang** (vor dem ersten Zug der Runde),
unabhängig davon, wer gerade aktiv ist. Gleichzeitig-Wahl in der App: beide Direktiven-UIs
sind zu Rundenbeginn offen, bis beide Spieler gewählt haben.

### Korrektur-Skizze

1. **`game_state.py:_reset_round_choice_state()` (Z. 576–591):** Für jede Fraktion mit
   `round_choice`-Daten ein Flag `protocol_directive_pending_<player>` auf `True` setzen
   (analog vorhandener `pending_*`-Flags). GENERISCH: kein Fraktions-String — über die
   `round_choice`-Daten-Struktur iterieren (die bereits data-driven ist).

2. **`src/gameMechanic/armyCard.py:_render_round_choice_ui()` (Z. 267–300):**
   `is_active`-Guard durch `protocol_directive_pending_<player>`-Prüfung ersetzen.
   Button erscheint, solange das Pending-Flag gesetzt ist — unabhängig vom aktiven Spieler.
   Flag nach Wahl löschen.

3. **Generisch halten:** kein neuer Fraktions-String in `src/`; die `round_choice`-
   Struktur ist bereits datengetrieben (aus YAML geladen). Änderung darf nur
   auf vorhandene Strukturschlüssel referenzieren.

### Test

`test_second_player_directive_pending_at_round_start` — prüft, dass das Pending-Flag
für beide Spieler am Rundenanfang gesetzt ist und unabhängig von `active` gesetzt wird.

---

## Bug 2 — Direktive des 6. (immer-aktiven) Protokolls nachträglich änderbar

### Ist-Zustand

`armyCard.py` Z. 219–225: Ein „Change extra directive"-Button erlaubt es, die Wahl der
Direktive des 6. (immer-aktiven) Protokolls jederzeit zurückzusetzen und neu zu treffen —
auch in Runde 3+ und in jeder Phase (Command, Movement, Shooting, Fight …). Das erlaubt
eine reaktive Anpassung nach Kenntnis des Spielzugs, was regelwidrig ist.

### Soll-Zustand

Die Direktive ist nach einmaliger Wahl für die laufende Runde gesperrt. Ein Reset passiert
ausschließlich durch `_reset_round_choice_state()` am Beginn der nächsten Runde (läuft
bereits, Z. 591) — kein manueller „Change"-Button in der laufenden Runde.

### Korrektur-Skizze

- **`armyCard.py` Z. 219–225:** Den „Change extra directive"-Block (`_render_extra_round_choice`)
  ersatzlos entfernen. Kombiniert mit dem Bug-1-Fix ist die Wahl auf das Rundenanfang-Fenster
  beschränkt, sodass kein separater Reset-Mechanismus nötig ist.
- Die reguläre `_reset_round_choice_state()`-Logik (wird am Rundenanfang gerufen) bleibt
  unverändert — sie erledigt den Runden-Reset bereits korrekt.
- Generisch in `_render_extra_round_choice` halten.

### Tests

- `test_extra_directive_locked_after_selection` — prüft, dass nach Wahl kein erneutes
  Setzen der Direktive in der laufenden Runde möglich ist.
- `test_extra_directive_reset_at_new_round` — prüft, dass `_reset_round_choice_state()`
  die Direktive für die nächste Runde korrekt zurücksetzt (Regressionstest).

---

## Scope (betroffene Dateien)

- `src/gameMechanic/armyCard.py` — Bug 1: `_render_round_choice_ui()` Z. 267–300;
  Bug 2: `_render_extra_round_choice` Z. 219–225 (Block entfernen).
- `src/gameMechanic/game_state.py` — Bug 1: `_reset_round_choice_state()` Z. 576–591
  (Pending-Flags ergänzen).
- `tests/gameMechanic/test_ability_engine.py` oder neues `test_armyCard_round_choice.py` —
  alle drei Regressionstests.

## Steps

### Step 1 — Bug 2: „Change extra directive"-Block entfernen (XS)

**Warum zuerst:** Kleinste, risikoärmste Änderung; kein State-Umbau nötig.

1. `armyCard.py` Z. 219–225 lesen; „Change extra directive"-Block identifizieren.
2. Block entfernen.
3. Regressionstest `test_extra_directive_locked_after_selection`.
4. Vollsuite `pytest --tb=short`.

**Manuelle UI-Verifikation:** In der App eine Direktive wählen → prüfen, dass kein
„Change"-Button mehr erscheint; Runden-Reset am nächsten Rundenanfang funktioniert.

**Token-Schätzung:** ~5–8k (Sonnet).

---

### Step 2 — Bug 1: Pending-Flag-Mechanik + `is_active`-Entkoppelung (S–M)

1. `game_state.py:_reset_round_choice_state()` lesen; Pending-Flags GENERISCH ergänzen
   (über `round_choice`-Daten iterieren, kein Fraktions-String).
2. `armyCard.py:_render_round_choice_ui()` — `is_active`-Guard durch Pending-Flag-Prüfung
   ersetzen; Flag nach Wahl löschen.
3. Scoping-Pflichtschritt: `grep -rn "is_active\|round_choice\|protocol_directive_pending"
   src/gameMechanic/armyCard.py src/gameMechanic/game_state.py` — alle Treffer prüfen.
4. Regressionstest `test_second_player_directive_pending_at_round_start`.
5. Vollsuite `pytest --tb=short`.

**Manuelle UI-Verifikation:**
- Runde-Start: Direktiven-UI beider Spieler sichtbar (auch inaktiver Spieler).
- Nach Wahl Spieler A: UI für A weg, B noch offen.
- Nach Wahl Spieler B: beide UIs weg bis nächste Runde.
- Normaler Spielfluss (Züge, Phasen) unverändert.

**Token-Schätzung:** ~15–20k (Sonnet).

---

## DoD-Checkliste (beide Steps)

1. **Regelkonform** — `faction_overview.txt` Z. 564–579 + `core_rules.txt` Z. 511–517
   belegen „at the start of each battle round" und Simultaneitäts-Roll-Off ✓.
2. **Generisch** — kein neuer Fraktions-String in `src/`; Pending-Flag läuft über
   vorhandene `round_choice`-Datenstruktur (data-driven) ✓.
3. **Tests grün** — Vollsuite `pytest --tb=short`, Coverage-Gate; je Fix ein Regressionstest.
4. **Architektur-Gate** — Änderungen in `gameMechanic/`; kein Layer-Verstoß erwartet
   (`pytest tests/architecture/ --no-cov -q` grün).
5. **Clean Code** — minimale additive Änderungen, `black`/`isort`/`ruff` sauber.
6. **UI manuell verifiziert** — Render-Code test-ausgeschlossen; Verifikationsschritte
   je Step benannt (s. o.); nie „fertig" ohne manuelle Prüfung.
7. **Artefakte aktuell** — `next_session.md` + `docs/goals/backlog.md` nach Abschluss
   aktualisieren.

## STOP conditions

- Vorher grüner Test wird rot → STOP, Nutzer fragen.
- `round_choice`-Datenstruktur hat unerwartete Schlüssel → STOP, Scope klären.
- Pending-Flag-Einführung bricht vorhandene `_reset_round_choice_state()`-Tests → STOP.
- `is_active`-Entkoppelung bewirkt, dass Direktiven-UI in falschen Phasen erscheint → STOP.
