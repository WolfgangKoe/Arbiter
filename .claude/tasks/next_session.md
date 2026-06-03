# Startprompt — Nächste Session
<!-- Kanonische Planung. Nicht durch separate Plan-Dateien ersetzen — immer hier ergänzen. -->

## ⚠️ Session-Regeln (immer beachten)

**Zu Beginn jeder Session lesen:**
- `CLAUDE.md` — Workflow, Freigabe-Pflicht, Code-Qualität, Branch-Strategie
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
| Ziel 1–5 — Grundgerüst, Phasen, Setup, Daten | ✅ fertig (2026-06-03) |
| **Ziel 6 — UI-Overhaul, ArmyCard, Attackensequenz** | ⬜ Spec fertig — Implementierung steht aus |
| Ziel 7 — Crusade-Erweiterung | ⬜ |
| Ziel 8 — Wahapedia Faction Fetcher | ⬜ |

Details: `docs/goals/index.md`

---

## Nächste Schritte

### Ziel 6 starten — empfohlene Reihenfolge

**6a zuerst** (klein, isoliert, sofort sichtbar):
1. `src/uiLayout/gameHeader.py`: VP/CP inline (eine Zeile), `← ↺ →` in eine Row, Badges doppelt so groß
2. Visuell prüfen (Browser)

**Dann 6g** (unabhängig, kein Daten-Impact):
3. `gameMechanic/game_log.py`: Log-Format strukturieren, `archive_and_reset_log()` einbauen
4. `game_state.py`: `reset_game()` ruft Archive auf
5. `uiLayout/setupScreen.py`: Archiv-UI (Liste, Download, Löschen)

**Dann 6b** (Voraussetzung für 6c/6d/6e):
6. `faction_dir_for()` Bug fixen (Default auf `"necrons"`)
7. armyCard: Fraktions-Keywords als Badges, generische Triggered-Abilities
8. Command Protocol aus `gameProtocoll.py` in armyCard verlagern
9. Orks WAAAGH prüfen / ergänzen

**Dann 6c → 6d → 6e → 6f** (aufeinander aufbauend):
10. Stratagems Default-Tab; Modifier-Datenstruktur anlegen
11. Attackensequenz simultan rendern (Modifier-Stack, FNP konditional)
12. Fähigkeiten aller Quellen in Phasen einbinden; CP-Doppelvergabe-Bug fixen
13. Ability-Badges auf unitCard

Vollständige Task-Listen in `docs/goals/ziel6.md`.

---

## Bekannte offene Lücken

| Lücke | Beschreibung | Priorität |
|-------|-------------|-----------|
| Adeptus Custodes | Nur Placeholder-Dateien — kein spielbarer Katalog | Nach Ziel 8 |
| CP Doppelvergabe | Befehlsphase kann mehrfach CP vergeben (zurück/vor wechseln) | Ziel 6e |
| Living Metal Bug | Erscheint bei falschen Fraktionen wegen `faction_dir` Default | Ziel 6b |

---

## Wichtige Constraints

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- Setup-Buttons: `player_slots` verwenden, NICHT `first_player`/`second_player`
- dev-Branch — kein direktes Committen auf main
- **Keywords immer `UPPERCASE` in YAML** — Checks via `unit.has_keyword()`
- Weapon-Zugriff mit Dual-Profile: `w.for_phase(use_melee)` — nicht `w.is_melee`
- Session-State Unit-Keys: `p1_units` / `p2_units` mit `#N`-Suffix für Duplikate
- Weapon strength: `_parse_strength()` in `_common.py` — nie direkt `int(profile.strength)`
- Fähigkeiten: **nie** auf Fraktionsnamen hardcoden — immer generisch über Keywords/YAML

### State-Key System

Mehrfach-Units gleichen Typs werden mit `#N`-Suffix disambiguiert:
- Erstes Vorkommen: `wh40k_9e.necrons.unit.warriors`
- Zweites Vorkommen: `wh40k_9e.necrons.unit.warriors#1`

`unit_id_from_state_key(key)` → echte `unit.id`.
`lookup(faction, uid)` in `_common.py` versteht State-Keys.

### Ziel-6-Datenstrukturen (neu in dieser Session definiert)

**`active_modifiers`** (Session-State, definiert in 6e):
```python
{
  "unit_key": str,       # betroffene Einheit (State-Key)
  "source": str,         # z.B. "Protokoll: Methodische Vernichtung"
  "effect": {...},       # modifier-spezifisch
  "expires_at_phase": str | None,
  "expires_at_round": int | None,
}
```

**Game-Log-Format** (strukturierte JSON, definiert in 6g):
```json
{
  "game_id": "<ISO-Timestamp>",
  "players": {"first": "...", "second": "..."},
  "rounds": [{"round": 1, "phases": [{"phase": "...", "events": [...]}]}],
  "result": {"winner": "...", "vp": {...}}
}
```
Events mit `attacker_unit`, `target_unit`, `target_destroyed` vorbereitet für Crusade (Ziel 7).

### Streamlit 1.57 — CSS-Selektoren

Vor dem Schreiben von CSS-Overrides immer JS-Source prüfen — Emotion-Klassen ändern sich zwischen Versionen.

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| NumberInput Step-Buttons | `[data-testid="stNumberInputStepUp"]`, `[data-testid="stNumberInputStepDown"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
| Selectbox | `.stSelectbox [data-baseweb="select"] > div` |
