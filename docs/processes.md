# Arbiter — Process Diagrams

> Numbering: P-NN (global unique). Find by phase or topic in the index below.
> Format: Mermaid flowcharts. Render in any Markdown viewer with Mermaid support.

---

## Index

| Nr.  | Prozess                                          | Phase(n)           |
|------|--------------------------------------------------|--------------------|
| P-01 | Unit wählen / abwählen                           | alle               |
| P-02 | Gegner-Einheit als Ziel designieren              | shooting/charge/fight |
| P-03 | Phasenstadien — Weiter-Logik (PhaseRunner)       | alle               |
| P-04 | Effektbestätigung — Schaden in PlayerArea        | alle (Effekt-Trigger) |
| P-05 | CommandPhase — Living Metal Heilung              | command            |
| P-06 | GO-Sichtbarkeit — Prüfkette                      | alle (Stratagems)  |
| P-07 | Schussphase — vollständiger Ablauf               | shooting           |
| P-08 | AttackSequence — Auflösungsreihenfolge           | shooting / fight   |
| P-09 | PhaseRunner — start → active → end              | alle               |

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

## P-03 — Phasenstadien — Weiter-Logik (alle Phasen)

Jede Phase durchläuft drei Stadien: **start → active → end**.
Der „→"-Pfeil springt erst durch Stadien, dann zur nächsten Phase.

```mermaid
flowchart TD
    A[Spieler klickt →] --> B{phase_stage?}
    B -- start --> C{gibt es Effekte\nfür 'active'?}
    C -- ja --> D[phase_stage = active\nst.rerun]
    C -- nein --> E{gibt es Effekte\nfür 'end'?}
    E -- ja --> F[phase_stage = end\nst.rerun]
    E -- nein --> G[next_phase\nphase_stage = start für neue Phase]
    B -- active --> E
    B -- end --> H[next_phase\nphase_stage = start]
    D --> Z[PlayerArea zeigt\nrelevante Aktionen für Stadium]
    F --> Z
    G --> Z
    H --> Z
```

**Hinweis:** Kein hartes Sperren — nur ein Hinweis wenn End-Effekte existieren.
Ein Phasensprung ist immer möglich (bewusste Entscheidung des Spielers).

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
    A[Befehlsphase beginnt\nphase_stage = start] --> B[resolve_command_start\nCP +1 wenn Battle-Forged]
    B --> C[get_triggered_abilities\nphase=command, stage=start]
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
    B --> C{Stratagem-Phase\n= aktuelle Phase?}
    C -- nein --> HIDE[nicht anzeigen]
    C -- ja --> D{Stratagem-Stage\n= aktueller phase_stage?}
    D -- nein --> HIDE
    D -- ja --> E{Bedingungen\nerfüllt?}
    E -- nein --> HIDE
    E -- ja --> F{Bereits diese\nPhase eingesetzt?}
    F -- ja --> GREY[anzeigen, ausgegraut]
    F -- nein --> G{CP ausreichend?}
    G -- nein --> GREY
    G -- ja --> CLICK[anzeigen, klickbar]
```

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

## P-09 — PhaseRunner — start → active → end (alle Phasen)

`phase_runner.py` ist der einzige Eintrittspunkt für `gameActionsArea.py`.

```mermaid
flowchart TD
    AREA[gameActionsArea\nruft render_current_phase auf] --> PR[PhaseRunner\nliest state.phase + state.phase_stage]
    PR --> REG{PHASE_REGISTRY\nHandler gefunden?}
    REG -- nein --> ERR[Fehler: unbekannte Phase]
    REG -- ja --> STAGE{phase_stage?}

    STAGE -- start --> HS[get_triggered_abilities\nphase, 'phase_start'\n→ Ability-Hook-Liste]
    HS --> RS[handler.render_start\nstate + triggered]

    STAGE -- active --> RA[handler.render_active\nstate]

    STAGE -- end --> HE[get_triggered_abilities\nphase, 'phase_end'\n→ Ability-Hook-Liste]
    HE --> RE[handler.render_end\nstate + triggered]

    RS --> WEITER[Spieler klickt →\nadvance_stage aufgerufen]
    RA --> WEITER
    RE --> WEITER

    WEITER --> ADV{Welche stage\nist aktuell?}
    ADV -- start --> TOACTIVE[phase_stage = active\nst.rerun]
    ADV -- active --> TOEND[phase_stage = end\nst.rerun]
    ADV -- end --> NEXT[next_phase\nreset_turn_flags für aktiven Spieler\nphase_stage = start\nst.rerun]
```

**Turn-Flag-Reset** in `advance_stage` beim Übergang `end → next_phase`:
```python
def reset_turn_flags(faction: str, state: dict) -> None:
    units_key = f"{faction.lower()}_units"
    for uid in state[units_key]:
        state[units_key][uid]["turn_flags"] = {
            "advanced": False, "retreated": False,
            "charged": False, "shot": False, "fought": False,
        }
```

**Stub-Phasen** (Ziel 3 — Movement, Charge, Psychic, Morale) implementieren das `PhaseHandler`-Protocol minimal:
- `render_start`: leer
- `render_active`: Phasenname + Info-Text + Hinweis auf turn_flags
- `render_end`: leer

Turn-Flags werden von den Stub-Phasen noch **nicht** gesetzt (folgt in Ziel 4).
