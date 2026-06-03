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
| Ziel 6e (teilw.) — Command Phase generic abilities | ✅ committed |
| Ziel 6e (teilw.) — Command Protocols verdrahtet | ✅ committed |
| Ziel 6g (teilw.) — Game Log Archiv + Setup-UI | ✅ committed |
| **Ziel 6h — Custodes Ka'tah YAML + Loader-Fix** | ⬅ NÄCHSTER SCHRITT |
| Ziel 6h — AdMech Canticles YAML | ⬜ |
| Ziel 6h — Auto-Progression (Space Marines Doctrines) | ⬜ |
| Ziel 6g — set_log_players() in init_state() | ⬜ klein |
| Ziel 6d — Attackensequenz simultan | ⬜ |
| Ziel 6f — Ability-Badges unitCard | ⬜ |

---

## Was wurde zuletzt gemacht (2026-06-03, diese Session)

### WAAAGH! Datenfehler korrigiert
- `orks/faction_abilities.yaml` + `unit_abilities.yaml`: `phase: charge` → `phase: command`
  (WAAAGH! wird in der Befehlsphase ausgerufen, nicht in der Charge Phase — Wahapedia Screenshot bestätigt)
- Betroffen: `waaagh_stage1`, `speedwaaagh_stage1`, `call_da_waaagh`, `call_da_speedwaaagh`, `great_waaagh`

### Generisches Fähigkeitssystem implementiert

**game_state.py:**
- `waaagh_state: dict = {}` in `init_state()` (Format: `{player_name: {stage, round_activated}}`)
- `_reset_turn_state()`: automatische Stage-1→2-Transition wenn `round_activated < current_round`

**armyCard.py:**
- `_active_ability_badge(text, color)`: HTML-Badge (amber für Protocols, grün für WAAAGH!)
- `_render_protocol_ui()`: zeigt nach Direktiven-Wahl jetzt **HTML-Badge** statt st.caption
- `_render_waaagh_ui(faction, faction_abilities, units)`: **generisch** — liest `ability_type: activated` + `trigger.phase: command` aus `faction_abilities`; zeigt Button wenn WARBOSS im Roster; Stage-Badge wenn aktiv
- `render_army_card()`: ruft beide UIs auf — für Necrons: Protocols; für Orks: WAAAGH!; für andere: no-op (bis YAML-Daten angelegt)

**_common.py `render_attack_form()`:**
- Sourced Modifier-Labels: statt `"Protocol: +1 to hit"` → `"Hungry Void (Primary): +1 to hit"`
- WAAAGH!-Effekte im Fight-Phase als Info-Text (display only, nicht in combat.py verdrahtet)

**369 Tests — alle grün.**

### Architektur-Dokumentation
- `docs/spec/faction_abilities.md` — vollständige Spec aller 6 Fähigkeitskategorien
- `data/wh40k_9e/_schema/round_choice.example.yaml` — Schema-Vorlage
- `data/wh40k_9e/_schema/one_time.example.yaml` — Schema-Vorlage
- `data/wh40k_9e/_schema/auto_progression.example.yaml` — Schema-Vorlage
- `docs/goals/ziel6.md`: neues Teilziel 6h mit allen fehlenden Fraktionen

---

## WICHTIGE ARCHITEKTUR-ERKENNTNIS (Wahapedia-Recherche 2026-06-03)

### 6 Kategorien von Fraktionsfähigkeiten

Die App muss für ALLE Fraktionen funktionieren. Lokale YAML-Dateien ≠ vollständige Daten.
**Niemals nur lokale Dateien für Architekturentscheidungen befragen — immer Wahapedia prüfen!**

| Kategorie | Fraktionen | Code-Pattern | Status |
|-----------|-----------|-------------|--------|
| Runden-Wahl | Necrons, **Custodes**, **AdMech**, **Tyranids** | `command_protocols.yaml` + `_render_protocol_ui()` | Code fertig, YAML fehlt |
| Einmalig | Orks, **T'au** | `faction_abilities.yaml` (activated/command) + `_render_waaagh_ui()` | Orks fertig, T'au fehlt |
| Auto-Progression | **Space Marines**, **Death Guard**, **Chaos SM** | `auto_progression` YAML + Info-Badge | Noch nicht implementiert |
| Ressourcen | Thousand Sons, Aeldari | Eigenes System | Noch nicht geplant |
| Verteilung | Astra Militarum | Orders-System | Noch nicht geplant |
| Passiv | Alle (Dynastien, Klan-Kulturen) | triggered-Abilities | Abgedeckt |

**Custodes Ka'tah = identische Struktur wie Necron Command Protocols!**
6 Optionen × 2 Stances (Aggressive/Stoic = Primary/Secondary) — kein Code-Änderung nötig, nur YAML.

---

## Konkrete nächste Schritte (priorisiert)

### 1. Custodes Ka'tah YAML anlegen (⬅ JETZT STARTEN)

Datei: `data/wh40k_9e/adeptus_custodes/command_protocols.yaml`
Schema: identisch zu `data/wh40k_9e/necrons/command_protocols.yaml`
Quelle: https://wahapedia.ru/wh40k9ed/factions/adeptus-custodes/

Die 6 Ka'tahs (je mit Aggressive Stance = Primary, Stoic Stance = Secondary):
1. **Calistus Ka'tah** — Aggressive: +D6" Advance / Stoic: gilt als stationär nach Bewegung
2. **Conservai Ka'tah** — Aggressive: Aktionen während Advance/Fall Back / Stoic: Schießen während Aktionen
3. **Dacatarai Ka'tah** — Aggressive: Pile-in/Consol -2" für Feind / Stoic: +1 Attacks (Dmg-1-Waffen)
4. **Salvus Ka'tah** — Aggressive: Reichweite +4" / Stoic: 2× schießen (Auric-Waffen, stationär)
5. **Rendax Ka'tah** — Aggressive: unmod. 6 = auto-wound vs VEHICLE/MONSTER / Stoic: +1 Str nach Charge
6. **Kaptaris Ka'tah** — Aggressive: Feind kann Hits nicht re-rollen / Stoic: verhindert Fallback

**Nach YAML-Anlage:** Test schreiben + sicherstellen dass `_render_protocol_ui()` Custodes korrekt anzeigt.

### 2. Loader fix: `secondary` optional machen

Datei: `src/gameObjects/loader.py` (CommandProtocol-Parser)
Problem: `CommandProtocol.secondary` und `secondary_effect` sind aktuell required
Fix: Optional machen (None wenn nicht in YAML → UI überspringt Direktiven-Wahl)
Für: AdMech Canticles (kein Secondary)

### 3. AdMech Canticles YAML anlegen

Datei: `data/wh40k_9e/adeptus_mechanicus/command_protocols.yaml`
Quelle: https://wahapedia.ru/wh40k9ed/factions/adeptus-mechanicus/
Alle 6 Canticles — nur Primary (kein Secondary)

### 4. Auto-Progression implementieren (Space Marines Doctrines)

Neue Funktion in `ability_engine.py`:
```python
def get_auto_progression_modifier(faction_dir: str, phase: str, current_round: int, use_melee: bool) -> dict[str, int]:
```
Neue Funktion in `armyCard.py`:
```python
def _render_auto_progression_badge(faction: str, faction_abilities: list[Ability]) -> None:
```
YAML: `data/wh40k_9e/space_marines/faction_abilities.yaml` mit `ability_type: auto_progression`

### 5. Tests für alle neuen Fraktions-Fähigkeiten

Neue Testdateien:
- `tests/test_faction_abilities_custodes.py`
- `tests/test_faction_abilities_admech.py`
- `tests/test_auto_progression.py`

Testmuster pro Fraktion:
```python
def test_load_<faction>_command_protocols():
    protocols = load_command_protocols("<faction_dir>")
    assert len(protocols) == N

def test_<faction>_protocol_badge_label():
    p = protocols[0]
    assert p.name_en != ""

def test_<faction>_protocol_modifier_<phase>():
    mod = get_active_protocol_modifier("<faction_dir>", "<phase>", use_melee=False)
    assert mod.get("hit") == expected_value
```

### 6. set_log_players() in init_state() (klein, 5 Minuten)

`game_state.py` `init_state()` nach Session-State-Zuweisungen ergänzen:
```python
from gameMechanic.game_log import set_log_players
set_log_players(p1_name, p2_name)
```

---

## Bekannte Constraints & Architektur-Entscheidungen

### Generische Fähigkeits-Architektur

```
YAML (command_protocols.yaml)          YAML (faction_abilities.yaml)
  └─ CommandProtocol: id, name,          └─ Ability: id, ability_type=activated,
     primary/secondary (optional),           trigger.phase=command, once_per_battle
     primary_effect/secondary_effect         stage_effects: {badge_label, effects[]}
          │                                       │
ability_engine.py                         armyCard._render_waaagh_ui()
  └─ get_active_protocol_modifier()         └─ filtert command_activated
     → {hit, wound, save}                      → Button oder Badge
          │                                       │
armyCard._render_protocol_ui()            game_state.waaagh_state{}
  └─ lädt command_protocols.yaml              └─ {player: {stage, round_activated}}
     → Radio + Button oder Badge
          │
_common.py render_attack_form()
  └─ sourced label: "Hungry Void (Primary): +1 to hit"
```

### Wired effect types (in combat.py)
`hit_modifier`, `wound_modifier`, `save_modifier`

### Nicht wired (nur Display)
`strength_modifier`, `attacks_modifier`, `ap_bonus`, `move_bonus`,
`advance_and_charge`, `reroll_hit_wound_1`, `reroll_save_1`,
`leadership_bonus`, `rp_reroll`, `rp_bonus`, `toughness_debuff`,
`invuln_save`, `extra_hit_on_6`, `shoot_after_fallback`

### Session-State Schlüssel (Command Phase + Protocols + WAAAGH!)

| Key | Typ | Bedeutung |
|-----|-----|-----------|
| `active_protocol_id` | `str \| None` | Aktives Protokoll / Ka'tah dieser Runde |
| `active_directive` | `"primary" \| "secondary" \| None` | Gewählte Direktive / Stance |
| `used_protocol_ids` | `list[str]` | Bereits verwendete Protokoll/Ka'tah-IDs |
| `waaagh_state` | `dict[str, dict]` | `{player: {stage, round_activated}}` |
| `command_ability_state` | `dict[ability_id, {target_uid, active_since_round}]` | Unit-Abilities |

### Wichtige Constraints
- **Freigabe vor Umsetzung** — Plan + Dateiliste zeigen, auf „ja" warten
- **Niemals nur lokale YAML-Daten für Architektur-Entscheidungen** — immer Wahapedia prüfen
- Seitenleisten IMMER fest: first_player links, second_player rechts
- dev-Branch — kein direktes Committen auf main
- Keywords immer `UPPERCASE` in YAML — Checks via `unit.has_keyword()`
- Weapon strength: `_parse_strength()` in `_common.py`
- Abilities: NIE auf Fraktionsnamen hardcoden — immer generisch via YAML/Keywords
- Command Protocols: kein Necrons-only mehr — Ka'tah + Canticles nutzen selbe Pipeline
- WAAAGH! + T'au: nutzen `_render_waaagh_ui()` — generisch via `faction_abilities`

### Streamlit 1.57 — CSS-Selektoren

| Komponente | Korrekte Selektoren |
|---|---|
| NumberInput Container | `[data-testid="stNumberInputContainer"]` |
| Buttons allgemein | `button[data-testid="stBaseButton-{kind}"]` |
| Container border=True | `.e1rw0b1u3` (Emotion-Klasse — prüfen bei Streamlit-Update!) |
