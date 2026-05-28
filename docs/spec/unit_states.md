# Unit States & Badge System

> Dieses Dokument beschreibt das Badge-Vokabular, die Zustandsübergänge und die
> Anzeigelogik für Einheiten-Badges in Arbiter.
> Badges sind digitale Spielmarker — sie bilden immer den Regelzustand ab, nie interne Felder.
> Dieses Dokument dient als Test-Spezifikation: Was hier steht, ist erlaubt.
> Was nicht hier steht, darf die App nicht ermöglichen.

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
| `RETREATED` | Aus Nahkampf zurückgezogen — löscht `IN MELEE` | ✗ Schuss, ✗ Charge, ✗ Kämpfen |
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

## Sektion 1: Transition-Constraints

Welche Folge-Aktionen ein Bewegungszustand erlaubt oder sperrt:

| Bewegungszustand | Schießen | Charge ansagen | Kämpfen (wenn in Melee) | Advance | Retreat |
|---|---|---|---|---|---|
| STATIONARY | ✓ | ✓ | ✓ | — | nur wenn IN MELEE |
| MOVED | ✓ | ✓ | ✓ | — | — |
| ADVANCED | nur Assault-Waffen | ✗ | ✓ | — | — |
| RETREATED | ✗ | ✗ | ✗ | — | — |
| IN MELEE (stationary) | ✗ | ✗ | ✓ | ✗ | ✓ |

**Constraint-Regeln:**
- IN MELEE → Nur STATIONARY oder RETREAT im Bewegungsschritt erlaubt.
- RETREATED → Keine weiteren Bewegungsoptionen mehr in diesem Zug.
- Deployed from Reserve → gilt als MOVED (kann schießen, angreifen, kämpfen; kein Advance).

---

## Sektion 2: Aktiver Spieler — vollständige Szenarien

Alle kanonischen Pfade für einen kompletten Zug des aktiven Spielers:

| # | Start | Bewegung | Schuss | Charge | Kampf | Rundenende |
|---|---|---|---|---|---|---|
| 1 | STATIONARY | stationary | — | — | — | STATIONARY |
| 2 | STATIONARY | stationary | schießt | — | — | STATIONARY |
| 3 | STATIONARY | MOVED | — | — | — | STATIONARY |
| 4 | STATIONARY | MOVED | schießt | — | — | STATIONARY |
| 5 | STATIONARY | MOVED | — | Charge ✗ | — | STATIONARY |
| 6 | STATIONARY | MOVED | — | Charge ✓ | kämpft | IN MELEE |
| 7 | STATIONARY | MOVED | schießt | Charge ✓ | kämpft | IN MELEE |
| 8 | STATIONARY | ADVANCED | — | — | — | STATIONARY |
| 9 | IN MELEE | stationary | — | — | kämpft (Feind überlebt) | IN MELEE |
| 10 | IN MELEE | stationary | — | — | kämpft (Feind vernichtet) | STATIONARY |
| 11 | IN MELEE | RETREATED | — | — | — | STATIONARY |
| 12 | IN RESERVE (R1) | — | — | — | — | IN RESERVE |
| 13 | IN RESERVE (R≥2) | MOVED (deploy) | schießt | — | — | STATIONARY |
| 14 | IN RESERVE (R≥2) | MOVED (deploy) | — | Charge ✓ | kämpft | IN MELEE |

### Szenario 7 — Badge-Verlauf im Detail (MOVED + SHOT + CHARGE + FOUGHT)

```
Zugstart           → STATIONARY
nach Bewegung      → MOVED
nach Schuss        → MOVED + SHOT
nach Charge-Erfolg → CHARGED + SHOT        (MOVED suppressed)
nach Kampf         → FOUGHT + SHOT + IN MELEE  (CHARGED suppressed by FOUGHT)
Zugwechsel         → IN MELEE              (ephemere Badges reset, persistent bleibt)
```

### Szenario 10 — Feind vernichtet (melee auto-clear)

```
Zugstart           → IN MELEE
nach Kampf         → IN MELEE + FOUGHT
Feind destroyed    → leave_melee() auto-called (apply_damage, melee_with not empty)
                   → FOUGHT                 (IN MELEE erlischt)
Zugwechsel         → STATIONARY
```

### Szenario 13/14 — Deployment aus Reserve

```
Bewegung           → set_deployment("normal") + set_movement_status("moved")
                   → MOVED (nicht ADVANCED — darf schießen und angreifen)
Regelbasis         → "gilt als Bewegungswert in Zoll bewegt" (Schritt 2: Verstärkungen)
```

---

## Sektion 3: Passiver Spieler — Zustände und Trigger

Der passive Spieler hat keine normale Zugabfolge, reagiert aber auf Aktionen des aktiven Spielers.

### Passive Szenarien

| # | Passive-Start | Ursache | Zustand danach | Trigger/Effekt |
|---|---|---|---|---|
| P1 | STATIONARY | Beschossen (Schaden erhalten) | STATIONARY (Wunden reduziert) | Living Metal (nächste BP), Reanimation Protocols (nach Angriff) |
| P2 | STATIONARY | Feindl. Charge erfolgreich | IN MELEE | Overwatch vor Angriffswurf möglich |
| P3 | STATIONARY | Heroische Intervention | IN MELEE | Nur CHARACTERMODELL-Einheiten |
| P4 | IN MELEE | Kämpft in Nahkampfphase | IN MELEE + FOUGHT oder FOUGHT | RP wenn Modelle verloren |

### P1 — Beschossen werden

- Einheit erhält Schaden → `current_wounds` sinkt, `lost_models_this_turn` steigt.
- Badge: bleibt STATIONARY/MOVED etc. — Beschuss ändert keine Bewegungs-Badges.
- **Living Metal**: Wird am Beginn der nächsten eigenen Befehlsphase ausgelöst (+1 LP pro Modell).
- **Reanimation Protocols**: Können nach feindlichem Angriff (Nahkampfphase oder Fernkampfphase) ausgelöst werden, wenn Modelle verloren gingen.

### P2 — Angegriffen werden (Charge)

- Aktiver Spieler sagt Charge an → passive Einheit wird Ziel.
- **Overwatch (Abwehrfeuer)**: Die passive Einheit darf schießen, **bevor** der Angriffswurf gewürfelt wird.
  - Nur unmodifizierte 6er treffen (unabhängig von BF und Modifikatoren).
  - Setzt **kein SHOT-Flag** — Abwehrfeuer ist kein regulärer Schuss.
  - Nicht möglich wenn passive Einheit selbst IN MELEE ist.
- Bei erfolgreichem Charge: `enter_melee()` → passive Einheit geht IN MELEE über.

### P3 — Heroische Intervention

- Ausgelöst nach allen Charges des aktiven Spielers (Schritt 2: Heroische Interventionen).
- **Bedingung:** CHARACTERMODELL-Einheit, nicht bereits IN MELEE, ≤ 3" horizontal / ≤ 5" vertikal von einer feindlichen Einheit entfernt.
- **Bewegung:** Bis zu 3" — jedes Modell muss näher an nächstem feindlichen Modell enden.
- **Ergebnis:** `enter_melee()` → IN MELEE.
- Maximal eine Heroische Intervention pro feindlicher Angriffsphase. Nie in eigener Angriffsphase.

### P4 — Kämpfen in der Nahkampfphase

- Die Nahkampfphase beginnt mit dem **inaktiven** Spieler.
- Passive Einheiten IN MELEE (aber nicht charged) kämpfen in regulärer Reihenfolge.
- **Ablauf:** Nachrücken (Pile In, bis 3") → Nahkampfattacken → Neu ordnen (Consolidation, bis 3").
- **Badge-Ergebnis:**
  - Feind überlebt → FOUGHT + IN MELEE
  - Feind vernichtet → `leave_melee()` → FOUGHT (IN MELEE erlischt)
- **RP-Trigger:** Wenn Modelle verloren gingen, Reanimation Protocols nach dem Angriff.

---

## Sektion 4: Verbotene Transitionen

Explizite Negativliste — diese Übergänge darf die App **nie** ermöglichen:

| Von | Nach | Grund |
|---|---|---|
| RETREATED | Bewegung (MOVED/ADVANCED/STATIONARY) | Rückzug ist final für diesen Zug |
| RETREATED | Schuss | Kein Schuss nach Rückzug |
| RETREATED | Charge | Kein Angriff nach Rückzug |
| RETREATED | Kämpfen | Kein Kampf nach Rückzug |
| ADVANCED | Charge | Kein Angriff nach Vorrücken |
| ADVANCED | Schuss (außer Assault) | Kein regulärer Schuss nach Vorrücken |
| IN MELEE + STATIONARY | MOVED | Einheit im Nahkampf kann sich nicht normal bewegen |
| IN MELEE + STATIONARY | ADVANCED | Einheit im Nahkampf kann nicht vorrücken |
| Deploy (MOVED) | ADVANCED | Deployments zählen als MOVED, nicht ADVANCED |

### Regressionstest-Pflicht

Der folgende Bug muss als dauerhafter Regressionstest abgedeckt sein:

> **Bug:** Retreated → dann Stationary → dann MOVED/ADVANCED möglich  
> **Ursache:** `set_movement_status("stationary")` setzt `flags["retreated"] = False`  
> **Fix:** Early-Return in `_active_movement` wenn `already_retreated = True`

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
| Melee auto-clear | `src/gameMechanic/unit_mutations.py: apply_damage()` |
| Bewegungs-Buttons + Rückzug-Fix | `src/gameMechanic/movementPhase.py: _active_movement()` |
| Deployment aus Reserve | `src/gameMechanic/movementPhase.py: _render_reinforcements_step()` |
| Tests (Badges) | `tests/uiLayout/test_common.py` |
| Tests (Bewegungs-Transitionen) | `tests/gameMechanic/test_movement_transitions.py` |
