# Necrons Katalog — Verifikationsbefund
> Erstellt: 2026-05-30 | Quelle: Wahapedia 9E (scraper tools/wahapedia_scraper.py) + BattleScribe
> Status: **Noch nicht umgesetzt** — Freigabe ausstehend
> Scraper läuft mit: `python3 tools/wahapedia_scraper.py necrons --all`

---

## Zusammenfassung

| Bereich | Fehler |
|---------|--------|
| units.yaml — Statlines falsch | 11 Felder in 7 Einheiten |
| units.yaml — Keywords falsch/fehlend | 8 Einheiten |
| units.yaml — Abilities-Texte falsch | 2 Einheiten |
| units.yaml — `attacks`-Feld komplett fehlend | alle 13 Einheiten |
| units.yaml — Lychguard invuln_save falsch | 1 Einheit |
| weapons.yaml — Falsche Werte | 8 Waffen |
| weapons.yaml — Fehlende Definitionen | 18 Waffen |
| weapons.yaml — Falsche Zuweisung (Spyder) | 1 Einheit |
| stratagems.yaml — Alle Einträge falsch | 15/15 |
| Katalog — Fehlende Einheiten | ≥ 2 (Technomancer, Lokhust Heavy Destroyers) |

---

## 1. UNITS.YAML — Bestätigte Statline-Fehler

Alle Werte direkt aus Wahapedia-Scraper (Stand 2026-05-30).

| Einheit | Feld | Ist (YAML) | Soll (Wahapedia) |
|---------|------|------------|------------------|
| `overlord` | `invuln_save` | null | **4** (Phase Shifter: 4+ invuln) |
| `royal_warden` | `strength` | 4 | **5** |
| `deathmarks` | `toughness` | 4 | **5** |
| `canoptek_wraiths` | `ws` | "3+" | **"4+"** |
| `canoptek_wraiths` | `strength` | 6 | **4** |
| `canoptek_wraiths` | `invuln_save` | 3 | **4** (Wraith Form: 4+ invuln) |
| `lychguard` | `ws` | "2+" | **"3+"** |
| `lychguard` | `invuln_save` | 4 | **null** (invuln nur mit Dispersion Shield wargear, nicht Default) |
| `annihilation_barge` | `ws` | "3+" | **"6+"** |
| `annihilation_barge` | `strength` | 6 | **5** |
| `annihilation_barge` | `wounds` | 12 | **8** |
| `canoptek_scarabs` | `bs` | "4+" | **"-"** (Scarabs kein Fernkampf, BS=Dash) |
| `canoptek_spyder` | `battlefield_role` | [Heavy Support] | **[Elites]** |

---

## 2. UNITS.YAML — Bestätigte Keyword-Fehler

Wahapedia-Keywords (ohne `<DYNASTY>` und dynasty-sub-Namen wie MEPHRIT etc.):

| Einheit | Ist (YAML) | Soll (Wahapedia) | Delta |
|---------|------------|------------------|-------|
| `overlord` | Infantry, Character, Noble, Overlord, Necrons, **Living Metal** | INFANTRY, CHARACTER, NOBLE, OVERLORD | Living Metal raus (ist eine Rule, kein Keyword) |
| `royal_warden` | Infantry, Character, **Noble**, Royal Warden, Necrons, Living Metal, **Core** | INFANTRY, CHARACTER, ROYAL WARDEN | Noble falsch, Core falsch, Living Metal raus |
| `plasmancer` | Infantry, Character, Cryptek, Plasmancer, Necrons, Living Metal | INFANTRY, CHARACTER, **FLY**, CRYPTEK, PLASMANCER | Fly fehlt, Living Metal raus |
| `warriors` | Infantry, Core, Necrons, Necron Warriors, **Reanimation Protocols**, **Their Number is Legion** | INFANTRY, CORE, NECRON WARRIORS | Abilities-Keywords raus |
| `immortals` | Infantry, Core, Necrons, Immortals, **Reanimation Protocols** | INFANTRY, CORE, IMMORTALS | Reanimation Protocols raus |
| `skorpekh_destroyers` | Infantry, Core, Destroyer Cult, Necrons, Skorpekh Destroyers, **Reanimation Protocols**, **Living Metal** | INFANTRY, CORE, DESTROYER CULT, SKORPEKH DESTROYERS | Rules-Keywords raus |
| `lychguard` | Infantry, Core, Necrons, Lychguard, **Reanimation Protocols** | INFANTRY, CORE, LYCHGUARD | Reanimation Protocols raus |
| `deathmarks` | Infantry, Core, Necrons, Deathmarks, **Reanimation Protocols** | INFANTRY, CORE, **HYPERSPACE HUNTER**, DEATHMARKS | Hyperspace Hunter fehlt; Reanimation Protocols raus |
| `canoptek_wraiths` | **Infantry**, **Fly**, Canoptek, Necrons | **BEAST**, CORE, **FLY**, CANOPTEK, CANOPTEK WRAITHS | Infantry → Beast, Core fehlt, Fly bleibt ✓ |
| `canoptek_spyder` | **Vehicle**, Fly, Canoptek, Necrons, Living Metal | **MONSTER**, CORE, FLY, CANOPTEK, CANOPTEK SPYDERS | Vehicle → Monster, Core fehlt, Living Metal raus |
| `annihilation_barge` | Vehicle, Fly, Quantum Shielding, Necrons, Living Metal | VEHICLE, **CORE**, QUANTUM SHIELDING, FLY, ANNIHILATION BARGE | Core fehlt, Living Metal raus, ANNIHILATION BARGE hinzu |
| `triarch_stalker` | Vehicle, Core, Triarch, Dynastic Agent, Quantum Shielding, Necrons, **Living Metal** | VEHICLE, CORE, DYNASTIC AGENT, QUANTUM SHIELDING, TRIARCH, TRIARCH STALKER | Living Metal raus, TRIARCH STALKER hinzu |

**Regel für alle Einheiten:** `Living Metal`, `Reanimation Protocols`, `Their Number is Legion` sind **Rules** (rules: []), keine Keywords. Aus dem keywords-Feld entfernen.

---

## 3. UNITS.YAML — Abilities-Texte falsch

### Overlord — My Will Be Done
- **Ist:** `"...re-roll a hit roll of 1"`
- **Soll:** `"...add 1 to that attack's hit roll."` — anderer Mechanismus!

### Plasmancer — Living Lightning (bisher fehlend/falsch)
- **In YAML:** `"Harbinger of Destruction: ...on hit roll of 6, target suffers 1 MW"` — FALSCH
- **Soll:** Zwei separate Abilities:
  1. `"Living Lightning: At the start of the Fight phase, roll one D6 for each enemy unit within 6\". On a 4+, that unit suffers 1 mortal wound."`
  2. `"Harbinger of Destruction: At the end of your Movement phase (if this model did not Fall Back), roll three D6. For each result of 4+, the closest visible enemy unit within 24\" suffers 1 mortal wound."`

---

## 4. UNITS.YAML — Schema-Lücke: `attacks` fehlt überall

Das `attacks`-Feld (A-Charakteristik) fehlt in allen Einheiten. Bestätigte Werte vom Scraper:

| Einheit | A |
|---------|---|
| overlord | 4 |
| royal_warden | 3 |
| plasmancer | 1 |
| warriors | 1 |
| immortals | 2 |
| skorpekh_destroyers | 3 |
| lychguard | 3 |
| deathmarks | 1 |
| canoptek_scarabs | 4 |
| canoptek_wraiths | 4 |
| triarch_stalker | 3 |
| annihilation_barge | 3 |
| canoptek_spyder | 5 |

---

## 5. WEAPONS.YAML — Bestätigte Fehler

| Waffe | Feld | Ist | Soll | Bestätigt durch |
|-------|------|-----|------|-----------------|
| `gauss_flayer` | `ap` | "0" | **"-1"** | Scraper: Rapid Fire 1, S4, AP-1, D1 |
| `gauss_cannon` | `ap` | "-2" | **"-3"** | Scraper: Heavy 3, S6, AP-3, D D3 |
| `gauss_cannon` | `damage` | "2" | **"D3"** | Scraper |
| `hyperphase_threshers` | `strength` | "5" | **"User"** | Scraper: Melee, User, AP-3, D2 |
| `hyperphase_reap_blade` | `strength` | "7" | **"User+2"** | Scraper: Melee, +2, AP-4, D3 (S5+2=7, User+2 besser) |
| `warscythe` | `strength` | "8" | **"User+2"** | Scraper: Melee, +2, AP-4, D2 (S5+2=7, nicht 8!) |
| `hyperphase_sword` | `strength` | "5" | **"User+1"** | Scraper: Melee, +1, AP-3, D1 |
| `tachyon_arrow` | `strength` | "10" | **"12"** | Scraper: Assault 1, S12, AP-5, D D6 |
| `feeder_mandibles` | `strength` | "3" | **"User"** | Scraper: Melee, User, AP0, D1 |
| `stalkers_forelimbs` | `strength` | "7" | **"User"** | Scraper: Melee, User, AP-2, D3 |
| `stalkers_forelimbs` | `damage` | "3" | **"3"** | Scraper: D3 als fixer Wert — bleibt (kein D3-Würfel, fester Wert 3) |
| `voidscythe` | `strength` | "10" | **"User×2"** | Scraper: Melee, x2, AP-4, D3 — numerisch OK (5×2=10), Notation anpassen |
| `heat_ray_focused` | abilities | "D6+3" (Halbreichweite) | **"D6+2"** | Scraper-Abilitiestext (teilweise erfasst) |

**Strength-Notation:** Wahapedia zeigt relative Stärken als `+2`, `User`, `x2`. Empfehlung: `"User"` für gleiche Stärke, `"User+1"` / `"User+2"` für relative, `"User×2"` für doppelte.

---

## 6. WEAPONS.YAML — Fehlende Definitionen (18 Waffen)

Alle Werte vom Wahapedia-Scraper bestätigt. Geordnet nach Einheit:

### Overlord (optional)
| id | Typ | Range | A | S | AP | D | Abilities |
|----|-----|-------|---|---|----|---|-----------|
| `hyperphase_glaive` | Melee | — | * | User+2 | -3 | D3 | — |
| `voidblade` | Melee | — | * | User | -3 | 1 | Each time bearer fights, +1 attack |

### Royal Warden
| id | Typ | Range | A | S | AP | D |
|----|-----|-------|---|---|----|---|
| `relic_gauss_blaster` | Rapid Fire 2 | 30" | 2 | 5 | -2 | 2 |

### Plasmancer
| id | Typ | Range | A | S | AP | D |
|----|-----|-------|---|---|----|---|
| `plasmic_lance_shooting` | Assault D3 | 18" | D3 | 7 | -3 | 2 |
| `plasmic_lance_melee` | Melee | — | * | User | -3 | 2 |

> Hinweis: Plasmic Lance ist eine Dual-Profile-Waffe. Beide Profile als separate IDs anlegen oder mit `profiles:`-Substruktur.

### Immortals
| id | Typ | Range | A | S | AP | D | Abilities |
|----|-----|-------|---|---|----|---|-----------|
| `gauss_blaster` | Rapid Fire 1 | 30" | 1 | 5 | -2 | 1 | — |
| `tesla_carbine` | Assault 2 | 24" | 2 | 5 | 0 | 1 | Unmod. 6 to hit = 2 extra hits |

### Deathmarks
| id | Typ | Range | A | S | AP | D | Abilities |
|----|-----|-------|---|---|----|---|-----------|
| `synaptic_disintegrator` | Heavy 1 | 36" | 1 | 5 | -2 | 1 | Unmod. 6 to wound = +1 MW; ignoriert "Look Out, Sir" |

### Canoptek Wraiths (alle drei: default + optional)
| id | Typ | Range | A | S | AP | D | Abilities |
|----|-----|-------|---|---|----|---|-----------|
| `vicious_claws` | Melee | — | * | User+2 | -2 | 2 | — |
| `whip_coils` | Melee | — | * | User | -1 | 1 | Makes 2 hit rolls per attack |
| `particle_caster` | Pistol 2 | 12" | 2 | 6 | 0 | 1 | — |
| `transdimensional_beamer` | Assault 1 | 12" | 1 | 4 | -3 | 3 | — |

### Triarch Stalker (optionale Ersatzwaffen)
| id | Typ | Range | A | S | AP | D |
|----|-----|-------|---|---|----|---|
| `twin_heavy_gauss_cannon` | Heavy 6 | 30" | 6 | 7 | -3 | D3 |
| `particle_shredder` | Heavy 8 | 24" | 8 | 6 | -1 | 2 |

### Annihilation Barge
| id | Typ | Range | A | S | AP | D | Abilities |
|----|-----|-------|---|---|----|---|-----------|
| `tesla_cannon` | Heavy 3 | 30" | 3 | 6 | 0 | 1 | Unmod. 6 to hit = 2 extra hits |
| `twin_tesla_destructor` | Heavy 10 | 36" | 10 | 7 | 0 | 1 | Unmod. 6 to hit = 2 extra hits |

### Canoptek Spyder
| id | Typ | Range | A | S | AP | D |
|----|-----|-------|---|---|----|---|
| `automaton_claws` | Melee | — | * | User+2 | -3 | 2 |

`*` = Attackzahl aus Einheiten-Stat, nicht aus Waffe (Melee-Waffen nutzen Einheiten-A-Wert)

---

## 7. WEAPONS.YAML — Falsche Zuweisung

| Einheit | Ist | Soll |
|---------|-----|------|
| `canoptek_spyder` | `close_combat_weapon` | **`automaton_claws`** |

Bestätigt durch BattleScribe + Wahapedia-Scraper.

---

## 8. STRATAGEMS.YAML — Komplett neu aufbauen

Alle 15 aktuellen Einträge sind entweder nicht im Codex vorhanden oder haben falsche Effekte.

| Unser Name | Problem |
|------------|---------|
| `adaptive_subroutines` | Nicht im Codex |
| `reclaim_the_galaxy` | Falsch: "Reclaim a Lost Empire" ist Nihilakh-only, anderer Effekt |
| `talent_for_annihilation` | Falsch: Mephrit-only, Effekt = Wound 6+ → +1 MW |
| `counter_tactics` | Nicht im Codex |
| `disruption_fields` | Existiert, aber Effekt falsch: echt = "+1 Strength" (nicht extra hit) |
| `their_number_is_legion` | Unit-Regel, kein Stratagem |
| `we_are_undying` | Nicht im Codex (verwechselt mit Resurrection Protocols) |
| `eternal_warrior` | Nicht im Codex |
| `acquire_and_destroy` | Nicht im Codex |
| `eternal_madness` | Nicht im Codex |
| `entropic_strike` | Falsch: C'TAN SHARD (2CP), nicht Scarabs (1CP); anderer Effekt |
| `programmed_retreat` | Nicht im Codex (nächster: Enslaved Protectors) |
| `quantum_deflection` | Existiert, aber: feste 4+ invuln, nicht "improve by 1" |
| `relentless_advance` | Nicht im Codex |
| `warp_pulse` | Nicht im Codex (nächster: Szarekhan Empyric Damping) |

### Echte Kern-Stratagems (Main Codex, aus Wahapedia gesichert)

| Name | CP | Phase | Bedingung | Effekt |
|------|----|-------|-----------|--------|
| Dimensional Corridor | 1 | Movement | DYNASTY CORE INFANTRY | Einheit durch Monolith teleportieren |
| Techno-Oracular Targeting | 1 | Shooting | beliebig | Auto-wound |
| Extermination Protocols | 2 | Shooting | LOKHUST DESTROYERS/HEAVY | Re-roll wound rolls |
| Storm of Flensing Blades | 2 | Fight (end) | FLAYED ONES | Fight again |
| Fractal Targeting | 1 | Shooting | TOMB BLADES | RF = Assault 2, kein Advance-Penalty |
| Judgement of the Triarch | 1 | Shoot/Fight | TRIARCH | +1 to hit |
| Eternal Protectors | 1 | Fight | LYCHGUARD + NOBLE | +1 Attacks |
| Resurrection Protocols | 1 | Any | INFANTRY NOBLE/CRYPTEK | D6 end of phase: 4+ = zurück mit D3W |
| Strange Echoes | 1 | Command | C'TAN SHARD | C'tan Power tauschen |
| The Deathless Arise | 1 | Command | TECHNOMANCER | Rites of Reanimation extra use |
| Dimensional Destabilisation | 2/1 | Movement | C'TAN SHARD | Extra C'tan Power |
| Entropic Strike | 2 | Fight | C'TAN SHARD | Invulns negieren |
| Hand of the Phaeron | 2 | Before Battle | OVERLORD | Overlord = Phaeron, My Will Be Done extra |
| Dynastic Heirlooms | 1 | Before Battle | WARLORD | Relic vergeben |
| Rarefied Nobility | 1 | Before Battle | WARLORD | Warlord Trait vergeben |
| Enslaved Protectors | 1 | Charge (Gegner) | CANOPTEK | Heroic Intervention |
| Stellar Alignment Protocol | 2/1 | Command | VEHICLE 10+ W | Voll-Profil bis nächste Command Phase |
| Reanimation Prioritisation | 2 | Shooting (Gegner) | mit REANIMATOR | Reanimation Beam einsetzen |
| Burrowing Nightmares | 1 | Movement | OPHYDIAN DESTROYERS | Abtauchen + Wiederauftauchen |
| Self-Destruction | 1 | Fight | CANOPTEK SCARAB SWARMS | D6: 2-5 = D3 MW, 6 = 3 MW; Model zerstört |
| Prismatic Dimensional Breach | 1 | Movement | CORE in Reserves + NIGHT SCYTHE/MONOLITH | Deployment aus Transportmodell |
| Shadows of Drazak | 1 | Any | FLAYED ONES | -1 to hit gegen diese Einheit |
| Aetheric Interception | 1 | Movement (Gegner) | HYPERSPACE HUNTER | Intercept Reinforcements + Shoot |
| Relentless Onslaught | 1 | Shooting | CORE INFANTRY | Rapid Fire unmod. 6 = extra hit |
| Curse of the Phaeron | 3/1 | Any | VEHICLE zerstört | Explodes auto |
| Atavistic Instigation | 1 | Shooting | DOOM SCYTHE | nach heavy death ray: D3 MW |
| Revenge of the Doomstalker | 2 | Any | CHARACTER zerstört + DOOMSTALKER | Doomstalker schießt sofort |
| Disruption Fields | 1 | Fight | NECRONS CORE | +1 Strength der Einheit |
| Disintegration Capacitors | 1 | Shooting | Gauss-Waffe | Unmod. 6 to hit = auto-wound |
| Malevolent Arcing | 1 | Shooting | Tesla-Waffe | nach Angriff: D6 je benachbarte Einheit: 4+ = 1 MW |
| Whirling Onslaught | 1 | Any | SKORPEKH DESTROYERS/LORD | -1 to wound gegen diese Einheit |
| Quantum Deflection | 1 | Any | QUANTUM SHIELDING | 4+ invuln bis Ende Phase |
| Solar Pulse | 1 | Shooting | beliebig | Ziels Cover wird ignoriert |
| Reconstitution Protocols | 1 | Command | GHOST ARK | Repair Barge = D6 statt D3 |

**Dynastic Stratagems:**

| Name | CP | Dynast | Effekt |
|------|----|--------|--------|
| Talent for Annihilation | 1 | Mephrit | Wound-Unmod. 6 = +1 MW (max 3/Phase) |
| Translocation Crypt | 1 | Nephrekh | Unit bekommt Dimensional Translocation |
| Reclaim a Lost Empire | 1 | Nihilakh | Aktion + Schießen in gleicher Phase erlaubt |
| Blood Rites | 1 | Novokh | +1 Attacks |
| Methodical Destruction | 2 | Sautekh | Friendly Sautekh +1 to hit auf markiertes Ziel |
| Empyric Damping | 1 | Szarekhan | 4+: Psychic-Power negieren |

---

## 9. Fehlende Einheiten (via BattleScribe + Scraper bestätigt)

### Technomancer (aus Vanguard-Detachment BattleScribe, Scraper ausgeführt)
| Stat | Wert |
|------|------|
| M | 5" |
| WS | 3+ |
| BS | 3+ |
| S | 4 |
| T | 4 |
| W | 4 |
| A | 1 |
| Ld | 10 |
| Sv | 4+ |
| Invuln | none |
| KW | INFANTRY, CHARACTER, CRYPTEK, TECHNOMANCER |
| Weapons | Staff of light (shooting+melee) |
| Abilities | Dynastic Advisors, Rites of Reanimation, Living Metal |

### Lokhust Heavy Destroyers (aus Vanguard-Detachment BattleScribe, Scraper ausgeführt)
| Stat | Wert |
|------|------|
| M | 8" |
| WS | 3+ |
| BS | 3+ |
| S | 4 |
| T | 5 |
| W | 4 |
| A | 2 |
| Ld | 10 |
| Sv | 3+ |
| Invuln | none |
| KW | INFANTRY, CORE, FLY, DESTROYER CULT, LOKHUST HEAVY DESTROYERS |
| Weapons | gauss_destructor (36" Heavy 1, S10, AP-4, D 3D3) oder enmitic_exterminator (36" Heavy 3D3, S7, AP-1, D1 Blast) |
| Abilities | Living Metal, Reanimation Protocols, Hardwired for Destruction |

---

## 10. Offene Fragen — Alle beantwortet (scraper-gesichert)

| Frage | Antwort |
|-------|---------|
| Annihilation Barge Wounds | **8** (scraper bestätigt W:8) |
| Stalker Forelimbs Damage | **3** (fixer Wert, kein D3-Würfel) |
| Supplement-Stratagems rein? | Nein — nur Main Codex + Dynastic zunächst |
| `attacks`-Feld in Spec? | Ja, muss ergänzt werden |
| Strength-Notation | "User", "User+1", "User+2", "User×2" |
| Living Metal als Keyword? | Nein — ist eine Rule, nicht Keyword |
| Overlord Wargear komplett? | Scraper hat alle 8 Profile erfasst — falls Freigabe: vollständig eintragen |

---

## Umsetzungs-Reihenfolge (nach Freigabe)

1. `docs/spec/army_builder.md` — Schema um `attacks`-Feld erweitern
2. `data/wh40k_9e/necrons/units.yaml` — alle Statlines, Keywords, Abilities, `attacks` korrigieren
3. `data/wh40k_9e/necrons/weapons.yaml` — 18 fehlende Waffen + 13 fehlerhafte Felder
4. `data/wh40k_9e/necrons/stratagems.yaml` — Komplett neu aufbauen
5. Neue Einheiten: Technomancer + Lokhust Heavy Destroyers in units.yaml ergänzen
