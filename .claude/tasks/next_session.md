# Startprompt — Nächste Session

## Kontext

Wir arbeiten an **Arbiter**, einem WH40k 9th Edition Battle Tracker in Streamlit.
Starten: `streamlit run src/app.py`

Projektstruktur:
```
src/          ← Streamlit-App (app.py, models.py, engine.py, ui.py)
backend/      ← Hexagonale Architektur für Datenblatt-Verwaltung (Crusade)
data/         ← YAML-Rohdaten (Waffen, Einheiten, Regeln)
docs/
  architecture.md       ← Modulstruktur, Datenfluss, Zielarchitektur
  goals.md              ← Projektziele (Ziel 1–7)
  rules/
    schlachtrunde.md    ← WH40k 9E Grundregeln (alle 7 Phasen, vollständig)
```

## Was in der letzten Session gemacht wurde

- `docs/rules/schlachtrunde.md` angelegt: vollständiger Regeltext der Schlachtrunde (alle 7 Phasen), formatiert als Markdown mit Tabellen, Beispielen (James-Beispiel, Schmetterschlag, DS-Beispiel, Schnelles Würfeln) und Regelreferenzen
- `docs/goals.md` neu strukturiert: 3-stufiger Plan für den Zentralbereich mit Verweisen auf `schlachtrunde.md` pro Phase:
  - **Ziel 3:** Durchstich — alle 7 Phasen zeigen Basisinformationen (kein Würfeln, nur Struktur)
  - **Ziel 4:** Phasenlogik — vollständige Würfel- und Regellogik pro Phase
  - **Ziel 5:** Armeeninteraktion — phasenübergreifende Mechaniken zwischen beiden Spielern

## Aktueller Stand der Ziele

| Ziel | Beschreibung | Status |
|------|-------------|--------|
| Ziel 1 | Grundstruktur & Layout | ✅ fertig |
| Ziel 2 | Einheitenstatus (−1W, Wundbalken, vernichtet) | ⬜ nicht begonnen |
| Ziel 3 | Zentralbereich Durchstich (alle Phasen) | ⬜ nicht begonnen |
| Ziel 4 | Zentralbereich Phasenlogik | ⬜ nicht begonnen |
| Ziel 5 | Zentralbereich Armeeninteraktion | ⬜ nicht begonnen |
| Ziel 6 | Armeelisten aus YAML laden | ⬜ nicht begonnen |
| Ziel 7 | Spielende & Auswertung | ⬜ nicht begonnen |

## Nächster konkreter Schritt

**Empfehlung:** Ziel 2 (Einheitenstatus) abschließen, bevor Ziel 3 (Durchstich) begonnen wird — die Einheitenkarten brauchen Wundstatus-Daten, auf die der Zentralbereich später zugreift.

Erster Task in Ziel 2:
- `−1W` / `+1W`-Buttons auf jeder Einheitenkarte in `ui.py`
- Wundbalken in `unit_card()` live aktualisieren
- Einheit als „vernichtet" markieren wenn LP = 0

Danach Ziel 3 starten mit der **Befehlsphase** (einfachste Phase, guter Einstieg):
- Regelreferenz lesen: `docs/rules/schlachtrunde.md#1-befehlsphase`
- `phase_command()` in `ui.py` füllen: BP-Anzeige + Button „+1 BP (Schlachtordnung)"

## Offene Designfragen

1. **HP-Anzeige bei Multi-Modell-Einheiten** (z. B. Skorpekh ×3 mit je 3 Wunden):
   - Option A: `8/10 Modelle` (Balken = Modelle)
   - Option B: `5/9 W` (Balken = Gesamtwunden)
   - Option C: `2 Modelle · letztes: 2/3 W` (kombiniert)
   → Noch keine Entscheidung. Vor Ziel 2 klären.

2. **Modulstruktur** (`todo.md`): `engine.py` schreibt direkt in `st.session_state`, was Unit-Tests verhindert. Refactoring zu pure functions (`apply_damage -> dict`) steht noch aus — kann parallel zu Ziel 3/4 oder als eigenständiger Schritt erfolgen.

## Wichtige Dateien zum Einlesen vor der Session

- `docs/goals.md` — vollständiger Zielplan
- `docs/rules/schlachtrunde.md` — Regeltext für die zu implementierende Phase
- `src/ui.py` — alle `phase_*`-Funktionen (aktuell leer/Platzhalter)
- `src/engine.py` — Spiellogik (Würfeln, State)
- `.claude/tasks/todo.md` — offene technische Tasks
