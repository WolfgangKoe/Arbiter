# Startprompt — Nächste Session

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — aktuelle Projektziele
3. `src/models.py` — Datenmodelle, PHASES
4. `src/engine.py` — Spiellogik, State-Management
5. `src/ui.py` — UI-Komponenten (~1000 Zeilen, wird refactored)

---

## Kontext

**Arbiter** — WH40k 9th Edition Battle Tracker in Streamlit.  
Starten: `streamlit run src/app.py`

```
src/          ← Streamlit-App (app.py, models.py, engine.py, ui.py)
data/
  wh40k_9e/  ← YAML-Katalog (necrons/, orks/ — Einheiten + Waffen)
  log/        ← game_log.json (Aktionsprotokoll)
docs/
  goals.md              ← Projektziele (immer lesen!)
  rules/
    schlachtrunde.md    ← WH40k 9E Grundregeln (bindend)
```

**App-UI und spielbezogene Begriffe: Englisch.**  
Austausch mit dem Nutzer: Deutsch.

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Grundstruktur & Layout | ✅ fertig |
| Einheitenstatus (Wundverwaltung) | ✅ fertig |
| Durchstich (Phasenstruktur, State, Zentralbereich) | ✅ fertig |
| UI Refactoring & Layout | ⏳ wartet auf Layout-Bilder vom Nutzer |
| Army Abstraction | ⬜ bereit zum Starten |
| Phase Logic | ⬜ nach Army Abstraction |

---

## Was in der letzten Session umgesetzt wurde

**Bug-Fixes & Ergänzungen (Commit `0d517ed`):**
- Seitenleisten fest auf `first_player`/`second_player` — kein Swap mehr mit `active`
- Deployment- und Movement-Status-Default: `"stationary"` statt `"normal"`
- `charged_this_turn`-Flag: CHARGED-Badge, "Fights first"-Anzeige in Nahkampfphase
- Reserve-Logik vollständig: Select/Target deaktiviert, Deploy-Button ab Runde 2
- Setup-Summary-Expander in allen Kampfphasen sichtbar

**Ziele überarbeitet (Commit `a27e77a`):**
- `docs/goals.md` neu strukturiert: UI Refactoring, Army Abstraction, Phase Logic

---

## Nächster konkreter Schritt

**Zwei parallele Einstiegspunkte — je nachdem was der Nutzer mitbringt:**

### Option A — Nutzer bringt Layout-Bilder
→ Mit **UI Refactoring** starten:
1. `ui.py` strukturell aufsplitten (kein Behavior-Change):
   - `ui/header.py` — Top-Bar, VP/CP, Phase-Stepper
   - `ui/unit_card.py` — Einheitenkachel
   - `ui/central/` — Phase-Renderer je Datei
2. Dann UX-Anpassungen anhand der Bilder einbauen

### Option B — Noch keine Bilder
→ Mit **Army Abstraction** starten:
1. YAML-Loader schreiben: `data/wh40k_9e/necrons/units.yaml` + `weapons.yaml` einlesen, Referenzen auflösen
2. `models.py` auf geladene Daten umstellen (hardcodierte Listen raus)
3. `engine.py` armeeneutral machen (keine `"necron_units"`/`"ork_units"`-Keys mehr)
4. Keyword-Dispatcher: zentrale Stelle für Keyword → Phasenverhalten

---

## Offene Designfragen

1. **Einheitenkachel-Layout** — Nutzer hat noch kein Bild geliefert. Kein Code-Change ohne Vorlage.
2. **Army Builder UI** — Wie wählt der Spieler Einheiten für eine Partie? Details noch offen, wird im Zuge von Army Abstraction geklärt.
3. **Psiphase** — bewusst zurückgestellt. Läuft mit bis es gebraucht wird.
