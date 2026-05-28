# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py`
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Dateien lesen (in dieser Reihenfolge)

1. `.claude/tasks/next_session.md` — diese Datei
2. `docs/goals.md` — vollständiger Plan
3. `src/uiLayout/armyCard.py` — aktuelle Implementierung (wichtig für Designdiskussion unten)
4. `src/gameObjects/ability.py` — aktuelles Ability-Datenmodell

---

## Was in dieser Session gemacht wurde

### Ziel 4b — armyCard + unitCard Redesign (committed)

**unitCard (`src/uiLayout/unitCard.py`):**
- Neue Layout-Reihenfolge: LP/Modell-Bars → Name-Button → State-Badges → Keywords
- `st.container(border=True)` — sichtbarer Rahmen, Badges eindeutig zugeordnet
- Hauptfraktionsschlüsselwort (`unit.faction`) aus Keywords-Anzeige gefiltert
- Keyword-Highlighting: `session_state.highlight_keywords: list[str]` — all-or-nothing Logik

**armyCard (`src/uiLayout/armyCard.py`):**
- Komplett neu: Border, Faction-Badge + Subfaction-Badge
- TriggeredAbility-Buttons (phasenabhängig sichtbar, z.B. Living Metal in Befehlsphase)

**Datenmodell:**
- `Ability.ability_type: str = "triggered" | "activated"` — neu
- YAMLs aktualisiert, Loader erweitert

**Refactoring:**
- `apply_living_metal()` von `commandPhase.py` → `unit_mutations.py` verschoben
- Living Metal Button aus commandPhase entfernt (jetzt in armyCard)
- `armyList.py` lädt und reicht `faction_abilities` weiter

**Tests:** 209 grün (vorher 200)

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A–1B — Struktur | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3 — Combat Foundation | ✅ fertig |
| Ziel A — Architektur-Review | ✅ fertig |
| Ziel 4a — Badge/State-System | ✅ fertig |
| **Ziel 4b — armyCard + unitCard Redesign** | ✅ **fertig** |
| Ziel 4c — Bewegungsphase vollständig | ⬜ geplant |
| Ziel 4d — Angriffsphase (Charge) | ⬜ geplant |

---

## ERSTE AUFGABE: Designdiskussion — generisches Ability-Modell

### Das Problem

`armyCard.py` enthält `_living_metal_eligible()` — eine Eligibility-Prüfung, die
`"livingMetal" in u.rules` direkt prüft. Das ist eine Necron-spezifische Implementierung,
die als generische Logik in das Ability-Datenmodell gehört.

**Kern-Frage:** Wie kann eine `Ability` ihre eigene Eligibility-Prüfung kapseln,
sodass `armyCard.py` nur noch `ability.get_eligible_units(units, states)` ruft?

### Nutzerwunsch (wörtlich aus Session)

> "Ich hätte hier lieber so etwas wie `armyAbility(...)` stehen auf ganz abstrakte Weise.
> Und Living Metal, RP usw. sind dann eben eine `armyAbility()`. `armyAbility()` wäre dann
> vielleicht eine Unterklasse von `ability()`."

### Aktuelles Ability-Modell (Kurzreferenz)

```python
# src/gameObjects/ability.py
@dataclass
class Ability:
    id: str
    name_en: str
    source: str          # "faction_rule" | "unit_ability" | "wargear"
    rule_text: str
    trigger: Trigger     # timing, phase, player, event
    conditions: list[Condition]  # has_rules, has_keywords, max_uses, ...
    effect: Effect       # type, target, amount, modifier, handler
    unit_id: str | None
    ability_type: str    # "triggered" | "activated"
```

### Diskussionspunkte für die Session

1. **Eligibility als Methode auf `Ability`?**
   ```python
   ability.get_eligible_units(units, states) -> list[str]
   ```
   Würde erfordern, dass `Ability` die Bedingungen gegen Unit-States auswerten kann —
   das ist eigentlich Aufgabe der `ability_engine.py`.

2. **`ArmyAbility` als Unterklasse?**
   Pro: klare Trennung army-wide vs. unit-specific.
   Con: `Ability` ist schon generisch genug — vielleicht reicht ein Feld `scope: "army" | "unit"`.

3. **Handler-Pattern (bereits in `Effect.handler`)?**
   `effect.handler = "livingMetal"` existiert schon für komplexe Effekte.
   Könnte man zu `eligibility_handler = "livingMetal"` erweitern.

4. **Conditions reichen aus?**
   `Condition.has_rules = ["livingMetal"]` ist bereits im YAML.
   Vielleicht muss `armyCard` nur `ability_engine.check_conditions()` aufrufen
   statt eine eigene `_living_metal_eligible()`-Funktion zu haben.

**Empfehlung zum Diskutieren:** Option 4 ist am elegantesten — die Conditions-Logik
existiert bereits in `ability_engine.py`. `armyCard` ruft sie einfach pro Unit auf.
Kein neuer Code, keine Unterklasse — nur den vorhandenen Mechanismus nutzen.

---

## Designregeln (fest)

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: `first_player` links, `second_player` rechts — niemals an `active` binden
- Aktionen nur kontextuell zur ausgewählten Einheit
- **Kein Design ohne Schema** — Nutzer definiert Farbpalette selbst; keine eigenständigen Farbentscheidungen
- `dev`-Branch — kein direktes Committen auf `main`
- Necron-Spezifika sind **Beispiele** — Hauptlogik und Doku bleiben generisch

---

## Architektur (Kurzreferenz)

```
src/
  app.py
  gameMechanic/
    combat.py | commandPhase.py | shootingPhase.py | fightPhase.py
    movementPhase.py | chargephase.py | game_state.py
    unit_mutations.py   ← apply_living_metal() jetzt hier
    game_log.py | ability_engine.py | phase_runner.py
  gameObjects/
    ability.py          ← Ability mit ability_type-Feld
    unit.py | weapon.py | loader.py
  uiLayout/
    _common.py
    unitCard.py         ← border, neue Reihenfolge, keyword highlighting
    armyCard.py         ← border, badges, triggered ability buttons
    armyList.py         ← lädt faction_abilities
    gameActionsArea.py
data/wh40k_9e/necrons/ | orks/
tests/
  gameMechanic/ | uiLayout/ | gameObjects/
  uiLayout/test_unit_card.py  ← neu
docs/
  goals.md | spec/ | work/
```
