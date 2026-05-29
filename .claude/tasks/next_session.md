# Startprompt — Nächste Session

## Was ist Arbiter?

**Arbiter** ist ein digitaler Spielbegleiter für Warhammer 40.000 9. Edition, gebaut in Streamlit (Python).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Starten: `streamlit run src/app.py` (Port fest: 8501)
Branch: `dev` (Entwicklung), `main` (stabiler Stand, nur per PR)

---

## Was in dieser Session gemacht wurde

**Planungssession für Ziel 4g** — kein Code geschrieben.

Analyse und vollständige Spezifikation der Angriffsphase erarbeitet:
- Melee-Beziehungsgraph-Konzept: `melee_with` auf `[faction, uid]`-Paare umstellen
- Alle Downstream-Auswirkungen von `in_melee` identifiziert und spezifiziert
- Heroische Intervention vollständig spezifiziert
- Big Guns Never Tire als Lücke in `can_shoot()` identifiziert
- "Nicht in befreundeten Nahkampf schießen" als fehlende Regel identifiziert

Vollständige Spezifikation in `docs/goals.md`, Abschnitt 4g (4g.1–4g.7).

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A–1B — Struktur | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3 — Combat Foundation | ✅ fertig |
| Ziel 4a–4e — Badges, UI, Ability Engine, Command, Movement | ✅ fertig |
| Ziel 4f — Psychic Phase (Smite + Deny + Perils) | ✅ fertig |
| Ziel 4f.1 — Psychic Phase Nachbesserungen | ✅ fertig |
| **Ziel 4g — Angriffsphase (Charge Phase)** | ⏳ **nächster Schritt** |

---

## NÄCHSTE AUFGABE: Ziel 4g — Angriffsphase

Vollständige Spezifikation in `docs/goals.md` → Abschnitt 4g.1–4g.7.
Regelreferenz: `docs/work/schlachtrunde.md`, Abschnitt "5. Angriffsphase"

### Empfohlene Reihenfolge

1. **4g.1** — Melee-Beziehungsgraph reparieren (`unit_mutations.py`)
   — Basis für alles andere; keine UI-Änderung, reine Logik
   — Tests zuerst schreiben (TDD)

2. **4g.2** — Charge-Eligibility-Bug beheben (`chargephase.py`)
   — Ein-Zeiler in `_active_charge()`

3. **4g.3** — Charge-Flow + Melee-Engagement-Anzeige + Break-Button
   — UI-Erweiterung in `chargephase.py`

4. **4g.4** — Heroische Intervention
   — Neuer Block in inaktiver Spalte der Charge Phase

5. **4g.5** — `can_shoot()` für VEHICLE/MONSTER (`shootingPhase.py`)
   — API-Erweiterung: `unit`-Parameter optional hinzufügen

6. **4g.6** — Friendly-Melee-Schuss-Sperre (`shootingPhase.py`)
   — Neue Hilfsfunktion + Prüfung bei Zielauswahl

7. **4g.7** — Tests
   — `tests/gameMechanic/test_charge_phase.py` neu anlegen

### Kernpunkte aus der Analyse

**Melee-Datenstruktur:**
```python
# Alt (buggy): list[str]
"melee_with": ["boyz_mob"]

# Neu: list[list[str, str]] — [faction, uid]
"melee_with": [["Orks", "boyz_mob"], ["Orks", "gretchin"]]
```
Kein Tuple — Streamlit Session State serialisiert Tuples zu Lists.
Nur Feind-Einheiten in der Liste. Many-to-many korrekt abgebildet.

**leave_melee() — kein Hardcode mehr:**
```python
for fac, euid in list(state["melee_with"]):
    enemy_key = "necron_units" if fac == "Necrons" else "ork_units"
    enemy_state = st.session_state[enemy_key].get(euid)
    # cleanup wie bisher
```

**Neue Funktion `leave_melee_pair()`** — löst nur ein spezifisches Pair (für Break-Button):
```python
def leave_melee_pair(uid, faction, enemy_uid, enemy_faction) -> None: ...
```

**Charge-Eligibility (3 Sperren):**
```python
if flags.get("advanced") or flags.get("retreated") or unit_state.get("in_melee"):
    st.warning("Cannot charge — [reason].")
    return
```

**Big Guns Never Tire:**
```python
def can_shoot(unit_state, unit=None) -> bool:
    if unit_state.get("in_melee"):
        if unit is not None:
            kws = {k.upper() for k in unit.keywords}
            if "VEHICLE" in kws or "MONSTER" in kws:
                pass  # Big Guns Never Tire — erlaubt
            else:
                return False
        else:
            return False
    ...
```
Betroffene Einheiten: Triarch Stalker, Canoptek Spyder, Mek Gun (alle VEHICLE).

**Heroische Intervention:**
- `turn_flags["heroic_intervened"]: False` hinzufügen (in `_unit_state()` + `next_phase()` reset)
- Erscheint in **inaktiver** Spielerspalte nach Abschluss von Schritt 1 (Charges)
- Nur CHARACTER-Einheiten (Keyword-Check: `"Character"` in `unit.keywords`)
- Nur Einheiten, die nicht bereits `in_melee` sind
- Nur 1× pro Einheit (`heroic_intervened`-Flag)
- Kann **nicht** in eigener Angriffsphase eingesetzt werden

### Melee-Engagement-Anzeige (UI-Muster)

```
⚔ Engaged with:
  • Boyz Mob A  [Break ✕]
  • Gretchin    [Break ✕]
```

`[Break ✕]` = `leave_melee_pair()` — manueller Override.
Erscheint wenn Einheit selected + `in_melee=True` (Charge Phase + Fight Phase).

---

## Weitere offene Ziele

### 4g.x — Overwatch (Scope TBD)
Wenn eine feindliche Einheit einen Angriff ansagt: Abwehrfeuer-Regel (nur unmodifizierte 6er treffen).
Wurde als `hit_modifier="only_6s"` skizziert. Scope noch nicht entschieden.

### 4h — Moralphase
- D6 + Verluste vs. Leadership → Modelle fliehen

### 4f.1.c — Blessing-Flow (befreundetes Ziel)
- Neuer Effect-Typ `"blessing"` in der Ability Engine

### 4i — Army Builder + Architektur
- `army.yaml` als Roster; Loader löst Werte aus `units.yaml`/`weapons.yaml` auf

---

## Designregeln (fest)

- Freigabe vor Umsetzung — Plan zeigen, auf „ja" warten
- Seitenleisten IMMER fest: `first_player` links, `second_player` rechts
- Aktionen nur kontextuell zur ausgewählten Einheit
- **Kein Design ohne Schema** — Nutzer definiert Farbpalette selbst
- `dev`-Branch — kein direktes Committen auf `main`
- Kein Auto-Würfeln — alle Würfelwürfe gibt der Spieler ein

---

## Architektur (Kurzreferenz)

```
src/
  app.py
  gameMechanic/
    chargephase.py    ← Ziel 4g (Stub → vollständig)
    psychicPhase.py   ← Ziel 4f + 4f.1 fertig
    game_state.py     ← heroic_intervened in turn_flags ergänzen
    commandPhase.py | movementPhase.py | shootingPhase.py
    fightPhase.py | moralePhase.py
    unit_mutations.py ← enter_melee / leave_melee / leave_melee_pair
    game_log.py | ability_engine.py | phase_runner.py
  gameObjects/
    unit.py | weapon.py | loader.py | ability.py | command_protocol.py
  uiLayout/
    _common.py        ← ggf. render_melee_engagements() Hilfsfunktion
    unitCard.py | armyCard.py | armyList.py
    gameActionsArea.py | gameProtocoll.py
data/wh40k_9e/
  necrons/army.yaml   ← Triarch Stalker + Canoptek Spyder: VEHICLE ✓
  orks/army.yaml      ← Mek Gun: VEHICLE ✓
tests/
  gameMechanic/test_charge_phase.py  ← NEU
  gameMechanic/ | uiLayout/ | gameObjects/
docs/
  goals.md | tasks/next_session.md
  work/schlachtrunde.md  ← Regelreferenz (Abschnitt 5. Angriffsphase)
```

---

## Units mit VEHICLE-Keyword (relevant für Big Guns Never Tire)

| Einheit | Fraktion | Keywords |
|---------|----------|---------|
| Triarch Stalker | Necrons | Vehicle, Core, Dynastic Agent |
| Canoptek Spyder | Necrons | Vehicle, Fly, Canoptek |
| Mek Gun | Orks | Vehicle, Artillery |
