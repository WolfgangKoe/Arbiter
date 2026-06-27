# Ziel 2 — Command Phase ✅

Ziel: Erste vollständige Phase als Blaupause für alle weiteren.

**Abgeschlossen.** Dateinamen weichen leicht vom Plan ab (state.py → game_state.py, protocol.py → game_log.py).

- [x] `gameMechanic/game_state.py` — `init_state`, `reset_game`, `next_phase`, `PHASES`, Unit-Loader
- [x] `gameMechanic/game_log.py` — `log_action`, `clear_game_log`
- [x] `gameMechanic/unit_mutations.py` — alle Unit/VP/CP-Mutations
- [x] `gameMechanic/commandPhase.py` — CP-Grant (1×/Phase), Living Metal, MWBD (CORE-Unit-Auswahl), Resurrection Orb (Unit-Auswahl + Heal-Buttons)
- [x] `uiLayout/gameActionsArea.py` — Layout vollständig, "Start Game"-Button in Setup
- [x] Select-Logik in `unitCard.py` vollständig verdrahtet
- [x] `gameProtocoll` — Battle-Log mit Expander nach Round/Phase
- [x] Tests für commandPhase
