# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**, Branch-Strategie
- `docs/goals/ziel6.md` — aktueller Ziel-6-Stand

**Am Ende jeder Session:**
- `docs/goals/ziel6.md` aktualisieren: Checkboxen abhaken, neue Erkenntnisse ergänzen

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Stand (nach Session 14, 2026-06-05)

### Was funktioniert ✅
- Ziel 1–5 (Grundgerüst, Phasen, Setup, Daten) — vollständig
- Ziel 6a–6e, 6g, 6h — committed
- 6d-v2 Attackensequenz: Deklaration + Resolution-Tabs, Wound-Tabelle, RP-Block, Cover-Dropdown
- 461 Tests grün

### Was diese Session erledigt wurde ✅
- Architekturanalyse: alle hardcodierten Fraktionsreferenzen inventarisiert (→ ziel6.md 6h)
- Command Protocol Bugs 1–3 analysiert und dokumentiert (→ ziel6.md 6e)
- `auto_round_1` aus `faction_abilities.yaml` entfernt (alle 6 Protokolle)
- 10 fehlende Command-/Fight-Phase-Abilities für Necrons ergänzt (unit_abilities.yaml):
  Royal Warden (Adaptive Strategy), Catacomb Command Barge (MWBD), Chronomancer (Chronometron),
  Orikan (Master Chronomancer + Stars Are Right), Lokhust Lord + Skorpekh Lord (United in Destruction),
  Canoptek Reanimator (Nanoscarab Beam), Canoptek Spyder (Scarab Hive), Ghost Ark (Repair Barge)

---

## Offene Aufgaben (priorisiert)

### AUFGABE 1 — Datengrundlage vollständig fixen (laufend)

**Schritt 1 (Necrons) — teilweise erledigt:**
- 10 Abilities ergänzt ✅
- Noch offen: Waffen-Profile prüfen (Chronomancer Aeonstave/Entropic Lance/Chronotendrils,
  Canoptek Doomstalker Doomsday Blaster, Tesseract Ark C'tan-Waffen usw.)
- Noch offen: Einheiten-Stats für beschädigte Wound-Tracks (Silent King, Triarch Stalker,
  Canoptek Doomstalker etc.) auf Korrektheit prüfen

**Schritt 2 (Orks) — noch nicht angefangen:**
- unit_abilities.yaml gegen `docs/work/wahapedia_orks/units_all.txt` prüfen

**Schritt 3 (Custodes) — noch nicht angefangen:**
- unit_abilities.yaml gegen `docs/work/wahapedia_adeptus_custodes/units_all.txt` prüfen

---

### AUFGABE 2 — Hardcoding aus gameMechanics entfernen (nächster großer Schritt)

Vollständiges Inventar in `docs/goals/ziel6.md` (Abschnitt 6h). Kernpunkte:
- `_OVERLORD_ID` aus commandPhase.py + unitCard.py → Resurrection Orb über wargear.yaml treiben
- `is_necron_faction()` aus game_state.py entfernen
- `resurrection_orb_used` aus init_state raus
- `waaagh_state` aus _common.py Attacken-Resolver raus
- `auto_round_1`-Feld aus command_protocol.py Dataclass + gameActionsArea.py + commandPhase.py entfernen
  (YAML ist bereits sauber — Code hängt noch dran)

**Voraussetzung für diesen Schritt:** Daten (AUFGABE 1) müssen für alle aktiven Fraktionen stabil sein.

---

### AUFGABE 3 — Command Protocol Bugs 2+3 (wartet auf AUFGABE 2)

- Bug 2: 6. Protokoll (immer aktiv) implementieren + eigene Direktiven-Wahl
- Bug 3: Dynastiebonus (beide Direktiven wenn Dynastieprotokoll) — braucht Dynastieinfo im Roster

---

### AUFGABE 4 — Command Protocols ✅ ERLEDIGT (58ebc0b)

---

## Weitere offene Punkte (nachrangig)

| Punkt | Priorität |
|---|---|
| Weapon-Ability-Badges (Tesla, Dakka) im Hit-Block | mittel |
| Stratagem Reset-Button (reaktive GOs rückgängig) | mittel |
| `once_per_battle` enforcement | niedrig |
| subfaction_affinity UI | niedrig |
| load_powers() verdrahten (Psychic Phase) | niedrig |

---

## Wichtige Constraints (unverändert)

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Planergänzung ≠ Freigabe** — Plan neu zeigen, nochmal warten
- **Kein Memory/Subagent/Skill ohne Freigabe**
- dev-Branch, kein direktes Committen auf main
- Seitenleisten: first_player links, second_player rechts (unveränderlich)
- Keywords immer `UPPERCASE` in YAML
- `_parse_strength()` für Waffenstärke, nie `int(strength)` direkt

---

## Historische Sessions (Kurzfassung)

| Session | Datum | Inhalt |
|---|---|---|
| 1–5 | 2026-06-03/04 | Grundgerüst, Datenkorrektur, Fähigkeitssystem |
| 6–7 | 2026-06-04 | GO-Daten vollständig, render_attack_form neu (2-Spalten) |
| 8 | 2026-06-04 | Design 6d-v2 abgestimmt |
| 9–10 | 2026-06-04 | 6d-v2 Kern implementiert (Deklaration + Resolution + RP) |
| 11 | 2026-06-04 | Bug-Fixes: Scenario-KeyError, shot/fought-Flags, apply_damage(resolved), Stratagems-Hint entfernt |
| 12 | 2026-06-04 | CLAUDE.md + Memory + settings.json bereinigt; Stratagem-Bugs analysiert; Wahapedia-Plan vorbereitet |
