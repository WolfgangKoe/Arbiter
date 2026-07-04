# Archiv — Teilziele 6a–6d, ausgelagert 2026-06-27

> Diese Datei enthält die weitgehend abgeschlossenen Teilziele 6a, 6b, 6c, 6d (inkl. 6d-v2, 6d-v3,
> Testsession-Fixes) aus `docs/goals/archive/ziel6.md`. Der Großteil ist ✅. **Einzelne 6d-v2/v3- und
> Testsession-Punkte sind noch offen** — sie werden über aktive Pläne (013 DONE / 015 / 017 / 018)
> bzw. den Backlog weiterverfolgt; der Verbleib jedes offenen Punktes steht in `ziel6.md` unter
> „Offene Restpunkte aus 6a–6d". Kein offener Punkt existiert ausschließlich hier.
> Aktive Inhalte (6e ff.) verbleiben in der Hauptdatei.

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
- [x] Heavy Cover: Charged-Check korrekt; phase-gebundene Anzeige ✅ (2026-06-06) → Bug-Fix 2026-06-09: `charged` prüfte `atk_state` statt `def_state` — Regel: Defender verliert Cover wenn **er selbst** charged hat, nicht der Angreifer

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
- [x] Protokoll-Effekte auf Living Metal / RP-Verbesserungen abbilden ✅ (Engine S86; 6./Dynastie-Direktive S93)
- [x] Dynastiebonus: Effekt wirkt (Affinität → beide Direktiven engine-seitig aktiv) ✅ (S93); Anzeige-Badge ✅ (UI-verifiziert S93)
- [ ] Anzeigereihenfolge: Regelkasten immer ganz oben (alle Phasen prüfen)

### WAAAGH! + Sonstiges

- [x] WAAAGH!-Badge auf unitCards der betroffenen Einheiten ✅ (2026-06-08)
- [x] Ork-Regeln prüfen: welche Einheiten ausgenommen? → +1S/+1A gilt für alle ORKS; Advance+Charge nur ORKS CORE/CHARACTER ✅ (2026-06-08)
- [x] Resurrection Orb: Regel lesen → keine KERN-Einschränkung; Implementierung war korrekt; jetzt via `wargear_ids` ✅ (2026-06-06/07)
- [x] Skarabäen: 6=auto-wound → bereits als `abilities`-Text in `weapons.yaml`; kein Code-Feature nötig ✅ (2026-06-06)
- [x] **Advance & Charge:** WAAAGH! Stage 1 — ORKS CORE / ORKS CHARACTER dürfen trotz Advance chargen ✅ (2026-06-08)
- [x] **+1 Attacks in Deklaration:** WAAAGH! Stage 1 + 2 geben +1 Attacks für alle ORKS-Modelle ✅ (2026-06-08)
- [ ] Gretchin Moralphase: Cowardly (−1 Attrition wenn kein RUNTHERD in 6") implementieren

