# Unit States & Badge System

> Dieses Dokument beschreibt das Badge-Vokabular, die Zustandsübergänge und die
> Anzeigelogik für Einheiten-Badges in Arbiter.
> Badges sind digitale Spielmarker — sie bilden immer den Regelzustand ab, nie interne Felder.

---

## Badge-Vokabular

### Persistente Badges (rundenübergreifend, kein Zugwechsel-Reset)

| Badge | Zustand | Feld im State |
|---|---|---|
| `IN MELEE` | Einheit ist im Nahkampf gebunden | `in_melee = True` |
| `RESERVE` | Einheit in Reserve gehalten | `in_reserve = True` |

### Ephemere Bewegungs-Badges (mutex — Zugstart-Default: `STATIONARY`)

| Badge | Bedeutung | Einschränkungen |
|---|---|---|
| `STATIONARY` | Hat sich nicht bewegt | keine |
| `MOVED` | Normal bewegt | keine |
| `ADVANCED` | Vorgestoßen | ✗ Schuss (außer Assault), ✗ Charge |
| `RETREATED` | Aus Nahkampf zurückgezogen — löscht `IN MELEE` | ✗ Schuss, ✗ Charge |
| `CHARGED` | Angestürmt — impliziert `IN MELEE`, kämpft zuerst | — |

### Aktions-Badges (additiv zum Bewegungs-Badge)

| Badge | Gesetzt wann | Verhalten |
|---|---|---|
| `SHOT` | Nach Schussauflösung (`render_attack_form`, phase_key="shooting") | Immer additiv |
| `FOUGHT` | Nach Kampfauflösung (`render_attack_form`, phase_key="fight") | Ersetzt `CHARGED` in der Anzeige |

### Spezial-Badges

| Badge | Reset-Zeitpunkt | Feld |
|---|---|---|
| `MWBD` | Zugwechsel (`_reset_turn_state`) | `my_will_be_done_active` |

---

## Anzeigelogik — Priorität

```
Bewegungs-Slot (mutex):
  FOUGHT > CHARGED > MOVED | ADVANCED | RETREATED | STATIONARY

Aktion (additiv):
  SHOT zeigt immer neben dem aktuellen Bewegungs-Slot

Persistent:
  IN MELEE zeigt immer — außer CHARGED ist aktiv (impliziert IN MELEE)
  FOUGHT unterdrückt IN MELEE NICHT — beide zeigen zusammen

Kombinationen:
  FOUGHT + IN MELEE  → kämpfte, noch gebunden
  SHOT + CHARGED     → schoss und chargte in gleicher Runde
  SHOT + FOUGHT + IN MELEE → voll aktiviert, noch gebunden
```

### Implementierung (`state_badges_html`)

```
1. Bewegungs-Slot bestimmen:
     fought?    → FOUGHT
     charged?   → CHARGED
     movement_choice in map AND NOT in_reserve → MOVED | STATIONARY | ADVANCED | RETREATED
     sonst      → kein Slot

2. SHOT additiv hinzufügen (wenn shot=True)

3. IN MELEE hinzufügen (wenn in_melee=True AND slot != CHARGED)

4. RESERVE hinzufügen (wenn in_reserve=True)

5. MWBD hinzufügen (wenn my_will_be_done_active=True)
```

---

## Zustandsübergänge — 13 Szenarien

| # | Startzustand | Bewegung | Fernkampf | Angriff | Nahkampf | Zugwechsel |
|---|---|---|---|---|---|---|
| 1 | STATIONARY | stationary | schießt | — | — | STATIONARY |
| 2 | STATIONARY | MOVED | schießt | — | — | STATIONARY |
| 3 | STATIONARY | ADVANCED | — | — | — | STATIONARY |
| 4 | STATIONARY | MOVED | schießt | Charge ✓ | kämpft | IN MELEE |
| 5 | STATIONARY | MOVED | — | Charge ✓ | kämpft | IN MELEE |
| 6 | STATIONARY | MOVED | — | Charge ✗ | — | STATIONARY |
| 7 | STATIONARY | MOVED | — | Charge ✓ | noch nicht | — |
| 8 | IN MELEE | stationary | — | — | kämpft | IN MELEE |
| 9 | IN MELEE | stationary | — | — | Feind vernichtet | STATIONARY |
| 10 | IN MELEE | RETREATED | — | — | — | STATIONARY |
| 11 | IN RESERVE | (Runde 1) | — | — | — | IN RESERVE |
| 12 | IN RESERVE | deploy (Runde ≥ 2) | — | — | — | STATIONARY |
| 13 | STATIONARY | MWBD aktiv | … | … | … | STATIONARY (MWBD cleared) |

### Szenario 4 — Badge-Verlauf im Detail

```
Zugstart           → STATIONARY
nach Bewegung      → MOVED
nach Schuss        → MOVED + SHOT
nach Charge-Erfolg → CHARGED + SHOT        (MOVED suppressed)
nach Kampf         → FOUGHT + SHOT + IN MELEE  (CHARGED suppressed by FOUGHT)
Zugwechsel         → IN MELEE              (ephemere Badges reset, persistent bleibt)
```

### Szenario 9 — Feind vernichtet (melee auto-clear)

```
Zugstart           → IN MELEE
nach Kampf         → IN MELEE + FOUGHT
Feind destroyed    → leave_melee() auto-called (apply_damage, melee_with not empty)
                   → FOUGHT                 (IN MELEE erlischt)
Zugwechsel         → STATIONARY
```

---

## Zugwechsel-Reset (`_reset_turn_state`)

Zurückgesetzt bei Zugwechsel (alle Einheiten beider Fraktionen):

| Feld | Reset-Wert |
|---|---|
| `turn_flags.*` | `False` |
| `movement_choice` | `"stationary"` |
| `lost_models_this_turn` | `0` |
| `my_will_be_done_active` | `False` |

Nicht zurückgesetzt (persistent):

- `in_melee`, `melee_with`
- `in_reserve`
- `current_wounds`, `models`, `destroyed`

---

## Code-Referenzen

| Was | Wo |
|---|---|
| Badge-HTML-Rendering | `src/uiLayout/_common.py: state_badges_html()` |
| Badge-HTML (unitCard) | `src/uiLayout/unitCard.py: _state_badges_html()` |
| SHOT/FOUGHT setzen | `src/uiLayout/_common.py: render_attack_form()` |
| MWBD-Reset-Bug | `src/gameMechanic/game_state.py: _reset_turn_state()` |
| Melee auto-clear | `src/gameMechanic/unit_mutations.py: apply_damage()` |
| Tests | `tests/uiLayout/test_common.py` |
