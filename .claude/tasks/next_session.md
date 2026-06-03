# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, **Unklarheiten IMMER zuerst fragen**, Branch-Strategie
- `docs/goals/ziel6.md` — aktueller Ziel-6-Stand: Spec, Checkliste, offene Punkte

**Am Ende jeder Session:**
- `docs/goals/ziel6.md` aktualisieren: Checkboxen abhaken, neue Erkenntnisse ergänzen, nächste Schritte fortschreiben

---

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Aktueller Status

| Ziel | Status |
|------|--------|
| Ziel 1–5 — Grundgerüst, Phasen, Setup, Daten | ✅ fertig |
| **Ziel 6a — gameHeader Redesign** | ✅ fertig (2026-06-03) |
| **Ziel 6b — armyCard generisches Fähigkeitssystem** | ✅ fertig (2026-06-03) |
| **Ziel 6c — Stratagems Default-Tab, Modifier-Export** | ✅ fertig (2026-06-03) |
| **Ziel 6g — Game Log Archiv** | ⬜ nächster Schritt |
| **Ziel 6d — Attackensequenz simultan** | ⬜ (nach 6g) |
| **Ziel 6e — Fähigkeiten-Integration alle Phasen** | ⬜ |
| **Ziel 6f — Ability-Badges unitCard** | ⬜ |
| Ziel 7 — Crusade-Erweiterung | ⬜ |
| Ziel 8 — Wahapedia Faction Fetcher | ⬜ |

Details: `docs/goals/index.md`

---

## Was wurde in dieser Session gemacht (2026-06-03)

### 6a — gameHeader Redesign ✅
- 4-Zeilen-Layout: Runde / Phase·Spieler / Scores+Badges / Navigation
- VP und CP Label gleich groß wie Zahl (`4.5rem bold`)
- `← ↺ →` in einer Zeile, zentriert
- Phase-Badges in Zeile 3 Mitte integriert (nicht mehr unterhalb)

### 6b — armyCard generisches Fähigkeitssystem ✅
- `faction_dir_for()`: kein `"necrons"`-Default mehr — KeyError wenn nicht initialisiert
- Command Protocol UI aus `commandPhase.py` herausgelöst → **einziger Einstiegspunkt ist jetzt armyCard**
- Nur Necrons haben Protokolle (generisch via `load_command_protocols()` — leere Liste = kein UI)
- Interaktive Auswahl (Befehlsphase) vs. Read-only-Status (alle anderen Phasen) in armyCard
- `_render_necron_protocols()` aus gameProtocoll.py entfernt

### 6c — Stratagems Default-Tab, Modifier-Export ✅
- Stratagems sind jetzt erster Tab in gameProtocoll (war Command Protocol)
- `StratagemModifier` Dataclass in `stratagem.py`; optionales `modifier`-Feld auf `Stratagem`
- Loader parst `modifier`-Block aus YAML
- `active_modifiers: list[dict]` im Session-State (init + reset + cleanup bei Phasenwechsel)
- Bei Stratagem-Nutzung: Modifier wird in `active_modifiers` geschrieben
- Modifier-Daten in YAML:
  - Necrons: `disruption_fields` (+1 wound, attacker), `whirling_onslaught` (-1 wound, defender), `methodical_destruction` (+1 hit, attacker)
  - Orks: `hit_em_harder` (+1 damage, attacker), `tough_as_squig_hide` (-1 wound, defender), `wreckaz` (+1 wound, attacker)

### VP-Bug-Fix ✅
- Siegpunkte-Vergabe nur für den **aktiven** Spieler (Buttons)
- Inaktiver Spieler: nur read-only Anzeige mit `(inactive — no scoring)`
- Datei: `src/uiLayout/gameActionsArea.py`

### Workflow-Verbesserung ✅
- CLAUDE.md: neuer Abschnitt „Bei Unklarheiten IMMER zuerst fragen (PFLICHT)"
- Memory gespeichert: `feedback_ask_before_assuming_scope.md`

---

## Nächste Schritte

### 6g — Game Log (empfohlen als nächstes, unabhängig)
1. `gameMechanic/game_log.py`: Log-Format auf strukturierte JSON umstellen (game_id, players, rounds, phases, events)
2. `gameMechanic/game_log.py`: `archive_and_reset_log()` — verschiebt Log nach `data/log/archive/<game_id>.json`
3. `gameMechanic/game_state.py`: `reset_game()` ruft `archive_and_reset_log()` auf
4. `uiLayout/setupScreen.py`: Archiv-Verwaltungs-Sektion (Liste, Download, Löschen)

### 6d — Attackensequenz simultan (nach 6c/6g)
5. `gameMechanic/combat.py`: `resolve_attack_modifiers()` — Modifier-Stack aus `active_modifiers`
6. `gameMechanic/combat.py`: `resolve_save()` und `resolve_fnp()`
7. Attack-Sequenz-Renderer: Treffer/Verwundung links, Save/FNP/Schaden rechts, alles gleichzeitig

### 6e → 6f (danach)
8. CP-Doppelvergabe-Bug fixen
9. Ability-Engine alle Quellen einbinden
10. Ability-Badges auf unitCard

Vollständige Task-Listen in `docs/goals/ziel6.md`.

---

## Bekannte offene Lücken

| Lücke | Beschreibung | Priorität |
|-------|-------------|-----------|
| Adeptus Custodes | Nur Placeholder-Dateien — kein spielbarer Katalog | Nach Ziel 8 |
| CP Doppelvergabe | Befehlsphase kann mehrfach CP vergeben | Ziel 6e |

---

## Wichtige Constraints

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Bei Unklarheiten ZUERST FRAGEN** — besonders bei Scope und „verlagern"-Aufgaben (siehe CLAUDE.md)
- Seitenleisten IMMER fest: first_player links, second_player rechts
- Setup-Buttons: `player_slots` verwenden, NICHT `first_player`/`second_player`
- dev-Branch — kein direktes Committen auf main
- **Keywords immer `UPPERCASE` in YAML** — Checks via `unit.has_keyword()`
- Weapon-Zugriff mit Dual-Profile: `w.for_phase(use_melee)` — nicht `w.is_melee`
- Session-State Unit-Keys: `p1_units` / `p2_units` mit `#N`-Suffix für Duplikate
- Weapon strength: `_parse_strength()` in `_common.py` — nie direkt `int(profile.strength)`
- Fähigkeiten: **nie** auf Fraktionsnamen hardcoden — immer generisch über Keywords/YAML
- **Command Protocols: NUR NECRONS** — armyCard ist einziger Einstiegspunkt, commandPhase hat keinen Aufruf mehr

### State-Key System

Mehrfach-Units gleichen Typs werden mit `#N`-Suffix disambiguiert:
- Erstes Vorkommen: `wh40k_9e.necrons.unit.warriors`
- Zweites Vorkommen: `wh40k_9e.necrons.unit.warriors#1`

`unit_id_from_state_key(key)` → echte `unit.id`.
`lookup(faction, uid)` in `_common.py` versteht State-Keys.

### Ziel-6-Datenstrukturen (implementiert in 6c)

**`active_modifiers`** (Session-State, init in `game_state.py`):
```python
{
  "unit_key": str | None,    # betroffene Einheit (State-Key); None = armeeweit
  "source": str,             # z.B. "Methodical Destruction"
  "effect": {
    "roll_type": str,        # "hit" | "wound" | "save" | "fnp" | "damage"
    "value": int,            # +1 oder -1
    "target": str,           # "attacker" | "defender"
    "phase": str,            # Phase in der der Modifier gilt
  },
  "expires_at_phase": str | None,
  "expires_at_round": int | None,
}
```

**`StratagemModifier`** (Dataclass in `gameObjects/stratagem.py`):
```python
roll_type: str        # hit | wound | save | fnp | charge | damage
value: int            # positiv = Bonus, negativ = Malus
target: str           # attacker | defender
expires_at: str       # phase_end | turn_end
source_label: str     # Anzeige-Label im Modifier-Stack
phase: str | None     # Override für angewandte Phase
```

**Game-Log-Format** (strukturierte JSON, definiert für 6g):
```json
{
  "game_id": "<ISO-Timestamp>",
  "players": {"first": "...", "second": "..."},
  "rounds": [{"round": 1, "phases": [{"phase": "...", "events": [...]}]}],
  "result": {"winner": "...", "vp": {...}}
}
```

### Streamlit 1.57 — CSS-Selektoren

Vor dem Schreiben von CSS-Overrides immer JS-Source prüfen — Emotion-Klassen ändern sich zwischen Versionen.

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |
