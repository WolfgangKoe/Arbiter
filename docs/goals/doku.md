# Doku-Bereinigung ⬜ (parallel zu Ziel 5)

Befund des Doku-Audits (2026-05-30) — folgende Inkonsistenzen beheben:

## architecture.md

- [ ] `protocol.py` → `game_log.py` (umbenannt in Ziel 2)
- [ ] `state.py` → `game_state.py` (umbenannt in Ziel 2)
- [ ] `"current_phase"` → `"phase"` im session_state-Schema
- [ ] Phase-Stubs (Movement, Charge, Fight, Morale) als fertig markieren — alle in Ziel 4 implementiert
- [ ] `keyword.py` TBD-Notiz entfernen — Datei wurde nie erstellt und nicht gebraucht

## processes.md

- [ ] "Stub-Phasen (Ziel 3)"-Notiz entfernen — alle Phasen fertig
- [ ] P-13 — Charge Phase (Flowchart)
- [ ] P-14 — Fight Phase (Flowchart)
- [ ] P-15 — Morale Phase (Flowchart)

## docs/work/

- [ ] `necrons.md` + `orks.md` — als veraltet markieren oder entfernen (rohe BS-Exports, durch Ziel 5b ersetzt)

## Neue Spec-Dateien (werden in Ziel 5a angelegt)

- [ ] `docs/spec/army_builder.md` — Roster-Format, Katalog-Schema, Loader-Vertrag
- [ ] `docs/spec/setup.md` — Spielmodi-Regeln (Matched/Open/Crusade)
