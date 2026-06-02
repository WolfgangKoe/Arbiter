# Wahapedia — WH40K 9th Edition: Crusade Rules

**Source URL:** https://wahapedia.ru/wh40k9ed/the-rules/crusade/ (404 — page not available at this URL)
**Alternate URL attempted:** https://wahapedia.ru/wh40k9ed/the-rules/crusade/crusade-rules/ (404)
**Date Fetched:** 2026-06-02

**Status:** The Wahapedia Crusade rules page returned HTTP 404. The content below is compiled from:
1. The overview reference in the Matched Play page
2. The app's existing spec (`docs/spec/setup.md`)
3. General 9th Edition Crusade rules knowledge

---

## Overview

Crusade is the campaign format for Warhammer 40,000 9th Edition. Unlike Matched or Open Play, Crusade tracks persistent campaign progress: units gain experience, earn battle honours, suffer battle scars, and can be permanently destroyed. Each player maintains a **Crusade Roster** and an **Order of Battle**.

---

## Force Creation

### Crusade Roster
- Each player maintains a Crusade Roster — a list of all units available to their Crusade force.
- The Roster has a **Supply Limit** (measured in Power Level), which caps how many units can be on the roster.
- Starting Supply Limit is typically 50 PL (Combat Patrol size) and grows as the campaign progresses.
- Units are added to the roster between games; they cannot be added mid-campaign without cause.

### Order of Battle
- Before each game, each player selects a subset of their Crusade Roster to form their **Order of Battle** (the actual force used in the game).
- The Order of Battle is limited by the agreed battle size (same point/PL limits as Matched/Open Play).
- Units NOT on the Order of Battle stay at the base and do not participate in the game.

### Crusade Points
- Units accumulate **Crusade Points** (experience) by participating in battles and achieving objectives.
- Crusade Points unlock **Battle Honours** (upgrades: Weapon Enhancements, Stratagems, Traits, etc.) and track unit history.
- Units can also gain **Battle Scars** (permanent negative effects from being destroyed or failing tests).

---

## Pre-Battle Sequence (Crusade)

Crusade games broadly follow the Matched Play pre-battle sequence with the following additions:

1. **Agree battle size** — determines Order of Battle size limit.
2. **Muster Order of Battle** — each player selects units from their Crusade Roster up to the agreed limit.
3. **Apply Requisitions** — players may spend Requisition Points to add units, upgrade them, or other campaign actions before the game.
4. **Proceed as Matched Play** — from Step 3 (Determine Mission) onwards, the sequence follows Matched Play (or an agreed Crusade mission pack).

---

## CP Rules in Crusade

Crusade uses the same starting CP as Matched Play, based on the agreed battle size:

| Battle Size   | Starting CP |
|---------------|-------------|
| Combat Patrol | 3           |
| Incursion     | 6           |
| Strike Force  | 12          |
| Onslaught     | 18          |

---

## Post-Battle Sequence

After each Crusade game, both players resolve the following:

1. **Determine Outcome** — win/loss/draw recorded.
2. **Experience Points** — surviving units and units that achieved objectives gain XP / Crusade Points.
3. **Battle Honours** — units with sufficient Crusade Points may select a Battle Honour.
4. **Battle Scars** — units destroyed during the game may gain Battle Scars (roll on a table or choose).
5. **Casualties** — units with too many Battle Scars can be permanently removed (destroyed forever).
6. **Requisition Points** — players earn Requisition Points to spend between games (adding units to roster, increasing Supply Limit, etc.).
7. **Update Crusade Roster** — record all changes.

---

## Key Crusade Concepts

| Term                | Meaning                                                                 |
|---------------------|-------------------------------------------------------------------------|
| Supply Limit        | Max Power Level allowed on the Crusade Roster (grows over campaign)     |
| Order of Battle     | Units selected from Roster for a specific game                          |
| Crusade Points      | Experience accumulated by units (enables Battle Honours)                |
| Battle Honours      | Permanent upgrades earned by experienced units                          |
| Battle Scars        | Permanent negative effects from being destroyed                         |
| Requisition Points  | Campaign currency spent between games to expand/upgrade the force       |
| Out of Action       | A unit removed mid-campaign due to accumulated Battle Scars             |

---

## Differences from Matched Play

| Aspect                 | Matched Play                  | Crusade                                      |
|------------------------|-------------------------------|----------------------------------------------|
| Army source            | Fresh list each game          | Persistent Crusade Roster                    |
| Unit upgrades          | Via Stratagems (per-game)     | Via Battle Honours (persistent)              |
| Unit limits            | Any valid units               | Only units on your Crusade Roster            |
| Army size limit        | Points per battle size        | Order of Battle from Roster (PL or points)   |
| Post-game              | Nothing persists              | XP, scars, honours, requisitions all tracked |
| Campaign structure     | None                          | Full campaign with growing forces            |

---

## App Implementation Notes (from `docs/spec/setup.md`)

The current spec references Crusade but defers details to Ziel 6:
- "Jeder Spieler hat ein Crusade Roster mit einem Versorgungslimit (Supply Limit)"
- "Einheiten haben Crusade Points (Erfahrung, Narben, Auszeichnungen)"
- "Vor dem Spiel: Einheiten aus dem Crusade Roster auf die Order of Battle wählen"
- "Punktlimit der Partie bestimmt Größe der Order of Battle"
- "Nach dem Spiel: Crusade Points vergeben, Narben/Auszeichnungen eintragen"

---

## Notes

- Wahapedia's Crusade page was inaccessible (404) — the URL structure may differ or the page requires navigation from within the site.
- Crusade rules span multiple chapters in the Core Book; the core mechanics above are well-established 9th Edition rules.
- The Crusade system is significantly more complex than either Matched or Open Play; full implementation belongs in Ziel 6.
