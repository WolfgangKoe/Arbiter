# Doku-Bereinigung ⬜ (parallel zu Ziel 5)

Befund des Doku-Audits (2026-05-30) — folgende Inkonsistenzen beheben:

## architecture.md

- [x] `protocol.py` → `game_log.py` (umbenannt in Ziel 2)
- [x] `state.py` → `game_state.py` (umbenannt in Ziel 2)
- [x] `"current_phase"` → `"phase"` im session_state-Schema
- [x] Phase-Stubs (Movement, Charge, Fight, Morale) als fertig markieren — alle in Ziel 4 implementiert
- [x] `keyword.py` TBD-Notiz entfernen — Datei wurde nie erstellt und nicht gebraucht

## processes.md

- [x] "Stub-Phasen (Ziel 3)"-Notiz entfernen — alle Phasen fertig
- [x] P-13 — Charge Phase (Flowchart)
- [x] P-14 — Fight Phase (Flowchart)
- [x] P-15 — Morale Phase (Flowchart)

## docs/work/

- [x] `necrons.md` + `orks.md` — als veraltet markiert (rohe BS-Exports, durch Ziel 5b ersetzt)

## Neue Spec-Dateien (werden in Ziel 5a angelegt)

- [x] `docs/spec/army_builder.md` — Roster-Format, Katalog-Schema, Loader-Vertrag
- [x] `docs/spec/setup.md` — Spielmodi-Regeln (Matched/Open/Crusade)
