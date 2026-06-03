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

## Aktueller Status

| Ziel | Status |
|------|--------|
| Ziel 1–5 — Grundgerüst, Phasen, Setup, Daten | ✅ fertig |
| Ziel 6a — gameHeader Redesign | ✅ fertig |
| Ziel 6b — armyCard generisches Fähigkeitssystem | ✅ fertig |
| Ziel 6c — Stratagems Default-Tab, Modifier-Export | ✅ fertig |
| Ziel 6e (teilw.) — Command Phase generic abilities | ✅ committed (2026-06-03) |
| Ziel 6e (teilw.) — Command Protocols verdrahtet | ✅ committed (2026-06-03) |
| Ziel 6g (teilw.) — Game Log Archiv + Setup-UI | ✅ committed (2026-06-03) |
| **Ziel 6e — Protocol-Badge + sourced Modifier-Display** | ⬅ NÄCHSTER SCHRITT |
| Ziel 6g — set_log_players() in init_state() | ⬜ klein, schnell |
| Ziel 6d — Attackensequenz simultan | ⬜ |
| Ziel 6f — Ability-Badges unitCard | ⬜ |

---

## Was wurde zuletzt gemacht (2026-06-03, commits caec44c + 350b387)

### Session 1: Tests + Bugfixes

- **9 neue Tests** für `get_activated_command_abilities()`: Overlord→MWBD, Necron Lord→Lord's Will,
  Warriors→leer, Ork-Fraktion→leer, badge_label, effect.type
- **3 neue Tests** für `active_buffs` Reset + `command_ability_state` Persistenz in game_state
- **5 pre-existing Failures gefixt**: `p1_faction_dir`-KeyError in 3 Dateien (nach `faction_dir_for()`-Refactoring),
  `my_will_be_done_active` → `active_buffs` in 2 UI-Test-Helpern

### Session 2: Command Protocol Effects + Game Log Archiv

**Command Protocols (Schritt 2):**
- `command_protocols.yaml`: strukturierte `directives`-Blöcke mit `effect`-Feldern für alle 6 Protokolle
- `CommandProtocol` Dataclass: `primary_effect: dict` + `secondary_effect: dict`
- `loader.py`: parst `directives.primary/secondary.effect` aus YAML
- `ability_engine.py`: `get_active_protocol_modifier(faction_dir, phase, use_melee)`
  — gibt `{hit, wound, save}` zurück; unwired Types (reroll, move, RP) still skipped
- `armyCard.py`: `_render_directive_buttons()` — Primary/Secondary Buttons nach Protokoll-Aktivierung;
  Bug gefixt: `_ETERNAL_GUARDIAN_ID` stimmte nicht mit YAML-ID überein
- `combat.py`: `DefendParams.save_modifier` — Eternal Guardian +1 Save wired
- `_common.py` `render_attack_form()`: liest Protokoll-Modifier für Angreifer (hit/wound)
  und Verteidiger (save), zeigt als `st.info()` + fließt in `AttackParams`/`DefendParams`
- `game_state.py`: `active_directive` in `init_state()` + `_reset_turn_state()`
- **9 neue Tests** für `get_active_protocol_modifier()`

**Game Log Archiv (Schritt 3):**
- `game_log.py`: neues JSON-Format (game_id/players/rounds/phases/events),
  `archive_and_reset_log()`, `list_archived_logs()`
- `game_state.py`: `reset_game()` → `archive_and_reset_log()`
- `setupScreen.py`: "Battle Log Archive" Expander (Liste, Download, Löschen mit Bestätigung)

---

## Bekannte offene Probleme / Nächste Schritte (priorisiert)

### 1. Protocol-Badge in armyCard + sourced Modifier in gameActionsArea (⬅ NÄCHSTE SESSION)

**Was fehlt:**
- **armyCard:** Nach Direktiven-Wahl: Badge mit Protokollname + Direktive
  (z.B. `HUNGRY VOID — PRIMARY` als buff-blauer Badge) + Effect-Text als Caption.
  Aktuell wird nur plain Text gezeigt.
- **gameActionsArea (`render_attack_form()`):** Protokoll-Modifier ist aktuell ein generisches
  `st.info("Protocol: +1 to hit modifier.")`. Soll durch sourced Einträge ersetzt werden —
  Protokollname als Quelle klar nennen, z.B. `Hungry Void (Primary): +1 to hit` —
  inline bei den Waffen-Stats oder als Badge-HTML.

**Betroffene Dateien:**
- `src/uiLayout/armyCard.py` — Badge nach Direktiven-Wahl
- `src/uiLayout/_common.py` — sourced Modifier-Zeile in `render_attack_form()`

**Nicht wired (bewusst ausgelassen für diese Session, da kein numerischer Modifier):**
- Reroll-Effekte (Conquering Tyrant secondary, Eternal Guardian secondary)
- Move-Bonus (Sudden Storm primary) → movementPhase nötig
- Advance and Charge (Sudden Storm secondary) → chargephase nötig
- Strength-Bonus (Hungry Void secondary) → AttackParams.strength_modifier bräuchte neues Feld
- AP-Bonus (Vengeful Stars secondary) → profile.ap wäre zu modifizieren
- RP-Effekte (Undying Legions) → reanimation system nötig
- Leadership-Bonus (Conquering Tyrant primary)

### 2. `set_log_players()` in `init_state()` (klein, 5 Minuten)

`set_log_players(first, second)` ist implementiert aber wird nicht aufgerufen.
In `game_state.py` `init_state()` nach den `st.session_state`-Zuweisungen ergänzen:
```python
from gameMechanic.game_log import set_log_players
set_log_players(p1_name, p2_name)
```
Betroffene Datei: `src/gameMechanic/game_state.py`

### 3. Ziel 6d — Attackensequenz simultan (größer, braucht eigene Session)

Alle Würfelblöcke (Treffer, Verwundung, Save, FNP, Schaden) gleichzeitig rendern.
Modifier-Stack mit Quellen transparent anzeigen. Benötigt `collect_modifiers_for_phase()`.
Spec: `docs/goals/ziel6.md` → 6d.

---

## Architektur-Entscheidungen (nicht vergessen)

### Command Protocol System

```
YAML (command_protocols.yaml)
  └─ CommandProtocol: id, name_en, primary, secondary,
                      primary_effect: {type, value, phase}
                      secondary_effect: {type, value, phase}
        │
ability_engine.py
  └─ get_active_protocol_modifier(faction_dir, phase, use_melee)
        → liest active_protocol_id + active_directive aus session_state
        → gibt {hit, wound, save} zurück (nur wired types)
        │
_common.py render_attack_form()
  └─ atk_protocol_mod → AttackParams.hit_modifier + wound_modifier
  └─ def_protocol_mod → DefendParams.save_modifier
```

**Wired effect types:** `hit_modifier`, `wound_modifier`, `save_modifier`
**Not wired (in YAML, nicht in Combat):** `reroll_save_1`, `reroll_hit_wound_1`,
`strength_modifier`, `ap_bonus`, `leadership_bonus`, `move_bonus`, `advance_and_charge`,
`rp_reroll`, `rp_bonus`

### Session-State Schlüssel (Command Phase + Protocols)

| Key | Typ | Bedeutung |
|-----|-----|-----------|
| `active_protocol_id` | `str \| None` | Aktives Protokoll dieser Runde |
| `active_directive` | `"primary" \| "secondary" \| None` | Gewählte Direktive |
| `used_protocol_ids` | `list[str]` | Bereits verwendete Protokoll-IDs (keine Wiederholung) |
| `command_ability_state` | `dict[ability_id, {target_uid, active_since_round}]` | Aktive Unit-Abilities |
| `cmd_awaiting_ability_id` | `str \| None` | Welche Ability wartet auf Zielauswahl |
| `cmd_awaiting_required_kw` | `list[str]` | Keywords die das Ziel haben muss |

### Unit-State Felder (relevant für Abilities)

| Feld | Typ | Bedeutung |
|------|-----|-----------|
| `active_buffs` | `list[dict]` | `[{ability_id, badge_label, effect_type}]` — aktive Buffs |

`active_buffs` wird bei `_reset_turn_state()` geleert.
`active_protocol_id` + `active_directive` werden bei `_reset_turn_state()` auf `None` gesetzt.

### Game Log Format

```json
{
  "game_id": "2026-06-03T14:22:00",
  "players": {"first": "Necrons", "second": "Orks"},
  "rounds": [
    {
      "round": 1,
      "phases": [
        {
          "phase": "shooting",
          "active": "Necrons",
          "events": [{"type": "action", "unit": "...", "action": "..."}]
        }
      ]
    }
  ]
}
```

Archiv: `data/log/archive/<game_id>.json` — entsteht bei `reset_game()`

### Wie das Ability-System funktioniert

```
YAML (unit_abilities.yaml)
  └─ Ability: id, unit_id, ability_type, trigger.phase, effect.type, badge_label
        │
ability_engine.py
  └─ get_activated_command_abilities(unit_id, faction_dir)
        │
commandPhase.py
  └─ _render_unit_command_abilities(selected_uid, faction, ...)
        └─ für effect.type in (buff_roll, reroll_hit_1): _render_buff_roll_ability()
                │
                └─ Button → cmd_awaiting_ability_id gesetzt
                        │
                unitCard.py: wenn cmd_awaiting_ability_id gesetzt
                        └─ Zeige Select-Button für jede Einheit die has_keywords erfüllt
                                │
                                └─ Bei Klick: active_buffs[{ability_id, badge_label, effect_type}]
                                             command_ability_state[ability_id] = {target_uid, round}
```

---

## Wichtige Constraints

- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Bei Unklarheiten ZUERST FRAGEN** — Regelwerk immer nachschlagen, nicht raten
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
- **Keywords immer `UPPERCASE` in YAML** — Checks via `unit.has_keyword()`
- Weapon-Zugriff mit Dual-Profile: `w.for_phase(use_melee)` — nicht `w.is_melee`
- Session-State Unit-Keys: `p1_units` / `p2_units` mit `#N`-Suffix für Duplikate
- Weapon strength: `_parse_strength()` in `_common.py` — nie direkt `int(profile.strength)`
- **Abilities: NIE auf Fraktionsnamen hardcoden** — immer generisch über Keywords/YAML/unit_id
- **Command Protocols: NUR NECRONS** — armyCard ist einziger Einstiegspunkt
- **Protocol-Direktiven:** `active_protocol_id` + `active_directive` sind global (nicht per Spieler).
  Bei Necrons vs. Necrons theoretisch buggy — für jetzt akzeptiert, da Protokoll-Fraktionen exklusiv.

### Streamlit 1.57 — CSS-Selektoren

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
