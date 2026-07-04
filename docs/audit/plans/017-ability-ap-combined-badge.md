# Plan 017: SAVE-Block — Fähigkeits-AP-Modifier als kombinierte Badge (Datenarchitektur)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `docs/audit/plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat f0f4e17..HEAD -- src/uiLayout/_common.py src/uiLayout/dice_html.py src/gameMechanic/combat.py`
> Drift in `_common.py` durch 013/014/016 ist ERWARTET. Wenn
> `_render_resolution_tab` (AP-/Save-Berechnung) oder
> `save_modifier_die_pair_html` strukturell anders aussehen: STOP.

## Status

- **Priority**: P3 (MITTEL, archive/ziel6.md Z. 498 + next_session „Fähigkeit + AP kombiniert")
- **Effort**: S–M (inkl. Recherche-Step — der eigentliche Engpass ist die Datenfrage)
- **Risk**: LOW–MEDIUM (Anzeige + eine AP-Rechenstelle)
- **Depends on**: 014 (gleiche Datei `_common.py` — nacheinander); 016 empfohlen
  (liefert `get_active_protocol_effects` für `ap_bonus`)
- **Category**: feature (Transparenz der Save-Berechnung) + Datenarchitektur (6j/6l)
- **Planned at**: commit `f0f4e17`, 2026-06-12

## Why this matters

archive/ziel6.md (Z. 498): „SAVE Modifier-Paare: Fähigkeit + AP kombiniert als eine
Badge darstellen (z. B. `Enslaved AP-1`) — erfordert Datenarchitektur (6j)."
Heute kennt der SAVE-Block AP nur als Waffen-Eigenschaft (`profile.ap`,
`_render_resolution_tab`, `_common.py:689`). Fähigkeiten/Direktiven, die AP
verbessern oder verschlechtern (z. B. Protocol of the Vengeful Stars
secondary: `ap_bonus`, `faction_abilities.yaml:145-149`), fließen weder in
die Rechnung noch in die Anzeige ein. Ziel: EINE kombinierte Badge in der
Badge-Spalte des SAVE-Blocks (D5-Raster), z. B. `AP-2 (Waffe -1, Vengeful
Stars -1)` bzw. Kurzform `<Quelle> AP-1` — statt zweier unzusammenhängender
Zeilen.

## Current state

- `_common.py` `_render_resolution_tab`: `ap = profile.ap` (Z. 689) →
  `resolve_save(base_save, invuln, ap, save_modifiers)` (Z. 755-760).
  Fähigkeits-AP existiert im Codepfad NICHT.
- `_collect_def_save_modifiers` (`_common.py:424-446`): liefert
  save-Modifier (Wert auf den Save-Wurf), KEINE AP-Veränderung — AP und
  Save-Modifier sind regeltechnisch verschieden (AP wirkt vor Cover-Cap etc.).
- `dice_html.py`: `save_modifier_die_pair_html(armour, value, label, color)`
  (Session-37-Signatur) rendert die Modifier-Reihen; Badge-Spalte 96px
  (D5-Spez Punkt 5).
- Protokoll-Effekt `ap_bonus` (necrons, value -1, phase shooting) ist der
  einzige bereits erfasste Fähigkeits-AP-Modifier in YAML. „Enslaved AP-1"
  aus dem ziel6-Beispiel ist KEINER vorhandenen YAML-Fähigkeit zuordenbar
  (geprüft: `enslaved_star_god` ist Auto-Pass-Morale) → Recherche nötig.
- Plan 016 liefert `get_active_protocol_effects(faction_dir, {"ap_bonus"})`.

## Commands you will need

| Zweck | Befehl | Erwartet |
|-------|--------|----------|
| venv | `source .venv/bin/activate` | `(.venv)` |
| Combat-Tests | `python -m pytest tests/gameMechanic/test_combat.py -q` | grün |
| Vollsuite | `pytest --tb=short` | grün, ≥80 % |

## Scope

**In scope**:
- Recherche: welche Fähigkeiten in den drei Fraktionen AP modifizieren
- YAML-Schema: `ap_modifier` als Ability-Effekt-Typ (6j-konform) — nur Schema
  + die in der Recherche gefundenen Einträge
- `src/gameMechanic/ability_engine.py` — Sammel-Helper für Fähigkeits-AP
  (analog `buff_stat_bonus`-Muster)
- `src/uiLayout/_common.py` — effektives AP = Waffen-AP + Fähigkeits-AP in
  `_render_resolution_tab`; kombinierte Badge im SAVE-Block
- `src/uiLayout/dice_html.py` — nur falls die Badge-Spalte einen neuen
  Render-Helper braucht
- Tests

**Out of scope** (NICHT anfassen):
- Stratagem-AP-Modifier (eigenes Schema, `active_modifiers`) — nur melden,
  wenn welche existieren.
- Weitere unverdrahtete Protokoll-Typen (`strength_modifier` etc.).
- D5-Raster/Spaltenlayout selbst — steht; nur Inhalte der Badge-Spalte.

## Git workflow

- Branch: `feature/017-ability-ap-badge`.
- Commit z. B. `Combine ability AP modifiers into the SAVE block badge`.
- Nicht pushen/PR ohne Anweisung.

## Steps

### Step 1: Recherche — AP-modifizierende Fähigkeiten (Lesen, kein Code)

1. `grep -rin "armour penetration\|AP of\|improve.*AP\|worsen.*AP" docs/work/wahapedia_necrons/ docs/work/wahapedia_orks/ docs/work/wahapedia_adeptus_custodes/`
2. Treffer kategorisieren: (a) verbessert eigene Waffen-AP (z. B. Vengeful
   Stars), (b) verschlechtert gegnerische AP / schützt den Verteidiger
   (Wahrscheinlichster Kandidat für das „Enslaved AP-1"-Beispiel des
   Nutzers). Liste mit Quelle/Wortlaut in den Bericht.
3. **Dem Nutzer die Liste + das vorgeschlagene Badge-Format zeigen**
   (eine Nachricht): z. B. Badge-Spalte `AP-2` mit Tooltip/Caption
   `Waffe -1 · Vengeful Stars -1`. Freigabe abwarten (CLAUDE.md:
   Schema-/Design-Entscheidung beim Nutzer).

**Verify**: Freigegebene Liste + Format liegen vor. Ohne Freigabe: STOP.

### Step 2: Schema + Daten

`docs/spec/faction_abilities.md` (6j-Spez) um den Effekt-Typ erweitern:

```yaml
effect:
  type: ap_modifier
  value: 1            # +1 = AP wird um 1 ABGESCHWÄCHT (Verteidiger-Schutz),
                      # -1 = AP um 1 verschärft (Angreifer-Buff)
  applies_to: attacker_weapons | incoming_attacks
  phase: shooting | melee | any
```

Die in Step 1 freigegebenen Fähigkeiten in die jeweiligen
`unit_abilities.yaml`/`faction_abilities.yaml` eintragen (Vorzeichen-
Konvention im Spec-Dokument festhalten — identisch zu `ap_bonus` der
Protokolle, dort ist -1 = Verschärfung).

**Verify**: `python -m pytest tests/gameObjects/test_loader.py -q` grün
(Loader parst die neuen Effekte über den bestehenden `_ability_from_dict`-Pfad).

### Step 3: Engine-Helper

`ability_engine.py`: `ability_ap_modifier(atk_faction, def_faction,
atk_unit, def_unit, phase, use_melee) -> list[dict]` — sammelt:
- aktive Protokoll-Direktiven mit `ap_bonus` (via
  `get_active_protocol_effects`, Plan 016) für den ANGREIFER,
- Abilities mit `effect.type: ap_modifier` beider Seiten gemäß
  `applies_to`/Targeting (Muster `_unit_matches_target` + Conditions wie
  in `buff_stat_bonus`).
Rückgabe: `[{"label": <name_en>, "value": int}, ...]` — Label aus YAML.

**Verify**: Neue Engine-Tests (Angreifer-Buff, Verteidiger-Schutz, keine
aktiven Quellen) grün.

### Step 4: SAVE-Block — Rechnung + kombinierte Badge

`_render_resolution_tab`:
1. `ap_mods = ability_ap_modifier(...)`; `effective_ap = profile.ap +
   sum(values)` (Vorzeichen gemäß Schema; AP nie über 0 „verbessern" —
   `min(0, …)`-Frage in Step 1 mit dem Regelwortlaut klären).
2. `resolve_save(..., ap=effective_ap, ...)`.
3. Badge-Spalte des SAVE-Blocks: kombinierte Badge nach dem in Step 1
   freigegebenen Format; Quellen-Aufschlüsselung als Caption. Buff-Grün /
   Debuff-Rot gemäß design_colors.md §3 (aus Sicht des VERTEIDIGERS:
   abgeschwächtes AP = Buff-Grün, verschärftes = Debuff-Rot).
4. Log/Anzeige konsistent: der Header-AP-Wert (falls irgendwo `profile.ap`
   angezeigt wird) bleibt Waffen-AP; nur der SAVE-Block rechnet effektiv —
   die Badge erklärt die Differenz.

**Verify**: Manuell: Vengeful-Stars-Direktive aktiv (secondary, Shooting) →
SAVE-Block zeigt verschärftes AP mit kombinierter Badge; ohne Direktive →
unverändert. Regressions-Sichtprüfung Save-Modifier-Reihen (Session-37-Fix
darf nicht kippen).

### Step 5: Vollsuite + Lint + Doku

`pytest --tb=short` grün, ≥80 %; Lint passt. `docs/spec/faction_abilities.md`
um den neuen Typ + Vorzeichen-Konvention ergänzt (Step 2).

## Test plan

- Engine: `ability_ap_modifier` — Quellenkombination, Phasen-Filter,
  Targeting.
- Rechnung: effektives AP in `resolve_save`-Aufruf (über einen extrahierten,
  testbaren Helper, z. B. `effective_ap(profile_ap, mods)` in
  `attack_math.py` — gemessen!).
- Keine aktiven Quellen → Verhalten byte-identisch zu heute
  (Regressionstests bestehen unverändert).

## Done criteria

ALLE müssen gelten:

- [ ] Recherche-Liste + Badge-Format vom Nutzer freigegeben (Step 1)
- [ ] `ap_modifier`-Schema dokumentiert + Daten eingetragen
- [ ] Effektives AP fließt in `resolve_save`; kombinierte Badge im SAVE-Block
- [ ] Keine Fraktions-Literale in `src/` (Labels aus YAML)
- [ ] `pytest --tb=short` grün, ≥80 %; Lint passt
- [ ] Bericht: manuelle Verifikationspunkte + Regel-Zitate
- [ ] Status-Zeile in `docs/audit/plans/README.md` aktualisiert

## STOP conditions

- Step-1-Recherche findet KEINE Verteidiger-seitige AP-Fähigkeit und der
  Nutzer kann das „Enslaved AP-1"-Beispiel nicht zuordnen → Scope mit dem
  Nutzer neu schneiden (evtl. nur Protokoll-`ap_bonus` verdrahten).
- Vorzeichen-/Stacking-Regeln (mehrere AP-Quellen, AP-Verbesserung über 0)
  sind im Regelwerk uneindeutig → Wortlaut vorlegen, nicht raten.
- `resolve_save` behandelt AP an mehreren Stellen (z. B. Cover-Cap-Logik)
  und die Änderung müsste in `combat.py` eingreifen → melden; `combat.py`
  ist voll gemessen, Änderungen dort brauchen explizite Tests zuerst.

## Maintenance notes

- `effective_ap` lebt in `attack_math.py` (gemessen) — Reviewer: AP-Mathe
  in Render-Funktionen ablehnen.
- Der `ap_modifier`-Typ ist die generische Schiene für ALLE künftigen
  AP-Fähigkeiten (4. Fraktion!) — keine Spezial-Flags pro Fähigkeit.
