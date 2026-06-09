# Ziel 6 — UI-Overhaul, ArmyCard, Attackensequenz, Fähigkeiten-Integration 🔄

**Voraussetzung:** Ziel 5 (inkl. 5i) abgeschlossen. ✅

---

## Übersicht

Ziel 6 besteht aus sieben Teilzielen, die unabhängig voneinander implementiert werden können:

| Teilziel | Thema | Abhängigkeiten |
|----------|-------|----------------|
| **6a** ✅ | gameHeader Redesign | – |
| **6b** ✅ | armyCard — generisches Fähigkeitssystem | – |
| **6c** ✅ | gameProtocoll — Stratagems als Default, Modifier-Export | 6b |
| **6d** ✅ | Attackensequenz — simultane Darstellung (Basis-Implementation) | 6b, 6c |
| **6d-v2** 🔵 | Attackensequenz — vollständiges UI-Redesign (Design abgestimmt) | 6d |
| **6e** ✅ | Fähigkeiten-Integration — Command Protocols regelkonform + Stratagem-Visibility-Fix | 6b |
| **6f** | Ability-Badges und Keyword-Highlighting auf unitCard | 6e |
| **6g** ✅ (teilw.) | Game Log — Archiv + Setup-UI | – |
| **6h** ✅ (teilw.) | Generisches Fraktion-Fähigkeits-System | 6b |
| **Daten-Review** 🔄 | YAML-Vollständigkeit (Silent King ✅, weitere Einheiten offen) | – |

---

## 6a — gameHeader Redesign

**Ziel:** Der Header sieht professionell aus. Steuerelemente sind konsistent angeordnet.

### Layout-Spec

```
┌──────────────────────────────────────────────────────────────────┐
│  [Fraktion A]              Runde 2              [Fraktion B]      │
│                                                                  │
│   3 VP  4 CP     [MOVEMENT] [SHOOTING] [CHARGE] [FIGHT] [MORALE] │
│                         ←   ↺   →                               │
│                   ← auf derselben Zeile wie ↺ und →             │
└──────────────────────────────────────────────────────────────────┘
```

- VP und CP auf **einer Zeile**, z.B. `3 VP  4 CP` — Zahl + Label inline, kein Label über der Zahl
- Linke und rechte Score-Gruppe auf **exakt derselben Höhe**
- `←`, `↺`, `→` auf **derselben untersten Zeile** im Center-Bereich
- Phase-Badges **doppelt so groß** wie aktuell (padding erhöhen, font-size hochsetzen)
- Aktive Phase-Badge: deutlich hervorgehoben (Farbe + Border)

### Tasks

- [x] `gameHeader.py`: 4-Zeilen-Layout (Runde / Phase·Spieler / Scores+Badges / Navigation)
- [x] `gameHeader.py`: VP/CP Label gleich groß wie Zahl (`4.5rem bold`)
- [x] `gameHeader.py`: `←`, `↺`, `→` in eine gemeinsame Row, zentriert
- [x] `gameHeader.py`: Phase-Badges in Zeile 3 Mitte integriert

---

## 6b — armyCard — generisches Fähigkeitssystem

**Ziel:** Die armyCard zeigt korrekte Fraktionsdaten und ermöglicht die Aktivierung aller armeeweit relevanten Fähigkeiten — fraktionsunabhängig.

### Bugs

- `faction_dir_for()` fällt auf `"necrons"` zurück wenn `p1_faction_dir`/`p2_faction_dir` nicht gesetzt → Living Metal erscheint bei Adeptus Custodes, WAAAGH fehlt bei Orks
- Command Protocol-Wechsel ist in `gameProtocoll.py` hart auf Necrons verdrahtet
- ⚠️ **armyCard entspricht Stand 2026-06-05 noch nicht vollständig der Spec** — triggered abilities, Wargear-Aktionen und Protokoll-UI nicht korrekt generisch; detaillierter Abgleich mit Spec nötig vor nächster Feature-Session

### Spec

- Fraktions-Keywords als Badges aus den Daten (`army.yaml` oder `units.yaml` keywords), nicht nur Fraktionsname
- Armeefähigkeiten werden **generisch** aktiviert: Die armyCard liest `faction_abilities.yaml` der korrekten Fraktion und rendert phase-abhängige Buttons
- Command Protocol-Wechsel zieht von `gameProtocoll.py` in die armyCard (nur sichtbar wenn Fraktion Protokolle hat)
- WAAAGH-Aktivierung erscheint für Orks in der Befehlsphase
- Aktivierte Fähigkeiten werden im Session-State vermerkt (für Modifier-System in 6d/6e)

### Tasks

- [x] `game_state.py`: `faction_dir_for()` — kein `"necrons"`-Default mehr, KeyError wenn nicht initialisiert
- [x] `armyCard.py`: Triggered-Abilities generisch rendern (unabhängig von Fraktionsname)
- [x] `gameProtocoll.py`: `_render_necron_protocols()` entfernt; `is_necron_faction`-Import entfernt
- [x] `armyCard.py`: Command Protocol-UI (interaktiv in Befehlsphase, read-only sonst) — einziger Einstiegspunkt
- [x] `commandPhase.py`: `_render_command_protocols()`-Aufruf entfernt — NUR armyCard ruft Protokolle auf
- [x] `data/wh40k_9e/orks/faction_abilities.yaml`: WAAAGH-Fähigkeit bereits vorhanden ✓

---

## 6c — gameProtocoll — Stratagems als Default, Modifier-Export

**Ziel:** Stratagems sind der Default-Tab. Verwendete Stratagems propagieren ihre Effekte als Modifier ins Spiel.

### Tasks

- [x] `gameProtocoll.py`: Tab-Reihenfolge getauscht — Stratagems zuerst, Command Protocol zweiter Tab
- [x] `gameObjects/stratagem.py`: `StratagemModifier` Dataclass + optionales `modifier`-Feld auf `Stratagem`
- [x] `gameObjects/loader.py`: `modifier`-Block aus YAML parsen
- [x] `data/wh40k_9e/necrons/stratagems.yaml`: `disruption_fields` (+1 wound), `whirling_onslaught` (-1 wound), `methodical_destruction` (+1 hit)
- [x] `data/wh40k_9e/orks/stratagems.yaml`: `hit_em_harder` (+1 damage), `tough_as_squig_hide` (-1 wound), `wreckaz` (+1 wound)
- [x] `gameMechanic/game_state.py`: `active_modifiers: list[dict]` im Session-State (init + reset + cleanup bei Phasenwechsel)
- [x] `gameProtocoll.py`: Modifier bei Stratagem-Nutzung in `active_modifiers` schreiben

---

## 6d — Attackensequenz — simultane Darstellung

**Ziel:** Treffer-, Verwundungs-, Rettungswurf, FNP und Schaden werden **gleichzeitig** angezeigt. Kein schrittweises Klicken. Modifikatoren aus Fähigkeiten, Ausrüstung und Stratagems werden transparent aufgelistet.

### Implementierter Zustand (superseded by 6d-v2)

> Das folgende Diagramm beschreibt den ursprünglichen Plan, der in `render_attack_form()` umgesetzt wurde. Es ist nicht mehr das Zielbild — das vollständige Redesign ist in **6d-v2** specifiziert.

```
Angreifer (links):          Verteidiger (rechts):
──────────────────          ───────────────────────
TREFFER  BS 3+              RÜSTUNGSWURF/RETTUNGSWURF
  Modifier-Stack              Sv + AP → effektiv
  → modifizierter Wert      FEEL NO PAIN (falls vorhanden)
                            SCHADEN-Input + Mortal-Input
VERWUNDUNG  S vs T          [Apply-Button]
  Modifier-Stack
  → modifizierter Wert
```

### Regeln

- **Gleichzeitig:** Alle Blöcke werden auf einmal gerendert, keine Weiter-Buttons
- **Angreifer-Seite:** Trefferwurf + Verwundungswurf (mit Modifier-Stack + Quellen)
- **Verteidiger-Seite:** Rettungswurf (normal + Invulnerable, bester wird genommen) + FNP (nur wenn vorhanden) + Schadenseingabe
- **FNP-Negation:** Generisch über Waffenfähigkeits-Flag `ignores_fnp: true` in `weapons.yaml` — nicht hardcoded auf Nightbringer
- **Stratagem-Buttons:** Erscheinen direkt beim betreffenden Würfels-Block; zeigen CP-Kosten; sind nur clickbar wenn CP verfügbar und nicht bereits verwendet
- **Nahkampf / Overwatch:** Inaktiver Spieler kann Angreifer sein — Seiten-Zuweisung basiert auf `attacker_faction`, nicht `active`
- **Schaden:** User gibt nur finalen zugewiesenen Schaden ein; Zwischenwerte (Anzahl Treffer etc.) werden nicht eingegeben

### Tasks

- [x] `gameMechanic/combat.py`: Funktion `resolve_attack_modifiers(skill, strength, toughness, weapon_type, advanced, modifiers, use_melee)` → strukturierter Modifier-Stack (±1-Cap, Heavy-Penalty)
- [x] `gameMechanic/combat.py`: Funktion `resolve_save(base_save, invuln_save, ap, save_modifiers)` → besten Save (Rüstung vs. Invuln), mit Stack
- [x] `gameMechanic/combat.py`: Funktion `resolve_fnp(fnp, ignores_fnp)` → FNP-Wert oder `None` wenn ignoriert/abwesend
- [x] `uiLayout/_common.py`: `render_attack_form()` komplett neu — 2-Spalten-Layout (Angreifer: Treffer/Verwundung · Verteidiger: Save/FNP/Schaden-Input)
- [x] `gameObjects/weapon.py`: `ignores_fnp: bool` Feld ergänzt
- [x] `gameObjects/loader.py`: `ignores_fnp` aus YAML parsen
- [x] `tests/test_combat_6d.py`: 28 Tests für die 3 neuen Funktionen
- [ ] Prüfen: Shootingphase, Fightphase, Overwatch in Chargephase — alle drei Kontexte korrekt (Overwatch: kein chargePhase.py vorhanden — separater Task)

---

---

## 6d-v2 — Attackensequenz — vollständiges UI-Redesign

**Ziel:** Die `gameActionArea` wird während einer Attackenabhandlung vollständig übernommen. Alle relevanten Würfelwurf-Informationen werden kontextuell angezeigt — ohne dass Zwischenergebnisse (Treffer, Verwundungen) eingegeben werden müssen. Nur Modellverluste und tödliche Verwundungen werden am Ende eingegeben.

**Voraussetzung:** Ziel 6d (Basis-Implementation) abgeschlossen ✅

### Bekannte Bugs (mit 6d-v2 zu beheben)

- [x] **Pistol in Melee**: `can_shoot()` in `shootingPhase.py` — Einheiten im Nahkampf dürfen nur Pistolen abfeuern; alle anderen Waffen müssen ausgeblendet werden. ✅ (2026-06-05)

### Scenario-Mockups (Testhilfe, unabhängig implementierbar)

Infrastruktur bereits vorhanden: `data/scenarios/`, `?scenario=<name>` URL-Parameter, `scenarios.py`.

- [x] `data/scenarios/necrons_shoot_orks.json` — Shooting Phase, Necrons aktiv: Immortals (Tesla Carbines, 5 Modelle) → Ork Boyz (20 Modelle). Selected Unit + Target vorgesetzt. Tesla-Badge sichtbar.
- [x] `data/scenarios/orks_fight_necrons.json` — Fight Phase, Orks aktiv: Boyz (20M) im Nahkampf mit Warriors (10M) + Skorpekh Destroyers (3M, 9LP). Whirling Onslaught aktivierbar (Necron reaktive GO). RP nach Apply relevant.
- [x] `data/scenarios/orks_shoot_necrons.json` — Shooting Phase, Orks aktiv: Boyz mit Sluggas (Pistol 1) → Warriors (einige im Nahkampf → Pistol-Bug sichtbar). CP: Orks 6, Necrons 6.
- [x] `data/scenarios/necrons_fight_orks.json` — Fight Phase, Necrons aktiv: Skorpekh Destroyers (CHARGED) → Boyz. Warriors daneben im Nahkampf (RP relevant nach Verlustanzeige).

**Wichtig:** Keys immer `p1_units` / `p2_units`. Roster: `necrons_alpha.yaml` (p1) + `orks.yaml` (p2). Bestehende Szenarien (`necron_units`-Key) sind fehlerhaft — nicht als Vorlage nutzen.

### Layout-Spec

> ⚠️ **Veraltet — wird durch 6d-v3 ersetzt.** Die Auflösungs-Blöcke (Treffer, Verwundung, Save, Schaden) werden auf Würfel-UI umgestellt. Die Deklarations-Phase bleibt weitgehend unverändert.

Die `gameActionArea` wechselt in zwei Phasen:

**Phase 1 — Deklaration** _(unverändert gültig)_
```
[Angreifer: Intercessors]  →  [+ Ziel hinzufügen ▾]

  ┌─ Ork Boyz ─────────────────────────────────────┐
  │  Waffe: [◉ Bolt Rifle]  [○ Bolt Pistol]        │
  │  Profil: [◉ Standard]  (kein zweites Profil)   │
  │  Modelle auf dieses Ziel: [8] [−][+]  → 8 att  │
  │  [Verteidiger-Aktionen: GO aktivieren ▾]        │
  └─────────────────────────────────────────────────┘
  ┌─ Gretchin ──────────────────────────────────────┐
  │  Waffe: [◉ Bolt Rifle]                         │
  │  Modelle auf dieses Ziel: [2] [−][+]  → 2 att  │
  └─────────────────────────────────────────────────┘
  Verbleibend: 0 / 10 zugeteilt ✓

  [Auflösung starten →]
```

Regeln:
- Triviale Fälle (1 Waffe, 1 Profil) auto-selektiert
- Gesperrte Profile ausgegraut mit Grund (`unit moved`, `stationary required`)
- Pistolen hervorgehoben wenn Einheit `IN MELEE`; alle anderen Waffen ausgegraut
- Reaktive GOs des Verteidigers erscheinen beim jeweiligen Ziel sobald es hinzugefügt wird
- Rapid Fire: Info-Badge `[RAPID FIRE · ½ = 12"]` — kein Toggle, nur Display

**Phase 2 — Auflösung (Tabs)** _(Würfel-UI in 6d-v3 — alte Textdarstellung veraltet)_

```
╔══ Bolt Rifle → Ork Boyz (8 Attacken) ══════════╗   ← veraltet, s. 6d-v3
║  TREFFER  BS 3+  [HEAVY −1]  → effektiv 3+     ║
║  VERWUNDUNG S4 < T5  → 5+  [+1 Wunde] → 4+    ║
║  SAVE Sv6+ / AP-1  INV 5+  FNP —               ║
║  [⚔ Schaden anwenden]    [↺ Zurücksetzen]      ║
╚═════════════════════════════════════════════════╝
```

**Necron RP-Block** _(bleibt unverändert)_:
```
REANIMATION PROTOCOLS
3 Warriors gefallen → 3 Würfel, Erfolg: 5+
[Proto: Undying Legions — Reroll]  [Reanimator +1]
Modelle zurück: [ 0 ] [−][+]
[RP anwenden]  [↺]
```

### Damage-Block — Fallunterscheidung

| Szenario | Eingabe |
|---|---|
| 1LP-Modelle, fester Schaden | `Modelle verloren [0][−][+]` |
| 1LP-Modelle, var. Schaden (D3) | `Modelle verloren [0][−][+]` (Schaden ≥1 = immer tot) |
| nLP-Modelle, fester Schaden | `Modelle verloren [0][−][+]` + `Wunden Frontmodell [0][−][+]` |
| nLP-Modelle, var. Schaden | wie oben + Hinweistext "Würfle D3 pro missgl. Wurf" |
| Tödliche Verwundungen | immer eigener Counter (Übertrag auf nächstes Modell ✓) |

### Cover-Dropdown (im Save-Block)

| Auswahl | Effekt | Phase |
|---|---|---|
| Kein Cover (default) | — | beide |
| Light Cover | +1 auf Rettungswurf | Shooting |
| Dense Cover | −1 auf Trefferwurf | Shooting |
| Heavy Cover | +1 auf Rettungswurf vs. Nahkampf (außer nach Charge) | Fight |

Invulnerable Saves sind von Cover nicht betroffen.

### Tasks

- [x] **Bug P0**: `can_shoot()` — Pistol in Melee erlauben, andere Waffen ausblenden
- [x] Scenario-Mockups (4 JSON-Dateien, s.o.)
- [x] `uiLayout/_common.py`: `render_attack_form()` in `render_attack_declaration()` + `render_attack_resolution()` aufteilen
- [x] `uiLayout/_common.py`: Deklarations-Phase — Ziel-Karten mit Modell-Counter + Waffenwahl + Profilwahl
- [x] `uiLayout/_common.py`: Auflösungs-Tabs — Hit-Block mit Modifier-Stack
- [x] `uiLayout/_common.py`: Wound-Tabelle (5 Zeilen, aktive Zeile highlight, Modifier-Stack-Badges)
- [x] `uiLayout/_common.py`: Save-Block (Rüstung / Invuln / FNP; Cover-Dropdown)
- [x] `uiLayout/_common.py`: Damage-Block (1LP/nLP Fallunterscheidung; Modelle+Wunden-Counter + Mortal Wounds)
- [x] `uiLayout/_common.py`: RP-Block nach Apply (nur Necron-Fraktion + Verluste > 0)
- [x] `uiLayout/_common.py`: Tab-Lock nach Apply + Reset-Button
- [x] `gameMechanic/combat.py`: `apply_damage_attacks(models_lost, wounds_on_front, mortal_wounds, wounds_per_model)` — reine HP-Berechnung
- [x] Weapon-Abilities als Badges im Hit-Block: Tesla, Dakka, Power Klaw, Auto-Hit ✅ (2026-06-05, in 6d-v2; Würfel-UI in 6d-v3)
- [x] Rapid Fire Info-Badge mit Reichweite + berechneter Halbreichweite ✅ (2026-06-05, in 6d-v3)
- [ ] Shooting/Fight Phase Handler: `render_attack_form()` durch neue Funktion ersetzen
- [ ] Tests für neuen Damage-Block + RP-Würfellogik

### Akzeptanzkriterien 6d-v2

- [x] Kein Input für Treffer oder Verwundungen — nur Modellverluste + Tödliche Verwundungen
- [x] Wound-Tabelle zeigt aktive Zeile highlighted; Modifier als Badges sichtbar
- [x] Save-Block: Rüstung / Invuln / FNP getrennt; Cover-Dropdown vorhanden (default: kein Cover)
- [x] Pistolen in Melee: nur Pistolen anzeigbar, Rest ausgegraut
- [x] RP-Block erscheint nach Apply bei Necron-Einheiten mit Verlusten
- [x] Tabs locken nach Apply; Reset bis Phase-End möglich
- [x] Weapon-Ability-Badges (Tesla, Dakka, Power Klaw, Auto-Hit) im Hit-Block ✅ (2026-06-05)
- [x] Scenario-Mockups aufrufbar via `?scenario=necrons_shoot_orks` etc.

### 🔵 6d-v3 — Würfel-UI Redesign (geplant, nächste Session)

Design-Grundlage: Handskizzen `Fotos/IMG_4038–4042` (analysiert 2026-06-06).

**Kernkonzept:** Jeder Würfelblock zeigt eine Reihe von SVG-Würfelfaces (1–6). Ein farbiger **Rahmen** umschließt die Würfel, die einen Treffer/Erfolg bedeuten — Würfel außerhalb des Rahmens sind Misses. Modifier-Fähigkeiten verschieben den Rahmen durch Würfelpaare mit Pfeilen. Eine **vertikale LINE** dient als Ausrichtungshilfe; die **DASHED LINE** zeigt das effektive Ergebnis nach Cap.

**Farbschema des Rahmens (Treffer & Verwundung, max ±1 Cap):**
- 2+/3+ → grüner Rahmen
- 4+ → gelber Rahmen
- 5+/6+ → oranger Rahmen
- [x]-Würfel = immer miss (1 immer; alle außerhalb Rahmen)

**Farbschema Verwundung (Schwelle aus S vs T):**
- 2+ → grün (S ≥ 2×T)
- 3+ → grün (S > T)
- 4+ → gelb (S = T)
- 5+ → orange (S < T)
- 6+ → orange (2×S ≤ T)

**S/T-Modifier (blau):** Fähigkeiten, die S oder T verändern, werden in Blau hervorgehoben. Der Rahmen passt sich an die neue Schwelle an.

**Beim Rettungswurf gilt kein ±1-Cap.**

---

#### Deklarations-Block (`IMG_4038`) — vor dem Trefferblock

```
DEKLARATION  (Shooting / Fight Phase)

YOU have eligible units to shoot / fight
  ▲ [ Einheit auswählen ] ▼

Check conditions (Shooting):
  ✓ moved              → kann schießen
  ✗ advanced           → kann nicht schießen, außer ASSAULT
  ✗ retreated          → kann nicht schießen, außer ability wie "adaptive strategy"
  ✓/✗ HEAVY            → −1 auf Trefferwurf wenn moved AND INFANTRY-unit
  ✓ has_ranged_weapons
  ✓ triggered abilities
  ✗ shot this phase    → bereits geschossen
  … weitere Bedingungen

Atk — eligible unit auswählen
  Shooting:              Fight:
  1. select target       1. select targets
  2. select weapon       2. ...
  3. resolve attacks

─────────────────────────────────────────────────────
Weapon-Auswahl (Shooting) — zeigt #attacks
┌──────────────────────────────────────────────────────────┐
│  #attacks      display Range (especially rapid fire)     │
│                                                          │
│  ☑ Weapon 1  ──────────────────────────────→  target-1   │
│   ...                                                    │
│  ☑ Weapon n                                              │
│  ☐ Weapon n+1   ─────────────────────────────target-2    │
│   ...                                         ...        │
│  ☐ Weapon m                                   target-x   │
│                                                          │
└──────────────────────────────────────────────────────────┘
"close display only / same attack display for fights"
```

---

#### Treffer-Block (`IMG_4039`)

```
TREFFER  8 Würfel

BS/WS    1      2     [3+]    4+     5+     6+
         ┌───┐ ┌───┐  ┌───────────────────────────────┐
         │[x]│ │ · │  │ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │  ← grüner Rahmen (BS 3+)
         └───┘ └───┘  │ │ · │ │ · │ │ · │ │ · │ │ · │ │
         misses       │ └───┘ └───┘ └───┘ └───┘ └───┘ │
                      └───────────────────────────────┘
                      │ (vertikale LINE)
[HEAVY]       ┌───┐ ←-1← ┌───┐                             ← Schwelle schlechter
              └───┘   │  └───┘
[MWBD]        ┌───┐ →+1→ ┌───┐                             ← Schwelle besser
              └───┘   │  └───┘
[Lords Will] ┌───┐    │                                    ← Reroll-Icon im Würfelsymbol (Einheitenfähigkeit)
             └───┘    │
                                                ┌────┐
[Tesla]                                         │+2Hit│    ← Waffenfähigkeit
                                                └────┘
- - - - - - - - - DASHED LINE - - - - - - - - -
Effektiv BS: [3+]  (max ±1 Cap)

Buttons (konditionell — Stratagem, CP-Kosten, Reset):  [Aktivieren]  [↺]

Rahmen-Farbe nach effektivem BS: 2+/3+ grün · 4+ gelb · 5+/6+ orange
[x]-Würfel: 1 = immer miss; alle Würfel links des Rahmens = miss (·)
```

---

#### Verwundungs-Block (`IMG_4040`) — gleiche Komponente wie Treffer

```
VERWUNDUNG

S = [5]   >   T = [4]   →   Schwelle: 3+

(Modifier auf S oder T erscheinen in Blau:)
S = [5] + [+1] (blau) = [6]  →  T = [4]  →  neue Schwelle: 3+ (S≥2T möglich)
S = [5]  →  T = [4] + [+1] (blau) = [5]  →  neue Schwelle: 4+ (S=T)
Rahmenfarbe passt sich automatisch an neue Schwelle an.

        1      2     [3+]    4+     5+     6+
        ┌───┐ ┌───┐  ┌────────────────────────────────┐
        │[x]│ │ · │  │ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │  ← grüner Rahmen (3+, S > T)
        └───┘ └───┘  │ │ · │ │ · │ │ · │ │ · │ │ · │ │
        misses        │ └───┘ └───┘ └───┘ └───┘ └───┘ │
                      └────────────────────────────────┘
        │ (vertikale LINE)
[Badge1]  ┌───┐ →+1→ ┌───┐   ← Wound-Modifier (Schwelle verbessert)
          └───┘        └───┘
[Badge2]  ┌───┐ ←-1← ┌───┐   ← Wound-Modifier (Schwelle schlechter)
          └───┘        └───┘
[Reroll]  ┌───┐                ← rot
          └───┘
[Miss]    ┌───┐                ← rot
          └───┘
- - - - - - - - - DASHED LINE - - - - - - - - -
Effektiv: [3+]  (max ±1 Cap)

Farbschema: 2+/3+ grün · 4+ gelb · 5+/6+ orange
```

---

#### Rettungswurf-Block (`IMG_4041`)

```
[Standard]
normal   2+  [3+]  4+  5+  6+    ← Basis-Save 3+ (highlighted, grün)
invuln   2+   3+  [4+] 5+  6+    ← Invuln 4+ (highlighted, gelb)

[mit AP & Cover]
normal  2+  [3+]  4+  5+  6+
                   │  (vertikale LINE — markiert Basis-Schwelle)
AP-2    ┌─┐ →-2→  ┌─┐  rot        ← Threshold 2 Schritte schlechter → 5+
        └─┘       └─┘
cover   ┌─┐ →+1→  ┌─┐             ← Cover verbessert um 1 → 4+
        └─┘       └─┘
eff.    ┌─┐ →-1→  ┌─┐             ← Netto: 4+ (gelb)
        └─┘       └─┘

invuln  2+   3+  [4+]  5+  6+
────── AP/Cover wirken nicht auf Invuln: LINE ──────

[Quantum Shielding]: Invuln direkt auf 4+ gesetzt (kein Modifier-Würfelpaar, direkter Override)

(kein ±1-Cap beim Rettungswurf)
```

---

#### Schaden-Block (`IMG_4042`)

```
SCHADEN   (2, 3, D6, D3+2, …)

normal   [1]   per Attacke
mortal   [1]   per (additional) per Attacke
               "string: default text oder weapon ability"
FNP      [6+]  (nur wenn Einheit FNP hat)

              ← Buttons →
Lost Models   [−1]  [+1]   (Einheiten mit mehreren Modellen)
Lost Wounds   [−1]  [+1]   (Frontmodell oder Einzelmodell)

────────────────────────────────────────────────────────
REANIMATION PROTOCOLS  (erscheint nach Apply, wenn Necron-Einheit Verluste hat)

  N Warriors gefallen → N Würfel, Erfolg: 5+
  [Proto: Undying Legions — Reroll]   [Reanimator +1]
  Modelle zurück:  [−1]  [ 0 ]  [+1]
  [RP anwenden]   [↺ Zurücksetzen]
────────────────────────────────────────────────────────
[⚔ Schaden anwenden]   [↺ Zurücksetzen]
```

---

#### Komponenten-API (geplant)

| Funktion | Signatur | Zweck |
|---|---|---|
| `dice_face_svg` | `(value: int, color: str, miss: bool) -> str` | Einzelner SVG-Würfel mit Dots |
| `dice_row_html` | `(threshold: int, modifier: int, cap: bool) -> str` | Würfelreihe 1–6 mit Rahmen + Miss-Würfeln |
| `modifier_die_pair_html` | `(label: str, value: int, color: str) -> str` | Würfelpaar mit Pfeil + Label |
| `special_die_html` | `(label: str, content: str) -> str` | Sondereffekt-Würfel (Tesla, Reroll, FNP) |

---

**Tasks (Freigabe 2026-06-06):**
- [x] `uiLayout/_common.py`: Englische Begriffe in allen Attack-Blocks (Declaration + Resolution + Damage + RP)
- [x] `uiLayout/_common.py`: Rapid Fire Info-Badge in Declaration (`[RAPID FIRE · 24" · ½ = 12"]` via `profile.range_inches`)
- [x] `uiLayout/_common.py`: `dice_face_svg()` + `dice_row_html()` + `modifier_die_pair_html()` + `special_die_html()` — SVG-Komponenten
- [x] `uiLayout/_common.py`: `_render_dice_roll_block()` → HIT-Block mit Würfelreihe + Rahmen + Modifier-Paaren + Tesla/Dakka/Power-Klaw-Badges
- [x] `uiLayout/_common.py`: `_render_dice_wound_block()` → S/T-Anzeige + Würfelreihe + Blau-Highlighting für S/T-Modifier
- [x] `uiLayout/_common.py`: `_render_dice_save_block()` → Normal-Save + AP/Cover-Modifier-Paare (rot) + Invuln-Zeile separat
- Damage-Block + RP-Block bleiben unverändert (Eingabe-basiert)

---

## Testsession-Fixes (2026-06-06)

> Beobachtungsdetail + Regelerkenntnisse: `.claude/tasks/next_session.md`

### 6d-v3 Würfel-UI Fixes

- [x] HIT/WOUND: Schwellenwert-Zeile über Würfeln (`2+  3+  4+  5+  6+`), aktive Schwelle mit Rahmen ✅ (2026-06-06)
- [x] HIT/WOUND: Senkrechte Ausrichtungslinie bei aktiver Schwelle; gestrichelte Linie zwischen Würfel 1 und 2 ✅ (2026-06-06)
- [x] Modifier-Paare: linker Würfel = Ausgangsschwelle (neutral), rechter = neue Schwelle (farbig) ✅ (2026-06-06)
- [x] Modifier-Paare: Positive Modifier-Farbe blau (wie unitCard-Badges), nicht grün ✅ (2026-06-06)
- [x] SAVE: Schwellenwert-Reihe + Würfelreihe für Rüstungs- und Invuln-Save ✅ (2026-06-06)
- [x] SAVE: Vertikales Alignment — Würfelreihen und Modifier-Effekte tabellenartig ✅ (2026-06-06)
- [x] SAVE: Effective Save als Würfelreihe mit farbigem Rahmen ✅ (2026-06-06)
- [x] SAVE: Invuln-Zeile — Schwellenwert-Reihe + Würfelreihe ✅ (2026-06-06)
- [x] 7+ / unmöglicher Save: roter `×`-Marker rechts neben 6er-Würfeln ✅ (2026-06-06)
- [x] Threshold > 6: alle 6 Würfel grau + `×`-Marker statt Zahlenwert ✅ (2026-06-06)
- [x] SAVE: Modifier-Würfelpaare zeigen `threshold − 1` (letzter fehlschlagender Würfel) ✅ (2026-06-07)
- [x] SAVE: Richtung immer Basis(grau/links) → Effektiv(farbig/rechts); Cover blau, AP rot ✅ (2026-06-07)
- [ ] SAVE Modifier-Paare: Fähigkeit + AP kombiniert als eine Badge darstellen (z.B. `Enslaved AP-1`) — erfordert Datenarchitektur (6j)

### Cover-Überarbeitung

- [x] Dropdown → separate Checkboxen (Dense/Light/Heavy unabhängig) ✅ (2026-06-06)
- [x] Phasenbindung: Dense + Light → nur Shooting; Heavy → nur Fight Phase ✅ (2026-06-06)
- [x] Dense Cover Checkbox direkt nach HIT-Block (−1 Trefferwurf) ✅ (2026-06-06)
- [x] Heavy Cover: Charged-Check korrekt; phase-gebundene Anzeige ✅ (2026-06-06)

### Damage-Block

- [x] Mortal Wounds: Eingabe nur wenn Waffe `mortal wound` in abilities hat ✅ (2026-06-06)
- [x] Einzelmodell-Einheit (`models_max ≤ 1`): nur Wunden-Eingabe, kein Modellverlust-Counter ✅ (2026-06-06)

### Fight Phase — Struktureller Fehler (kritisch)

> Regelgrundlage: `core_rules.txt` Z. 1941–1973

- [x] Inaktiver Spieler kann in Fight Phase Einheiten auswählen und kämpfen ✅ (2026-06-06, Root-Cause-Fix Session 20: `unitCard.py` `is_active` nutzt `fight_current_player`)
- [x] `charged` / `in_melee` / `fought` als separate Flags korrekt setzen und auswerten ✅ (2026-06-06)
- [x] Ablauf 9E: erst alle CHARGED-Einheiten aller Spieler → dann abwechselnd (Startspieler: inaktiv) ✅ (2026-06-06)
- [x] Attacken-Splitting für Single-Modell-Einheiten: Angriffs-Counter statt Modell-Counter in Fight-Phase-Deklaration (z.B. Overlord 2+2 auf zwei Ziele) ✅ (2026-06-08)
- [x] `_compute_attacks`: `"*"`-Angriffswert behandelt wie `"Melee"` → korrekte Necron-Nahkampfangriffe ✅ (2026-06-08)
- [ ] Counterattack GO einsetzbar (reaktive Unterbrechung) — Teil von 6e (GO-System)

### Nahkampf-Deklaration — Waffe × Ziel × Attacken (regelkonform)

> Regelgrundlage: `core_rules.txt` Z. 1995–2040

**Problem (Stand 2026-06-08):** Die aktuelle Deklaration (`render_attack_declaration`) wählt eine Waffe (Multiselect) pro Ziel. Bei mehreren gewählten Waffen zeigt die App für jede Waffe die volle Attackenzahl — das ist eine Doppelzählung. Die Regel verlangt:

- Vor der Auflösung: Ziel(e) + Waffe für ALLE Attacken deklarieren
- Jede Attacke wählt genau ein Ziel UND genau eine Waffe
- Attacken können frei aufgeteilt werden: 2× Power Klaw → Ziel A, 1× Slugga → Ziel A ist erlaubt
- Auflösungsreihenfolge: erst alle Attacken gegen Ziel A, dann Ziel B; innerhalb eines Ziels erst alle Attacken mit Profil X, dann Profil Y

**Aktuell existiert ein single-model `use_atk_counter` Pfad (Attacken-Counter) und ein multi-model `model-counter` Pfad. Beide sind für Nahkampf regelwidrig wenn mehrere Waffen gewählt werden.**

**Lösung:**

Deklarationseinträge umstrukturieren auf `(weapon, profile_idx, target, atk_count)`:

```
Gesamtattacken = models_alive × (unit.attacks + waaagh_bonus)

UI:
  Für jede Waffe:
    → Für jeden Ziel-Target:
      Anzahl Attacken: [0][−][+]   ← Summe aller Einträge muss = Gesamtattacken

Validierung: Summe aller atk_count Einträge ≤ Gesamtattacken
Warnung wenn Summe < Gesamtattacken (nicht alle Attacken zugeteilt)
Fehler wenn Summe > Gesamtattacken (zu viele)
```

- Melee **immer** mit Attacken-Counter (kein model-counter mehr für Nahkampf)
- Multi-Modell-Einheiten: Gesamtattacken = `models_alive × unit.attacks`; User teilt ALLE Attacken auf, nicht Modelle
- Für Schussphase bleibt das model-counter Modell (Schusswaffen nicht betroffen)

**Betroffene Dateien:**
- `uiLayout/_common.py` — `render_attack_declaration()`: Eintrags-Logik neu
- `gameMechanic/fightPhase.py` — kein Eingriff nötig wenn Eintrags-Struktur kompatibel bleibt

**Tasks:**
- [x] Plan + Freigabe einholen vor Implementierung ✅ (2026-06-08)
- [x] `render_attack_declaration()`: melee-Pfad auf `(weapon, target, atk_count)` Einträge umstellen ✅ (2026-06-08)
- [x] Multiselect für Waffen entfernen; stattdessen pro Waffe separate Zeilen im Deklarationsblock ✅ (2026-06-08)
- [x] Validierungslogik: Summe aller `atk_count` Einträge gegen Gesamtattacken prüfen ✅ (2026-06-08)
- [x] Tests für neue Eintrags-Struktur ✅ (2026-06-08)

### Heroic Intervention

> Regelgrundlage: `core_rules.txt` Z. 1824–1848 (Schritt 2 der Charge Phase)

- [x] Intervene-Button erst sichtbar nach "All Charges Done →" (Step 2) ✅ (2026-06-07)
- [x] Nur CHARACTER-Einheiten dürfen intervenieren ✅ (2026-06-07)
- [x] HEROIC INT.-Badge auf unitCard ✅ (2026-06-07)
- [x] Intervention: Spieler wählt welche feindlichen Einheiten in Engagement Range landen ✅ (2026-06-07)
- [ ] GOs die Non-CHARACTER-Einheiten HI erlauben (z.B. `enslaved_protectors`) greifen in HI-Eligibility

### GOs in gameActionArea

- [ ] GO-Buttons kontextuell direkt in gameActionArea (aktiver + inaktiver Spieler), nicht als Liste
- [ ] Overwatch als reaktive GO in Charge Phase

### Necron — Command Phase Fixes

- [x] Living Metal: einmalig pro Phase ✅ (2026-06-08)
- [x] 6. Protokoll: einmalig im Setup für das gesamte Spiel festgelegt (nicht jede Runde neu) ✅ (2026-06-05, 6e Bug 2)
- [ ] Protokoll-Effekte auf Living Metal / RP-Verbesserungen abbilden
- [ ] Dynastiebonus: wenn Direktive durch Dynastiezugehörigkeit gilt → Effekt anzeigen
- [ ] Anzeigereihenfolge: Regelkasten immer ganz oben (alle Phasen prüfen)

### WAAAGH! + Sonstiges

- [x] WAAAGH!-Badge auf unitCards der betroffenen Einheiten ✅ (2026-06-08)
- [x] Ork-Regeln prüfen: welche Einheiten ausgenommen? → +1S/+1A gilt für alle ORKS; Advance+Charge nur ORKS CORE/CHARACTER ✅ (2026-06-08)
- [x] Resurrection Orb: Regel lesen → keine KERN-Einschränkung; Implementierung war korrekt; jetzt via `wargear_ids` ✅ (2026-06-06/07)
- [x] Skarabäen: 6=auto-wound → bereits als `abilities`-Text in `weapons.yaml`; kein Code-Feature nötig ✅ (2026-06-06)
- [x] **Advance & Charge:** WAAAGH! Stage 1 — ORKS CORE / ORKS CHARACTER dürfen trotz Advance chargen ✅ (2026-06-08)
- [x] **+1 Attacks in Deklaration:** WAAAGH! Stage 1 + 2 geben +1 Attacks für alle ORKS-Modelle ✅ (2026-06-08)
- [ ] Gretchin Moralphase: Cowardly (−1 Attrition wenn kein RUNTHERD in 6") implementieren

---

## 6e — Fähigkeiten-Integration in alle Phasen

**Ziel:** Fähigkeiten aus Armee, Einheit, Ausrüstung und Stratagems greifen in den richtigen Phasen. CP-Doppelvergabe-Bug gefixt.

### ⚠️ Command Protocol Bugs (Session 2026-06-04)

Die aktuelle Implementierung weicht in drei Punkten von der Regelregel ab:

**Bug 1 — `auto_round_1` existiert nicht in den Regeln:**
Die Regeln erlauben, alle 5 Protokolle frei auf Runden 1–5 zu verteilen. `auto_round_1: true` für Eternal Guardian ist eine erfundene Einschränkung. Das Setup zeigt nur Runden 2–5 (`range(2,6)`) — muss `range(1,6)` sein. Das Flag muss aus YAML, Dataclass, Setup-UI und commandPhase.py entfernt werden.

**Bug 2 — 6. Protokoll fehlt komplett:**
Es gibt 6 Protokolle; 5 werden Runden zugewiesen, das 6. (übrige) ist **jede Runde zusätzlich aktiv**. Die Spielerin wählt dessen Direktive am Rundenanfang. Die App kennt dieses Konzept nicht.

**Bug 3 — Dynastiebonus fehlt:**
Falls das 6. Protokoll das Dynastieprotokoll ist (z.B. Eternal Guardian für Nihilakh), gelten **beide Direktiven** gleichzeitig. Erfordert Dynast-Info im Roster/Unit-Daten — noch nicht vorhanden.

Betroffene Dateien: `faction_abilities.yaml` (Flag weg), `command_protocol.py` (Feld weg), `gameActionsArea.py` (Setup-UI), `commandPhase.py` (Render-Logik), `game_state.py` (`active_protocol_id = "eternal_guardian"` weg).

### ⚠️ Stratagems und Phasenbedingungen (Session 2026-06-04)

Stratagems sind daten-seitig vollständig (`phase`, `timing`, `event`, `once_per_battle` gesetzt), aber die **Anbindung in den Phase-Handlern ist unvollständig**:
- `timing: phase_reactive` GOs werden wie proaktive behandelt (UI-Unterschied fehlt)
- Keine Phase-Handler rufen `stratagem_visibility()` mit korrektem `stage` auf
- Effekte aktiver GOs (`modifier`-Feld) werden in der Attackensequenz nicht ausgewertet
- `once_per_battle` wird nicht enforced

### Tasks

- [ ] `gameMechanic/commandPhase.py`: CP-Vergabe als einmaligen Phase-Grant implementieren (Flag `cp_granted_this_phase` im Session-State, Reset beim Phasenwechsel)
- [ ] `gameMechanic/commandPhase.py`: Einheiten mit Befehlsphase-Fähigkeiten anzeigen (ähnlich Psiphase-Hinweise)
- [ ] `gameMechanic/ability_engine.py`: `collect_modifiers_for_phase(phase, attacker_unit, weapon, target_unit)` — sammelt alle aktiven Modifier aus allen Quellen
- [ ] `gameObjects/ability.py`: Ability-Schema um `modifier`-Felder erweitern (analog zu Stratagem in 6c)
- [ ] `data/wh40k_9e/*/unit_abilities.yaml` + `faction_abilities.yaml`: Modifier-Felder für relevante Fähigkeiten nachtragen (Pilot: Necrons + Orks)
- [ ] Phase-Handler (Shooting, Fight, Charge): rufen `collect_modifiers_for_phase()` auf und übergeben Ergebnis an Attackensequenz-Renderer
- [x] Command Protocol Bug 1 — `auto_round_1` komplett entfernen ✅ (2026-06-05)
- [x] Command Protocol Bug 2 — 6. Protokoll (immer aktiv) + eigene Direktiven-Wahl ✅ (2026-06-05)
- [x] Command Protocol Bug 3 — Dynastiebonus; `dynasty`-Feld in Roster-YAML ✅ (2026-06-05)

---

## 6f — Ability-Badges und Keyword-Highlighting auf unitCard

**Ziel:** Aktive Buffs auf einer Einheit sind auf der unitCard sofort sichtbar.

### Spec

- Badge pro aktivem Buff (Stratagem, Fähigkeit, Protokoll) auf der unitCard
- Badge zeigt: Name der Quelle + Ablauf (z.B. "bis Phasenende")
- Ablauf-Logik kommt aus `active_modifiers` (6c) — Badge verschwindet wenn Modifier abläuft
- Betroffene Keywords visuell hervorgehoben wenn eine Fähigkeit auf sie zutrifft

### Tasks

- [ ] `uiLayout/unitCard.py`: `active_modifiers` aus Session-State lesen, Badges für betroffene Einheit rendern
- [ ] `uiLayout/unitCard.py`: Keyword-Highlighting wenn `active_modifiers` ein Keyword-Condition-Modifier betrifft
- [ ] `gameMechanic/game_state.py`: `active_modifiers` Datenstruktur definieren: `{unit_key, source, effect, expires_at_phase, expires_at_round}`

---

## 6g — Game Log — Archiv, strukturiertes Format, Setup-UI

**Ziel:** Reset archiviert das Log. Das Format ist für Crusade-Vorbereitung (Ziel 7) geeignet. Setup-Screen hat eine Log-Verwaltungs-UI.

### Log-Format (JSON)

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
          "events": [
            {
              "type": "attack",
              "attacker_unit": "wh40k_9e.necrons.unit.warriors",
              "attacker_unit_name": "Warriors",
              "target_unit": "wh40k_9e.orks.unit.boyz",
              "target_unit_name": "Boyz",
              "weapon": "gauss_flayer",
              "damage_dealt": 2,
              "mortal_wounds": 0,
              "target_destroyed": false
            }
          ]
        }
      ]
    }
  ],
  "result": {"winner": "Necrons", "vp": {"Necrons": 75, "Orks": 42}}
}
```

### Tasks

- [x] `gameMechanic/game_log.py`: Log-Format auf strukturiertes JSON (game_id/players/rounds/phases/events)
- [x] `gameMechanic/game_log.py`: `archive_and_reset_log()` — verschiebt aktuelles Log nach `data/log/archive/<game_id>.json`
- [x] `gameMechanic/game_state.py`: `reset_game()` ruft `archive_and_reset_log()` auf
- [x] `uiLayout/setupScreen.py`: Archiv-Verwaltungs-Sektion (Liste, Download, Löschen mit Bestätigung)
- [x] `gameMechanic/game_state.py`: `init_state()` ruft `set_log_players()` auf (Spielernamen im Log-Header)
- [ ] Prüfen: Nach Reset keine alten Einträge im Battle Log sichtbar

---

## 6h — Generisches Fraktion-Fähigkeits-System (alle Fraktionen)

**Ziel:** Die App funktioniert korrekt für ALLE Fraktionen, nicht nur für Necrons und Orks. Das Fähigkeitssystem ist vollständig generisch — neue Fraktionen erfordern nur YAML-Daten, keinen Code-Änderungen.

**Hintergrund:** Wahapedia-Recherche (2026-06-03) ergab 6 Fähigkeitskategorien über alle 10 Hauptfraktionen.
Vollständige Spec: `docs/spec/faction_abilities.md`. Schema-Beispiele: `data/wh40k_9e/_schema/`.

### Kategorie 1 — Runden-Wahl (identisch zu Command Protocols)

| Fraktion | Mechanik | Status |
|----------|----------|--------|
| Necrons | Command Protocols (6 Optionen, Primary/Secondary) | ✅ implementiert |
| **Adeptus Custodes** | **Martial Ka'tah (6 Ka'tahs, Aggressive/Stoic Stance)** | ⬜ YAML fehlt |
| **Adeptus Mechanicus** | **Canticles of the Omnissiah (6, kein Secondary)** | ⬜ YAML fehlt |
| **Tyranids** | **Synaptic Imperatives (bis 10, dynamischer Pool)** | ⬜ YAML + Pool-Logik fehlt |

**Code-Änderungen nötig:**
- [ ] `gameObjects/loader.py`: `CommandProtocol.secondary` + `secondary_effect` optional machen
- [ ] `armyCard._render_protocol_ui()`: Falls kein secondary: Directive-Wahl überspringen, direkt auto-apply
- [ ] Tyranids: Pool-Check ob Synapse-Unit noch lebt (Unit-Keyword-Check in UI)

**YAML nötig:**
- [x] `data/wh40k_9e/adeptus_custodes/faction_abilities.yaml` — alle 6 Ka'tahs ✅ (Batch 1+)
- [ ] `data/wh40k_9e/adeptus_mechanicus/faction_abilities.yaml` — alle 6 Canticles
- [ ] `data/wh40k_9e/tyranids/faction_abilities.yaml` — alle Synaptic Imperatives

**Tests nötig:**
- [x] `tests/test_faction_abilities_custodes.py` — ✅ (Batch 6)
- [ ] `tests/test_faction_abilities_admech.py` — load, no-secondary auto-apply
- [ ] `tests/test_faction_abilities_tyranids.py` — dynamic pool when synapse units die

### ⚠️ Hardcoded Fraktionslogik — Inventar (Stand 2026-06-08)

Keine Fraktion darf namentlich in gameMechanics/uiLayout hardcoded sein.

| Datei | Problem | Status |
|---|---|---|
| `commandPhase.py` | `_OVERLORD_ID = "wh40k_9e.necrons.unit.overlord"` | ✅ entfernt (6k) |
| `unitCard.py` | `_overlord_id` (doppelt) | ✅ entfernt (6k) |
| `game_state.py` | `is_necron_faction()` | ✅ entfernt (6e) |
| `game_state.py` | `active_protocol_id = "eternal_guardian"` | ✅ entfernt (6e Bug 1) |
| `faction_abilities.yaml` | `auto_round_1: true/false` | ✅ entfernt (6e Bug 1) |
| `psychicPhase.py` | `"gloom_prism" in u.rules` in `can_deny()` | ✅ generisch via `load_deny_wargear_names` (6j) |
| `unitCard.py:248` | `"wh40k_9e.necrons.wargear.resurrection_orb" in unit.wargear_ids` | 🔴 offen → **Fix A** |
| `game_state.py` | `resurrection_orb_used = False` in globalem `init_state` | 🟡 offen → **Fix D** |
| `armyCard.py:_render_waaagh_ui` | `"WARBOSS"` Keyword + `"waaagh" in a.id` + Effekttexte hardcoded | 🟡 offen → **Fix B** |
| `armyCard.py:_render_protocol_ui` | `active_protocol_id` / `active_directive` nicht per-Fraktion | 🟡 offen → **Fix C** |
| `_common.py` | `waaagh_state` im Attacken-Resolver (Stärke/Attacken-Modifier) | 🟡 offen → Teil 6e |

---

### 6h — Generifizierungs-Plan (Audit 2026-06-08)

#### Fix A — unitCard: Resurrection Orb Bearer-Ausschluss ohne Wargear-ID (🔴 einfach)

**Problem:** `unitCard.py:248` prüft eine konkrete Necron-Wargear-ID.

**Lösung:**
- `commandPhase.py`: beim Setzen von `res_orb_awaiting_target = True` zusätzlich `wargear_awaiting_bearer_uid = uid` setzen; beim Abbruch/Bestätigung wieder löschen
- `unitCard.py:248`: `if uid == st.session_state.get("wargear_awaiting_bearer_uid")` statt Wargear-ID-String
- Kein Datenmodell-Änderung nötig — der Bearer ist ohnehin bekannt wenn die Aktion ausgelöst wird

**Dateien:** `commandPhase.py`, `unitCard.py`

---

#### Fix B — armyCard: WAAAGH!-UI vollständig generisch (🟡 mittel)

**Problem:** `_render_waaagh_ui` hat drei hardcoded Stellen:

1. **Ability-Suche per ID-String:** `"waaagh" in a.id.lower()` → Ersetzen durch generische Bedingung: alle `activated` Command-Phase-Abilities, deren `conditions[0].once_per_battle == True`. Das YAML hat das bereits als `once_per_battle: true` in den Conditions.

2. **WARBOSS-Keyword:** `has_warboss = any(u.has_keyword("WARBOSS") ...)` → Ersetzen durch `any(check_conditions(ability, u, {}) for u in units)` — die Ability-Conditions enthalten bereits `has_keywords: [WARBOSS]`.

3. **Effekttexte:** Stage-1- und Stage-2-Texte hardcoded → YAML-Feld `active_text` in `faction_abilities.yaml` ergänzen; `Ability`-Dataclass um optionales `active_text: str | None` erweitern.

```yaml
# faction_abilities.yaml (Orks) — Ergänzung:
- id: wh40k_9e.orks.faction.waaagh_stage1
  active_text: "+1 Strength · +1 Attacks · 5+ invuln · Advance & Charge"
  ...
- id: wh40k_9e.orks.faction.waaagh_stage2
  active_text: "+1 Strength · +1 Attacks · 6+ invuln"
  ...
```

**Dateien:** `gameObjects/ability.py`, `gameObjects/loader.py`, `data/wh40k_9e/orks/faction_abilities.yaml`, `armyCard.py`

---

#### Fix C — armyCard/ability_engine: Protokoll-Session-Keys per Fraktion (🟡 aufwändig)

**Problem:** `active_protocol_id`, `active_directive`, `extra_directive` sind globale Session-State-Keys. Sobald zwei Fraktionen mit Protokollen spielen (Necrons vs. Custodes Ka'tahs), überschreiben sie sich gegenseitig.

**Lösung:** Keys auf `faction_dir` scopen:
- `active_protocol_id` → `protocol_active_{faction_dir}`
- `active_directive` → `protocol_directive_{faction_dir}`
- `extra_directive` → `protocol_extra_directive_{faction_dir}`

`get_active_protocol_modifier(faction_dir, ...)` liest bereits `faction_dir` — nur die Key-Namen ändern.

**Dateien:** `armyCard.py` (_render_protocol_ui, _render_extra_protocol, _render_directive_buttons), `gameMechanic/ability_engine.py`, `gameMechanic/game_state.py` (init + reset), ggf. `commandPhase.py`

**Voraussetzung für:** Custodes Ka'tahs, AdMech Canticles (6h Kategorie 1)

---

#### Fix D — game_state: `resurrection_orb_used` aus globalem Init herauslösen (🟡 einfach)

**Problem:** `game_state.py init_state()` initialisiert `resurrection_orb_used = False` — Necron-Wargear-State im globalen Init.

**Lösung:** Ersetzen durch generischen `wargear_used: dict[str, bool] = {}`. `commandPhase.py` schreibt `state["wargear_used"]["wh40k_9e.necrons.wargear.resurrection_orb"] = True` — der Key-Name ist dann in commandPhase, nicht in game_state.

**Dateien:** `gameMechanic/game_state.py`, `gameMechanic/commandPhase.py`

---

#### Reihenfolge

| Priorität | Fix | Aufwand | Abhängigkeit |
|---|---|---|---|
| 1 | **A** — unitCard Orb-Bearer | klein | — |
| 2 | **D** — wargear_used generic | klein | — |
| 3 | **B** — WAAAGH! generisch | mittel | — |
| 4 | **C** — Protokoll-Keys per Fraktion | groß | — |

A+D können in einem Commit, B+C jeweils einzeln.

### Kategorie 2 — Einmalig-Deklariert (wie WAAAGH!)

| Fraktion | Mechanik | Status |
|----------|----------|--------|
| Orks | WAAAGH! (2 Stages) | ✅ implementiert |
| **T'au Empire** | **Mont'ka / Kauyon (Runden-Fenster)** | ⬜ fehlt |

**Code-Änderungen nötig:**
- [ ] `armyCard._render_waaagh_ui()`: `active_rounds`-Feld aus YAML auslesen; Badge nur zeigen wenn aktuelle Runde im Fenster liegt
- [ ] `game_state._reset_turn_state()`: Runden-Fenster-Prüfung für T'au ergänzen

**YAML nötig:**
- [ ] T'au `faction_abilities.yaml`: `montka` + `kauyon` mit `active_rounds` Feld

**Tests nötig:**
- [ ] `tests/test_faction_abilities_tau.py` — montka_active_rounds, kauyon_active_rounds

### Kategorie 3 — Auto-Progression (kein Player-Input)

| Fraktion | Mechanik | Status |
|----------|----------|--------|
| Space Marines | Combat Doctrines (R1 Heavy / R2 Assault / R3+ Melee) | ⬜ fehlt |
| Death Guard | Contagions of Nurgle (Reichweite skaliert) | ⬜ fehlt |
| Chaos SM | Let the Galaxy Burn (R1+R2 auto, R3 Wahl) | ⬜ fehlt |

**Code-Änderungen nötig:**
- [ ] `ability_engine.py`: `get_auto_progression_modifier(faction_dir, phase, round)` → `dict[str, int]`
- [ ] `armyCard.py`: `_render_auto_progression_badge(faction)` — Info-Badge ohne Button
- [ ] `_common.py`: Auto-Progression-Modifier in `render_attack_form()` einbinden

**YAML nötig:**
- [ ] `ability_type: auto_progression` + `progression: [{round, effects}]` Schema (Beispiel: `_schema/auto_progression.example.yaml`)
- [ ] YAML für Space Marines, Death Guard, Chaos SM

**Tests nötig:**
- [ ] `tests/test_auto_progression.py` — round→modifier Mapping, round_max, kein Player-Input

---

## Daten-Review — Stratagem-Schema + fachliche Korrekturen

**Ziel:** Alle YAML-Datendateien fachlich gegen Wahapedia verifizieren. Jede GO erhält korrekte `phase`, `stage`, `player`, `timing`, `event` und ein maschinenlesbares `effect`-Feld.

### Schema-Erweiterung `Stratagem`-Dataclass (2026-06-04)

Neue Felder (konsistent mit `Ability.Trigger` / `Ability.Effect`):

| Feld | Typ | Bedeutung |
|------|-----|-----------|
| `phase` | `str \| list[str]` | Einzelphase oder Liste; `"any"` nur wenn wirklich jede Phase gilt |
| `timing` | `str \| None` | `None` = proaktiv; `"phase_reactive"` = reaktiv auf Ereignis |
| `event` | `str \| None` | `"after_roll"` / `"on_destroy"` / `"on_target"` / `"on_declaration"` |
| `once_per_battle` | `bool` | `True` wenn rule_text "once per battle" sagt |
| `effect` | `Effect \| None` | Maschinenlesbarer Effekt — reuse aus `ability.py` |

Effect-Typen (Vocabulary aus `ability.py`): `buff_roll`, `debuff_roll`, `mortal_wounds`, `heal`, `reanimate`, `free_attack`, `auto_pass_morale`, `reroll`, `move`, `disembark`, `shoot_reaction`, `auto_explode`, `teleport`, `invuln_save`, `restriction`, `mark_target`

### Offene Entscheidungen

| Entscheidung | Status |
|---|---|
| `once_per_battle` enforcement | Datenfeld gesetzt; Enforcement braucht `used_this_battle` in Session-State + neuen Parameter in `stratagem_visibility()` — noch nicht implementiert |
| Variable CP-Kosten | Derzeit Kommentar im YAML (`# variable: 1CP / 2CP`). Ggf. `cp_cost_max`-Feld ergänzen. |
| Reaktive GO UI | `timing: phase_reactive` korrekt in Dataclass; UI behandelt diese GOs noch wie proaktive |

### ⚠️ Daten-Lücken — Truncated Scraper (Session 2026-06-04)

Der Wahapedia-Scraper hat bei allen drei implementierten Fraktionen **substantiell unvollständige Daten** geliefert. Betroffen sind insbesondere:
- Einheiten-Profile (fehlende Stats, fehlende Keywords, unvollständige Waffenprofile)
- Fähigkeiten (Abilities/Rules nicht vollständig — z.B. Dynastiebonus-Mechanik bei Command Protocols komplett fehlend)
- Stratagems bereits manuell nachgearbeitet ✅ — Units/Weapons noch offen

**Vorgehen:** Vor jedem weiteren Feature-Build für eine Fraktion zuerst Daten gegen Wahapedia verifizieren.

### Tasks

- [x] `gameObjects/stratagem.py`: `phase: str | list[str]`, `timing`, `event`, `once_per_battle`, `effect: Effect`
- [x] `gameObjects/loader.py`: neue Felder parsen
- [x] `gameObjects/stratagem.py`: `stratagem_visibility()` list-phase-fähig
- [x] `_shared/stratagems.yaml`: alle 7 GOs vollständig
- [x] `necrons/stratagems.yaml`: 7 bekannte Fehler behoben
- [x] `orks/stratagems.yaml`: wreckaz + careen behoben
- [x] `necrons/stratagems.yaml`: alle 59 GOs vollständig — `effect`, `once_per_battle`, `timing/event` für reaktive GOs; `player` korrigiert bei quantum_deflection + shadows_of_drazak; `rule_text` bei whirling_onslaught nachgetragen
- [x] `orks/stratagems.yaml`: alle 28 GOs vollständig — `effect`, `once_per_battle`, `timing/event`, `player` bei tough_as_squig_hide + orks_is_never_beaten korrigiert
- [x] `necrons/faction_abilities.yaml`: Trigger/Conditions spot-check — alle Trigger korrekt, keine Korrekturen nötig
- [x] `orks/faction_abilities.yaml`: Trigger/Conditions spot-check — alle Trigger korrekt, keine Korrekturen nötig
- [ ] `once_per_battle` enforcement in Session-State + `stratagem_visibility()`
- [ ] Optional: Tests für korrekte Phase/Stage-Werte

---

## 6i — Auto-Advance: Abgehandelte Einheiten ans Listenende

**Ziel:** Nach dem Abhandeln einer Einheit in einer Phase wandert ihre unitCard ans Ende der Armeeliste. So ist die nächste unbehandelte Einheit immer oben — kein Zurückscrollen nötig. Phase-Reset stellt Standardreihenfolge wieder her.

### Handled-Kriterien pro Phase

| Phase | Kriterium |
|---|---|
| movement | `state["movement_choice"] is not None` |
| shooting | `turn_flags["shot"] == True` |
| psychic | `turn_flags["cast"] == True` |
| charge | `turn_flags["charged"] == True` |
| fight | `turn_flags["fought"] == True` |
| command / morale / setup | keine Sortierung |

### Tasks

- [x] `uiLayout/detachmentCard.py`: `(unit, state_key)`-Paare vor dem Rendern sortieren — unbehandelte zuerst, behandelte zuletzt (stabile Sortierung)

---

## 6j — YAML-Konsolidierung: Doppel-Dateien zusammenführen

**Ziel:** Jede Fraktion hat pro Datentyp genau eine YAML-Datei. Die aktuell parallelen `*_abilities.yaml`-Dateien (redundante Maschinen-Repräsentation) werden in die jeweilige Stammdatei integriert. Alle Listen-Dateien bekommen eine einheitliche Top-Level-Struktur (direkte Liste).

### Hintergrund (Session 22, 2026-06-07)

Vollständiger Audit über alle Fraktionen ergab drei Redundanz-Muster:

1. **Doppel-Datei-Paare**: `weapons.yaml + weapon_abilities.yaml` und `wargear.yaml + wargear_abilities.yaml` — je zwei Dateien für dasselbe Objekt (Stammdaten + Maschinen-Repräsentation)
2. **Header-Inkonsistenz**: Fünf verschiedene Top-Level-Formate für dieselbe Grundstruktur „Liste von Objekten"
3. **Lokalisierung inkonsistent**: Mal `name_en/de`, mal nur `text_de`, mal `rule_text` ohne Übersetzung

`faction_abilities.yaml` vs. `unit_abilities.yaml` sind **kein** Redundanzproblem — verschiedene Konzepte, kein Merge.

### Schritt 1 — `weapon_abilities.yaml` in `weapons.yaml` integrieren

Betrifft: Necrons, Orks (je eine Datei entfällt)

Neue Struktur: Ability als optionales `effect`-Feld im Waffen-Eintrag:
```yaml
- id: wh40k_9e.necrons.weapon.tesla_carbine
  name_en: Tesla Carbine
  profiles: [...]
  effect:          # optional — nur wenn Waffe Sonderregel hat
    type: extra_hits
    trigger_value: 6
    unmodified: true
    hits: 2
```

**Dateien:**
- [x] `data/wh40k_9e/necrons/weapons.yaml` — `effect`-Felder aus `weapon_abilities.yaml` einpflegen ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/weapons.yaml` — dto. ✅ (2026-06-07)
- [x] `data/wh40k_9e/necrons/weapon_abilities.yaml` — **gelöscht** ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/weapon_abilities.yaml` — **gelöscht** ✅ (2026-06-07)
- [x] `src/gameObjects/loader.py` — `load_weapon_abilities()` liest aus `weapons.yaml` ✅ (2026-06-07)
- [x] Tests anpassen — 470 Tests grün, keine Änderungen nötig ✅ (2026-06-07)

### Schritt 2 — `wargear_abilities.yaml` in `wargear.yaml` integrieren ✅ (2026-06-07)

Betrifft: Necrons, Orks

Neue Struktur: direkte Liste (kein `schema/faction/entries:` Header), Ability inline:
```yaml
- id: wh40k_9e.necrons.wargear.gloom_prism
  name_en: Gloom Prism
  rule_text: "In your opponent's Psychic phase, the bearer's unit can attempt to deny one psychic power as if it were a PSYKER."
  effect:
    type: deny_psychic
    target: self
  trigger:
    timing: phase_reactive
    phase: psychic
    player: inactive
  source: { publication: Codex Necrons 9e }
```

`deny: true` Flag entfällt — `can_deny()` prüft `effect.type == "deny_psychic"` direkt.

**Dateien:**
- [x] `data/wh40k_9e/necrons/wargear.yaml` — Header entfernen, direkte Liste, Ability-Felder einpflegen ✅
- [x] `data/wh40k_9e/orks/wargear.yaml` — dto. ✅
- [x] `data/wh40k_9e/necrons/wargear_abilities.yaml` — **gelöscht** ✅
- [x] `data/wh40k_9e/orks/wargear_abilities.yaml` — **gelöscht** ✅
- [x] `data/wh40k_9e/necrons/arkana.yaml` — **neu** (Arkana-Block ausgelagert) ✅
- [x] `src/gameObjects/loader.py` — `load_wargear_abilities()` und `load_deny_wargear_names()` auf neue Struktur umgestellt ✅

### Schritt 3 — Header vereinheitlichen (restliche Dateien)

Betrifft: `warlord_traits.yaml`, `relics.yaml` in Necrons + Orks

Aktuell mit `schema:` + `entries:`-Header → direkte Liste wie `weapons.yaml` und `stratagems.yaml`.

**Dateien:**
- [x] `data/wh40k_9e/necrons/warlord_traits.yaml` — `schema/entries:` entfernen → direkte Liste ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/warlord_traits.yaml` — dto. ✅ (2026-06-07)
- [x] `data/wh40k_9e/necrons/relics.yaml` — `schema/relics:` entfernen → direkte Liste ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/relics.yaml` — dto. ✅ (2026-06-07)
- [x] `src/gameObjects/loader.py` — kein Loader für diese Dateien vorhanden; Format jetzt konsistent ✅ (2026-06-07)

### Reihenfolge

~~Schritt 2 zuerst~~ ✅ → dann Schritt 1, dann Schritt 3.

---

## 6k — Wargear-Effekt-Interpreter

**Ziel:** Persistente Wargear-Effekte (Stat-Änderungen, Keyword-Grants, Saves, FNP) werden beim Roster-Laden auf die Unit-Instanz angewendet und in der App überall dort sichtbar, wo der Originalwert stünde. Kein `type: complex`-Platzhalter mehr für einfache Effekte.

**Voraussetzung:** 6j Schritt 2 abgeschlossen ✅

### Schema-Erweiterung (`wargear.yaml`)

Neues optionales Feld `persistent_effects:` neben dem bestehenden `effect:`-Feld:

```yaml
- id: wh40k_9e.necrons.wargear.canoptek_cloak
  ...
  persistent_effects:
    - type: set_stat
      stat: move
      value: "10\""
    - type: grant_keyword
      keyword: FLY
  # triggered heal bleibt als effect: {type: heal, ...} (Ziel-Auswahl → complex)
```

**Persistente Effekt-Typen (80%):**

| Typ | Felder | Beispiel |
|---|---|---|
| `set_stat` | `stat`, `value` | Move = 10" (absolut) |
| `buff_stat` | `stat`, `modifier` | Move +2 (relativ) |
| `grant_keyword` | `keyword` | FLY, INFANTRY |
| `set_invuln` | `value` | Invuln = 4+ |
| `buff_save` | `modifier` | Save +1 |
| `set_fnp` | `value` | FNP = 6+ |

**Komplex-Liste (20% — nicht implementiert, hardcoded oder display-only):**

| Wargear | Warum komplex | Status |
|---|---|---|
| `canoptek_cloak` heal D3 | Triggered, Ziel-Auswahl innerhalb 3", ein Modell | display-only |
| `canoptek_control_node` Aura | Echtzeit-Reichweiten-Check auf Nachbareinheiten | display-only |
| `resurrection_orb` | Functionally implemented, aber hardcoded auf OVERLORD keyword statt Wargear-ID | 6h-Migration |
| `phylactery` | Modifiziert Living-Metal-Effekt dynamisch (konditionell) | display-only |
| `fabricator_claw_array` | Triggered, Ziel-Auswahl VEHICLE innerhalb 3" | display-only |
| Ork: `grot_oiler` | Modifiziert Mekaniak-Ergebnis konditionell | display-only |
| Ork: `ammo_runt` | Triggered, once-per-battle | display-only |
| Ork: `bomb_squig`, `ramming_spur`, `squig_bomb` | Komplexe Bedingungen + Ziel-Auswahl | display-only |

### Betroffene Dateien

- [x] `gameObjects/unit.py` — `wargear_ids: list[str]` Feld hinzufügen ✅ (2026-06-07)
- [x] `gameObjects/loader.py`: `load_wargear_catalog()`, `_apply_persistent_effect()`, `_apply_wargear()` erweitert ✅ (2026-06-07)
- [x] `data/wh40k_9e/necrons/wargear.yaml` — `persistent_effects:` für canoptek_cloak, dispersion_shield, shieldvanes, shadowloom ✅ (2026-06-07)
- [x] `data/wh40k_9e/orks/wargear.yaml` — `persistent_effects:` für cybork_body, kustom_job_souped_up_driveshaft, kustom_job_extra_armour_platez ✅ (2026-06-07)
- [x] `uiLayout/unitCard.py` — wargear-granted Keywords in Keyword-Zeile anzeigen ✅ (2026-06-07)
- [x] Tests — 14 neue Tests ✅ (2026-06-07)

### Hinweis: `resurrection_orb` bereits funktional

Die Resurrection-Orb-UI ist funktional und nutzt seit 6k `"resurrection_orb" in unit.wargear_ids` statt OVERLORD-Keyword-Check. ✅ (2026-06-07)

### Tasks

- [x] Schema + YAML-Felder für persistente Effekte (Necrons + Orks) ✅ (2026-06-07)
- [x] `_apply_persistent_effect()` Interpreter in loader.py ✅ (2026-06-07)
- [x] `_apply_wargear()` erweiterung ✅ (2026-06-07)
- [x] unitCard: granted Keywords anzeigen (blau markiert) ✅ (2026-06-07)
- [x] resurrection_orb: Wargear-ID-Check statt OVERLORD-Keyword ✅ (2026-06-07)
- [x] Tests (14 neue Tests) ✅ (2026-06-07)

---

## 6l — Relic-Effekt-Interpreter (geplant)

**Ziel:** Relics mit Conditions und Effekten werden maschinenlesbar — analog zu 6k (Wargear). Aktuell werden `ability_en`-Texte nur angezeigt, aber nie ausgewertet. Trigger (z.B. „At the start of your Command phase") und Effekte (z.B. „roll D6 on 4+: gain 1 CP") existieren nur als Freitext.

**Betrifft alle Fraktionen** — Necrons und Orks je ~10 Relics, künftige Fraktionen ebenso.

**Beispiel (Orks):**

```yaml
# Aktuell — nur Freitext:
- id: wh40k_9e.orks.relic.morgogs_finkin_cap
  ability_en: >
    At the start of your Command phase, if the bearer is on the battlefield, roll one D6:
    on a 4+, you gain 1 Command point.

# Ziel — maschinenlesbar:
- id: wh40k_9e.orks.relic.morgogs_finkin_cap
  ability_en: >
    At the start of your Command phase, if the bearer is on the battlefield, roll one D6:
    on a 4+, you gain 1 Command point.
  trigger:
    timing: phase_start
    phase: command
    player: active
  effect:
    type: gain_cp
    roll: D6
    threshold: 4
    amount: 1
    condition: bearer_on_battlefield
```

**Analog zu 6k:** Relic-Effekte können in drei Klassen eingeteilt werden:
1. **Persistent** — Stat-Änderungen, Keyword-Grants, Invuln-Saves (analog `persistent_effects` in Wargear)
2. **Triggered** — CP-Gain, Heilung, FNP-Modifikation bei bestimmten Events
3. **Weapon-Relic** — hat `profiles:` → bereits über Waffen-Renderer abgedeckt (display-only)

**Vorbedingung:** 6k vollständig ✅ — Schema und Interpreter bereits bekannt.

**Noch nicht spezifiziert** — vor Umsetzung: YAML-Schema für alle Relic-Effekt-Typen definieren, dann Necrons + Orks nachziehen.

---

## Ork Waffen-Audit — Befunde (Session 29, 2026-06-08)

> Vollständiger manueller Abgleich aller Ork-Einheiten gegen Wahapedia-Quelldaten.

### Befund 1: Stärke-Werte — korrekt ✅

`_parse_strength()` in `_common.py` verarbeitet alle Notationen korrekt: `User` → `unit_strength`, `+2` → `unit_strength + 2`, `User×2` → `unit_strength * 2`. Kein Handlungsbedarf.

### Befund 2: Boss-Nob-Waffen fälschlicherweise für alle Modelle sichtbar ❌

In multi-Modell-Einheiten sind Waffen, die nur der Boss Nob tragen darf, flach in `weapons[]` gelistet — ohne Einschränkung. Die App erlaubt damit jedem Modell, diese Waffen im Nahkampf zu wählen.

| Einheit | Waffe | Tatsächliche Einschränkung |
|---|---|---|
| `boyz` | big_choppa, killsaw, power_klaw, power_stabba | Boss Nob only |
| `boyz` | big_shoota, rokkit_launcha | 1 pro 10 Modelle |
| `beast_snagga_boyz` | thump_gun | 1 pro 10 Modelle |
| `kommandos` | big_choppa, power_klaw | Boss Nob only |
| `kommandos` | big_shoota, breacha_ram, burna, kustom_shoota, rokkit_launcha, shokka_pistol | 1 pro 10 Modelle |
| `tankbustas` | tankhammer (**Nahkampfwaffe!**), pair_of_rokkit_pistols | 1 pro 5 Modelle |
| `warbikers` | big_choppa, power_klaw | Boss Nob only |
| `stormboyz` | power_klaw | Boss Nob only |
| `nobz`, `meganobz`, `flash_gitz`, `squighog_boyz` | alle | jedes Modell ✅ |

**Geplante Lösung (Option A):** Optionales `model_restriction`-Feld in `weapons[]`-Einträgen der Units:

```yaml
# units.yaml — Beispiel Boyz
weapons:
  - ref: wh40k_9e.orks.weapon.choppa          # alle Modelle (kein Feld = keine Einschränkung)
  - ref: wh40k_9e.orks.weapon.power_klaw
    model_restriction: boss_nob_only
  - ref: wh40k_9e.orks.weapon.big_shoota
    model_restriction: "1_per_10"
```

**Betroffene Dateien:** `data/wh40k_9e/orks/units.yaml`, `gameObjects/unit.py` (WeaponRef-Dataclass), `gameObjects/loader.py` (Parsing), `uiLayout/_common.py` (Deklarations-Filter)

### Befund 3: `extra_attacks`-Waffeneffekt nie ausgewertet ❌ (kritisch)

`_compute_attacks()` (`_common.py:358`) ignoriert den `effect`-Block aus `weapons.yaml` vollständig. Bei `weapon_type: Melee` wird immer `models × unit.attacks` berechnet — ohne Bonus für Waffen mit `extra_attacks`-Effekt.

Zwei Unterklassen:

**3a — „+N additional attacks" ohne Cap** (bearer kämpft mit `unit.attacks + N`):

| Waffe | Effekt | Ist | Soll (Beispiel S:4, 3 attacks) |
|---|---|---|---|
| choppa | +1 additional attack | 3 | 4 |
| beastchoppa | +1 additional attack | 3 | 4 |
| 'urty syringe | +1 additional attack | 3 | 4 |
| grabba stikk | +1 additional attack | 3 | 4 |
| dread klaw | +1 additional attack | 3 | 4 |

**3b — „+N additional attacks, no more than N" (fester Cap)** (immer genau N Attacken, unabhängig von `unit.attacks`):

| Waffe | Cap | Ist (Warboss A:5) | Soll |
|---|---|---|---|
| attack squig | max 2 | 5 | 2 |
| squighog jaws | max 2 | 3 | 2 |
| squigosaur's jaws | max 3 | 5 | 3 |
| smasha squig jaws | max 2 | 4 | 2 |
| grabbin' klaw | max 1 | 6 | 1 |
| wreckin' ball | max 1 | 6 | 1 |
| butcha boyz | max 4 | 6 | 4 |
| savage horns and hooves | max 4 | 6 | 4 |

**Geplante Lösung:** `effect`-Block in `weapons.yaml` um `max_attacks`-Feld erweitern; `_compute_attacks()` und `_total_attacks_int()` auslesen:

```yaml
# weapons.yaml — attack_squig (Klasse 3b)
effect:
  type: extra_attacks
  amount: 2
  max_attacks: 2   # neu — "no more than N" Cap

# choppa (Klasse 3a)
effect:
  type: extra_attacks
  amount: 1
  # kein max_attacks → unit.attacks + 1
```

**Betroffene Dateien:** `data/wh40k_9e/orks/weapons.yaml` (max_attacks-Felder ergänzen), `gameObjects/weapon.py` (WeaponProfile-Dataclass), `gameObjects/loader.py`, `uiLayout/_common.py` (`_compute_attacks`, `_total_attacks_int`)

### Befund 4: Optional-Wargear-Attachments nicht in YAML ⚠️ (display-only)

Folgende Attachment-Wargear-Einträge fehlen vollständig in `wargear_options` aller Ork-Einheiten. Sie sind als `display-only` in der 6k-Komplex-Liste bereits dokumentiert (kein neuer Handlungsbedarf):

| Wargear | Trägereinheit(en) | Effekt |
|---|---|---|
| grot oiler | Big Mek-Varianten | +D3 bei Mekaniak-Reparatur |
| ammo runt | Nobz (1/5), Flash Gitz, Kaptin Badrukk | Re-roll 1 Treffer/Runde |
| grot orderly | Painboy, Painboss | Verbessert Sawbonez |
| gitfinda squig | Flash Gitz Kaptin | +1 Hit mit Snazzgun |
| squig hound / grot-lash | Runtherd | Gretchin-Moral-Modifikator |
| bomb squig | Kommandos (1/10), Squighog Boyz (1/3), Tankbustas (2/5) | Mortal Wounds bei Charge |
| distraction grot | Kommandos (1/10) | −1 Hit auf Feind |

### Priorisierung der Fixes

| Priorität | Fix | Aufwand | Kritikalität |
|---|---|---|---|
| **1** | extra_attacks Klasse 3b (Cap-Waffen: feste Attackenzahl) | klein | hoch — falsche Attackanzahl |
| **2** | extra_attacks Klasse 3a (Choppa etc.: +N) | mittel | hoch — betrifft fast alle Ork-Nahkämpfer |
| **3** | model_restriction in YAML + Filter in UI | groß | mittel — regelwidrig, aber Spieler bemerkt es |
| **4** | Optional-Wargear-Attachments | sehr groß | niedrig — display-only akzeptiert |

### Tasks

- [x] `data/wh40k_9e/orks/weapons.yaml`: `max_attacks`-Feld für alle Klasse-3b-Waffen ergänzen ✅ (2026-06-08)
- [x] `gameObjects/weapon.py`: `WeaponProfile.max_attacks: int | None = None` ✅ (2026-06-08)
- [x] `gameObjects/loader.py`: `max_attacks` aus YAML parsen ✅ (2026-06-08)
- [x] `uiLayout/_common.py`: `_compute_attacks()` + `_total_attacks_int()` — Klasse 3b (max_attacks) + Klasse 3a (+N) auswerten ✅ (2026-06-08)
- [x] `data/wh40k_9e/orks/units.yaml`: `model_restriction`-Felder für alle Boss-Nob-Waffen ✅ (2026-06-08)
- [x] `gameObjects/unit.py`: `Unit.weapon_restrictions: dict[str, str]` — Badge-Lookup ✅ (2026-06-08)
- [x] `gameObjects/loader.py`: `model_restriction` aus YAML parsen ✅ (2026-06-08)
- [x] `uiLayout/_common.py`: `render_attack_declaration()` — Boss-Nob-Badge in Melee+Shooting ✅ (2026-06-08)
- [x] Tests für neue extra_attacks-Logik (25 Tests) ✅ (2026-06-08)
- Note: grot_prod hat laut Wahapedia kein extra_attacks (Ability-Text: `-`) — war in Session-29-Notizen falsch

---

## Akzeptanzkriterien (Ziel 6 komplett)

- [ ] Header: VP/CP inline, alle Steuerelemente auf einer Zeile, Badges doppelt so groß
- [ ] armyCard: Korrekte Fähigkeiten für jede Fraktion, kein Necron-Fallback-Bug
- [ ] WAAAGH aktivierbar, Command Protocol wechselbar — beide über armyCard
- [ ] **Ka'tah (Custodes) + Canticles (AdMech) funktionieren ohne Code-Änderung** (nur YAML)
- [ ] **Auto-Progression-Badge zeigt korrekte Doctrine für Space Marines**
- [ ] Stratagems sind Default-Tab in gameProtocoll
- [ ] Attackensequenz: simultan, Modifier transparent, kein Zwischenwert-Klicken
- [ ] CP-Doppelvergabe unmöglich
- [ ] Ability-Badges auf unitCard sichtbar und korrekt ablaufend
- [ ] Reset archiviert Log; neues Spiel startet sauber
- [ ] Archiv-UI im Setup-Screen: Liste, Download, Löschen
