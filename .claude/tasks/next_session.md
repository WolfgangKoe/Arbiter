# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — Projektziele mit Detailchecklisten
3. `docs/rules/schlachtrunde.md` — Regelreferenz
4. `src/models.py` — Datenmodelle, PHASES
5. `src/engine.py` — Spiellogik, State-Management
6. `src/ui.py` — Einheitenkarten, Zentralbereich, Phasen-Renderer

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`

```
src/          ← Streamlit-App (app.py, models.py, engine.py, ui.py)
data/         ← YAML-Rohdaten, log/game_log.json
docs/
  goals.md              ← Projektziele
  rules/
    schlachtrunde.md    ← WH40k 9E Grundregeln (bindend)
```

**App-UI und spielbezogene Begriffe: Englisch.**
Austausch mit dem Nutzer: Deutsch.

---

## Aktueller Stand der Ziele

| Ziel | Beschreibung | Status |
|------|-------------|--------|
| Ziel 1 | Grundstruktur & Layout | ✅ fertig |
| Ziel 2 | Einheitenstatus (Wundverwaltung) | ✅ fertig |
| Ziel 3 | Durchstich (Setup + State-Modell + Phasenstruktur) | 🔧 Durchstich fertig, Korrekturen nötig |
| — | Armeelisten aus YAML laden | ⬜ nach Ziel 3 |
| — | Spielende & Auswertung | ⬜ offen |

---

## Was in der letzten Session umgesetzt wurde

**Ziel 3 — Erster Durchstich implementiert (Commit: `2f805b5`):**

- `PHASES` um `("Setup", "setup")` an Index 0 erweitert
- `unit_state()` bekommt 5 neue Felder: `movement_status`, `in_melee`, `in_reserve`, `deployment`, `acted_this_phase`, `lost_models_this_turn`
- `engine.py`: neue Hilfsfunktionen (`set_deployment`, `set_movement_status`, `set_in_melee`, `log_action`), `next_phase()` überarbeitet (Setup → Command, Moralphase → Spielerwechsel + State-Reset)
- `ui.py`: `unit_card()` mit permanenter + dynamischer Sektion, Select/Target-Buttons; alle 8 Phase-Renderer mit 3-stufigem Zentralbereich; JSON-Aktionslog in `data/log/game_log.json`

---

## Bekannte Fehler & offene Punkte (Priorität: nächste Session)

### 🔴 BUG 1: Seitenleisten wechseln mit aktivem Spieler (falsch!)

**Problem:** `main()` zeigt den `active`-Spieler immer links — das führt dazu, dass die Seitenleisten pro Halbrunde wechseln. CP/VP-Anzeige im Header ebenfalls betroffen.

**Gewünschtes Verhalten:**
- Seitenleisten sind fest auf den Startspieler gebunden (aus Setup-Wahl)
- Links = immer Startspieler (z.B. Necrons, wenn so gewählt)
- Rechts = immer zweiter Spieler
- VP/CP im Header entsprechend auch fest
- `active` bleibt im State für die Spiellogik (welche Einheiten wählbar sind), beeinflusst aber **nicht** das Layout

**Fix in `engine.py`:**
- `init_state()` bekommt `st.session_state.first_player = "Necrons"` und `st.session_state.second_player = "Orks"`
- In `phase_setup()`: wenn Startspieler gewählt → `first_player` und `second_player` setzen
- `active` wird weiterhin von `next_phase()` gewechselt

**Fix in `ui.py` / `main()`:**
- Ersetze `left_faction = active` durch `left_faction = st.session_state.first_player`
- `right_faction = st.session_state.second_player`
- Score-Gruppe links = `first_player`, rechts = `second_player`
- Nur die Select/Target-Buttons und Aktions-Buttons reagieren auf `active`

---

### 🔴 BUG 2: Deployment-Default falsch

**Problem:** `_unit_state()` setzt `deployment: "normal"` und `movement_status: "normal"`. Der Nutzer möchte **`"stationary"`** als Default für alle Einheiten (vor der Bewegungsphase sind alle stationär).

**Fix in `engine.py` / `_unit_state()`:**
```python
"deployment": "stationary",   # war "normal"
"movement_status": "stationary",  # war "normal"
```

---

### 🟡 FEHLT: `charged_this_turn`-Status

**Problem:** Nach einer erfolgreichen Angriffsphase muss bekannt sein, welche Einheiten gestürmt haben — sie kämpfen in der Nahkampfphase als erste. Dafür fehlt ein dedizierten Flag.

**Zu tun:**
- `_unit_state()` bekommt `"charged_this_turn": False`
- `set_in_melee()` bzw. der Charge-Success-Button in `_central_charge_actions()` setzt `state["charged_this_turn"] = True`
- `_reset_turn_state()` setzt `charged_this_turn` zurück auf `False`
- Badge `CHARGED` zu `_BADGE_COLORS` hinzufügen
- In `_state_badges_html()`: wenn `charged_this_turn`, Badge anzeigen
- In `_dynamic_fight()` und `_central_fight_actions()`: Einheiten mit `charged_this_turn` klar als "fights first" kennzeichnen

---

### 🟡 FEHLT: Reserve-Einheiten ab Runde 2

**Problem:** Logik für "Reserve erst ab Runde 2" ist nur in `_dynamic_movement()` rudimentär drin. Fehlt an:
- Angriffsphase: Reserve-Einheiten können nicht angreifen
- Fernkampf: Reserve-Einheiten können nicht schießen
- Alle Phasen: Reserve-Einheiten sollten `in_reserve: True` im Badge zeigen und den Select-Button deaktivieren

**Fix:** In `unit_card()` — wenn `in_reserve and round == 1`: Select-Button deaktiviert, alle dynamischen Sektionen zeigen "In Reserve — arrives Round 2". Ab Runde 2: Reserve-Einheit kann normal aufgestellt werden (Button "Deploy" in Bewegungsphase → setzt `in_reserve = False`, `deployment = "normal"`).

---

### 🟡 FEHLT: Setup-Zusammenfassung im Zentralbereich

Nach Ende der Setup-Phase soll eine eingeklappte Zusammenfassung im Zentralbereich jederzeit einsehbar sein:
- Startspieler
- Deployment-Status aller Einheiten

Einfachste Umsetzung: `st.expander("Setup Summary", expanded=False)` am Ende jedes Phase-Renderers.

---

### 🔵 DISKUSSIONSPUNKT: Einheitenkarte Layout

Der Nutzer möchte besprechen, wie die Profilwerte (M/T/Sv/W/++/Ld/OC) in der Karte organisiert sein sollen. Derzeit immer im permanenten Block sichtbar. Der Nutzer will dazu etwas aufmalen — **kein Code-Change ohne seine Vorlage!**

---

## Empfohlene Reihenfolge für die nächste Session

1. **BUG 1 fixem** (Seitenleisten fest, VP/CP fest) — `engine.py` + `ui.py` (~30 Zeilen)
2. **BUG 2 fixen** (Deployment-Default Stationary) — `engine.py` (2 Zeilen)
3. **`charged_this_turn`** einbauen — `engine.py` + `ui.py`
4. **Reserve-Logik vervollständigen** — `ui.py`
5. **Setup-Zusammenfassung** — `ui.py`
6. Erst danach: Diskussion über Einheitenkarte-Layout mit Nutzer-Vorlage

---

## Offene Designfragen

1. **Einheitenkarte Layout**: Nutzer hat noch kein Bild gezeigt. Warten auf seine Vorlage.
2. **Würfeln**: Noch komplett manuell (Nutzer würfelt physisch). Soll optional hinzukommen (nach Ziel 3).
3. **Modulstruktur**: `engine.py` schreibt direkt in `st.session_state` → Unit-Tests nicht möglich. Nach Ziel 3 als eigenständiger Schritt.
