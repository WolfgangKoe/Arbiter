# Adeptus Custodes — Datendokumentation

> Stand: 2026-06-04 | Quelle: Wahapedia WH40k 9E

---

## Ka'tahs of the Broadsword (`round_choice`)

Geladen via `load_round_choice_abilities("adeptus_custodes")`.  
`round_choice_label: "Ka'tahs of the Broadsword"`  
**Kein** `auto_round_1` — Spieler wählt frei ab Runde 1.

| Ka'tah ID | Name | Subfaction Affinity (Shield Host) | Aggressive Stance | Stoic Stance |
|-----------|------|-----------------------------------|-------------------|--------------|
| `katah_calistus` | Calistus Ka'tah | **solar_watch** | +D6" Advance | Zählt als stationär |
| `katah_conservai` | Conservai Ka'tah | **emissaries_imperatus** | Actions während Advance/Fall Back | Schießen während Actions |
| `katah_dacatarai` | Dacatarai Ka'tah | dread_host | Gegner Pile-In/Consolidate nur 1" | +1 Angriff mit Damage-1-Waffen |
| `katah_salvus` | Salvus Ka'tah | aquilan_shield | +4" Waffenreichweite | Auric-Waffen schießen 2× wenn stationär |
| `katah_rendax` | Rendax Ka'tah | **emperors_chosen** | Unmod. 6 verwundet VEHICLE/MONSTER auto | +1 Strength nach Charge |
| `katah_kaptaris` | Kaptaris Ka'tah | shadowkeepers | Gegner kann Hits nicht re-rollen | Gegner kann nicht Fall Back |

> **Hinweis:** 3 Korrekturen 2026-06-04 via Wahapedia:
> - calistus: emissaries_imperatus → **solar_watch**
> - conservai: solar_watch → **emissaries_imperatus**
> - rendax: wardens → **emperors_chosen**

---

## Shield Hosts (Subfaction IDs)

| ID | Shield Host |
|----|-------------|
| `solar_watch` | Solar Watch |
| `emissaries_imperatus` | Emissaries Imperatus |
| `dread_host` | Dread Host |
| `aquilan_shield` | Aquilan Shield |
| `emperors_chosen` | Emperor's Chosen |
| `shadowkeepers` | Shadowkeepers |
