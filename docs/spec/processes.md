# Arbiter — Process Diagrams

> Numbering: P-NN (global unique). Find by phase or topic in the index below.
> Format: Mermaid flowcharts. Render in any Markdown viewer with Mermaid support.

---

## Index

| Nr.  | Prozess                                          | Phase(n)           |
|------|--------------------------------------------------|--------------------|
| P-01 | Unit wählen / abwählen                           | alle               |
| P-02 | Gegner-Einheit als Ziel designieren              | shooting/charge/fight |
| P-03 | "→ Weiter"-Button — Phasenübergang (PhaseRunner) | alle               |
| P-04 | Effektbestätigung — Schaden in PlayerArea        | alle (Effekt-Trigger) |
| P-05 | CommandPhase — Living Metal Heilung              | command            |
| P-06 | GO-Sichtbarkeit — Prüfkette                      | alle (Stratagems)  |
| P-07 | Schussphase — vollständiger Ablauf               | shooting           |
| P-08 | AttackSequence — Auflösungsreihenfolge           | shooting / fight   |
| P-09 | PhaseRunner — Dispatch auf render_active         | alle               |
| P-10 | Bewegungsphase — vollständiger Ablauf            | movement           |
| P-11 | Befehlsphase — Kommandoprotokolle (Necrons)      | command            |
| P-12 | Psychic Phase — vollständiger Ablauf             | psychic            |
| P-13 | Angriffsphase — vollständiger Ablauf             | charge             |
| P-14 | Nahkampfphase — vollständiger Ablauf             | fight              |
| P-15 | Moralphase — vollständiger Ablauf                | morale             |

---

## P-01 — Unit wählen / abwählen (alle Phasen)

```mermaid
flowchart TD
    A[Spieler klickt Einheitsnamen\nin seiner armyList] --> B{setup_complete?}
    B -- nein --> Z[kein Effekt]
    B -- ja --> C{Einheit bereits\nselektiert?}
    C -- ja --> D[selected_unit = None\nselected_target = None]
    C -- nein --> E[selected_unit = faction, uid]
    D --> F[st.rerun]
    E --> F
    F --> G[gameActionsArea rendert\naktive PlayerArea mit Einheit]
```

**Zustand nach Selektion:**
- `st.session_state.selected_unit = (faction, uid)` oder `None`
- `st.session_state.selected_target = None` (wird bei Neu-Selektion immer zurückgesetzt)

---

## P-02 — Gegner-Einheit als Ziel designieren (shooting / charge / fight)

```mermaid
flowchart TD
    A[Spieler klickt Einheitsnamen\nder gegnerischen armyList] --> B{Phase erlaubt\nTargeting?}
    B -- nein\ncommand/movement/etc. --> C[nur Namens-Label anzeigen\nkein Button-Effekt]
    B -- ja\nshooting/charge/fight --> D{Einheit bereits\nals Target gesetzt?}
    D -- ja --> E[selected_target = None]
    D -- nein --> F[selected_target = faction, uid]
    E --> G[st.rerun]
    F --> G
    G --> H[inactive PlayerArea zeigt\nZiel-Info + T/Sv/++ Werte]
    H --> I[DisplayArea zeigt\nkombinierten Angriffs-Summary]
```

---

## P-03 — "→ Weiter"-Button — Phasenübergang (alle Phasen)

Jede Phase hat genau **eine** Ansicht (`render_active`). Es gibt kein Stage-
Konzept (`start`/`active`/`end`) — der „→"-Pfeil springt direkt zur nächsten
Phase.

```mermaid
flowchart TD
    A[Spieler klickt →] --> B[next_phase aufgerufen]
    B --> C{letzte Phase\nder Runde? morale}
    C -- ja --> D[Spielerwechsel\n_reset_turn_state\nneue Runde ggf. +1]
    C -- nein --> E[phase_idx + 1]
    D --> F[selected_unit/-targets\nzurückgesetzt, st.rerun]
    E --> F
```

**Hinweis:** Kein hartes Sperren — ein Phasensprung ist immer möglich
(bewusste Entscheidung des Spielers). Der Turn-Flag-Reset (`advanced`,
`retreated`, `charged`, `shot`, `fought`, …) läuft in `_reset_turn_state`,
nur beim Spielerwechsel nach der Moralphase.

---

## P-04 — Effektbestätigung — Schaden/Heilung in PlayerArea

Wenn ein Effekt Schaden oder Heilung an einer Einheit verursacht, erscheinen
die Wundbuttons in der **PlayerArea des betroffenen Spielers** (nicht auf der unitCard).

```mermaid
flowchart TD
    A[Effekt tritt ein\nbsp. Living Metal Heilung] --> B[active_effect = Effekt-Dict\nst.rerun]
    B --> C[PlayerArea des Spielers\nzeigt Bestätigungs-Buttons]
    C --> D[Spieler klickt +1 / -3 / etc.]
    D --> E[apply_damage oder heal_unit\nwird aufgerufen]
    E --> F[active_effect = None\nst.rerun]
    F --> G[PlayerArea kehrt\nzu Normal-Ansicht zurück]
```

**Aktueller Stand:** Wundbuttons erscheinen direkt bei selektierter Einheit.
`active_effect`-Mechanismus wird in Ziel 3 vollständig ausgebaut.

---

## P-05 — CommandPhase — Living Metal Heilung

```mermaid
flowchart TD
    A[Befehlsphase beginnt] --> B[resolve_command_start\nCP +1 wenn Battle-Forged]
    B --> C[get_triggered_abilities\nphase=command, timing=phase_start]
    C --> D{Einheiten mit\nlivingMetal Regel?}
    D -- ja --> E[apply_living_metal\nfür jede berechtigte Einheit]
    E --> F[Heilungs-Ergebnis\nin PlayerArea anzeigen]
    D -- nein --> G[Keine Heilung]
    F --> H[Spieler bestätigt\noder passt an]
    G --> H
    H --> I[Log-Eintrag schreiben]
```

**Einschränkung Living Metal:** `max_alive = models_remaining × unit.wounds`
Verhindert dass Modelle über ihre Startanzahl hinaus geheilt werden.

---

## P-06 — GO-Sichtbarkeit — Prüfkette (Stratagems)

```mermaid
flowchart TD
    A[Phase beginnt] --> B[Alle Stratagems\nder Armee laden]
    B --> C{Bedingungen\nerfüllt?}
    C -- nein --> HIDE[nicht anzeigen]
    C -- ja --> T{timing =\nphase_reactive?}
    T -- ja --> HIDE
    T -- nein --> D{Stratagem-Phase\n= aktuelle Phase?}
    D -- nein --> HIDE
    D -- ja --> F{Bereits diese\nPhase/Battle eingesetzt?}
    F -- ja --> GREY[anzeigen, ausgegraut]
    F -- nein --> G{CP ausreichend?}
    G -- nein --> GREY
    G -- ja --> CLICK[anzeigen, klickbar]
```

**`stage` ist KEIN Sichtbarkeitskriterium:** 9E bindet Stratagems nur an die
Phase; Innerhalb-der-Phase-Timing ("at the start of…", "at the end of…") steht
im Fließtext (`rule_text`) und wird der Spielerin/dem Spieler angezeigt, nicht
hart gefiltert (siehe `docs/spec/acceptance/rules.md`, R-CMD-05).

**Player-Sichtbarkeit:** `player = "active"` → nur aktiver Spieler sieht GO.
`player = "inactive"` → nur inaktiver Spieler (Reaktion auf Gegneraktion).
`player = "both"` → beide Spieler sehen die GO.

---

## P-07 — Schussphase — vollständiger Ablauf

```mermaid
flowchart TD
    A[Schussphase beginnt] --> B[Spieler wählt\nAngreifer-Einheit ▶]
    B --> C{Kann schiessen?}
    C -- nein\nadvanced/retreated/melee --> D[Warnung in PlayerArea]
    C -- ja --> E[Waffen-Profile\nin active PlayerArea]
    E --> F[Spieler wählt\nZiel-Einheit ▷]
    F --> G[T/Sv/++ in\ninactive PlayerArea]
    G --> H[DisplayArea zeigt\nkombinierten Angriffs-Summary]
    H --> I[Spieler würfelt\nphysisch auf dem Tisch]
    I --> J[Spieler klickt\nSchaden-Buttons in PlayerArea]
    J --> K[apply_damage aufrufen]
    K --> L{RP triggerbar?\nmodels_lost_since_last_rp > 0}
    L -- ja --> M[Reanimation Protocol\nin inactive PlayerArea]
    L -- nein --> N[Log-Eintrag schreiben]
    M --> N
    N --> O[Nächste Einheit oder\nPhase beenden]
```

**MWBD-Effekt:** Falls `my_will_be_done_active = True` beim Angreifer:
`Modifier(step="hit", target_type="roll", operation="add", value=1)` wird in `AttackParams.modifiers` injiziert.
Wird in `active_buffs` der Einheit gespeichert und im `build_attack_display` angezeigt.

---

## P-08 — AttackSequence — Auflösungsreihenfolge (shooting / fight)

Die zentrale Funktion `resolve_attack_sequence(params, save_choice, n_hits, n_wounds, n_failed_saves)`.
**Halbmanuell:** Der Spieler würfelt physisch, gibt Anzahlen ein. Keine Auto-Würfel in dieser Funktion.

### Grundprinzipien

| Regel | Konsequenz |
|---|---|
| AP modifiziert den **Würfelwurf**, nicht den Threshold | `effective_save_roll = raw + ap` — Threshold `unit.save` bleibt unverändert |
| Rettungswurf ignoriert AP | `save_choice = "invuln"` → `ap_modifier = 0` |
| Roll-Modifier für Treffer/Verwundung: **max ±1 netto** (9E) | `clamp(Σ roll_modifiers, -1, +1)` — AP hat keinen Cap |
| Unmodifizierter 1 = immer Fehler | Prüfung auf `raw_roll == 1`, unabhängig vom Modifier |
| Unmodifizierter 6 = immer Treffer/Verwundung | Prüfung auf `raw_roll == 6`, unabhängig vom Modifier |
| Quellparameter zuerst auflösen | `source_strength` + `source_toughness` Modifier → dann erst `wound_threshold` berechnen |

### Modifier-Typen

```python
@dataclass
class Modifier:
    step:        Literal["hit", "wound", "save", "damage"]
    target_type: Literal[
        "roll",             # Würfelergebnis direkt  (+1 hit, AP, +1 wound)
        "threshold",        # Vergleichswert direkt  (selten)
        "source_strength",  # → beeinflusst wound_threshold indirekt
        "source_toughness", # → beeinflusst wound_threshold indirekt
    ]
    operation:   Literal["add", "subtract", "reroll_ones", "reroll_all", "mortal_on", "ignore_ap"]
    value:       int | None = None
    condition:   str | None = None  # "on_unmodified_6" | "if_keyword:CORE" | …
```

**Beispiele:**

| Ability | step | target_type | operation | value |
|---|---|---|---|---|
| MWBD (+1 to hit) | `hit` | `roll` | `add` | `1` |
| AP-1 (Waffe, fest) | `save` | `roll` | `subtract` | `1` |
| +1 to wound roll | `wound` | `roll` | `add` | `1` |
| +1 Stärke | `wound` | `source_strength` | `add` | `1` |
| Mortal Wound bei Wound-6 | `wound` | `roll` | `mortal_on` | `6` |
| Reanimation Protocols | eigene Ability-Logik, kein Modifier auf AttackParams |

### Auflösungsreihenfolge (Pflicht)

```mermaid
flowchart TD
    A([AttackParams eingehend\nn_hits / n_wounds / n_failed_saves\nvom Spieler eingegeben]) --> S1

    S1["SCHRITT 1 — Quellparameter auflösen\nstrength += Σ source_strength_modifiers\ntoughness += Σ source_toughness_modifiers"]
    S1 --> S2

    S2["SCHRITT 2 — Vergleichswerte bestimmen\nwound_threshold = s_vs_t_table(strength, toughness)\nhit_threshold = params.hit_threshold\n+ Σ threshold_modifiers (selten)"]
    S2 --> S3

    S3["SCHRITT 3 — Roll-Modifier sammeln\nhit_roll_mod   = clamp(Σ hit roll mods, −1, +1)\nwound_roll_mod = clamp(Σ wound roll mods, −1, +1)\nap_mod = params.ap\n(wenn save_choice = invuln → ap_mod = 0)"]
    S3 --> DISPLAY

    DISPLAY["build_attack_display → UI zeigt:\n• Trefferwurf: brauche {hit_threshold}\n• Modifikator: {hit_roll_mod:+d}\n• Verwundungswurf: brauche {wound_threshold}+\n• Rüstung: {save}+ mit AP{ap} → effektiv\n• Rettung: {invuln}+ (AP ignoriert)"]
    DISPLAY --> ROLL["Spieler würfelt physisch\ngibt n_hits / n_wounds\nsave_choice / n_failed_saves ein"]

    ROLL --> S4

    S4{"Spezialregeln\nprüfen"}
    S4 --> UNMOD1["Unmod. 1 → immer Fehler\n(auch mit +1 Modifier)"]
    S4 --> UNMOD6["Unmod. 6 → immer Treffer/Verwundung\n(auch mit −1 Modifier)"]
    S4 --> MORTAL["mortal_on-Modifier:\nzähle separate mortal_wounds"]

    UNMOD1 --> S5
    UNMOD6 --> S5
    MORTAL --> S5

    S5["SCHRITT 4 — Schaden berechnen\ndamage_dealt = n_failed_saves × params.damage\nmortal_wounds = aus mortal_on-Modifier"]

    S5 --> HOOKS["Ability-Hooks feuern\ntiming: after_unit_attacked\nBeispiel: RP (Necrons) → UI erscheint\nAndere Armeen: nichts"]

    HOOKS --> RESULT([AttackResult\nhits, wounds, failed_saves\ndamage_dealt, mortal_wounds\nwound_threshold, effective_save_threshold\nlog_lines])
```

### Parameter-Quellen: Fernkampf vs. Nahkampf

| Parameter | Fernkampf | Nahkampf |
|---|---|---|
| `n_attacks` | `weapon.attacks` (Waffenprofil) | `unit.attacks` (A-Wert, Einheitenprofil) |
| `hit_threshold` | `unit.bs` (BF) | `unit.ws` (KG) |
| `strength` | `weapon.strength` | `weapon.strength`; `"User"` → `unit.strength` |
| `toughness` | `target.toughness` | `target.toughness` |
| `ap` | `weapon.ap` | `weapon.ap` |
| `damage` | `weapon.damage` | `weapon.damage` |
| `save` / `invuln_save` | `target.save` / `target.invuln_save` | ← identisch |

**`"User"`-Auflösung** findet **vor** `resolve_attack_sequence()` statt (in `shootingPhase` / `fightPhase`).
Die Funktion selbst sieht nur `int` — kein String-Parsing in `combat.py`.

---

## P-09 — PhaseRunner — Dispatch auf render_active (alle Phasen)

`phase_runner.py` ist der einzige Eintrittspunkt für `gameActionsArea.py`.
Jede Phase hat genau eine View; es gibt kein Stage-Konzept mehr.

```mermaid
flowchart TD
    AREA[gameActionsArea\nruft render_current_phase auf] --> PR[PhaseRunner\nliest state.phase_idx → phase_key]
    PR --> REG{PHASE_REGISTRY\nHandler gefunden?}
    REG -- nein --> WARN[st.warning:\nkein Handler registriert]
    REG -- ja --> RA[handler.render_active\nstate]
    RA --> WEITER[Spieler klickt →\nnext_phase aufgerufen]
    WEITER --> ADV{letzte Phase\nder Runde? morale}
    ADV -- nein --> IDX[phase_idx + 1\nst.rerun]
    ADV -- ja --> SWITCH[Spielerwechsel\n_reset_turn_state\nst.rerun]
```

**Turn-Flag-Reset** in `_reset_turn_state` (`game_state.py`), beim
Spielerwechsel nach der Moralphase — nicht bei jedem Phasenübergang:
```python
def _reset_turn_state() -> None:
    for key in ("p1_units", "p2_units"):
        for state in st.session_state[key].values():
            flags = state["turn_flags"]
            for flag in flags:
                flags[flag] = False
            state["lost_models_this_turn"] = 0
            state["fled_models_this_turn"] = 0
            state["movement_choice"] = "stationary"
            state["movement_chosen"] = False
```

Alle Phasen sind vollständig implementiert (Ziel 4).

---

## P-10 — Bewegungsphase — vollständiger Ablauf

```mermaid
flowchart TD
    A[Bewegungsphase beginnt] --> B[Spieler wählt Einheit ▶]
    B --> C{in_reserve?}
    C -- ja --> RESERVE[Caption: In reserve —\nmanage in Step 2 below]
    C -- nein --> D{already_retreated?}
    D -- ja --> LOCKED[Caption: Already retreated\n— no further movement]
    D -- nein --> E{in_melee?}

    E -- ja --> F[Nur STATIONARY oder RETREAT\n— MOVE + ADVANCE deaktiviert]
    E -- nein --> G[MOVE / ADVANCE /\nSTATIONARY / RETREAT]

    F --> H{Spieler klickt RETREAT}
    H --> I[set_movement_status 'retreated'\nleave_melee\nlog_action]
    F --> J{Spieler klickt STATIONARY}
    J --> K[set_movement_status 'stationary']

    G --> L{Spieler klickt MOVE}
    L --> M[set_movement_status 'moved']
    G --> N{Spieler klickt ADVANCE}
    N --> O[set_movement_status 'advanced'\n✗ Charge / ✗ Shoot except Assault]
    G --> P{Spieler klickt STATIONARY}
    P --> Q[set_movement_status 'stationary']

    A --> REINF[Step 2: Reinforcements\nimmer sichtbar für aktiven Spieler]
    REINF --> R{reserve_units vorhanden?}
    R -- nein --> SKIP[Caption: No reinforcements]
    R -- ja, Round 1 --> WAIT[Caption: Cannot deploy until Round 2]
    R -- ja, Round ≥ 2 --> DEPLOY[Button: Deploy {unit} from Reserve]
    DEPLOY --> S[set_deployment 'normal'\nset_movement_status 'moved'\ngilt als MOVED — darf schießen/angreifen]
```

**Einschränkungen (aus `unit_states.md` Sektion 4):**
- `RETREATED` → kein weiterer Bewegungsschritt möglich in diesem Zug
- `IN MELEE + STATIONARY` → kein MOVED/ADVANCED
- `Deployed (MOVED)` → kein ADVANCED (Deployment ≠ ADVANCED)

**Code-Referenzen:**
- `src/gameMechanic/movementPhase.py: _active_movement()` — Constraint-Logik
- `src/gameMechanic/movementPhase.py: _render_reinforcements_step()` — Reserve-Deploy
- `src/gameMechanic/unit_mutations.py: set_movement_status()` — State-Mutation
- Tests: `tests/gameMechanic/test_movement_transitions.py`

---

## P-11 — Befehlsphase — Kommandoprotokolle (Necrons)

Die Necron-Armeeregel „Kommandoprotokolle" wird einmal pro Befehlsphase aktiviert.
Jedes Protokoll kann max. 1× pro Spiel gewählt werden.

```mermaid
flowchart TD
    A[Befehlsphase beginnt\nNecrons aktiver Spieler] --> B{Round == 1?}
    B -- ja --> C[Ewiger Wächter automatisch aktiv\nPrimär + Sekundär-Direktive gelten\nautomatisch ohne Spielerauswahl]
    B -- nein --> D{Noch ungenutzte\nProtokolle vorhanden?}
    D -- nein --> E[Alle Protokolle verwendet\nkein Protokoll in dieser Runde]
    D -- ja --> F[Zeige Liste der verfügbaren\nnicht-genutzten Protokolle]
    F --> G[Spieler klickt Protokoll]
    G --> H[active_protocol_id = p.id\nused_protocol_ids.append p.id]
    H --> I[Protokoll + beide Direktiven\nwerden in gameProtocoll angezeigt]
    C --> I
```

**State in `game_state`:**
| Feld | Typ | Bedeutung |
|---|---|---|
| `active_protocol_id` | `str \| None` | aktuell gewähltes Protokoll |
| `used_protocol_ids` | `list[str]` | alle bereits genutzten Protokoll-IDs |

**Mechanische Effekte:** Noch nicht automatisch appliziert — nur Anzeige + Auswahl.
Vollautomatischer Effekt-Dispatch: Ziel 4i / Ability Engine Erweiterung.

**Code-Referenzen:**
- `src/gameMechanic/commandPhase.py: _render_command_protocols()` — UI
- `src/gameObjects/command_protocol.py` — Dataclass
- `data/wh40k_9e/necrons/command_protocols.yaml` — 5 Protokolle

---

## P-12 — Psychic Phase — vollständiger Ablauf

Generalisierter Psi-Flow: `selectPsyker → rollManifest → (Deny) → resolve Smite`

```mermaid
flowchart TD
    A[Psychic Phase beginnt] --> B{Aktive Armee\nhat PSYKER?}
    B -- nein --> SKIP[Caption: No PSYKER units\n— skip this phase]
    B -- ja --> C{Einheit ausgewählt?}
    C -- nein --> SEL[Caption: Select a PSYKER\nfrom your army list]
    C -- Nicht-PSYKER --> WARN[Warning: Not a PSYKER]
    C -- PSYKER --> D[Zeige Smite — WC 5\n2D6-Eingabe + Attempt Manifest]

    D --> E{Roll eingegeben\nund Button geklickt}
    E --> F{roll == 2 oder 12?}
    F -- ja --> G[Perils of the Warp!\nW3-Schadenseingabe\nam Psyker selbst]
    G --> H{Perils applied?}
    H -- ja --> I{roll ≥ 5?}
    F -- nein --> I

    I -- nein\nroll < 5 --> FAIL[Failed. + Reset-Button\npsi_result = None]
    I -- ja --> MANI[Manifested!\nSmite bereit\nZielauswahl via gegnerische Armeeliste]

    MANI --> DENY{Gegner hat\ncan_deny?}
    DENY -- nein --> DMGAREA[Schadensbereich\nW3 oder W6 bei roll ≥ 11\nApply mortal wounds → Zieleinheit]
    DENY -- ja, denied = None --> WAIT_DENY[Inaktive Spalte:\n2D6 > manifest_roll\nAttempt Deny / Skip]
    WAIT_DENY --> DENIED_RES{deny_roll > manifest_roll?}
    DENIED_RES -- ja --> BLOCKED[Denied! Smite gesperrt]
    DENIED_RES -- nein --> DMGAREA
    DENY -- ja, denied = False --> DMGAREA

    DMGAREA --> APPLY[apply_damage mortal=True\nan Zieleinheit\npsi_result = None\nLog-Eintrag]
```

**`psi_result` — Session-State-Struktur:**
```python
psi_result: dict | None = {
    "faction": str,   # Fraktion des Psykers
    "uid":     str,   # Unit-ID des Psykers
    "roll":    int,   # 2D6-Ergebnis
    "manifested":     bool,       # roll >= 5
    "perils":         bool,       # roll in (2, 12)
    "perils_applied": bool,       # W3-Schaden am Psyker angewendet
    "denied":         bool | None, # None = noch nicht versucht
    "deny_roll":      int | None,
}
```

**Hilfsfunktionen (`psychicPhase.py`):**

| Funktion | Signatur | Zweck |
|---|---|---|
| `has_psyker` | `(units) → bool` | Prüft PSYKER-Keyword |
| `can_deny` | `(units) → bool` | PSYKER-Keyword ODER `"gloom_prism"` in `unit.rules` |
| `initial_deny_state` | `(opponent_units) → bool \| None` | `False` wenn `can_deny(opponent_units)` nein (kein Deny-Versuch möglich, S129-Fix), sonst `None` (wartet auf Deny-Versuch) |
| `smite_targets` | `(selected_targets, caster_faction) → list` | Smite-Ziele = gewählte Einheiten fremder Fraktion; Klick-Auswahl via Unit-Cards des inaktiven Spielers (`_TARGET_PHASES` in `unitCard.py` muss `"psychic"` enthalten, S129-Fix) |
| `is_perils` | `(roll) → bool` | `roll in (2, 12)` |
| `smite_damage_die` | `(roll) → str` | `"W6"` bei ≥ 11, sonst `"W3"` |
| `deny_succeeds` | `(manifest, deny) → bool` | `deny > manifest` (strikt größer) |

**Bannversuch — Canoptek Spyder (Gloom Prism):**
- Kein PSYKER-Keyword — Bannfähigkeit via `"gloom_prism"` in `unit.rules`
- Direkt über `can_deny()`-Check, nicht über Ability Engine (kein Effect-Typ `"deny_psychic"`)
- Vollständige Ability-Engine-Abstraktion: Ziel 4i

**Scope (Ziel 4f):** Nur Smite (WC 5). Blessing-Flow (befreundetes Ziel) folgt später.

**Code-Referenzen:**
- `src/gameMechanic/psychicPhase.py` — Handler + alle Hilfsfunktionen
- `data/wh40k_9e/orks/army.yaml` — Weirdboy + Wurrboy (PSYKER-Einheiten)
- `data/wh40k_9e/necrons/army.yaml` — Canoptek Spyder (`rules: [gloom_prism]`)
- Tests: `tests/gameMechanic/test_psychic_phase.py`

---

## P-13 — Angriffsphase — vollständiger Ablauf

```mermaid
flowchart TD
    A[Angriffsphase beginnt] --> B[Spieler wählt Einheit ▶]
    B --> C{advanced?}
    C -- ja --> NOCHARGE[Warnung: Advanced — kein Angriff möglich]
    C -- nein --> D{retreated?}
    D -- ja --> NOCHARGE
    D -- nein --> E{in_melee?}
    E -- ja --> NOCHARGE2[Warnung: Already in melee — kein Angriff]
    E -- nein --> F[Spieler wählt Ziel-Einheit via gegnerischer Armeeliste ▷]
    F --> G{Ziel ausgewählt?}
    G -- nein --> INFO[Info: Select one or more targets to charge]
    G -- ja --> H[Ziel-Einheitsnamen anzeigen\nHinweis: Roll 2D6, must reach target]
    H --> I{Spieler klickt Charge Successful?}
    I -- ja --> J[set_charged für Angreifer\nenter_melee für Angreifer + Ziel\nlog_action charge ... success]
    I -- nein --> K{Spieler klickt Charge Failed?}
    K -- ja --> L[log_action charge ... failed\nkeine Bewegung]
    J --> M[selected_targets leeren\nst.rerun]
    L --> M

    A --> HI[Inaktiver Spieler: Heroic Intervention]
    HI --> N{CHARACTER-Einheit\neligibel?}
    N -- nein --> SKIP[kein Angebot]
    N -- ja --> O[Button: Intervene pro Einheit]
    O --> P[turn_flags.heroic_intervened = True\nenter_melee mit Angreifer\nlog_action]
```

**Eligibility Heroic Intervention:** Einheit ist CHARACTER, nicht destroyed, nicht bereits in_melee, `heroic_intervened` noch nicht gesetzt.

**Overwatch:** Im inaktiven Bereich angezeigt: *„Overwatch: only unmodified 6s hit."* — kein eigener Ablauf implementiert (Scope Ziel 4d).

**Code-Referenzen:**
- `src/gameMechanic/chargephase.py` — Handler, `_active_charge`, `_render_heroic_intervention`
- `src/gameMechanic/unit_mutations.py: set_charged`, `enter_melee`
- Tests: `tests/gameMechanic/test_charge_phase.py`

---

## P-14 — Nahkampfphase — vollständiger Ablauf

```mermaid
flowchart TD
    A[Nahkampfphase beginnt] --> PRIO[Nicht-aktiver Spieler hat Kampfpriorität\nwählt zuerst eine Einheit]
    PRIO --> B[Spieler wählt Einheit ▶]
    B --> C{can_fight?\nin_melee ODER charged this turn}
    C -- nein --> WARN[Warnung: Not in melee — no fight action]
    C -- ja --> D{fights_first Keyword?}
    D -- ja --> INFO1[Info: Fights First — activates before others]
    D -- nein --> E{charged this turn?}
    E -- ja --> INFO2[Hinweis: Fights first charged this turn]
    E -- nein --> F[Nahkampfwaffen anzeigen\nA/WS/S/AP/D pro Waffe]

    F --> G[Spieler wählt Ziel ▷ aus gegnerischer Armeeliste]
    G --> H{Ziel selected?}
    H -- nein --> HINT[Caption: Designate a target to resolve attacks]
    H -- ja --> I{is_target_engaged?\nZiel in melee_with des Angreifers}
    I -- nein --> WARN2[Warnung: Target not engaged — select engaged enemy]
    I -- ja --> FORM[render_attack_form\nuse_melee=True\nAttack-Sequenz via combat.py]

    FORM --> J[Spieler gibt Hits/Wounds/Saves ein\nApply Damage]
```

**Kampfpriorität (9E):** Der nicht-aktive Spieler wählt als erster eine Einheit zum Kämpfen. Danach alternierend.

**Engagierung-Check:** `_is_target_engaged` prüft ob das Ziel in `unit_state.melee_with` des Angreifers steht. Nicht engagierte Einheiten können nicht angreifen.

**Code-Referenzen:**
- `src/gameMechanic/fightPhase.py` — Handler, `can_fight`, `_is_target_engaged`, `_render_display`
- `src/uiLayout/_common.py: render_attack_form` — Angriffsformular (use_melee=True)
- Tests: `tests/gameMechanic/test_fight_phase.py`

---

## P-15 — Moralphase — vollständiger Ablauf

```mermaid
flowchart TD
    A[Moralphase beginnt] --> B{Einheit hat lost_models_this_turn > 0?}
    B -- nein --> SKIP[Success: Keine Verluste — kein Moraltest]
    B -- ja --> C{models_max == 1?}
    C -- ja --> SKIP
    C -- nein --> D{unit destroyed?}
    D -- ja --> SKIP
    D -- nein --> E{morale_tested bereits gesetzt?}
    E -- ja --> RESULT[Ergebnis anzeigen:\ngeflohen oder bestanden]
    E -- nein --> F[Berechne threshold = Ld − lost + 1]

    F --> G{threshold > 6?}
    G -- ja --> AUTOPASS[Success: Kann nicht fehlschlagen\nButton: Bestätigen auto-bestanden]
    AUTOPASS --> SET[turn_flags.morale_tested = True\nlog_action]

    G -- nein --> H{threshold ≤ 1?}
    H -- ja --> ALWAYS[Error: Schlägt immer fehl]
    H -- nein --> NORM[Anzeige: Schlägt fehl ab W6-Ergebnis X]

    ALWAYS --> BUTTONS[Buttons: ✓ Bestanden / ✗ Fehlgeschlagen]
    NORM --> BUTTONS

    BUTTONS --> PASS{Bestanden geklickt?}
    PASS -- ja --> SET
    PASS -- nein --> FAIL{Fehlgeschlagen geklickt?}
    FAIL -- ja --> INPUT[Eingabe: Wie viele Modelle geflohen?\nmin=1 max=models]
    INPUT --> CONFIRM[Button: Bestätigen]
    CONFIRM --> FLEE[flee_models: models − fled\nlost_models_this_turn + fled\nmorale_tested = True\nlog_action]
```

**Befreiungscheck:** Einheiten mit `models_max == 1` sind grundsätzlich befreit (kein Moraltest).

**Threshold-Formel:** `threshold = leadership − lost_models_this_turn + 1`
- Schlägt fehl wenn W6 ≥ threshold
- `threshold > 6` → kann nie fehlschlagen (auto-bestanden)
- `threshold ≤ 1` → schlägt immer fehl

**Code-Referenzen:**
- `src/gameMechanic/moralePhase.py` — Handler, `_fail_threshold`, `_render_unit_morale`
- `src/gameMechanic/unit_mutations.py: flee_models`
- Tests: `tests/gameMechanic/test_morale_phase.py`
