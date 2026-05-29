# Test-Szenarien

Alle Szenarien starten in Runde 1 mit Necrons als aktivem Spieler.
App starten: `streamlit run src/app.py`

| Phase | URL |
|-------|-----|
| Command | http://localhost:8501?scenario=command_phase |
| Movement | http://localhost:8501?scenario=movement_phase |
| Psychic | http://localhost:8501?scenario=psychic_phase |
| Shooting | http://localhost:8501?scenario=shooting_phase |
| Charge | http://localhost:8501?scenario=charge_phase |
| Fight | http://localhost:8501?scenario=fight_phase |
| Morale | http://localhost:8501?scenario=morale_phase |

## Hinweise

- **Charge**: Warriors ↔ Boyz in Melee, Overlord für Heroic Intervention verfügbar
- **Fight**: Warriors ↔ Boyz in Melee
- **Psychic**: Weirdboy (Orks) als Psyker verfügbar
- **Shooting**: Keine Einheiten in Melee, freies Schussfeld
- **Reset**: App neu laden ohne Query-Parameter → `http://localhost:8501`
