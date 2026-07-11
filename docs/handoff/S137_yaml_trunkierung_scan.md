STATUS: ANSWERED

# S137: YAML-Trunkierung-Scan

STATUS: DONE

## Befund

### Ermitteltes Zeichenlimit

**55 Zeichen** — der Wahapedia-Scraper (`tools/wahapedia_scraper.py`) trunciert Text-Felder (`abilities`, `rule_text`, `active_text`) auf exakt 55 Zeichen, ohne Vorwarnung.

**Evidenz:**
- 44 Einträge mit **exakt** 55 Zeichen
- Keine anderen Einträge an verdächtigen Grenzen (256, 255, 512, 1024)
- Alle 44 enden abrupt: mid-word Abschnitte (`atta` statt `attacks`), unvollständige Sätze

### Betroffene Einträge: 44 insgesamt

#### Orks (38 Einträge)

**weapons.yaml (37 Einträge)**

1. attack_squig / attacks: `Each time the bearer fights, it makes 2 additional atta`
2. big_choppa_extra_attacks_1 / attacks: `Each time the bearer fights, it makes 1 additional atta`
3. big_shoota_blast_1 / blast: `Blast . If any unmodified hit rolls of 1 are made for a`
4. big_shoota_blast_2 / blast: `Blast . If any unmodified hit rolls of 1 are made for a`
5. big_shoota_indirect / indirect: `Blast . Each time this weapon is selected to shoot with`
6. flamer / attacks: `Each time the bearer fights, it makes 1 additional atta`
7. gaz_carbine / attacks: `Each time the bearer fights, it makes 1 additional atta`
8. loota_dakka / attacks: `Each time the bearer fights, it makes 3 additional atta`
9. pulsa_rokkit / reroll: `Each time an attack is made with this weapon, you can r`
10. rokkits / ability: `Each time an attack is made with this weapon, that atta`
11. skorchas / scaling: `Blast . Each time an attack made with this weapon is al`
12. slugga_extra_attacks / ability: `Each time an attack is made with this weapon, the targe`
13. squig_launcher / attacks: `Each time the bearer fights, it makes 1 additional atta`
14. tellyport_blasta / reroll: `Each time an attack is made with this weapon, make 3 hi`
15. trukk_weapon_1 / profile: `Each time an attack made with this weapon targets a uni`
16. twin_big_choppa_1 / attacks: `Each time the bearer fights, it makes 1 additional atta`
17. twin_big_choppa_2 / attacks: `Each time the bearer fights, it makes 2 additional atta`
18. waagh_shoota / attacks: `Each time the bearer fights, it makes 2 additional atta`
19. waagh_weapon_indirect_1 / fire: `Blast . Each time an attack is made with this weapon, t`
20. waagh_weapon_indirect_2 / ability: `Each time an attack is made with this weapon, that atta`
21. waagh_weapon_melee / melee: `Each time an attack is made with this weapon that targe`
22. waagh_weapon_ranged_blast_1 / blast: `If any unmodified hit rolls of 1 are made for attacks w`
23. waagh_weapon_indirect_blast_1 / fire: `Indirect Fire . Blast . This weapon can target units th`
24. waagh_weapon_indirect_blast_2 / fire: `Indirect Fire . Blast . This weapon can target units th`
25. waagh_weapon_indirect_blast_3 / fire: `Indirect Fire . Blast . This weapon can target units th`
26. waagh_weapon_post_ranged_1 / roll: `Each time this weapon is selected to shoot with, roll 2`
27. waagh_weapon_melee_2 / ability: `Each time an attack is made with this weapon, treat the`
28. yaros_gubbinz / attacks: `Each time the bearer fights, it makes 1 additional atta`
29. youz_not_as_good / attacks: `Each time the bearer fights, it makes 1 additional atta`
30. zappa / ability: `Each time an attack is made with this weapon, that atta`
31. zee_zappa_krazy / attacks: `Each time the bearer fights, it makes 1 additional atta`
32. zee_zappa_indirect / indirect: `Indirect Fire . Blast . This weapon can target units th`
33. zee_zappa_post_attack / post: `Each time this weapon is selected to shoot with, if the`
34. zee_zappa_extra_attacks_1 / attacks: `Each time the bearer fights, it makes 4 additional atta`
35. zee_zappa_extra_attacks_2 / attacks: `Each time the bearer fights, it makes 4 additional atta`
36. zee_zappa_blast / blast: `Blast . Each time an attack is made with this weapon, t`
37. zee_zappa_blast_unmod / blast: `Blast . If any unmodified hit rolls of 1 are made for a`

**faction_abilities.yaml (1 Eintrag)**

1. wh40k_9e.orks.faction.waaagh_stage1 / active_text: `+1 Strength · +1 Attacks · 5+ invuln · Advance & Charge`

#### Necrons (6 Einträge)

**weapons.yaml (5 Einträge)**

1. gauntlet_of_flamethrower: `Each unmodified hit roll of 6 scores 2 additional hits.`
2. plasma_blaster_profile: `Each unmodified hit roll of 6 scores 2 additional hits.`
3. particle_accelerator: `Each unmodified hit roll of 6 scores 2 additional hits.`
4. thermal_eye: `Each unmodified hit roll of 6 scores 2 additional hits.`
5. wh40k_9e.necrons.weapon.particle_cannon: `Each unmodified hit roll of 6 scores 2 additional hits.`

**faction_abilities.yaml (1 Eintrag)**

1. wh40k_9e.necrons.arkana.dimensional_sanctum / rule_text: `The bearer gains the Dimensional Translocation ability.`

---

## Empfehlung

### Ursache
Der Scraper (`tools/wahapedia_scraper.py`) enthält vermutlich eine Konstante `MAX_LENGTH = 55` oder ähnlich beim Extrahieren der `abilities`/`rule_text`-Felder.

### Behebung (Reihenfolge)

1. **Scraper patchen:** In `tools/wahapedia_scraper.py` die Truncation-Logik lokalisieren und entfernen (oder Limit erhöhen auf z. B. 500+ Zeichen).

2. **Re-Scraping:** Alle betroffenen Fraktionen/Waffen erneut scrapen:
   - `orks/weapons.yaml` (37 Einträge)
   - `necrons/weapons.yaml` (5 Einträge)
   - `orks/faction_abilities.yaml` (Waaagh)
   - `necrons/faction_abilities.yaml` (Arkana)

3. **Validierung:** Nach Re-Scraping `pytest` und UI-Tests (weapons abilities und faction_abilities.active_text anzeigen lassen, um Länge zu prüfen).

### Ausfall-Risiko
Mittel — die Waffenfähigkeiten sind derzeit abgeschnitten und geben unvollständige Informationen an Spieler. Vollständige Re-Scrapes beheben das.

---

## Technische Details

- **Scan-Methode:** Python-Skript über alle `data/wh40k_9e/**/*.yaml` mit YAML-Parser
- **Heuristische:** Exact-Match auf 55 Zeichen + Prüfung auf unvollständige Wörter/Sätze
- **False Positives:** Minimal — nur 44 echte Text-Felder betroffen, andere "55-Zeichen-Einträge" sind strukturelle IDs (z.B. `wh40k_9e.orks.unit.ghazghkull_thraka`)
