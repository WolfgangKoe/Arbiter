# Setup — Spec

> Ziel 5a. Beschreibt den Setup-Screen und die Spielmodi (Matched / Open / Crusade).
> Crusade-Details: Ziel 6.

---

## Spielmodi

| Modus | Einheitenwahl | Punkte | CP | Crusade-Mechaniken |
|-------|--------------|--------|----|--------------------|
| **Matched Play** | Armeeliste (Punkte) | Pflicht | Detachment-Regeln | nein |
| **Open Play** | Beliebig | optional (Power Level) | fest: 3 CP | nein |
| **Crusade** | Crusade Roster | Versorgungslimit | wie Matched | ja (Ziel 6) |

---

## Matched Play

### Spielgrößen

| Größe | Punkte | Start-CP | Missionen |
|-------|--------|----------|-----------|
| Combat Patrol | ≤ 500 | 3 | Incisive Attack, Outriders, Encircle |
| Incursion | ≤ 1000 | 6 | 6 Missionen (Divide and Conquer – Shifting Front) |
| Strike Force | ≤ 2000 | 12 | 6 Missionen (Retrieval Mission – Vital Intelligence) |
| Onslaught | ≤ 3000 | 18 | Lines of Battle, All-out War, Pathway to Glory |

Quelle: Wahapedia Matched Play — `docs/work/wahapedia_matched_play.md` (2026-06-02)

**Hinweis Detachment-Limits:** Die Matchedplay-Seite bestätigt nur: Combat Patrol = exakt 1 Patrol Detachment. Limits für Incursion/Strike Force/Onslaught stammen aus den Core Battle-Forged Rules (nicht auf der Matched Play-Seite) — Verifikation ausstehend.

### CP-Regeln

- **Start-CP:** nach Spielgröße (Tabelle oben) — dies ist der initiale Pool
- **+1 CP pro Runde:** Battle-Forged Bonus aus den Core Rules (Command Phase) — nicht im Matched Play-Kapitel geregelt, gilt aber für alle Battle-Forged Armeen in Matched Play
- CP-Kosten für Stratagems werden aus dem Pool abgezogen

### Attacker / Defender

- Beide Spieler würfeln; der Gewinner wählt seine Rolle (Attacker oder Defender).
- **Einfluss auf Deployment:** Defender deployt zuerst, Attacker zuletzt.
- Relevanz für App: Roll-off Button im Setup-Screen; Ergebnis in `session_state["attacker"]` speichern.

### Detachment-Regeln (Battle-Forged)

| Detachment | HQ | Troops | Elites | Fast Attack | Heavy Support | Flyer | Dedicated Transport | Lord of War |
|------------|----|----|--------|-------------|---------------|-------|---------------------|-------------|
| Patrol | 1–2 | 1–2 | 0–2 | 0–2 | 0–2 | 0–2 | 0–2 | — |
| Battalion | 2–3 | 3–6 | 0–6 | 0–3 | 0–3 | 0–2 | 0–3 | — |
| Brigade | 3–5 | 3–6 | 3–8 | 3–5 | 3–5 | 0–2 | 0–3 | — |
| Outrider | 1–2 | 0–3 | 0–3 | 3–6 | 0–3 | 0–2 | 0–2 | — |
| Spearhead | 1–2 | 0–3 | 0–3 | 0–3 | 3–6 | 0–2 | 0–2 | — |
| Vanguard | 1–2 | 0–3 | 3–6 | 0–3 | 0–3 | 0–2 | 0–2 | — |
| Super-Heavy | — | — | — | — | — | — | — | 1–3 |
| Super-Heavy Auxiliary | — | — | — | — | — | — | — | 1 |

Quelle: `data/wh40k_9e/_shared/detachment_types.yaml`

### Punkte-Validierung

- Roster-Gesamtpunkte müssen ≤ Spielgröße-Limit sein
- Der Setup-Screen zeigt Punkte-Zusammenfassung pro Detachment + Gesamt
- Überschreitung = Warnung (kein hartes Sperren — Open-Table-Freundlichkeit)

---

## Secondary Objectives (Matched Play)

> **Optional** — Spieler können beim Setup entscheiden, ob Secondary Objectives gespielt werden.
> Ohne Secondaries gelten nur Primary Objectives (45 VP max + optionales Battle Ready).

### Kategorien (5 Stück)

1. Purge the Enemy
2. No Mercy, No Respite
3. Battlefield Supremacy
4. Shadow Operations
5. Warpcraft

### Regeln

- Jeder Spieler wählt **3 Secondaries**, je **eine pro Kategorie** (keine zwei aus derselben Kategorie).
- Auswahl erfolgt **geheim**, dann gleichzeitig aufgedeckt.
- **VP-Cap:** max. **15 VP** pro Secondary Objective.
- Scoring-Typen: *Progressive* (während Partie) oder *End Game* (nur am Spielende).
- Gesamtmaximum: 45 VP Secondary + 45 VP Primary + 10 VP Battle Ready = **100 VP total**.

### App-Umsetzung

- Toggle im Setup-Screen: "Use Secondary Objectives" (default: off)
- Wenn aktiv: 3 Objective-Slots pro Spieler, Dropdown je Kategorie
- VP-Tracking pro Objective (0–15, nicht überschreitbar)
- Anzeige in gameActionsArea: Primary VP / Secondary VP aufgeteilt

---

## Open Play

- Keine Punktebeschränkung
- Armeewahl: beliebige Einheiten aus dem Katalog
- Start-CP: 3 pro Spieler (aus Core Rules — nicht explizit auf Wahapedia Open Play-Seite, aber konsistent mit Combat Patrol Matched Play)
- Power Level optional als Balancing-Hilfe (kein Enforcement in der App)
- Detachment-Regeln gelten nicht (kein Battle-Forged erforderlich)
- **Attacker/Defender:** Spieler mit höherem Power Level = Attacker; bei Gleichstand: Roll-off
- **Deploy-Reihenfolge:** Attacker zuerst (umgekehrt zu Matched Play)
- **Mission:** 3 Missionen je nach PL-Verhältnis (Annihilation / Hold at All Costs / Death or Glory)
- Keine Secondary Objectives

---

## Crusade

Setup-Übersicht — Details in Ziel 6.

- Jeder Spieler hat ein **Crusade Roster** mit einem Versorgungslimit (Supply Limit)
- Einheiten haben **Crusade Points** (Erfahrung, Narben, Auszeichnungen)
- Vor dem Spiel: Einheiten aus dem Crusade Roster auf die **Order of Battle** wählen
- Punktlimit der Partie bestimmt Größe der Order of Battle
- Nach dem Spiel: Crusade Points vergeben, Narben/Auszeichnungen eintragen

---

## Setup-Screen — Flow

```
1. Spielmodus wählen (Matched / Open / Crusade)
   └── Matched: Spielgröße wählen → CP-Werte setzen
               Mission wählen (Dropdown je Spielgröße)
               Secondary Objectives: Toggle on/off
                 └── wenn on: je 3 Objectives pro Spieler (1 pro Kategorie)
   └── Open:    CP = 3 (fest)
               Mission wird durch PL-Verhältnis bestimmt (kein Dropdown)
   └── Crusade: Verweis auf Ziel 6

2. Spieler 1 Roster wählen
   └── Roster aus data/rosters/ laden (Dropdown)
   └── Unmatched-Warnung anzeigen falls vorhanden

3. Spieler 2 analog

4. Attacker / Defender festlegen
   └── Matched: Roll-off Button
   └── Open: automatisch nach Power Level (oder Roll-off bei Gleichstand)

5. Startspieler festlegen (first_player)
   └── Zufalls-Button oder manuell

6. "Spiel starten" → setup_complete = True, Runde 1, Befehlsphase
```

---

## session_state Setup-Felder

```python
{
    "game_type":    Literal["matched", "open", "crusade"],
    "game_size":    Literal["patrol", "incursion", "strike_force", "onslaught"] | None,
    "mission":      str | None,                   # z.B. "Retrieval Mission"
    "attacker":     Literal["p1", "p2"] | None,
    "setup_complete": bool,
    "first_player": Literal["p1", "p2"],
    "use_secondaries": bool,                      # False = kein Secondary-Tracking
    "secondaries":  {                             # nur wenn use_secondaries=True
        "p1": [str, str, str],                    # Namen der 3 gewählten Objectives
        "p2": [str, str, str],
    } | None,
    "secondary_vp": {                             # VP pro Objective (0–15)
        "p1": [int, int, int],
        "p2": [int, int, int],
    } | None,
}
```

Roster-Zuordnung:

```python
{
    "armies": {
        "p1": {
            "faction":    str,         # z.B. "Necrons"
            "subfaction": str | None,
            "roster_path": str | None, # Pfad zur Roster-YAML, None = alle Katalog-Einheiten
            ...
        },
        "p2": { ... }
    }
}
```

---

## Offene Fragen (Ziel 5e)

| # | Frage | Impact |
|---|-------|--------|
| 1 | Roster-Auswahl UI: Dropdown aus `data/rosters/` oder Datei-Upload? | setup screen |
| 2 | Soll Punkte-Validierung hard blocken oder nur warnen? | setup flow |
| 3 | Welche Detachment-Typen sollen initial unterstützt werden (alle 8 oder nur Patrol/Battalion)? | detachment_types.yaml |
| 4 | Startspieler-Würfel: soll das App-intern gewürfelt oder manuell gesetzt werden? | setup screen |
