# Plan 016: Command-Protocol-Effekte auf RP/Living Metal abbilden + Dynastiebonus anzeigen

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat f0f4e17..HEAD -- src/gameMechanic/ability_engine.py src/uiLayout/_common.py src/uiLayout/armyCard.py data/wh40k_9e/necrons/faction_abilities.yaml`
> Drift in `_common.py` durch Pläne 013/014 ist ERWARTET. Wenn
> `get_active_protocol_modifier` oder `_render_rp_block` strukturell anders
> aussehen als unter Current state: STOP.

## Status

- **Priority**: P2 (MITTEL — next_session.md „Necron Command Phase")
- **Effort**: S–M
- **Risk**: LOW (überwiegend Anzeige-Hinweise; ein generischer Engine-Helper)
- **Depends on**: — (nach 014 ausführen, wenn parallel gearbeitet wird — gleiche Datei `_common.py`)
- **Category**: feature (Regel-Transparenz Command Protocols)
- **Planned at**: commit `f0f4e17`, 2026-06-12

## Why this matters

Die Command Protocols sind in YAML vollständig erfasst
(`necrons/faction_abilities.yaml:46-149`), aber nur drei Effekt-Typen sind
verdrahtet (`ability_engine.py:66`: `hit_modifier`, `wound_modifier`,
`save_modifier`). Direktiven, die **Reanimation Protocols** betreffen
(`rp_reroll`, `rp_bonus` — Protocol of the Undying Legions, Z. 115-131),
werden still verschluckt: Die Spielerin sieht im RP-Block keinerlei Hinweis,
dass sie rerollen darf oder +1 Modell zurückbekommt. Gleiches gilt für den
Dynastiebonus: Das 6. Protokoll mit `subfaction_affinity == dynasty` gilt
mit BEIDEN Direktiven (Bug 3, gefixt 2026-06-05), aber die UI zeigt nicht
an, WANN eine Direktive aus der Dynastiezugehörigkeit kommt.

## Current state

- `ability_engine.py:69-110` — `get_active_protocol_modifier(faction_dir,
  phase, use_melee)`: liest `protocol_active_{faction_dir}` +
  `protocol_directive_{faction_dir}` aus dem Session-State, liefert nur
  hit/wound/save. Alle anderen Typen → `{}` (Docstring sagt es explizit).
- `_common.py:454-499` — `_render_rp_block()`: zeigt
  „X gefallen → Y Würfel · Erfolg: 5+" + Counter. KEIN Protokoll-Hinweis.
- Protokoll-Effekt-Typen in YAML (necrons): `save_modifier`, `reroll_save_1`,
  `hit_modifier`, `strength_modifier`, `leadership_bonus`,
  `reroll_hit_wound_1`, `move_bonus`, `advance_and_charge`, `rp_reroll`,
  `rp_bonus`, `wound_modifier`, `ap_bonus`.
- Living Metal (`faction_abilities.yaml:4-23`): triggered heal, 1 LP —
  KEIN Necron-Protokoll modifiziert Living Metal direkt (geprüft: die 7
  Protokolle oben). Der next_session-Punkt „Protokoll-Effekte auf Living
  Metal" reduziert sich damit auf: **verifizieren gegen
  `docs/work/wahapedia_necrons/` und im Bericht festhalten** (Step 1).
- Dynastie-Felder: `st.session_state.p1_dynasty` / `p2_dynasty`
  (`game_state.py:279-280`); Protokoll-Zuordnung pro Runde + 6. Protokoll
  werden in `armyCard.py` / Setup gehandhabt (Bug 1–3 ✅ 2026-06-05).

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Engine-Tests | `python -m pytest tests/gameMechanic/test_ability_engine.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- `src/gameMechanic/ability_engine.py` — generischer Helper
  `get_active_protocol_effects(faction_dir, types)` (Verallgemeinerung)
- `src/uiLayout/_common.py` — RP-Block: Hinweise für `rp_reroll`/`rp_bonus`
- `src/uiLayout/armyCard.py` — Dynastiebonus-Kennzeichnung
- Tests

**Out of scope** (NICHT anfassen):
- `ap_bonus`/`strength_modifier` in der Attackensequenz verdrahten → Plan 017
  bzw. später (hier nur RP + Anzeige).
- `move_bonus`, `leadership_bonus`, `advance_and_charge`, Reroll-Typen in
  Spiellogik verdrahten — separates Thema; `advance_and_charge` existiert
  bereits generisch über `charge_after_advance_allowed` für activated
  abilities, NICHT für Protokolle (falls gewünscht: melden, nicht bauen).
- Custodes Ka'tah / generische round_choice anderer Fraktionen: der Helper
  ist generisch, aber Daten-Nachpflege nur für Necrons.

## Git workflow

- Branch: `feature/016-protocol-rp-effects`.
- Commit z. B. `Surface protocol RP effects and dynasty bonus in UI`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Regel-Verifikation (Lesen, kein Code)

`docs/work/wahapedia_necrons/` (Command-Protocols-Abschnitt) lesen:
1. Bestätigen, dass KEIN Protokoll Living Metal modifiziert (Erwartung: ja).
2. Wortlaut von Undying Legions prüfen: gilt `rp_bonus` „+1 model returned"
   pro RP-Ereignis oder pro Phase? Wirkt `rp_reroll` auf den ganzen Pool
   oder einzelne Würfel? Wortlaut im Bericht zitieren — die Hinweis-Texte
   in Step 3 müssen dem Wortlaut folgen.

**Verify**: Zitate im Abschlussbericht; bei Widerspruch zur YAML
(`primary`/`secondary` vertauscht o. ä.): STOP.

### Step 2: `get_active_protocol_effects()` in der Engine

`ability_engine.py`, neben `get_active_protocol_modifier`:

```python
def get_active_protocol_effects(faction_dir: str, types: set[str]) -> list[dict]:
    """Raw effect dicts of the active directive(s) matching the given types.

    Includes the dynasty protocol's BOTH directives when it applies
    (6th-protocol rule). Generic: works for any faction with round_choice
    abilities.
    """
```

- Gleiche State-Quelle wie `get_active_protocol_modifier`
  (`protocol_active_…`/`protocol_directive_…`) PLUS die Dynastie-Logik:
  nachsehen, wie das 6. Protokoll/der Dynastiebonus seit Bug-3-Fix im
  Session-State repräsentiert ist (armyCard/Setup), und beide Direktiven des
  Dynastie-Protokolls einbeziehen. Quelle der Wahrheit ist der bestehende
  Fix — NICHT neu erfinden; wenn der Dynastie-Zustand nirgends abfragbar
  ist: STOP (siehe unten).
- `get_active_protocol_modifier` danach intern auf den neuen Helper
  umstellen (ein Idiom, kein Duplikat).

**Verify**: Neue Engine-Tests (Protokoll aktiv → Effekte gefiltert nach
`types`; Dynastie-Protokoll → beide Direktiven) grün; bestehende
`get_active_protocol_modifier`-Tests unverändert grün.

### Step 3: RP-Block-Hinweise

`_render_rp_block` (`_common.py:454`): vor dem Counter
`get_active_protocol_effects(faction_dir_for(def_faction), {"rp_reroll",
"rp_bonus"})` abfragen:

- `rp_reroll` aktiv → `st.caption("⟳ Protocol of the Undying Legions:
  RP-Würfe dürfen wiederholt werden.")` (Label generisch aus dem
  Protokoll-Namen, nicht hardcoded — Name kommt aus dem YAML/Helper).
- `rp_bonus` aktiv → Caption „+N Modell(e) zusätzlich zurück" UND
  `max_value` des Counters um N erhöhen (`models_lost + N`, gedeckelt durch
  die laut Step 1 verifizierte Regel — falls RAW bei `models_lost` deckelt:
  nur Caption, kein max_value-Anstieg; Entscheidung aus Step 1 ableiten und
  im Code-Kommentar begründen).

WICHTIG (Generic src/): Texte/Labels aus YAML-Daten (`name_en` des
Protokolls), keine Necron-Literale im Code.

**Verify**: Manuell: Undying Legions als Runden-Protokoll aktiv, Direktive
secondary → RP-Block zeigt Bonus-Hinweis; anderes Protokoll → keine Captions.

### Step 4: Dynastiebonus in der armyCard kennzeichnen

`armyCard.py`: dort, wo das aktive Protokoll/die Direktive angezeigt wird,
beim Dynastie-Protokoll einen Zusatz rendern (z. B. Suffix-Badge
„DYNASTY — beide Direktiven aktiv", Buff-Grün `#4a9a5a` gemäß
design_colors.md §0; KEINE neue Farbe einführen). Exakte Platzierung an die
bestehende Protokoll-Anzeige anlehnen — wenn dafür mehrere Layouts denkbar
sind, Mini-Mockup dem Nutzer zeigen (eine Zeile reicht).

**Verify**: Manuell: Roster mit `dynasty:`-Feld laden → Dynastie-Protokoll
zeigt die Kennzeichnung; Roster ohne Dynastie → keine.

### Step 5: Vollsuite + Lint

`pytest --tb=short` grün, ≥80 %; `ruff check src/ && black --check src/ &&
isort --check-only src/` passt.

## Test plan

- `get_active_protocol_effects`: kein Protokoll aktiv → `[]`; aktiv mit
  passendem Typ → Effekt-Dict; Typ-Filter; Dynastie-Protokoll → beide
  Direktiven.
- `get_active_protocol_modifier` delegiert (Identitäts-/Verhaltens-Tests
  bestehen unverändert).
- RP-Hinweis-Logik als reine Funktion testbar machen (z. B. Helper
  `_rp_protocol_hints(faction_dir) -> list[str]`), damit der Render-Anteil
  minimal bleibt (Coverage-Schnitt beachten).

## Done criteria

ALLE müssen gelten:

- [ ] Regel-Zitate (Undying Legions, Living-Metal-Negativbefund) im Bericht
- [ ] `get_active_protocol_effects` generisch + Dynastie-Doppeldirektive
- [ ] RP-Block zeigt Reroll-/Bonus-Hinweise datengetrieben (kein Necron-Literal in src/)
- [ ] armyCard kennzeichnet den Dynastiebonus
- [ ] `pytest --tb=short` grün, ≥80 %; Lint passt
- [ ] Bericht: manuelle Verifikationspunkte (RP mit/ohne Protokoll, Dynastie an/aus)
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Der Dynastie-/6.-Protokoll-Zustand ist im Session-State nicht abfragbar
  (Bug-3-Fix anders gebaut als angenommen) → melden, Zustandsmodell zeigen,
  auf Entscheidung warten.
- Wahapedia-Wortlaut widerspricht den YAML-Direktiven → YAML NICHT
  eigenmächtig ändern; Differenz melden.
- `_render_rp_block` wurde durch Plan 014 strukturell verändert →
  Einfügepunkte neu bestimmen, bei Unklarheit melden.

## Maintenance notes

- `get_active_protocol_effects` ist ab jetzt DIE Schnittstelle für
  Direktiven-Effekte. Wer weitere Typen verdrahtet (`ap_bonus`,
  `strength_modifier`, Rerolls), erweitert Konsumenten — nicht den Helper.
- Hinweis-Texte folgen dem YAML (`name_en`, `primary`/`secondary`-Texte) —
  Reviewer: hardcodierte Protokollnamen in `src/` ablehnen.
