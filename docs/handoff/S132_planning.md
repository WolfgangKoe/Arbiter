STATUS: ANSWERED

# Planning — S132 (2026-07-09) — überarbeitet nach Stakeholder-Entscheid

**Priorität:** P1 (Design-System-Roadmap, Stakeholder-Auflage S130) **Scope:** Paket 1 der
GO-UI-Migration (`design_system.md` §6) + Command-Re-Roll-Angebot für Advance/Charge (ohne
Werterfassung) + Start-Game-Button-Position (Beobachtung ③) + XS-Doku-Nachzug.
Refinement Spielvorbereitungsscreen (Beobachtung ②) bleibt offener Punkt, kein Code diese Session.

## Grundannahme (vom Stakeholder bestätigt, verschärft)

**Die App würfelt NICHT — und braucht für Advance/Charge auch KEINE Wurf-Eingabe.** Man würfelt
am Tisch und handelt entsprechend: in der Bewegungsphase zählt nur der Zustand „Advanced" (egal
welches Ergebnis), beim Charge nur Erfolg oder Fehlschlag. Command Re-Roll = Button drücken,
1 CP wird gebucht, der Nutzer würfelt am Tisch neu — keine Werterfassung, keine App-Bewertung.

## Entschieden am 2026-07-09 (Stakeholder-Antworten)

1. **Split 1a/1b: bestätigt** — bleibt wie vorgelegt.
2. **KEIN Wurf-Feld für Advance/Charge**, auch nicht neu bauen. Ex-Auftrag 2a (`dice_input.py`)
   entfällt ersatzlos; Ex-2b wird zu Auftrag 2: nur das Inline-Re-Roll-ANGEBOT verdrahten
   (Re-Use `render_inline_command_reroll`, `_common.py:601`, Pull-not-Push).
3. **Charge-Erfolgsermittlung: bleibt exakt die manuelle Erfolg/Fehlschlag-Bestätigung** —
   keine automatische Bewertung (war mehrfach dokumentiert, Frage 3 des Erstentwurfs hinfällig).
4. **`go_card.py` als neues Modul: bestätigt.** `dice_input.py` entfällt (s. 2). Zusätzlich
   beauftragt + freigegeben: Backlog-Notiz „`_common.py` refactoren, Attackensequenz eigene
   Datei" — **eingetragen** in `docs/goals/backlog.md` §4 Architektur-Schulden.

**Umsetzungs-Freigabe erteilt** (Stakeholder, 2026-07-09, Chat): Aufträge 1a → 1b → 2 → 3 → 4.
Beobachtung ④ (Profilkarte Setup-Screen) NICHT in S132 — als offener Punkt in `next_session.md` mitführen.

## Ergebnis-Log (vom Koordinator aus konsumierten DONE-Handoffs überführt)

**1a DONE** (Vollsuite 1601 passed, Cov 99,15 %, mypy 75=Baseline): `src/uiLayout/go_card.py` neu
(HTML-Builder, 100 % Cov, `GoCardState` dormant/ready/used/locked) + `render_go_card()`-Wrapper in
`_common.py` (+100 Z. — **Review-Punkt:** `_common.py` sollte eigentlich nicht weiter wachsen) +
18 Tests. Akkordeon-Root-Cause: nacktes `st.expander(expanded=False)` hält Open-State über Reruns;
Fix = expliziter `key` + `on_click`-Callback setzt Flag vor dem nächsten Run auf False.

**1b DONE** (Vollsuite 1607 passed + 1 failed nur Handoff-Hygiene, Cov 99,15 %, mypy 75):
`gameProtocoll._render_stratagem_column` rendert GO-Karten; neu `_go_state_and_reason()`
(clickable→ready; greyed+Undo-Fenster→used; sonst locked mit Grund "used"/"CP insufficient") und
`undo_stratagem()` in `_common.py` als kanonisches Gegenstück zu `spend_stratagem` (CP zurück,
used-Sets, active_modifiers); +7 Tests. Fachverhalten unverändert, nur Darstellung.

**2 DONE** (Vollsuite 1608 passed 0 failed, Cov 99,15 %, mypy 75): reine Verdrahtung —
`movementPhase.py:140` (Angebot unter Status-Buttons, nur bei „advanced") und
`chargephase.py:114` (unter „Roll 2D6"-Caption, vor Successful/Failed), je `reopen_key=uid`,
`on_reroll`=No-op; kein Datenbau, kein Umbau von `render_inline_command_reroll`.
Manuelle Prüfpunkte 2: Advance-Klick → `↻ Command Re-Roll (1 CP)` erscheint, Klick bucht 1 CP,
Angebot verschwindet (used this phase), bei 0 CP gar nicht sichtbar, KEIN Zahlenfeld;
Charge analog vor der Erfolg/Fehlschlag-Entscheidung, Successful/Failed fachlich unverändert.

**3 DONE** (Vollsuite 1608 passed 0 failed, Cov 99,15 %, mypy 75): Start-Game-Button (divider +
if-Block) in `gameActionsArea.py` von Z. 254–262 nach direkt unter die „X goes first"-Buttons
verschoben (vor die Round-Choice-Schleife); Button-Code ist von der Schleife unabhängig.
Manuelle Prüfpunkte 3: Button sitzt unter der Erstspieler-Auswahl, Spielstart funktioniert,
Round-Choice-Zuweisung darunter bleibt bedienbar.

**4 DONE** (Doku-Gate 18 passed): `design_system.md` §6.3 Advance/Charge aus „Gilt für"-Liste
entfernt + Gegenbeispiel + Mockup Advance→Deny; `backlog.md` §2 Paket-2-Text präzisiert;
`next_session.md` ▶2 präzisiert (ohne Wurf-Eingabe-Baustein).

**Konsolidierte manuelle UI-Prüfpunkte 1a/1b** (vor Session-Ende abarbeiten): GO-Karten-Liste pro
Spieler-Spalte (Core- vor Fraktions-Sektion); `bereit` Gold-Rahmen `Use (N CP)` → Klick bucht CP,
Karte wird `verwendet`; `verwendet` `↺ Undo (+N CP)` → CP zurück, Karte wieder `bereit`;
`gesperrt` gedimmt mit kursivem Grund-Suffix, Button disabled; Kompaktform ohne Chips; Akkordeon
bleibt nach Use/Undo-Rerun ZU, offen nur nach aktiver Nutzer-Öffnung; Keyword-Chips nur bei
vorhandenen `conditions`.

## Executor-Aufträge

| # | Aufgabe | Effort | Token | Modus | Tier | Dateien |
|---|---|---|---|---|---|---|
| 1a | GO-Karten-Baustein: reiner HTML-Builder (Header/Name/CP/Aktions-Slot, Keyword-Chips via `chip()`, 4-Zustand-Farblogik §6.5) + dünner Streamlit-Wrapper (Buttons, Akkordeon-Fix: explizites `st.session_state`-Flag statt nacktem `st.expander(expanded=False)`, da Streamlit den Open-State sonst implizit über Reruns hinweg hält — root cause der S130-Beschwerde) | M | ~30k | Gate | Sonnet | neu: `src/uiLayout/go_card.py`; Re-Use `src/uiLayout/badges.py` (`chip()`) |
| 1b | Zentrale Stratagems-Liste (`gameProtocoll.py::_render_stratagem_column`) auf den GO-Karten-Baustein umstellen; State-Mapping: `stratagem_visibility()` liefert `clickable`/`greyed`/`hidden` → `bereit`/(`verwendet`\|`gesperrt`)/entfällt — **„ruhend" kommt in der zentralen Liste nicht vor**, nur 1a testet den 4. Zustand isoliert | S–M | ~22k | Gate | Sonnet | `src/uiLayout/gameProtocoll.py` |
| 2 | Inline-Command-Re-Roll-Angebot (Re-Use `render_inline_command_reroll`, KEINE Werterfassung) in zwei Kontexten verdrahten. **Platzierung Advance:** `movementPhase.py::_active_movement`, direkt unter den Status-Buttons, nur solange `movement_choice == "advanced"` (Fenster „Advance-Wurf liegt frisch auf dem Tisch"); `on_reroll` = No-op (nichts wiederzuöffnen), `reopen_key` = uid. **Platzierung Charge:** `chargephase.py::_active_charge`, unter der „Roll 2D6"-Caption neben den Successful/Failed-Buttons (Re-Roll wird VOR der Erfolg/Fehlschlag-Entscheidung gedrückt); `reopen_key` = uid. YAML deckt beide Phasen bereits ab (`_shared/stratagems.yaml:13`: `phase: [movement, …, charge]`, `event: after_roll`) — kein Datenbau | S | ~12k | Gate | Sonnet | `src/gameMechanic/movementPhase.py`, `src/gameMechanic/chargephase.py` |
| 3 | „Start Game"-Button direkt unter die First-Player-Toggle-Buttons verschieben (vor die `_render_round_choice_assignment`-Schleife, nicht danach) | XS–S | ~8k | Gate | Haiku | `src/uiLayout/gameActionsArea.py::_render_setup` (Z. 225–262) |
| 4 | **Doku-Nachzug (Drift-Befund, s. u.):** `design_system.md` §6.3 + `backlog.md` §2 Paket-2-Text + `next_session.md` ▶2 präzisieren: Tisch-Wurf-Eingabe-Baustein gilt nur, wo Werte bereits erfasst werden (Damage/Psychic/Deny/Morale-Kasualties); Advance/Charge = nur Re-Roll-Angebot ohne Werterfassung; §6.3-Advance-Mockup ersetzen/korrigieren | XS | ~5k | Gate | Haiku | `docs/spec/design_system.md`, `docs/goals/backlog.md`, `.claude/tasks/next_session.md` |

**Reihenfolge:** 1a → 1b → 2 → 3 → 4 (2/3/4 unabhängig voneinander, bei Bedarf umsortierbar).
Jeder Brief einzeln durchs Freigabe-Gate (§6.6); jeder Brief nennt den Handoff-Marker, falls er
nach `docs/handoff/` schreibt.

### Doku-Drift-Prüfung (Koordinator-Auftrag) — DRIFT BESTÄTIGT

- `design_system.md` §6.3 listet explizit „Gilt für: **Advance-Wurf, Charge-Wurf**, Morale-Test,
  Manifest/Deny, Damage-Block" und zeigt als Mockup ein `Advance roll (D6): [ 3 ]`-Eingabefeld —
  widerspricht der Entscheidung direkt.
- `backlog.md` §2 Paket-2-Zeile „Tisch-Wurf-Baustein + Command Re-Roll bei Advance-/Charge-Wurf"
  und `next_session.md` ▶2 „Tisch-Wurf-Eingabe-Baustein + Command Re-Roll für Advance/Charge" —
  beide implizieren den Baustein für Advance/Charge.
- → Auftrag 4 (XS) definiert, NICHT selbst umgeschrieben.

### Test-Strategie

- 1a: `go_card.py`-HTML-Builder ist Streamlit-frei → volle Coverage, Tests für alle 4 Zustände +
  Voll-/Kompaktform (analog `tests/uiLayout/test_badges.py`). Streamlit-Wrapper (Buttons,
  Akkordeon) ist Render-Code → manuell verifiziert.
- 1b: bestehende `tests/uiLayout/test_game_protocoll.py` als Regressionsbasis, HTML-Output der
  neuen Karte in der Liste ergänzen wo machbar; Render-Teil manuell.
- 2: keine neue Business-Logik (`render_inline_command_reroll`, `reactive_stratagems_for`,
  `stratagem_visibility` sind bestehend + getestet); `*Phase.py` ist Render-Code → Verdrahtung
  per grep belegen + manuell prüfen; bestehende Suite bleibt grün.
- 3: reines Render-Reordering → kein neuer Unit-Test, manuelle Prüfung + Suite grün.
- 4: Doku-Gates (`pytest tests/docs/ --no-cov -q`) müssen grün bleiben (next_session.md
  Zeilendecke 120 beachten).
- **Pro Brief genau EINE Vollsuite am Ende, im Vordergrund** (`pytest --tb=short`,
  `run_in_background` VERBOTEN); während der Entwicklung gezielte Tests (`pytest <datei> -q --no-cov`).

### Manuelle UI-Prüfpunkte (PFLICHT vor „fertig", Render-Code ist coverage-frei)

- [ ] 1a/1b: Karte zeigt in der zentralen Liste `bereit` (Gold-Rahmen), `verwendet` (Undo-Button,
      `+N CP`), `gesperrt` (gedimmt, Grund als Suffix) korrekt; Regeltext-Akkordeon bleibt nach
      Rerun (Button-Klick/Undo) **zu**, außer der Nutzer öffnet ihn aktiv erneut.
- [ ] 2 (Advance): nach Klick auf „Advance" erscheint `↻ Command Re-Roll (1 CP)`; Klick bucht
      1 CP (GameHeader), Angebot verschwindet danach (used this phase); bei 0 CP erscheint es
      gar nicht (Pull-not-Push, nicht ausgegraut). KEIN Wurf-/Zahlenfeld sichtbar.
- [ ] 2 (Charge): Angebot erscheint bei gewähltem Charge-Ziel neben Successful/Failed; Buchung
      wie oben; „Charge Successful/Failed"-Verhalten fachlich völlig unverändert.
- [ ] 3: Start-Game-Button erscheint direkt unter den beiden „X goes first"-Buttons; Spiel
      startet weiterhin korrekt, Round-Choice-Zuweisung darunter bleibt bedienbar.

## Befunde (Checkbox-Sync, unverändert aus Erstentwurf)

- Kein Stale-Check: `next_session.md` S131-Stand deckt sich mit `git log --oneline -25`
  (`e3d7753`, `a230c2c`, `2e3aa98`, `b5c774b`); `ziel7.md` §0-Haken mit Commit-Hashes belegt.
- `backlog.md` §2 nutzt 🟢/🔲-Marker, keine `[x]`-Checkboxen — nichts stale.
- `docs/handoff/Stakeholder_Beobachtungen.md` NICHT verändert (nur gelesen).

## Offene Punkte (aus `next_session.md` unverändert mitgeführt)

S130-GO-Verifikation + Necron-Roster-Check verschoben auf nach dem UI-Umbau (Paket 7-Kandidat);
Scroll-Render iframe→parent coverage-frei → in die manuelle Checkliste nach Umbau; `before_battle`-Fix
Teil von Paket 3 (S133); 037 Docker-Smoke vor Merge; Deny-Caption-Prüfung blockiert (braucht Roster
mit Deny-Einheit); Direction-Entscheide (Ziel9/Deployment/Mission-Scoring) → Backlog §5, weiter
vertagt bis Ziel7 Stufe B/C.

## Nicht Teil dieser Session

**Beobachtung ②** (Spielvorbereitungsscreen überarbeiten) bleibt unkonkret — kein Executor-Auftrag,
erst ein Mockup-/Refinement-Schritt mit dem Stakeholder (Backlog §2).
